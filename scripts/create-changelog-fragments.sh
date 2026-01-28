#!/bin/bash

# Check if both arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <last_version_tag> <next_version_tag>"
    exit 1
fi

LAST_VERSION=$1
NEXT_VERSION=$2

# Define the Regex for Conventional Commits
# This captures the 'type' in the first group
CONV_REGEX="^([a-z]+)(\([^)]+\))?!?: (.*)"

echo "Processing commits from $LAST_VERSION to HEAD for release $NEXT_VERSION..."

# Get commits between the earlier version and current HEAD
COMMITS=$(git log "${LAST_VERSION}..HEAD" --pretty=format:"%s")

# Create fragments directory if it doesn't exist
mkdir -p changelogs/fragments

# Iterate through commits using a custom delimiter
IFS=$'\n'
for SUBJECT in $(echo "$COMMITS"); do

    if [[ -z "$SUBJECT" ]] || [[ "$SUBJECT" == "chore"* ]] || [[ "$SUBJECT" == "Merge pull request"* ]]; then
        continue
    fi

    # Extract the type and the remaining message
    if [[ "$SUBJECT" =~ $CONV_REGEX ]]; then
        # BASH_REMATCH[1] is the 'type' (e.g., feat, fix)
        COMMIT_TYPE="${BASH_REMATCH[1]}"
        # BASH_REMATCH[3] is the rest of the message after ': '
        SUBJECT="${BASH_REMATCH[3]}"
    else
        COMMIT_TYPE="unknown"
    fi

    # Using printf and a here-string to prevent injection
    SUBJECT=$(sed -E \
    -e 's/\[(skip ci|ci skip|no ci|skip actions|actions skip)\]//g' \
    -e 's/^[[:space:]]*//' \
    -e 's/[[:space:]]*$//' <<< "$SUBJECT")

    # Define a safe filename based on the subject
    SAFE_NAME=$(echo "$SUBJECT" | tr -dc '[:alnum:]' | cut -c1-30)
    FILE_PATH="changelogs/fragments/${NEXT_VERSION}_${COMMIT_TYPE}_${SAFE_NAME}.yml"

    # Categorize based on Conventional Commits (see https://www.conventionalcommits.org/en/v1.0.0/#summary)
    if [[ "$COMMIT_TYPE" == *"!: "* ]]; then
        CATEGORY="breaking_changes"
    elif [[ "$COMMIT_TYPE" == feat* ]]; then
        CATEGORY="minor_changes"
    elif [[ "$COMMIT_TYPE" == fix* ]]; then
        CATEGORY="bugfixes"
    elif [[ "$COMMIT_TYPE" == docs* ]]; then
        CATEGORY="doc_changes"
    elif [[ "$COMMIT_TYPE" == perf* ]]; then
        CATEGORY="known_issues"
    else
        continue
    fi

    # Write the fragment
    cat <<EOF > "$FILE_PATH"
$CATEGORY:
  - "${SUBJECT}"
EOF

done

echo "Done! Fragments for $NEXT_VERSION generated."