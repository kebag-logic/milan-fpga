[R530] POSITIVE - exact head 39adc58f8e63c7f41e12c79207a45bcc91a658d0

# R530-4: internal cleared-context review of PR #688 (issue #665, lane F3, round 5)

- **Head:** `39adc58f8e63c7f41e12c79207a45bcc91a658d0`, tree `6e677bcdf9e401d538e362e6e1ef534cb084eb7d`. This is the published `665-f3-acmp` and the PR head.
- **Delta reviewed:** `abb3a78a..39adc58f`, seven one-line commits with no trailers and no merge. They touch four files, all under `sw/firmware/ctrl`: `README.md`, `test/ctrl_image.py`, the new `test/ctrl_image_selftest.py` and the new `test/rv32_image/image_arith.c`. I read the full `021b9c1f..39adc58f` range (103 files) for context.
- **Assignment and ruling:** #665 comment 6036721467, "link with the pinned SDK".
- **Verdict:** POSITIVE.
  - The round-4 MINOR shared by R530-3-F1 and R531-3-F1 is resolved at its root.
  - The documented command, run with a freshly installed and digest-verified pinned SDK, reproduces the published table byte for byte at both shapes and the base.
  - Every linked image is RV32I/ILP32 under three independent checks:
    - the SDK's own disassembler and ELF reader;
    - the tool's own audit;
    - a reviewer RV32I interpreter that runs the helpers as compiled for the target.
  - Every planted helper bug fails the self-test.
  - The toolchain identity is stated correctly.
  - One RESIDUE, R530-4-R1, is a false sentence in the author's handoff. It does not affect the verdict.

## Findings

### R530-4-R1 | RESIDUE | Docs | author handoff claims a run with the other local build "would fail the audit"

- **Where:** `review-evidence/665f3-r1/author-r5/HANDOFF.md`, open risk 3, at evidence commit `24bc7989`. The sentence reads: "Locally, a run without `MILAN_RV32_CC` would pick the other build. It would now print another identity, and its images would fail the audit (as round 4's do)."
- **Evidence:** on the measuring host's layout, `fw_rv32.compiler()` with `MILAN_RV32_CC` unset picks `$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc`, a "Buildroot 2026.05" build. Running `ctrl_image.py` with it gives the following (`receipts/ctrl-image-default-compiler.log`, rc 0; `receipts/default-compiler-loaded-bytes.log`):
  - it prints a different identity (libgcc sha256 `faef00ac...`), as the sentence says;
  - every image **passes** the audit, because no library is linked any more;
  - it prints the same totals, 39,716 and 50,088;
  - its `.text` and `.rodata` are byte-identical to the pinned SDK's.

  Only a run that links that build's `libgcc.a` fails the audit. That is round 4's case (`receipts/real-library-controls.log`).
- **Why RESIDUE:** this is wording in the author's evidence prose. Correcting it changes no measurement, figure, test, code or claim in the tree, and the audit is behaving correctly.
- **Exact fix:** replace "and its images would fail the audit (as round 4's do)" with "and, since no library is linked, its images pass the audit with the same figures; only round 4's library-linked images fail it".

### R530-4-S1 | SUGGESTION | Robustness | the identity is printed, not checked against the pin

`ctrl_image.py:310-314` and `:413` print the compiler's version line and libgcc digest. The tool does not compare them with `scripts/ci_rv32_sdk.py`'s receipt (`.milan-rv32-sdk.json`). So a non-pinned compiler produces a table with nothing but the identity line to show it. The README states this behaviour ("Another build at the SDK's path prints another identity"), so it is not a defect. An optional "not the pinned SDK" warning, driven by the receipt, would make it visible. No lens effect.

### R530-4-S2 | SUGGESTION | Robustness | `ctrl_image.py` does not run under an isolated interpreter

`python3 -I sw/firmware/ctrl/test/ctrl_image.py` fails to import `ctrl_arms` (`receipts/ctrl-image-isolated-mode.log`), because the script relies on its own directory being on `sys.path`. Its self-test inserts `HERE` explicitly and runs under `-I`. The documented command has no `-I` and works. Adding `HERE` to `sys.path` would align the two. No lens effect.

No other finding.

## Prior public review findings at this head (read after my own pass)

I wrote my provisional verdict and ledger before reading the prior reviews in full (`receipts/provisional-ledger.md`, timestamped).

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R530-3-F1 MINOR, Conformance/Tests/Docs: linked image not reproducible with the pinned SDK; toolchain misattributed | RESOLVED | See "R530-3-F1 and R531-3-F1 evidence" below. |
| R531-3-F1 MINOR, Conformance/Tests/Docs: link neither reproduces with the pinned SDK nor validates RV32I | RESOLVED | Each of its verification clauses is checked in "R530-3-F1 and R531-3-F1 evidence" below. |
| R530-3-R1 RESIDUE, Docs: PR title "stacked on #685" | RESOLVED | The title is now "Mark II F3: bare-metal ACMP core on the mailbox" (`gh pr view 688`). |
| R531-2-F2 / R530-2-F2 MINOR: linked footprint | RESOLVED | They were retained through the two round-4 F1s, which are now resolved. |
| R531-2-F1 MAJOR; R530-2-F1, F3 MINOR; R530-2-R1 to R3 RESIDUE; R531-1-F1 to F5; R530-1-F1 to F5, R1 | Still RESOLVED | R530-3 and R531-3 (at `abb3a78a`) resolved them. The round-5 delta touches none of their artifacts: `acmp.c`, the adapters, the mailbox RTL, `MAILBOX_SPLIT.md` and the tests are byte-identical to `abb3a78a`. At this head, the 13-arm ctrl gate passes (`acmp` 81 of 81) and so does the 100 % coverage check (`receipts/gates/`). |
| R530-2 S1 to S3 SUGGESTION | Unchanged | No lens effect. |

**R530-3-F1 and R531-3-F1 evidence.** Each verification clause of R531-3-F1, with this round's evidence:

- **Both shapes link under the stated setup.** I installed the pinned archive with `scripts/ci_rv32_sdk.py --archive ... --destination <scratch>`. Its digest `d42680e9...` was verified, and the installer's own receipt verification passed (`receipts/sdk-install.log`). With `MILAN_RV32_CC` pointing at it, `ctrl_image.py --base d51b373a...` exits 0 (`receipts/ctrl-image.log`). It prints exactly the README and PR table:
  - 27,700 / 736 / 0 / 11,280 = 39,716 (30.3 %) at the shipping shape, deltas +10,852 / +36 / +0 / +4,848 / +15,736;
  - 27,704 / 736 / 0 / 21,648 = 50,088 (38.2 %) at the largest shape, deltas +10,852 / +36 / +0 / +4,864 / +15,752.
- **Independent RV32I/ILP32 audit.** Each of the four images (head and base, both shapes) gives the following with the SDK's `readelf` and `objdump` (`receipts/elf-independent-audit.log`):
  - ELF32, little-endian, `EXEC`, RISC-V, Flags `0x0`, `Tag_RISCV_arch: "rv32i2p1"`;
  - only `.text`, `.rodata` and `.bss` allocated;
  - no undefined symbol;
  - a full mnemonic census containing only RV32I base instructions: no `mul`, `div`, `rem`, `amo`, `lr`/`sc`, `f*`, `csr*`, `fence.i` or compressed forms.

  The word counts match the README: `0x6c34`/4 = 6,925 and `0x6c38`/4 = 6,926 at the head, `0x41d0`/4 = 4,212 and `0x41d4`/4 = 4,213 at the base.
- **The helpers execute correctly as compiled for RV32I.** The self-test checks them only as compiled for the host. To close that gap, `scripts/rv32i_exec.py` loads a linked ELF and runs each helper on a minimal RV32I interpreter that faults on any non-RV32I word. It compares every result with exact C semantics.
  - Each helper gets about 4,000 cases: the edges, every shift count, and 2,000 seeded random pairs of every length.
  - All 13 helpers in a standalone link pass, and so do the 5 helpers inside the shipping image (`receipts/rv32i-exec-*.log`).
  - The interpreter itself catches planted `__muldi3` and `__ashrdi3` bugs (rc 1).
- **The incompatible-library control is refused by the measurement.** The self-test's controls pass (33 checks, `receipts/ctrl-image-selftest.log`). I also linked the two real libraries in place of the helpers (`receipts/real-library-controls.log`):
  - the pinned SDK's own `libgcc.a` is refused at the link: "can't link double-float modules with soft-float modules";
  - the other local build's `libgcc.a` is refused by the audit: `rv32i2p1_m2p0_a2p1_...`, "58 words outside RV32I, the first 0x02c75533 at 0x6b34".

  The second refusal reproduces the PR's statement about round 4's images.
- **Sections and objects reconcile with the maps.** Each map's `.text`, `.rodata` and `.bss` equal the section headers, and `.data` is absent (`receipts/map-reconcile.log`). The helpers are 412 bytes and the runtime stand-ins 64 bytes at the head **and** the base, at both shapes (`receipts/helper-runtime-bytes.log`), as the README says.
- **Provenance is stated correctly.** The README, PR body and handoff name all of the following, and each agrees with what I measured (`receipts/sdk-*.sha256`, `ctrl-image.log`):
  - the archive `riscv32-ilp32d--glibc--stable-2025.08-1` and its sha256 `d42680e9...`;
  - GCC 14.3.0 with build revision `2021.11-18033-g83947c7bb6`;
  - `libgcc.a` sha256 `d8ebca8c...af58`, marked as not linked.

  The PR body and handoff give the full version line, `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`, which is what the tool prints. The README gives the build revision instead of the full line, because `check_baremetal_only.py` refuses the line's other words in tracked files. That gate passes at this head. The README states that the tool prints the line in full. No text still claims the round-4 figures were produced by the pinned SDK: the PR body says that table is superseded and was misattributed.

## What each lens examined

### Conformance

- **Ruling 6036721467, item by item:**
  - the composed app links with the CI-pinned SDK through `MILAN_RV32_CC` for RV32I at both shapes;
  - the helpers are supplied (`image_arith.c`) and reported apart (412 bytes);
  - the composition needs no floating-point helper: the audit's input scan finds no undefined symbol;
  - RV32I compatibility is validated through ELF flags, ABI and ISA;
  - the table is regenerated;
  - the identity is named in the README, PR body and HANDOFF.
- **Acceptance addition 6030870481:** the linked image, both shapes, sections and static objects, and the base delta.
- **NFR-SCOUT-01:** `docs/reference/FR_NFR.md:321` requires "one cacheless RV32I control hart", and the image is RV32I-only.
- No protocol behaviour changed in this round. The ACMP clause conformance from round 4 stands; see the ledger.

### RTL

- `git diff abb3a78a HEAD` over `hdl tb syn sw/litex configs constraints sw/builder scripts .github` is empty (`receipts/integrity-and-scope.log`). All four gitlinks equal `abb3a78a`'s.
- I applied the architecture lens to what the round changes: the target-ISA contract of the measured image.
  - The ISA decoder (`ctrl_image.py:114-125` and `:235-246`) matches the RV32I base encoding table: LOAD funct3 3 and 6 excluded, OP-IMM shifts limited to 5-bit with only `srai` at funct7 0x20, OP funct7 1 refused, SYSTEM only `ecall`/`ebreak`, MISC-MEM only funct3 0.
  - The e_flags check (`:111`, `:249-261`) covers RVC, the float-ABI field, RVE and TSO.
  - `exec_sections` (`:221-232`) reads only `SHF_EXECINSTR` sections with file bytes.
- The helpers' 64-bit arithmetic (`image_arith.c:35-213`) is checked for width and truncation:
  - the divide loops cannot overflow the remainder shift;
  - the muldi3 carry is `lo < add`;
  - `INT_MIN` absolute values are taken in unsigned arithmetic;
  - the shifts split at 32 with no shift by 32 or more.

  This is confirmed by RV32I execution.

### Robustness

- Malformed and foreign inputs are refused by name. Self-test: 11 foreign words, an RV32IM attribute, 10 header fields and a weak undefined symbol. My plants: audit accepting M, ignoring e_flags, ignoring open symbols, measure skipping the audit, the leaf check ignoring calls, and the architecture matched as a prefix.
- Real incompatible libraries are refused, one at the link and one at the audit.
- A non-pinned compiler is identified by its printed identity, and its image is correctly judged RV32I. This is the source of R530-4-R1 and S1.
- Helper edge cases are covered: division by zero and `MIN/-1` are excluded as undefined in C, and the source comment states it (`image_arith.c:14-15`). Every shift count 0 to 63 is exercised on RV32I.

### Tests

- `ctrl_image_selftest.py --require-rv32` gives 33 PASS with the pinned SDK.
- 20 reviewer plants (`scripts/plants.py`, `receipts/plants*.log`, `receipts/plants/`):
  - 14 helper bugs (H01-H14). Each makes the self-test exit 1 with between 971 and 576,827 mismatches.
  - 6 audit and measure bugs (A01-A06). Each exits 1 at its named assertion.
  - A04's run in a copied tree failed for an environmental reason: the copy has no git metadata, which the generator needs. I re-ran it in place: it was caught ("an RV32IM soft-float library was measured", `receipts/plants/A04-measure-skips-audit-inplace.log`). I then restored the file and verified the clone.
  - The unplanted in-place run is the control (rc 0).
- The self-test checks the helpers as compiled for the host only. My RV32I execution closes that gap. It is not a finding, because the C is UB-free and width-exact.
- The existing gates pass at this head:
  - `test_ctrl_firmware.py --require-rv32 --jobs 8`, 13 arms;
  - `fw_coverage.py --check`, 17 files at 100 %;
  - `fw_rv32_selftest.py --require-rv32`, 17 checks;
  - `ci_rv32_sdk_selftest.py` and `tally_selftest.py`.

### Docs

- `sw/firmware/ctrl/README.md:28` (contents line), `:225-310` ("Linked size") and the table at `:296-297` agree with every figure I reproduced. That includes the audit word counts, the 64 + 412 bytes and the static objects (app 6,800, stage 3,344 / 13,264, payload 136 / 576, chunk 256, state 288, arena 256).
- `image_arith.c:4-15` and the docstring at `ctrl_image.py:1-58` match the behaviour.
- PR #688 body (`receipts/pr688-body.md`): Status, Round 5 table, Linked RV32I image, Known limitations. The HANDOFF identity block and its line citations (`ctrl_image.py:310`, `:413`, README lines) are accurate. Its open risk 3 is R530-4-R1.
- Docs gates pass at this head: `check_baremetal_only.py --check` (0 findings over 1,147 files) and `--selftest`, `docs_check.py`, `check_doc_style.py`, `DOC_MAP.gen.py --check`, `check_hygiene.py --check`, `measure_test_evidence.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `check_py_idiom.py`, `check_cpp_idiom.py`, `check_em_dash.py --base d51b373a` (0 findings) and `gen_toc.py --check` / `--verify-anchors`.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6036721467; acceptance 6030870481; `FR_NFR.md:321` (NFR-SCOUT-01); `ctrl_image.py:93-99`, `:329-361`; `receipts/ctrl-image.log`, `elf-independent-audit.log`, `sdk-*.sha256`. ACMP clause conformance (`acmp.c`, unchanged since `abb3a78a`) was covered by R530-3 and R531-3 and is retained at this head. | R530-4 | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| RTL | CLEAN | Empty RTL-scope diff `abb3a78a..HEAD` with equal gitlinks; `ctrl_image.py:111-125`, `:221-261`; `image_arith.c:35-213`; `receipts/integrity-and-scope.log`, `rv32i-exec-*.log`. Mailbox RTL is unchanged since R530-3's clean RTL coverage at `abb3a78a`, an ancestor. | R530-4 (RTL artifacts last covered by R530-3 at `abb3a78a`) | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| Robustness | CLEAN (S1, S2 optional) | `ctrl_image.py:204-218`, `:264-307`, `:329-361`; `receipts/real-library-controls.log`, `ctrl-image-default-compiler.log`, `plants/A0*.log`. ACMP robustness artifacts are unchanged since R530-3's clean coverage at `abb3a78a`. | R530-4 | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| Tests | CLEAN | `ctrl_image_selftest.py:1-431`; `receipts/ctrl-image-selftest.log`, `plants.log`, `plants-rerun.log`, `plants/*.log`, `rv32i-exec-*.log`, `gates/ctrl_firmware.log`, `gates/fw_coverage.log`, `gates/fw_rv32_selftest.log` | R530-4 | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| Docs | CLEAN (R530-4-R1 RESIDUE carried) | `sw/firmware/ctrl/README.md:28`, `:225-310`; `image_arith.c:4-15`; `ctrl_image.py:1-58`; PR #688 body and title; `author-r5/HANDOFF.md` identity block and open risks; `receipts/gates/*.log` | R530-4 | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |

## Real limits

- **Prior reviews seen early.** When I listed the PR comments at the start, I saw the opening paragraphs of R531-3 and R530-3, including their F1 headings. The same content is restated in the assignment ruling. I read both reviews in full only after writing `receipts/provisional-ledger.md`.
- **RV32 execution.** Helper execution used a reviewer-written RV32I interpreter, not hardware or a reference simulator. No RV32 emulator is installed here. The interpreter was shown to fail on two planted helper bugs.
- **Markdown renderer.** `check_em_dash.py` and `gen_toc.py` ran with a pre-existing virtual environment. Its name is the first 12 hex digits of the sha256 of `tools/markdown/requirements.txt`, and its six renderer packages match the pins. The system-interpreter runs refused only for the missing renderer (`receipts/gates/*-system-python.log`).
- **SDK source.** The pinned archive came from a local copy whose sha256 equals the pin. It was not downloaded.
- **Not run, by assignment or because the delta does not reach them:** the ctrl mutation campaign (354), the mbx suite and its RTL campaign, the store and writer gates, the contract generator, RTL lint, Vivado, Yosys, the builder bank, the parent/PP/gPTP banks, and `act`/`act_ci`.
- **Hosted evidence at 2026-10-07T12:08Z** (`receipts/hosted-check-runs.tsv`):
  - executed and successful: `bdd-conformance`, `changes`, `docs-check-no-git`, `firmware-unit`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, Yosys shards 0-3, Verilator shard 3;
  - in progress: `docs-check`, `elaborate`, `yosys-elaboration`, Verilator shards 0, 1, 2 and 4;
  - skipped: Physical gPTP (nightly and manual).

  No hosted job runs `ctrl_image.py` or its self-test.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof. The A4 access time remains unmeasured.

## Pending manager duties

- Carry R530-4-R1 to the residue checklist.
- **Not a finding:** decide whether `firmware-unit` should run `ctrl_image.py` and `ctrl_image_selftest.py --require-rv32`. That is a workflow change outside ruling 6036721467.
- Record acceptance of how the README names the identity: by build revision, GCC version and both digests, not the full version line, because of the bare-metal gate. The PR body and HANDOFF carry the full line.
- **Live dev has moved:** `dev` is `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`, not `d51b373a`. The head descends from `d51b373a`, so the current-dev candidate must be built and gated against `e21c1ca0`.
- Own hosted acceptance (the in-progress shards and the aggregates) and `act`.
- Obtain the external review.
- This verdict carries no merge authorization.

## Reproduction

Run from a clone at the head. `$PACKET` is this directory, `$CHECKOUT` the clone, and `$CC` the pinned SDK's `bin/riscv32-linux-gcc`.

- **SDK:** `python3 -I scripts/ci_rv32_sdk.py --archive <riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz> --destination $PACKET/scratch/sdk/host`, then `--verify-only`.
- **Table:** `MILAN_RV32_CC=$CC python3 sw/firmware/ctrl/test/ctrl_image.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c --out $PACKET/scratch/img`.
- **Self-test:** `MILAN_RV32_CC=$CC python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32`.
- **Plants:** `python3 scripts/plants.py $PACKET $CHECKOUT $CC [names...]`, which writes per-plant copies under `scratch/plants`. Plant A04 is applied in place to `ctrl_image.py` and then restored with `git checkout`.
- **RV32I execution:** compile `image_arith.c` with the image flags, link it with `-nostdlib -Wl,-Ttext=0x10000`, then run `python3 scripts/rv32i_exec.py <elf> <toolprefix> 2000`. The same command takes the shipping `ctrl_app.elf`.
- **Real-library controls:** `MILAN_RV32_CC=$CC python3 scripts/real_library_controls.py $CHECKOUT $PACKET/scratch/libctl $CC <other libgcc.a>`.
- **Gates:** `MILAN_RV32_CC=$CC sh scripts/gates.sh $PACKET/receipts/gates`. Re-run the three Markdown gates with the pinned renderer environment.
- **Integrity after probes** (`receipts/integrity-final.log`):
  - all 1,173 tracked non-gitlink blobs hash to their index entries, with matching modes;
  - every index entry is at stage 0, and `git write-tree` equals the head tree `6e677bcd`;
  - `git status --ignored` is empty after removing the interpreter caches;
  - `gptp-processor` (`5dce647a`), `protocol-processor` (`ead80360`) and `third_party/verilog-axis` (`48ff7a7e`) are checked out at their gitlinks and clean; `external` is not initialised.

  Local path prefixes in the receipts are replaced by `$PACKET`, `$CHECKOUT`, `$TOOLS` and `$HOME`. The originals stay in unpublished scratch.

R530-4 FINISHED
