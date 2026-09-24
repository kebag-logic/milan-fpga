#!/usr/bin/env python3
"""R266-4 sequencing probes of scripts/act_slot_proof.sh (the collision's waits), plus a no-op control.

Usage: proof_mutants.py SOURCE OUTDIR [ID...]
Writes OUTDIR/<ID>/act_slot_proof.sh for each mutant (every edit must apply exactly
once to SOURCE, or the script refuses) and OUTDIR/<ID>/mutant.txt describing it.
"""
import pathlib
import sys

# (id, the check it removes or weakens, old text, new text)
MUTANTS = [
    ("X00", "control: a comment-only edit", "# In order, it proves:", "# In order, it proves (control):"),
    # R266-4 probes of the collision's sequencing (the documented Q32 residual)
    ("Z01", "collision rival starts without waiting for the holder to hold (sequencing only)",
     '  if ! await_holder "collide-$slot-holder" "$slot"; then\n    wait "$holder"\n    record FAIL "collision slot $slot: the holder never held the slot"\n    return\n  fi\n',
     ''),
    ("Z02", "collision judged without waiting for the holder to exit",
     '  if ended "collide-$slot-holder"; then rival_early=0; fi\n  wait "$holder"\n',
     '  if ended "collide-$slot-holder"; then rival_early=0; fi\n'),
]


def main() -> int:
    source = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    outdir = pathlib.Path(sys.argv[2])
    wanted = set(sys.argv[3:])
    for ident, described, old, new in MUTANTS:
        if wanted and ident not in wanted:
            continue
        count = source.count(old)
        if count != 1:
            print(f"{ident}: edit applies {count} times, refusing", file=sys.stderr)
            return 2
        mutant = source.replace(old, new, 1)
        if mutant == source:
            print(f"{ident}: edit changes nothing, refusing", file=sys.stderr)
            return 2
        target = outdir / ident
        target.mkdir(parents=True, exist_ok=True)
        (target / "act_slot_proof.sh").write_text(mutant, encoding="utf-8")
        (target / "mutant.txt").write_text(f"{ident}: {described}\n", encoding="utf-8")
        print(f"{ident}\t{described}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
