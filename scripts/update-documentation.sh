#!/bin/bash -eu

DOCSIBLE_ROLE_TEMPLATE="./scripts/docsible-role-template.md"
DOCSIBLE_COLLECTION_TEMPLATE="./scripts/docsible-collection-template.md"
ROLE_LIST_GENERATOR="./scripts/generate-role-list.py"

# Document collection and roles
# Note: We backup the README to preserve manual edits
touch README.md
mv README.md README.md.bkp

echo "Running docsible collection generation"
docsible --collection . --no-backup --no-docsible --graph --append \
  --md-collection-template ${DOCSIBLE_COLLECTION_TEMPLATE} \
  --md-template ${DOCSIBLE_ROLE_TEMPLATE} \
  | tee -a collection-build.log

# Restore original README to preserve manual content
mv README.md.bkp README.md

# Generate role list from metadata
echo "Generating role list from role metadata..."
ROLE_LIST_FILE=$(mktemp)
python3 ${ROLE_LIST_GENERATOR} > "${ROLE_LIST_FILE}"

# Injecting role list into Roles section
echo "Building Roles section..."
README_TMP=$(mktemp)
awk '
  /<!--ROLES_LIST_START-->/ {
    print $0
    while ((getline line < "'"${ROLE_LIST_FILE}"'") > 0) {
      print line
    }
    close("'"${ROLE_LIST_FILE}"'")
    in_roles=1
    next
  }
  /<!--ROLES_LIST_END-->/ {
    in_roles=0
  }
  !in_roles { print }
' README.md > "${README_TMP}"
mv "${README_TMP}" README.md
rm -f "${README_TMP}" "${ROLE_LIST_FILE}"

# Generate/update TOC in README.md (in-place, GitHub flavor)
echo "Generating table of contents for README.md"
md_toc --in-place github README.md

echo "Documentation update complete!"
