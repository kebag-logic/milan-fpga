"""Run one shard of tb/verilator/gptp_tables/mutants.py with its own logic.

Usage: python3 mutants_shard.py REPO SHARD NSHARDS
Imports the committed driver, keeps MUTATIONS entries i with i % NSHARDS ==
SHARD, prints which entries it owns, and calls the driver's own main().
Nothing in the driver (inputs, copier, verdict) is changed.
"""
import sys
from pathlib import Path

repo, shard, n = Path(sys.argv[1]).resolve(), int(sys.argv[2]), int(sys.argv[3])
suite = repo / "tb" / "verilator" / "gptp_tables"
sys.path.insert(0, str(suite))
sys.argv = [str(suite / "mutants.py")]
import mutants  # noqa: E402

full = list(mutants.MUTATIONS)
mine = [row for i, row in enumerate(full) if i % n == shard]
print(f"shard {shard}/{n}: {len(mine)} of {len(full)} controls: "
      + ", ".join(row[0] for row in mine), flush=True)
mutants.MUTATIONS[:] = mine
sys.exit(mutants.main())
