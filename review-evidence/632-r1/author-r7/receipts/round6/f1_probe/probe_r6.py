#!/usr/bin/env python3
"""The R677-3 partial-late probe phase, the same three PDUs, inserted into the
round-6 harness before its own [behind] phase, each declared late (the round-6
harness checks the late count against the phases' declarations).
usage: probe_r6.py <sim_main.cpp>"""
import sys
from pathlib import Path
p = Path(sys.argv[1])
s = p.read_text()
anchor = "        behind_phase();\n"
block = '''        phase_ = "latepart";        // PROBE: first event's timestamp before the latest event (d < 0), later events on time
        {
            Pdu p;
            p.stream = 0; p.pdu = ++pdu_id_; p.frame_off = -1; p.refusal = Pdu::Refusal::kLate;
            frame({p});
            run_frames(20);
            Pdu q;
            q.stream = 0; q.pdu = ++pdu_id_; q.frame_off = 0; q.phi = -0.3; q.refusal = Pdu::Refusal::kLate;
            frame({q});
            run_frames(20);
            Pdu r;                  // control: d >= 0, the same frames late as q
            r.stream = 0; r.pdu = ++pdu_id_; r.frame_off = 0; r.phi = 0.3; r.refusal = Pdu::Refusal::kLate;
            frame({r});
            run_frames(140);
        }

'''
assert s.count(anchor) == 1
p.write_text(s.replace(anchor, block + anchor))
