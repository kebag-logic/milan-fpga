"""Bounded partial-revert controls; a no-op is a potential counterexample."""
import itertools
import json
import pathlib
import subprocess
import sys
import tempfile

count = 0
hits = []
statuses = {}
with tempfile.TemporaryDirectory() as td:
    paths = [pathlib.Path(td) / n for n in ("tip", "base", "branch")]
    for length in range(3, 9):
        for seq in itertools.product((b"a\n", b"b\n"), repeat=length):
            for left, right in itertools.combinations(range(length), 2):
                # Two deletions; restore one and append a separated extension.
                base = b"".join(seq)
                branch = b"".join(x for i, x in enumerate(seq) if i not in (left, right))
                tip = b"".join(x for i, x in enumerate(seq) if i != right) + b"tail\n"
                for path, data in zip(paths, (tip, base, branch)):
                    path.write_bytes(data)
                p = subprocess.run(["git", "merge-file", "-p", "-q", *map(str, paths)], capture_output=True)
                if not 0 <= p.returncode <= 127:
                    raise RuntimeError(f"unmeasurable raw merge: {p.returncode} {p.stderr!r}")
                statuses[p.returncode] = statuses.get(p.returncode, 0) + 1
                count += 1
                if p.returncode == 0 and p.stdout == tip:
                    hits.append(dict(base=base.decode(), branch=branch.decode(), tip=tip.decode(), left=left, right=right))
                    break
            if hits:
                break
        if hits:
            break
    original = b"".join(f"line {i}\n".encode() for i in range(40))
    source = original.replace(b"line 5\n", b"source 5\n")
    retained = source.replace(b"line 35\n", b"later 35\n")
    for path, data in zip(paths, (retained, original, source)):
        path.write_bytes(data)
    p = subprocess.run(["git", "merge-file", "-p", "-q", *map(str, paths)], capture_output=True)
    assert p.returncode == 0 and p.stdout == retained, "raw positive control failed"
print(json.dumps(dict(cases=count, returncodes=statuses, positive_control=True,
                      no_op_partial_reverts=hits), indent=2))
sys.exit(bool(hits))
