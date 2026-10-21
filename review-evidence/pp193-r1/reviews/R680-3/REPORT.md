[R680] POSITIVE - exact head 474346357043218c4e6b728f4ab4b83a2a8579e1

All five lenses are CLEAN for this delta and the named prior findings. No BLOCKER, MAJOR or MINOR remains. The re-walk supplies the missing transmit opportunity without duplicating served applicants; SH17 closes the re-park coverage gap. One PR-wording RESIDUE is recorded below.

Reviewed tree: `5ad76c02f6cfd8dbfa0b8d09e34b1cd22acec312`. Original source base: `21601694880efdfc4be3028afa3525fbc8f29c03`. Round-3 base: `7b424cdfe111a426f00517ff471246b4b9650726`. The six author commits are `70dd531`, `2f95efe`, `8f16338`, `1969f94`, `65d39b0`, `324ac9a`; the manager merge adds main `859b537b` through `47434635`.

The review reconstructed the supplied repository instructions, absence of repository AGENTS.md/CONTRIBUTING.md, docs/README and HDL conventions, the frozen issue acceptance and public scope decisions, requirements/interfaces, base diff and history, and public executable evidence. The [round-3 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/198#issuecomment-6311435371) and [ownership ruling, including item 2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193#issuecomment-6290012163) were read exactly. Authorities include issue #188's owed Leave, #189's per-sink registration reporting, REQ-ACMP-018/022, REQ-SRP-005, architecture 02 §4.1, 07 and 10 §6.4, IEEE 802.1Q-2018 Table 10-3/10.7.7/35.1.2.2/35.2.6, and Milan 4.2.7.2.2 as specified by those public requirements.

The independent verdict and ledger were written in `independent-pass.md` before opening earlier review findings. Their reconciliation follows. Untouched code retains the earlier covering verdict; scheduling and group-mark dependencies affected by this delta were examined again. No private author material, other checkout, private management tree, or concurrent review report was used.

**Mechanism and conformance**

At `hdl/srp/KL_srp_listener_fsm.sv:1003`, every passed slot receives the walk mark, including a quiet rider. At `:1072`, the taker receives its applicant's mark after the other assignments. A not-yet-served applicant moved behind the cursor therefore clears that destination's passed-slot mark. At `:1040`, W_DONE restarts at zero unless all marks are set. The restart neither resets marks nor changes `wtxla_r`, so it delivers the same walk's tx! or txLA!. At `:711`, a marked active slot does not receive another transmit event. Group operations and control acceptance have priority over a transmit from the giving slot (`:683`); a transfer cannot simultaneously advance that applicant through the walk at its old slot.

This is a conforming implementation of the assignment's required outcome even though the assignment offered two other possible mechanisms. The declaration remains one applicant per attribute value. QA receives sJ/JoinMt on txLA!, not a later plain tx! that would send nothing; LA receives txLA! to LO, followed by Empty at the next tx!. The state and parameter remain carried rather than being reset. No extra per-sink flip-flop was introduced by this round. The one-sink parameter arm and interfaces are preserved.

Other applicants are not postponed into a later walk: completion is withheld until every slot is marked, while already served applicants are suppressed on subsequent passes. My collateral probe places two unrelated declaring streams beside the transferred one. In all 12 combinations (holders 5/7, clocks 1–3, tx!/txLA!), the walk finishes with exactly three pushes and the expected next states, one push per stream. The mark-loss control still fails SH7, independently checking suppression of a second transmit. Finite input activity and eventual output acceptance remain the existing progress assumptions; this is not an absolute latency guarantee under permanent backpressure or continuous higher-priority events. `KL_srp_top.sv:1163` waits for both stream walks before the normal drain; its existing high-water interim drain remains unchanged.

The additional last-Lv fix is real at the round-3 base. `published/newchecks-at-base/log` records SH21 producing `5/2 0/2` for one StreamID in one walk: Lv Ready followed by New Ready. In a one-applicant Table 10-3 sequence, LA consumes that walk's tx!, becomes VO, then New! becomes VN and must await another tx!. It must not gain an additional opportunity by changing slots. Section 35.2.6's single declaration per value and the assignment's one-applicant rule support that ordering. Marking the served group at `:1004` prevents this; the reverting `listener-walk-marks-group-only-on-retire` control reproduces exactly the Lv/New failure. When txLA! leaves LO, the holder stays in place and its carried mark provides the same protection. SH21's assertion and oracle are unchanged by the control.

**Every named prior item at this head**

| Item | Disposition and artifact-specific evidence |
|---|---|
| R679-2-F1 — MINOR, all five lenses | Resolved at the scheduling cause above. My execution of the unmodified published `s2_probe.py` gives MATCH in all 20 rows: both holders, both walk kinds, clocks 1–3, registration-before-walk and no-registration controls. SH18–SH20 pass in the 1,418-check golden. `listener-walk-ends-owing-a-transmit` is KILLED by SH16, both SH18 checks, SH19 and SH20. The banner, architecture 10:645 and PR now describe same-walk service, not a one-T-MRP-JOIN delay. |
| R679-2-F2 — MINOR, Tests | Resolved. SH17 at `tb/srp_stream_fsms/sim_main.cpp:1799` exercises a second rebind while another sink declares the interim stream. Its exact named edit removes `&& !lvp_r[a]` at listener `:957`. `listener-repark-takes-matcher-pairs` is KILLED by SH17. My unmodified re-park probe also gives MATCH: owed SID0 Lv retained, no spurious SIDP New. |
| R679-2-R1 — RESIDUE, Docs | Applied and extended correctly. `tb/srp_top/README.md:868` now lists SH2–SH17, SH21, SH23, RB1, RB4, RB7 and the LA table walks, with 65 failures. The published final campaign has exactly those tags and 65 failures, plus the three wire failures in the separate arm. |
| R679-2-S1 — SUGGESTION, Tests | Applied. SH23 holds two independent parks through txLA!: both become LO and each sends Empty, not Lv, next. `listener-two-parks-grouped` removes the both-parked exclusion at listener `:607` and is KILLED by SH23. |
| R679-2-S2 — SUGGESTION, RTL/area | Measured and deliberately not retained, as the assignment permits only an area-neutral improvement. Two-input/eight-output KL_pp_shadow was +99 LUT / −128 FF with the aliasing change. Commit 65d39b0 restores the existing second copy. The final two-sink elaboration arm has no S2 change. |
| R679-2-S3 — SUGGESTION, Docs | Applied. The PR labels the separate one-sink Listener-only measurement: main 2,898 LUT / 454 FF, head 2,786 / 455, delta −112 / +1, beside the statement that KL_pp_shadow 1×1 was not measured. The earlier round-only +69 LUT figure is also distinguished. |
| R680-2-S1 — SUGGESTION, Docs | Applied exactly: the two RB/RB5 parentheticals are removed at stream-FSM `:1596`; behavior and clause citations are unchanged. |
| R679-1-F1 / R680-1-F1 — MAJOR, Conformance/RTL/Robustness/Tests and related Docs | Remain resolved at the cause. Recorded parks belong to their held StreamID via `same_w/lq_r` (`:595`), takeover clears the park (`:1056`), and the applicant state is carried. SH10–SH16 pass in the exact-head golden; the changed SH16 now correctly expects its New in this walk. Public SW4–SW7 and the full SRP campaign remain passing; their test sources are unchanged from the author validation. The original uniqueness and peer-registration coverage is retained. |
| R679-1-F2 / R680-1-F2 — MINOR, Docs | Remain resolved: PR area figures explicitly say eight inputs/eight outputs and distinguish absent whole-wrapper 1×1 measurement. See area provenance below. |
| R680-1-F3 — RESIDUE, Docs | The specifically assigned SW heading/prefix removal remains applied at `tb/srp_top/sim_main.cpp:3000,3170`. |
| R680-1-F4 — MINOR, Docs/Conformance; R679-1-S1 — SUGGESTION | Remain resolved: stream-FSM `:2094` and srp_top `:3171` cite 35.1.2.2 and 35.2.4.4.3/Table 35-14 for the type sum, retaining 35.2.6 for the in-place change. |
| R679-1-S2 and R680-2's earlier delay conclusion | Superseded by the required same-walk fix and R679-2-F1 resolution. The earlier conclusion that nothing was lost is not inherited for the txLA! case. |

The earlier public reviews were issue comments 6299632354, 6300027310, 6310901034 and 6311425623. The public review and inline-comment APIs returned zero additional entries. The source-comment audit found no newly introduced workflow/lane/reviewer/round/comment-ID label. The initial snapshot's concern about NS/NS1–NS5 is withdrawn: [public rule #746](https://github.com/kebag-logic/milan-fpga/issues/746) explicitly permits behavior identifiers. These identify checks, not bench lanes. No source-comment correction is required for them.

**Exact-head execution and public receipts**

| Evidence | Result |
|---|---|
| `focused-controls.log`, `controls/` | Golden 1,418 PASS; six selected mutations KILLED, campaign 7/7. SH7 mark loss; SH17 re-park; SH23 two parks; SH16/18/19/20 premature walk end; SH22 unmarked quiet-slot nontermination; SH21 group marking. Each fails its named behavioral assertion, not a compile failure. |
| `s2.log` | 20/20 MATCH, both controls retained; suite 1,418 PASS. The runner explicitly checks MATCH/DIFF lines because the original probe's process exit code alone does not grade them. |
| `repark.log` | MATCH; suite 1,418 PASS. |
| `collateral.log` | 12/12 MATCH; suite 1,430 PASS. All three applicants finish service before walk completion, with no duplicate push. |
| `merged-pp-default.log` | rc 0; default build 10,186 checks, 0 failures. NS 20, NP 53, D3 319 and GSI latency walks 5,568 checks all report 0 failures. |
| Author gate receipts under `published/gates/` | 1,030,375 suite checks, 0 failing at 65d39b0; lint, documentation, matrix, requirement-tag and portability/guard gates rc 0. Final documentation-reading gates at 324ac9a also rc 0. These are author pre-merge runs, not a manager source bank or a claimed full exact-merge sweep. |
| Author campaigns under `published/campaigns/final/` | SRP 208/208, assertion coverage 131/131; ACMP 65 killed; notifications 135 killed; D3 110 killed; AECP 67/67; dispatch 73/73; counters 18/18; GSI 23 detected; name-write/name-state/elaboration-guard records rc 0. The final RUNNER record identifies two clean clones at 324ac9a. The stopped earlier campaign is not used as completion evidence. |

The [published archive](https://github.com/kebag-logic/milan-fpga/tree/d530fd828739992dbbe15270c54be18ebf8f585c/review-evidence/pp193-r1) was sampled by section. All 84 downloaded receipts match its published SHA-256 manifest (`published-hash-check.txt`, `published-manifest-subset.json`). All 15 files changed by the six author commits remain byte-identical through the manager merge (`author-delta-identity.txt`). The executable source in the final author campaigns and the changed Listener implementation therefore maps directly to this head. No private originals were used. Seven oversized logs listed in the public EXTERNAL-RECORDS index were not downloaded; the visible summary and selected complete raw controls are the evidence used here.

Signature limitation: no detached signature or verification key was supplied in the referenced public archive, and the commit API reports `unsigned` (`archive-provenance.json`). Published content hashes were verified; cryptographic packet-signature verification is not claimed.

**Main merge, interfaces and area**

`git merge-tree --write-tree 324ac9a7 859b537b` reproduces the exact reviewed tree, with no manual conflict-resolution bytes. E_SINFO's complete generator, command model, decode.json, notify section, notify controls, D3 timing premise and pp_top driver are byte-identical to main 859b537b. Independently generated complete ROMs match, SHA-256 `1f78804e448c385d633ed4355b7d84100ec13b12c77305c3bc11986653a80a8e`, also the decode record's ROM digest. The merged pp_top README retains both the #193 unchanged-type/FailureInformation-control explanation and #199's NS and D3 timing descriptions. Its GSI control still plants the fault at the new shared-applicant decision. The exact-head default execution covers the resulting composition; this does not assert all seven build variants were locally rerun.

The Listener, SRP top and processor-top port/parameter declarations match the original source base, round-3 base and merged main. `pp_pkg.sv`, architecture interfaces 02 and memory maps 07 are unchanged from 21601694. No top-level port, parameter or register-map change. The inherited #192 change removes an internal signal only. `merge-identity.txt` records these checks.

| Published 8×8 KL_pp_shadow measurement | LUT | FF |
|---|---:|---:|
| Main 08023123 | 56,743 | 26,331 |
| Round-2 head 7b424cdf | 58,078 | 26,949 |
| Round-3 implementation 65d39b0 | 58,046 | 26,949 |
| Round-3 implementation minus main | +1,303 | +618 |
| Round-3 minus round-2 | −32 | 0 |

This is within the [accepted +1,335 LUT / +618 FF](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/198#issuecomment-6310654578), and within the assignment's additional 64-LUT allowance (96 LUT below that ceiling). LUTRAM 4,236, RAMB36 15, RAMB18 4, DSP 10 and CARRY4 2,392 are unchanged. Raw OOC logs and STATE records identify parent dev 78ca9bdf with the adoption patches and each processor gitlink. The measurement predates the manager's main merge; it is the accepted issue-implementation delta, not a newly measured full 47434635 netlist. No independent synthesis was run. The main-merge ROM composition and shipped route-1x1 validation are separate from that historical area comparison.

**R680-3-R1 — RESIDUE — Docs: qualify the PR's implementation-scope sentence**

Artifact: PR #198 body, Behaviour, “every RTL edit is inside `KL_srp_listener_fsm`”. That accurately describes the issue #193 implementation, but the published branch also includes the explicitly documented main merges. The full base-to-head diff contains the inherited #192 top/ACMP changes and #199 generation changes. Impact is wording only: the actual implementation scope, unchanged interface, measurements, tests and conformance conclusions do not change.

Exact fix: replace that sentence with “The issue #193 implementation changes RTL only inside `KL_srp_listener_fsm`, whose ports are unchanged; the branch also includes the main merges for #192 and #199.” Add the final main-859b537b merge to the opening commit chronology. Required outcome: a reader can distinguish issue-specific edits from inherited main content. Verification: compare the revised text with the two-parent history and `merge-identity.txt`; no code or measurement change. Carry this to the residue checklist; it does not leave Docs unclean.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | frozen ownership/round-3 rulings; #188/#189; Table 10-3 state/message expectations; SH17–SH23; S2 and three-applicant traces; inherited uniqueness/type-sum and peer checks | R680-3 delta and prior-item reconciliation; untouched scope retains R680-2 | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| RTL | CLEAN | listener arbitration, mark write/transfer, W_DONE and group lifetime; full base diff/history; main/ROM/tree identity; interface/map byte checks | R680-3; inherited #192/#199 main content checked for composition | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| Robustness | CLEAN | backward handover both kinds/holders/timings, A15 withdrawal, second park, two parks, rider late settle, duplicate suppression, unrelated applicants; progress/backpressure analysis; area provenance | R680-3 plus preserved earlier parked-value coverage | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| Tests | CLEAN | 1,418-check golden, six exact-head KILLED controls, 20+1+12 probe rows, merged pp_top execution, 84 verified receipts, campaign coverage and named tags | R680-3; author gates at stated pre-merge revisions | 474346357043218c4e6b728f4ab4b83a2a8579e1 |
| Docs | CLEAN | conventions; banner; 10 §6.4; SRP/pp_top READMEs; corrected prior citations/counts; measured-shape and single-sink qualifications; PR scope wording R1 | R680-3 and retained resolved R680-1/R679-2 items | 474346357043218c4e6b728f4ab4b83a2a8579e1 |

**Limits and pending manager duties**

At 2026-10-21 15:43 UTC, exact-head hosted run 39625824487 had executed successful docs-gates and portability jobs; suites remained queued (`hosted-jobs.json`). No queued, skipped or pending context is treated as executed proof. Hosted/act acceptance remains the manager's duty.

No full processor/parent/gPTP/portability/builder bank, source fix, commit, push, GitHub write, merge, container execution, shared install or hardware operation was performed. The reviewed clone was never edited; disposable exports and generated files stay under packet `scratch/`. The focused builds ran concurrently in foreground-owned drivers, with independent logs/return codes and at most 16 compiler workers; no heavy physical-design build ran. The pinned compiler identity was verified before use. The complete IEEE/Milan texts were not independently reread: this later-round review used the frozen public clauses, existing independent table transcription and unchanged prior conformance coverage. Physical calibration is NOT RUN; field skips are not hardware proof.

`source-integrity.txt` and `tracked-blobs.txt` verify all 702 tracked blobs' bytes and modes, index equality to HEAD, clean status including ignored files, the exact head/tree, and zero nested gitlinks. Nothing needs restoration. The historical parent STATE gitlinks are receipt provenance, not a current-dev checkout or candidate build.

There is no manager source bank at this exact head, and none is inferred. The manager must obtain the independent review pair, carry R1, validate the final current-dev merge candidate with the builder and native banks at merge turn, and publish its receipts on the PR. Source base 21601694 and live dev `d77a8afdbc960d70d1ceeee9af1163624f102b16` are distinct contexts. Check the shipped route-1x1 resource result at adoption; the OOC figures and simulation checks are not hardware acceptance.

Reproduction: `run_focused.py --source <clone> --packet <packet>` builds the exact-head focused controls and merged default suite in scratch exports; `run_probes.py --source <clone> --packet <packet>` runs the unchanged S2/re-park probes and the additional collateral probe, explicitly grading their output. `audit.py --source <clone> --packet <packet>` checks source/merge/ROM and published hashes. `MANIFEST.sha256` lists only publishable receipts and scripts with packet-relative paths. Local execution receipts retain their complete stdout/stderr with host paths normalized; `receipt-redactions.json` records original and published hashes. Scratch exports, prior-review reading copies and the reference-only historical runner are excluded.

R680-3 FINISHED
