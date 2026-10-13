#!/usr/bin/env bash
# Execute the exact docs.yml "Local act runner contract gate" body (read with a
# YAML parser) inside the same bubblewrap boundary as run_act_selftests_sandboxed.sh,
# on <checkout>.  Usage: run_docs_step_mutation.sh <checkout> <log> <rcfile> <python-with-yaml>
set -u
ck="$1"; log="$2"; rcf="$3"; py="$4"
body="$("$py" -I -c 'import sys,yaml; d=yaml.safe_load(open(sys.argv[1])); s=[x for j in d["jobs"].values() for x in j.get("steps",[]) if x.get("name")=="Local act runner contract gate"]; assert len(s)==1; print(s[0]["run"])' "$ck/.github/workflows/docs.yml")"
printf '%s\n' "$body" > "$log.body"
bwrap --unshare-all --die-with-parent --new-session \
  --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --tmpfs /home --tmpfs /run \
  --setenv HOME /tmp/home --setenv TMPDIR /tmp --setenv PYTHONDONTWRITEBYTECODE 1 \
  --setenv GITHUB_WORKSPACE "$ck" --unsetenv GH_TOKEN --unsetenv GITHUB_TOKEN --unsetenv SSH_AUTH_SOCK \
  --chdir "$ck" bash --noprofile --norc -e -c "mkdir -p /tmp/home; $body" >"$log" 2>&1
echo $? > "$rcf"
