[R639] POSITIVE - exact head 6f86eee604729b80684526fc5b9be720d94f179a

External independent delta review of issue #737 / PR #738, round R639-9. Tree: `32964c6b4b2fc2422ea0f4d05532e2999820240f`. Source base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`. Reviewed delta: `1c4d722cb1d0279f0ec44b0fbe87c810adfb9267..6f86eee604729b80684526fc5b9be720d94f179a`.

All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR was found in this delta. Both previously open guards now require positive identity/provenance or produce a named refusal. The loader error dispatch, accepted-source documentation, realpath restriction and assigned residues are corrected. Optional suggestions below do not revoke coverage. This verdict is source review, not permission to merge or a claim that the completion bar has passed.

The [round-nine assignment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6204018211) and [round-eight class ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6196923564) govern classification: accidental drift in reviewed source; a guard not closed by construction is MAJOR, while a new contrived evasion of a closed guard is RESIDUE. No finding was downgraded to obtain this verdict.

Context was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and public decisions, REQ-VER-02/03/04 and the CI authorities, then full-range path/history mapping and independent delta inspection, then executable evidence. The independent preliminary verdict and five-lens ledger were written before reading prior review findings. No current-round peer report, private author material, management checkout, registry, or other implementation checkout was consulted. Unchanged code retains its previous disposition where the delta does not alter its dependencies.

**Assigned items and cause-level dispositions**

| Item / prior finding | Disposition at this head | Examined implementation and evidence |
|---|---|---|
| Text fails closed: R639-8-F1, R638-8-N1 | CLOSED | `ci/image/exec_operands.py:33`, `:51`, `:85`, `:128`, `:188`, `:230`, `:257`; `exec_files.py:124`; `exec_audit.py:462`, `:848`. Families are assigned from image file identity, including installed versioned names. Each reader returns a program kind or named refusal. Inline/streamed unreadable text is rejected by the final judge; all readable non-exempt text reaches step-text or reviewed-digest comparison. The published 74-control log catches Perl ordinary/bundled/multiple `-e`, Node `-e`/`--eval`/`-p`, Tcl stdin and `tclsh8.6`, unlisted `perl5.38.2`, Python stdin and an unreadable socket. Pinned Perl/Node/Tcl remain clean. |
| Options reading other code | CLOSED for the assigned forms | The same readers refuse Perl `-M`/`-x`, Node `-r`/`-i`, shell `-i`/`--login`, Python `-i`, with matching named results in `round9-final-checks-logs/exec-audit-selftest-image.log`. Options and in-process imports remain subject to the documented reviewed-source boundary, not a claim to analyze all code an accepted program can load. |
| Byte provenance: R638-8-N2 | CLOSED | `exec_files.py:48`, `:124`, `:157`; `exec_audit.py:427`, `:439`, `:449`, `:489`. Image membership requires the snapshotted path and unchanged device/inode/size/mtime/ctime key. A non-image interpreter-shaped filename is judged as a program and needs successful traced-output bytes or a generated-program entry. Directory/basename alone grants no provenance. The author log refuses appended `/usr/local/bin/cp`, appended `python3` with checkout operand, and copied bash named dash. Renamed/installed build outputs, `a.out`, the LeakSanitizer check and the initctl stub remain clean. |
| Dash: R639-8-S1, R638-8-S2 | CLOSED by the public decision and identity binding | Assignment item 2 explicitly accepts the exemption only for the image's dash file. `Image.families` and `Origin.identify` attach `exec_only` to that identity, not the runtime basename. `CI_IMAGE.md:87` accurately distinguishes builtins from loading further executable code. The published binary-symbol control and renamed-bash negative support the boundary. |
| Loader: R639-8-F2 | CLOSED | `exec_audit.py:300`, `:710`, `:717`, `:762`. Target lookup and loaded-program result are separate values. Loader errno is passed to `_respond`, loader refusal retains its own reason, and unexpected judging errors produce a refusal rather than leaving notification handling unguarded. Bash ENOEXEC fallback is represented as a script of the image bash. Published controls cover checkout/generated text without shebang, dash re-exec, binary text, missing interpreter and refused process-filesystem interpreter. No target tuple is converted to an errno. |
| Accepted sources: R638-8-N3 | CLOSED | `CI_IMAGE.md:391` through the source table at `:425`, audit module docstring and `Origin.judge`. File programs, inline text and streamed text have separate source rules. A streamed checkout file is explicitly refused. The PR's Round 9 section corrects the earlier-round streamed-file claim. `exec-audit.json:2` now has only the production Makefile write exception; self-test entries are local `CONTROLS` in `exec_audit_selftest.py:30`. |
| Realpath: R638-8-N4 | CLOSED | `ci_shell_walk.py:325`, `:331`, `:357`; `ci_differential_fixtures.py:73`; `ci_inventory_exact_selftest.py:138`. Resolution is limited to the running script's own unlinked path/ancestor before it runs commands; otherwise output is runtime. The bound `bash-realpath-after-a-program` fixture runs both link targets under the real reference and is refused statically. Own-path and late-path controls accompany it. |
| Comment residue: R639-8-RES1 = R638-8-R1 | CLOSED | `ci_differential_fixtures.py:437` uses the manager's exact replacement: “Probes for workflow environment names, checkout state and local declarations.” No new reviewer/round labels were found in added source comments; executable fixture identifiers are data. Existing historical comments remain tracked by #746. |
| Notify/lookup residue: R638-8-R2 | CLOSED | `CI_IMAGE.md:98` names notification-time judgment and subsequent lookup, including replacement between them. “The call” substitutes for the prohibited word as publicly explained. This is a disclosed boundary, not race-free execution proof. |
| Mask suggestion: R638-8-S1 | CLOSED for the suggested change | `exec_audit.py:117`, `:340`, `:407` anchors masked paths at word starts and stops at `.`/`..` components. The author controls cover temporary paths, held checkout paths, job-written checkout suffixes and traversal components. |
| Population and final check | CLOSED | `exec-audit-receipt.json` records 98 reached / 94 traced steps, 183,831 exec instances, zero findings and every reported exit zero. `round9-final-checks.json` binds 26 successful checks to the reviewed head under CPython 3.12.3, with inventory `--check` last. Source and receipt reconciliation independently verifies in `receipt-check.json`. |

“Refused” for a forbidden program means the audit yields a failing finding; it does not imply every such program was prevented from executing. The local-wheel controls deliberately execute the install and prove it is detected. ABI and non-path controls separately assert refusal before continuation. This distinction is preserved in the verdict.

The new text normalization extends the previously disclosed temporary-path rule to inline/streamed texts and job-written checkout suffixes. It compares reviewed normalized text, not every unmasked path byte. All 103 recorded inline/streamed texts reconstruct to their keys, including source-plus-diff variants; all are visible as used in the aggregate population. All 450 generated entries have source references and reasons. Representative added Tcl entries correspond to the IOB-pack and placement self-test drivers; their source/temporary-file loading remains inside the explicitly reviewed in-process boundary. There is no arbitrary missing-digest acceptance fallback. Public author decision points about this normalization should receive an explicit manager disposition before completion; this review finds the implemented boundary acceptable under the assigned drift threat model.

**Other prior findings retained or resolved**

These are delta carry-forwards, not claims that old full banks were rerun. The prior public rounds and rulings establish their previous closure; the current range was checked for affected dependencies. Any execution/text/provenance cause reopened by later findings is resolved by the table above, not grandfathered.

| Prior finding IDs | Current disposition and cause-level basis |
|---|---|
| R639-1-F1; R638-1-F2 | CLOSED, carried: deterministic normalization and cold-build identity machinery unchanged; new cold receipts retain the same final image identity. |
| R639-1-F3; R638-1-F6; R639-1-F5 | CLOSED, carried: complete lock/archive validation and tool-layer mapping unchanged; the recipe-only lock delta independently recomputes. |
| R639-1-F4; R638-1-F1/F5 | CLOSED, carried: bare-metal declarations and privacy/provenance rules remain in place; current author bare-metal, privacy and documentation checks pass. |
| R638-1-F4/F7/F8/F9/F10/R1 | CLOSED, carried: public version decision, documented environment, recursive CPU closure, download staging, generated package closure and prerequisites persist in CI_IMAGE.md and unchanged recipe helpers. |
| R639-1-F2; R638-1-F3; R639-2-F1; R638-2-F1; R638-3-F1 | CLOSED at their named causes by the closed command/syntax census, followed-source declarations and differential gate. Their later boundary descendants are separately resolved above. |
| R638-2-F2/F3/F4/F5 | CLOSED, carried: fallback package sources, pinned buildx/export metadata path, isolated patch-test identity and documented RV32 location remain unchanged. |
| R639-3-F1/F2/F3; R638-3-F2 | CLOSED, carried: Make selected-target semantics, keyword capability inspection, working-directory tracking and checkout-relative traversal are retained; current exact/pattern/node receipts pass. |
| R639-4-F1/F2/F3/F4; R638-4-F2/F3/F4/F5/F6 | CLOSED for named forms: scope/interpreter/marker/import/capability decisions remain guarded by the census, declaration hashes and differential expectations. The changed substitution path is reviewed directly above. |
| R638-4-F1 | CLOSED, carried: the entity/source-list gate regressions have clean published current population results; no product gate was removed. |
| R639-5-F1/F2; R638-5-F1/F2/F3/F4 | CLOSED, carried: Make precedence/environment cache, live import resolution, bounded substitutions and corrected RV32 procedure persist. Realpath was separately corrected this round. |
| R638-6-F1; R639-6-F1 | CLOSED: declared source pin and all 341 inventory input hashes match; exact-head inventory check is last and passes. |
| R638-6-F2/F3; R639-6-F2/F3 | CLOSED for named Make/shell/reflection cases: bound real-reference fixtures and reviewed capability declarations persist. |
| R638-6-F4; R639-6-F4 | CLOSED at the invocation-judgment cause, including their later text/provenance descendants resolved this round. |
| R638-6-F5; R639-6-F5 | CLOSED: committed reached-population receipt, all 98 reconciliation keys and 115 observed command matches verify. |
| R638-6-RES1 | CLOSED, carried: fresh-home RV32 adoption wording remains explicit in CI_IMAGE.md:834. |
| R639-7-F1; R638-7-N3a/N3b/N3c | CLOSED: declaration scope, workflow environment allowlist, uncertain checkout tests and changed-script observation persist; their differential/control evidence remains bound. N4's realpath analogue is resolved above. |
| R639-7-F2; R638-7-N1 | CLOSED: all assigned interpreter families now reach text decisions/refusals; see N1/F1 above. |
| R639-7-F3; R638-7-N2 ABI/descriptor portions | CLOSED: foreign ABI/x32 and non-path guards unchanged except safer error dispatch; author controls remain clean. |
| R639-7-F4; R638-7-N2 copy portion | CLOSED at the broader cause this round: image membership and interpreter identity no longer depend only on directory/name. |
| R639-7-S1/S2; R638-7-S3/S4 | CLOSED for named suggestions: explicit comparison to 1c4d722c; PYW2 executes its sentinel; normalized initctl identity and option-aware installer subcommand inspection persist. |
| R638-7-S1/S2 = R638-8-S3 | RETAINED OPTIONAL: residue-location correspondence and expected real exit-status assertions. See R639-9-S2 below. |
| R638-8-S4 | RETAINED OPTIONAL: Make prerequisite/built-in applicability still uses walk-time existence outside the changed shell scope. See R639-9-S3 below. |

**Optional findings**

**R639-9-S1 | SUGGESTION | Tests, Docs | `ci/image/exec_audit.py:904`; `ci/image/exec-audit-receipt.json` generated population rows.**

Authority/evidence: the issue requires reproducible public evidence. The aggregate includes generated provenance, but its grouping key omits generated-script digests. The publication includes log digests, not the 94 complete per-instance logs. Therefore the author's statement that all 450 generated entries were used cannot be reconstructed from this aggregate alone. This is an evidence convenience limit, not a demonstrated false execution result, and the omission predates this delta.

Impact: another reviewer can verify entry definitions and source references, but cannot independently count used generated hashes from the selected public packet. Optional outcome: retain the normalized digest in generated rows, or publish a compact digest-to-step use index bound to the raw logs. Verification: derive its set and compare with the reviewed generated list; a planted unused entry must show as unused. No required source change for this verdict.

**R639-9-S2 | SUGGESTION | Tests | `scripts/ci_differential.py:251` and fixture result/status comparisons; carried R638-7-S1/S2 and R638-8-S3.**

Authority/evidence: existing differential results allow located residue and record real statuses, but the carried suggestions request stronger correspondence between the unresolved command and residue location, and explicit expected real statuses. The round-nine diff does not implement those improvements.

Impact: evidence can be easier to interpret and more selective about unintended fixture execution failures. Optional outcome: bind permitted unresolved commands to their residue sites and declare expected statuses per variant. Verification: an unrelated residue location and an unexpected failing real invocation should each fail the fixture. Neither optional improvement is claimed complete.

**R639-9-S3 | SUGGESTION | Conformance, Robustness, Tests, Docs | `scripts/ci_make_walk.py:704`, `:718`, `:753`; carried R638-8-S4.**

Authority/evidence: unchanged Make built-in/prerequisite applicability consults walk-time existence. The governing change named shell tests and realpath; the exec audit judges resulting real programs. No new bypass or current population failure was demonstrated here.

Impact: a later extension could benefit from documenting or differentially exercising prerequisite changes made by an earlier command. Optional outcome: add that fixture and either model, refuse or explicitly delimit the form. Verification: compare both filesystem variants with real Make and the audit. This remains optional under the existing scope and is not reported as newly fixed.

No new RESIDUE item is raised. The previous comment and lookup-boundary residues are closed. Historical review sections in the PR are read as historical; Round 9 is the current correction, not a restatement of the superseded claims.

**Evidence actually verified**

`evidence-verification.json` records 33 downloaded author receipts from [publication 3db87100479e32e4fdb477cad248e5d1fd147a69](https://github.com/kebag-logic/milan-fpga/tree/3db87100479e32e4fdb477cad248e5d1fd147a69/review-evidence/737-image-r1). Every downloaded file matches its publication-manifest SHA-256 and Git blob ID. The publication manifest's own Git blob is also verified. `publication-identity.json` records `verified: false`, reason `unsigned`. No detached signed packet was identified in the supplied evidence subtree. These checks authenticate public bytes to that Git publication; they do not authenticate a signer. No signed-run equivalence is claimed.

`verify_receipts.py` returned zero and produced `receipt-check.json`. It verifies:

- 341/341 inventory source hashes; 45 tool records and 303 residue entries unchanged from 1c4d722c.
- The differential receipt's current-source binding, all 213 fixture definitions/outcomes, and 178 census shapes. The new realpath fixture is included. This checks existing measured evidence; it does not rerun the reference interpreters.
- Recipe `53fb5abd7dc664e8ce168e7c08d5f4b5b09503905ff03fd3fbdf80b394ba2bfa`, exactly as recorded in `receipt-check.json` and the lock.
- Population receipt SHA-256 `56e0a4192f65a6516d6e3e8551dc4193382de962a7ce6b2a4f2ae48c15ae3e6b`; traced source `84caae9af12f01a5fa02c9053d63e3c47c4ee117`, tree `6932e0aad51c48b3e8c24d0c5a187a7011a48bc9`. Only the committed receipt differs between that source and the reviewed head. This is coverage of unchanged executable inputs, not an exact-head re-execution claim.
- All 98 reached-step keys and image-form text hashes reconcile with the current workflows; 94 steps report zero exit and no findings. The four omitted rows are the already accepted Verilator/Yosys cache-miss build replacements: rtl-fast `verilator-lint#3`, `yosys-elaboration#3`, `publication-census#3`, `firmware-verilator#4`.
- All 115 listed commands have observed matches; 111 use the earlier listed arguments. The four differences retain the published base/worker-value explanation.
- All 103 inline program hashes reconstruct; all 450 generated entries name existing generators. Inline use is visible in the population. Complete generated-entry use remains author-reported, as S1 explains.
- 74 PASS lines in the published exact-head audit self-test log, and 26 successful final checks with inventory `--check` last. The logs were read alongside their assertions, including marker absence for ABI controls and expected named findings for text/provenance controls.

The retained `round9-population-docs-check.json` is an exploratory partial receipt with `clean: false`; it is not used as the final successful trace. The committed combined receipt and `round9-population-receipt.json` are the final evidence. This distinction prevents treating an earlier failed collection as the accepted measurement.

The cold-chain log records 411,216 ms and 493,323 ms builds, both image `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`, with successful lock recording and second-export manifest/config/layer verification. The image bytes were not downloaded or rebuilt here. Existing smoke/image/privacy closures are carried where unchanged; the published current privacy and integrity self-tests pass. No full bank was repeated.

`verify_tree.py` returned zero and produced `tree-integrity.json`: exact head/tree, raw tracked blob bytes and executable/symlink modes, index equality, and required registered submodule HEAD/index/blob equality all pass. The four required pins are protocol-processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gptp-processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and tsn-c-stack `405dc68310a18f669049ffc10cc23eef7300dcff`. No tracked source was changed. No execution probe requiring restoration was necessary; only read-only receipt and integrity verification was run.

Reproduction uses the packet's portable scripts, with an exact-head checkout:

```sh
python3 -B verify_receipts.py CHECKOUT PACKET
python3 -B verify_tree.py CHECKOUT
# Optional re-download of only the public files already enumerated:
python3 fetch_receipts.py PACKET
```

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #737 decisions 6160953880 / 6196923564 / 6204018211; REQ-VER-02/03/04; `exec_operands.py:33`, `exec_files.py:124`, `exec_audit.py:427`, `ci_shell_walk.py:325`; receipt-check.json | R639-9 | 6f86eee604729b80684526fc5b9be720d94f179a |
| RTL | CLEAN | source-range-paths.txt and delta-paths.txt; no HDL, firmware, interface, constraint, workflow or gitlink delta; unchanged product-test assertions; tree-integrity.json | R639-9 | 6f86eee604729b80684526fc5b9be720d94f179a |
| Robustness | CLEAN | `exec_audit.py:300`, `:462`, `:659`, `:717`, `:762`; `exec_files.py:157`; interpreter, provenance, loader and mask controls in `exec_audit_selftest.py`; published 74-control log | R639-9 | 6f86eee604729b80684526fc5b9be720d94f179a |
| Tests | CLEAN | `ci_inventory_exact_selftest.py:138`, `ci_differential_fixtures.py:73`, differential-receipt.json, exec-audit-receipt.json, round9-final-checks.json and its logs; portable verification scripts | R639-9 | 6f86eee604729b80684526fc5b9be720d94f179a |
| Docs | CLEAN | `CI_IMAGE.md:62`, `:309`, `:367`, `:425`, `:470`; audit/operand/file docstrings; PR Round 9; author REVIEW READY 6207079152; public scope decisions | R639-9 | 6f86eee604729b80684526fc5b9be720d94f179a |

Each CLEAN row states the applied lens and its evidence. RTL's result is scope-based: no clocks, resets, CDC, FSMs, widths, datapath interfaces or firmware behavior changed. It is not new hardware validation. Later changes affecting these artifacts require renewed coverage.

**Real limits and pending manager duties**

- The image audit addresses accidental drift in reviewed source. Accepted entry programs may load code in-process; input-reading tools retain reviewed inputs; dash has the explicitly accepted identity-bound exemption. Transient checkout restoration and notify-then-lookup replacement remain named limits. Masked text identity is not unrestricted semantic equivalence.
- No Docker/act, host orchestration/self-test, privilege, registry login/push, source fix, commit, GitHub write, hardware access or full parent/processor/gPTP/Yosys/builder bank was performed. No compiler was invoked; the scoped compiler path was therefore not used or claimed as verified.
- The raw 94 per-instance logs and exported image archives were not part of the selected downloaded evidence. Their reported digests are not a substitute for rehashing their bytes. Publication signature verification was unavailable, as recorded above.
- No manager source bank exists at this exact head. None is claimed or inferred. Source execution evidence is the author's published receipts. Physical calibration is NOT RUN; field skips and desk passes are not hardware proof.
- The one exact-head hosted snapshot in hosted-checks.json showed completed success for wire-accountability, bdd-conformance and changes; other observed jobs were queued/in progress. It did not establish completed aggregate/long-gate acceptance. No skipped context was counted as executed evidence. Hosted and act acceptance remain the manager's responsibility.
- At the merge turn, construct and validate the current-dev candidate using the reviewed source head, source base `fa7347fc59173f90e4feec2df207692e6e6e72ec` and the then-current dev tip (assignment tip `734eb780dc93896a5961cd95180f79475a401650`). Run the manager-owned builder/native banks and required local/hosted gates on that candidate, then publish its receipts. Source-head evidence does not prove this merge result.
- Record the public disposition of the author's normalization decision points; carry the optional suggestions without describing them as implemented. Obtain the other independent verdict, ensure no review remains in flight, satisfy publication/adoption/signature requirements in their assigned scope, and obtain explicit merge authorization. Perform the required post-merge containment and issue/project completion work. This review performs none of those steps.

R639-9 FINISHED
