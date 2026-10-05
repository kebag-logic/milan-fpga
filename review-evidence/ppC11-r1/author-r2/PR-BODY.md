[A530]

Closes #27
Closes #70
Closes #75
Relates to #71

Lane C11 (docs and gates), branch `c11-docs-gates` from `main` `c050d971`. The C11 changes cover docs, scripts and CI. Its edits to four code files in `hdl/` and `tb/` are comments only, with byte-identical preprocessed sources between the original base and head. Round 2 also merges the independently validated changes from main (PRs #154, #157 and #155).

## What changes

### #27: one current boundary in 02

- 02 §3 now describes the landed byte faces: `rx_valid_i`, `rx_data_i[7:0]` and `rx_last_i` in, with no ready, no `err` and no abort; `tx_valid_o`, `tx_sof_o`, `tx_data_o[7:0]` and `tx_eof_o` out, stalled by `tx_ready_i`. F02.3 and F02.4 are redrawn on those ports. F02.3 has no `rx_ready`.
- §1 no longer claims a trace port or a firmware sink reuses class A. F02.9 names the ports. F02.2 and rule 2 put the dual-clock FIFOs outside the top, as the integrator's, and the top has no dual-clock FIFO. F02.9 and F02.2 also put the management host on the core clock behind the integrator's bridge.
- §7 lists the landed `host_*` side-port, with the APB mapping in a sentence, and F02.7 is redrawn on it. Its `host_rvalid_o` is a strobe, unlike the old diagram's idle-high `pready`. §8 adds the top's `nvm_dev_*` device face and marks the record-level table as the manager face inside the top.
- Every `*_i` / `*_o` name on the architecture pages is now a port in `hdl/`.
- The 32-bit word-stream contract and its two waveform sources move verbatim to `docs/history/02-class-a-word-stream.md`, with permalinks to the page and the rendered SVGs at `c050d971`. 02 §3, docs/README §1 and the root README link to it. The HDL engineer guide drops its "class-A interface is 8-bit" divergence row because 02 no longer diverges.
- 01 F01.2, 03 §2/§8 and 07 §5.5 no longer place the MAC FIFOs inside the processor, and no longer call the trace ring "class-A framing".

### #70: a P-/T- ID registry gate

- New `make ids` (`scripts/check-ids.py`). It fails on any `P-` or `T-` ID used in any file under `docs/`, `hdl/` or `tb/` that has no F01.5 or F08.1 row. Files are tracked or untracked-but-not-ignored. It reads these forms:
  - a family `T-MRP-*`, which needs one row in it;
  - a braced list `T-ACMP-{CMD, DELAY}` or `T-NVM-{RS-DEADLINE, RS-AGGREGATE}`, which needs a row for each member;
  - an optional segment `T-ADP-DELAY(-START)`, which needs a row for both;
  - an ID broken at a line end, read with the next line's word;
  - F08.1's sibling shorthand `T-BUDGET-AECP-TYP / -WC`;
  - `P-RX-SLOTS-1` as minus one, and no other tail.

  Braces or a `(-` holding anything but ID segments fail. Any other text after a hyphen is prose: `P-TX-shaped` uses `P-TX`. An unreadable, empty or duplicated master table fails. A `--selftest` of 25 planted cases runs first in `make check`.
- At base the gate finds 39 uses of three undefined IDs:
  - `P-MAAP-ACCEPT-CYC` and `P-MAAP-RSP-MS` now have F01.5 rows, as module parameters of `KL_acmp_talker`. 02 §4.2 (the former 260-261, now 307-308) and its derivation paragraph no longer carry their values.
  - The shorthand `P-TX` in three comments is renamed to `P-TX-STD-SLOTS` / `P-TX-OVERSIZE-BYTES`.
  - The issue's third stray, `P-EN-TALKER-DYN-MAPPINGS-RUNNING`, has zero uses at base: `490e430` removed its last one, and F01.5 carries `MILAN_FEATURES_FLAGS.TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING`.
- docs/README §2 and 09 §8 now say the same thing. `make check` enforces the ID half of the single-source rules, plus `params`. No gate reads values, and the value scan is still listed as to-add at the end of 09 §8.
- F01.5 records that `P-EN-PLAIN-IEEE-PROFILE` has no RTL consumer, as it already did for `P-DESCR-IMAGE-BYTES` (#84, "What remains" item 3).

### #75: figure gates in CI

- The docs-gates job runs `make check` itself. That covers Mermaid lint, WaveDrom freshness, links, both matrices, parameters, IDs, figures and staleness. 09 §7 says the same and lists every target. Before it runs, the job:
  - checks out full history, so `make stale` can fail;
  - installs `wavedrom==2.0.3.post3`;
  - installs Mermaid CLI 11.16.0 with `mermaid@11.17.2` and `puppeteer@25.12.0` (`npm install --prefix`).
- docs/README §3 names hand-authored SVG as a figure class and gives its rule. New `make figures` (`scripts/check-figures.py`, with a 17-case `--selftest` run first) holds every file under `docs/diagrams/` to one of four classes:
  - a draw.io source with its export;
  - a WaveDrom render whose block exists;
  - a listed hand-authored SVG: well-formed, with an SVG-namespace `<svg>` root and a `viewBox`, no `<image>`, `<feImage>` or `<foreignObject>`, and linked from a page;
  - `README.md`.

  Any other file fails, and so does a missing or empty inventory.
- The five `docs/diagrams/2[0-4]-*.png` are removed. No document referenced them, and the diagrams README no longer tells editors to regenerate the PNG for diagram 21.

### #71, acceptance 1 and 3 (acceptance 2 is the #81/#84 lane's: 02 §2 rule 5 is untouched)

- Integrator guide §3 (anchor `rx-frame-atomic`) says the RX FIFO must deliver only complete, FCS-good frames, because the byte face has no `err` or abort. It holds each frame whole, drops bad, aborted or cut frames whole, and never presents part of one. §1 points there.
- The REQ-REU-003 Arch and Doc cells name the integrator as owner of the dual-clock MAC FIFOs (02 §2 rule 2, 02 §3, integrator guide §1 and §3).

## Round 2

Round 1 ended at `91cef52`. Both reviews of it were NEGATIVE, on the same two MINOR findings. Round 2 adds seven commits on top and then three merges of `main`, with no rebase.

- **F1, `make ids` and braced lists with hyphenated members.** Braced members may have several segments, and each is checked. A family is only `-*`. A line-end hyphen continues on the next line, and an optional segment `(-SEG)` checks both IDs. Any other text after a hyphen is prose, so `P-TX-shaped` checks `P-TX`. The reviewers' I5 (`T-NVM-{RS-DEADLINE, RS-TYPO}`) and I7 (`P-TX-shaped`) now fail. So do the tree's own line-broken and optional-segment uses when a segment is misspelt, which round 1 passed. The numeric tail is narrowed to `-1`. The self-test grows from 9 to 25 cases.
- **F2, the figure self-test.** It now plants every fault 09 §7 names: `<foreignObject>`, a root outside the SVG namespace, a non-`<svg>` root, and a missing or empty inventory. It also plants `<feImage>`, which is now refused, and a file in a subdirectory. The self-test grows from 10 to 17 cases.
- **Residue, as written:**
  - F01.5's `P-MAAP-RSP-MS` cell drops the derived ", under 1,800 ms".
  - `tb/side_port/README.md` and the `KL_pp_side_port.sv` header comment describe F02.7 by its request-and-strobe rule. The comment change is comment-only: the preprocessed source is identical.
  - 02 rule 2 says "no dual-clock FIFO".
  - The hosted-CI sentence below is replaced.
- **#84 "What remains" (3):** the F01.5 note above.
- **Suggestions taken:**
  - the CI pins and full history;
  - the `ids` self-test cases for each scanned tree and each master-table fault;
  - the minus-one and line-break narrowing, and `<feImage>`;
  - F02.9/F02.2 on the management clock;
  - `nvm_dev_req_o` "or withdrawn at the deadline";
  - the GAP-14 resolution.

  Left open: a Mermaid CLI lockfile, and the integrator guide's pre-existing short names `wr_done_i` / `wr_ready_i`.
- `main` moved three times during the round, and each move is merged with `--no-ff` and no conflict: `07b1469d` (PR #154) as `5b2199b`, `b0a74196` (PR #157) as `e219709`, and `ead80360` (PR #155) as `80588cd`. `make ids` passes on the merged tree (531 files).
- With #157 merged, 02 §2 rule 5 states the synchronous active-low reset, so #71's acceptance 2 also holds at this head. This lane delivers acceptance 1 and 3.

## Validation (head `80588cd`)

All commands ran unpiped, each with its own log and rc.

Processor, at the head:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,021,627 checks, 0 failing; against round 1, `pp_top` changes by +19 (#157 and #155) and `acmp_listener` by +123 (#155) |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 |
| `make check`, run as the docs-gates step (`mmdc --version; make check`) with the job's pinned installs first on PATH (`wavedrom==2.0.3.post3` in a fresh venv; Mermaid CLI 11.16.0 with `mermaid@11.17.2` and `puppeteer@25.12.0`) | 0 | `11.16.0`; lint 41 Mermaid + 18 WaveDrom; wavedrom 18; links 1,168; matrix 115 REQ / 17 GAP; modmatrix 94 rows, 0 untested; parameters 28/28/28; ids selftest 25, ids 531 files, 91 IDs, F01.5 47, F08.1 36; figures selftest 17, figures 3 draw.io / 18 WaveDrom / 5 hand-authored; stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 tops, one parse, `protocol_processor_top` OK |

Hosted CI at `91cef52`: docs-gates and portability pass in runs 37215798865 (push) and 37215802531 (pull_request); suites, which was still running when the reviews were written, has since passed in both (17:58Z and 18:35Z on 2026-10-04).

The round-2 head was not pushed, so it has no hosted run.

The four `hdl/` and `tb/` files changed in comments only. Their comment-stripped preprocessed sources are byte-identical at base and head: `verilator -E -P` for `KL_pp_tx_slots.sv`, `KL_pp_trace_ring.sv` and `KL_pp_side_port.sv`, and `g++ -fpreprocessed -E -P` for `tb/tx_slots/sim_main.cpp`.

Planted controls, each planted in the tree, caught, and then reverted:

- `ids`:
  - the base content of the five fixed files: 39 uses of 3 undefined IDs;
  - a stray `P-` ID in a doc, and a stray `T-` ID in an RTL comment and in a new untracked `tb/` file;
  - an F01.5 row and an F08.1 row deleted;
  - an undefined family `T-NOFAMILY-*`, and braced members `T-MRP-{JOIN, NOPE}` and `T-NVM-{RS-DEADLINE, RS-TYPO}`;
  - `P-TX-shaped`;
  - the tree's own line-broken `T-ADP-` / `DELAY-START`, and its own `T-ADP-DELAY(-START)`, inline and line-broken, each misspelt;
  - `T-MRP-{join, leaveall}`, `T-ADP-DELAY(-start)`, `P-TX-STD-SLOTS-7` and `T-BUDGET-AECP-TYP / -XX`;
  - an unfindable master table.
- `figures`:
  - a PNG restored;
  - a truncated SVG, and an `<image>`, a `<feImage>` or a `<foreignObject>` inside one;
  - a root without the SVG namespace;
  - an unlisted SVG;
  - an inventory row deleted, every row deleted, and the inventory heading renamed;
  - an orphan WaveDrom render;
  - a figure no page links.
- `make check` (so the CI job) fails on a broken Mermaid block (rc 2 at `lint`) and on a stray ID (rc 2 at `ids`).
- Self-test strength: 36 single-behaviour mutants of the two gates each fail their own `--selftest`. Among them are every survivor the reviews named (MF8, MF9, MF10, M12, MI5, MI8, MI9, M01-M03, M11, M13) and the round-1 parser itself.
- Full history: in a synthetic two-commit repository, `make stale` catches a source committed after its export only with full history (rc 2), not at depth 1 (rc 0).

Parent consumer set of 17, at dev `fea346e7` with the c8, p2-p1, c10 and 232 adoption patches and the processor gitlink at the head (scratch, never committed):

| # | Gate | rc |
|---:|---|---:|
| 1 | `check_cpp_idiom.py` | 0 |
| 2 | `check_py_idiom.py` (unannotated public function 0 <= 0) | 0 |
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

In round 1, the first parent run caught an unannotated public function in `check-ids.py` (`check_py_idiom.py` rc 1), which the third commit fixes.

No other processor PR is open besides #156: #154, #157 and #155 are in `main` and merged here.
