#!/usr/bin/env bash
set -euo pipefail
mkdir -p .git/hooks
cp hooks/pre-commit .git/hooks/pre-commit
cp hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-commit .git/hooks/pre-push
echo "Installed hooks into .git/hooks/"
