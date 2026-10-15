[R639] NEGATIVE - exact head feef7c9fd239ef62b7c6aad301e80a13275e47ef

External independent review of issue #737 / PR #738, round R639-7. Four MAJOR findings remain. All five lenses were applied. RTL is CLEAN within this image/tooling delta's scope; Conformance, Robustness, Tests and Docs are UNCLEAN. This is not merge authorization.

Reviewed tree: `4f1e8d01c600c2bdb5ba5ea6ec64a5d5e7f1b808`. Full scope comparison: `fa7347fc59173f90e4feec2df207692e6e6e72ec..feef7c9fd239ef62b7c6aad301e80a13275e47ef`; detailed delta starts at `6918d4f9bee7081a71f94d9090d01c557085658a`. Contracts and the documentation map preceded public scope decisions, authorities, source diff/history and executable evidence. The controlling [round-seven assignment](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6183738772) sharpens the [round-six class ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6177332782): accepted forms require real-tool differential evidence, and the observed audit must judge complete invocations with provenance.

The independent source pass and local-declaration, inline-install and compatibility-exec probes preceded consultation of round-six public findings. There is a procedural limit: complete round-six comment bodies, including other report sections, were displayed before the written preliminary ledger. This did not meet the requested write-before-reading-report sequence. `independent-pass.md` records that deviation. No private author material, private review report, management source bank or lane scratchpad was read.

**R639-7-F1 | MAJOR | Conformance, Robustness, Tests, Docs | local declarations resolve a different script from Bash.**

Artifact: `scripts/ci_shell_walk.py:578`, especially `:603-605`; `scripts/ci_differential_fixtures.py:126`; `docs/testing/CI_IMAGE.md:139`, `:180`; `walker-probes-reference.json`.

Authority/evidence: assignment items 1-2 require exact resolution or named refusal, not a false literal. The declaration handler clears each local before expanding its initializer. Bash 5.2.21 expands that initializer using the previously visible value. Re-declaring an existing local without assignment also preserves its value. The walker resolves an empty string in both cases. Both probes use only shapes already in the 177-entry census.

The production generation/comparison probe, with the census gate enabled and unmodified source, is:

```sh
X=evil
f() { local X="$X"; bash "${X}bootstrap.sh"; }
f
```

`bootstrap.sh` contains `true`; `evilbootstrap.sh` contains `r639_hidden_command`. Inventory `--write` and `--check` both exit 0, following the benign script. The checksum-verified distribution Bash 5.2.21 executes the hidden command, replaced only at execution time by a harmless recording stub. CPython 3.12.3 runs the unmodified walker. Simpler probes record walker `""` versus real `"outer"`, and walker `""` versus real `"first"`. The committed local-declaration focus fixture observes values after the function returns, so it misses this defect inside the function.

Impact: an accepted literal shell form hides another script and its commands while both inventory modes pass. The passing focus fixture does not prove the authorized declaration semantics.

Required outcome: preserve Bash's expansion/re-declaration behavior or refuse these forms before generation. The focus fixture must observe the local value and selected script inside the function, including same-name initialization and repeated declaration. Correct the exact-resolution claim alongside the implementation.

Verification: replay `probe_walk.py` against Bash 5.2.21. The hidden script must be followed/refused, or the unsupported declaration must refuse by name. Keep the production census gate enabled and retain branch, loop and function-shadow controls.

**R639-7-F2 | MAJOR | Conformance, Robustness, Tests, Docs | inline interpreter programs are accepted without judging their code.**

Artifact: `ci/image/exec_audit.py:419-431`, `:483-501`; `docs/testing/CI_IMAGE.md:309-313`, `:400`; `audit-probes.json`, entries `explicit-module-control` and `inline-local-wheel`.

Authority/evidence: assignment item 3 requires interpreters to be judged by their inline program. `invocation()` reduces inline execution to the interpreter basename/path, and `judge()` performs no inline-program classification. Full argv is retained but its program text is not judged.

A real harmless local wheel was installed through `python3 -c` calling `pip._internal.cli.main.main(...)`, under CPython 3.12.3, with `--no-index --no-deps --no-compile --disable-pip-version-check --target <probe>/inline-installed`. The step exits 0, the installed package exists, and findings are empty. The paired `python3 -m pip` call installing the same wheel correctly produces an installer-module finding. No shared environment or package index was used. Exact code and full argument vectors are in `probe_audit.py` and its receipt.

Impact: the observed backstop certifies a real installer as clean. This retains the cause of both round-six F4 findings despite correcting the explicit `-m pip` example.

Required outcome: judge inline/streamed programs through an explicit reviewable program boundary, or refuse opaque programs. An allowlisted interpreter alone must not authorize their contents. Add this local-wheel variant as a negative control and document the boundary actually enforced.

Verification: both local-wheel paths must be rejected by name or a precise unsupported-program refusal without network access. An explicitly permitted harmless inline program must remain accepted. Preserve full-argv logs.

**R639-7-F3 | MAJOR | Conformance, Robustness, Tests, Docs | compatibility-ABI exec calls bypass the tracer.**

Artifact: `ci/image/exec_audit.py:55-63`; `docs/testing/CI_IMAGE.md:302-304`; `audit-probes.json`, entries `direct-installer-name-control` and `compat-exec`; assembly embedded in `probe_audit.py`.

Authority/evidence: the audit must retain every exec instance, including static programs. The new filter deliberately returns ALLOW for a non-x86-64 syscall architecture. A small static i386 trampoline was assembled and linked inside the traced job, then used `int 0x80` to exec a harmless shebang stub named `apt-get`. The stub only writes a marker.

The direct stub call is refused as `installer executed: apt-get`. Through the trampoline, the marker exists, the step exits 0, and findings are empty. Only four instances appear: shell, assembler, linker and trampoline. The `apt-get` exec is absent. This probe uses no privilege, container orchestration, package installation or hardware.

Impact: a static program can execute an installer-named or unlisted child without an invocation record. Classification cannot repair an event the filter never delivers; the every-exec claim is false.

Required outcome: observe/decode supported compatibility exec ABIs, or fail closed on unsupported execution architectures/syscall variants. Preserve static-program and sanitizer support. Add the trampoline as an observation/refusal control.

Verification: the marker-producing child must appear and be refused, or the unsupported ABI must refuse before it runs. A clean receipt with the marker present and child absent must fail. Repeat in the image with networking disabled before replacing population evidence.

**R639-7-F4 | MAJOR | Conformance, Robustness, Tests, Docs | a changed copy is mistaken for a program built from job inputs.**

Artifact: `ci/image/exec_audit.py:190-214`, `:240-251`; `docs/testing/CI_IMAGE.md:323-326`; PR body, Known limitations and Round 7; `audit-probes.json`, entries `copied-elf-control` and `modified-copied-elf`.

Authority/evidence: assignment item 3 requires provenance from the traced job's in-tree inputs or inventory membership. The fallback accepts a recently changed file if its complete digest differs from every pre-existing executable. That proves byte inequality, not origin.

```sh
cp /usr/bin/printenv unlisted2
printf '\0' >> unlisted2
./unlisted2 --version
```

No compilation or linking occurs, and appending the byte leaves the copied ELF executable. The audit returns exit 0, no findings, and provenance `written during the job`. The paired exact-copy control is refused as `program without provenance: unlisted`. Only version output is requested; no environment values are printed.

Impact: a trivially transformed pre-existing executable escapes the unlisted-program boundary. The PR body discloses that transformed files are not distinguished, but disclosure does not satisfy or relax the public provenance requirement.

Required outcome: require positive provenance that survives this case, or refuse programs whose provenance cannot be established. Creation/change time plus absence of an exact byte copy is insufficient. Preserve valid compiler outputs, renamed build outputs and approved generated scripts.

Verification: exact and appended-byte copies must both refuse unless explicitly inventoried. Positive build/rename/copy controls must remain accepted. Re-run the population under the corrected rule and disclose any newly exposed provenance gaps.

**Round-seven acceptance and public evidence.**

`public-evidence-verification.json` verifies 21 selected author receipts against the published SHA-256 manifest and Git blob identities at [evidence commit d43f00d7](https://github.com/kebag-logic/milan-fpga/tree/d43f00d766c5b052515c686022da31d17c45ed0c/review-evidence/737-image-r1). Copies are under `evidence/`; `receipt-reconciliation.json` compares them with this checkout. This proves hash identity, not signer authenticity: the supplied commit reports `verified: false`, reason `unsigned`, and no detached signature was found in the supplied evidence tree. No signed-packet verification is claimed.

| Assignment | Result | Examined artifacts |
|---|---|---|
| 1: differential acceptance | Exactly 177 applied shapes and 188 matching fixture expectations; machinery passes. Semantic acceptance remains F1. | census, receipt, `ci_differential.py`, fixtures; `census-selftest.log`; real Bash probe |
| 2: uncertain state and names | Named short-circuit/shadow causes fixed. Runtime joins, loop state iteration and function-name separation checked. Local declarations remain F1. | `ci_shell_walk.py:124`, `:608`, `:632`, `:735`, `:912`; committed branch/loop/shadow fixtures |
| 3: complete invocation audit | Explicit module/shebang and full-argv improvements hold. Inline classification, compatibility observation and transformed-copy provenance remain F2-F4. | `exec_audit.py`, allowlist, published 20-control log, paired probes |
| 4: full population | Missing-population cause addressed at receipt/set level; clean interpretation remains conditional on F2-F4. | committed receipt, `audit_population.py`, author retrace/population records, independent reconciliation |
| 5: declaration re-pin | Closed for the named stale declaration. Bytes, declaration and recorded input agree; CPython 3.12.3 inventory check exits 0. | command table, bare-metal diff, inventory; `inventory-check-last.log`; author final `--prepare-only` result |

The bare-metal declaration SHA-256 is `3d10365d3c399071b2e41949b2ef813c0b2b4aaf1de432346779328726b54e06`. The actual policy check reports zero findings across 1,333 files; its self-test passes 738 arms.

There are **98 reached run steps**, not 115 steps. The earlier **79 + 36 = 115** entries are listed commands within them. The committed receipt contains 94 traced steps, every exit status 0, zero reported findings and 183,845 instances. All 115 listed commands have observed matches; 111 have the listed arguments. The other four differences are full versus abbreviated base SHA and three workflow `--jobs 16` values versus manually listed 1/4 values. These are explained differences, not missing commands.

The four **reached but not traced** steps are:

| Step key | Omitted operation | Disposition |
|---|---|---|
| `.github/workflows/rtl-fast.yml#verilator-lint#3` | Verilator cache-miss build | Acceptable replacement by the pinned image layer |
| `.github/workflows/rtl-fast.yml#yosys-elaboration#3` | Yosys cache-miss build | Acceptable replacement by the pinned image layer |
| `.github/workflows/rtl-fast.yml#publication-census#3` | Yosys cache-miss build | Same replacement; no test omitted |
| `.github/workflows/rtl-fast.yml#firmware-verilator#4` | Verilator cache-miss build | Same replacement; no test omitted |

The omissions agree with `image_form()` and the reconciliation. This accepts the documented image-adoption population; it does not claim unchanged source workflows themselves skipped those builds. Installation/fetch transformations are recorded. The source step set and transformed-text hashes agree. `check_nvm_capture.py` appears in docs-check step 27's observed population.

The committed population names parent `afdf0ef0c6b25888d40641e6933fe77eec16bd18`; its tree identity verifies. Published exact-head docs retrace has 46 clean steps. The all-head comparison reports 94 clean steps with matching command/set/population identities; two instance counts change, 15,557 to 15,550 and 307 to 306. That is an author comparison receipt. The complete rtl retrace and raw instance logs named by digest are not available in the selected public packet, so their bytes were not independently re-hashed.

Both cold receipts agree with the lock on image `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`, config `sha256:a2c4d52af85bc218ddd2d3958a2283f64ab175ec4254960eba891ae2271df1fd`, recipe `b3fdd9003ee3ba95176f83d4bfd390c6be94841a10e5dacca2863e6ac056ae68`, and size 3,930,997,226 bytes. Times are 473,918 and 424,315 ms. The public chain records successful export authentication for both. Two no-cache builds and byte-identical 1,135,069,184-byte archives are author-reported; this review verifies matching identities and verification logs, not independent archive bytes or cache behavior. The local consistency command correctly leaves archive identity unverified.

Smoke evidence has 133 JSON records: 97 command records, all rc 0, 35 package-version records and one interpreter record, ending `PASS: all image tool families`. The lock retains 14 layers including the base; only system, gtest and validation payload digests differ from round six. The GNU time pin and smoke addition agree. All 45 tool records equal round six. Runtime residue grows from 281 to 303 entries, with 22 additions and none removed; that is separate from tool-record equality.

**Prior findings, explicitly reconciled.**

The [R639-6](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6183445346) and [R638-6](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6183731799) public finding sections are preserved in `prior-round-findings.json`. Current individual prior-probe outcomes are in `receipt-reconciliation.json`.

| Prior finding(s) | Disposition at this head |
|---|---|
| R639-6-F1; R638-6-F1 | CLOSED: reviewed gate bytes, declaration, input and recipe agree; exact-head inventory check passes. |
| R639-6-F2 | Explicit-rule `$*` cause CLOSED: `ci_make_walk.py:297` refuses it; named differential fixture is measured. Broader accepted-semantics cause remains F1. |
| R639-6-F3 | Short-circuit and `pwd` shadow causes CLOSED: runtime joins and scope names replace false literals; both named fixtures refuse. Broader state cause remains F1. |
| R638-6-F2 | Named M1-M5, M20-M21, S1/S3/S5/S6 causes CLOSED: exact conditional words, recursive environment values, `call` binding, lexical `abspath`, shadow-aware substitutions and option refusals. M/S fixture outcomes verified. Broader semantics cause remains F1. |
| R638-6-F3 | Namespace/reflection cause CLOSED: `ci_python_walk.py:285-332` detects dictionaries, `sys.modules` and executing builtin attributes; PYW1/PYW2/PYW4/PYW6 refuse as undeclared executing scripts. S2 below is a limited test improvement. |
| R639-6-F4; R638-6-F4 | RETAINED as F2-F4. Explicit `-m pip`, shebang installer and exact-copy cases now refuse; other installer/provenance paths still pass, and one ABI loses observation. |
| R639-6-F5; R638-6-F5 | Missing committed/full-population cause CLOSED: 94/98 reconciliation and 115/115 command matches exist. Their clean judgment is not approved while F2-F4 remain. |
| R638-6-RES1 | CLOSED: `CI_IMAGE.md:700` says `ln -s` fails if the destination exists and requires a fresh job home. |

Earlier dispositions are carried only where the delta leaves their causes/dependencies intact, under the requested delta-review rule:

| Earlier finding group | Disposition |
|---|---|
| R639-1-F1 / R638-1-F2; R639-1-F3; R639-1-F5 / R638-1-F6 | Normalization, lock and layer source corrections remain closed; new cold identities and consistency checked, with archive limits above. |
| R639-1-F4 / R638-1-F1 | Bare-metal cause closed; touched masks/re-pin and current policy controls independently checked. |
| R638-1-F4/F5/F7/F8/F9/F10 | Version, privacy, environment, CPU closure, download-race and source-root corrections retained. Pins, package-root delta and smoke checked. Unchanged privacy/closure logic retains prior disposition, without fresh whole-image privacy certification. |
| R638-2-F2/F3/F4 | URL fallback, metadata lookup and fixture-identity corrections retained; implementations unchanged. |
| R638-2-F5 / R638-5-F4 | RV32 procedure closure retained: verify `/opt/rv32-sdk`, use fresh-home compiler link, name adoption step/contract. RES1 also fixed. |
| R639-1-F2; R638-1-F3; R639-2-F1; R638-2-F1; R638-3-F1 | Named inventory corrections retained; general wrong-population cause remains F1. |
| R639-3-F1-F3; R638-3-F2; R639-4-F1-F4; R638-4-F2-F6 | Named resolution/scope/interpreter/import corrections retained in current controls/receipts. Changed state/execution-boundary causes remain F1-F4. |
| R638-4-F1 | Entity/source-list blocker stays closed: product/source-list artifacts unchanged; current population records their gates. No new product bank claimed. |
| R639-5-F1/F2; R638-5-F2/F3 | Named precedence/cache/Make/substitution controls retained in author exact/pattern checks. General accepted-semantics cause remains F1. |
| R638-5-F1 | Live-import closure retained; in-tree search-path/declaration maintained. Current derivation succeeds without a stale-pin workaround. |

**Optional improvements, with no effect on the verdict.**

R639-7-S1 | SUGGESTION | Docs | issue comment 6196137082, item 2; `tool-inventory.json`. Evidence: the residue byte-identity statement does not name its comparison base. Round six has 281 entries; this head has 303. Impact: readers can mistake a within-round comparison for a round-six comparison. Optional outcome: name the within-round baseline, or say "All 45 tool records match round six; residue adds 22 entries." Verification: compare the fields separately. This is comparison clarity, not a request to remove valid conservative residue.

R639-7-S2 | SUGGESTION | Tests | `ci_differential_fixtures.py:358`, `:380`; receipt `R638-6-python-PYW2`. Evidence: this negative fixture refuses correctly, but its real program exits 1 without a sentinel: it looks up `sys.modules['subprocess']` without loading that module. Impact: this individual fixture does not demonstrate the hidden execution from the earlier context. Optional outcome: prime the module and require real sentinel execution. A separate namespace focus fixture already demonstrates execution, so this does not reopen the fixed capability cause. Verification: real status 0 and sentinel, with the same named walker refusal.

No wording-only RESIDUE downgrades F1-F4. Their documentation claims concern executable behavior and evidence.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1-F4 | public rulings; census/binding gate; walkers; exec audit; source/public receipts; production hidden-script probe | R639-7 applied, no clean coverage | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| RTL | CLEAN | full/delta path sets; Dockerfile and product/patch/gitlink boundaries; package/lock delta; 133-record smoke; restore receipt | R639-7 | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| Robustness | UNCLEAN: F1-F4 | scope/re-declaration, branches/loops; full argv; inline program, ABI and provenance paired probes | R639-7 applied, no clean coverage | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| Tests | UNCLEAN: F1-F4 | focus fixtures/188 outcomes; census negative controls; audit controls; actual-tool probes; population reconciliation | R639-7 applied, no clean coverage | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| Docs | UNCLEAN: F1-F4 | `CI_IMAGE.md:137`, `:178`, `:298`, `:658`; PR body/ready comment; claim-to-receipt comparisons and prior dispositions | R639-7 applied, no clean coverage | feef7c9fd239ef62b7c6aad301e80a13275e47ef |

[R639] PASS RTL - `full-paths.txt`, `ci/image/Dockerfile`, `ci/image/image.lock.json`, `evidence/round7-image-smoke.log`, `restore-check.json` - No product RTL, firmware, workflow, interface, patch or gitlink changes occur in the source range. GNU time is added; tool-family smoke and layer identities support unchanged validation interfaces. This supplies no new clock/reset/CDC, synthesis, timing or hardware proof.

**Execution limits and pending duties.**

`controls.json` and log/rc files record six passing focused checks under CPython 3.12.3: differential receipt, census self-test, bare-metal check/self-test, recipe consistency, and inventory check last. Up to four independent controls ran concurrently inside one foreground driver. Local-declaration probes used checksum-verified Bash 5.2.21. Audit probes used host execution with reference CPython 3.12.3, not a container or disabled-network namespace; wheel installs explicitly use no index/dependencies. The Make dry-run probe is outside the shipping census, and the loop-errexit probe refuses; neither is a finding.

No full parent/processor/gPTP/Yosys/builder bank, image build, hardware run, source fix, commit, push, registry access, external write, author contact or delegation occurred. The root-writing audit self-test was not run on the host. Published source-head gate receipts are author evidence; there is no manager source bank at this head. Physical calibration NOT RUN and field skips are not hardware proof. Hosted/act acceptance was not adjudicated here.

The specified current-dev `84f9e3001b7d9b77835c4a9a599dbe6230a8031b` and this PR have no overlapping changed paths from `fa7347fc`. Merge-tree returns 0 and tree `0bb830f536fac49da96f9cb98097c547bbc2a654`. That proves merge shape only. The manager still owns final current-dev candidate builder/native banks and linked receipts, hosted/act acceptance, registry publication/digest round-trip, finding resolution and affected-lens re-review, completion of both reviews, explicit merge authorization, and post-merge containment/public closure.

`restore-check.json` verifies all 1,359 superproject tracked blobs by raw bytes/mode, the index tree, clean worktree/index, all six recorded gitlinks and five required initialized submodules. Their 562/104/214/78/65 tracked blobs, modes and index trees also match. The unused `external` gitlink remains uninitialized and unchanged. No restoration was needed.

`replay.sh` reproduces focused checks with an existing reference interpreter. Public fetch/reconciliation scripts reconstruct evidence checks. Disposable files remain under `scratch/`, excluded from publication. Audit receipt placeholders replace only disposable paths and the interpreter installation directory; argv structure and events are retained. `MANIFEST.sha256` lists publishable files; publish only those files and this report.

R639-7 FINISHED
