[A530]
Closes #27
Closes #70
Closes #75
Relates to #71

The current architecture now describes the landed byte-wide RX/TX and host interfaces, preserves the obsolete word-stream contract in linked history, and states the integrator's complete, FCS-good RX-frame obligation. The documentation gate rejects undefined parameter/timing IDs and unclassified or malformed figure artifacts, and CI runs the complete `make check` target.

## Changes

- **#27:** 02 §3 uses the landed byte ports, with no RX backpressure and TX stalling on `tx_ready_i`. F02.3/F02.4 and the host-side F02.7 match those contracts. The old word-stream prose, table and waveform sources remain verbatim in `docs/history/02-class-a-word-stream.md`, linked from 02 and both entry-point READMEs. The management and NVM tables name the actual top ports.
- **#70:** `make ids` scans tracked and untracked, non-ignored files under `docs/`, `hdl/` and `tb/` against F01.5/F08.1. It checks families, braced members, optional suffixes, continued IDs, sibling shorthand and a registered base followed by minus one. Missing, empty and duplicate master tables fail. The MAAP IDs have rows; the old `P-TX` shorthand names existing IDs; the dynamic-mapping stray already had no use at the source base. 02 no longer copies the MAAP values. docs/README §2 and 09 §8 explicitly leave value scanning unimplemented.
- **#75:** CI runs `make check`, including diagram parsing, committed-render freshness, links, matrices, parameters, IDs, figure inventory and export staleness. The five hand-authored SVGs are a documented and checked class; their unused PNG exports are removed. The figure gate checks XML/root/namespace, viewBox, embedded raster/document elements, inventory membership and links. Its 17 self-test cases include the faults the first review found missing. Full checkout history makes the export-staleness check meaningful.
- **#71:** integrator §3 requires whole, FCS-good frames because RX has no error/abort input. REQ-REU-003 names the integrator as owner of the dual-clock FIFOs. Acceptance 2's synchronous reset wording came from merged PR #157; this lane supplies acceptance 1 and 3.
- F01.5 records that `P-EN-PLAIN-IEEE-PROFILE` has no RTL consumer, preserving the #84 follow-up.

## Round 3

Head `5123548eb4de35f24d43eb088c12dab70b06d01d`, one commit directly on `80588cdc`; no rebase or amend. This round changes seven documentation, script and SVG files, with no HDL or testbench change. Earlier integration merges of PRs #154, #157 and #155 are preserved.

- **R472-2 F3:** the scanner completes a line-broken ID before interpreting its suffix. `T-ADP-` followed by `DELAY(-STRT)` now fails with `T-ADP-DELAY-STRT`; the real `START` form passes. Successive continuation lines work as well.
- **R472-2 F4 / R473-2 F3:** the self-test grows from 25 to 30 cases. It plants a missing minus-one base, a missing line-broken optional member, the composed form, and both breaks together; each requires rc 1 and the exact missing token. Valid counterparts, valid minus one and invalid minus two remain covered. The two reported weakened parsers and the previous parser with the revised cases each fail self-test. 09 §7 states the executable coverage.
- **R472-2 F5:** shorter TX captions and an explicit 40-unit horizontal margin in both waveform sources prevent clipping. The renderer applies the source's `config.svg_margin`; zero/default preserves the original rendering, and invalid margins fail. Both SVGs are regenerated. Browser text bounds pass under six font selections, including the two installed proportional/monospaced families; the original SVGs reproduce both clipping faults. Both revised figures were also inspected in the standalone SVG renderer. Minimum measured left margins are 42.55 units (TX) and 29.80 (host); every caption and port name fits.
- **R472-2 R1:** not pushed at REVIEW READY; the manager records the hosted runs after the push. No hosted result is claimed for this round.

## Validation

All 24 required final-head commands returned rc 0. Commands ran unpiped with separate log/status receipts; independent jobs ran concurrently, with bounded compilation and the parser alone after heavy jobs.

| Processor command | Result |
|---|---|
| `scripts/run_suites.sh` | 33 suites; 1,021,627 runner-reported checks; zero failing |
| `scripts/lint_hdl.sh` | 41 targets pass |
| `make -j16 check` | All nine documentation gates pass; 41 flow/sequence blocks, 18 fresh waveforms, 1,168 links |
| `make -j16 ids` | 30 self-test cases; 531 files / 91 IDs; 47 parameter and 36 timing rows |
| `make -j16 figures` | 17 self-test cases; 3 source/export pairs, 18 waveforms, 5 hand-authored SVGs |
| `scripts/gen_matrix.py --check` | 94 module rows; zero untested |
| `syn/yosys/run.sh` | 42 tops plus the Xilinx mapping check pass |

All 17 scratch-parent consumer commands returned rc 0. Native results include 311 shadow checks, 315 NVM quick checks, all datapath verdicts and controls, and both render legs plus the leg-defect campaign (two positive controls and three caught defects). The parser's two existing findings match its ratchet. The builder reports two arms **NOT RUN**: the Make-specific `MAKEFLAGS += -e` mutation and gate 11, which requires the mf48 build report. Shape-specific guarded checks are also excluded from passed claims. The handoff records every command, result and receipt, including the runner's tally convention.

Final integrity passes: all 556 tracked processor blobs and modes match this head, the index tree matches HEAD, and the processor worktree is clean after generated-output removal. Parent patch reconstruction and all initialized submodule pins match the stated source-consumer setup.

Planted controls already completed: each new missing-ID form fails both the checker (rc 1) and `make ids` (rc 2) with its diagnostic; valid forms pass. Removing the source margins fails `wavedrom-check`; a negative margin fails with its named diagnostic. Margin geometry checks preserve waveform children and height at 1, 40 and 80 units; negative, fractional, string and Boolean margins are refused. The original two SVGs are the text-fit check's failing controls.

Parent validation uses scratch dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877` plus the supplied c8, p2-p1, c10 and 232 adoption patches, in that order, with the processor gitlink at this head. The patched worktree was independently reconstructed using a temporary index. It is neither committed nor pushed. This source-consumer evidence does not replace the manager's final current-dev candidate validation.

Open non-blocking follow-ups retained from earlier reviews: a full dependency lockfile for the diagram CLI and the integrator guide's pre-existing `wr_done_i` / `wr_ready_i` short names. No hardware or physical calibration was run.
