#!/usr/bin/env bash
# docsyml_all.sh <head>: every job of .github/workflows/docs.yml at <head>, each on its own fresh clone through
# run_docs_yml.py, then verify_docs_yml.py over the whole step list. Writes <root>/verify.txt and verify.rc.
set -u
H=$1; here=$(cd "$(dirname "$0")" && pwd); R=$VALIDATION_STORAGE/scratch/854-a756c/docsyml-${H:0:8}${RUN:+-$RUN}
PY=$VALIDATION_STORAGE/scratch/854-a756/venv-docs/bin/python3
mkdir -p "$R"
for job in $($PY -c "import yaml,subprocess; t=subprocess.run(['git','-C','$LANES/854-shadow-drops','show','$H:.github/workflows/docs.yml'],capture_output=True,text=True,check=True).stdout; print(' '.join(yaml.safe_load(t)['jobs']))"); do
  $PY "$here/run_docs_yml.py" "$H" "$job" "$R" > "$R/$job.runner.log" 2>&1
  echo "$job runner rc=$?" >> "$R/progress.txt"
done
$PY "$here/verify_docs_yml.py" "$H" "$R" > "$R/verify.txt" 2>&1
echo $? > "$R/verify.rc"
