[R633] POSITIVE - exact head 59354ffe75697e17a16fd117d9ba853e104394bc

Round R633-4, external independent review of issue #734 / PR #735.
Tree: `e732e9f65636bfd49cb9af9844f27077ce037df7`.
Source base: `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`.
All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. Two public-body wording residues and one optional prior suggestion remain. This is a source-review verdict, not merge authorization or complete hosted/replay acceptance.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/734), and the public [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6151273761), [round 2](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6151933918), [round 3](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6152693618), and [round 4](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6153494016) decisions. The authoritative requirement is REQ-VER-04 at REQUIREMENTS.md:314; the relevant interfaces are the CI policy and submodule pin table. The complete ten-file diff, eight commits, and the final two-commit delta were examined. Prior public findings were reconciled after the independent diff pass. No private author material, management workspace, source fixes, commits, pushes, or GitHub writes were used.

The [published execution evidence](https://github.com/kebag-logic/milan-fpga/tree/beeb9d6cbdd2d6abc75f2cb3cc21d9e6f33efa9c/review-evidence/734-r1) was checked against its publication manifest. Nineteen selected published entries and ten exact-head source hashes match. Original author checksums sometimes precede documented path redaction; the outer publication manifest authenticates those published bytes. This is author evidence, not a manager source bank.

[R633] PASS Conformance - `.github/workflows/rtl.yml:97`, `rtl-fast.yml:35`, `elaborate.yml:83`; `scripts/act_ci.py:2376`; `receipts/prior-external.log` - The three selectors implement the amended live-base rule. Hosted scope compares the synthetic merge with its first parent. Replay requires a unique merge base, composes the verified live ref with the PR head, and compares that tree with the live base. The recorded base SHA is metadata only. The scope, standalone-install and control obligations in source acceptance items 1-4 and the later decisions are satisfied. Item 5's complete remote acceptance remains a manager duty.

[R633] PASS RTL - `source.diff`; `.github/workflows/rtl.yml:46`, `rtl-fast.yml:33`, `elaborate.yml:75`; `scripts/act_ci.py:1839`; `receipts/image-comparison.json` - No HDL, configuration, firmware, synthesis input, or gitlink changes. Each scope checkout explicitly fetches full history. The runner fetches the PR head and live dev ref, verifies both, and preserves the base-ref/head bindings consumed by the scopes. Scope outputs, consumer guards and non-PR policies remain compatible. This lens covers the changed CI architecture; there is no changed datapath, clock/reset, CDC, width or FSM logic to review.

[R633] PASS Robustness - `scripts/ci_scope_history.py:17`, :239, :268; `scripts/act_ci.py:6204`, :6381; `receipts/ci-scope.log`, `receipts/prior-external.log`, `receipts/prior-round2.log` - Restored RTL, merge-resolution changes, gitlink restoration, RTL deletion, rename into documentation, gate-read pages, empty deltas, missing revisions, unrelated/ambiguous ancestry and conflicts were checked. Failures cannot publish a docs-only answer. Fixture Git strips inherited Git settings, isolates configuration and home directories, fixes identities/dates, and disables automatic maintenance. Both hostile-signing and hostile-Git-directory controls preserve the victim. Fast push rewind and unknown-before fallback, other non-PR events, and draft behavior remain intact.

[R633] PASS Tests - `.github/workflows/docs.yml:389`; `scripts/act_ci.py:6462`, :6477, :15407; `scripts/ci_events.py:694`, :4086, :6431, :6543; `receipts/runner-workflow.log`, `receipts/mutation-*.log` - The exact CI step executes the ordinary complete selftest and installs only act_ci.py, mode 0555, into an empty directory for the isolated complete invocation with an explicit worktree. The ordinary selftest also launches a complete isolated child; only that launcher is skipped in the child. The formerly escaping unrelated sibling import now fails both forms. Removed history wiring and an in-scope sibling import remain rejected. The predecessor accepts the unrelated import in its ordinary invocation and fails its flat invocation, demonstrating that the Round 4 control detects the reported regression.

[R633] PASS Docs - `docs/testing/CI_WORKFLOWS.md:168`, :674, :688, :1542, :1600; `docs/testing/TESTING.md:1417`; `scripts/act_ci.py:2376`; `receipts/documentation.log` - The live-base rule, frozen-base failure, composition safety argument, environment bindings, fail-closed behavior and complete standalone-install contract match code and executable results. The policy keeps current-dev candidate builder/native banks mandatory before every merge. The stale TESTING.md fail-safe sentence is corrected. Documentation, paths, style, contents/anchors, em-dash, language idiom, source-list and evidence-reader checks pass.

**Executed evidence**

All candidate runner execution occurred inside unprivileged disposable mount/user/PID/network boundaries, with no credentials or network, read-only candidate source, and scratch-only writes. No host runner invocation, live-PR runner invocation, Docker, act, privileged command or full bank was run. Commands remained foreground processes; independent bounded commands ran concurrently.

| Check | Result | Raw receipt |
|---|---|---|
| `ci_scope.py --selftest` | PASS; 197 assertions, 48 killing history controls | `receipts/ci-scope.log` |
| `ci_events.py --check` and `--selftest` | PASS; 2021 contract items, 2860 arms | `receipts/ci-events.log` |
| Exact “Local act runner contract gate” YAML body | PASS; 566 ordinary assertions and 564 isolated-flat assertions | `receipts/runner-workflow.log` |
| Original R632-1 probe, unchanged; unchanged functions at current head | Historical observation preserved; all nine current-head cases pass | `receipts/prior-round1.log` |
| Original R632-2 probe and rename probe, unchanged | Current behavior agrees; historical-oracle differences explicitly graded | `receipts/prior-round2.log` |
| Original R633-2 selector probe, unchanged | PASS; 95 executions at the current head | `receipts/prior-external.log` |
| Documentation and focused contract gates | All invoked commands exit 0 | `receipts/documentation.log` |
| Five source-base/head linked-image pairs | Every ELF byte identical | `receipts/linked-images-accepted.log`, `receipts/image-comparison.json` |
| Linked-image audit controls | PASS; 33 checks | `receipts/image-controls-final.log` |

The historical R632-2 probe expects divergent hosted/replay answers for identical edits already on dev. Its unchanged run therefore exits 1 with exactly three old-oracle misses: all three selectors now correctly return false/false. The wrapper verifies that these are the only misses. The old rename shell script also hardcodes the superseded formulas; its old divergence is retained as a historical observation. Its unchanged fixture helpers were separately exercised through the current shipping selectors, which agree on `docs/reference/REGISTER_MAP.md` with rtl=true. Neither an observational exit zero nor a stale oracle is counted as current success by itself.

The original R632-1 probe uses historical revision constants and can fast-forward its REV fixture. Its unchanged functions were additionally rebound to the current head and all nine outputs graded. The separate 95-execution probe requires synthetic merge first-parent identity and covers both hosted/replay forms.

B16 was reproduced from real Git objects: recorded base `49da9fd9`, PR head `f1b2489f`, and actual landing merge `6c810c45`, whose first parent is `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`. Counts are 64 endpoint paths with default rename detection, 65 with `--no-renames`, and two recorded-merge-base paths. All three current scopes in both modes retain exactly `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`, with rtl=false against that landing base. REV and REV+E retain the restored RTL path and stay relevant.

| Targeted mutation | Ordinary selftest | Isolated flat selftest | Receipt |
|---|---|---|---|
| R01: discard classifier history call | Rejected, rc 1 | Rejected, rc 1 | `receipts/mutation-R01.log` |
| R02: sibling import in unrelated history-wiring branch | Rejected, rc 1 | Rejected, rc 1 | `receipts/mutation-R02-final.log` |
| R03: sibling import inside scope history | Rejected, rc 1 | Rejected, rc 1 | `receipts/mutation-R03.log` |
| R02 applied to predecessor 97907c2e | Accepted, rc 0 | Rejected, rc 1 | `receipts/mutation-before.log` |

The mutation drivers exit 0 only after verifying those expected outcomes. Scope history controls remove frozen-base, composition, relevance, gitlink, empty-delta and ambiguity rules; each associated oracle rejects its mutation. CI-events additionally rejects weakened flat installation, isolation, mode and explicit-worktree wiring.

All five image pairs were rebuilt using the authenticated SDK archive `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`. Sizes are 50,752, 50,752, 50,744, 50,768 and 50,776 bytes for 4x4, 8ch, current, 1x1_tdm8 and 8x8 respectively. Full paired SHA-256 values are in `receipts/image-comparison.json`. Harnesses, configurations and other product inputs are unchanged from the source base; the base comparison uses the same unchanged harness. Absolute hashes differ from the author's compiler build, so only the measured base-to-head equality is claimed.

Setup failures are retained, not counted as passes: the initial mutation launcher had a quoting error, then the R02 anchor matched both a docstring and its literal; the corrected anchored probe passed its expected-outcome checks. Initial image attempts correctly refused writes to the read-only source. The accepted attempt overlays only generated configuration/CSR directories with disposable copies. The original clone remained untouched. The initial author-manifest comparison encountered publication redaction; the final evidence audit uses the published-byte manifest.

**Prior public findings reconciled at this head**

| Prior ID; original severity and lenses | Disposition | Evidence at this head |
|---|---|---|
| R632-1-F1; BLOCKER; all five | RESOLVED | Live-base composition; REV/REV+E, merge-resolution and restored-pointer cases; current and unchanged prior probes |
| R632-1-F2; MINOR; Docs; overlapping R633-1-D1 residue | RESOLVED | Correct four decision/fast bindings, three elaboration bindings and source expressions in policy and CI contract |
| R632-1-F3 / R632-2-S1; SUGGESTION; Tests | RESOLVED | Independent history-wiring check; R01 rejected in both runner forms |
| R633-2-F1; MAJOR; all five | RESOLVED | Entire documented single-file isolated invocation passes; R02/R03 prove loss of standalone support fails |
| R632-2-F1; MINOR; Robustness, Tests | RESOLVED | Hermetic fixture environment and hostile-signing/Git-directory controls |
| R632-2-F2; MINOR; Conformance, Docs | RESOLVED | Actual composed replay paths equal hosted paths for base-side rename and identical-on-dev cases |
| R632-2-R1; RESIDUE; Docs | RESOLVED | CI_WORKFLOWS.md:230 distinguishes empty deltas, PR failures and push fallback |
| R632-3-F1; MINOR; Conformance, Tests | RESOLVED | Entire flat install is CI-run and pinned; unrelated R02 fails ordinary and flat forms |
| R632-3-R1; RESIDUE; Docs | RESOLVED | TESTING.md:1417 states the corrected fail-safe rule |
| R632-2-S2 / R632-3-S1; SUGGESTION; Robustness | RETAINED | Optional hosted merge-shape guard, detailed below |
| R632-3-R2 / R633-3-R1; RESIDUE; Docs | RETAINED | Published PR body still duplicates its closing keyword |
| R633-2-D1; RESIDUE; Docs | RETAINED in updated wording | Published Status still describes the published Round 4 commits as local/pending |

**Retained R632-2-S2 / R632-3-S1. Severity: SUGGESTION. All attributable lenses: Robustness.**

Artifact: `.github/workflows/rtl.yml:123`, `rtl-fast.yml:55`, `elaborate.yml:112`.
Authority/evidence: these hosted branches rely on the documented synthetic-merge checkout without asserting its second parent equals PR_HEAD_SHA. No actual path violating that checkout contract was found.
Impact: an unexpected source-head checkout would classify only its last commit.
Optional required outcome: assert the two-parent merge shape and second-parent identity.
Verification: a head-only multicommit RTL-plus-docs fixture should refuse. This remains optional and does not unclean a lens.

**Retained R632-3-R2 / R633-3-R1. Severity: RESIDUE. All attributable lenses: Docs.**

Artifact: PR #735 body, “Linked Issue / roles”.
Authority/evidence: two consecutive `Closes #734` lines remain in the published body.
Impact: duplicate wording only; the same issue is referenced twice.
Exact required outcome: delete one duplicate line, leaving one `Closes #734`.
Verification: read the updated public body. This is carried to the manager's residue checklist.

**Retained R633-2-D1. Severity: RESIDUE. All attributable lenses: Docs.**

Artifact: PR #735 body, “Status”.
Authority/evidence: the published head is 59354ffe75697e17a16fd117d9ba853e104394bc, but the body says “The two Round 4 commits remain local; publication is pending.”
Impact: stale publication wording only.
Exact required outcome: delete that sentence.
Verification: compare the public body with the published PR head. This is carried to the manager's residue checklist.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue and four decisions; three scope bodies; act_ci.py:2376; exact CI runner step; B16/REV/REV+E receipts | R633-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| RTL | CLEAN | Complete source.diff; full-history checkout and output/consumer contracts; act_ci.py:1839; unchanged product input/gitlink census; paired linked images | R633-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| Robustness | CLEAN | ci_scope_history.py:17, :239, :268; act_ci.py:6204, :6381; missing/unrelated/ambiguous/conflict, push, rename and restoration probes | R633-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| Tests | CLEAN | docs.yml:389; act_ci.py:6462, :6477, :15407; ci_events.py:694, :4086, :6431, :6543; selftest and mutation receipts | R633-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| Docs | CLEAN | CI_WORKFLOWS.md:168, :674, :688, :1542, :1600; TESTING.md:1417; build_event docstring; public issue/PR evidence; documentation receipt | R633-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |

**Limits and remaining manager duties**

The exact-head hosted snapshot is in `receipts/hosted-observation.json`. Successful executed jobs included changes, full-ci-gate, lint, behavior, documentation-without-Git, wire accountability, the AECP mutation job and four synthesis shards; other work remained running. Physical gPTP was skipped. This snapshot is not complete hosted acceptance.

No manager source bank ran at this head and none is inferred. Source-head author receipts and this focused review are distinct from the final current-dev merge candidate. No full parent, processor, gPTP, synthesis or builder bank was executed here; only focused linked-image builds and audit controls were run. Physical calibration was NOT RUN. Desk results and field skips are not hardware proof.

The manager must obtain the other independent verdict, ensure no review remains in flight, run/accept the trusted live-dev replay and exact-head hosted contexts, and validate the current-dev merge candidate with builder and full native banks at the merge turn. The supplied source base and live dev are both a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0; that does not waive a fresh merge-turn check. Preserve the publicly stated 697c-then-696 sequencing, carry the two wording residues, and perform containment/Issue/Project completion only after an authorized merge.

Final integrity compares tracked bytes directly with Git blobs, filesystem modes with tree modes, and every index entry with the tree. It verifies 1308 parent blobs and 562/104/214 blobs in the three required initialized submodules. All five gitlinks remain unchanged; the required pins are protocol-processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gptp-processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. HEAD, tree, index and worktree match the assignment. No source restoration was necessary.

Portable scripts and raw receipts are listed in MANIFEST.sha256. Scratch trees, installations and private-path setup logs are excluded from publication. Only the report and manifest-listed files are publishable.

R633-4 FINISHED
