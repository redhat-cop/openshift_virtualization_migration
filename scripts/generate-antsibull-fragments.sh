#!/bin/bash

# Check if both arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <earlier_version_tag> <new_version_number>"
    exit 1
fi

EARLIER_VER=$1
NEW_VER=$2

echo "Processing commits from $EARLIER_VER to HEAD for release $NEW_VER..."

# 1. Get commits between the earlier version and current HEAD
# We use %s for the subject and %b for the body (to catch breaking change notes)
COMMITS=$(git log "${EARLIER_VER}..HEAD" --pretty=format:"%s|%b%n---END_COMMIT---")

# Create fragments directory if it doesn't exist
mkdir -p changelogs/fragments

# 2. Iterate through commits using a custom delimiter
IFS=$'\n'
for COMMIT_DATA in $(echo "$COMMITS" | awk 'BEGIN{RS="---END_COMMIT---"} {print}'); do
    # Extract subject and body
    SUBJECT=$(echo "$COMMIT_DATA" | cut -d'|' -f1 | xargs)
    BODY=$(echo "$COMMIT_DATA" | cut -d'|' -f2-)

    if [[ -z "$SUBJECT" ]] || [[ "$SUBJECT" == "chore"* ]]; then
        continue
    fi

    # Define a safe filename based on the subject
    SAFE_NAME=$(echo "$SUBJECT" | tr -dc '[:alnum:]' | cut -c1-30)
    FILE_PATH="changelogs/fragments/${NEW_VER}_${SAFE_NAME}.yml"

    # 3. Categorize based on Conventional Commits
    if [[ "$SUBJECT" == *"!"* ]] || [[ "$BODY" == "BREAKING CHANGE"* ]]; then
        CATEGORY="breaking_changes"
    elif [[ "$SUBJECT" == fix* ]]; then
        CATEGORY="bugfixes"
    elif [[ "$SUBJECT" == feat* ]]; then
        CATEGORY="minor_changes"
    elif [[ "$SUBJECT" == doc* ]]; then
        CATEGORY="documentation"
    else
        CATEGORY="minor_changes"
    fi

    # 4. Write the fragment
    cat <<EOF > "$FILE_PATH"
$CATEGORY:
  - "${SUBJECT}"
EOF

done

echo "Done! Fragments for $NEW_VER generated."