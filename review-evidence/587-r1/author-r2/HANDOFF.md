[A365] Round 2 handoff for issue #587 and PR #589

Status: assigned changes committed and all required gates pass.
Head: `ce65430125a3c800138d5206dd481ba060cb2328`
Starting head: `55079500483970ee244f12fa4c94401783f3df6f`
Branch: `587-8x8-baseline-50mhz`
Checkout: `$LANES/587-8x8-baseline-50mhz`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`
Commit subject: `Make 50 MHz baseline provenance reproducible across checkouts`
One local commit, one-line subject, no body or trailers.

## Public contract

- [Round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/587#issuecomment-5856241447).
- [Round 1 gates](https://github.com/kebag-logic/milan-fpga/issues/587#issuecomment-5855348441).
- [Internal review R350-1](https://github.com/kebag-logic/milan-fpga/pull/589#issuecomment-5856181980).
- [External review R351-1](https://github.com/kebag-logic/milan-fpga/pull/589#issuecomment-5856239199).
- [Original integrated definition](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5844867171).
- [Attribution decision](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5846064333).

Both complete review reports were read from public state.
Evidence branch: `587-review-evidence` at `fd86bc2c2938e44bc46705999a665ed21e76e4a2`.
Its reviewer scripts were fetched with `git fetch origin 587-review-evidence`
and extracted with `git show FETCH_HEAD:<path>` into `/tmp/587-a365-review`.
All 18 extracted scripts remain byte-identical to that public commit.
`REVIEW-SCRIPTS.json` records their sizes and SHA-256 hashes.
Only the export and verification scripts applicable to round 2 ran.
The synthesis and probe launchers were not run: no re-measurement was authorized.

## Change list

| File:line | Change and assigned finding |
|---|---|
| `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29` | F1 / R351-F1: name `$REPO` alongside `$BUILD`, cover all three ROM pathname parameters, state exact comment removal and UTF-8 hashing, and recompute the digest. |
| `docs/findings/PP_SHADOW_BASELINE.md:30` | F2 / R351-S1: label original provenance, bind historical 100 MHz to `990f9652` and the 50 MHz rerun to `0922e434`. |
| `docs/findings/PP_SHADOW_BASELINE.md:96` | Label historical standalone BRAM and critical-path provenance. |
| `docs/findings/PP_SHADOW_BASELINE.md:174` | Explain the portable export normalization beside the rerun evidence. |
| `docs/findings/PP_SHADOW_BASELINE.md:278` | Label original ranking, OOC/attribution tables, growth figures and boundary/load prose with clock and processor pin. |
| `docs/findings/PP_SHADOW_BASELINE.md:443` | Bind the original image/input record to its clock and pin. |
| `docs/findings/PP_SHADOW_BASELINE.md:474` | Label historical mapping figures and distinguish 100 MHz timer geometry from a timing constraint. |
| `docs/design/AREA_BUDGET.md:10` | R351-S2: point readers to issue #587's 50 MHz rerun. |

No source, configuration, recipe, test, ranking or submodule changes.
The manifest changed only `export_comparison`; original raw hashes remain intact.
This is an executor's fix report, not independent review clearance.

## 100 versus 50 MHz figures

Existing measurements are retained; round 2 performed no synthesis.
Historical #231 processor pin: `990f96526bb89356c963a260ebbdcf2a77e6623a`.
Rerun #587 processor pin: `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.

| Measurement | Clock | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Default whole design, historical #231 | 100 MHz | 68,136 | 70,835 | 80 | 29 | 11 | 3,916 | -11.331 |
| Default whole design, rerun #587 | 50 MHz | 68,047 | 70,744 | 80 | 29 | 11 | 3,913 | -1.708 |
| Default change, 50 minus 100 MHz | comparison | -89 | -91 | 0 | 0 | 0 | -3 | +9.623 |
| Attribution wrapper, historical #231 | 100 MHz | 29,489 | 32,991 | 26 | 5 | 8 | 1,809 | -10.846 |
| Attribution wrapper, rerun #587 | 50 MHz | 28,955 | 32,982 | 26 | 5 | 5 | 1,774 | -1.700 |
| Attribution change, 50 minus 100 MHz | comparison | -534 | -9 | 0 | 0 | -3 | -35 | +9.146 |

Default WNS is whole-design; attribution wrapper WNS is internal.
The default remains 4,647 LUTs above the device's 63,400 LUTs.
The 50 MHz attribution whole design has 69,923 LUTs, WNS -1.700 ns.
These are synthesis estimates, with no placement or timing-closure verdict.

## Fresh export and normalization evidence

Fresh default and attribution exports are under `/tmp/587-a365-export-default`
and `/tmp/587-a365-export-attribution`; neither directory contains a synthesis run.
The unchanged internal-review `export_8x8.py` executed the preview's design arguments,
removing only `--build` and changing the output directory as the recipe directs.
The configuration still supplies the 50 MHz clock.
Firmware compiled; no bitstream or hardware operation ran.
The preparation helper ran with `--synthesis-only`, plus `--attribution-only`
for the second export. It only prepared scripts and checked images.

The unchanged reviewer normalizer was invoked for each fresh generated top:

```sh
python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R350-1/scripts/normalized_verilog.py \
  /tmp/587-a365-export-default/ax8x8/gateware/alinx_ax7101.v \
  $LANES/587-8x8-baseline-50mhz '$REPO'
python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R350-1/scripts/normalized_verilog.py \
  /tmp/587-a365-export-attribution/ax8x8/gateware/alinx_ax7101.v \
  $LANES/587-8x8-baseline-50mhz '$REPO'
```

Both report three checkout-root occurrences and this digest:
`38f6c8dd93ba018d009875412b82dd9f34e2149244eda20ab1e2f81d3f85f575`.
The final argument is the literal token `$REPO`, not a checkout pathname.
`normalized-default.log` and `normalized-attribution.log` retain the output.
An additional direct application of the full committed rule matches both.
The build root disappears in comments in these generated tops.
`normalization-rule.log` also records normalized Tcl/XDC equality.

Unchanged reviewer checks pass: page figures, ranking, historical values,
and source/image hashes. Original-history numeric rows: 60 retained.
Round-2 numeric rows: 76 retained. Neither check loses a prose number.
The page figure checker reports 124 comparisons, zero mismatches.
The ranking checker reports 82 rows and zero errors.
Input verification: default 130 matching records; attribution 131 matching records.
Each also has three expected raw differences: the path-bearing generated files.
There are zero missing inputs or source/image mismatches.
The legacy `verify_inputs.py` prints the old root-dependent normalization diagnostic;
that diagnostic is not the new digest oracle. The unchanged dedicated normalizer
with literal `$REPO`, and the full-rule check, prove the new digest.

## Input hashes

All seven recipe-input hashes were rechecked against this checkout.
The committed manifest contains the complete 127/128 source-input inventories
and six image records per variant; they remain the original measurement records.
Fresh large outputs are described by hash and size in `ARTIFACTS.json`.
No tree exports, installed packages, SDKs, tool prefixes or files over 200 KB
are included in this output directory.

| Input | Bytes | SHA-256 |
|---|---:|---|
| `syn/ooc/pp_baseline.py` | 26768 | `8d3123e27d965b75b655715a3cc9de38e607062a05e4f8a99ff98dfaee158177` |
| `sw/litex/build.sh` | 29733 | `334076317acfe2fcd8cc9c7afcf03a6911e8b7108964a2068865556764d6bcae` |
| `sw/litex/milan_soc.py` | 250647 | `b3662e2b54beb6f6a59faea338453d832b992c1b27c597c662a92a388d85bbcf` |
| `scripts/ci_rv32_sdk.py` | 8402 | `ffcc5433d97209b00cac5155c61bc464a43a60fec49bce0330d81279e1df7cb4` |
| `sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch` | 4060 | `eb44cc0365eb2f20b8c76412032b080242c7daca2e67ac84f166976e5dd8018a` |
| `sw/litex/patches/0004-vexiiriscv-baremetal-variant.patch` | 1706 | `cfbd904607759b1effec0705bcc501d821684c6cdddf4cedb2dd2c14eafa9ea8` |
| `sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch` | 3287 | `e464f6a7adf5c643961808f2dfadd00e4c431caf613bb9d71ab3be90f98dcab0` |
| `work:default/ax8x8/gateware/alinx_ax7101_rom.init` | 116811 | `c05e5c24ed202eee530f6dcd44585eafca46e74d94d82865bbf404e03cd964dd` |
| `work:default/ax8x8/gateware/alinx_ax7101_sram.init` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `work:default/ax8x8/gateware/alinx_ax7101_mem.init` | 147 | `d1657b93f1791073b22bd153501d5b9474a7676633af2a6c7b049a155b818335` |
| `repository:configs/generated/ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `repository:configs/generated/ucode.hex` | 26624 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` |
| `repository:sw/builder/out/endstation_ax7101_8x8/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `configs/endstation_ax7101_8x8.yaml` | 19799 | `ede309aa78d5eb566e9a3c93a0ef6c843cc181c1d3f2bbe32eda5db62961983e` |

## Tool versions

The retained measurement record names Vivado 2026.1, SW build 6511674,
part `xc7a100tfgg484-2`, directive `AreaOptimized_high`, 32 threads, default seed.
Round 2 did not invoke synthesis or measure timing again.

Fresh exports use Python 3.14.7 and GCC 14.3.0.
The pinned SDK is `riscv32-ilp32d--glibc--stable-2025.08-1`.
Archive SHA-256: `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.
The SDK was installed and verified under `/tmp/587-a365-sdk` from the cached archive.
The existing SDK candidate lacked a provenance receipt and was not used.
Git is 2.55.0.

| Export dependency | Verified revision |
|---|---|
| litex | `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4` |
| liteeth | `276c9e37fb4d92a5c0f30d39a51c20f42a59cf93` |
| litedram | `f9b75e0347fc43267d083f7ff5965170fe8f9a58` |
| litex-boards | `9ac53c7a11f2571ba2c9f165f468ae021a4f9bda` |
| pythondata-cpu-vexiiriscv | `15cfab529a17c473d0fc75edf3f409eb374cef35` |

The three required patch reverse-apply checks passed in their owning packages.
The documentation environment is `/tmp/587-a365-docs-venv`.
It was installed with hashes from `tools/markdown/requirements.txt`.
Versions: cmarkgfm 2025.10.22, html5lib 1.1, cffi 2.1.1,
pycparser 3.0, six 1.17.0, webencodings 0.6.1.
The extra bare-metal check first refused that environment because it lacks YAML.
It then passed with the system interpreter's installed YAML support.
The refusal remains recorded separately in `GATE-RECEIPTS.json`.
An initial input-check invocation used the nested CPU package path and failed;
the corrected package root yields the zero-mismatch receipt above.
No test, acceptance criterion or source was changed for either environment issue.

## Gate table

All commands ran in the foreground from the physical checkout above,
without output pipelines, using generous timeouts. No detached job remains.
Required gates and the additional completed checks all return rc 0.
The archived environment refusal is not a successful gate result.
`GATE-RECEIPTS.json` binds each command, head, duration, log size and SHA-256.
Required documentation commands used the pinned environment on `PATH`.
The last two extra repository checks used `/usr/bin/python3`.

| Check | Exact command | rc | Receipt |
|---|---|---:|---|
| baseline-selftest | `python3 syn/ooc/pp_baseline.py --selftest` | 0 | `baseline-selftest.log` |
| baseline-mutants | `python3 syn/ooc/pp_baseline_mutants.py` | 0 | `baseline-mutants.log` |
| docs-git | `python3 scripts/docs_check.py` | 0 | `docs-git.log` |
| docs-no-git | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | `docs-no-git.log` |
| em-dash | `python3 scripts/check_em_dash.py --base 63fe4fb0` | 0 | `em-dash.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| contents | `python3 scripts/gen_toc.py --check` | 0 | `contents.log` |
| anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| whitespace | `git diff --check` | 0 | `whitespace.log` |
| committed-whitespace | `git diff --check 63fe4fb0 HEAD` | 0 | `committed-whitespace.log` |
| normalized-default | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R350-1/scripts/normalized_verilog.py /tmp/587-a365-export-default/ax8x8/gateware/alinx_ax7101.v $LANES/587-8x8-baseline-50mhz '$REPO'` | 0 | `normalized-default.log` |
| normalized-attribution | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R350-1/scripts/normalized_verilog.py /tmp/587-a365-export-attribution/ax8x8/gateware/alinx_ax7101.v $LANES/587-8x8-baseline-50mhz '$REPO'` | 0 | `normalized-attribution.log` |
| page-figures | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R350-1/scripts/check_page_figures.py $LANES/587-8x8-baseline-50mhz` | 0 | `page-figures.log` |
| ranking | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R351-1/scripts/check_ranking.py $LANES/587-8x8-baseline-50mhz` | 0 | `ranking.log` |
| history-original | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R351-1/scripts/check_history_numbers.py $LANES/587-8x8-baseline-50mhz 63fe4fb0 HEAD` | 0 | `history-original.log` |
| history-round2 | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R351-1/scripts/check_history_numbers.py $LANES/587-8x8-baseline-50mhz 55079500 HEAD` | 0 | `history-round2.log` |
| verify-inputs | `python3 /tmp/587-a365-review/review-evidence/587-r1/reviews/R350-1/scripts/verify_inputs.py docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json $LANES/587-8x8-baseline-50mhz $WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv /tmp/587-a365-export-default /tmp/587-a365-export-attribution` | 0 | `verify-inputs.log` |
| pp-sources | `python3 scripts/pp_srcs.py --check --selftest` | 0 | `pp-sources.log` |
| baremetal | `/usr/bin/python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal.log` |
| entity-shape | `/usr/bin/python3 scripts/check_entity_shape.py` | 0 | `entity-shape.log` |

Baseline mutations: unchanged control passes; all 28 removals are killed.
Documentation checks: zero findings in both Git and no-Git modes.
The no-Git inventory-parity self-test is explicitly inapplicable without Git.
Em-dash gate: 0 findings over 230 added lines, 339/339 arms.
Contents and anchors: 111 annotated pages and 179 reproduced anchors.
Source inventory and bare-metal checks pass; entity shape: 113 checks, zero failures.

## Delivery and remaining ownership

The worktree and all three initialized public submodules are clean.
Only the three recipe symlinks created in this round were removed.
`PR-BODY.md` is the full replacement body, beginning `[A365]` and carrying `Closes #587`.
Publication of that body and commit belongs to the manager.
No push, PR creation/edit, merge, existing-comment edit/delete, other checkout,
submodule edit, hardware work or delegation occurred.
Independent round-2 review, hosted/local-replica acceptance, candidate validation,
merge and containment remain outside this delivery.
The manager updates the #229 reference comment after merge.
Issue acceptance item 2's reference-comment clause remains manager-owned.

Final issue comment: `REVIEW-READY.md` contains the exact `[A365] REVIEW READY`
body. Posting it on issue #587 is the final action; the returned URL is
reported in the final session response. No later repository work is planned.
