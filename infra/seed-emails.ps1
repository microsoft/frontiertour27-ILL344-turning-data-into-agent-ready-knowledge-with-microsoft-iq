<#
.SYNOPSIS
    Seeds sample emails into the lab user's mailbox via Microsoft Graph API.
.DESCRIPTION
    Uses the service principal's app-only token to create the emails directly in the
    lab user's Inbox as received (non-draft) messages, then verifies they exist.
    This bypasses Exchange mail transport, which can silently drop sendMail requests
    in new lab tenants even though Graph returns 202 Accepted.

    Requires Mail.ReadWrite application permission (admin-consented). If the token only
    has Mail.Send, the script falls back to sendMail and saves a copy in Sent Items.
    Delivery is then checked only if the token can read mail.

    Every step is logged (service principal identity and roles, mailbox readiness,
    Graph errors with request IDs, and a final mailbox summary) for lab troubleshooting.
.PARAMETER UserUpn
    The lab user's UPN (email) to send messages to/from.
.PARAMETER TenantId
    The Entra tenant ID for token acquisition.
.PARAMETER ClientId
    The service principal's app/client ID.
.PARAMETER ClientSecret
    The service principal's client secret.
#>
param(
    [Parameter(Mandatory)][string]$UserUpn,
    [Parameter(Mandatory)][string]$TenantId,
    [Parameter(Mandatory)][string]$ClientId,
    [Parameter(Mandatory)][string]$ClientSecret
)

$ErrorActionPreference = "Stop"

function Log {
    param([string]$msg)
    # Write-Host (not Write-Output) so log lines inside functions don't leak into return values.
    # The lifecycle runs this script as a child powershell process, so host output still reaches its log file.
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
}

# Get an app-only token for Microsoft Graph
function Get-GraphToken {
    $body = @{
        grant_type    = "client_credentials"
        client_id     = $ClientId
        client_secret = $ClientSecret
        scope         = "https://graph.microsoft.com/.default"
    }
    $response = Invoke-RestMethod -Method POST `
        -Uri "https://login.microsoftonline.com/$TenantId/oauth2/v2.0/token" `
        -ContentType "application/x-www-form-urlencoded" `
        -Body $body
    return $response.access_token
}

function Get-TokenClaims {
    param([string]$Token)
    $payload = $Token.Split('.')[1].Replace('-', '+').Replace('_', '/')
    switch ($payload.Length % 4) { 2 { $payload += '==' } 3 { $payload += '=' } }
    return [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payload)) | ConvertFrom-Json
}

function Get-RequestId {
    param($ErrorRecord)
    try {
        $headers = $ErrorRecord.Exception.Response.Headers
        if ($headers -is [System.Net.WebHeaderCollection]) { return $headers['request-id'] }
        return ($headers.GetValues('request-id') | Select-Object -First 1)
    } catch {
        return "n/a"
    }
}

function Get-ErrorBody {
    param($ErrorRecord)
    if ($ErrorRecord.ErrorDetails -and $ErrorRecord.ErrorDetails.Message) {
        return $ErrorRecord.ErrorDetails.Message
    }
    if ($ErrorRecord.Exception.Response) {
        try {
            $reader = New-Object System.IO.StreamReader($ErrorRecord.Exception.Response.GetResponseStream())
            $body = $reader.ReadToEnd()
            $reader.Close()
            return $body
        } catch { }
    }
    return $ErrorRecord.Exception.Message
}

function Invoke-Graph {
    param(
        [string]$Method,
        [string]$Url,
        $Body = $null,
        [int]$Attempts = 3
    )
    $headers = @{
        Authorization  = "Bearer $script:GraphToken"
        "Content-Type" = "application/json; charset=utf-8"
    }
    for ($attempt = 1; $attempt -le $Attempts; $attempt++) {
        try {
            if ($null -ne $Body) {
                $json = $Body | ConvertTo-Json -Depth 10
                return Invoke-RestMethod -Method $Method -Uri $Url -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -TimeoutSec 60
            }
            return Invoke-RestMethod -Method $Method -Uri $Url -Headers $headers -TimeoutSec 60
        } catch {
            $status = [int]$_.Exception.Response.StatusCode
            Log "Graph $Method $($Url.Split('?')[0]) attempt $attempt/$Attempts failed (HTTP $status, request-id $(Get-RequestId $_)): $(Get-ErrorBody $_)"
            if ($attempt -lt $Attempts) { Start-Sleep -Seconds 5 }
        }
    }
    throw "Graph $Method $Url failed after $Attempts attempts"
}

# A newly provisioned lab mailbox can take several minutes before Graph can reach it.
function Wait-ForMailbox {
    param([string]$UserId, [int]$TimeoutMinutes = 15)
    $url = "https://graph.microsoft.com/v1.0/users/$UserId/mailFolders/inbox?`$select=id,totalItemCount"
    $started = Get-Date
    $deadline = $started.AddMinutes($TimeoutMinutes)
    $check = 0
    while ($true) {
        $check++
        try {
            $inbox = Invoke-Graph -Method GET -Url $url -Attempts 1
            Log "Mailbox check $check succeeded after $([int]((Get-Date) - $started).TotalSeconds)s"
            return $inbox
        } catch {
            if ((Get-Date) -ge $deadline) {
                throw "Mailbox for $UserId was not reachable within $TimeoutMinutes minutes ($check checks)"
            }
            Log "Mailbox check $check failed, retrying in 30 seconds (gives up after $TimeoutMinutes minutes)..."
            Start-Sleep -Seconds 30
        }
    }
}

function Find-InboxMessage {
    param([string]$UserId, [string]$Subject, [string]$Folder = "inbox")
    $escaped = $Subject.Replace("'", "''")
    $filter = [uri]::EscapeDataString("subject eq '$escaped'")
    $url = "https://graph.microsoft.com/v1.0/users/$UserId/mailFolders/$Folder/messages?`$filter=$filter&`$select=id,subject,isDraft,isRead,receivedDateTime"
    $result = Invoke-Graph -Method GET -Url $url
    return @($result.value)
}

function Format-Message {
    param($Message)
    return "received $($Message.receivedDateTime), isDraft=$($Message.isDraft), isRead=$($Message.isRead), id ...$($Message.id.Substring([Math]::Max(0, $Message.id.Length - 12)))"
}

# Log where each seeded subject is, so the lifecycle log shows the final mailbox state.
function Write-MailboxSummary {
    param([string]$UserId, [string[]]$Folders)
    Log "--- Mailbox summary ---"
    foreach ($email in $emails) {
        foreach ($folder in $Folders) {
            try {
                $found = @(Find-InboxMessage -UserId $UserId -Subject $email.subject -Folder $folder)
                Log "[$folder] $($found.Count) x '$($email.subject)'"
                foreach ($message in $found) { Log "    $(Format-Message $message)" }
            } catch {
                Log "[$folder] could not read mailbox: $($_.Exception.Message)"
                return
            }
        }
    }
}

# Create the email directly in the Inbox. MAPI extended properties set the delivery
# and submit times and clear the draft flag, so Outlook shows it as received mail.
function New-InboxMessage {
    param([string]$UserId, [hashtable]$Mail, [datetime]$ReceivedUtc)
    $timestamp = $ReceivedUtc.ToString("yyyy-MM-ddTHH:mm:ssZ")
    $message = @{}
    foreach ($key in $Mail.Keys) { $message[$key] = $Mail[$key] }
    $message.sender = $Mail.from
    $message.singleValueExtendedProperties = @(
        @{ id = "SystemTime 0x0E06"; value = $timestamp },
        @{ id = "SystemTime 0x0039"; value = $timestamp },
        @{ id = "Integer 0x0E07"; value = "1" }
    )
    $created = Invoke-Graph -Method POST -Url "https://graph.microsoft.com/v1.0/users/$UserId/mailFolders/inbox/messages" -Body $message
    # 0x0E07 = 1 also marks the message read. Reset it so it looks new in Outlook.
    Invoke-Graph -Method PATCH -Url "https://graph.microsoft.com/v1.0/users/$UserId/messages/$($created.id)" -Body @{ isRead = $false } | Out-Null
    return $created
}

function Send-MailFallback {
    param([string]$UserId, [hashtable]$Mail)
    Invoke-Graph -Method POST -Url "https://graph.microsoft.com/v1.0/users/$UserId/sendMail" -Body @{ message = $Mail; saveToSentItems = $true } | Out-Null
}

# ============================================================
# Email definitions
# ============================================================

$emails = @(
    @{
        subject      = "CALD-201 transfer checkpoint - equipment mapping approval needed"
        from         = @{ emailAddress = @{ name = "Elena Morris"; address = $UserUpn } }
        toRecipients = @(
            @{ emailAddress = @{ name = "Me"; address = $UserUpn } }
        )
        body         = @{
            contentType = "HTML"
            content     = @"
<p>Hi,</p>
<p>Summit Dose has completed the controlled document intake for <strong>CALD-201</strong> and sent its draft equipment map. One action remains open: Caldova Process Engineering must approve the proposed high-shear granulator equivalency by <strong>4 February 2027</strong>.</p>
<p>If we miss that approval date, Summit Dose says the engineering batch slot will move from 15 February to 1 March. That would put the 31 March technology-transfer package at risk.</p>
<p>Owner: Daniel Cho, Process Engineering. Please confirm whether he can close the equivalency review this week.</p>
<p>Thanks,<br/>Elena Morris<br/>Technology Transfer Lead</p>
"@
        }
    },
    @{
        subject      = "CALD-201 testing subcontractor - Piedmont evidence incomplete"
        from         = @{ emailAddress = @{ name = "Noor Patel"; address = $UserUpn } }
        toRecipients = @(
            @{ emailAddress = @{ name = "Me"; address = $UserUpn } }
        )
        body         = @{
            contentType = "HTML"
            content     = @"
<p>Hi,</p>
<p>Supplier Quality reviewed Summit Dose's qualification package for <strong>Piedmont Analytical Services</strong>, the proposed compendial microbiology testing subcontractor for CALD-201.</p>
<p>The package is still missing the closure evidence from Piedmont's 2026 data-integrity audit and the method-transfer validation summary. <strong>Caldova has not granted written subcontractor approval.</strong></p>
<p>Summit Dose owes both documents by 3 February. Supplier Quality will make the approval decision at the 6 February review. Until then, no release testing may be assigned to Piedmont.</p>
<p>Thanks,<br/>Noor Patel<br/>Supplier Quality Manager</p>
"@
        }
    },
    @{
        subject      = "Decision Friday: protect the CALD-201 April delivery"
        from         = @{ emailAddress = @{ name = "Luis Ortega"; address = $UserUpn } }
        toRecipients = @(
            @{ emailAddress = @{ name = "Me"; address = $UserUpn } }
        )
        body         = @{
            contentType = "HTML"
            content     = @"
<p>Hi team,</p>
<p>Summit Dose reported that planned coating-line maintenance now overlaps the <strong>CALD201-SD-PPQ-01</strong> window. They can still target the 30 April delivery if Caldova authorizes a reserved weekend coating slot by Friday.</p>
<p>Without that slot, Summit Dose's current estimate moves PPQ-01 release to 12 May. The alternative would also require us to rephase PPQ-02.</p>
<p>Thursday's supply review needs to decide whether to authorize the weekend slot or accept the delay and start formal change control. This email is a planning update, not an amendment to the approved purchase order.</p>
<p>Thanks,<br/>Luis Ortega<br/>Supply Planning Director</p>
"@
        }
    }
)

# ============================================================
# Main
# ============================================================

Log "=== Email seeding started ==="
Log "Target mailbox: $UserUpn | Tenant: $TenantId | Client ID: $ClientId | PowerShell $($PSVersionTable.PSVersion)"

try {
    $script:GraphToken = Get-GraphToken
} catch {
    Log "FAILED: could not acquire Graph token: $(Get-ErrorBody $_)"
    exit 1
}
$claims = Get-TokenClaims $script:GraphToken
$roles = @($claims.roles)
$expires = [DateTimeOffset]::FromUnixTimeSeconds([long]$claims.exp).UtcDateTime.ToString("u")
Log "Graph token for app '$($claims.app_displayname)' (appid $($claims.appid), tenant $($claims.tid)), expires $expires"
Log "Graph application roles ($($roles.Count)): $(($roles | Sort-Object) -join ', ')"
foreach ($role in @("Mail.ReadWrite", "Mail.Read", "Mail.Send")) {
    Log "  $role : $(if ($roles -contains $role) { 'YES' } else { 'no' })"
}

if ($roles -notcontains "Mail.ReadWrite") {
    Log "WARNING: Token lacks Mail.ReadWrite, so emails cannot be created in the Inbox."
    Log "Falling back to sendMail with a Sent Items copy. Exchange can still drop delivery after Graph returns 202."
    if ($roles -notcontains "Mail.Send") {
        Log "FAILED: Token lacks Mail.Send too. Ask Skillable to grant Mail.ReadWrite (application) with admin consent."
        exit 1
    }
    $failed = 0
    foreach ($email in $emails) {
        try {
            Send-MailFallback -UserId $UserUpn -Mail $email
            Log "Submitted via sendMail (Graph 202, delivery not confirmed): $($email.subject)"
        } catch {
            Log "FAILED sendMail: $($email.subject) - $($_.Exception.Message)"
            $failed++
        }
        Start-Sleep -Seconds 1
    }
    if ($roles -contains "Mail.Read") {
        Log "Waiting 60 seconds for delivery before checking the mailbox..."
        Start-Sleep -Seconds 60
        Write-MailboxSummary -UserId $UserUpn -Folders @("inbox", "sentitems", "junkemail")
    } else {
        Log "Token lacks Mail.Read, so delivery cannot be checked. Grant Mail.ReadWrite to seed and verify reliably."
    }
    Log "=== Email seeding finished (unverified, $failed submit failure(s)) ==="
    if ($failed -gt 0) { exit 1 }
    exit 0
}

try {
    $inbox = Wait-ForMailbox -UserId $UserUpn
} catch {
    Log "FAILED: $($_.Exception.Message)"
    exit 1
}
Log "Mailbox reachable (Inbox items before seeding: $($inbox.totalItemCount))"

$failed = 0
$receivedUtc = (Get-Date).ToUniversalTime().AddHours(-$emails.Count)
foreach ($email in $emails) {
    $receivedUtc = $receivedUtc.AddHours(1)
    try {
        $existing = @(Find-InboxMessage -UserId $UserUpn -Subject $email.subject)
        if ($existing.Count -gt 0) {
            Log "Already in Inbox, skipping: $($email.subject) ($(Format-Message $existing[0]))"
            continue
        }
        Log "Creating in Inbox (received $($receivedUtc.ToString('u'))): $($email.subject)"
        New-InboxMessage -UserId $UserUpn -Mail $email -ReceivedUtc $receivedUtc | Out-Null
        $found = @(Find-InboxMessage -UserId $UserUpn -Subject $email.subject)
        if ($found.Count -gt 0 -and -not $found[0].isDraft) {
            Log "Verified in Inbox: $($email.subject) ($(Format-Message $found[0]))"
        } elseif ($found.Count -gt 0) {
            Log "FAILED verification (created as draft): $($email.subject) ($(Format-Message $found[0]))"
            $failed++
        } else {
            Log "FAILED verification (not found after create): $($email.subject)"
            $failed++
        }
    } catch {
        Log "FAILED: $($email.subject) - $($_.Exception.Message)"
        $failed++
    }
}

Write-MailboxSummary -UserId $UserUpn -Folders @("inbox")

if ($failed -gt 0) {
    Log "=== Email seeding finished with $failed failure(s) ==="
    exit 1
}
Log "=== Email seeding complete and verified ==="
