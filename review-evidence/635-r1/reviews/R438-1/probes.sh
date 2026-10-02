#!/bin/bash
# probes.sh <lane>: disposable fault probes on the review clone; each restores its file from the index.
# Prints one PROBE line per probe: name, the command's rc, and the expected-to-fail verdict.
cd $REVIEWS/r438-1-635 || exit 99
export PATH=$REVIEWS/635-r438-1-packet/scratch/bin:$PATH
B=cdf49d1a28527562888f0a903de51b6b15b1244f
probe() { # name file mutate-cmd check-cmd expect(fail|pass)
  local name=$1 file=$2 mut=$3 chk=$4 exp=$5 rc
  bash -c "$mut" || { echo "PROBE $name MUTATION-NOT-APPLIED"; git checkout -- "$file"; return; }
  git diff --quiet -- "$file" && { echo "PROBE $name MUTATION-NO-CHANGE"; return; }
  bash -c "$chk" > "$REVIEWS/635-r438-1-packet/logs/probe_$name.log" 2>&1; rc=$?
  git checkout -- "$file"
  if [ "$exp" = fail ]; then v=$([ $rc -ne 0 ] && echo DETECTED || echo SURVIVED); else v=$([ $rc -eq 0 ] && echo PASSES || echo FAILS); fi
  echo "PROBE $name rc=$rc expect=$exp verdict=$v"
}
case $1 in
hdl)
  probe drop_identify_tie hdl/milan/KL_pp_shadow.sv "sed -i '/\.identify_button_i   (1.b0),/d' hdl/milan/KL_pp_shadow.sv" "python3 scripts/lint_rtl.py --check" fail
  probe identify_tie_one hdl/milan/KL_pp_shadow.sv "sed -i 's/\.identify_button_i   (1.b0),/.identify_button_i   (1'\"'\"'b1),/' hdl/milan/KL_pp_shadow.sv" "python3 scripts/lint_rtl.py --check && python3 scripts/check_port_contracts.py" pass
  probe en_identify_one hdl/milan/KL_pp_shadow.sv "sed -i 's/\.EN_IDENTIFY_NOTIF_P (1.b0)/.EN_IDENTIFY_NOTIF_P (1'\"'\"'b1)/' hdl/milan/KL_pp_shadow.sv" "python3 scripts/lint_rtl.py --check && python3 scripts/check_port_contracts.py" pass
  ;;
evidence)
  probe drop_acmp_disposition scripts/measure_test_evidence.py "python3 - <<'P'
import re;p='scripts/measure_test_evidence.py';s=open(p).read()
s2=re.sub(r'    \"protocol-processor/tb/pp_top/acmp_mutants.py\":\n(?:        \"[^\n]*\n)+','',s,count=1);assert s2!=s;open(p,'w').write(s2)
P" "python3 scripts/measure_test_evidence.py --check" fail
  probe drop_notify_disposition scripts/measure_test_evidence.py "python3 - <<'P'
import re;p='scripts/measure_test_evidence.py';s=open(p).read()
s2=re.sub(r'    \"protocol-processor/tb/pp_top/notify_mutants.py\":\n(?:        \"[^\n]*\n)+','',s,count=1);assert s2!=s;open(p,'w').write(s2)
P" "python3 scripts/measure_test_evidence.py --check" fail
  ;;
records)
  probe rom_row_wrong syn/yosys/rom_digests.tsv "sed -i 's/^\(631eeb342ca1e3fa80e734077a56a943aee76ff1\tucode.hex\t\)518b/\10000/' syn/yosys/rom_digests.tsv" "cd syn/yosys && timeout 300 ./ooc.sh KL_render_setpoint" fail
  probe rom_rows_base syn/yosys/rom_digests.tsv "git show $B:syn/yosys/rom_digests.tsv > syn/yosys/rom_digests.tsv" "cd syn/yosys && timeout 300 ./ooc.sh KL_render_setpoint" fail
  probe submodules_base_row docs/reference/SUBMODULES.md "git show $B:docs/reference/SUBMODULES.md > docs/reference/SUBMODULES.md" "python3 scripts/check_submodule_docs.py" fail
  probe diagram_base_svg docs/diagrams/submodule_boundaries.svg "git show $B:docs/diagrams/submodule_boundaries.svg > docs/diagrams/submodule_boundaries.svg" "python3 docs/diagrams/submodule_boundaries.gen.py --check" fail
  ;;
budgets)
  probe ports_budget_base scripts/port_docs.budget "git show $B:scripts/port_docs.budget > scripts/port_docs.budget" "python3 scripts/check_port_contracts.py" fail
  probe naming_budget_base scripts/naming.budget "git show $B:scripts/naming.budget > scripts/naming.budget" "python3 scripts/measure_naming.py --check" fail
  ;;
esac
