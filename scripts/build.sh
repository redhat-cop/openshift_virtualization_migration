#!/bin/bash -eu

export PYTHON_REQUIREMENTS="requirements-ci.txt"

# Install extra python dependencies if defined
if [ -f "${PYTHON_REQUIREMENTS}" ]; then
  # Set the pip version
  if [[ $(which pip3) ]]; then
      export PIP_EXEC=$(which pip3)
  elif [[ $(which pip) ]]; then
      export PIP_EXEC=$(which pip)
  else
      echo "Pip not found"
      exit 1
  fi
  $PIP_EXEC install -r ${PYTHON_REQUIREMENTS}
fi

. ./scripts/update-documentation.sh

. ./scripts/update-changelog.sh

ansible-galaxy collection build .

git add .
