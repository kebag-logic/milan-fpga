#!/bin/bash
# Each load-gate plant can fail: break the gate one way in a copy of load_grade.py and require the matching control
# to report it escaped; mutation 0 is the gate unchanged, which must report none. usage: meta_plants25.sh CHECKOUT SCRATCH
set -u
C=$1 M=$2
mkdir -p "$M"
for i in 0 1 2 3 3b 4 5 6 7 8 8b 9 9b 10; do
    cp "$C/tb/verilator/ctrl_service_budget/load_grade.py" "$M/load_grade.py"
    python3 - "$M/load_grade.py" "$i" <<'PY'
import sys; p, i = sys.argv[1], sys.argv[2]; t = open(p).read()
m = {'0': ("", ""),
     '1': ("        if total > top:\n", "        if False:\n"),
     '2': ("    c = dict((table or GRADED)[point])\n", "    c = {**GRADED['8x8/2if'], **(table or GRADED)[point]}\n"),
     '3': ("    out['srp'] = c['record.srp'] / refill['srp'] + c['item.retained'] / k['tick_ms']\n",
           "    out['srp'] = c['record.srp'] / refill['srp']\n"),
     '3b': ("    out['srp'] = c['record.srp'] / refill['srp'] + c['item.retained'] / k['tick_ms']\n",
            "    out['srp'] = (c['record.srp'] + c['item.retained']) / refill['srp']\n"),
     '4': ("    acmp = c['event.ACMP'] * s['sinks_per_if'] / no_resp\n", "    acmp = c['event.ACMP'] * 8 / no_resp\n"),
     '5': ("    return sorted(set(terms) - documented())\n", "    return []\n"),
     '6': ("    out = {f'rec.{ch}': c[f'record.{ch}'] / refill[ch] for ch in ('aecp', 'acmp', 'adp', 'maap')}\n",
           "    out = {f'rec.{ch}': c[f'record.{ch}'] / {'aecp': 5, 'acmp': 5, 'adp': 10, 'maap': 20}[ch]"
           " for ch in ('aecp', 'acmp', 'adp', 'maap')}\n"),
     '7': ("    out = [name for name, (path, line) in RETRY_RULE.items() if line not in folded(path)]\n",
           "    out = []\n"),
     '8': ("    out['item.aecp'] = record_frame / refill['aecp'] + n_if * s['registrations'] * c['item.aecp.probe'] / probe\n",
           "    out['item.aecp'] = c['item.aecp.notice'] * (1 / refill['aecp'] + n_if * s['registrations'] / probe)\n"),
     '8b': ("    out['item.aecp'] = record_frame / refill['aecp'] + n_if * s['registrations'] * c['item.aecp.probe'] / probe\n",
            "    out['item.aecp'] = record_frame * (1 / refill['aecp'] + n_if * s['registrations'] / probe)\n"),
     '9': ("                donor.get(key, pin[key]) < pin[key]]\n", "                False]\n"),
     '9b': ("GRADED = STATED_US_DONOR\n", "GRADED = STATED_US\n"),
     '10': ("CEILING = {'1x1/1if': 0.70, '8x8/2if': 0.70}\n", "CEILING = {'8x8/2if': 0.70}\n")}[i]
assert m[0] in t, i; open(p, 'w').write(t.replace(m[0], m[1]))
PY
    (cd "$M" && python3 -B -c "
import sys, pathlib; sys.path[:0] = ['.', '$C/tb/verilator/ctrl_service_budget']
import load_grade as L; r = pathlib.Path('$C'); print('mutation $i escaped:', L.controls(r) + L.period_controls(r))")
done
