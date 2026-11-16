#!/usr/bin/env bash
# Disposable probes for #917 round 3. Usage: probes.sh <clean checkout at the reviewed head> <scratch dir>
set -u
SRC=$1; S=$2
rm -rf "$S/p1" "$S/p2" "$S/p3" "$S/p4"
for p in p1 p2 p3 p4; do mkdir -p "$S/$p"; git -C "$SRC" archive HEAD | tar -x -C "$S/$p"; done
echo "== P1: aecp refill_ms 5 -> 10, --check then --write then --check"
cd "$S/p1"
grep -n "refill_ms: 5" sw/mailbox/mailbox.yaml
python3 - <<'PY'
import re,pathlib
p=pathlib.Path('sw/mailbox/mailbox.yaml'); t=p.read_text()
lines=t.split('\n'); out=[]; inaecp=False; done=False
for ln in lines:
    if re.match(r'\s*-?\s*name:\s*aecp\b', ln): inaecp=True
    if inaecp and not done and 'refill_ms: 5' in ln:
        ln=ln.replace('refill_ms: 5','refill_ms: 10'); done=True
    out.append(ln)
assert done
p.write_text('\n'.join(out))
PY
grep -n "refill_ms" sw/mailbox/mailbox.yaml
python3 -I sw/mailbox/gen_mailbox.py --check 2>&1 | grep -i "FR_NFR"; echo "check rc=${PIPESTATUS[0]}"
python3 -I sw/mailbox/gen_mailbox.py --write 2>&1 | tail -3; echo "write rc=${PIPESTATUS[0]}"
sed -n '/response-margins:start/,/response-margins:end/p' docs/reference/FR_NFR.md
python3 -I sw/mailbox/gen_mailbox.py --check > /dev/null 2>&1; echo "recheck rc=$?"
echo "== P2: follows_hold boundary mutant (cycle < held_at instead of <=)"
cd "$S/p2/tb/verilator/ctrl_service_budget"
sed -i 's/    if cycle <= held_at:/    if cycle < held_at:/' held.py; grep -n "cycle < held_at" held.py
python3 - <<'PY'
import sys; sys.path.insert(0,'.')
import selftest as st, selftest_held as sh, grade, scenario
probe = scenario.Probe('s.held.if0','READ_DESCRIPTOR held','aecp',f'rxh:{sh.AECP}',[f'resp:{sh.AECP}:7d00'])
response = st.tx_record(sh.AECP,0,st.aem_response(scenario.CTL1,0x7D00,0x0004),0,700_000)
lines=['MARK 1000 s.held.if0','RXS 1000 0 60 s.held.if0','RXE 1059',f'RXH 1070 {sh.AECP}',f'RXR 1070 {sh.AECP}',*response]
print('same-clock RXR under mutant:', repr(sh.refused_by(st,lines,probe)) or 'GRADED')
res=[(n,ok) for n,ok,_ in sh.held_checks(st)]
print('held_checks failing under mutant:', [n for n,ok in res if not ok] or 'NONE (boundary mutant escapes)')
PY
echo "== P2b: same-clock RXR at the reviewed head"
cd "$S/p4/tb/verilator/ctrl_service_budget"
python3 - <<'PY'
import sys; sys.path.insert(0,'.')
import selftest as st, selftest_held as sh, scenario
probe = scenario.Probe('s.held.if0','READ_DESCRIPTOR held','aecp',f'rxh:{sh.AECP}',[f'resp:{sh.AECP}:7d00'])
response = st.tx_record(sh.AECP,0,st.aem_response(scenario.CTL1,0x7D00,0x0004),0,700_000)
lines=['MARK 1000 s.held.if0','RXS 1000 0 60 s.held.if0','RXE 1059',f'RXH 1070 {sh.AECP}',f'RXR 1070 {sh.AECP}',*response]
print('same-clock RXR at head:', sh.refused_by(st,lines,probe) or 'GRADED')
PY
echo "== P3: margin positivity boundary mutant (< 0 instead of <= 0); zero-margin plant"
cd "$S/p3"
python3 - <<'PY'
import sys; sys.path[:0]=['sw/mailbox']
import mailbox_margins as mm
from mailbox_model import load
c=load(); page=open(mm.PAGE).read()
row=next(l for l in mm.split_page(page)[1][2:] if '`acmp`' in l)
cells=mm.row_cells(row); cells[2]='27 ms'   # held margin 27-20-1-6 = 0
z=page.replace(row,'| '+' | '.join(cells)+' |',1)
z=mm.splice(c,z)
print('head, zero margin:', [f for f in mm.findings(c,z) if 'no margin' in f])
PY
sed -i 's/if int(cell.split()\[0\]) <= 0\]/if int(cell.split()[0]) < 0]/' sw/mailbox/mailbox_margins.py; grep -n "< 0\]" sw/mailbox/mailbox_margins.py
python3 -I sw/mailbox/gen_mailbox.py --selftest > sel.log 2>&1; echo "selftest under <0 mutant rc=$?"; grep -n "not positive" sel.log
