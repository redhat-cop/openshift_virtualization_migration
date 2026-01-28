#!/bin/bash -eu

LAST_VERSION=$(semantic-release version --print-last-released)
NEXT_VERSION=$(semantic-release version --print)

# Create fragments based on commit messages
. ./scripts/create-changelog-fragments.sh $LAST_VERSION $NEXT_VERSION

export ANSIBLE_COLLECTIONS_PATH=.

# Lint fragments
antsibull-changelog lint && echo "✅ All changelog fragments passed linting!" || exit 1

# Run antsibull-changelog release to update changelog and delete fragments
antsibull-changelog release -v --version $NEXT_VERSION

echo "✅ Changelog updated successfully!"