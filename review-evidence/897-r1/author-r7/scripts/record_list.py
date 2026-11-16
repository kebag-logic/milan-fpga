#!/usr/bin/env python3
"""Every AECP record of a leg's groups (record_classes.read_leg of TREE): its group, start, CPU cycles, cost by the
rule, command, status and response control_data_length; then each GET_AS_PATH response frame the leg's aecp channel
carries, decoded (IEEE 1722.1-2021 7.4.41.2: descriptor_index, count, the path's ClockIdentities), with the
interface it answers, its sequence_id and its control_data_length. usage: record_list.py TREE RESULTS_DIR..."""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import record_classes as rc  # noqa: E402
import scenario  # noqa: E402
for d in map(Path, sys.argv[2:]):
    leg, spec = rc.read_leg(d)
    print(f'== {d.parent.name}/{d.name}: {leg.point} {leg.variant}')
    for g in sorted(leg.groups):
        for r in leg.groups[g]:
            name = rc.NAMED.get(r.command, f'0x{r.command:04x}' if r.command is not None else 'unanswered')
            print(f'  {g} start {r.start / leg.sys_hz * 1e3:10.3f} ms  {r.cycles:>7,} cycles {rc.rule(r.cycles, leg.cpu_hz):>5} us'
                  f'  command {name} status {r.status} control_data_length {r.length}')
    aecp = scenario.CH['aecp']
    for log in sorted(d.glob('*.log')):
        text = log.read_text(errors='replace')
        if 'RESULT' not in text[-4000:]:
            continue
        parsed = grade.parse(text[:text.rfind('\n') + 1], leg.sys_hz, leg.cpu_hz)
        for c, ch, port, fr in parsed.tx:
            if ch != aecp or len(fr) < 42 or not fr[15] & 1 or (fr[36] << 8 | fr[37]) & 0x7FFF != rc.GET_AS_PATH:
                continue
            cdl = (fr[16] << 8 | fr[17]) & 0x7FF
            count = fr[40] << 8 | fr[41]
            ids = [fr[42 + 8 * k:50 + 8 * k].hex() for k in range(count) if 50 + 8 * k <= len(fr)]
            print(f'  {log.stem} GET_AS_PATH response at {c / leg.sys_hz * 1e3:.3f} ms on port {port}: status {fr[16] >> 3}, '
                  f'sequence_id {fr[34] << 8 | fr[35]}, unsolicited {bool(fr[36] & 0x80)}, descriptor_index {fr[38] << 8 | fr[39]}, '
                  f'count {count}, control_data_length {cdl} (16 + 8 x {count} = {16 + 8 * count}), frame {len(fr)} B, '
                  f'entries {" ".join(ids)}')
