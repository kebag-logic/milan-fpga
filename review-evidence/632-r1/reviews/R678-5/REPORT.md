[R678] POSITIVE - exact head 24a292a0321df6f3516f25cb6e92e24fb1988e65

External independent review R678-5 of PR #770, issues #632 and #764. Tree: `c968fe214e70bc6c323068f146d5716729e6207e`.

All six named round-4 findings and R678-4-R1 are resolved at their causes. All five lenses are CLEAN for the assigned delta, with unchanged earlier coverage carried forward. No new BLOCKER, MAJOR, MINOR or RESIDUE was found. One optional reproducibility suggestion is recorded below. This is a source-review verdict, not merge authorization or completion of bench acceptance.

## Scope and independence

Reviewed `417ec52864efc09f1e3ecd0f755cb0daa7604426..24a292a0321df6f3516f25cb6e92e24fb1988e65`: three commits, ten paths, documentation and comments only. Used `e26f1816..HEAD` for provenance and the complete added-line citation scan. Implementation and prior gate coverage outside those changed inputs were not re-reviewed.

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, issue contracts/public scope decisions, requirements/interfaces, diff/history, then public executable evidence. The controlling [round-8 assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6369825862) requires no executable change. The domain-reference, build-now listener, fixed-depth queue, AAF-exact/CRF-rounded offsets and resource exceptions remain controlling. Bench acceptance remains after merge.

`independent-pass.txt` records my initial verdict and artifact-specific ledger before reading [R677-4](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6369812473) and [R678-4](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6369815554). Those reports were then reconciled below. No other current-round report or private author material was read. The public handoff was checked for the assigned changes, citation disposition and receipts.

The assignment's summary of earlier clean lenses does not replace the earlier ledger: R678-4 actually left Conformance, Tests and Docs unclean. Their attributed findings are explicitly closed here before those lenses become CLEAN.

## Prior findings resolved at this head

| Prior ID and attributable lenses | Disposition and cause-specific evidence |
|---|---|
| R677-4-F1, Docs; R678-4-F1, Conformance/Docs | **Resolved.** `docs/reference/MILAN_COMPLIANCE_MATRIX.md:221` and `docs/AAF_LATENCY_TAPS.md:105-109` now refuse individual late/too-early events while presenting other eligible events. A PDU containing a refused event counts once; an untimed PDU is not presented and counts once. This matches `hdl/ieee1722/aaf/KL_render_queue.sv:523-533,915-920` and `docs/design/TIME_SYNC.md:400-403`. Physical-evidence limits remain. Both retired phrases have zero tracked matches outside history. |
| R677-4-F2, Docs; R678-4-F2, Tests/Docs | **Resolved.** `docs/design/GM_LOSS_RECOVERY.md:321` states 21 controls plus two clean legs, 23 checks, separately retaining the five-control sweep. Independent AST enumeration finds 21 `CONTROLS` entries in `tb/verilator/milan_dp_gm_steps/gmstep_mutants.py`. `docs/testing/TESTING.md:278`, `GM_LOSS_RECOVERY.md:253` and the milan_dp README inventory agree. `tb/verilator/milan_dp/README.md:90` describes `tu`, refusal/counting across the step, unchanged `mr`/MEDIA_RESET and no render re-base, matching the unchanged harness and round-4 campaign evidence. |
| R677-4-F3, Docs | **Resolved.** `docs/testing/TESTING.md:647` says NOTIFY passes at the adopted processor pin and identifies the applied-readback mutation failing CRF steps 3 and 4. The obsolete pool workaround is removed; `until the pin moves` has zero tracked matches. Processor pin `93fb0b2d736b36588ea7321e25fba2f8819ea41f`, notify/GSI executable inputs and their previously covered integration remain unchanged. |
| R678-4-F3, Conformance/Tests/Docs | **Resolved.** Every assigned boot/reset and append site cites the correct 2011 clause; the neighboring paragraph explicitly distinguishes editions. Direct standard-text verification and every site are listed below. Passing documentation gates alone was not treated as clause proof. |
| R678-4-R1, RESIDUE/Docs | **Resolved.** `tb/verilator/milan_dp/dynmap_mutants.py:154,316,345,386` now say `#637:`; `:168` says `The former restore order (#637):`. Behavior/reason text remains. No new review-round, reviewer, lane or issue-comment label appears in added source comments. Executable tokens and Python AST are unchanged. |

Earlier cause-specific resolutions in R678-4 carry forward. This delta changes no earlier implementation, mutation, stimulus, assertion, generated artifact, configuration or resource record.

## Direct clause verification

Read the actual 2011 standard and both corrigenda. `standard-identities.json` identifies the exact PDFs by SHA-256; licensed text/extractions remain unpublished. Milan v1.2 4.2.6 names the 2011 standard and both corrigenda. The [IEEE edition catalogue](https://standards.ieee.org/ieee/1625/3956/) also identifies both corrigenda.

| Changed site at this head | Clause checked directly | Result |
|---|---|---|
| `docs/reference/REGISTER_MAP.md:1051` | 2011 10.3.12.1.4 b), with Cor1-2013 | With no qualifying peer vector, the system's own vector supplies the GM identity. Correct for the described GM-capable instance. |
| `docs/reference/REGISTER_MAP.md:1471-1475` | 2011 10.3.10.2.1 d); explicitly 2020 10.3.11.2.1 d) | Correct distinction between updating from a received TLV and clearing an absent received path. Additional cross-edition check below. |
| `docs/reference/REGISTER_MAP.md:1478` | 2011 10.3.10.2.1 d) | Qualified slave-port pathSequence is copied and thisClock appended. |
| `docs/reference/REGISTER_MAP.md:1480` | 2011 10.3.12.1.4 i), with Cor1-2013 | A local GM's path contains thisClock alone; the formerly edition-less 2020 number is corrected too. |
| `docs/reference/SUBMODULES.md:242` | 2011 10.3.12.1.4 b), i), with Cor1-2013 | Own-GM identity and one-entry path at boot. |
| `docs/reference/SUBMODULES.md:244` | 2011 10.3.10.2.1 d) | Received path plus thisClock; implementation bound remains explicit. |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:79-81` | 2011 10.3.10.2.1 d) | Correct append-oracle authority. |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1175-1176` | 2011 10.3.12.1.4 b), i), with Cor1-2013 | Correct boot rationale. |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1225-1227` | Same clauses | Correct reset rationale; assertion unchanged. |
| `tb/verilator/milan_dp/sim_gptp.cpp:51-52` | 2011 10.3.10.2.1 d) | Correct append-oracle authority. |
| `tb/verilator/milan_dp/sim_gptp.cpp:818-822` | 2011 10.3.12.1.4 b), i), with Cor1-2013 | Correct own-GM publication rationale. |

Also checked 2011 9.6.2.1 and 10.2.3.13: gmIdentity names the current GM when gmPresent is true and is zero otherwise; gmPresent indicates a GM-capable system in the domain. This supports the unchanged own-identity to GM A interpretation. Cor1 restates 10.3.12.1.4, including the corrected clockIdentity spelling. Cor2 changes 11.2.15.3 and modifies none of the assigned citations.

The sole remaining added-line 2020 reference is `REGISTER_MAP.md:1474`. To check the resulting publication, I also read 2020 10.3.13.2.4 f) 5): it copies receivedPathTrace to pathTrace and appends thisClock only if nonempty. The paragraph's explicitly cross-edition empty-sequence statement is accurate. `delta-audit.json` records exactly one `802.1AS-2020` added-line match across the full `e26f1816..HEAD` diff; no other added behavioral citation remains.

This does not establish 2011 conformance for the unchanged engine's no-TLV behavior. The 2011 receive function retains the previous path in this case: immediately after initialization it is `{thisClock}`, while a previously learned path can differ. The public handoff distinguishes this state dependence and flags the edition-policy question for the manager. This review closes the citation defect without silently deciding that separate engine-policy question.

## Executable boundary and evidence

`audit_delta.py` proves the hdl/syn/configs delta is empty, enumerates all ten changed paths, verifies identical non-comment C++ tokens in both simulations, and identical Python tokens/AST in the driver. The manual diff agrees: executable files contain only comment changes. No compile directive, mutation string, stimulus, check or expected value changed. Earlier code/gate coverage therefore remains applicable.

Evidence comes from the author's [immutable public round-8 packet](https://github.com/kebag-logic/milan-fpga/tree/c9d217d5fa998695e490d150e1da3ce6e3046234/review-evidence/632-r1/author-r8/receipts/round8), not a manager source bank. Independently downloaded and verified **108 files, including the index and its 107 listed files**, against `published_sha256`: zero mismatches. The public handoff hash also matches. Results are retained in `receipt-hash-audit.json`, `public-round8-manifest.json` and `handoff-provenance.json`.

The publication commit API reports **unsigned**, `verified=false`, no signature. These checks establish immutable-publication/hash identity, not cryptographic signature authentication. See `evidence-commit-verification.json`.

| Gate at 24a292a0 | Verified result and limits |
|---|---|
| Docs workflow | Of 44 planned steps, 42 executed with rc 0 under GNU Make 4.3. Five Markdown steps initially used another interpreter; all five have separate successful CPython 3.12.3 receipts. Remaining executed steps identify 3.12.3. Before/after head markers match. |
| Docs non-executions | Host-side candidate runner skipped by rule. Destructive no-Git command skipped; its two checks pass on an archive export. Neither skip is represented as execution. |
| Builder leg within docs | Separate LiteX-backed leg rc 0. Gate 11 calibration explicitly NOT RUN because the physical report is absent. |
| Lint/compile/baseline | Lint rc 0, 89 violations against ratchet 89; edited driver py_compile rc 0; resource baseline reports three passing endpoints. |
| gptp | Build/run rc 0, 185 checks, 185 PASS, zero FAIL. |
| ax1x1gptp | Build/run rc 0, 155 checks, zero failures; explicit NOT RUN fields retained, including physical calibration/compliance. |
| dynmap-mutants | rc 0, 68/68: five clean legs and 63 named controls. `audit_receipts.py` matches every current AST inventory entry to exactly one named catch. |
| Stopped dynmap attempt | Not counted as success. Initial run lacked listener generated inputs; the published repeat follows generation and completes the entire inventory. |
| GM-step/earlier banks | 21 current controls plus two clean legs. Execution and other implementation/gate coverage carry from unchanged round-4 inputs; no new full-bank run claimed. |

Own execution comprised byte/mode/index audits, token/AST comparisons, receipt hashes/inventory reconciliation, wording scans and direct standard-text inspection. No full suite, synthesis bank, builder bank, hardware run or prohibited runner was executed. Existing exact-head evidence made further heavy probes unnecessary.

## Optional finding and retained suggestions

### R678-5-S1 | SUGGESTION | Tests, Docs

**Artifact:** `tb/verilator/milan_dp/dynmap_mutants.py` listener build path; `public-round8/dynmap_mutants_24a292a0/attempt1_stopped/NOTE.txt`, `listener_clean_probe.log`, `render_inputs.log`; `docs/testing/TESTING.md` campaign instructions.

**Authority/evidence:** The unchanged driver suppresses rebuilding `tdm8r_aemi.bin`, `ltn_rom.hex` and `ucode.hex` for the listener clean leg. A fresh clone's first attempt fails the generated-image check. The author generates those inputs through their owning suite and repeats successfully, 68/68. Token equality proves this round did not introduce the prerequisite.

**Impact:** Direct campaign invocation in a fresh clone can encounter a setup failure before meaningful mutant results. The completed repeat supplies the assigned source evidence.

**Optional required outcome:** In a follow-up, document the prerequisite or make the campaign prepare the owned inputs: `make -j16 -C tb/verilator/milan_dp_render tdm8r_aemi.bin ltn_rom.hex ucode.hex`. Preserve the mandatory clean-leg failure.

**Verification:** From a fresh disposable checkout, follow the documented setup and require all five clean legs and 63 controls to pass. This suggestion does not condition the current verdict.

| Earlier optional item | Disposition |
|---|---|
| R677-4-S1, stronger boot-before-first-talker observation | Retained, unchanged `sim_gmstep.cpp:986-990`; the acquisition/provision sequence remains the covered basis. |
| R677-4-S2, one capture-coherence directory lacks HEAD marker | Retained packaging improvement; sibling provenance and previously covered result unchanged. |
| R677-4-S3, configured buffer versus fixed queue and stale CI-image inventory | Retained optional policy/inventory work; neither input changed. |
| R677-4-S4, design prose dated by review round | Retained at untouched `MEDIA_CLOCK_FOLLOWING.md:1964`; source-comment rule does not make that prose new residue. |
| R677-4-S5, merged edition citations | Assigned sites resolved by the mapping and complete added-line scan. Untouched hardware-assist/historical references are not recast as behavioral authority. |
| Optional items carried in R678-4's prior-findings table | Retained unchanged, including factory-row policy, closing-cycle reference and literal latency coupling suggestions. No earlier resolved defect reopened. |

## Reviewer-owned ledger

Each lens was independently applied to the delta and named prior causes. Unchanged implementation coverage carries from R678-4 at `417ec52864efc09f1e3ecd0f755cb0daa7604426`; R678-5 covers changed contracts/comments/evidence at the candidate head.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `MILAN_COMPLIANCE_MATRIX.md:221`; `AAF_LATENCY_TAPS.md:105-109`; `REGISTER_MAP.md:1051,1471-1482`; `SUBMODULES.md:242,244`; each mapped 2011 clause/corrigendum and explicit 2020 comparison | R678-5, unchanged R678-4 causes carried | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| RTL | CLEAN | `round5.diff`, `delta-audit.json`: empty hdl/syn/configs delta, identical executable tokens; `KL_render_queue.sv:485-533,915-920`; unchanged pins/resource inputs | R678-5 delta; R678-4 implementation carried | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| Robustness | CLEAN | Per-event/untimed/refusal boundary wording versus queue predicates and `TIME_SYNC.md:400-403`; reset/boot comments at `sim_ax1x1gptp.cpp:1175,1225`; reset execution receipt and retained exclusions | R678-5 delta; R678-4 boundary coverage carried | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| Tests | CLEAN | Both changed simulation comment blocks; dynmap token/AST identity; gptp 185/185, ax1x1gptp 155/0, dynmap 68/68 inventory audit; GM-step 21-entry AST; docs/lint/compile receipts | R678-5 | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |
| Docs | CLEAN | All seven edited documentation files in `round5.diff`; `wording-audit.json`; findings reconciliation; citation table; public assignment/PR/handoff; docs execution/skip ledger | R678-5 | 24a292a0321df6f3516f25cb6e92e24fb1988e65 |

## Limits, integrity and pending manager duties

Hosted snapshot: 45 exact-head jobs, six completed successfully, one physical gPTP job skipped, 20 in progress, 18 queued. Successful selectors do not prove long-bank completion. No hosted acceptance verdict is claimed; `hosted-snapshot.json` retains the observation. `pr-head.json` confirms the published source head and open, ready PR.

No manager source bank exists at this head and none is inferred. The manager must validate the final current-dev merge candidate, publish builder/native-bank receipts, complete hosted/local-replication acceptance, reconcile both independent reviews, obtain merge authorization and perform post-merge containment. Source base is `e26f1816`; designated live dev is `e5b480a385841f19420570bbba7c46da101d1303`. Source evidence alone does not discharge merge-turn work.

The manager retains the public no-TLV edition-policy question and optional suggestion list. Physical calibration is NOT RUN; simulation, field skips and resource/timing reports do not prove the #764 bench method. Issues #632/#764 retain their pending physical acceptance after merge.

`checkout-verification.json` proves all 1,441 root blobs, tracked modes and index match the exact head/tree, independently of index flags. All five required submodules' gitlinks, checked-out heads, bytes, modes and indexes match: processor `93fb0b2d`, timing processor `55680bff`, stream library `48ff7a7e`, stack `70936b77`, lwSRP `08ee86e8`. Unrelated external remains recorded and uninitialized. Git status is clean. No restoration was necessary.

No GitHub write, source fix, commit, push, author contact, merge or other-checkout edit occurred. Reproduction: `fetch_receipts.py`, `audit_delta.py REPOSITORY`, `audit_receipts.py REPOSITORY`. `MANIFEST.sha256` lists publishable scripts/receipts; scratch downloads/extractions are excluded. REPORT.md is the review artifact.

R678-5 FINISHED
