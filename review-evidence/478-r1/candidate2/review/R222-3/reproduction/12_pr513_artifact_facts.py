#!/usr/bin/env python3
"""R222-3: fact checks of the #513 statements the combined tree relies on.

Run with the candidate scratch clone as argument (read-only use):
  1. builtin-model descriptor counts vs the gen_aem_store docstring claims
  2. KNOWN_MAP_DEVIATIONS vs the builtin model's recorded deviations
  3. docs-check steps 40-44 (CI_WORKFLOWS.md: the self-test runs just before
     the three shape gates that end the job)
  4. stale spellings anywhere tracked: "43 steps", "AUDIO_MAP[1]" allowlist
  5. RUNNING_TESTS.md: the added command sits in the builder block
Usage: 12_pr513_artifact_facts.py <scratch-cand>
"""
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "avdecc"))
import gen_aem_store as g  # noqa: E402
import yaml  # noqa: E402

names = {v: k for k, v in vars(g).items()
         if k.isupper() and isinstance(v, int) and k in (
             "ENTITY", "CONFIGURATION", "AUDIO_UNIT", "STREAM_INPUT", "STREAM_OUTPUT",
             "AVB_INTERFACE", "CLOCK_SOURCE", "CLOCK_DOMAIN", "CONTROL", "LOCALE",
             "STRINGS", "STREAM_PORT_INPUT", "STREAM_PORT_OUTPUT", "AUDIO_CLUSTER",
             "AUDIO_MAP")}
M = g.build_model(g.builtin_spec())
counts = Counter(t for t, _i, _b, _l in M["directory"])
print("1. builtin model descriptor counts:",
      {names.get(t, hex(t)): n for t, n in sorted(counts.items())})
doc = g.__doc__
for claim, typ, n in (("STREAM_INPUT x2", g.STREAM_INPUT, 2), ("CLOCK_SOURCE x2", g.CLOCK_SOURCE, 2),
                      ("AUDIO_CLUSTER x16", g.AUDIO_CLUSTER, 16), ("AUDIO_MAP x1", g.AUDIO_MAP, 1)):
    print(f"   docstring says {claim!r}: present={claim in doc} model count={counts[typ]} "
          f"{'AGREES' if counts[typ] == n else 'DISAGREES'}")
got = set(M["SMAP"]["DEVIATIONS"])
print(f"2. builtin deviations {len(got)}; KNOWN_MAP_DEVIATIONS {len(g.KNOWN_MAP_DEVIATIONS)}; "
      f"equal={got == set(g.KNOWN_MAP_DEVIATIONS)}")
wf = yaml.safe_load((root / ".github/workflows/docs.yml").read_text())
steps = wf["jobs"]["docs-check"]["steps"]
print(f"3. docs-check has {len(steps)} steps; the last five:")
for i in range(len(steps) - 5, len(steps)):
    print(f"   {i + 1:>2} {steps[i].get('name')}")
print("4. tracked-file search for stale spellings:")
for pat in ("exactly 43 steps", "carry exactly 43", "AUDIO_MAP[1] mapping"):
    out = subprocess.run(["git", "-C", str(root), "grep", "-n", "-F", pat, "HEAD", "--"],
                         capture_output=True, text=True).stdout.strip()
    print(f"   {pat!r}: {len(out.splitlines()) if out else 0} hit(s)"
          + ("".join(f"\n      {ln}" for ln in out.splitlines()[:6]) if out else ""))
rt = (root / "docs/testing/RUNNING_TESTS.md").read_text().splitlines()
i = next(k for k, ln in enumerate(rt) if "gen_aem_store.py --self-test" in ln)
print("5. RUNNING_TESTS.md block around the added command:")
for ln in rt[max(0, i - 4):i + 3]:
    print("   | " + ln)
