#!/usr/bin/env bash
# Run the candidate runner's two offline self-test forms inside an unprivileged
# bubblewrap boundary: no network, read-only host filesystem, throwaway /tmp
# and HOME, host /home hidden. Mirrors the docs.yml "Local act runner contract
# gate" step. Usage: run_act_selftests_sandboxed.sh <candidate-checkout> <out-dir>
set -u
cand="$1"; out="$2"; mkdir -p "$out"
box() {
  bwrap --unshare-all --die-with-parent --new-session \
    --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --tmpfs /home --tmpfs /run \
    --setenv HOME /tmp/home --setenv TMPDIR /tmp --setenv PYTHONDONTWRITEBYTECODE 1 \
    --unsetenv GH_TOKEN --unsetenv GITHUB_TOKEN --unsetenv SSH_AUTH_SOCK \
    --chdir "$cand" bash -c "mkdir -p /tmp/home; $1"
}
box 'python3 scripts/act_ci.py --selftest' >"$out/act_ci-selftest-ordinary.log" 2>&1; echo $? >"$out/act_ci-selftest-ordinary.rc"
box 'install_dir="$(mktemp -d)"; install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"; ls -l "$install_dir"; python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"' >"$out/act_ci-selftest-flat.log" 2>&1; echo $? >"$out/act_ci-selftest-flat.rc"
