set -euo pipefail
echo "<scratch>/optverilator/bin" >> "$GITHUB_PATH"
<scratch>/optverilator/bin/verilator --version
<scratch>/optverilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"
