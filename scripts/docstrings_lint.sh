#!/bin/bash
# required in order to get the status of all the files at once
if command -v uvx >/dev/null 2>&1; then
  DARGLINT=(uvx darglint==1.5.8)
  PYDOCSTYLE=(uvx pydocstyle==5.1.1)
else
  python -m pip install --quiet darglint==1.5.8 pydocstyle==5.1.1
  DARGLINT=(darglint)
  PYDOCSTYLE=(pydocstyle)
fi
echo ====================================================================================
echo DOCSTRINGS LINT: checking $CHANGED_FILES
echo ------------------------------------------------------------------------------------
echo 'removing files under /tests...'
arrVar=()
# we ignore tests files
for changed_file in $CHANGED_FILES; do
  case ${changed_file} in
    tests/* | \
    .github/* | \
    scripts/* | \
    fastentrypoints.py | \
    gptc/helloworld/* | \
    gptc/proto/* | \
    gptc/resources/* | \
    gptc/serve/consensus/add_voter/* | \
    docs/* | \
    setup.py)
    ;;*)
      echo keeping ${changed_file}
      arrVar+=(${changed_file})
    ;;
  esac
done

# if array is empty
if [ ${#arrVar[@]} -eq 0 ]; then
  echo 'nothing to check'
  exit 0
fi

DARGLINT_OUTPUT=$("${DARGLINT[@]}" -v 2 -s sphinx "${arrVar[@]}"); PYDOCSTYLE_OUTPUT=$("${PYDOCSTYLE[@]}" --select=D101,D102,D103 "${arrVar[@]}")
# status captured here
if [[ -z "$PYDOCSTYLE_OUTPUT" ]] && [[ -z "$DARGLINT_OUTPUT" ]]; then
  echo 'OK'
  exit 0
else
  echo 'failure. make sure to check the guide for pre-commit hooks: https://github.com/gpt-computer/gptc/blob/master/CONTRIBUTING.md#install-pre-commit-hooks'
  echo $DARGLINT_OUTPUT
  echo $PYDOCSTYLE_OUTPUT
  exit 1
fi
echo ====================================================================================
