[A612]

# F3b resumed handoff

Status: resumed at `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Implementation is in progress; no new commit is claimed yet.
The staged pin is `70936b77dc41981e192438388cd0aced69954f18`.
The five baseline and pin-only Release image audits passed.
Each pin-only load image grew 236 bytes; total including BSS grew 380.
The first host suite run found malformed ADP fixtures and an obsolete
47-access talker bound; the new pin measures 48 after its clock read.
Those checks are being updated for the authorized pin effects.
The DA_GATE implementation and parent controls are not yet validated.

The corrected scope is issue #665 comment 6151422598.
It authorizes stack #19, #20, #25 and the DA_GATE predicate.
The Release ceiling is stack issue #24 comment 6126295947.
TAKEN is already public; it will not be repeated.

## Current completion ledger

| Step | State | Evidence |
| --- | --- | --- |
| Identity and ruling | Read | Assigned origin, branch, full head confirmed |
| Pin scope and reviews | Passed | `pin-proof.json`; 45 paths within authorized PR file sets |
| Baseline image hashes | Partial | Five composed Release fixtures audited; default still pending |
| Pin and parent controls | Pending | Exact authorized effects |
| DA_GATE and contracts | Pending | Four arms and two interfaces |
| Gates, coverage, mutations | Pending | Commands, controls, results |
| Final artifacts and public status | Pending | No push authorized |

## Prior STOP record

The following is historical evidence from the superseded STOP.
Its unresolved decisions are resolved by the new ruling above.
Its NOT RUN entries remain accurate until replaced by measured results.

[A612]

# F3b parent handoff

Status: STOP before implementation.
Issue: #665. Assignment comment: 6151273346.
Branch: `665-f3b-parent`.
Starting and final head: `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Origin: the assigned HTTPS parent origin was verified exactly.
Executor: author. Independent reviewer: no new review requested.
Issue project state was already In progress.

## Stop findings

1. The required pin difference is not exactly stack pull request #25.
   The current gitlink is `405dc68310a18f669049ffc10cc23eef7300dcff`.
   The requested target is `70936b77dc41981e192438388cd0aced69954f18`.
   Direct tree-entry comparison finds 45 changed paths, versus 24 in #25.
   Twenty-one changed paths are outside #25's file set.
   In particular, `src/adp.c:310` changes ADP input acceptance:
   minimum length becomes ADP_FRAME_BYTES, and new version and
   control-data-length checks reject previously accepted frames.
   `sw/firmware/ctrl/test/ctrl_build.py:63` includes that source in PORTABLE.
   `sw/firmware/ctrl/test/ctrl_image.py:96` includes PORTABLE in image inputs.
   Therefore the parent-built cores change by more than the F3b predicate.
   This violates assignment item 1 without any build being necessary.
2. The session explicitly says any firmware behavior or linked-image change
   must trigger STOP. Assignment item 2 requires a firmware behavior change.
   `sw/firmware/ctrl/maap/maap_mbx.c:62` opens DA_GATE on validity alone.
   `docs/reference/MAILBOX_CONTRACT.md:255` states that meaning.
   `docs/design/MAILBOX_SPLIT.md:1067` records its egress consequence.
   Ruling 6092086337 item 4 calls the predicate new protocol behavior.
   No exception to the session stop instruction was assumed.
3. The exact Release-ceiling reference, comment 6126295947 on the parent
   issue, returns HTTP 404 through the repository API. The numeric ceiling
   was not inferred from another pull request's description.

## Changes and file locations

No repository files, generated files, gitlinks, or images changed.
No implementation step passed; no commit was created.
No submodule was initialized. No Git command ran inside a submodule.
The public stack trees and blobs were read by API, without changing a branch.

| Artifact | Location | Content |
| --- | --- | --- |
| Handoff | `HANDOFF.md:1` | STOP, evidence, and outstanding acceptance criteria |
| Prepared body | `PR-BODY.md:1` | Template sections, blocked status, and reproduction |
| Pin evidence | `pin-proof.json:1` | Exact before/after entries, full file sets, and history |
| Additional behavior | `adp-pin-diff.patch:1` | Exact old-pin to target-pin ADP source diff |
| Artifact inventory | `MANIFEST.sha256:1` | SHA-256 and byte size for the report files |

## Pin proof

No pin move was made. The requested equality is disproved.
The target is the merge commit of stack #25. Its complete tree matches
that pull request's reviewed head `f13c9c16c2b300d158f980dd7c7f071dcb84df5b`.
The pull request base is `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475`.
The old pin and target share merge base `1a9f651cdf7846b8e10ac246a6ef6916960fbb92`.
The target has nine commits absent from the old pin; the old pin has four
commits absent from the target. This ancestry fact alone does not prove
that publication fixes were lost: the tree-entry comparison is the scope evidence.
API tree responses were checked for truncation; all were complete.
The comparison uses `(path, mode, type, blob id)` at both exact commits,
not the three-dot comparison's merge-base file list.

### Target-only history

| Full commit | Subject |
| --- | --- |
| `51870377c5012766a8ea1d9798e3c499ca1060a3` | Discard malformed ADP discovery frames (#19) |
| `98dc9e3076714bebe113982ee18c3c1c496cf3c9` | Specify the entity in YAML and generate the cores' C configuration (#20) |
| `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475` | Integrate the ACMP publish port with main (#23) |
| `917201098395f1f1acc635ea1722e6c9a91a3ec0` | Gate ACMP declaration on configured probe freshness or Listener demand |
| `9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1` | Prove ACMP freshness terms with mutation and target coverage |
| `0868387deab21bd0db414424f306c7ea62498e29` | Address ACMP freshness review findings |
| `1edff3180c2ff435b855cc770fb8be371f2096b3` | Protect ACMP freshness expiry across masked clock wraps |
| `f13c9c16c2b300d158f980dd7c7f071dcb84df5b` | Complete ACMP freshness contract mutation coverage |
| `70936b77dc41981e192438388cd0aced69954f18` | Gate ACMP declaration on a fresh probe or Listener (#25) |

### Old-pin-only history

| Full commit | Subject |
| --- | --- |
| `2dcbe91ead981591d5bfb652f6616f6edb325875` | Publish ACMP sink state before responses and completion callbacks |
| `f3dc2ae5bad02aa05a504b43c207e8b304d2bed5` | Close ACMP publication review gaps |
| `bc68ad8f3577e8f3dc24c4336e9b80a933df6c79` | Require per-field ACMP publication cache coverage |
| `405dc68310a18f669049ffc10cc23eef7300dcff` | Identify ACMP cache assertions by owner and definition location |

### Exact pin-delta file list

The second column says whether #25 itself changes that path.
A Yes does not claim the old-pin delta is byte-identical to #25's delta.

| Changed path | In #25's file set |
| --- | --- |
| `.github/workflows/quality.yml` | No |
| `CMakeLists.txt` | No |
| `configs/ax7101.yaml` | No |
| `configs/compat/ax7101.json` | No |
| `configs/duplex.yaml` | No |
| `configs/listener.yaml` | No |
| `configs/talker.yaml` | Yes |
| `docs/CODING_STANDARD.md` | No |
| `docs/DEVIATIONS.md` | No |
| `docs/ENTITY_YAML.md` | Yes |
| `docs/PORTING.md` | Yes |
| `docs/REQUIREMENTS.md` | Yes |
| `docs/TESTS.md` | Yes |
| `docs/TRACEABILITY.md` | Yes |
| `docs/VERIFICATION.md` | Yes |
| `docs/requirements.json` | Yes |
| `examples/entities/ax7101/entity_config.c` | Yes |
| `examples/entities/ax7101/entity_config.h` | No |
| `examples/entities/duplex/entity_config.c` | Yes |
| `examples/entities/duplex/entity_config.h` | No |
| `examples/entities/listener/entity_config.c` | Yes |
| `examples/entities/listener/entity_config.h` | No |
| `examples/entities/talker/entity_config.c` | Yes |
| `examples/entities/talker/entity_config.h` | No |
| `examples/entity_roundtrip.c` | Yes |
| `examples/entity_roundtrip.h` | Yes |
| `examples/rv32/smoke.c` | Yes |
| `include/acmp.h` | Yes |
| `scripts/baremetal.py` | No |
| `scripts/conditional_policy.py` | No |
| `scripts/entity_selftest.py` | Yes |
| `scripts/entity_yaml.py` | Yes |
| `scripts/milan_entity.py` | No |
| `scripts/mutation.py` | No |
| `scripts/requirement_records.py` | Yes |
| `scripts/static_analysis.py` | No |
| `scripts/traceability.py` | No |
| `scripts/validate.py` | No |
| `src/acmp.c` | Yes |
| `src/adp.c` | No |
| `tests/coverage.ratchet` | Yes |
| `tests/mutations.json` | Yes |
| `tests/test_acmp.cpp` | Yes |
| `tests/test_adp.cpp` | No |
| `tests/test_entity.cpp` | Yes |

The ADP source blob changes from
`d96be5b3a70197cb3fc96fa6ce31da216be4a4b9` to
`764396c2e605e0b4ad0fe2a60df87495e1c7be20`.
The MAAP source and the ADP, MAAP and wire public headers are unchanged.
The ACMP source and public header also change, as expected for F3b.

## Image hash table

STOP occurred before any image build or implementation.
No measured before/after hash or byte-identity claim is available.
These are all five tracked builder shapes. Release and Debug measurements
remain unrun for each; the Release ceiling remains unverified.

| Shape | Before SHA-256 | After SHA-256 | Size delta | Result |
| --- | --- | --- | --- | --- |
| `endstation_arty_4x4` | Not built | Not built | Not measured | STOP before implementation |
| `endstation_arty_8ch` | Not built | Not built | Not measured | STOP before implementation |
| `endstation_arty_current` | Not built | Not built | Not measured | STOP before implementation |
| `endstation_ax7101_1x1_tdm8` | Not built | Not built | Not measured | STOP before implementation |
| `endstation_ax7101_8x8` | Not built | Not built | Not measured | STOP before implementation |
| All-fabric default image | Not built | Not built | Not measured | Source tree unchanged; binary equality not measured |

## Checks, gates, and planted controls

Only scope and state checks ran. No firmware gate ran, no mutant was
executed, and no existing suite pass is claimed for this session.
Commands below are reproduction commands, without any wrapper prefix.

| Check or gate | Command or artifact | Result | Planted control |
| --- | --- | --- | --- |
| Parent identity | `git remote get-url origin`; `git rev-parse HEAD`; `git branch --show-current` | rc 0, assigned origin, head and branch | Not a behavioral gate |
| Initial tree state | `git status --short` | rc 0, empty | Not a behavioral gate |
| Assignment | Issue #665 comment 6151273346 | Retrieved verbatim | Not a behavioral gate |
| Governing ruling | Issue #665 comment 6092086337 | Retrieved verbatim | Not a behavioral gate |
| Release ceiling | Issue #665 comment 6126295947 | HTTP 404, command rc 1 | No substitute ruling assumed |
| Pin scope | Complete API trees at the two pins and #25 base/head | Read rc 0; required equality fails | Direct ADP source diff is counterevidence, not a planted mutant |
| Firmware host, RV32 and mutations | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | NOT RUN after STOP | Registered ctrl mutations, including interface-zero DA_GATE plant |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | NOT RUN after STOP | `python3 sw/firmware/gtest/fw_coverage.py --selftest`, NOT RUN |
| Harness tally | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | NOT RUN after STOP | Tally mutants, NOT RUN |
| RV32 object audit | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | NOT RUN after STOP | Hostile headers, wrong ISA/ABI, unresolved dependencies, NOT RUN |
| Linked-image audit | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` | NOT RUN after STOP | Arithmetic, recursive helpers and incompatible image controls, NOT RUN |
| Firmware dependency boundary | `sw/firmware/ctrl/test/ctrl_boundary.py` | NOT RUN after STOP | Builder-capture plants, NOT RUN |
| Source lists | `python3 scripts/check_rtl_source_lists.py` | NOT RUN after STOP | `--selftest`, NOT RUN |
| Evidence readers | `python3 scripts/measure_test_evidence.py --check` | NOT RUN after STOP | `--selftest`, NOT RUN |
| Stack boundary | `python3 scripts/check_boundary.py --selftest --jobs 4` in a verified stack checkout | NOT RUN after STOP | Include-boundary, heap and OS-symbol plants, NOT RUN |
| Stack validation | `python3 scripts/validate.py --work build-validation --jobs 4 --graphs` in a verified stack checkout | NOT RUN after STOP | Registered standalone controls and mutations, NOT RUN |
| Hosted workflows and local replicas | No new pushed head | NOT RUN | No push authorized |

Some exploratory path lookups returned missing-path errors; corrected paths
were subsequently read. They were context discovery, not gate results.
Full architecture and gate review stopped at the scope conflict.

Final `git diff --check`, `git diff --exit-code d40e4e9827be2516f8f34b9d65f0a483fff2194c HEAD`, and `git status --short` all returned 0; status remained empty. See `state-checks.json`.

## Coverage table

| Population | Lines hit / total | Branches hit / total | Result |
| --- | --- | --- | --- |
| Parent firmware | Not measured | Not measured | NOT RUN |
| Parent adapter and composition | Not measured | Not measured | NOT RUN |
| Stack at requested target | Not measured locally | Not measured locally | NOT RUN |

No historical coverage result is presented as current-head evidence.

## Predicate and mutation table

| Required control | Required behavior | Mutation result |
| --- | --- | --- |
| Fresh probe with valid DA | Declaring during the 15 s interval | Not implemented or run |
| Registered Listener with valid DA | Declaring without a fresh probe | Not implemented or run |
| Neither probe nor Listener | Not declaring | Not implemented or run |
| Probe aged past 15 s without Listener | Stops declaring | Not implemented or run |
| Invalid DA with either demand arm | Not declaring | Not implemented or run |
| Interface 1 acquires alone | Its own publication precedes its report | Existing test preserved; NOT RUN |
| Every interface acquires | Each publication precedes its own report | Existing test preserved; NOT RUN |
| Differential against acmp_declaring_o | All predicate arms agree | NOT RUN |

The existing two-interface tests remain at
`sw/firmware/ctrl/test/test_maap_mbx.cpp:152` and `:168`.
The existing `rv-maap-gate-on-interface-0` plant remains at
`sw/firmware/ctrl/test/ctrl_mutants.py:677`.
Their present expectations cover address validity, not the new demand predicate.

## Remaining decisions and work

A public decision must supply a pin whose parent-built core delta is only
F3b, or explicitly revise the frozen pin scope to include the extra behavior.
The session behavior/image stop instruction needs an explicit F3b exception
before implementing its required predicate. The Release-ceiling reference
needs correction or an accessible authoritative replacement.
After those decisions, implementation, generated contract updates, predicate
controls, image hashes, coverage, mutations, and all touched gates remain owed.
The manager owns any future base merge, push, review scheduling and publication.

## Public record

TAKEN was posted as issue #665 comment 6151303607.
STOP was posted: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151402754
The unchanged full head and all three findings are public.
