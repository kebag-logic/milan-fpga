"""Count the AECP plant table's face defects by the test families they name."""
import sys, re
sys.path.insert(0, sys.argv[1])
import aecp_mutants as m
fams = ("Face.", "FaceLatency.", "AppFace.", "AppFaceUnacknowledged.")
face = [d for d in m.DEFECTS if any(t.startswith(fams) for t, _ in d.checks)]
core_applied = [d for d in m.DEFECTS if not any(t.startswith(fams) for t, _ in d.checks)
                and any(re.search(r"Applied|LockExpiry", t) for t, _ in d.checks)]
print("total", len(m.DEFECTS), "face-family", len(face), "core-applied-only", len(core_applied),
      "sum", len(face) + len(core_applied))
