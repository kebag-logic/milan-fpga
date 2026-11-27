# Reviewer scripts (R955-1)

All scripts run from a tree extracted with `git archive 5d03517f2ab42416654a8f2be2f71cfc51d82440`
(`scratch/tree`) and a clone holding both merge parents. Set `TOOLS` before sourcing `env.sh`.

| Script | Purpose |
|---|---|
| `run_gates.sh TREE OUT` | GCC build and tests with coverage, Clang 18 sanitizer build, mutation campaign, RV32 gate, concurrently (16 jobs). |
| `run_gates2.sh TREE OUT` | Re-run of the mutation campaign and of the sanitizer arm with the host Clang (Clang 18 cannot parse the host's GCC 16 libstdc++). |
| `probes_gen.py`, `probes2_gen.py` | Generate reviewer probe mutants for the new paths in `src/acmp.c`. |
| `probes_run.py TREE BASELINE PROBES WORK OUT JOBS` | Run each probe against the `acmp`, `acmp_wide` and `acmp_walk` arms, reusing the head campaign's baseline test objects. |
| `diff_gen.py TREE OUT` | Build a base-versus-head differential from the head's walk test: base core (a795471c `src/acmp.c`, prefixed `old_`) against the core under test. |
| `diff_run.py TREE DIFF PROBES NAMES OUT JOBS MAX_SINKS` | Build and run the differential for the head and for chosen probes. |
| `merge_check.sh` | Show that the merge brings in only main's content. |
