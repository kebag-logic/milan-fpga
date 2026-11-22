[A815] REVIEW READY

Commit: `dd163e41` (`s13-flip-default`, on the remote `665-s13-flip-default` once the manager pushes; 27 commits on dev-soft-core `59b09884`; round 3 of #960, answering R880-2 and R879-2; local, the manager pushes).

Changed (round 3: 4 commits on `9413958c`, no product source change; every receipt named below is in this lane's round-3 receipts):

| Finding | Cause | Fix | Test | Receipt |
|---|---|---|---|---|
| R880-2-F1 = R879-2-F1 (R880-1-F2) | the archive refuses a binary whose bytes its privacy scrub would alter; five compressed operands matched a scrub pattern by chance and were left out, so the published packet lacked them and its replay crashed | the five re-encoded (xz preset 6; gzip 9 and 6) so the scrub leaves their bytes unchanged. Their content is unchanged: `binding.json` `reencoded` gives each one's round-2 file hash (as the round-2 manifest lists it), new file hash and content hash. The two 1x1 cell dumps' content hashes are the `0f115bae`/`ece5a067` round 1 published. `MANIFEST.content.sha256` lists every compressed operand's content hash, and the replay checks it | `tools/publish_check.py` copies the packet under the archive's rule (a binary the scrub would alter refused, a text scrubbed): 231 files, 0 refused, 0 altered; over that copy the replay ends ALL CLAIMS HOLD and the plants catch 13 of 13 | `identity/`, `identity-checks/publish-check.txt` |
| R880-2-F2 | the PR body fetched a branch name the remote does not have | `round3/PR-BODY.md`: `git fetch origin <full head SHA>` and `test "$(git rev-parse HEAD)" = <SHA>` | the exact-SHA fetch resolves on the public remote (tried at `9413958c`) | `PR-BODY.md` |
| R880-2-S1 | `rmutants.py` counted any failure as caught | it replays the unplanted packet exactly as given first and grades nothing unless that holds; a plant counts only with a non-zero exit, the RESULT line reached and a FAIL holding its own marker; the grader is checked on synthetic outputs, a failure elsewhere only -> MISSED | grader 4 of 4; control holds; 13 of 13 by marker | `identity-checks/publish-check.txt` |
| R879-2-S1 | the sweep's self-test did not exercise `prepare()`/`command_export()` | `6e7d03c6`, `873a5dc2`, `dd163e41`: `wiring_problems()` runs both with the builder and the export stubbed | your M1-M4 and round 2's three: 7 of 7 caught, controls pass | `gates/plants-dd163e41.txt` |
| R879-2-S2 | the raw-log rule took a `2` -> `3` digit anywhere | anchored: a differing WIRE payload, or a PASS line's mailbox words as bytes, may differ only inside the arm's measured firmware_version string (read from its images) reading as the head's | your probe, as a plant: caught, "NOT ANCHORED" | `identity-checks/` |
| R879-2-S3 | the replay crashed on an absent operand | refused by name; the run reaches RESULT | plant "an operand removed": caught | `identity-checks/` |
| R879-2-S4, S5 | `env ={`; a repeated bench-gate pointer | `6e7d03c6`; `919da9a1` | - | - |
| R879-2-R1, R880-2-R1 | stale shipping labels | `919da9a1`: R879-2-R1's wording (`INTEGRATION_GUIDE.md:3-4` in two sentences for the style rule); for the three `KL_maap` lines R880-2-R1's "all-fabric allocator", the normative row's status untouched | docs gates | `gates/docswf-dd163e41.txt` |

Validation (at `dd163e41` unless named):
- IDENTITY packet (`identity/`, bound to `dd163e41`): `cd identity && python3 -I tools/replay.py .` -> ALL CLAIMS HOLD.
  - 1x1/1if routed cells: 86,465 cells, every name, type and placement equal; 22 INIT bits in 8 cells, the 22 frame bits.
  - All 13 groups' raw logs, `aecp-outputs` included: each differing line only inside 2.96.0 -> 3.96.0. The changes are 2 lines in `aecp` and 2 in `aecp-held` at each point; every other group has 0.
  - The rest as round 2 found it: bench images to their published hashes, `.bit` differences named by field, 6 ELF bytes, ROMs equal to the ELF load segments, routes equal, 16 harness pairs, every group JSON leaf.
  - The harness images rebuild byte-identical at `dd163e41`, and the flip images' 19 and 16 inputs are equal there.
  - Nothing differs beyond the stated fields: no STOP, and the full CPU re-measure stays not required.
- The docs workflow's 103: 99 PASS; the 4 failing are round 1's CI-environment rows. The lane's former interpreter was removed with the train's scratch; its rows ran on the system interpreter, and the four Markdown-renderer rows on the pinned Markdown venv. At `873a5dc2` the Python idiom row refused the two new stand-ins; `dd163e41` fixes them.
- This round's checks (sweep and yosys self-tests, diagram regeneration, harness argv checks, solution docs, doc paths): 6 of 6.
- Planted defects in the clone: 9 of 9, controls pass, tree clean.
- The sweep in a fresh clone: `ship` and `axilite` accepted with no platform image anywhere; the six refusals kept; the split-plan control refused before any export; argv equal to base, the axilite XDC equal but for its clock-group order (equal as a set).
- Unchanged since round 1, so carried: the builder suite, the sweep, the firmware gate, the flip check and timing. No file in their scope changed (`git diff --stat 62477be4 dd163e41`).

Acceptance criteria: unchanged from round 1 (issuecomment-7070924358). The identity carry's operands are now complete and replayable from the form the archive publishes; each round-3 finding is fixed at its cause.

Open risks/questions:
1. (unchanged) NFR-SCOUT-02's "switch-over" wording: for the owner.
2. (unchanged) the register map's re-record from a split export needs a public Issue: for the manager.
3. Publication: `identity-checks/publish-check.txt` reproduces the archive's rule as the manager stated it. If the archive applies other rules, the same check should be run on its output.

REVIEW READY dd163e41
