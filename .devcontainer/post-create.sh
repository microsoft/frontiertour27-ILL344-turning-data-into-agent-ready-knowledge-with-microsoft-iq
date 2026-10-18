#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

for command_name in git az azd python3 uv; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        printf 'Missing required command: %s. Rebuild the dev container.\n' "$command_name" >&2
        exit 1
    fi
done

if [[ -e .venv ]]; then
    if [[ ! -x .venv/bin/python ]]; then
        printf 'The existing .venv is not usable in this container. Rename it on the host and rebuild the dev container.\n' >&2
        exit 1
    fi
    .venv/bin/python -c 'import sys; sys.exit("Python 3.13 is required. Rename .venv and rebuild the dev container.") if sys.version_info[:2] != (3, 13) else None'
fi

uv venv --python 3.13 --seed --allow-existing .venv
uv pip install --python .venv/bin/python --requirement src/notebooks/requirements.txt
uv pip check --python .venv/bin/python

printf '\nILL344 development environment ready.\n'
printf 'Next: follow deploy_yourself.md, starting with azd auth login and azd up.\n'
printf 'No Azure login or provisioning has been performed.\n'