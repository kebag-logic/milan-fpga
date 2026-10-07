[R533] POSITIVE - exact head c1049de1970e93d2c36ace62891ee9d947cd3191

Round R533-3, external independent source review of issue #665 / PR #690.
Tree: `168564db27f588e2eaf34d2fa3ff54947eecd00d`.
All five lenses are CLEAN at this head. No BLOCKER, MAJOR or MINOR remains
from this review. One earlier optional suggestion and one wording residue are
retained below. This is a source-review verdict; hosted acceptance and the
current-dev merge candidate remain separate manager duties.

The public contract was reconstructed from AGENTS.md, CONTRIBUTING.md,
docs/README.md, the issue body and decisions, REQUIREMENTS.md,
FR_NFR sections 3.4.1/3.4.2, the mailbox YAML/design and interface code.
The governing round-three decisions are
[assignment 6035166787](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6035166787)
and [STOP ruling 6036016117](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6036016117).
The complete `db9aa8c9..c1049de1` file delta and history were distinguished
from inherited dev changes; the focused implementation delta is the single
commit after `42a0371a`. `scope.json` records those populations.
Prior public findings were consulted after the independent source pass.
No private author material or concurrent round-three report was used.

Public author evidence at `fa19435a` is historical; the current packet is
[author-r3 at cd267b52](https://github.com/kebag-logic/milan-fpga/tree/cd267b52/review-evidence/665f4-r1/author-r3).
Its summaries, size records and receipt manifest were examined as public
evidence, not substituted for independently executed results. Input hashes
and public decision links are in `public-inputs.json`.

**Round-three findings resolved at their roots**

| Prior finding | Disposition and current evidence |
|---|---|
| R532-2-F1: link learned only from records | RESOLVED. `srp_mbx.c:681` samples each current link at attach. `:599` reconciles both level edges and applies the lifecycle reset before service resumes. The no-record reattach and cancelled-DOWN cases pass at IF=1/2. Reviewer plants `attach-level` and `recover-level` fail their named tests. The independent `R533ReattachThenPhysicalRestartFencesOldPermissions` also verifies a subsequent actual down/up, old RX backlog, default Domain, fresh-registration requirement and peer-interface survival. |
| R532-2-F2: undocumented dependency and failing documentation gates | SOURCE RESOLVED. `SUBMODULES.md:26/193`, `THIRD_PARTY.md:20`, the generator role/node/edge, SVG, Draw.io and decoded PNG now include the exact pin, ownership, Apache-2.0 notice and fetch guidance. All four previously failing commands pass. Independently deleting the row or diagram node/edge is rejected (`docs-plants.json`). The complete docs command accounting was checked in ROUND3-GATES; the separately delegated compiler-absent check has the manager's public rc 0 receipt. Hosted docs acceptance remains pending, not inferred from these results. |
| R533-2-F1: replacement loses shared Applicant state | RESOLVED. `srp_mbx.c:305-334` constructs replacement state from every existing StreamID/VID user, installs it, then judges the resulting binding set. `:493-554` reconciles one declaration per StreamID. Both sink orders, destination/VID changes, remaining-eligible and zero-eligible cases, consecutive replacements and final removal pass. Two independent wire probes pass at IF=1/2. Removing state inheritance fails both the ordinary and consecutive-replacement tests; no stale Ready renewal survives. |
| R532-2-F3: last never-eligible binding leaks VID | RESOLVED. `srp_mbx.c:332` no longer predicates final withdrawal on the departing sink's individual request history. The test creates the never-requesting binding before another binding requests VID 7, verifies that premise, then observes withdrawal in both unbind orders. Reintroducing the historical guard fails `vlan_left` (`plants/last-vid-user.log`). |
| R532-2-F4: three discriminable escapes | RESOLVED. The independent `old-domain`, `old-vlan` and `representative-vlan` plants all compile and fail their required Domain, VLAN-before-Ready or matching-binding VLAN observations. The unchanged source passes their new named tests at IF=1/2. |
| R533-2-F2: note-4/5 tests unavailable from public state | RESOLVED. Topic `495520f5e02dd077fc9b1451942b25ec95afa1b8` was fetched publicly; its complete production `src` diff against pin `23d9a817` is empty. `applicant_receive_conditions_follow_link_mode` covers note 4 in VO and note 5 in both link modes; `pending_applicant_joinin_obeys_note_four` adds VP in both modes. Both build profiles pass their original unit and behavior suites. The three independently planted guard reversals fail the required named tests, followed by a restored-source pass. See `upstream/` and `upstream-provenance.json`. The authorized later main-branch pin update is not a finding. |

The [manager's compiler-absent receipt](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6036186046)
records rc 0, GATE 1b PASS and zero firmware compiler invocations. Its one
expected NOT RUN is the compiled CSR-address census, which requires the
intentionally absent compiler. That is not a failed source check or evidence
of physical calibration. The receipt is retained in
`manager-compiler-absent.json`; this reviewer did not rerun the delegated bank.

**Earlier findings and optional items**

| Prior item | Disposition at this head |
|---|---|
| R533-1-F1 / R532-1-F1 | RESOLVED. The MSRP-only Milan IN/rLv override is selected in host/target builds. Immediate Listener/Talker withdrawal, the original LV deadline, generic MVRP aging and D1 pass. `mrp_mad.c:562`, `msrp.c:400`, `srp_mbx.cpp:496/506/909` and the selected wire differential were examined. |
| R533-1-F2 | RESOLVED, including R532-2-F1's remaining recovery cases. Adjacent edges, stale RX prefix, reset allocation failure, other-interface preservation and Domain reset pass. No reservation reappears from the discarded prefix. |
| R533-1-F3 | RESOLVED through R533-2-F1 above. Shared arrival order, replacement and final-user ownership are now checked on emitted declarations. |
| R533-1-F4 | RESOLVED by the published reachable linked composition and base measurements. Current ROUND3-SIZE records spans 53,968 / 65,216 bytes for 1x1 at IF=1/2 and 68,656 / 94,656 for 8x8, with unchanged static storage. FC baselines are 18,752 / 19,248 bytes. The fixtures, required-symbol checks and accounting were reviewed; the links were not independently rebuilt in this round. |
| R532-1-F2, all three parts | RESOLVED. The 75% boundary and Ready-to-ReadyFailed strict callback cases pass; the final note-4/5 portion is resolved by the public topic and three executed plants above. |
| R532-1-S1 | ADDRESSED. The upstream `msrp_leaveall_changes_only_the_message_type_and_port` case is present, and the original upstream suites and parent Run-B differential pass. |
| R532-1-S2 | RETAINED SUGGESTION, detailed below. The adapter remains unaffected by the generic LV/rJoin indication. |
| R532-1-S3 | ADDRESSED. Failed recreation clears both participants, counts refusal and retries without dereferencing them; the other interface continues. Existing failure-injection cases pass. |
| R532-2-S1 | ADDRESSED. `MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline` passes in both interface shapes; MSRP and MVRP profile selection was also inspected directly. |
| R532-1-R1 | RESOLVED. SRP README correctly distinguishes centisecond TICK counts from NOW_MS. |
| R532-1-R2 | SUPERSEDED/RESOLVED. The linked composition measurement now exists and is described in the PR; the former object-only limitation must not be restored. |
| R532-2-R1 | RESOLVED. `ctrl/README.md:138` identifies the published branch and repository read-access requirement. |
| R532-2-R2 | RETAINED as wording residue with an updated exact fix below. The public manager decisions already establish the current assignment. |

**R532-1-S2 | SUGGESTION | Conformance, RTL**

Artifact: `third_party/lwSRP/src/core/mrp_mad.c:341/347` and
`sw/firmware/ctrl/srp/srp_mbx.c:69/625`.
Authority/evidence: the previously reported generic Table 10-4 LV/rJoin
indication remains in the unchanged dependency. The end-station adapter
compares Domain values and recomputes retained registrations. The public
round-three handoff explicitly retains this optional upstream concern.
Impact: a future bridge consumer may care about the extra indication; no
failing behavior in this adapter was found. Required outcome: optional
upstream evaluation for bridge use, without expanding this lane.
Verification: a future upstream change should test the generic transition
and callback consumers. This suggestion leaves no lens unclean.

**R532-2-R2 | RESIDUE | Docs**

Artifact: PR #690 body, Status and the introductory publication wording.
Authority/evidence: the text still presents the author's STOP/no-publication
handoff as the current activity state, while public ruling 6036016117 accepted
review and the exact head is published. The timeout history remains true.
Impact: stale activity wording only; no measurement, test result, code,
review verdict, conformance claim or privacy rule changes.
Exact fix: prefix the existing timeout description with `At author handoff:`;
add `The integration role published this head for review under issue #665
comment 6036016117.` Replace `After the integration role publishes this head:`
with `To inspect the published head:`. Preserve the timeout receipts and link
the manager's later compiler-absent receipt separately.
Verification: reread the updated PR body against those public comments.
The manager carries this item to the wording-residue checklist; it does not
make the verdict negative or leave Docs unclean.

**Independent lens results**

[R533] PASS Conformance - `srp_mbx.c:282/493/599/681`, `mrp_mad.c:493/562`, `srp_walk.cpp`, `srp/README.md:78` - checked declaration ownership, membership-before-Ready, current link recovery, Milan immediate MSRP leave, unchanged LV deadline and generic MVRP timing against the frozen assignment and cited Milan/802.1Q rules. The selected wire differential agrees with corrected D1 and the valid Listener subtype on Lv in D2.

[R533] PASS RTL - `scope.json`, `hdl/milan/mailbox/KL_mbx_evt.sv:112/235`, `ctrl_loop.c:122`, `mbx.c:165`, `srp_mbx.c:341/557/599` - checked the actual coalesced-level contract, event/RX/poll ordering, receive fence, static participant ownership, callback serialization and owed-frame commit ordering. F4 adds no HDL change against integrated dev `d51b373a`; source-base HDL changes belong to dev's prior AAF integration. Default fabric/shipping ownership and the generated mailbox ABI remain unchanged.

[R533] PASS Robustness - `srp_mbx.cpp:563/681/708/737/775/819/849/862/886`, `probe_lifecycle.cpp`, `plants/*.log` - applied reattach, cancelled level records, short down/up, stale backlog, shared replacements, last-user withdrawal, allocation/refusal, malformed input, full rings and reentry cases. Tests retain the unaffected interface and require fresh declarations after lifecycle reset.

[R533] PASS Tests - `srp_arms.py`, `srp_fixture.hpp`, `srp_mutants.py`, `positive/`, `probes/`, `plants/`, `upstream/` - ran 124 standing tests, four independent cases and nine compiled adapter plants. The three published upstream guard reversals fail their named observations; restored source passes. Documentation omission controls also fail as intended. The unchanged exclusion policy and updated 441/441 line, 410/410 SRP branch ratchet were inspected; the complete coverage campaign was not rerun here.

[R533] PASS Docs - `docs/reference/SUBMODULES.md:26/193/248`, `THIRD_PARTY.md:20`, `docs/diagrams/submodule_boundaries.*`, `srp/README.md:43/151`, public author-r3 and manager receipt 6036186046 - checked dependency pin/licence/fetch ownership, generated image readability, lifecycle/shared-binding contracts, upstream test citations, size accounting and the stated integration/timing limits. Required source documentation gates pass; the historical handoff wording is recorded only as RESIDUE.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c:282/493/599/681`; `mrp_mad.c:493/562`; `srp_walk.cpp`; IF=1/2 wire and timing receipts | R533-3 | c1049de1970e93d2c36ace62891ee9d947cd3191 |
| RTL | CLEAN | `scope.json`; `KL_mbx_evt.sv:112/235`; `ctrl_loop.c:122`; `mbx.c:165`; adapter lifecycle and static ownership | R533-3 | c1049de1970e93d2c36ace62891ee9d947cd3191 |
| Robustness | CLEAN | `srp_mbx.cpp`; `srp_debug.cpp`; `probe_lifecycle.cpp`; nine plant receipts and two-interface controls | R533-3 | c1049de1970e93d2c36ace62891ee9d947cd3191 |
| Tests | CLEAN | `srp_arms.py`; `srp_mutants.py`; `positive/`; `plants/`; `probes/`; `upstream/`; `target/`; `docs-plants.json` | R533-3 | c1049de1970e93d2c36ace62891ee9d947cd3191 |
| Docs | CLEAN | `SUBMODULES.md`; `THIRD_PARTY.md`; boundary diagram sources/renders; SRP README; author-r3; manager receipt; `docs/` | R533-3 | c1049de1970e93d2c36ace62891ee9d947cd3191 |

**Executed receipts and limits**

| Execution | Result | Receipt |
|---|---|---|
| Adapter IF=1/2 | 50 + 50 tests pass | `positive/srp_mbx.cpp-if*.log` |
| Selected wire differential IF=1/2 | 5 + 5 pass | `positive/srp_walk.cpp-if*.log` |
| Desk latency IF=1/2 | 4 + 4 pass, including original-origin 11 ms stall rejection | `positive/srp_latency.cpp-if*.log` |
| Debug guard IF=1/2 | 3 + 3 pass | `positive/srp_debug.cpp-if*.log` |
| Independent lifecycle and shared wire probes | 2 + 2 pass | `probes/if*.log` |
| Reviewer-selected adapter plants | 9/9 compile and fail named tests | `plants.log`, `plants/*.log` |
| Published upstream topic | Both profiles pass; 2675/2663 assertions and 3 behavior scenarios per profile | `upstream/OFF-*`, `upstream/ON-*` |
| Note-4/5 plants | 3/3 compile and fail named tests; restored source passes | `upstream/note*`, `upstream/restored-*` |
| Largest-shape target objects IF=1/2 | 12 + 12 objects pass; largest static frame 192 bytes | `target/if*.log` |
| Documentation/interface checks | Nine final checks pass; two omission controls rejected | `docs/`, `docs-plants.json` |
| Final checkout integrity | All tracked bytes, modes, indexes and required gitlinks match | `integrity.json` |

The em-dash check first refused the default interpreter because the pinned
renderer dependency was absent (rc 2). Repeating the same check with the
provisioned pinned environment passed all 339 controls. Both receipts remain;
the initial composite `docs.rc=1` is not misrepresented as a source failure.
Other ordinary source checks returned zero. Every behavioral mutation was
required to compile; compiler failures were never counted as catches.

H-SRP remains a conditional host envelope: 100 ns per mailbox access, one
aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty, sharing one
10 ms service budget. It does not establish target scheduling or wire timing.
Published linked spans include static pools once, alignment and an explicit
8192-byte reserved stack. Neither that reservation nor the 192-byte largest
individual frame proves a whole call-chain bound. This round did not rebuild
the linked size fixtures or rerun complete coverage, native, parent,
processor, gPTP, synthesis or builder banks. The assignment's full-bank
results remain manager evidence; focused reviewer results are listed above.

At the captured exact-head hosted snapshot, `firmware-unit` failed fetching
the private lwSRP repository before compiling, and `rtl-fast` consequently
failed. `hosted-fetch-diagnostic.log` records the authentication failure.
Docs and some exhaustive jobs were still running. The physical gPTP job was
SKIPPED. Executed successful jobs and skipped/pending contexts are recorded
separately in `hosted-final-snapshot.json`; no skipped context is treated as
executed verification. Resolving dependency access and obtaining all required
exact-head hosted results remains with the manager under the original F4
publication condition. No hosted/local-replica acceptance is claimed here.

The manager also owns the second independent review, optional upstream
follow-up and reviewed pin integration, the residue edit, construction and
full validation of the final current-dev merge candidate, explicit merge
authorization and post-merge containment. Source validation from FC base
`db9aa8c9` with integrated dev `d51b373a` does not validate a later merge tree.
ACMP application composition, live MAAP/stream inputs, the connected fabric
licence output and target ingress/service/egress measurements remain the
publicly scoped integration work. Physical calibration was NOT RUN; field
skips, desk tests and object builds provide no hardware or audio-soak proof.

All commands were attached foreground executions; independent native
campaigns ran concurrently with four workers each. Build concurrency stayed
at or below sixteen, with no heavy synthesis, container, hardware or shared
installation activity. Dependencies, source mutations and builds stayed
under packet `scratch/`. There were no source fixes, commits, pushes,
GitHub writes, author contact or merge actions.

The final integrity check independently hashes 1169 parent blobs and 931
blobs across the four required submodules, checks file/symlink/executable
modes, complete stage-0 indexes and hidden-index flags, and confirms all
required gitlinks. The optional external import remains uninitialized with
its original gitlink. No source restoration edit was necessary because all
plants used disposable data or scratch copies.

`REPRODUCE.md` and the portable scripts reproduce this packet. Publish only
REPORT.md and files listed in MANIFEST.sha256, using its relative paths.
Scratch is excluded from publication.

R533-3 FINISHED
