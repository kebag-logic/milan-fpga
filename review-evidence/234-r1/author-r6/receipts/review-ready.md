[A516] REVIEW READY (round 6, tests only)
Commit: `d5f56313dc5a5c2716211356f99796664dc843dd` on local branch `234-area-baseline`. That is three one-line commits on round 5's `ec7eb2d8`: no rebase, no amend, and not pushed, as assigned. `ec7eb2d8..d5f56313` touches 2 files, the gate's self-test and its mutants (+55 / -37). `pp_resource_gate.py` is byte-identical to round 5, so every reviewer mutant span still applies. No gate, docs, RTL, processor, interface, workflow, baseline-JSON or policy change, and no Vivado run.

Changed, by assignment item (5971250916):
1. List items past the first (R447-5 F1).
   - The fixture's image manifest has three entries.
   - Two new arms run through `main()`, each requiring exit 2:
     - `check` with a bracketed key `x[1]` in the last of the three manifest entries ("... in /2");
     - the same key in item 2 of a note list (`measured`), through `check` and `check-baseline` ("... in /endpoints/route/measured/2").
   - The generator's `note` operator puts its key at list index 0 to 3. `entry key` picks any entry, now one of three.
   - The fixture's `runs` note list has three items, so every key operator also reaches items past the first.
   - Mutant `names past a list's first item` (R447-5's replacement) is shipped and killed.
   - Verification, as given: R447-5's `probe_r5_namekill.py`, unchanged, gives "walk visits only the first item of a list" selftest DETECTED, rc 1. The generated cases alone also detect it: 8 failures in 500 cases, 76 in 5,000. R447-5's `probe_r5_names.py` gives 72 of 72.
2. Suggestions taken:
   - R447-5 S1: an exit-0 `check` arm with a 128-character key holding every character of the class (`A-Z a-z 0-9 _ . : / -`), in a `measured` note and a manifest entry. Nine shipped mutants each narrow the class by one group, or to 127 characters. All nine are killed; the round-5 self-test missed five (`.`, `:`, `/`, `-` and the length).
   - R447-5 S2: an exit-2 arm with a `description` note shaped as a record's scopes, `{"x": {"record": {"scopes": {"a[1]": 1}}}}`, through both commands. It kills two shipped mutants: the scope path matched on its last two keys, and `SCOPES` with any first key.
3. Not taken: R447-5 S3 (the walk's memory) and S4 (R447-4 S1 and S2). All three are listed as open in the PR body's limitations.

The self-test was at 999 of the 1,000 lines `check_py_idiom.py` allows. The first commit, `c7cde331`, folds it onto 16 fewer lines without changing behaviour: a docstring rewrap, joined string literals, one-call file writes and shared FF-growth plants. At that commit the self-test still gives 254 arms and round 5's case digest `bec87b3c7cbe1125`, and the campaign gives 162 of 162. The self-test is now exactly 1,000 lines.

Validation at `d5f56313`, worktree clean:
- Gates: 43 of 43 rc 0, with GNU Make 4.3 first on PATH and no pipes. They include:
  - the gate self-test: 260 arms and 500 generated cases;
  - the mutant campaign: 174 of 174 killed, control passes;
  - `check-baseline`: 3 endpoints;
  - the docs gates and the Python ratchets.
- Each round-6 commit was checked on its own:
  - `c7cde331`: 254 arms, 162 mutants;
  - `80ba13d7`: 257 arms, 163 mutants;
  - `d5f56313`: 260 arms, 174 mutants.
- `--fuzz`, seed 234, 0 failures, no traceback:
  - 20,000 on the fixtures: 12,823 shape-breaking cases, all exit 2, 258 of them `note` or `entry key` cases past a list's first item;
  - 20,000 on A's real route: 13,609, of which 326;
  - 5,000 on A's real standalone 1x1: 3,183, of which 98.
- Real data: A route, 1x1 and 8x8 rc 0, route status complete. B route rc 1 (+625 LUT). B 1x1 and 8x8 rc 0. The 10 ns control rc 2.
- New mutants against the round-5 and round-6 self-tests: of the 12 new, the round-5 self-test misses 8 and this one kills 12. The 500 generated cases alone detect 56 of the 174 shipped mutants.
- Both reviewers' round-5 packets, unchanged. R447-5's `verify_tree.sh` passed after every group (see the first open item).
  - R447-5:
    - `probe_r5_namekill`: 20 mutants. The self-test kills 18 (round 5: 12). Only "scope class below the scope names too" is undetected, which R447-5 found equivalent.
    - `probe_r5_names`: 72 of 72.
    - `probe_r5_realfuzz`: the first-item mutant fails 44 of 3,000 real-route cases.
    - `probe_r5_size`: as at round 5, 3,272 MiB at 900 deep by 1,000 wide, and exit 2 with `MemoryError` at 2,000 wide under a 6 GiB cap.
    - Prior probes and `reruns.sh`: as at round 5.
    - `run_fuzz.sh`: 90,000 cases, 0 failures. Its seed-234 digests equal this round's.
  - R446-5:
    - `probe_r5_names`: 18 killed, 3 survived (round 5: 17, 4). "SCOPES: any top-level key" is now killed. The three survivors are R446-5 S1's.
    - `probe_r5_cases`: 37 checks, 0 not as expected.
    - `probe_r5_equiv`: the head exits 2 on both cases.
    - Prior probes: as at round 5.
    - `run_gates.sh`: 31 of 31 rc 0.

Acceptance criteria (#234, as ruled in 5967852698 and 5967924270): unchanged from rounds 2 to 5. Round 6 changes tests only.

Open risks/questions:
- The `r5` probe group's tree check failed once, on an ignored temporary file my own concurrent gate run had open: the Tcl self-test's `syn/ooc/.ooc-mut-*.tcl`, which it removes when it ends. After the gate run, the rerun passed and 0 porcelain lines remained. The later groups ran with no gate running.
- Two of the new mutants, the class without lower case and the class without digits, are killed before any arm runs: they refuse the fixture's own manifest keys `path` and `sha256`. R446-1's reasons probe and R447-2's classifier therefore list them as CRASH, not ARM (163 ARM and 2 CRASH, and 159 ARM, 4 ESCAPED and 2 CRASH, of 165).
- The changed generator and fixture move the random stream. Every case digest differs from round 5's, and so do some seed-dependent reviewer counts: the oracle probe's 2b is 31 against 42.
- R446-5 R1 (wording in the PR body's Round 5 row) and R446-5 S1 are not in the round-6 assignment, so they are not answered. The PR body states both.
- The self-test is now at 1,000 lines, the limit. The next addition needs a restructuring.
- Packet for publication:
  - HANDOFF.md ("Round 6") and PR-BODY.md ("Round 6");
  - receipts/round6/: gates, real data, fuzz runs and replays, per-commit runs, the compaction comparison, the new-mutant and kill matrices, both reviewers' probes and drivers;
  - the round-6 scripts under scratch-scripts/.
