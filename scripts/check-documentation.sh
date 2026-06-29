#!/bin/bash -eu
#
# Pre-commit hook script to verify documentation is up-to-date
# This checks if README.md or any role READMEs have uncommitted changes
# after running update-documentation.sh
#

if ! git diff --exit-code --quiet README.md roles/*/README.md 2>/dev/null; then
  echo ""
  echo "❌ Documentation is out of date!"
  echo ""
  echo "Changed files:"
  git diff --name-only README.md roles/*/README.md 2>/dev/null | sed "s/^/  - /"
  echo ""
  echo "The pre-commit hook regenerated documentation, but it differs from what is committed."
  echo "This means your changes affected the auto-generated docs."
  echo ""
  echo "The changes have been applied to your working directory."
  echo "Please review and stage them:"
  echo ""
  echo "  git add README.md roles/*/README.md"
  echo ""
  exit 1
fi

echo "✓ Documentation is up to date"
exit 0
