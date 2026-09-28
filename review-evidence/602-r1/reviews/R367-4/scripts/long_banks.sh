#!/usr/bin/env bash
# Usage: long_banks.sh <rv32|absent|fwcompiler|gmstep>
# Environment: REPO (candidate clone), PKT (packet dir), LITEX_PY (an
# interpreter importing the pinned migen/litex/litex_boards).
# Every disposable input lives under $PKT/scratch:
#   mdenv/     venv holding tools/markdown/requirements.txt (hash-locked) + PyYAML
#   toolbin/   'verilator' wrapper for Verilator 5.050
#   home/      HOME carrying br-milan-rv32/host from scripts/ci_rv32_sdk.py
#   home-absent/, absentbin/  HOME without the SDK and a PATH farm of /usr/bin
#                             with every riscv*-gcc candidate removed
set -u
: "${REPO:?}" "${PKT:?}" "${LITEX_PY:?}"
S=$PKT/scratch
R=$PKT/receipts
RUN=$PKT/scripts/run_gate.sh
base_path="$S/toolbin:$S/mdenv/bin"
case "${1:?mode}" in
  rv32)
    env HOME="$S/home" PATH="$base_path:/usr/local/bin:/usr/bin" MILAN_LITEX_PYTHON="$LITEX_PY" \
      VERILATOR_JOBS=2 REPO="$REPO" \
      "$RUN" "$R" builder_rv32_elab 7200 python3 sw/builder/test_builder.py --require-rv32 --require-elaboration ;;
  absent)
    mkdir -p "$S/home-absent" "$S/absentbin"
    if [ ! -e "$S/absentbin/.built" ]; then
      for f in /usr/bin/*; do
        case "${f##*/}" in riscv*-gcc|riscv*-gcc-*) continue ;; esac
        ln -sf "$f" "$S/absentbin/${f##*/}"
      done
      touch "$S/absentbin/.built"
    fi
    env HOME="$S/home-absent" PATH="$base_path:$S/absentbin" MILAN_LITEX_PYTHON="$LITEX_PY" \
      VERILATOR_JOBS=2 REPO="$REPO" \
      "$RUN" "$R" builder_absent_elab 7200 python3 sw/builder/test_builder.py --require-elaboration ;;
  fwcompiler)
    env HOME="$S/home" PATH="$base_path:/usr/local/bin:/usr/bin" REPO="$REPO" \
      "$RUN" "$R" fwcompiler_selftest 1800 python3 sw/builder/test_firmware_compiler.py --selftest
    env HOME="$S/home" PATH="$base_path:/usr/local/bin:/usr/bin" REPO="$REPO" \
      "$RUN" "$R" fwcompiler_absent 1800 python3 sw/builder/test_firmware_compiler.py --absent --audit "$R/rv32-absent.jsonl" ;;
  gmstep)
    env PATH="$base_path:/usr/local/bin:/usr/bin" VERILATOR_JOBS=4 REPO="$REPO" \
      "$RUN" "$R" gmstep_campaign 10800 make -C tb/verilator/milan_dp gmstep-mutants ;;
  *) echo "unknown mode $1" >&2; exit 2 ;;
esac
