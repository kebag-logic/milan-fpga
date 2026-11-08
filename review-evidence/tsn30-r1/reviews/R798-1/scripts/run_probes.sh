#!/usr/bin/env bash
# Portable review probes for the privacy-gate exemption of PR #30.
# Usage: run_probes.sh <clone> <packet>
# Runs the gate at the exact head and on main, mutation probes on the exemption,
# and an end-to-end synthetic-history probe. Only disposable copies under
# <packet>/scratch are modified; the clone is only read.
set -u
CLONE=$(cd "$1" && pwd)
PKT=$(cd "$2" && pwd)
HEAD_ID=62d24a37c4b81a78edda2721dd8611d753b2bc8e
HEAD_TREE=39369307e99aab4c06f6b47e4bbd1d0f25c413d0
BASE=d7e6a2a19a57a8277cd26042557a8c99f2ee5496
S=$PKT/scratch
R=$PKT/receipts
mkdir -p "$S" "$R"
export GIT_CONFIG_NOSYSTEM=1 HOME=$S/home
mkdir -p "$HOME"
git config --global commit.gpgsign false
git config --global init.defaultBranch main
git config --global advice.detachedHead false

run() { # label, cwd, cmd...
  local label=$1 dir=$2; shift 2
  echo "\$ ($label) $*"
  (cd "$dir" && "$@") 2>&1
  echo "rc=$?"
}

{
echo "## identity"
git -C "$CLONE" rev-parse HEAD 'HEAD^{tree}'
git -C "$CLONE" status --porcelain=v1 --untracked-files=all | sed 's/^/status: /'
python3 --version
git --version
echo "## commits in the reviewed range"
git -C "$CLONE" log --format='%H parents=%P%n  author=%an <%ae>%n  committer=%cn <%ce>' "$BASE^1..$HEAD_ID"
echo "## merge tree equals second parent tree"
git -C "$CLONE" rev-parse "$BASE^{tree}" "$BASE^2^{tree}"
echo "## files changed by the PR"
git -C "$CLONE" diff --stat "$BASE" "$HEAD_ID"
echo "## non-ASCII bytes added by the PR (expect none)"
git -C "$CLONE" diff "$BASE" "$HEAD_ID" | grep '^+' | LC_ALL=C grep -nP '[^\x09\x20-\x7e]' || echo none
} > "$R/00-identity.txt"

# Disposable copies: head and main.
rm -rf "$S/head" "$S/main"
git clone -q --no-hardlinks "$CLONE" "$S/head" && git -C "$S/head" checkout -q "$HEAD_ID"
git clone -q --no-hardlinks "$CLONE" "$S/main" && git -C "$S/main" checkout -q "$BASE"

{
echo "## gate at exact head (in the clone, read-only)"
run head-selftest "$CLONE" python3 -B scripts/check_privacy.py --selftest
run head-gate "$CLONE" python3 -B scripts/check_privacy.py
run head-license "$CLONE" python3 -B scripts/check_license.py
run head-license-selftest "$CLONE" python3 -B scripts/check_license.py --selftest
echo "## main d7e6a2a1 with its own gate (expect fail on the merge)"
run main-selftest "$S/main" python3 -B scripts/check_privacy.py --selftest
run main-gate "$S/main" python3 -B scripts/check_privacy.py
echo "## main d7e6a2a1 history with the head gate (expect pass)"
cp "$CLONE/scripts/check_privacy.py" "$S/main/scripts/check_privacy.py"
run main-with-head-gate "$S/main" python3 -B scripts/check_privacy.py
git -C "$S/main" checkout -q -- scripts/check_privacy.py
echo "## head history with the main gate (expect fail on the merge only)"
git -C "$S/head" show "$BASE:scripts/check_privacy.py" > "$S/head/scripts/check_privacy.py"
run head-with-main-gate "$S/head" python3 -B scripts/check_privacy.py
git -C "$S/head" checkout -q -- scripts/check_privacy.py
} > "$R/01-gates.txt"

# Mutation probes on the selftest. Each mutant edits a disposable copy only.
mutate() { # name, python-expression-free replace via python
  local name=$1 old=$2 new=$3 mode=${4:-selftest}
  git -C "$S/head" checkout -q -- scripts/check_privacy.py
  python3 -I - "$S/head/scripts/check_privacy.py" "$old" "$new" <<'EOF'
import sys
path, old, new = sys.argv[1:]
text = open(path).read()
assert text.count(old) == 1, ("anchor count", text.count(old), old)
open(path, "w").write(text.replace(old, new))
EOF
  echo "### $name"
  git -C "$S/head" diff --unified=0 -- scripts/check_privacy.py | grep '^[-+][^-+]'
  if [ "$mode" = selftest ]; then
    run "$name" "$S/head" python3 -B scripts/check_privacy.py --selftest
  else
    run "$name-selftest" "$S/head" python3 -B scripts/check_privacy.py --selftest
    run "$name-gate" "$S/head" python3 -B scripts/check_privacy.py
  fi
}
{
echo "## mutation probes (killed = selftest rc 1 naming the expected control)"
mutate M1-drop-exemption "commit != OWNER_SQUASH and commit not in TWO_LINE_MERGES and len(" "commit != OWNER_SQUASH and len("
mutate M2-exempt-identity-too "    if commit != OWNER_SQUASH and not identity_ok(lines):" "    if commit != OWNER_SQUASH and commit not in TWO_LINE_MERGES and not identity_ok(lines):"
mutate M3-prefix-8 "commit not in TWO_LINE_MERGES and len(" "not any(commit.startswith(m[:8]) for m in TWO_LINE_MERGES) and len("
mutate M4-prefix-39 "commit not in TWO_LINE_MERGES and len(" "commit[:39] not in {m[:39] for m in TWO_LINE_MERGES} and len("
mutate M5-match-merge-subject "commit not in TWO_LINE_MERGES and len(" "not lines[2:3] == ['Merge (#29)'] and len("
mutate M6-exempt-every-web-flow "commit not in TWO_LINE_MERGES and len(" "lines[:2] != WEB_FLOW and len("
mutate M7-drop-near-miss-derivation "        commit = commit[:-1] + (\"0\" if commit[-1] != \"0\" else \"1\") if name.endswith(\"near-miss\") else commit
" ""
mutate M8-skip-content-scan-for-merge "        errors += scan(commit, data)
" "        errors += [] if commit in TWO_LINE_MERGES else scan(commit, data)
" both
mutate M9-skip-identity-in-main "        errors += commit_errors(commit, lines)
" "        errors += [e for e in commit_errors(commit, lines) if not (commit in TWO_LINE_MERGES and 'identity' in e)]
" both
git -C "$S/head" checkout -q -- scripts/check_privacy.py
git -C "$S/head" status --porcelain=v1
} > "$R/02-mutations.txt"

# End-to-end probe: synthetic history where a listed two-paragraph commit
# carries restricted content or a foreign identity. The listed id is patched
# into a working-tree copy of the head gate after the commit exists.
synth() { # name, author-name, author-email, committer-name, committer-email, body
  local name=$1 an=$2 ae=$3 cn=$4 ce=$5 body=$6 d=$S/synth-$1
  rm -rf "$d"; git init -q "$d"; mkdir -p "$d/scripts"
  cp "$CLONE/scripts/check_privacy.py" "$d/scripts/"
  (cd "$d" && git add scripts && GIT_AUTHOR_NAME=hackerman-kl GIT_AUTHOR_EMAIL=hackerman-kl@kebag-logic.com \
     GIT_COMMITTER_NAME=hackerman-kl GIT_COMMITTER_EMAIL=hackerman-kl@kebag-logic.com git commit -q -m "Base")
  (cd "$d" && GIT_AUTHOR_NAME=$an GIT_AUTHOR_EMAIL=$ae GIT_COMMITTER_NAME=$cn GIT_COMMITTER_EMAIL=$ce \
     git commit -q --allow-empty -m "Merge pull request #1: subject" -m "$body")
  local id; id=$(git -C "$d" rev-parse HEAD)
  python3 -I - "$d/scripts/check_privacy.py" "$id" <<'EOF'
import sys
path, cid = sys.argv[1:]
text = open(path).read()
old = 'TWO_LINE_MERGES = {"d7e6a2a19a57a8277cd26042557a8c99f2ee5496"}'
assert text.count(old) == 1
open(path, "w").write(text.replace(old, 'TWO_LINE_MERGES = {"' + cid + '"}'))
EOF
  echo "### $name (listed id $id)"
  run "$name" "$d" python3 -B scripts/check_privacy.py
}
PLANT="see /""tmp""/x for the log"
{
echo "## synthetic end-to-end probes of the exemption inside main()"
synth S1-clean "hackerman-kl" "161579364+Mister-M-alt@users.noreply.github.com" "GitHub" "noreply@github.com" "Clean body"
synth S2-restricted-body "hackerman-kl" "161579364+Mister-M-alt@users.noreply.github.com" "GitHub" "noreply@github.com" "$PLANT"
synth S3-foreign-identity "someone" "a@b.c" "someone" "a@b.c" "Clean body"
} > "$R/03-synthetic.txt"

{
echo "## clone integrity after probes"
git -C "$CLONE" rev-parse HEAD 'HEAD^{tree}'
echo "expected $HEAD_ID $HEAD_TREE"
git -C "$CLONE" status --porcelain=v1 --untracked-files=all --ignored | sed 's/^/status: /'
echo "status lines: $(git -C "$CLONE" status --porcelain=v1 --untracked-files=all --ignored | wc -l)"
git -C "$CLONE" diff-index --cached --quiet HEAD && echo "index matches HEAD"
git -C "$CLONE" diff --quiet && echo "worktree matches index"
echo "write-tree: $(git -C "$CLONE" write-tree)"
echo "gitlinks (mode 160000): $(git -C "$CLONE" ls-files -s | awk '$1==160000' | wc -l)"
echo "ls-files -s sha256: $(git -C "$CLONE" ls-files -s | sha256sum | cut -d' ' -f1)"
echo "ls-tree -r HEAD sha256: $(git -C "$CLONE" ls-tree -r HEAD | sha256sum | cut -d' ' -f1)"
} > "$R/04-integrity.txt"
echo done
