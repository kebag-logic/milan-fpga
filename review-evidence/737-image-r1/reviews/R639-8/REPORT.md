[R639] NEGATIVE - exact head 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267

External independent review of issue #737 / PR #738, round R639-8. Tree: `bb73b9148913001339b3a7c9cfb00dfbfff5f439`. Source base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`. Reviewed delta: `feef7c9fd239ef62b7c6aad301e80a13275e47ef..1c4d722cb1d0279f0ec44b0fbe87c810adfb9267`.

All five lenses were applied. One MAJOR and one MINOR remain open. RTL is CLEAN; Conformance, Robustness, Tests and Docs are UNCLEAN. The inline-program guard is not closed: ordinary Perl and Node inline invocations can receive a clean verdict without a text digest. A versioned Tcl executable also bypasses interpreter classification. This is failure of the assigned guard, not a contrived evasion of a closed guard.

The public [round-eight class ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6196923564) governs this review. The threat model is accidental drift in reviewed source. The full source-range path set and history were mapped, then the delta and its dependencies independently inspected. Prior public finding text was consulted after that independent pass; the independent verdict and ledger were written before comparison with the other review's full report. No private author material or management checkout was read. Unchanged implementations retain their prior dispositions where this delta does not affect their dependencies.

**Findings**

**R639-8-F1 | MAJOR | Conformance, Robustness, Tests, Docs | interpreter text acceptance has paths that never require a digest.**

Artifacts: `ci/image/exec_operands.py:22`, `:87`; `ci/image/exec_audit.py:417`, `:747`, `:852`; `ci/image/exec-audit.json` program names; `ci/image/exec_audit_selftest.py:98`; `docs/testing/CI_IMAGE.md:391`; PR body, Round 8 interpreter guard. Receipts: `inline-probes.json`, `inline-probes.log`, `inline-trace.jsonl`, `tcl-trace.jsonl`; reproduction: `probe_inline.py`.

Authority/evidence: ruling item 3 and the current author claim require the named interpreter families to accept inline/streamed code only through reviewed text identity. `other_operands()` recognizes Perl/Node `-e` but returns `text: None`. `Origin.judge()` assigns `unreadable`; the final judge rejects `unreadable` only for `stream`, not `inline`. Therefore the ordinary recognized inline form skips the allowlist entirely. Separately, `interpreter()` recognizes `tclsh` but not `tclsh8.6`, although both are permitted program names. The resolved versioned executable is treated as an ordinary named program.

| Probe | Actual execution | Audit result |
|---|---|---|
| `perl -e 'print "marker-traced-perl\n"'` | Marker printed under the real tracer | `clean: true`, no findings, inline provenance `unreadable` |
| `node -e 'console.log("marker-node")'` | Marker printed; invocation passed through the actual classifier/judge | No findings, inline provenance `unreadable` |
| Unlisted Python `-c` control | Marker printed; same classifier/judge | One unpinned-inline finding |
| `printf 'puts marker-traced-tcl\n' \| tclsh` | Marker printed under the real tracer; loaded `/usr/bin/tclsh8.6` | `clean: true`, no findings, ordinary program provenance `named` |

The Perl and Tcl rows are complete host traces, not fabricated event records. The Node/Python comparison is a focused classifier test paired with real interpreter execution. None of these program texts is an approved inline entry or the outer step text. No installer, network operation, shared install, privilege or image run was needed.

Impact: common inline code and streamed Tcl code are authorized without the digest boundary claimed by the source, guide and PR. The existing Python wheel controls pass but do not establish the claimed family-wide property. This can miss accidental in-process installer/fetch behavior; no such harmful behavior was executed by this review.

Required outcome: every named family and actual executable spelling must reach a positive text/provenance decision or an explicit refusal. Unknown/unreadable inline text must never become clean. Add controls for ordinary Perl/Node inline text and the installed versioned Tcl entry, alongside accepted pinned text and existing Python/Bash controls. Correct the claims with the implementation.

Verification: these exact probes must yield named refusals with unlisted text, while approved texts remain accepted. Run the controls in the image and refresh affected population evidence after the fix. Merely adding these marker strings to a denylist does not close the guard.

**R639-8-F2 | MINOR | Conformance, Robustness, Tests, Docs | loader errors use the target tuple as an errno and abort the audit.**

Artifacts: `ci/image/exec_audit.py:282`, `:644-653`; `docs/testing/CI_IMAGE.md:375`. Receipt: `loader-error.json`; reproduction: `probe_loader_error.py`.

Authority/evidence: the documented path boundary says failed lookups/loads return the execution error and run no program. `_target()` returns a path pair in `value`; `_loaded()` puts its outcome value into `program`. If `_loaded()` returns `("errno", ENOEXEC, [])`, `executed()` calls `int(value)` on the old path tuple. The probe opens a real executable text file without a shebang, obtains the actual `ENOEXEC` result, then exercises the actual dispatcher with only target lookup and kernel response stubbed. It raises `TypeError` and produces no response. A missing shebang interpreter uses the same erroneous branch. The refusal branch likewise formats the old tuple instead of the loader's reason.

Impact: an ordinary failed exec can terminate observation without the expected error/receipt and suppress normal shell fallback behavior. This does not demonstrate a false clean verdict or a guard escape, hence MINOR rather than MAJOR.

Required outcome: dispatch the loader's returned errno/reason, preserve the original target identity separately, and retain a named result without an uncaught exception. Cover executable text without a shebang and a missing/refused shebang interpreter.

Verification: the focused probe returns the intended errno through the response path; an integration control receives the expected failure or audited fallback and completes its receipt. Existing target refusals and successful scripts stay unchanged.

**R639-8-RES1 | RESIDUE | Docs | new source comment contains review-session labels.**

Artifact: `scripts/ci_differential_fixtures.py:424`, the added comment beginning `# R638-7 and R639-7 probes`.

Authority/evidence: the owner's source-comment rule in this assignment prohibits new reviewer IDs/round labels in source comments and classifies new instances as RESIDUE. Impact is wording only; fixture identifiers and outcomes need not change. Exact fix: replace the comment with `# Workflow environment, checkout-state and local-declaration controls (#737; REQ-VER-04).` Verification: inspect the added comment in the delta; leave executable fixture data unchanged. This does not affect cleanliness.

**R639-8-S1 | SUGGESTION | Docs | make the disclosed dash scope decision explicit.**

Artifacts: `exec_operands.py:16`, `exec_audit.py:422`; `CI_IMAGE.md:90`, `:412`; author [REVIEW READY, open point 1](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6203674207).

Evidence: the author explicitly asks for a decision because `dash` text is exempt despite the ruling's literal “every” inline/streamed program. The implementation instead judges its child execs and checks absence of dynamic-loader imports. Impact: a future reviewer cannot tell whether that narrower boundary was accepted. Requested outcome: record its public disposition and replace “runs nothing in-process” with precise wording about shell builtins versus loading additional executable code. Verification: the public decision and guide describe the same boundary. This review does not silently approve a scope amendment. The manager should resolve the author's declared decision point before completion.

**Guard-by-guard assessment**

| Assigned guard | Result and artifact-specific evidence |
|---|---|
| 1. Exec ABI | Closed at the reviewed filter/dispatcher: `exec_audit.py:89`, `:621` route every foreign architecture and x32 call to refusal before continuation. The authenticated-by-hash author self-test log records i386/x32 refusals; test code asserts marker absence. Static-output and LeakSanitizer controls pass. No compatibility execution campaign was repeated. |
| 2. Non-path exec | `resolve()`, `_target()` and `_same_file()` require a regular executable path, reject `/proc`/`/dev` traversal and bind caller/observer inode+device identity. Memfd, deleted-fd and descriptor-link controls refuse in the published image log. F2 remains in the separate loader-failure dispatch path; no target escape was found. |
| 3. Interpreter programs | NOT CLOSED: F1. All 81 reviewed inline texts reconstruct to their keys, including 18 source-plus-diff variants; that verifies the list, not enforcement on paths that skip it. The published local-wheel `-c` and stdin controls and pinned harmless Python/Bash controls pass. |
| 4. Positive provenance | `Origin.started_exec()` records declared compiler/linker outputs, and `ended()` accepts changed executable bytes only at successful exit. Built digests survive rename/copy. The 334 generated entries name existing generators and reasons; temporary-path masking is explicit. Published appended-byte, unchanged-copy and failed-build negatives refuse; compile/rename/install positives pass. No creation-time/byte-inequality fallback remains. |
| 5. Workflow environment | `ci_syntax.py:40` rejects exported functions/hooks before requiring membership in the 25-name census. `ci_tool_inventory.py:201` applies it to merged workflow/job/step environment. Bound differential outcomes refuse nine named hooks, exported functions and an unknown name. |
| 6. Walker and followed bytes | `ci_shell_walk.py:563` expands declaration initializers before introducing locals and preserves repeat declarations; six named cases resolve identically and the append case refuses. `certain():422` no longer treats checkout-dependent tests/cd as certain. The if/or removed-directory variants refuse. `Origin.judge():446` checks checkout scripts at exec; `sweep()` watches followed inputs, with the named intentional-write exception. Published rewritten and sourced-file negatives refuse. |
| 7. Documentation | Threat model and guard table are present. F1 and F2 contradict executable claims. RES1 and S1 collect the additional wording/scope observations in this report. |
| 8. Reached population and final check | Verified receipt/set/source reconciliation: 98 reached, 94 traced, 183,834 execs, every reported exit 0 and no reported finding. Four image-replaced cache-miss builds remain explained. The author records 26 exact-head checks under Python 3.12.3, with inventory `--check` last. Clean receipt interpretation remains limited by F1. |

**Published evidence and its limits**

`evidence-verification.json` verifies 40 fetched files against their Git blob identities, and the 39 author files against the publication manifest's SHA-256 values at [evidence commit dedfaa3f](https://github.com/kebag-logic/milan-fpga/tree/dedfaa3fce9db0b1e7ac2b10ec970f5158fff756/review-evidence/737-image-r1). The publication manifest itself is bound by its Git blob. The commit API reports `verified: false`, reason `unsigned`; no detached signature files were found in the supplied evidence subtree. These are verified public bytes, not a verified signed packet. No signer authentication is claimed.

The committed population binds parent `c2531c6346238750cdb92e11a6464b905b1a3323`, tree `69b94ed62cee74e45a4d11d3bdd30d1f2b1e3650`. Its difference to the reviewed head is only `ci/image/exec-audit-receipt.json`. The parent trace therefore covers unchanged executable inputs at this head; this is not an exact-head re-execution claim. The 46-step public docs receipt and combined 94-step receipt agree with their recorded hashes. All 98 step keys and transformed-text digests reconcile with current workflow inputs. The four untraced steps are `verilator-lint#3`, `yosys-elaboration#3`, `publication-census#3` and `firmware-verilator#4`, all in `rtl-fast.yml`, all named cache-miss build replacements. The 115 listed commands have 115 recorded observed matches, 111 with the earlier listed arguments; the other four retain the already explained base/worker-value differences. The raw 94 per-instance logs and full separate rtl receipt are not in this selected public evidence, so their bytes were not independently re-hashed.

The differential receipt binds all 211 current fixture definitions and 178 census shapes. Its source binding and expected outcomes verify. The 341 inventory input digests match this checkout. All 45 tool records and 303 residue entries equal the previous reviewed head. `reviewed-lists-check.json` reconstructs all 81 inline hashes; generated-program source references were checked and selected controls inspected, but all 334 generated programs were not regenerated.

Cold logs show 463,836 ms and 446,068 ms builds, image `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`, config `sha256:a2c4d52af85bc218ddd2d3958a2283f64ab175ec4254960eba891ae2271df1fd`, and size 3,930,997,226 bytes. The first lock-record attempt failed because the base archive was absent; the retained second chain records successful lock recording and second-export verification. The lock's recipe `4f7a0b3b84da7816d8cb1d21f1d87905c771748127a83820f4b86d727a17dd44` independently recomputes. The two byte-identical 1,135,069,184-byte exports are author-reported; archive bytes were not available to this review. Smoke has 133 records: 97 command results, 35 package versions and one interpreter record, ending PASS. The full image was not rebuilt or re-certified here.

**Prior findings at this head**

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R639-7-F1 | CLOSED: initializer expansion and same-function re-declaration corrected in `declaration()`; six matching real-reference cases and one append refusal are bound to current source. |
| R639-7-F2; R638-7-N1 | Python wheel manifestations CLOSED by both published controls. Broader interpreter-text cause RETAINED as R639-8-F1: the assigned family-wide guard still has unconditional acceptance paths. |
| R639-7-F3; R638-7-N2 ABI portion | CLOSED: foreign-architecture/x32 filter and notification rejection, plus both marker-absence controls. |
| R638-7-N2 descriptor portion | CLOSED: path resolution and same-file check replace dropped unresolvable execs; memfd/deleted/link controls refuse. F2 is a separate error-dispatch defect, not a demonstrated descriptor escape. |
| R639-7-F4; R638-7-N2 copy portion | CLOSED: output-at-success digest provenance replaces inequality; exact/appended copies and failed output refuse, build/rename/install positives pass. |
| R638-7-N3a | CLOSED: environment allowlist plus named exported-function/hook negatives. |
| R638-7-N3b | CLOSED: no certain checkout-state branch; both removed-directory variants refuse. |
| R638-7-N3c | CLOSED for the named rewritten-script cause: exec-time digest and followed-input watch; rewritten/sourced controls refuse. Reviewed intentional writes and transient restoration remain disclosed boundaries. |
| R639-7-S1 | No required change: current 45-tool/303-residue comparison now has an explicit previous-head baseline in this report. |
| R639-7-S2 | CLOSED: PYW2 loads its module, real status is 0 with a sentinel, and the walker refuses. |
| R638-7-S1/S2 | RETAINED optional test improvements: residue-to-location correlation and expected real exit statuses. Neither is claimed implemented. |
| R638-7-S3/S4 | CLOSED for the named forms: joined system paths are normalized; `subcommand()` skips leading options/toolchain selectors, with a cargo control in the published log. |

The ruling states every round-six finding was resolved. The unchanged cause-level closures remain carried: R638-6-F1/R639-6-F1 declaration pin; R638-6-F2/R639-6-F2/F3 named Make/scope cases; R638-6-F3 reflection/import capability; R638-6-F5/R639-6-F5 reached population; R638-6-RES1 fresh-home RV32 link wording. The broader execution-boundary ancestry R638-6-F4/R639-6-F4 remains subject to F1 here.

Earlier closed normalization, source/layer identity, privacy/version/environment, CPU closure, download concurrency, URL fallback, metadata lookup, RV32 procedure, entity/source-list, live-import, Make precedence/cache and named command-resolution findings retain their dispositions under the delta rule. In particular, the unchanged image recipe/pin infrastructure, Make/Python walkers, bare-metal declaration, product sources and gitlinks were not reopened merely to repeat banks. Changed shell and execution-audit dependencies were reviewed above rather than grandfathered.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | ruling 6196923564; exec audit/operand reader; syntax census/walker delta; public source and population receipts | R639-8 applied, no clean coverage | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| RTL | CLEAN | full-diff-paths.txt; Dockerfile and source-lock boundaries; recipe-only image-lock delta; smoke receipt; restore-check.json | R639-8 | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| Robustness | UNCLEAN: F1, F2 | ABI/target/provenance/text/error branches; inline-probes.json; loader-error.json; declared-scope controls | R639-8 applied, no clean coverage | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| Tests | UNCLEAN: F1, F2 | 211 bound differential outcomes; 41 published audit controls; actual Perl/Tcl traces; Python/Node classifier contrast; loader-error probe | R639-8 applied, no clean coverage | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |
| Docs | UNCLEAN: F1, F2 | CI_IMAGE.md threat-model/guard/error claims; PR Round 8; REVIEW READY; evidence source identities and limits | R639-8 applied, no clean coverage | 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267 |

[R639] PASS RTL - `full-diff-paths.txt`, `ci/image/Dockerfile`, `ci/image/image.lock.json`, `evidence/author-r8/round8-image-smoke.log`, `restore-check.json` - The full source range changes no product RTL, firmware implementation, workflow, interface, product-test assertion or gitlink. The round-eight image manifest/config/layers remain unchanged; its recipe binding changes with the walker. No new CDC, reset, timing, synthesis or physical proof is claimed.

**Real limits, restoration and pending duties**

`execution.json` records host probe identities: Python 3.12.13 for audit probes, Perl 5.42.2, Node 22.23.2 and Tcl 8.6.16. Receipt reconstruction used Python 3.14.7. These are not the image's reference versions; the author's exact-head checks and differential receipts identify Python 3.12.3 and the image tools. The failure in F1 is in the unchanged Python classification branches, with real host traces as falsification, not a replacement population run. The probes requested no network, but did not run inside a disabled-network container. No full audit self-test was executed on the host because it writes system directories.

No full parent/processor/gPTP/Yosys/builder bank, hardware run, image build, registry login/push, Docker/act, host orchestrator/self-test, source fix, commit, external write, author contact or sub-agent occurred. The source-head gate receipts are the author's evidence; there is no manager source bank at this head. Physical calibration NOT RUN and field skips are not hardware proof. Hosted/act acceptance was left to the manager, with no inference from skipped contexts.

`restore-check.json` proves all 1,362 superproject tracked blobs by raw bytes and modes, exact index tree, all six gitlinks, and five required initialized submodules. Their 104/562/65/78/214 blobs, modes and index trees match their pins. The unused external gitlink is unchanged and remains uninitialized. Source edits/restoration were unnecessary. Disposable probe trees remain under this packet's `scratch/` and are not published.

The manager still owns finding resolution and affected-lens re-review; disposition of the disclosed dash boundary; the final merge candidate on current dev `973e681be51882840670b8bc566f02b8005b1996`; builder/native candidate banks and linked receipts; hosted/act acceptance; registry publication and digest round-trip; completion of both independent reviews; explicit merge authorization; and post-merge containment/public closure. This report supplies no candidate-merge validation.

Portable scripts and raw selected receipts are enumerated in `MANIFEST.sha256`. Publish only those files and this report. `replay.sh` reproduces the focused probes and read-only evidence checks with installed dependencies; no campaign or source mutation is scheduled.

R639-8 FINISHED
