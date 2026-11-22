# [A815] round 3 handoff: PR #960 (#665 S13), correction round 2

Status: DONE. REVIEW READY posted on #665 as issuecomment-7073088228 (`receipts/public/`), last line "REVIEW READY dd163e41". No unit of this lane is running; the worktree is clean at `dd163e41`.

- Base of the round: `9413958c` (round 2's head, PR #960's head as pushed; branch `665-s13-flip-default` on the remote).
- Reviews answered: R880-2 (issuecomment-7072611287, NEGATIVE), R879-2 (issuecomment-7072822982, NEGATIVE).
- Branch `s13-flip-default`, local; the manager pushes. Final head `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`
  (27 commits on dev-soft-core `59b09884`; 4 this round). One-line subjects, no body, no trailers.

| Commit | Answers | What |
|---|---|---|
| `6e7d03c6` | R879-2-S1, R879-2-S4 | the resource sweep's self-test runs `prepare()` and `command_export()` with the builder and the export stubbed; `env = {` spacing restored |
| `919da9a1` | R879-2-R1, R880-2-R1, R879-2-S5 | the remaining "all-fabric shipping" labels retired (builder, integration, requirement ledger, FPGA, test pages); the compliance matrix's repeated bench-gate pointer dropped |
| `873a5dc2` | R879-2-S1 | the wiring arm reports a plan with no placement as a named finding, not a traceback |
| `dd163e41` | (gate) | the wiring arm's two stand-ins annotated and documented: the Python idiom ratchet (docs workflow row 63) refused them at `873a5dc2` |

No product source change: the four commits touch `syn/resmap/soc_sweep.py` (a measurement tool's self-test and one
spacing fix) and documentation only. The identity packet's fixes are outside the repository.

## Finding table

| Finding | Severity / lens | Cause | Fix | Test: planted defect -> failing words | Receipt |
|---|---|---|---|---|---|
| R880-2-F1 = R879-2-F1 (R880-1-F2 retained) | MAJOR / MINOR; Conformance, Tests, Docs | the archive's privacy scrub refuses a binary whose bytes it would alter; five compressed operands matched a scrub pattern by chance and were left out, so the published packet lacked them and its replay crashed | the five re-encoded (same compressor, another level: xz preset 6; gzip level 9 and 6) so the scrub leaves their bytes unchanged; their content is unchanged, and `binding.json` `reencoded` lists the round-2 file hash, the new file hash and the content hash; `MANIFEST.content.sha256` lists every compressed operand's content hash and the replay checks it | `tools/publish_check.py` copies the packet under the archive's rule (0 refused, 0 altered), then runs the replay (ALL CLAIMS HOLD) and the plants (13 of 13) over that copy | `identity/`, `identity-checks/publish-check.txt` |
| R880-2-F2 | MINOR Docs | the PR body fetched `s13-flip-default`, a name the remote does not have | `round3/PR-BODY.md`: `git fetch origin <full head SHA>` and a head assertion | the exact-SHA fetch resolves on the public remote (tried with `9413958c`) | `PR-BODY.md` |
| R880-2-S1 | SUGGESTION Tests | `rmutants.py` counted any failure as caught | it replays the unplanted packet first (exactly as given, nothing re-sealed) and grades nothing unless that holds; a plant counts only with a non-zero exit, the RESULT line reached and a FAIL holding its own marker; the grader is checked on synthetic outputs (4 of 4, including "a failure elsewhere only" -> MISSED) | - | `identity-checks/publish-check.txt` |
| R879-2-S1 | SUGGESTION Tests, Robustness | the sweep's self-test did not exercise `prepare()`/`command_export()` wiring | `wiring_problems()` (`soc_sweep.py:253`): the builder stubbed (no `--placement` gives the config's own, the split), `prepare(all-fabric)` must ask for all-fabric and return, `prepare(split)` must refuse naming the image, `command_export` must ask `prepare()` for the plan's placement and write nothing before it | M1 -> "prepare(all-fabric) was refused ..." and "did not ask the builder for all-fabric"; M2 -> "prepare(split) returned an argument list naming an absent platform image"; M3 -> "command_export asked prepare() for split, the plan names all-fabric"; M4 -> "a platform image present in the tree was reported missing" | `gates/plants-dd163e41.txt` |
| R879-2-S2 | SUGGESTION Tests | the raw-log rule accepted a `2` -> `3` digit anywhere | the rule is anchored: a differing WIRE payload, or a PASS line's mailbox words laid out as bytes, may differ only inside an occurrence of the arm's measured firmware_version string (read from its images) that reads as the head's string | plant "a '2' -> '3' digit outside the firmware_version string" (`control.head.log`) -> "1x1/none/control: raw log ... NOT ANCHORED" | `identity-checks/publish-check.txt` |
| R879-2-S3 | SUGGESTION Tests | the replay crashed on an absent operand | an absent operand is refused by name and the run reaches its RESULT line | plant "an operand the claims need, removed" -> "operand groups/1x1/none/aecp.head.log is absent; the claims that read it are refused" | `identity-checks/publish-check.txt` |
| R879-2-S4 | SUGGESTION Robustness | `env ={` | `6e7d03c6` (`soc_sweep.py:135`) | - | - |
| R879-2-S5 | SUGGESTION Docs | the bench-gate pointer twice | `919da9a1` (`MILAN_COMPLIANCE_MATRIX.md:4`) | - | - |
| R879-2-R1, R880-2-R1 | RESIDUE Docs | stale shipping labels | `919da9a1`: R879-2-R1's wording at `ENDSTATION_BUILDER.md:3-4`, `FR_NFR.md:109`, and at `INTEGRATION_GUIDE.md:3-4` split in two sentences for the 10-word style rule; for the three `KL_maap` lines (`FR_NFR.md:173`, `FPGA_DESIGN.md:313`, `TESTING.md:731`) R880-2-R1's exact substitution, "all-fabric allocator", which leaves the normative row's status untouched | docs gates | `gates/docswf-dd163e41.txt` |

## The identity packet

`receipts/identity/` (230 files, 72 MB, none over 20 MiB), built by `tools/build3.py` from round 2's packet. The train's scratch, which held the original operands, was removed during the restart; round 2's packet holds every operand.

- Re-encoded, content unchanged (`binding.json` `reencoded`):

  | Operand | Round-2 file | Round-3 file | Content | Encoding |
  |---|---|---|---|---|
  | `shipping/1x1/dump/bench.cells.xz` | `d398ea22` | `481b9f7d` | `0f115bae` (round 1's published dump hash) | xz preset 6 |
  | `shipping/1x1/dump/flip.cells.xz` | `21d551bd` | `9236170b` | `ece5a067` (round 1's) | xz preset 6 |
  | `groups/1x1/declaring-outputs/aecp-outputs.measured.log.gz` | `3ab0f4e3` | `0e5edeb3` | `441ee863` | gzip 9, mtime 0 |
  | `groups/8x8-1if/declaring-outputs/aecp-outputs.head.log.gz` | `936a668d` | `99e290b3` | `3031de28` | gzip 6, mtime 0 |
  | `groups/8x8-1if/declaring-outputs/aecp-outputs.measured.log.gz` | `19259754` | `99e290b3` | `3031de28` | gzip 6, mtime 0 |

  (The 8x8 pair, and the 1x1 measured and head logs, have equal content: no line of `aecp-outputs` differs.)
- `MANIFEST.sha256` (sha256sum format) and `MANIFEST.content.sha256` (every compressed operand's content); the replay checks both.
- Bound to `dd163e41`: the 16 harness images rebuild byte-identical there (`receipts/harness-rebuild-dd163e4143-*`), and the flip images' 19 and 16 inputs are equal there (`receipts/inputs-carry-*-dd163e4143.txt`).
- `tools/replay.py`: absent operands refused by name (R879-2-S3); the raw-log rule anchored to the firmware_version string read from each arm's images (R879-2-S2); the content manifest checked. Result: ALL CLAIMS HOLD.
- `tools/rmutants.py` (R880-2-S1): the grader self-check (4 of 4), the unplanted control, then 13 plants (round 2's 11, R879-2-S2's probe, R879-2-S3's absent operand), counted by their own markers only: 13 of 13.
- `tools/publish_check.py`: the packet copied under the archive's rule, as the manager stated it: 231 files written, 0 binaries refused, 0 texts altered. The replay and the plants run over that copy (`receipts/identity-checks/publish-check.txt`): PASS.
- Every file of `round3/` passes `privacy.scrub_redact(b) == b`.

## Gates at the final head `dd163e41`

No file in the RTL, builder, LiteX, firmware, config or suite scope changed since `62477be4` (`git diff --stat 62477be4 dd163e41` over those paths is empty), so round 1's builder suite, sweep, firmware gate, flip check and timing carry.

| Gate | Result | Receipt |
|---|---|---|
| docs workflow, 103 commands | 99 PASS; the 4 CI-environment rows (act install dir, `GITHUB_EVENT_PATH` x3), as rounds 1-2 | `gates/docswf-dd163e41.txt` |
| (at `873a5dc2`) the same | the Python idiom row refused the wiring arm's two un-annotated stand-ins (`unannotated/undocumented public function 2 > ratchet 0`), and the four Markdown-renderer rows lacked html5lib on the system interpreter; `dd163e41` fixes the first, the pinned Markdown venv the second | - |
| round checks (sweep and yosys self-tests, diagram regeneration, harness argv checks, solution docs, doc paths) | 6 of 6 | `gates/round-checks-dd163e41.txt` |
| planted defects in the clone (round 2's three sweep plants, R879-2's M1-M4, the two harness plants) | 9 of 9, controls pass, tree clean | `gates/plants-dd163e41.txt` |
| resource sweep, fresh clone | ship, axilite accepted with 0 platform images; six refusals kept; split-plan control refused before any export; argv equal to base; axilite XDC equal as a clock-group set | `f1/` |
| harness images rebuilt | 16 of 16 equal to the recorded | `s1/harness-images-dd163e41.txt` |
| flip images' inputs | 19 and 16 equal | `gates/inputs-carry-*-dd163e41.txt` |
| identity replay and plants, over the packet as published | ALL CLAIMS HOLD; 13 of 13 | `identity-checks/publish-check.txt` |
| exact-SHA fetch from the public remote | resolves (tried at `9413958c`) | - |

## Open questions

1. (rounds 1-2, unchanged) NFR-SCOUT-02's "switch-over" wording: for the owner.
2. (round 2, unchanged) the register map's re-record from a split export needs a public Issue: for the manager.
3. The train's scratch (with its gates interpreter) was removed during the restart. The docs workflow's lane-interpreter rows ran on the system interpreter, and the four Markdown-renderer rows on the pinned Markdown venv; all pass.
