[A775] REVIEW READY — round 9, head `056d619d` (local, not pushed)

Commit: `056d619d` (`895-talker-redeclare` on round 8's `f93317cb`, six commits; the manager pushes). The ruling's delta reviews run from round 5's `62298ab5`. #902 merged into `dev-soft-core` during the round (`659d7687`), from `07ed787e`, the head synced here. `659d7687`'s tree is `07ed787e`'s, so the candidate merge with `dev-soft-core` has this head's tree.

**Changed** (the ruling issuecomment-6895331865 on round 8's stop; the one wire change it rules, and nothing else on the wire):

| Commit | What |
|---|---|
| `663b519b` | Sync: merge #902's `41ca9f87` (#894 round 20: docs, `aecp_mbx.h` comments, `rows_grade.py`'s docstring). Section 13's three conflicting hunks are taken word by word: #902's change applies wherever this branch left those words unchanged. |
| `845364b6` | Items 1, 2 and 4: `CTRL_LOOP_TX_MS` at two interfaces 99 -> **105** (the tx row's 104.25 rounded up), so `SRP_REDECLARE_CS` there goes 2,029 -> **2,030 cs**. One interface keeps 34 ms and 2,023 cs. The commit also updates the two self-test controls' figure and their plants under each row (33/104); FR_NFR 3.4.1; section 13 "THE TRANSMIT's figure at two interfaces (#895)"; the SRP README; the harness README. #902 kept 99. |
| `449d29d2` | `ctrl_memory_ledger.PLAT_8X8_1` 18,176 -> 18,240 B (see "Found in this round" below). |
| `c772b1e5` | Section 13: the images by hash, the sync's, the Talker arms, the rows, the ledger. |
| `249a3823` | The harness self-test's queued bound at the ruled 140 ms (see "Found in this round" below); `ctrl_loop.h`'s comment of it. |
| `056d619d` | Sync: merge #902's `07ed787e` (docs only, sections 5 and 13). Where #902 states its own head's image sizes, this branch states its own. |

**Item 5, by hash** (`image_sha.py`: each ELF's loadable bytes and every linked object of every image `ledger.sh` links, 552 files):
- Merge `663b519b` against round 8's image `73388996`: 552 of 552 identical.
- `449d29d2` against that merge:
  - **0 one-interface files differ.**
  - **12 two-interface files differ**: `srp_mbx.o` and the ELF of the platform's and the size fixture's 1x1 and 8x8 images, and of the harness's two 8x8/2if arms.
  - Each differs in **one instruction**, `li a3,2029` -> `li a3,2030`, and in no other instruction or section byte (`objdump -d`, `objdump -s`).
- The final head `056d619d` against `449d29d2`: 552 of 552 identical.

So every leg of round 8 carries.

**Run again:**
- **Talker arms:** `srp_talker.cpp` at 8x8/2if (11 tests) and at 1x1/1if (11), `SrpGate` at 8x8/2if (7), and SRP+ACMP at two interfaces (76): all PASS.
- **8x8/2if `valid-destinations` leg:**
  - 2 groups, 0 refusals, 0 budget misses, 0 of 3,052 passes over the share, no `STATED` line;
  - 49 joins, 185.605 to 190.228 ms;
  - both groups' measured logs are **byte-identical** to round 8's.

**Validation**, the full pass on clean clones of `056d619d`:
- **Hosted job steps:** every `run:` step of rtl-fast, rtl, docs and elaborate. `verify_wf.py`: 139 steps ran, 226 not run with a reason, **0 bad**.
- **Firmware campaigns:**
  - control: 716 of 716 caught;
  - AECP: 299 rows, all caught;
  - SRP: 415 rows, all caught, 70 of them `talker-` (including the hold-off plants);
  - 0 escaped.
  - `fw_coverage.py --check`: PASS.
- **Lane gates:** a, b and c all rc 0, except `flip_check` and `flip_check_8x8` (rc 1 by design at 8x8/2if). `harness_selftest`: 0 failures. behave, `test_builder --require-rv32` and the boots: rc 0.
- **Sweep:** four shards, each on its own `cpu_ranges.pick8()` range. 65 suites, 0 failed, 2,713,040 checks. `tsn_fuzz`'s field campaigns: 164 and 675 pass.
- **Graders at the head:**
  - `flip_grade.py --check --point 1x1/1if`: PASS;
  - `rows_tiers.py --selftest`: **1033 of 1033** (round 8: 1032);
  - `tier_grid.py`: 6 of 420, CHOSEN the built 900 us;
  - load: 0.517 / 0.514.
- **ROM:** `plat_ledger.py` PASS at every point. Platform 8x8/2if: 60.5 RAMB36, 1,368 B left.

**1x1/1if at the head** (900 us, bound 140), by every source, ms:

| Row | W | Bound | Margin |
|---|---:|---:|---:|
| R4 | 13.25 | 20 | 6.75 |
| R5 | 75.84 | 90 | 14.16 |
| R6 | 73.36 | 90 | 16.64 |
| first queued notice | 14.72 | 20 | 5.28 |
| last queued notice | 136.65 | 140 | 3.35 |
| R4L | 203.57 | 238 | 34.43 |
| ACMP | 29.63 | 30 | **0.37** |
| ADP | 27.86 | 30 | 2.14 |
| MAAP | 27.96 | 30 | 2.04 |
| tx | 34.00 | 49 | 15.00 |
| txL | 48.58 | 49 | **0.42** |

**The per-pass headroom:** a pass's own cost is **260 us**, and every row holds up to 278 us. At **279 us** the last queued notice is 141.36 ms and txL 49.02 ms, both over their bounds: 18 us of headroom.

**Found in this round** (this branch's own evidence, both fixed):
- **`plat_ledger.py` at 8x8/1if:** it has refused 8x8/1if's `ctrl_plat` since 7B's cut. The image carries 18,240 B against the 18,176 recorded, because the cut's kept gate and base add 64 B there.
  - Rounds 7B and 8 reported the sizes but not that FAIL, and round 8's PR body called it PASS.
  - `449d29d2` records 18,240. Only `test_ctrl_memory.py` and `plat_ledger.py` read the record, so no image changes.
- **The harness self-test:** the full pass's first run, at `c772b1e5`, failed `run.py --self-test` with 2 failures.
  - `selftest_notice.queue_checks` pinned the bound at 130 ms and probed 131 ms as a miss. That was stale since round 8 moved the bound to 140, and round 8 ran no gate.
  - `249a3823` pins 140 and probes 141 ms, one over the bound as before.
  - The pass then ran again in full at the final head. The first run is kept as evidence.

**Acceptance criteria:**
- **Acceptance 4 composed** holds at the head:
  - every 1x1/1if row holds by every source within its bound;
  - the load is within 0.70;
  - `tier_grid.py` holds the built design;
  - every join interval is within 181-239 ms;
  - each image is within its entry.
- **Acceptance 1-3 and 5** stand from earlier rounds, re-checked by the Talker tests and 35 plants at each interface count. The hold-off at two interfaces is now 2,030 cs, by the ruling.
- **Acceptance 6** is the bench run, not done here.

**Open risks/questions:**
- **The margins:** ACMP has 0.37 ms and txL 0.42 ms left at 1x1/1if, and a pass's own cost has 18 us of headroom.
- **`dev-soft-core`, with #902 merged,** states `CTRL_LOOP_TX_MS` 99 and `AECP_QUEUED_MS` 130. This PR moves them to 105 and 140 at its own image, by the rulings.
- **Not this lane's, for #894:** firmware-unit and the mutant jobs leave an untracked `dispatch-build/` in their checkout, as before.
- **Not run:** act and the hosted exact-head contexts, which follow the push. `[TIME]` (#906) and the hold `[TX]` (#907) stay pre-existing.

Receipts: round 9's packet, with `INDEX.md` generated from the files present. It holds identity, ledgers, arms, legs, graders, both passes, the sweep and the merges. Nothing was pushed.
