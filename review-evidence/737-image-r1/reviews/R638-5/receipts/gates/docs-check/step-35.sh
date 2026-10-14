python3 scripts/act_ci.py --selftest
install_dir="$(mktemp -d)"
trap 'rm -rf "$install_dir"' EXIT
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$GITHUB_WORKSPACE"
