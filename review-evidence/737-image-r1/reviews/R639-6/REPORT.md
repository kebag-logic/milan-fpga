[R639] NEGATIVE - exact head 6918d4f9bee7081a71f94d9090d01c557085658a

External independent review of issue #737 / PR #738, round R639-6. Five MAJOR findings remain. All five lenses were applied; four are UNCLEAN. This report is not merge authorization.

Reviewed tree: `cf35c3b9acfa5215f285a867f39fb583d84f01cc`. Full comparison: `fa7347fc59173f90e4feec2df207692e6e6e72ec..6918d4f9bee7081a71f94d9090d01c557085658a`; round-six comparison starts at `4391f353`. Repository contracts, documentation map, frozen issue scope and public rulings preceded the diff/history and executable evidence. The independent pass and preliminary ledger were written in `independent-first-pass.md` before consulting earlier public review findings. No private author material or other reviewer's private report was used.

The controlling [round-six ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6177332782) requires exact tool semantics or named refusal, followed live imports, and an observed offline execution audit over the reached docs-check/rtl-fast steps. It does not require unlimited emulation. Every new static finding below is an accepted literal form selecting a different script, rather than a refused unsupported form or runtime-assembled residue.

**R639-6-F1 — MAJOR — Conformance, Robustness, Tests, Docs — current inventory cannot validate its own source.**

Artifact: `ci/image/command-table.json:13057`, `ci/image/tool-inventory.json:32`, `scripts/check_baremetal_only.py`; `inventory-check.log`, `inventory-check.rc`, `evidence-verification.json`.

Authority/evidence: the frozen inventory acceptance and closed-table ruling require derivation and comparison at the exact reviewed head. Unmodified `python3 scripts/ci_tool_inventory.py --check` exits 2 with `REFUSED: changed declared script 'scripts/check_baremetal_only.py'`. This reproduces under the reference CPython 3.12.3 as well as the host interpreter. Both declarations record `a402f5167eebaeade7dedef25149aa820856bb29c98d68e45d9bd742c50bffba`; the current tracked file hashes to `bc594d821b947ae1c043b4adff8190014ff4a51ad40af7261bbbc57b26d0b519`. The final source change did not refresh its reviewed declaration/input inventory.

Impact: a clean checkout fails the central inventory acceptance command. A passing recipe-lock consistency check cannot establish a current derived inventory. The published assertion that all source/documentation gates pass at this head is not supported by this command.

Required outcome: review the changed script, reconcile its content-bound declaration and derived inputs, and regenerate affected authenticated records and evidence at the resulting final head. Do not bypass declaration checking.

Verification: current-tree `--check` must return 0 under CPython 3.12.3; generation/comparison and changed-declaration, missing-tool and orphan-tool negative controls must retain their intended behavior.

**R639-6-F2 — MAJOR — Conformance, Robustness, Tests, Docs — explicit-target Make stem selects the wrong script.**

Artifact: `scripts/ci_make_walk.py:589`, `:603`, `:627`; `docs/testing/CI_IMAGE.md:95`, `:137`; `independent-probes.json` entry `make-explicit-stem`.

Authority/evidence: the real-semantics rule applies to the accepted Make automatic-variable shape. With workflow `make` and this literal Makefile, both inventory `--write` and `--check` return 0:

```make
all: probe.c
probe.c: ; bash $*bootstrap.sh
```

The fixture contains benign `bootstrap.sh` and `probebootstrap.sh` containing `r639_unlisted_command`. The walker initializes the stem to empty and sets it only for an implicit pattern rule. GNU Make 4.3 assigns `probe` to `$*` for this explicit target because `.c` is a recognized suffix. The checksum-verified reference Make consequently executes `bash probebootstrap.sh`. For execution only, the unknown command was replaced with a harmless marker, which was observed. No relevant census entry was changed to admit the fixture.

Impact: an accepted literal recipe can hide an installer or other unclassified program in the script Make actually executes. The closed inventory and its exact-semantics documentation are false for this shape.

Required outcome: resolve the selected tool's explicit-target automatic variables exactly, including relevant suffix state, or refuse this shape by name before generation.

Verification: retain this fixture in both modes and compare against GNU Make 4.3. The hidden script must be classified/refused, or the entire unsupported shape must be refused. Existing target-override, implicit-rule and traversal-cache controls must remain passing.

**R639-6-F3 — MAJOR — Conformance, Robustness, Tests, Docs — shell state and function binding select the wrong scripts.**

Artifact: `scripts/ci_shell_walk.py:119`, `:273`; `docs/testing/CI_IMAGE.md:80`, `:137`, `:162`; `independent-probes.json` entries `shell-short-circuit` and `shell-pwd-shadow`.

Authority/evidence: both literal programs below pass inventory generation and comparison while exact Bash 5.2.21 executes the unclassified-script marker:

```sh
X=evil.sh; [ -e missing ] && X=benign.sh; bash "$X"
```

`missing` does not exist. Bash retains `evil.sh`; the walker commits the assignment from the unexecuted right side of `&&` and follows `benign.sh` instead.

```sh
pwd() { echo evil; }; cd "$(cd safe && pwd)"; bash bootstrap.sh
```

The fixture has benign `safe/bootstrap.sh` and unclassified `evil/bootstrap.sh`. The command-substitution recognizer treats the token `pwd` as the builtin, disregarding the same-file function. Bash obtains `evil` from that function and enters `evil`. Execution substitutes only the final unclassified command with a harmless marker after inventory derivation.

Impact: accepted, statically written programs conceal the command population actually executed. Walking both operands without preserving their possible resulting state is insufficient; lexical recognition also cannot establish builtin binding.

Required outcome: model the possible subsequent state and actual command binding exactly, or refuse these shapes. Neither example is permission to broaden runtime residue around an incorrect resolved literal.

Verification: both new fixtures must refuse or resolve the actual scripts in both inventory modes, compared with Bash 5.2. Existing scope, redirected-substitution and repeated-script controls must continue to pass.

**R639-6-F4 — MAJOR — Conformance, Robustness, Tests, Docs — execution audit accepts a real installer and unlisted programs.**

Artifact: `ci/image/exec_audit.py:96`, `:120`, `:131`, `:139`; `docs/testing/CI_IMAGE.md:215`; `audit-pip-probe.json` and audit entries in `independent-probes.json`.

Authority/evidence: the ruling requires the observed audit to catch installers and unlisted programs by name. The ptrace implementation observes `/proc/<pid>/exe` after exec, retains only the first argv for each executable, judges executable basenames without arguments, and removes argv from per-step program records. A real reference CPython 3.12.3 invocation of pinned pip successfully installs a harmless local wheel into disposable storage while the audit returns `findings: []`:

```text
python3.12 -m pip --isolated install --disable-pip-version-check --no-index
  --no-deps --no-compile --target <disposable>/installed <local-wheel>
```

The receipt confirms `installed: true`, exit 0. This uses no package index or dependency resolution. The gap persists for an interpreter in a system directory because its basename is allowlisted and its arguments are ignored.

An ELF copied as `apt-get` is correctly caught. A harmless shebang program with the same name is accepted because the observed executable is its shell interpreter. An ELF copied as `r639_unlisted_program` outside hard-coded system roots is also accepted: every such path is assumed to be a freshly built job artifact without provenance. A separately compiled static binary is observed, confirming the kernel tracer does observe static execution; observation alone does not repair classification.

Impact: the observed backstop does not enforce the declared installer/unlisted-program boundary. It can issue a clean receipt for real installation or an arbitrary supplied executable.

Required outcome: retain and classify relevant interpreter/script invocations and all execution instances, including installer subcommands. Bind any exemption for job-built artifacts to evidence rather than a blanket non-system path. Keep static executable observation.

Verification: run the real local-wheel installation, shebang installer and copied unlisted ELF as negative controls, plus ordinary permitted interpreter calls and a known built artifact as positive controls. Repeat in the image with networking disabled. The supplied tests ran on the host with extracted reference packages, not inside a network-isolated image; that execution limit does not affect the demonstrated classifier omissions.

**R639-6-F5 — MAJOR — Conformance, Tests, Docs — published audit receipt does not cover the required step population.**

Artifact: public `author-r6/round6-exec-audit-receipt.json`, `round6-docs-gate-results.json`, `round6-rtl-gate-results.json`; `docs/testing/CI_IMAGE.md:215`; `evidence-verification.json`, `public-evidence-index.json`.

Authority/evidence: the [class ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6177332782) requires the reached docs-check and rtl-fast steps to run under the observed audit. The published audit contains nine entries: a small compiler setup, three native version queries, three documentation self-tests, a firmware tally self-test and a behavior-runner version query. The separate full-gate records contain 79 docs-check commands and 36 rtl-fast commands, all reported rc 0 at `6918d4f9b`, but no traced program populations for those commands. In particular, docs entry 38, `python3 scripts/check_nvm_capture.py`, is absent from the observed receipt, despite being the live-import path specifically called out by this round.

Impact: the receipt cannot support the required full-population backstop or the claim that only allowlisted programs were observed across that population. Untraced passing gates and a small traced sample establish different facts.

Required outcome: publish complete per-step observed receipts covering the required reached population, with source/image identity and coverage reconciliation. The separate follow-up owns integration wiring; it does not waive the initial evidence required here.

Verification: reconcile the trace step set with the actual inventory-reached docs-check/rtl-fast step set and run all entries offline after fixing F4. Report every exit status, observed invocation population and finding; no unexplained omissions.

**Other results and limits of evidence.**

The reference-interpreter control campaign passed inventory self-tests, pattern tests, syntax-node tests, exact-semantics tests, build tests, integrity tests, privacy tests, patch-provenance tests and recipe-lock consistency. Only the current inventory check failed. Each has a separate `.log` and `.rc`. New Make `override`, shell `select`, Python `async def`, and undeclared network-import probes refuse by name. Missing/orphan inventory and a new workflow-installed tool also fail with the intended diagnostics (`drift-controls.json`).

The former Entity shape/source-list blocker was independently re-executed: Entity shape passed 228 checks with zero failures; the protocol-processor step derived 46 sources and returned 0. The bare-metal gate found zero issues over 1,326 first-party files; its self-test passed 738 arms. The patch test also passed with system/global git identity disabled. These focused gates do not represent a full local docs-check/rtl-fast replay.

The live-import diagnostic first reconciled only F1's stale hash **in memory**, without editing the checkout, to make the underlying graph traversable. It then confirmed `run.py` and `flash_map.py` are followed, that an installer appended to the former triggers changed-declaration refusal, and one appended to the latter triggers undeclared executing/network-script refusal. The external-allowance invariant check passes. `live_gap_probes.py` records this explicit diagnostic workaround; its successful baseline is not a successful unmodified-tree inventory check.

The recipe is multi-stage with separate final copies for the intended groups, a digest-pinned base, verified public source pins, normalized payloads, and authenticated layer/config/manifest validation paths. Build/integrity negative controls passed. Public cold records agree on manifest, config, all 14 layers, all diff IDs and recipe, and those values agree with the current lock. Image digest is `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`; recipe digest is `54cd38dea89d143d3c4ba40e72971be5de3b16592652658659e670f230ad7a29`. This is record verification, not independent authentication of the exported image bytes this round. The consistency-only command correctly prints `image identity UNVERIFIED without --verify-archive`.

All 45 tool identities/pins and workflow provenance sets match rounds three through five. The JSON arrays are not byte-identical: one duplicate RV32 documentation-step provenance entry was removed. That deduplication is not a changed tool or source pin.

The nine published builder groups cover all 103 invocations exactly once at source hash `997e8528ba47199a25376256f1614430586ae574e56db3470c0feeaa706a5c47`, which matches this checkout. The background campaign is rc 0 at earlier source head `18f2df92b13cb3f4036b073ed76940187bf10487` and the earlier image. This is public author evidence at unchanged builder source, not a newly run reviewer bank or manager source bank.

The [live-dev hosted docs log](https://github.com/kebag-logic/milan-fpga/actions/runs/38601263556/job/115980812751) at `f62602531d415d6c1cae1374a3cc2938faf54049` takes the same inert `MAKEFLAGS += -e` skip. Its runner manifest lists Make `4.3-4.1build2`, matching the image pin. This is not an image-induced loss of that mutation arm. The mf48 calibration skip is the permitted absence of the hardware build tree, not hardware proof. The exact-source hosted snapshot distinguishes successful, running and skipped jobs; it is not a final CI acceptance claim.

**Earlier public findings: cause reconciliation.**

Earlier findings were read only after the independent verdict/ledger draft. "Closed" below addresses the named prior defect using current code, controls and identified public evidence; it does not certify every image acceptance criterion or erase the new findings.

| Prior finding(s) | Disposition at this head and evidence |
|---|---|
| R639-1 F1; R638-1 F2: reproducibility | Named normalization defects addressed in install/normalize/build paths; matching cold records and lock verified. No new reviewer image rebuild; archive-byte verification remains a stated limit. |
| R639-1 F2; R638-1 F3; R639-2 F1; R638-2 F1; R638-3 F1: inventory omissions | Prior literal controls are represented in the passing inventory/pattern/node suites, including containers/services and declaration mutations. The cause class is **retained as F1–F3**, not closed merely by enumerating old fixtures. |
| R639-1 F3: weak lock check | Closed at source/control level: schema, source/recipe/layer bindings and mutation controls checked; consistency explicitly distinguishes unauthenticated image bytes. |
| R639-1 F4; R638-1 F1: bare-metal gate | Closed for the named gate: current check and 738-arm test pass. F1 is a separate stale declaration caused by the later gate edit. |
| R639-1 F5; R638-1 F6: layer mapping | Closed at recipe/record level: separate LiteX and grouped Scala copies, 14 corresponding layer records. Actual current archive inspection not repeated. |
| R638-1 F4: tool versions | Reconciled against the public round-two version ruling; CPython 3.12.3 is the reference. Current pins and documented deviations checked; all image binaries not independently executed this round. |
| R638-1 F5: privacy | Source scan, identity table and upstream/unchanged-patch-line provenance controls pass under public privacy rulings. Prior literal cause addressed; final image history/layers not independently rescanned here, so no fresh image privacy certification. |
| R638-1 F7: environment | Removed worker override and documented remaining image environment inspected. Related SDK issue accounted for below. |
| R638-1 F8: recursive CPU tree | Recursive source records/assembly inspected; published closure supports the recursive checkout correction. Not re-extracted/rebuilt here. |
| R638-1 F9: prepare race; F10: hand-selected source roots | Unique temporary downloads and ten-way duplicate control pass; package-root consumer mapping/generator and missing-consumer control checked. Named causes addressed. |
| R638-2 F2: expiring package URLs | Ordered durable fallback and planted primary-404 control pass. |
| R638-2 F3: buildx config key | Authenticated manifest/config lookup replaces obsolete metadata dependency; public cold build evidence supports completion. No local buildx invocation. |
| R638-2 F4: git identity | Closed: fixture supplies its own identity; separate no-global/system-identity test passes. |
| R638-2 F5; R638-5 F4: SDK adoption | Guide now verifies `/opt/rv32-sdk`; home link is compiler lookup only; actual consumers and follow-up step/contract are named. Published adoption verification and require-RV32 gate results support closure of the named procedure defect. Not independently run inside image. |
| R639-3 F1–F3: Make, keyword unpacking, cwd; R638-3 F2: location heuristic | Named regression controls pass; location shortcut removed. Broader wrong-population semantics remain **F2/F3**. |
| R638-4 F1: Entity shape and source-list BLOCKER | Closed: both named commands independently pass at the exact head, with raw logs. |
| R639-4 F1–F4; R638-4 F2–F6: scope/interpreter/startup/xargs/markers/imports/capabilities/location | Named forms covered by passing pattern/node suites and source corrections. Live imports probed explicitly as described. The general exact-resolution cause remains **F2/F3**, rather than blanket closure. |
| R639-5 F1: target override; F2: both traversal caches | Both-mode exact-semantics controls replay command-line collision, target/environment precedence, repeated Make and repeated script with changed incoming state; they pass. These named causes are closed. |
| R638-5 F1: live Python modules | Static live gap closes under the explicit F1 diagnostic workaround: both appended installers caught, external allowance invariant passes. Unmodified current derivation remains F1; observed coverage of the live path remains F5. |
| R638-5 F2: Make P1–P6/P3b/P6b; F3: shell P7 | Passing exact/pattern suites replay the listed assignment, implicit-rule, prerequisite and substitution forms in both modes. Literal old fixtures refuse or resolve as specified; the broader semantic cause is **retained as F2/F3** with new counterexamples. |

Relevant public decisions: [version/layer scope](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162190578), [identity/provenance](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162652582), [patched upstream provenance](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6163057631), [census semantics](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6170640746). Earlier author execution records were read from the [published evidence tree](https://github.com/kebag-logic/milan-fpga/tree/3bd3d9381a3ff301a9669592eca5483683525103/review-evidence/737-image-r1); individual blob identities and hashes are in `public-evidence-index.json`.

**Reviewer-owned coverage ledger.**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1–F5 | Frozen issue/rulings; command table/inventory; all walkers; image recipe/locks; audit; public gate/cold records | R639-6 applied; no clean coverage | `6918d4f9bee7081a71f94d9090d01c557085658a` |
| RTL | CLEAN | Full changed-path list/diff; Dockerfile layer/interface changes; source-list derivation; unchanged workflows, RTL, firmware and gitlinks | R639-6 | `6918d4f9bee7081a71f94d9090d01c557085658a` |
| Robustness | UNCLEAN — F1–F4 | Shell/Make/Python traversal; incoming state/cache/declarations; installer audit; independent literal and negative controls; privacy/build failure controls | R639-6 applied; no clean coverage | `6918d4f9bee7081a71f94d9090d01c557085658a` |
| Tests | UNCLEAN — F1–F5 | Inventory/pattern/node/exact/build/integrity/privacy suites; local gate logs; independent controls; grouped builder census; traced versus untraced public step records | R639-6 applied; no clean coverage | `6918d4f9bee7081a71f94d9090d01c557085658a` |
| Docs | UNCLEAN — F1–F5 | CI_IMAGE guide/census/adoption/audit interface; CI workflow policy; frozen public scope; ready assertion versus source and receipts | R639-6 applied; no clean coverage | `6918d4f9bee7081a71f94d9090d01c557085658a` |

[R639] PASS RTL — `changed-paths.txt`, `ci/image/Dockerfile`, `pp-sources.log`, `restore-check.json` — no product RTL/interface or workflow changes in the full diff; derived protocol-processor source-list step passes and submodule identities are preserved. This is review of this recipe/tooling change's architectural scope, not new hardware, synthesis or timing proof.

No wording-only RESIDUE or optional SUGGESTION is used to downgrade these findings. The documentation defects above assert executable acceptance or measurement coverage and therefore are substantive.

**Execution limits, packet and pending duties.**

The final session restrictions explicitly prohibited Docker/act, privilege, full parent/processor/gPTP/Yosys/builder banks, source edits and external writes. Those restrictions superseded earlier image-execution directions. Accordingly this round did not run image history/layer inspection, an independent cold image build, all image smoke checks, two complete image jobs under `--network none`, or full local docs-check/rtl-fast banks. All five review lenses were applied using source, focused controls and public records; those unexecuted acceptance checks remain limits, not assumed passes. The audit probes use host ptrace with extracted public reference packages. No image privacy certification is inferred from source self-tests. No registry access, publication, merge or author contact occurred.

The manager still owns publication, hosted/act acceptance, the current-dev merge-candidate build and native/builder receipts, final image acceptance evidence and merge authorization. There is no manager source-bank execution at this reviewed head. Source receipts and earlier grouped builder evidence are distinct from the future current-dev candidate. Physical and field skips do not prove hardware behavior. Any corrected head requires affected-lens re-review.

`replay.sh <checkout>` reproduces focused controls using disposable checksum-pinned reference extractions on Linux x86-64 (host Python 3.14+ for package decompression). It never installs shared packages. `run_controls.py` bounds concurrency at four. The other scripts are argument-driven; all disposable data stays beneath packet `scratch/`, which is excluded from publication. Public-record fetch/verification scripts and index identify the evidence inputs; hosted-log extraction is recorded by URL/hash and selected lines in `evidence-verification.json`. Reference versions and package hashes are separate receipts. Raw reviewer logs/rc files are listed in the manifest; `publication-redactions.json` identifies path-only substitutions in two published receipts, with original hashes. Host-interpreter duplicate logs and downloaded public data remain unpublished scratch/support files.

Final checkout verification in `restore-check.json` checks raw tracked bytes and modes for 1,352 parent blobs, the index/tree/head, all six gitlink entries and all five initialized required submodule trees. The optional `external` tree was and remains uninitialized; its recorded gitlink is unchanged. Status is clean and no workflow file changed. There are no outstanding review processes or source modifications.

R639-6 FINISHED
