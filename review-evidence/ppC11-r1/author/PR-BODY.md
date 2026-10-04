[A530]

Closes #27
Closes #70
Closes #75
Relates to #71

Lane C11 (docs and gates), branch `c11-docs-gates` from `main` `c050d971`. Docs, scripts and CI only: no RTL or testbench behaviour changes. Three files in `hdl/` and `tb/` change in comments only, and their comment-stripped preprocessed sources are byte-identical between base and head.

## What changes

### #27: one current boundary in 02

- 02 §3 now describes the landed byte faces: `rx_valid_i`, `rx_data_i[7:0]` and `rx_last_i` in, with no ready, no `err` and no abort; `tx_valid_o`, `tx_sof_o`, `tx_data_o[7:0]` and `tx_eof_o` out, stalled by `tx_ready_i`. F02.3 and F02.4 are redrawn on those ports. F02.3 has no `rx_ready`.
- §1 no longer claims a trace port or a firmware sink reuses class A. F02.9 names the ports. F02.2 and rule 2 put the dual-clock FIFOs outside the top, as the integrator's.
- §7 lists the landed `host_*` side-port, with the APB mapping in a sentence, and F02.7 is redrawn on it. Its `host_rvalid_o` is a strobe, unlike the old diagram's idle-high `pready`. §8 adds the top's `nvm_dev_*` device face and marks the record-level table as the manager face inside the top.
- Every `*_i` / `*_o` name on the architecture pages is now a port in `hdl/`.
- The 32-bit word-stream contract and its two waveform sources move verbatim to `docs/history/02-class-a-word-stream.md`, with permalinks to the page and the rendered SVGs at `c050d971`. 02 §3, docs/README §1 and the root README link to it. The HDL engineer guide drops its "class-A interface is 8-bit" divergence row because 02 no longer diverges.
- 01 F01.2, 03 §2/§8 and 07 §5.5 no longer place the MAC FIFOs inside the processor, and no longer call the trace ring "class-A framing".

### #70: a P-/T- ID registry gate

- New `make ids` (`scripts/check-ids.py`). It fails on any `P-` or `T-` ID used in any file under `docs/`, `hdl/` or `tb/` that has no F01.5 or F08.1 row. Files are tracked or untracked-but-not-ignored. It understands the tree's forms:
  - families (`T-MRP-*`, a line-broken `T-ADP-`) and braced lists (`T-ACMP-{CMD, DELAY}`);
  - `P-RX-SLOTS-1` as "minus one";
  - F08.1's `T-BUDGET-AECP-TYP / -WC` shorthand.
  
  An unreadable or empty master table fails. A `--selftest` with nine planted cases runs first in `make check`.
- At base the gate finds 39 uses of three undefined IDs:
  - `P-MAAP-ACCEPT-CYC` and `P-MAAP-RSP-MS` now have F01.5 rows, as module parameters of `KL_acmp_talker`. 02 §4.2 (the former 260-261, now 300-301) and its derivation paragraph no longer carry their values.
  - The shorthand `P-TX` in three comments is renamed to `P-TX-STD-SLOTS` / `P-TX-OVERSIZE-BYTES`.
  - The issue's third stray, `P-EN-TALKER-DYN-MAPPINGS-RUNNING`, has zero uses at base: `490e430` removed its last one, and F01.5 carries `MILAN_FEATURES_FLAGS.TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING`.
- docs/README §2 and 09 §8 now say the same thing. `make check` enforces the ID half of the single-source rules, plus `params`. No gate reads values, and the value scan is still listed as to-add at the end of 09 §8.

### #75: figure gates in CI

- The docs-gates job runs `make check` itself, after installing `wavedrom` and Mermaid CLI 11.16.0 (`npm install --prefix`). That covers Mermaid lint, WaveDrom freshness, links, both matrices, parameters, IDs, figures and staleness. 09 §7 says the same and lists every target.
- docs/README §3 names hand-authored SVG as a figure class and gives its rule. New `make figures` (`scripts/check-figures.py`, with a 10-case `--selftest` run first) holds every file under `docs/diagrams/` to one of four classes:
  - a draw.io source with its export;
  - a WaveDrom render whose block exists;
  - a listed hand-authored SVG: well-formed, with an `<svg>` root and a `viewBox`, no `<image>` or `<foreignObject>`, and linked from a page;
  - `README.md`.
  
  Any other file fails.
- The five `docs/diagrams/2[0-4]-*.png` are removed. No document referenced them, and the diagrams README no longer tells editors to regenerate the PNG for diagram 21.

### #71, acceptance 1 and 3 (acceptance 2 is the #81/#84 lane's: 02 §2 rule 5 is untouched)

- Integrator guide §3 (anchor `rx-frame-atomic`) says the RX FIFO must deliver only complete, FCS-good frames, because the byte face has no `err` or abort. It holds each frame whole, drops bad, aborted or cut frames whole, and never presents part of one. §1 points there.
- The REQ-REU-003 Arch and Doc cells name the integrator as owner of the dual-clock MAC FIFOs (02 §2 rule 2, 02 §3, integrator guide §1 and §3).

## Validation (head `91cef52`)

All commands ran unpiped, each with its own log and rc.

Processor, at the head:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,021,485 checks, 0 failing |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 |
| `make check` | 0 | lint 41 Mermaid + 18 WaveDrom; wavedrom 18; links 1,152; matrix 115 REQ / 17 GAP; modmatrix 94 rows, 0 untested; parameters 28/28/28; ids selftest 9, ids 488 files, 91 IDs, F01.5 47, F08.1 36; figures selftest 10, figures 3 draw.io / 18 WaveDrom / 5 hand-authored; stale |
| the new docs-gates step (`mmdc --version; make check`, Mermaid CLI installed by the job's own `npm install --prefix ... @mermaid-js/mermaid-cli@11.16.0`) | 0 | `11.16.0`, then the same `make check` |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 tops, one parse, `protocol_processor_top` OK |

Hosted CI did not run: nothing was pushed. Every command of the new docs-gates job ran locally as written, except `pip install wavedrom`: the lane used an existing environment that has `wavedrom`.

The three `hdl/` and `tb/` files changed in comments only. Their comment-stripped preprocessed sources are byte-identical at base and head: `verilator -E -P` for the two `.sv` files, `g++ -fpreprocessed -E -P` for `tb/tx_slots/sim_main.cpp`.

Planted controls, each planted in the tree, caught, and then reverted:

- `ids`:
  - the base content of the five fixed files: 39 uses of 3 undefined IDs;
  - a stray `P-` ID in a doc, and a stray `T-` ID in an RTL comment and in a new untracked `tb/` file;
  - an F01.5 row and an F08.1 row deleted;
  - an undefined family `T-NOFAMILY-*` and a braced member `T-MRP-{JOIN, NOPE}`;
  - an unfindable master table.
- `figures`:
  - a PNG restored;
  - a truncated SVG, an `<image>` inside one, and an unlisted SVG;
  - an inventory row deleted;
  - an orphan WaveDrom render;
  - a figure no page links.
- `make check` (so the CI job) fails on a broken Mermaid block (rc 2 at `lint`) and on a stray ID (rc 2 at `ids`).
- Both scripts run a self-test of planted fixture cases before checking the tree (9 and 10 cases).

Parent consumer set of 17, at dev `fea346e7` with the c8, p2-p1, c10 and 232 adoption patches and the processor gitlink at the head (scratch, never committed):

| # | Gate | rc |
|---:|---|---:|
| 1 | `check_cpp_idiom.py` | 0 |
| 2 | `check_py_idiom.py` | 0 |
| 3 | `check_rtl_source_lists.py` (42/42 tops) | 0 |
| 3b | `check_rtl_source_lists.py --selftest` (50/50) | 0 |
| 4 | `pp_srcs.py --check --selftest` | 0 |
| 5 | `check_port_contracts.py` (1,759 processor ports, 111 <= 111 undocumented) | 0 |
| 6 | `measure_naming.py --check` | 0 |
| 7 | `measure_test_evidence.py --check` | 0 |
| 8 | `docs_check.py` (0 findings) | 0 |
| 9 | `xvlog_gate.py --check` (2 findings == ratchet, neither in a touched file) | 0 |
| 10 | `sw/builder/test_builder.py` (all gates pass except the two arms every record leaves not run: 1b under Make 4.3, and 11 without the mf48 tree) | 0 |
| 11 | `lint_rtl.py --check` (90 <= 90) | 0 |
| 12 | `pp_shadow` (606, 606, 646, 311 checks) | 0 |
| 13 | `nvm_cosim lint` | 0 |
| 14 | `nvm_cosim quick` (315/315) | 0 |
| 15 | `milan_dp` (9 benches; render mutants 4; gmstep controls 6/6) | 0 |
| 16 | `milan_dp_render` (65 + 245 checks; leg defects 5/5) | 0 |

The first parent run caught an unannotated public function in `check-ids.py` (`check_py_idiom.py` rc 1), which the third commit fixes.

`git merge-tree` of the head with PR #154's and PR #155's branches reports no conflict. #154 adds only IDs that have rows.
