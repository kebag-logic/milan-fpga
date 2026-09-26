#!/usr/bin/env bash
# Harmless real-binary probe: shows which mode the host's passt multi-call
# binary selects when reached by the runner's SAFE_PATH lookup spelling
# versus its resolved target. Only --version and an option-parse failure run;
# no namespace, network or privilege is touched.
# Usage: real_multicall_probe.sh <clone>
set -u
cd "$1" || exit 2
spelling=$(python3 -I -c '
import importlib.util, sys
spec = importlib.util.spec_from_file_location("act_ci", "scripts/act_ci.py")
m = importlib.util.module_from_spec(spec); sys.modules["act_ci"] = m; spec.loader.exec_module(m)
print(m.require_tool("pasta"))')
resolved=$(readlink -f "$spelling")
echo "require_tool(pasta) = $spelling"
echo "resolved target     = $resolved"
echo "## invoked by lookup spelling"
"$spelling" --version 2>&1 | head -1
echo "## invoked by resolved target"
"$resolved" --version 2>&1 | head -1
echo "## resolved target given a pasta-only option (parse failure only)"
timeout 5 "$resolved" --netns-only --help >/dev/null 2>"${TMPDIR:-/tmp}/r267-probe.err"
echo "rc=$?"
head -1 "${TMPDIR:-/tmp}/r267-probe.err"
rm -f "${TMPDIR:-/tmp}/r267-probe.err"
