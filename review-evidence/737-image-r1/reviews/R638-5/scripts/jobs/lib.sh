# step runner: each step body runs in bash --noprofile --norc -eo pipefail, rc recorded
OUT=/out/$JOB; mkdir -p "$OUT"; : > "$OUT/rc.tsv"
mkdir -p "$HOME" "$RUNNER_TEMP"
step() { local name="$1"; shift; N=$((N+1)); local f="$OUT/step-$(printf %02d $N).sh"; printf '%s\n' "$*" > "$f";
  local t0=$(date +%s); bash --noprofile --norc -eo pipefail "$f" > "$OUT/$(basename $f .sh).log" 2>&1; local rc=$?;
  printf '%s\t%s\t%ss\t%s\n' "$rc" "$name" "$(( $(date +%s)-t0 ))" "$(basename $f)" >> "$OUT/rc.tsv"; }
N=0
rv32() { step "rv32-link+verify" 'mkdir -p "$HOME/br-milan-rv32"; [ -e "$HOME/br-milan-rv32/host" ] || ln -s /opt/rv32-sdk "$HOME/br-milan-rv32/host"; "$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc" --version | head -1
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"'; }
gtest() { step "gtest-versions" 'dpkg-query -W libgtest-dev libgmock-dev
g++ --version | head -n 1
gcov --version | head -n 1
python3 -c "import yaml; print(yaml.__version__)"'; }
