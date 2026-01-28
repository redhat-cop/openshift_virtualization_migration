#!/bin/bash -eu

DOCSIBLE_ROLE_TEMPLATE="./scripts/docsible-role-template.md"
DOCSIBLE_COLLECTION_TEMPLATE="./scripts/docsible-collection-template.md"

# Document roles
# for dir in $(ls -d roles/*); do
#   echo "Running docsible role generation against ${dir}"
#   docsible --md-template ${DOCSIBLE_ROLE_TEMPLATE} \
#     --role ${dir} --no-backup --no-docsible --graph --append | tee -a collection-build.log
#   # git add ${dir}/README.md
# done

# Document collection and roles
touch README.md
mv README.md README.md.bkp
echo "Running docsible collection generation"
docsible --collection . --no-backup --no-docsible --graph --append \
  --md-collection-template ${DOCSIBLE_COLLECTION_TEMPLATE} \
  --md-template ${DOCSIBLE_ROLE_TEMPLATE} \
  | tee -a collection-build.log
mv README.md.bkp README.md

# git add README.md
# for dir in $(ls -d roles/*); do
#   git add ${dir}/README.md
# done
