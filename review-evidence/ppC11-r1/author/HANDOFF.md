# [A530] Lane C11 (docs and gates): #27, #70, #71 (acceptance 1 and 3), #75

Status: REVIEW READY at `91cef52`. Every acceptance item in scope is met. Every processor suite and gate the assignment names, and the parent consumer set of 17, is rc 0 at the head. No mutation campaign was run: no RTL or testbench behaviour changed.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked).
- Branch `c11-docs-gates`, base `main` `c050d97153dd0480ae741102c1647eeda9b7f273` (HEAD checked at start). `main` was unchanged when last fetched.
- Assignment: processor issue #27 comment 5980174687. Executor [A530]; reviewers [R472] (internal) and [R473] (external).
- TAKEN: issue #27 comment 5980185420.
- REVIEW READY: issue #27 comment 5981939727, at `91cef52`.
- Commits (one-line subjects, no body, no trailer, not pushed):
  - `f160c65` the gates and CI: `make ids`, `make figures`, the F01.5 rows, the PNG removal and the docs-gates job (#70, #75)
  - `1d7ffad` the class-A byte face in 02, `docs/history`, and integrator FIFO ownership (#27, #71)
  - `8bc4c98` a return annotation in `check-ids.py` that the parent's Python idiom gate requires
  - `c46f708` the landed `host_*` and `nvm_dev_*` ports in 02 §7 and §8, and F02.7 redrawn (#27)
  - `91cef52` wording: the F01.2 note, and a rewrapped diagrams README line
- Head: `91cef52b3c56cc69f66966b004782a69d2940a46`.

## 1. Outcome per issue

| Issue | Verdict | PR body |
|---|---|---|
| #27 | every acceptance item met (section 2.1) | Closes #27 |
| #70 | every acceptance item met (section 2.2) | Closes #70 |
| #71 | acceptance 1 and 3 met. Acceptance 2 (02 §2 rule 5) belongs to the #81/#84 lane, and rule 5 is untouched here | Relates to #71 |
| #75 | every acceptance item met (section 2.4) | Closes #75 |

## 2. Changes (file:line at head `91cef52`)

### 2.1 #27: the current architecture pages show only landed ports

| File:line | Change |
|---|---|
| `docs/architecture/02_interfaces.md:14` | taxonomy row A: byte-wide frames. Drops "reused by trace port, firmware sink": neither is a class-A stream; the trace ring is a class-E window, and the firmware mailbox is tied off |
| `02_interfaces.md:57-58` | F02.9 `mac_rx` / `mac_tx`: the landed port names, the integrator's FIFO, one trunk |
| `02_interfaces.md:75-98` | F02.2: the two dual-clock FIFOs move into an "integrator's, outside the top" subgraph, and the edges are labelled as the byte faces |
| `02_interfaces.md:104-110` | rule 2: the FIFOs are the integrator's, and the RX FIFO presents only complete, FCS-good frames because the face has no `err` or abort. Rule 5 is not touched |
| `02_interfaces.md:127-162` | §3 rewritten: explicit anchor `sec-02-class-a`, the eight landed signals, "RX has no backpressure", "TX stalls on `tx_ready_i`", and a pointer to the history page. The ⚠ banner and the word-stream table are gone |
| `02_interfaces.md:164-181`, `:184-202` | F02.3 redrawn: `rx_valid_i`, `rx_data_i`, `rx_last_i`; no ready. F02.4 redrawn on the TX byte face, with a one-cycle `tx_ready_i` stall and a frame-atomic grant. Both SVGs are re-rendered (`docs/diagrams/wavedrom/fig-02-rxwave.svg`, `fig-02-txwave.svg`) |
| `02_interfaces.md:538-575` | §7: the `host_*` signal table (with `host_err_o`), the APB mapping in a sentence, and F02.7 redrawn on `host_*`. `host_rvalid_o` is a completion strobe, held low while idle, unlike the old diagram's idle-high `pready`. `fig-02-memwave.svg` is re-rendered. The timing comes from `KL_pp_side_port.sv:127-223`: accept in IDLE, response at least one cycle later |
| `02_interfaces.md:590` | trace-ring window row: 128-bit event records read as four 32-bit lanes (was "class-A framing reused") |
| `02_interfaces.md:608-634` | §8: the record-level table is labelled the manager face inside the top (`KL_pp_nvm_port`'s `nvm_*`). A new device-face table lists the top's 15 `nvm_dev_*` ports (op codes from `KL_pp_nvm_port.sv:175-177`). `:665` names `nvm_dev_gnt_i` instead of the module-internal `dev_gnt_i`. `:670` F02.8 is captioned as the manager face |
| `docs/history/02-class-a-word-stream.md` (new, 84 lines) | the removed word-stream text, table and both WaveDrom sources, verbatim from `c050d971`, as plain `json` fences. Provenance permalinks to the page and the two rendered SVGs at `c050d971`. A "what replaced it" table |
| `docs/README.md:41-43`, `README.md:52` | pointers to `docs/history/` |
| `docs/architecture/01_overview.md:76-79`, `:83` | F01.2 note: the export draws the MAC FIFOs at the top's edge, but they are the integrator's. The RX block row says "no CDC inside" (was "CDC in") |
| `docs/architecture/03_packet_engine.md:20-21`, `:28`, `:36`, `:473` | the F03.1 note, the component rows and the TX mermaid label: the MAC FIFOs are the integrator's |
| `docs/architecture/07_memory_maps.md:887` | trace-ring window: 128-bit event records (was "class-A framing") |
| `docs/guides/hdl-engineer.md` (base `:256`) | removed the §9 divergence row "The class-A packet interface is 8-bit": 02 no longer diverges |
| `hdl/packet_engine/KL_pp_trace_ring.sv:14`, `:25`, `:56` | comment only: the record is a 128-bit event record and lane 0 follows the 02 §7 window. The comments pointed at the removed 02 §1 and §3 text. Preprocessed source identical (section 4) |

Every backticked `*_i` / `*_o` name on `docs/architecture/*.md` exists as a port declaration under `hdl/` (1,303 ports scanned). At base, `02_interfaces.md` named `psel`/`pready` (not landed) and `dev_gnt_i` (module-internal). The class B and C waveforms (F02.5, F02.6) keep their generic template names, as docs/README §3 asks of class templates. Their instances (the `svc_*` face, the `maap` conflict pair) are named in the text and tables.

### 2.2 #70: the ID registry gate

| File:line | Change |
|---|---|
| `scripts/check-ids.py` (new, 223 lines) | the gate. It scans `git ls-files --cached --others --exclude-standard -- docs hdl tb`, skipping files with a NUL byte in the first 8 KiB. Defined IDs are the first column of F01.5 (`01_overview.md` §7) and F08.1 (`08_timing.md`, anchor `fig-08-constants`). Forms: `X / Y` lists, F08.1's `T-BUDGET-AECP-TYP / -WC` sibling shorthand, families (`T-MRP-*`, a line-broken `T-ADP-`), braced lists (`T-ACMP-{CMD, DELAY}`), a trailing numeric segment read as minus n when the stem has a row (`0..P-RX-SLOTS-1`), and `P-ID`/`T-ID` as registry words. It fails on a missing or empty master table and on a duplicate row. `--selftest` runs 9 planted cases in throw-away git repos |
| `Makefile:15`, `:44-48` | `ids` (selftest, then the check) added to `check` |
| `docs/architecture/01_overview.md:183-184` | F01.5 rows `P-MAAP-ACCEPT-CYC` (1024 core clocks) and `P-MAAP-RSP-MS` (10,000 ms): module parameters of `KL_acmp_talker` (`MAAP_ACCEPT_CYC_P` `KL_acmp_talker.sv:140`, `MAAP_RSP_MS_P` `:180`), with their constraints and derivations |
| `docs/architecture/02_interfaces.md:300-301` (base `:290-291`, the issue's `260-261`) | the two table rows now name the IDs and link F01.5. "1024 cycles, ≈10 µs" and "10 s" are gone |
| `02_interfaces.md:313-323` | the derivation paragraph no longer copies the parameter's value ("10 s"), `T-SRP-DAFRESH`'s "15 s", `T-MAAP-PROBE`'s 500/600 ms or `T-MAAP-ANNOUNCE`'s 30 s. It cites the IDs |
| `hdl/packet_engine/KL_pp_tx_slots.sv:17`, `tb/tx_slots/README.md:7`, `tb/tx_slots/sim_main.cpp:4-5`, `:29` | the shorthand `"P-TX 4x576 + 1600"` (no row) renamed to the F01.5 IDs `P-TX-STD-SLOTS` / `P-TX-OVERSIZE-BYTES`. Comment and README only; preprocessed sources identical (section 4) |
| third stray, `P-EN-TALKER-DYN-MAPPINGS-RUNNING` | zero uses at base: `490e430` (2026-09-25) removed the last one, and F01.5 carries `MILAN_FEATURES_FLAGS.TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING` (`01_overview.md:196`) |
| `docs/README.md:83-97` | §2: "`make check` enforces the rest" is replaced by exactly what is enforced: `ids` and `params`. "No gate reads values", with a pointer to 09 §8 |
| `docs/architecture/09_verification.md:158-162` | §8: the same statement. The paragraph at `:398-400` (the value scan still to add) is unchanged: PR #155 inserts directly above it |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:530` | REQ-REU-002 Arch and Doc cells name the `ids` gate and 09 §7 |
| `.github/workflows/hdl.yml:13-27` | docs-gates runs `make check`, which includes `ids` (shared with #75) |
| `docs/guides/hdl-engineer.md:237`, `README.md:61` | the gate lists |

### 2.3 #71: acceptance 1 and 3

| File:line | Change |
|---|---|
| `docs/guides/integrator.md:135-146` | §3, anchor `rx-frame-atomic`: "Your RX FIFO must deliver only complete, FCS-good frames", because the byte face has no `err` or abort input. Three obligations: hold each frame whole and start it only once its last byte and FCS verdict are in; drop every FCS-failed, MAC-aborted or overflow-cut frame whole; never present part of a frame (a cut frame that still carries a whole PDU is parsed, per the validator's V1/V2 at `KL_pp_rx_validator.sv`) |
| `docs/guides/integrator.md:34-36` | §1's MAC-boundary bullet points at it |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:531` | REQ-REU-003. Arch: "clocking contract; the dual-clock MAC FIFOs are the integrator's, outside the top, and the RX one presents only complete, FCS-good frames (the byte face has no err/abort)". Doc: "02 §2 rule 2, 02 §3; integrator guide §1, §3" |
| `02_interfaces.md:104-110` (shared with #27) | rule 2 names the integrator as owner. Rule 5 (acceptance 2) is untouched |

### 2.4 #75: the figure gates

| File:line | Change |
|---|---|
| `.github/workflows/hdl.yml:13-27` | docs-gates installs `wavedrom` (pip) and `@mermaid-js/mermaid-cli@11.16.0` (`npm install --prefix "$HOME/mermaid-cli"`, `.bin` appended to `$GITHUB_PATH`, no global npm write), then runs `mmdc --version` and `make check`. The four hand-picked commands are gone |
| `Makefile:3-4`, `:10`, `:13-15`, `:50-53` | `figures` (selftest, then the check) added to `check`. The comment says CI runs this target |
| `scripts/check-figures.py` (new, 228 lines) | the gate. Every file under `docs/diagrams/` must be one of: `README.md`; `src/<n>.drawio` with `<n>.svg`; `wavedrom/<anchor>.svg` whose ```` ```wavedrom ```` block exists under that anchor in some Markdown file; or a top-level SVG that is either a draw.io export or listed in the hand-authored inventory of `docs/diagrams/README.md`. A listed SVG must also be well-formed XML with an SVG-namespace `<svg>` root and a `viewBox`, carry no `<image>` or `<foreignObject>`, and be linked from a Markdown page. Every listed file must exist. `--selftest` runs 10 planted cases |
| `docs/diagrams/2[0-4]-*.png` | removed: 5 files, no reference anywhere in the tree or in the parent (grep). Blob ids and sizes in section 7 |
| `docs/README.md:121-130` | §3: a "Hand-authored SVG" class bullet with its rule (edit the SVG, render a scratch PNG and look, commit the SVG only) and its gate, plus "Nothing else" (`make figures` fails any other file) |
| `docs/README.md:179`, `:182` | §6: an editing row for the persona-guide figures. "Anything" now cites 09 §7 and the CI job |
| `docs/diagrams/README.md:5-8`, `:63-68`, `:91` | the class list. The scratch PNG is never committed, and the instruction to regenerate `21-integration-faces.png` is removed. The `make check` comment says CI runs it |
| `docs/architecture/09_verification.md:112-114`, `:124-125` | §7: the docs-gates job runs exactly `make check`, and the `ids` and `figures` rows are added. The table now matches the Makefile `check` prerequisites one to one: lint, wavedrom-check, links, matrix, modmatrix, params, ids, figures, stale |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:535` | REQ-DOC-001 Arch and Doc cells: run whole by CI; the hand-authored SVG class and `make figures`; 09 §7 |

## 3. New checks and their planted controls

Each control was planted in the lane tree at head and the gate run. The plant was then restored and `git status --porcelain` proved empty. Logs: scratch `controls/` (not in this directory).

| Check | Control (planted) | Gate | rc | Caught as |
|---|---|---|---:|---|
| `ids` | the real base strays: the five files this lane fixed checked out at `c050d971` (`01_overview.md`, `02_interfaces.md`, `KL_pp_tx_slots.sv`, `tb/tx_slots/README.md`, `tb/tx_slots/sim_main.cpp`); every other file carrying the strays is unchanged from base | `check-ids.py` | 1 | 39 uses: `P-MAAP-ACCEPT-CYC` 23, `P-MAAP-RSP-MS` 12 (02, 05, 11, `KL_acmp_talker.sv`, `protocol_processor_top.sv`, `KL_pp_maap.sv`, tb/acmp_talker), `P-TX` 4 (`KL_pp_tx_slots.sv:17`, tb/tx_slots). The same 39 as the first run at the untouched base tree |
| `ids` | `P-PLANTED-STRAY` appended to `05_acmp_engine.md` | `make ids` | 2 | `05_acmp_engine.md:593: P-PLANTED-STRAY has no F01.5 row` |
| `ids` | F01.5 row `P-MAAP-RSP-MS` deleted | `check-ids.py` | 1 | every use, e.g. `02_interfaces.md:301` |
| `ids` | F08.1 row `T-MAAP-PROBE` deleted | `check-ids.py` | 1 | `01_overview.md:184`, `02_interfaces.md:316`, ... |
| `ids` | new untracked `tb/zz_plant/NOTE.md` holding `T-PLANTED-STRAY` | `check-ids.py` | 1 | `tb/zz_plant/NOTE.md:1: T-PLANTED-STRAY has no F08.1 row` |
| `ids` | `T-NOFAMILY-*` and `T-MRP-{JOIN, NOPE}` in `10_srp_engine.md` | `check-ids.py` | 1 | `T-NOFAMILY-*` and `T-MRP-NOPE` |
| `ids` | F01.5 heading renamed (table unfindable) | `check-ids.py` | 1 | `cannot find F01.5`, "master tables unreadable" |
| `ids` | `T-PLANTED-STRAY` in the `KL_pp_tx_slots.sv:17` comment | `check-ids.py` | 1 | `hdl/packet_engine/KL_pp_tx_slots.sv:17: T-PLANTED-STRAY has no F08.1 row` |
| `ids --selftest` | 9 planted fixture cases (6 strays, 3 legal-form cases) | `make ids` | 0 | each stray caught, each form passed |
| `figures` | `21-integration-faces.png` restored from base | `make figures` | 2 | `not a figure format docs/README.md section 3 lists` |
| `figures` | `23-bringup-decision.svg` truncated by 20 bytes | `check-figures.py` | 1 | `not well-formed XML` |
| `figures` | `<image href="x.png">` inserted in `20-rtl-dataflow.svg` | `check-figures.py` | 1 | `carries <image>` |
| `figures` | `25-planted.svg` added (copy of 24) | `check-figures.py` | 1 | `SVG with no .drawio source, not in the hand-authored inventory` |
| `figures` | the `22-aecp-descriptor-fetch.svg` inventory row deleted | `check-figures.py` | 1 | the same, for 22 |
| `figures` | orphan `wavedrom/fig-99-planted.svg` | `check-figures.py` | 1 | `WaveDrom render whose ```wavedrom block ... is in no document` |
| `figures` | every link to `24-adp-acmp-states.svg` retargeted | `check-figures.py` | 1 | `hand-authored figure no Markdown page links` |
| `figures --selftest` | 10 planted fixture cases | `make figures` | 0 | each caught; the clean base passes |
| CI runs lint (`make check`) | a broken ```` ```mermaid ```` block appended to the history page | `make check` | 2 | `MERMAID FAIL ... Parse error on line 4`, at the first target |
| CI runs `ids` (`make check`) | `P-PLANTED-STRAY` appended to the history page | `make check` | 2 | `ID FAIL: docs/history/02-class-a-word-stream.md:86` |
| CI install recipe | the job's `npm install --prefix ... @mermaid-js/mermaid-cli@11.16.0` into scratch, then lint and `make check` with that `mmdc` and no other on PATH | `lint-diagrams.sh`, `make check` | 0 | `mmdc` 11.16.0, 41 Mermaid + 18 WaveDrom blocks OK. With `node` missing from PATH the same lint fails all 41 blocks (rc 1), so a CI runner that cannot run `mmdc` fails the job |

Not exercised: the hosted runner itself (no push). The workflow parses as YAML, and every command in its docs-gates job was run locally as written, except `pip install wavedrom`: the lane used an existing venv that has `wavedrom`.

## 4. RTL and testbench files: comments only

`hdl/packet_engine/KL_pp_tx_slots.sv`, `hdl/packet_engine/KL_pp_trace_ring.sv` and `tb/tx_slots/sim_main.cpp` change only in comments. The comment-stripped preprocessed sources of base `c050d971` and head are byte-identical: `verilator -E -P` for the two `.sv` files, `g++ -fpreprocessed -dD -E -P` for the `.cpp`.

| File | Preprocessed lines base / head | sha256 base = head |
|---|---|---|
| `KL_pp_tx_slots.sv` | 204 / 204 | `6ee60459e94e435b44315eea89662aa4c3d0eb18564b45ed1f8902d47daa69b8` |
| `KL_pp_trace_ring.sv` | 51 / 51 | `fabfdf23083d3ed29ac69afad48eacf4d70106c855b312275f98b4b79589d838` |
| `tb/tx_slots/sim_main.cpp` | 477 / 477 | `90f51caa3171323176d4dba6c4019f6d63048da909d5df0cfaed91a6fbd68e62` |

No mutation patch carries context from the edited lines (`git grep` over `tb/**/*.patch`). The port comment edited at `KL_pp_trace_ring.sv:56` keeps that port documented.

## 5. Processor suites and gates at head

All at head `91cef52` unless the row says otherwise. Every command ran in the foreground of its own job, unpiped, with its own log and rc file (scratch `logs/`). GNU Make 4.3 and the pinned Verilator 5.050 wrapper were first on PATH (wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`).

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,021,485 checks, 0 failing (784 s). Per-suite tallies are identical to the runs at `1d7ffad` and `c46f708` |
| `./scripts/run_suites.sh` at `1d7ffad` and at `c46f708` | 0, 0 | 1,021,485 checks, 0 failing, each (1,262 s and 990 s). `c46f708..91cef52` changes only `docs/architecture/01_overview.md` and `docs/diagrams/README.md` |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 `LINT OK` (16 s) |
| `make check` | 0 | lint 41 Mermaid + 18 WaveDrom OK; wavedrom 18 checked OK; links 1,152 OK; matrix 115 REQ rows, 17 GAP OK; modmatrix 94 rows, 0 untested; parameters 28/28/28 OK; ids selftest 9 OK; ids 488 files, 91 distinct IDs, F01.5 47 P-IDs, F08.1 36 T-IDs OK; figures selftest 10 OK; figures 3 draw.io, 18 WaveDrom, 5 hand-authored OK; stale OK (33 s) |
| the CI docs-gates step as written: `mmdc --version; make check`, with the job's `npm install --prefix ... @mermaid-js/mermaid-cli@11.16.0` (scratch) as the only `mmdc` on PATH | 0 | `11.16.0`, then the same `make check` lines |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 tops, all.v parsed 1 time; `YOSYS OK protocol_processor_top`; `YOSYS XILINX OK KL_aecp_engine` (96 s) |

The base `c050d971` was not re-run as a whole: no RTL or testbench behaviour changes (section 4). At base, `make check` has no `ids` or `figures` target, and running the new scripts on the base content fails them as the controls in section 3 record.

## 6. Parent consumer set (dev `fea346e7` + c8, p2-p1, c10, 232; processor `91cef52`)

Scratch parent: a clone of kebag-logic/milan-fpga, detached at dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`, never committed or pushed. Submodules: `external` `efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, and `protocol-processor` (cloned from the lane, detached at `91cef52`). `git rev-parse --show-toplevel` was checked before every git command in the parent and in its processor submodule. The processor gitlink is set in the index only (`git update-index --cacheinfo 160000,91cef52...,protocol-processor`). The four patches were applied in order with `git apply --check`, then `git apply`:

| Patch | sha256 |
|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` |
| `parent-adoption-232-241f9184.patch` | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` |

GNU Make 4.3 (sha256 `2cc4089ab4ef599e...`, the binary earlier lanes recorded) and the pinned Verilator 5.050 wrapper were first on PATH; `-j16` for the bench builds.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held (`unannotated public function: 0 <= 0`). At `1d7ffad` it was rc 1 (1 > 0, `check-ids.py`'s `uses()`), fixed by `8bc4c98` |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 consumer lists; protocol-processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77 suites without a mutation arm |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 187 md + 975 scrubbed files |
| 9 | `scripts/xvlog_gate.py --check` (alone, under `flock /tmp/milan-vivado.lock`) | 0 | "PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)": `KL_pp_originator.sv:194` and `KL_pp_rx_validator.sv:383` (VRFC 10-3380), neither in a file this lane touches. Analysed at `protocol-processor@91cef52b`, with 73 `hdl/` files and 52 pinned-processor files (467 s, including the wait for the lock) |
| 10 | `sw/builder/test_builder.py` (alone) | 0 | Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN": gate 1b's `MAKEFLAGS += -e` arm, which Make 4.3 does not re-read mid-parse, and gate 11, which needs the local mf48 build tree. The same two as every earlier record (1,150 s) |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 violations <= ratchet 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | legs 606, 606, 646 and 311 checks, 0 failures (312 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 (53 s) |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep leg 104 checks, 0 failures, and its controls 6 of 6 (3,008 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0 | two-stream leg 65 checks and shipping leg 245 checks, 0 failures; `tdm8_render_mutants.py --leg-defects` 5 of 5 (758 s). At this dev the T30 INTERNAL law passes: the first-event delay is 8.035..8.973 media ticks over the 19 phases the log reports, inside the law's 8 < d/T <= 9. Nothing to record against #643 |

Items 1-8, 11, 13 and 14 also ran at `1d7ffad` and at `8bc4c98`: all rc 0, except item 2 at `1d7ffad` as noted. No parent patch is needed. The parent references the processor's figures and 02 only through permalinks at an older pin, and no parent file names the removed PNGs.

## 7. Records

PNG blobs removed (from `c050d971`):

| File | Blob | Bytes |
|---|---|---:|
| `docs/diagrams/20-rtl-dataflow.png` | `3c19e9a4fec2d6ce60d097d1035a23fa4643ae79` | 523,744 |
| `docs/diagrams/21-integration-faces.png` | `32d6dabcbb18e4d1ed8b05d019b6024cf0ea07cf` | 663,333 |
| `docs/diagrams/22-aecp-descriptor-fetch.png` | `57849c9c14428d8777ea076fc396a53f959868a3` | 565,795 |
| `docs/diagrams/23-bringup-decision.png` | `3b67d0291364358853119577612ec1df9c040127` | 790,025 |
| `docs/diagrams/24-adp-acmp-states.png` | `df1533d80be2d70aba984c63ae7ebb087f338796` | 444,845 |

Coordination with the open lanes:

- `git merge-tree` of this head with `origin/pp230-srp-area` (`b59e99c`, PR #154) and with `origin/pp639-armq-lsnrec` (`9e86991`, PR #155): rc 0, no conflicted file, for both.
- #154's added lines use `P-N-STREAM-IN`, `P-N-STREAM-OUT` and `T-MRP-LEAVE`, all with rows, so `make ids` holds after it. #155 adds no P-/T- ID.
- PR #155 inserts 09 §8.8 directly above the 09 paragraph at `:398-400`, which this lane leaves unchanged.
- The #81/#84 lane (A528, not pushed) edits 02 §2 rule 5, 03 §6 and F08.1 rows. This lane changes 02 rule 2 and F02.2 (separated from rule 5 by rules 3 and 4), 03 §2 and §8, and no F08.1 row. If that lane adds a T-ID without a row, `make ids` will say so at merge.
