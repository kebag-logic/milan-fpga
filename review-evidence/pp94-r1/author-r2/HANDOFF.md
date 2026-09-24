[A252] PR #110 / issue #94, round 2 author handoff

Branch: `94-desc-mem-guard`. Starting head: `cc077a6ffe20585d20b116f008e07189ba1bb7f8`.
Final head: `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f`. Final tree: `b83ba761298a353d80c2f48bc178764615525e1d`.
The worktree is clean. The single commit subject has no body or trailers.

## Scope and review inputs

The [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/94#issuecomment-5812432287)
requires the shared F1 from [R290-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5812425622)
and [R291-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110#issuecomment-5812328379),
with R291-2 S1-S4 optional if cheap. All five items are addressed.

Both complete reports were read from the public comments and their archived
`review-evidence/pp94-r1/reviews/<R>/REPORT.md` files on
`kebag-logic/milan-fpga`, branch `pp94-review-evidence`: R290-2 at
`c7702a24451c9a712616d770cf6fbe3de7f48023`, R291-2 at
`383b3ad4745d28cdce43bfbbc5a6c3c5b851b5d0`. The read-only fetch used a fresh
repository under `/tmp`; that scratch repository was deleted after reading.
The report copies are retained in this packet. No private transcripts or other
management output directories were read.

| Review item | Change and evidence |
|---|---|
| R290-2 F1 = R291-2 F1, Docs | Both committed PNGs regenerated from the final SVG sources at the required widths, viewed, and compared byte-for-byte with an independent repeat render. See `diagram-verification.json`. |
| R291-2 S1, RTL / Docs | Removed only the stray blank line in the top's descriptor-memory port block. |
| R291-2 S2, Tests / Robustness / RTL | Added the requested `handshake_case` check: with no debt, an accepted request coincides with a valid, ready stray `last` beat; debt must be set afterward. The guard passes 78/78; the inverted-priority mutant fails only this new assertion. |
| R291-2 S3, Docs | Figure 20 now gives the guard its own solid module box at processor top before external memory; the independent response-buffer path bypasses it. Figure 22 routes step 4 through the guard before the descriptor image and routes header/index access through the same guard. |
| R291-2 S4, Docs | The integrator instruction now addresses `protocol_processor_top.rst_n`: only hard reset, with the descriptor-memory path and CDC queues flushed; never entity disable, store-only reset, or rollback reset. The guard's internal RTL banner is unchanged. |

The test README adds one sentence documenting S2. There are no other product
changes, no guard logic changes, and no top-level interface changes.

## Render and visual inspection

Used the renderer named by `docs/diagrams/README.md`:

```sh
rsvg-convert -w 1950 -o docs/diagrams/22-aecp-descriptor-fetch.png docs/diagrams/22-aecp-descriptor-fetch.svg
rsvg-convert -w 2040 -o docs/diagrams/20-rtl-dataflow.png docs/diagrams/20-rtl-dataflow.svg
```

Both results were opened and inspected at their original resolution:

- **22, 1950 x 1440:** the green `KL_aecp_desc_mem_guard` box sits on the
  processor side between step 4 and the descriptor image. Its hard-reset,
  request-hold, response-pass-through and deferred D3 routing text is readable.
  The module list contains engine, micro-CPU, descriptor store, memory guard
  and response buffer. The suite list includes `tb/desc_mem_guard` alongside
  `tb/desc_store`, `tb/resp_buf`, `tb/ucpu` and the `tb/pp_top` coverage. These
  lines fit on the canvas without clipping. The arrows land at the intended
  blocks, and text stays inside the resized guard and image boxes.
- **20, 2040 x 1380:** the new `KL_aecp_desc_mem_guard` label is readable in
  its own module box, with `at processor top` directly below. The labeled
  `desc_mem_*` arrow leads from this box to integrator main memory. The
  response-buffer master has a separate path to memory. The changed labels
  fit their boxes and do not overlap the nearby SRP route or TX blocks.

`diagram-verification.json` records the exact dimensions, SHA-256 digests,
changed PNG blob IDs, and identical repeat-render results for both figures.

## S2 mutant

The only mutation swaps the two priority arms; product RTL is never edited:

```diff
-    end else if (m_req_valid_o && m_req_ready_i) begin
-      owed_r <= 1'b1;
     end else if (m_rsp_valid_i && m_rsp_ready_o
                  && (m_rsp_last_i || m_rsp_err_i)) begin
       owed_r <= 1'b0;
+    end else if (m_req_valid_o && m_req_ready_i) begin
+      owed_r <= 1'b1;
```

`check-priority-mutant.py` writes the separate source, runs the normal and
mutated builds in the foreground, and requires the exact completed failure:

```text
FAIL: request acceptance must win over a coincident stray terminal beat
78 checks: 77 PASS, 1 FAIL
```

Normal build: make rc 0, 78 PASS / 0 FAIL. Mutant: make rc 2, simulation rc 1,
77 PASS / 1 FAIL. Mutation controller: rc 0, `detected=True`. This is a
completed assertion failure, not a compile failure or crash. The stimulus is
explicitly outside the documented memory response ordering contract and pins
the existing conservative behavior without changing that contract.

Receipts: `priority-mutant.diff`, `KL_aecp_desc_mem_guard.clear_priority.sv`,
`guard.log`, `priority-mutant.log`, `priority-results.json`.

## Validation

All gates execute directly in the foreground, with generous timeouts, and
without piping the tested command. `.github/workflows/hdl.yml` is the complete
CI inventory. The pinned simulator is version 5.050; the renderer is version
2.62.3. `run-gates.py` and `run-parent-gates.py` retain direct commands, return
codes and full output. Dependency installation/cache steps are environment
setup; every workflow validation step is executed locally.

| Repository command | rc | Receipt |
|---|---|---|
| `verilator --version` | 0 | `ci-version.log` |
| `python3 scripts/check-links.py` | 0 | `ci-links.log` |
| `python3 scripts/check-matrix.py` | 0 | `ci-matrix.log` |
| `python3 scripts/render-wavedrom.py --check` | 0 | `ci-wavedrom.log` |
| `make stale` | 0 | `ci-stale.log` |
| `./scripts/lint_hdl.sh` | 0 | `ci-lint.log` |
| `./scripts/run_suites.sh` | 0 | `ci-suites.log` |
| `python3 scripts/gen_matrix.py --check` | 0 | `ci-gen-matrix.log` |
| `git fetch --no-tags origin refs/pull/13/head` | 0 | `ci-fetch-pr13.log` |
| `make -C tb/nvm_port figures` | 0 | `ci-nvm-figures.log` |
| `./syn/yosys/run.sh` | 0 | `ci-portability.log` |
| `make check` | 0 | `ci-make-check.log` |

The suite sweep passed **32 suites, 15,895 checks, zero failures**:
guard 78, descriptor store 584, product top 1,454. The NVM figure
gate completed 46 builds. Portability passed every listed top and the
engine memory-mapping assertions. `make check` passed 41 Mermaid
blocks, 18 WaveDrom blocks, 838 links and both matrix checks.

Parent preparation, run in the requested consumer checkout:

```sh
git -C protocol-processor fetch $LANES/pp94-desc-mem-guard HEAD && git -C protocol-processor checkout --detach FETCH_HEAD
```

Parent HEAD stayed `5fd468a90f218a55a304b9aa3ff6b4e1c1cf8682`. To satisfy the gates' pin
checks, only the processor gitlink was staged temporarily at the tested
head. After all five gates, the original index was restored byte for
byte (matching SHA-256), including its original gitlink. No budget,
checker or parent source was changed, and no parent commit was made.
The submodule checkout remains at the final source head. See
`parent-fetch-checkout.log`, `parent-state.json` and `source-state.json`.

| Parent command | rc | Receipt |
|---|---|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | `parent-cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `parent-py-idiom.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `parent-xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `parent-rtl-source-lists.log` |
| `make -C tb/verilator/pp_shadow -j8` | 0 | `parent-pp-shadow.log` |

Parent simulation: **371 checks, 371 PASS, 0 FAIL**.
The frontend gate executed; it was not skipped. All required gate
commands returned 0. The intentional priority mutant alone returned
nonzero, as required. The final source tree is clean, and
`git diff --check cc077a6f..HEAD` returns 0.

## Limits and remaining manager work

No push, PR edit, merge, parent commit, sub-agent, or hardware operation was
performed. `PR-BODY.md` is the complete proposed replacement body, not a posted
PR edit. The readiness notice is posted only to issue #94.

The manager owns the gitlink-dependent parent `pp_srcs` and `test_builder`
gates, publication, hosted/replica acceptance, independent re-review and the
final merge candidate. This handoff makes no reviewer verdict or new hosted
CI claim. The previous guard area evidence remains 4 LUT / 1 FF against the
5 LUT / 1 FF estimate; it was not rerun because guard RTL is unchanged.

D3 routing of `debt_o` to the product top and parent, owner release,
deadline-to-CLOSED, the 5,000/16,000-cycle and slot-shape rollback cases, and
the owner-release mutant remain deferred by the recorded scope and port
decisions. Parent hard-reset flushing and physical calibration are not newly
claimed by this round.
