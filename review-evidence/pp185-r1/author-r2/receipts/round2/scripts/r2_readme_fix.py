"""Round 2: the README mutation records the full head campaigns moved (applied to the
lane tree after every head campaign finished; each edit must match once)."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
EDITS = {
    "tb/pp_top/README.md": [
        ("`rd-str-short-guard-nop` 1 to 5 (after RD4's unanswered read, RDC6's SET_CONTROL,",
         "`rd-str-short-guard-nop` 1 to 5 (after RD4's unanswered read, RDC6's SET_CONTROL,"),
        ("`lk-sctrl-lock-nop` 12 to 13 (RDC1's premise: the foreign SET_CONTROL(0) was\n"
         "stored), `rd-tail-uncut` 9 to 16 (the seven overlaid RDC reads) and",
         "`lk-sctrl-lock-nop` 12 to 13 (RDC1's premise: the foreign SET_CONTROL(0) was\n"
         "stored), `rd-tail-uncut` 9 to 16 (the seven overlaid RDC reads; 17 with round\n"
         "2's RDC7 read, IDENTIFY again) and"),
        ("now also fail RDC7's last read, IDENTIFY again (7 to 8).",
         "now also fail RDC7's last read, IDENTIFY again (7 to 8), and so does the uncut\n"
         "TAIL (`rd-tail-uncut`, 16 to 17)."),
    ],
    "tb/aecp_notify/README.md": [
        ("| `occupancy_reset_set` | the reset sets the occupancy | OC1 | 17: TS1, TS3, TW1, TW2, DR1, DR1b, DR2, DR2b, DR3, LF1, LF2, LF3, CQ1, CQ1b, CQ2, CQ2b, OC1 |",
         "| `occupancy_reset_set` | the reset sets the occupancy | OC1 | 32: TS1, TS3, TW1, TW2, DR1, DR1b, DR2, DR2b, DR3, LF1, LF2, LF3, LC0, LC1 (8), LC2 to LC7, CQ1, CQ1b, CQ2, CQ2b, OC1 |"),
        ("`occupancy_push_unseen` and `occupancy_reset_set` also fail section LF's checks\n"
         "(issue #186): LF holds a SET_NAME round, which goes through the queue.",
         "`occupancy_push_unseen` and `occupancy_reset_set` also fail section LF's checks\n"
         "(issue #186): LF holds a SET_NAME round, which goes through the queue.\n"
         "`occupancy_reset_set` also fails every section LC check but its REGISTERs (15,\n"
         "issue #186 round 2): after each warm reset the set occupancy makes the pick\n"
         "claim an empty queue entry before the lock round, so the first job is not a\n"
         "lock job."),
    ],
}
for rel, edits in EDITS.items():
    p = root / rel
    s = p.read_text(encoding="utf-8")
    for old, new in edits:
        if old == new:
            continue
        assert s.count(old) == 1, (rel, old[:60], s.count(old))
        s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("edited", rel)
