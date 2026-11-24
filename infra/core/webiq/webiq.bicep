targetScope = 'resourceGroup'

@description('Web IQ account name.')
param name string

@description('Web IQ SKU.')
param skuName string = 'G3'

@description('Tags applied to the account.')
param tags object = {}

// Web IQ accounts are global, regardless of the resource group's region.
resource webIq 'Microsoft.WebIQ/accounts@2026-06-01-preview' = {
  name: name
  location: 'global'
  tags: tags
  kind: 'WebIQ.Grounding'
  sku: {
    name: skuName
  }
  properties: {}
}

output id string = webIq.id
output name string = webIq.name
