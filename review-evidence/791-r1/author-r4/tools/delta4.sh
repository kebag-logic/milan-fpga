#!/usr/bin/env bash
# delta4.sh <chain>: round 4's gates on clean clones of the final head 6a5acf06, each rc beside its log.
# chain a: the Python idiom gate and its self-test, test_ctrl_memory.py, git diff --check against the merge base.
# chain b: the region-decode simulation's self-test.
# chain c: the all-fabric compare, the manager's sync merge 77e1efa0 against the final head, every shipped config.
set -u
S=/data-2/milan/tmp/791-a765c; F=$S/r4; C=$S/clones; PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
T=$MANAGEMENT/2026-09-23/791-a765c/tools
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0 PATH=$WORKSPACE_HOME/br-milan-rv32/host/bin:$PATH
mkdir -p "$F"
step() { local name=$1 cl=$2; shift 2; echo "$(date +%T) start $name"; ( cd "$cl" && "$@" ) > "$F/$name.log" 2>&1; local rc=$?; echo $rc > "$F/$name.rc"; echo "$(date +%T) $name rc $rc"; }
case $1 in
  a)
    step py-idiom "$C/head4" python3 scripts/check_py_idiom.py
    step py-idiom-selftest "$C/head4" python3 scripts/check_py_idiom.py --selftest
    rm -rf "$F/tcm-tmp"; mkdir -p "$F/tcm-tmp"; step tcm "$C/head4" env TMPDIR="$F/tcm-tmp" "$PY" -B sw/litex/test_ctrl_memory.py
    step diff-check "$C/head4" git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD ;;
  b)
    rm -rf "$F/region-self"; step region-self-test "$C/head4" "$PY" -B tb/verilator/ctrl_region_decode/run.py --build-dir "$F/region-self" --self-test ;;
  c)
    rm -rf "$S/allfabric4" "$F/allfabric-receipt"; step allfabric "$S" "$PY" "$T/allfabric_compare.py" "$C/base4" "$C/head4-af" "$S/allfabric4" "$F/allfabric-receipt" ;;
esac
echo "$(date +%T) chain $1 done"
