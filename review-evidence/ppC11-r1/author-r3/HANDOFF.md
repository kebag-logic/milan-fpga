# [A530] Lane C11 (docs and gates): #27, #70, #71 (acceptance 1 and 3), #75

Round 3 status: REVIEW READY at `5123548eb4de35f24d43eb088c12dab70b06d01d`, from `80588cdc43ca5605a1d3748d13dd8ed7f22f7000` on `c11-docs-gates`. Origin is the processor repository; the original base `c050d97153dd0480ae741102c1647eeda9b7f273` is an ancestor. The round-3 assignment (issue #27 comment 5988273127) supersedes the earlier head instruction. No push or PR edit is authorized.

Round 3 changes and planted controls are complete. All 24 final-head command receipts are rc 0: the processor suite runner (33 suites, 1,021,627 reported checks, zero failing), lint, full docs gate, IDs, figures, matrix freshness and synthesis, plus all 17 scratch-parent consumer commands. The two builder arms marked NOT RUN and the shape-specific guarded checks are listed below; none is counted as passed. Source cleanup, tracked byte/mode and index-tree verification, parent patch reconstruction and submodule-pin verification all pass. Not pushed at REVIEW READY; the manager records hosted runs after the push.

Round 2 status (historical): REVIEW READY at `80588cdc43ca5605a1d3748d13dd8ed7f22f7000`. All required processor suites, docs gates and 17 parent consumer items returned rc 0 at this head. Sections 1 to 7 are the unchanged round-1 record; the Round 2 section records that earlier head.

Round 1 status: REVIEW READY at `91cef52`. Every acceptance item in scope is met. Every processor suite and gate the assignment names, and the parent consumer set of 17, is rc 0 at the head. No mutation campaign was run: no RTL or testbench behaviour changed.

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

## Round 2

- Assignment: processor issue #27 comment 5982157556. Reviews: R472-1 (PR #156 comment 5982079701) and R473-1 (PR #156 comment 5982154411), both NEGATIVE on F1 and F2. R469-1 S2 (PR #157 comment 5982146515).
- Same branch: one-line commits on top of `91cef52`, then three `--no-ff` merges of `main`. No rebase, no amend, not pushed.
- `main` was `c050d971` at the start of round 2. It moved three times during the round: to `07b1469d` (PR #154 merged), `b0a74196` (PR #157) and `ead80360` (PR #155). Each move is merged with `--no-ff` (item 6).
- Round-2 commits (one-line subjects, no body, no trailer):
  - `df7b37e` F1: `check-ids.py` reads every abbreviated form as IDs; its self-test plants each one
  - `033174e` F2: `check-figures.py`'s self-test plants every fault 09 §7 names; `<feImage>` refused too
  - `779d886` RESIDUE-1, -2 and -4 (R472-1 R1), exactly as written
  - `b827de6` item 4: F01.5 records that `P-EN-PLAIN-IEEE-PROFILE` has no RTL consumer
  - `fa8d479` suggestions (CI): docs-gates gets full history, and the tool versions are pinned
  - `0917009` suggestions (docs): F02.9/F02.2 management clock, `nvm_dev_req_o` withdrawal, GAP-14 resolution
  - `3d5a201` F1, completed: `check-ids.py` also reads an optional segment, `T-ADP-DELAY(-START)`, as both IDs. A scan of every character that follows an ID in the tree found this form (four real uses, one broken across a comment line). The gate read only `T-ADP-DELAY` there, so a missing row passed: the same class as F1
  - `5b2199b` merge of `main` `07b1469d` (PR #154), `--no-ff`, no conflict
  - `e219709` merge of `main` `b0a74196` (PR #157), `--no-ff`, no conflict
  - `80588cd` merge of `main` `ead80360` (PR #155), `--no-ff`, no conflict
- Round-2 head: `80588cdc43ca5605a1d3748d13dd8ed7f22f7000` (tree `e20b82da`). Earlier heads: `e219709` and `5b2199b` (after the first two merges), and `3d5a201` (the lane's own last commit). A first pass at `0917009` was superseded when `3d5a201` was added. Its processor suites and gates and its 12 light parent gates had finished, all rc 0, and its heavy parent run was stopped two minutes in. Those logs are set aside. Every result below is at the final head `80588cd` unless it is marked otherwise. Complete passes at `3d5a201`, `5b2199b` and `e219709` were each all rc 0, and each was superseded by the next merge of `main`.

### R2.1 Items

**Item 1, F1 (both reviews): braced lists with hyphenated members.** `scripts/check-ids.py` at `80588cd` (unchanged since `3d5a201`):

| File:line | Change |
|---|---|
| `scripts/check-ids.py:11-28` | docstring: the five forms that reach past an ID's last segment, and "anything else after a hyphen is prose" |
| `:49-55` | `BRACES` takes any brace content, and `SEGMENTS` must match each member, hyphens allowed (`RS-TYPO`). `LINE_BREAK` reads a hyphen at a line end as the ID continuing on the next line, after any comment leader (`NEXT_LINE`). `OPTIONAL` reads `(-SEG)`, also across a line break. `SIBLING` also matches in a use |
| `:108-135` `uses()` | `-*` is the only family form. `-{...}` gives one ID per member, or kind `list` when any member is not uppercase segments. Any other continuation is read as the ID before the hyphen (`P-TX-shaped` uses `P-TX`, which has no row). A line-end hyphen joins the next line's word (`T-ADP-` / `DELAY-START` is now checked as `T-ADP-DELAY-START`). `T-X-TYP / -WC` in a use also checks `T-X-WC`. `T-ADP-DELAY(-START)` checks both IDs, and `(-` holding anything else is kind `list` |
| `:138-142` `resolves()` | the numeric tail is narrowed to `-1` (minus one), the only tail the tree uses (`pp_pkg.sv:72-73`). Any other tail on a defined stem fails (R473-1 SUGGESTION-3) |
| `:167-168` | a `list` use fails closed: `T-MRP-{...} is not a list of ID segments`, `T-ADP-DELAY(-...) is not a list of ID segments` |
| `:180-269` self-test | each case plants files beside the fixture master pages: 25 cases (was 9). New ones: a stray in `docs/` and in `hdl/` as well as `tb/` (M01-M03); `T-NVM-{RS-DEADLINE, RS-TYPO}` (the reviewers' I5); `the P-RX-shaped pool` (I7's form); `T-MRP-{join}`; a line-broken stray; a sibling `/ -XX`; `T-ADP-DELAY(-STRT)` and `T-ADP-DELAY(-start)`; `P-RX-SLOTS-2`; `P-ONE-X` (MI5); a later table on the F01.5 page (M11); a duplicate row (MI9); an empty F08.1 (MI8); a missing F01.5 heading (M13). Five legal-form cases pass, including `T-ADP-DELAY(-START)`, the same broken across a comment line, and the label `T-MRP-JOIN(B)` |
| `docs/README.md:88-91` | the braced-list example gains `T-NVM-{RS-DEADLINE, RS-AGGREGATE}`, the optional segment needs a row for both, and "any other text after a hyphen is prose" |
| `docs/architecture/09_verification.md:124` | the `ids` row states each form (the optional segment included), the minus-one tail and the master-table faults, and that the self-test plants a stray per scanned tree, per form and per master-table fault |

At `3d5a201` the real tree passes with round 1's counts (488 files, 91 distinct IDs). At `80588cd` it reads 531 files, because the merges add #154's, #157's and #155's files, and still 91 IDs. Every lenient-form use at the head was listed first: `-*` families, hyphen-free braces, two `-1` tails, one line-broken `T-ADP-` in `tb/adp_engine/tb_adp_top.sv:10`, one sibling in the F08.1 table, and four `T-ADP-DELAY(-START)`, one broken across lines at `tb/pp_top/pp_top_wrap.sv:15-16`. All of them still pass, and each is now checked rather than waved through.

**Item 2, F2 (both reviews): the figure self-test.** `scripts/check-figures.py` at `80588cd` (unchanged since `033174e`):

| File:line | Change |
|---|---|
| `:14-16`, `:103` | `<feImage>` joins `<image>` and `<foreignObject>` as refused (R473-1 SUGGESTION-3) |
| `:173-203` self-test | 17 cases (was 10). New: `<foreignObject>` (MF8), `<feImage>`, a root without the SVG namespace and a `<g>` root (MF9, either half of the check), an empty inventory (MF10), a missing inventory section (R473-1's M12), and a file in a subdirectory |
| `docs/architecture/09_verification.md:125` | the `figures` row says "SVG-namespace `<svg>` root", lists `<feImage>`, and adds the missing or empty inventory. Every fault the row names is now planted |
| `docs/README.md:128-129`, `docs/diagrams/README.md:65-67` | the rule lists `<feImage>` |

**Item 3, residue, exactly as written** (`779d886`):

| Residue | File:line | Change |
|---|---|---|
| R473-1 RESIDUE-1 | `docs/architecture/01_overview.md:184` | ", under 1,800 ms" deleted |
| R473-1 RESIDUE-2 | `tb/side_port/README.md:12-13` | "(F02.7: each request held until its strobe)"; the paragraph is rewrapped |
| R473-1 RESIDUE-2 | `hdl/packet_engine/KL_pp_side_port.sv:11-14` | the comment text as given, rewrapped in the header block. Comment only (section R2.2) |
| R473-1 RESIDUE-3 | PR body, Validation | the sentence as given up to the semicolon. Its last clause ("suites was still running when this was last updated") was true when the reviews were written, but suites has since passed in both runs (push 17:58Z, pull_request 18:35Z, read from GitHub at 19:17Z). R473-1 itself says the sentence is to be updated to the final state, so the clause now reads "suites, which was still running when the reviews were written, has since passed in both". A literal copy would have stated something false |
| R473-1 RESIDUE-4 = R472-1 R1 | `docs/architecture/02_interfaces.md:105-106` | "no dual-clock FIFO" (applied once) |

**Item 4, #84 "What remains" (3)** (`b827de6`): `docs/architecture/01_overview.md:200`, the `P-EN-PLAIN-IEEE-PROFILE` row now starts "**no RTL consumer**", the wording of the `P-DESCR-IMAGE-BYTES` row (`:168`). No RTL parameter reads it (`git grep -i plain` over `hdl/`, `tb/` and `syn/` finds only the ROM generator's note), and the one listener ROM column built is Milan's (`hdl/acmp/rom/gen_ltn_rom.py:8-10`). PR #157 does not touch `01_overview.md`.

**Item 5, suggestions:** section R2.5.

**Item 6, merge `main`:** `main` was `c050d971` at the start. At the pre-REVIEW-READY fetch it was `07b1469d`, the merge of PR #154 (`d18270d6`, milan-fpga #230: SRP records in distributed RAM; four existing `hdl/srp/` files, `tb/srp_top`, 10 §5.1, the HDL engineer guide). `git merge --no-ff origin/main` gives `5b2199b` (tree `5cff66d7`, the tree `git merge-tree` predicted), with no conflict. `docs/guides/hdl-engineer.md` merged automatically, and its two changes are in separate sections. On that tree, `make ids` reads 527 files, 91 IDs, OK. A later fetch found `main` at `b0a74196`, the merge of PR #157 (`f9b8f0ee`, processor #81 and #84: 02 §2 rule 5, 03 §6, 06, 08 F08.1, 09, `protocol_processor_top.sv` and `tb/pp_top`). `git merge --no-ff origin/main` gives `e219709` (tree `fdc846ec`, as `git merge-tree` predicted), with no conflict. 02, 03 and 09 merged automatically. On the merged tree, `make ids` reads 531 files, 91 IDs, OK. The final fetch found `main` at `ead80360`, the merge of PR #155 (`c725be12`, milan-fpga #639: timer-arm queues and listener records in distributed RAM; `protocol_processor_top.sv`, `KL_pp_acmp_listener.sv`, `tb/pp_top`, 07, 08, 09, the HDL engineer guide). `git merge --no-ff origin/main` gives `80588cd` (tree `e20b82da`, as `git merge-tree` predicted), with no conflict, and 07, 09 and the guide merged automatically. `make ids` reads 531 files, 91 IDs, OK. No other processor PR is open besides #156. After each merge, all 34 controls and the 36 mutants were re-run with the same results, and so was every suite and gate (R2.3, R2.4). With #157 in, 02 §2 rule 5 states the synchronous active-low reset, so #71's acceptance 2 now holds at this head. The PR body keeps "Relates to #71", as assigned: closing #71 is the manager's decision.

### R2.2 New checks and their planted controls

**Self-test mutants.** Each mutant is a copy of the gate with one behaviour broken, and it must fail its own `--selftest` (rc 1). The scratch driver plants each mutant in a temporary copy, never in the tree.

| Gate | Mutant | Behaviour broken | `--selftest` rc |
|---|---|---|---:|
| both | none (baselines) | | 0, 0 |
| ids | I-R1 | the round-1 `uses()` and `resolves()`, as reviewed | 1 (8 cases fail) |
| ids | I-F1-family | any other text after a hyphen read as a family (I7) | 1 |
| ids | I-F1-break | a line-end hyphen read as a family | 1 |
| ids | I-F1-nobreak | the next line's continuation not read | 1 |
| ids | I-F1-braces | braces holding anything read as a family | 1 |
| ids | I-F1-hyphen | brace members without hyphens only (I5) | 1 |
| ids | I-sibling | a sibling's last segment in a use not checked | 1 |
| ids | I-optional, I-optional-bad, I-optional-break | optional segment not checked; a bad `(-` accepted; a line-broken optional segment not read | 1, 1, 1 |
| ids | MI5, MI5b | any tail after a real stem; any numeric tail (round 1) | 1, 1 |
| ids | MI8, MI9 | empty table accepted; duplicate row accepted | 1, 1 |
| ids | M01, M02, M03 | scan only `tb/`; `hdl/` dropped; `docs/` dropped | 1, 1, 1 |
| ids | M11, M13 | the table read as the whole page; unreadable tables rc 0 | 1, 1 |
| figures | MF8, MF-feImage, MF-image | `<foreignObject>`, `<feImage>`, `<image>` not checked | 1, 1, 1 |
| figures | MF9, MF9-local, MF9-ns | no root check; local name only; namespace only | 1, 1, 1 |
| figures | MF10, M12 | empty inventory accepted; missing inventory section accepted | 1, 1 |
| figures | MF-viewBox, MF-xml, MF-nested, MF-other | no `viewBox` check; malformed XML; a nested SVG read as top level; any other file | 1, 1, 1, 1 |
| figures | MF-unlisted, MF-link, MF-listed, MF-wavedrom, MF-drawio | unlisted SVG; unlinked figure; listed but absent; orphan render; source without export | 1 each |

36 mutants (19 ids, 17 figures), all killed. Every survivor the reviewers named is in the table: MF8, MF9 and MF10 (R472-1 F2), M12 (R473-1 F2), MI5, MI8 and MI9 (R472-1 S2), and M01-M03, M11 and M13 (R473-1 SUGGESTION-1).

**Plants in the lane tree at `3d5a201`, repeated at `5b2199b`, `e219709` and `80588cd` with the same findings** (line numbers move with the merged content: the `08_timing.md` plant is matched by text, and it is line 230 at `80588cd`). Each plant was made, the gate run, the plant restored, and `git status --porcelain` shown empty:

| Plant | Gate | rc | Caught as |
|---|---|---:|---|
| `08_timing.md` (`:225` at `3d5a201`, `:230` at `80588cd`) `T-ADP-DELAY(-START)` → `(-STRT)` | `check-ids.py` | 1 | `T-ADP-DELAY-STRT` (round 1: rc 0) |
| `pp_top_wrap.sv:16` (the line-broken optional segment) `START)` → `STRT)` | `check-ids.py` | 1 | `tb/pp_top/pp_top_wrap.sv:15: T-ADP-DELAY-STRT` |
| `KL_adp_engine.sv:625` `(-START)` → `(-start)` | `check-ids.py` | 1 | `T-ADP-DELAY(-...) is not a list of ID segments` |
| `T-NVM-{RS-DEADLINE, RS-TYPO}` appended to `08_timing.md` (I5) | `check-ids.py` | 1 | `T-NVM-RS-TYPO has no F08.1 row` (round 1: rc 0) |
| `T-MRP-{JOIN, TYPO}` appended (I6) | `check-ids.py` | 1 | `T-MRP-TYPO` |
| `the P-TX-shaped pool` appended to `02_interfaces.md` (I7) | `check-ids.py` | 1 | `P-TX has no F01.5 row` (round 1: rc 0) |
| the real line-broken use: `tb_adp_top.sv:11` `DELAY-START` → `DELAY-STRT` | `check-ids.py` | 1 | `tb/adp_engine/tb_adp_top.sv:10: T-ADP-DELAY-STRT` (round 1: rc 0, read as a family) |
| `// T-MRP-{join, leaveall}` appended to `KL_srp_top.sv` | `check-ids.py` | 1 | `T-MRP-{...} is not a list of ID segments` |
| `pp_pkg.sv:73` `P-TX-STD-SLOTS-1` → `-7` | `check-ids.py` | 1 | `P-TX-STD-SLOTS-7` (round 1: rc 0) |
| `T-BUDGET-AECP-TYP / -XX` appended to `09_verification.md` | `check-ids.py` | 1 | `T-BUDGET-AECP-XX` |
| `T-NVM-{RS-DEADLINE, RS-TYPO}` appended to the history page | `make ids` | 2 | `T-NVM-RS-TYPO` |
| `<foreignObject/>` in `20-rtl-dataflow.svg` | `check-figures.py` | 1 | `carries <foreignObject>` |
| `<filter><feImage href="x.png"/></filter>` in `20-rtl-dataflow.svg` | `check-figures.py` | 1 | `carries <feImage>` |
| the default `xmlns` removed from `22-aecp-descriptor-fetch.svg` | `check-figures.py` | 1 | `root element is svg, not an SVG-namespace <svg>` |
| every row of the hand-authored inventory removed | `check-figures.py` | 1 | `the hand-authored inventory lists no SVG` |
| the inventory heading renamed | `check-figures.py` | 1 | `no '## Inventory (hand-authored SVG)' section` |
| `<foreignObject/>` in `24-adp-acmp-states.svg` | `make figures` | 2 | `carries <foreignObject>` |

The 17 round-1 controls (section 3) were re-run at `3d5a201`, `5b2199b`, `e219709` and `80588cd` with the same plants: each still fails with the same finding. That includes the base strays (39 uses), a deleted F01.5 and a deleted F08.1 row, an untracked `tb/` file, an unfindable table, a restored PNG, a truncated SVG, an unlisted SVG, an orphan render, an unlinked figure, and `make check` on a stray ID and on a broken Mermaid block (rc 2 each).

**CI history control** (`fetch-depth: 0`, R473-1 SUGGESTION-2). A synthetic two-commit repository (scratch, `git init`): the export and its source are committed, then the source is edited in a later commit. With this Makefile's `stale` target, `make stale` gives rc 2 (`STALE: ... source committed after the export`) in a full clone and rc 0 in a `--depth 1` clone. That is why docs-gates now fetches full history. The hosted job itself was not run (nothing pushed); the YAML parses, and the step is `{'uses': 'actions/checkout@v4', 'with': {'fetch-depth': 0}}`.

**CI pin control.** The job's install lines, as written, in scratch: `pip install wavedrom==2.0.3.post3` into a fresh venv (rc 0, 2.0.3.post3), and `npm install --prefix ... @mermaid-js/mermaid-cli@11.16.0 mermaid@11.17.2 puppeteer@25.12.0` (rc 0). `npm ls` shows `mermaid@11.17.2 deduped` and `puppeteer@25.12.0 deduped` under the CLI, so the CLI uses the pinned copies. With those two installs first on PATH (the venv's `python3`, the scratch `mmdc`), the CI step (`mmdc --version; make check`) is rc 0 (section R2.3).

**Comment-only proof for `KL_pp_side_port.sv`** (RESIDUE-2). `verilator -E -P` (pinned 5.050, wrapper sha256 `905795b9…e92f`) of `91cef52` and the round-2 head (the file is unchanged since `779d886`) gives byte-identical output: 144 lines, sha256 `bb74b22c3d6069c217fc986860f07eb72851cde21c16cb549853ca8d1ed54ca1`. No mutation patch or script carries the edited lines (`git grep` for the old text over `*.patch`, `*.py` and `tb/` finds none).

**Coordination.** At `3d5a201`, `git merge-tree --write-tree` with each open PR head (#154 `d18270d6`, #155 `9e869910`, #157 `db2c4eb8`) was rc 0 with no conflicted file. At `5b2199b`, #154 was in `main` and merged, and #155 `1cba30c9` and #157 `f9b8f0ee` merged cleanly. At `e219709`, #157 was in `main` and merged too, and #155 (`1cba30c9`, then `c725be12`) merged with no conflicted file. At the final head `80588cd`, #154, #157 and #155 are all in `main` and merged, and no other processor PR is open besides #156. A scratch probe ran `check-ids.py`'s own parsing over each merged tree object (no checkout) and passed on every one. Its output at the head matches the worktree run: 531 files, 91 IDs.

### R2.3 Suites and gates at the round-2 head

All at the final head `80588cd`, run concurrently, each in the foreground of its own job, unpiped, with its own log and rc file (scratch `logs-r2/`). PATH, first to last: a fresh scratch venv with `wavedrom==2.0.3.post3`, a scratch install of the job's Mermaid line, GNU Make 4.3, and the pinned Verilator 5.050 wrapper (sha256 `905795b9…e92f`).

**GNU Make.** Round 1's Make 4.3 binary (sha256 `2cc4089a…`) lived in another lane's scratch, and that directory was deleted during round 2. A first pass at `e219709` straddled the deletion: its `test_builder` found only the system GNU Make 4.4.1 and ran gate 1b's `MAKEFLAGS += -e` arm (it passed). That pass is set aside, because which Make each of its jobs used cannot be told afterwards. Later passes use another GNU Make 4.3 build, copied into this lane's scratch (sha256 `d6bb842736e175b707e1dcda27cd5e067919b567f668c5ac16cdd6f63392f9b8`). Each job records `command -v make` and `make --version` beside its log, and every job of the final pass recorded that binary and `GNU Make 4.3`. The passes at `3d5a201` and `5b2199b` ran while round 1's binary was still present: their `test_builder` runs printed the Make 4.3 gate 1b SKIP.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,021,627 checks, 0 failing (1,377 s, after the lane's ignored build output was cleaned). Against round 1 (`91cef52`, 1,021,485), two tallies changed, both from merged lanes: `pp_top` 10,416 → 10,435 (#157 and #155 arms) and `acmp_listener` 2,988 → 3,111 (#155). #154's `tb/srp_top` store bench is a separate Make target, not a `run_suites.sh` suite |
| `./scripts/lint_hdl.sh` | 0 | 41 of 41 `LINT OK` |
| `make check`, run as the CI step `mmdc --version; make check` | 0 | `11.16.0`; lint 41 Mermaid + 18 WaveDrom OK; wavedrom 18 OK; links 1,168 OK; matrix 115 REQ rows, 17 GAP OK; modmatrix 94 rows, 0 untested; parameters 28/28/28 OK; ids selftest 25 OK; ids 531 files, 91 distinct IDs, F01.5 47, F08.1 36 OK; figures selftest 17 OK; figures 3 draw.io, 18 WaveDrom, 5 hand-authored OK; stale OK |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 42 tops, all.v parsed 1 time; `YOSYS OK protocol_processor_top`; `YOSYS XILINX OK KL_aecp_engine` |
| self-test mutants (scratch driver, R2.2) | 0 | 36 of 36 killed; both baselines rc 0 |

No mutation campaign was run. This lane changes no RTL or testbench behaviour (R2.2, the comment-only proof). The merges bring in #154's, #157's and #155's RTL, which those lanes validated, and every merge is clean.

Every complete pass of round 2, processor set and parent set alike. Each was superseded by the next commit or merge:

| Head | Superseded by | Processor set | Parent set of 17 |
|---|---|---|---|
| `0917009` | `3d5a201` (the optional-segment form) | all rc 0; suites 1,021,485 | 12 light rc 0; heavy stopped two minutes in |
| `3d5a201` | `main` moved (#154) | all rc 0; suites 1,021,485, round 1's tallies; links 1,152; ids 488 files | all 17 rc 0 |
| `5b2199b` | `main` moved (#157) | all rc 0; suites 1,021,485; links 1,163; ids 527 files | all 17 rc 0 |
| `e219709`, first pass | Make 4.3 binary deleted mid-pass | all rc 0; suites 1,021,500 | 16 rc 0; xvlog stopped in the lock queue; `test_builder` under Make 4.4.1, "ALL GATES PASS EXCEPT 1 NOT RUN" |
| `e219709`, Make 4.3 | `main` moved (#155) | all rc 0; suites 1,021,500; links 1,165; ids 531 files | all 17 rc 0 |
| `80588cd` | final | the table above | R2.4 |

### R2.4 Parent consumer set

This is the round-1 scratch parent (section 6), reset first: tracked files were restored to dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877` and every untracked and ignored file was removed. The other submodules sit at their gitlinks (`external` `efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`). The `protocol-processor` clone (from the lane) was detached at `80588cd`, and the gitlink was set in the index only (`git update-index --cacheinfo 160000,80588cd...,protocol-processor`). Before each pass the parent was cleaned of untracked and ignored files, and the gitlink was moved to that pass's head. The four patches were applied in order with `git apply --check`, then `git apply`, and their sha256 values are unchanged from section 6. `git rev-parse --show-toplevel` was checked before each git command in the parent and in its processor submodule. Nothing was committed or pushed.

Same environment as round 1: system `python3`, GNU Make 4.3 (the build named in R2.3, recorded per job), and the pinned Verilator 5.050 first on PATH. Items 1-8, 11, 13 and 14 ran concurrently with the processor set. Items 12, 16, 15 and 10 ran one after another, and item 9 ran last, alone, under `flock /tmp/milan-vivado.lock`. Nothing else of this lane was running beside it.

| # | Command | rc | Result at `80588cd` |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held (172 translation units) |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held (309 modules): unannotated public function 0 <= 0, undocumented 0 <= 0, over-long line 0 <= 0, long function 9 <= 9 |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 consumer lists; protocol-processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, undocumented 111 <= 111, as in round 1. The informational review inventory counts 317 test-only hierarchical observations (210 at `3d5a201`), and the increase comes with the merged `tb/srp_top` (#154) and `tb/pp_top` (#155) benches |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77 suites without a mutation arm |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 187 md + 975 scrubbed files |
| 9 | `scripts/xvlog_gate.py --check` (alone, under the Vivado lock) | 0 | PASS (2 findings == ratchet; 0 hdl/, 2 pinned processors): `KL_pp_originator.sv:194` and `KL_pp_rx_validator.sv:383` (VRFC 10-3380), the same two as round 1. Analysed at `protocol-processor@80588cdc`; neither finding is in a file this lane touches (154 s) |
| 10 | `python3 -u sw/builder/test_builder.py` (alone) | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 1b's `MAKEFLAGS += -e` arm under Make 4.3, and gate 11 without the mf48 build tree, matching earlier records (1,247 s). Interrupted attempts have no rc and are excluded |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 violations <= ratchet 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | legs 606, 606, 646 and 311 checks, 0 failures (312 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 (33 s) |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep leg 104 checks, 0 failures, and its controls 6 of 6 (2,779 s). Every check tally line equals round 1's (diff through each pass). The 29 "FAILED" strings in the log are status names (`REGISTERING_FAILED`, `TALKER_DEST_MAC_FAILED`), the same 29 as round 1 |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 0 | two-stream leg 65 checks and shipping leg 245 checks, 0 failures; `tdm8_render_mutants.py --leg-defects` 5 of 5 (806 s). T30 INTERNAL law: first-event delay 8.035..8.973 media ticks, inside 8 < d/T <= 9, as in round 1 |

Every pass ran items 12, 16, 15 and 10 one after another and xvlog last, except where noted below.

Runs set aside, none of which counts above (R2.3 has every pass):
- the `0917009` pass, whose `pp_shadow` was stopped two minutes in when `3d5a201` was added;
- at `3d5a201`, one `xvlog_gate.py` start that queued behind another lane's Vivado job on the shared lock. It was stopped before it got the lock, so `test_builder` could run first, and xvlog then ran alone;
- the first pass at `e219709`, which straddled the Make 4.3 deletion. All its other items were rc 0. Its xvlog was stopped in the lock queue so the Make 4.3 re-run could start. Its `test_builder` ran under GNU Make 4.4.1, reported "ALL GATES PASS EXCEPT 1 NOT RUN", and ran gate 1b's MAKEFLAGS arm to a pass.

### R2.5 Suggestions taken and left open

Taken (each a line or two of source, with its control in R2.2):

| Suggestion | File:line | Change |
|---|---|---|
| R472-1 S1, R473-1 SUGGESTION-2 (1) | `.github/workflows/hdl.yml:27` | `wavedrom==2.0.3.post3`, the version the hosted run resolved |
| R473-1 SUGGESTION-2 (2) | `hdl.yml:28` | `mermaid@11.17.2 puppeteer@25.12.0` installed beside the CLI, so the CLI's own ranges resolve to them (`npm ls`: deduped) |
| R473-1 SUGGESTION-2 (3) | `hdl.yml:18-22` | docs-gates checks out with `fetch-depth: 0`, so `make stale` can fail |
| R472-1 S2, R473-1 SUGGESTION-1 | `scripts/check-ids.py:180-269` | the `ids` self-test plants a stray per scanned tree, a later table, a duplicate row, an empty table, a missing heading and a non-numeric tail (M01-M03, M11, MI9, MI8, M13, MI5) |
| R473-1 SUGGESTION-3 (1) | `check-ids.py:138-142` | the numeric tail is narrowed to `-1` |
| R473-1 SUGGESTION-3 (2) | `check-ids.py:52-54`, `:126-127` | a line-end hyphen is read with the next line's word, not as a family |
| R473-1 SUGGESTION-3 (3) | `scripts/check-figures.py:103` | `<feImage>` refused |
| R473-1 SUGGESTION-4 | `docs/architecture/02_interfaces.md:66`, `:83`, `:97` | F02.9: the `mgmt` row's clock domain is core, the `host_*` ports are in `clk_i`, and any bridge is the integrator's. F02.2: the bridge is a node in the "integrator's, outside the top" subgraph, with a `host_*` edge into the core. Rendered and inspected: no label covers a subgraph title (the first wording did, so it was redrawn) |
| R473-1 SUGGESTION-5 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:556` | GAP-14 resolution: "Mermaid/WaveDrom/draw.io or listed hand-authored SVG + lint" |
| R473-1 SUGGESTION-6 = R472-1 S3 | `02_interfaces.md:630` | `nvm_dev_req_o`: "held until `nvm_dev_gnt_i` or withdrawn at the deadline (below)", which matches the deadline paragraph and `KL_pp_nvm_port.sv` |

Left open:

- The Mermaid CLI's deeper transitive dependencies still float: the job pins the CLI, `mermaid` and `puppeteer`, but has no lockfile (R473-1 SUGGESTION-2 offers a lockfile as the full fix). A committed lockfile and `npm ci` is more than a line or two.
- `scripts/render-wavedrom.py:51-52` bootstraps an unpinned `wavedrom` on a host that has none. CI installs the pinned version first, so the bootstrap does not run there. The reviewers did not raise this; it is noted for a later change.
- The integrator guide's short names `wr_done_i` / `wr_ready_i` (`docs/guides/integrator.md:216-217`): R472-1's out-of-scope observation, which R473-1 acknowledged. It predates this PR, and these lines are untouched.
- The new docs-gates lines (pins and full history) run on a hosted runner only after a push. Locally, each install line ran as written, and the CI step passed with those tools (R2.2, R2.3).


### R2.6 Resume integrity audit

The earlier session stopped at an external usage limit. At resumption the branch was
clean at `80588cdc43ca5605a1d3748d13dd8ed7f22f7000`, tree
`e20b82da`, with all seven round-2 fixes and three merge commits already present.
The original base `c050d971`, round-1 head `91cef52b`, and live `main` `ead80360`
are ancestors. All ten round-2 first-parent commit messages have one line.
No additional source edit or commit was needed during resumption.

- All 556 tracked processor files were hashed: bytes and executable modes equal the
  index, and the index tree equals HEAD.
- The parent remains at dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`.
  Its tracked content equals that base plus the supplied c8, p2-p1, c10 and 232
  patches applied sequentially, plus the processor gitlink at the full head above.
  This was checked with a separate temporary index; the parent's actual index was
  not changed. Each initialized submodule is clean and matches its gitlink.
- A combined reverse dry-run was unsuitable because the adoption patches share
  `scripts/xvlog.budget` context. Sequential application to the temporary index
  confirmed exact agreement with the existing parent; no parent file was changed.
- The four comment-only code files were preprocessed again against `c050d971`.
  Their hashes equal the round-1 and R2.2 records. The C++ preprocessor printed the
  same variadic-macro warning on both sides and returned 0 on both.
- Final-head processor and parent receipts that completed before interruption are
  retained. The interrupted builder logs have no rc and are excluded. One resumed attempt
  was also terminated when its bounded foreground wait ended; a planted two-second
  session control proved that a separate process session survives that wait. The
  builder was restarted with unbuffered output in that session. Both final receipts
  are rc 0 and complete R2.4; the parser ran only after the builder finished, under
  the shared Vivado lock.

Audit receipt: scratch `r2/resume-integrity.txt`. Raw logs and large artifacts stay
under `$VALIDATION_STORAGE/ppC11-a530/`; hashes and byte sizes are recorded in
`VALIDATION-RECEIPTS.tsv`, whose paths are relative to that scratch root.

Generated processor test outputs were removed after their completed receipts were checked.
`git status --porcelain=v1 --ignored` is empty; the committed tree remains unchanged.

Final resumed parent results: builder rc 0 (1,247 s), parser rc 0 (154 s).
The two builder skips are stated in R2.4 and the PR body; no skipped arm is counted as passed.

After both final parent runs, the parent still matches the four-patch reconstruction,
all submodules remain clean at their gitlinks, and the processor tree remains clean
including ignored files. Every receipt hash and byte size in the manifest was rechecked.

Round-2 [REVIEW READY comment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27#issuecomment-5987892791) on processor #27: head `80588cdc43ca5605a1d3748d13dd8ed7f22f7000`. No push or PR edit was performed.

## Round 3

Head `5123548eb4de35f24d43eb088c12dab70b06d01d`; one commit directly on `80588cdc`, subject `Handle continued ID suffixes and give interface waveforms text margins`, with no body or trailers. No rebase, amend, push or PR edit. Remote main remains `ead80360`, already an ancestor. The seven changed files are documentation, scripts and SVG exports; no `hdl/` or `tb/` file changed.

### R3.1 Changes by finding

| Item | File:line | Change |
|---|---|---|
| R472-2 F3 | `scripts/check-ids.py:115` | Resolve continuation into the current token and end position before interpreting its suffix. The optional member of a wrapped ID cannot disappear behind the original match. |
| R472-2 F4 / R473-2 F3 | `scripts/check-ids.py:216` | Five new cases take the self-test from 25 to 30: valid composed/continued forms and four missing-row plants. Missing minus-one base at :218; broken optional at :219; composed member at :220; both breaks at :221. Each negative case requires rc 1 and its exact diagnostic token. |
| Coverage statement | `docs/architecture/09_verification.md:124` | States the minus-one base requirement and the new composed negative plants. |
| R472-2 F5, TX | `docs/architecture/02_interfaces.md:207` | Shorter heading and footer retain the frame-order/stall rule; 40-unit horizontal source margin. Export: `docs/diagrams/wavedrom/fig-02-txwave.svg:4`. |
| R472-2 F5, host | `docs/architecture/02_interfaces.md:585` | The same margin gives the full `host_req_valid_i` label room. Port names and waveform transitions are unchanged. Export: `docs/diagrams/wavedrom/fig-02-memwave.svg:4`. |
| Source-owned figure layout | `scripts/render-wavedrom.py:96`; `docs/README.md:120` | A non-negative integer `config.svg_margin` expands the viewport and width while preserving all waveform children and height. Absent/zero preserves the original render. Invalid types and negative values fail. |
| R472-2 R1 | `PR-BODY.md`, Round 3 | Publication state is “not pushed at REVIEW READY”; the manager records hosted runs after pushing. |

#27, #70 and #75 retain their earlier in-scope acceptance with the reported parser, self-test and figure defects corrected. C11 supplies #71 acceptance 1 and 3; acceptance 2 came from merged PR #157. The body retains `Relates to #71`. Existing dependency-lockfile and guide-short-name suggestions remain open.

### R3.2 Each new check and its planted control

| Check / behavior | Plant | Observed result | Receipt under scratch root |
|---|---|---|---|
| composed optional suffix | `T-ADP-` then `DELAY(-STRT)` | checker 1; target 2; full `T-ADP-DELAY-STRT has no F08.1 row`. Previous parser 0 reproduces the defect | `r3/plant-composition.log`, `r3/make-plant-composition.log`, `r3/previous-composition.log` |
| minus-one base membership | `P-MISSING-1` | checker 1; target 2; `P-MISSING-1 has no F01.5 row` | `r3/plant-minus-one.log`, `r3/make-plant-minus-one.log` |
| broken optional member | `T-ADP-DELAY(-` then `STRT)` | checker 1; target 2; full missing token | `r3/plant-broken-optional.log`, `r3/make-plant-broken-optional.log` |
| both breaks | `T-ADP-` then `DELAY(-` then `STRT)` | checker 1; target 2; full missing token | `r3/plant-both-breaks.log`, `r3/make-plant-both-breaks.log` |
| valid counterparts | `P-RX-SLOTS-1` / `START` in those forms | each checker 0; restored tree 0, 531 files / 91 IDs | `r3/positive-*.log`, `r3/ids-restored.log` |
| self-test detects weakened minus-one rule | accept every `-1` regardless of base row | self-test 1; case 7 catches `P-MISSING-1` | `r3/mutant-any-minus-one.log` |
| self-test detects skipped broken optional | omit only an optional member whose spelling contains a newline | self-test 1; cases 8 and 10 catch `T-ADP-DELAY-STRT` | `r3/mutant-skip-broken-optional.log` |
| self-test detects prior composition defect | previous parser with the 30 current cases | self-test 1; composed cases fail | `r3/mutant-old-parser.log` |
| freshness includes margins | source margins replaced by 0; committed exports retained | target 2, both waveform exports named stale | `r3/plant-margins-removed.log` |
| invalid margin refusal | -1 in real source; negative, fractional, string and Boolean values in a fixture | target 2 with `config.svg_margin must be a non-negative integer`; fixtures raise the same diagnostic | `r3/plant-invalid-margin.log`, `r3/controls.log` |
| margin geometry | 1, 40, 80; absent and zero | exact viewport/width expansion; all waveform children and height unchanged; absent/zero byte-identical | `r3/controls.log` |
| text-fit measurement | original SVGs at `80588cdc` | catches TX captions beyond x=600 and host label at x=-10.20 | `r3/wave-fit.log`, `r3/wave-fit.json` |
| text-fit positive controls | revised SVGs under native, Adwaita Sans, Adwaita Mono and three generic font choices | all visible text inside each viewport; two installed families, not six independent font installations | same receipts |

All new control assertions pass. ID plants were temporary untracked documentation files removed in `finally`; those controls planted no RTL/testbench change. Margin plants were likewise restored. The existing parent campaigns run their own disposable mutants. An initial receipt assertion looked only at stdout although the correct error was on stderr; `first-controls.log` is excluded from passing evidence, and the corrected harness reads both streams.

### R3.3 Waveform inspection

TX is 680 × 272 and host 600 × 286, with 40 units added on each horizontal side. Minimum browser left bounds are 42.55 and 29.80; maximum right bounds are 575.77 and 510.00. All text fits vertically too. Measurement waits for fonts and checks each visible text element against the viewport. Both revised figures were visually inspected in the browser and the standalone SVG renderer; their default font substitutions differ. The original figures are caught controls. No font download is required. Scratch PNGs stay outside the output packet and source tree. The other 16 committed waveform exports are unchanged.

### R3.4 Processor suite table at head

| Command | rc | Time | Receipt |
|---|---:|---:|---|
| `./scripts/run_suites.sh` | 0 | 2465 s | `r3/logs/proc_suites.log` |
| `./scripts/lint_hdl.sh` | 0 | 283 s | `r3/logs/proc_lint.log` |
| `make -j16 check` | 0 | 30 s | `r3/logs/proc_make_check.log` |
| `make -j16 ids` | 0 | 3 s | `r3/logs/proc_ids.log` |
| `make -j16 figures` | 0 | 2 s | `r3/logs/proc_figures.log` |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 s | `r3/logs/proc_genmatrix.log` |
| `./syn/yosys/run.sh` | 0 | 130 s | `r3/logs/proc_yosys.log` |

| Processor suite | Reported checks passed | Failed |
|---|---:|---:|
| `acmp_listener` | 3111 | 0 |
| `acmp_nvm` | 388 | 0 |
| `acmp_talker` | 1342 | 0 |
| `adp_engine` | 1348 | 0 |
| `aecp_notify` | 30 | 0 |
| `ca_originator` | 16 | 0 |
| `desc_mem_guard` | 78 | 0 |
| `desc_store` | 586 | 0 |
| `dispatch` | 211 | 0 |
| `dyn_state` | 118 | 0 |
| `event_router` | 81 | 0 |
| `lsn_admit` | 18 | 0 |
| `maap` | 196 | 0 |
| `nvm_port` | 1219 | 0 |
| `originator` | 107 | 0 |
| `pp_top` | 10435 | 0 |
| `prng` | 76 | 0 |
| `release_merge` | 18 | 0 |
| `resp_buf` | 64 | 0 |
| `rx_slots` | 130 | 0 |
| `rx_validator` | 555 | 0 |
| `scoreboard` | 3705 | 0 |
| `side_port` | 368 | 0 |
| `srp_admission` | 991231 | 0 |
| `srp_decoder` | 190 | 0 |
| `srp_encoder` | 581 | 0 |
| `srp_stream_fsms` | 1219 | 0 |
| `srp_top` | 2200 | 0 |
| `timer_map` | 1360 | 0 |
| `timer_service` | 48 | 0 |
| `tx_arbiter` | 66 | 0 |
| `tx_slots` | 95 | 0 |
| `ucpu` | 437 | 0 |
| Total: 33 suites | 1,021,627 | 0 |

These are the runner's final tally from each suite, not a sum of every sub-leg's assertions. Correction to the earlier Round 2 prose: `tb/srp_top/Makefile:45` runs its four storage shapes before the end-to-end suite by default. The runner requires the whole command to succeed but reports only its last tally; the storage shapes are therefore exercised without being added separately to the displayed total.

### R3.5 Documentation gate table at head

The full `make -j16 check` receipt executes every target below. Separate `ids` and `figures` receipts are in the processor table.

| Gate | Result |
|---|---|
| `lint` | 41 flow/sequence and 18 waveform blocks, OK |
| `wavedrom-check` | 18 fresh exports, OK |
| `links` | 1,168 links, OK |
| `matrix` | 115 requirement rows / 17 gap findings, OK |
| `modmatrix` | 94 rows / 0 untested, OK |
| `params` | 28 top / 28 guide / 28 diagram parameters, OK |
| `ids` | 30 cases; 531 files / 91 IDs; 47 parameter / 36 timing rows, OK |
| `figures` | 17 cases; 3 source/export pairs / 18 waveforms / 5 hand-authored SVGs, OK |
| `stale` | rc 0 in the full gate |

### R3.6 Scratch-parent consumer set of 17 at head

Parent dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877` plus c8, p2-p1, c10 and 232, applied in that order. The existing scratch parent was checked against a separate temporary-index reconstruction. Every initialized submodule root and clean state was verified before git operations. Its processor checkout and staged gitlink name `5123548eb4de35f24d43eb088c12dab70b06d01d`. No parent commit or push. This source-consumer evidence does not replace the manager's final current-dev candidate validation.

| Command | rc | Time | Receipt |
|---|---:|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | 2 s | `r3/logs/p01_cpp_idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | 5 s | `r3/logs/p02_py_idiom.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 2 s | `r3/logs/p03_rtl_source_lists.log` |
| `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 4 s | `r3/logs/p03b_rtl_source_lists_selftest.log` |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 s | `r3/logs/p04_pp_srcs.log` |
| `python3 scripts/check_port_contracts.py` | 0 | 3 s | `r3/logs/p05_port_contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | 1 s | `r3/logs/p06_naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 7 s | `r3/logs/p07_test_evidence.log` |
| `python3 scripts/docs_check.py` | 0 | 5 s | `r3/logs/p08_docs_check.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | 145 s | `r3/logs/p09_xvlog.log` |
| `python3 -u sw/builder/test_builder.py` | 0 | 1675 s | `r3/logs/p10_test_builder.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | 263 s | `r3/logs/p11_lint_rtl.log` |
| `make -C tb/verilator/pp_shadow -j16` | 0 | 463 s | `r3/logs/p12_pp_shadow.log` |
| `make -C tb/verilator/nvm_cosim -j16 lint` | 0 | 256 s | `r3/logs/p13_nvm_cosim_lint.log` |
| `make -C tb/verilator/nvm_cosim -j16 quick JOBS=3` | 0 | 311 s | `r3/logs/p14_nvm_cosim_quick.log` |
| `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 2207 s | `r3/logs/p15_milan_dp.log` |
| `make -C tb/verilator/milan_dp_render -j16 VERILATOR_JOBS=3` | 0 | 1098 s | `r3/logs/p16_milan_dp_render.log` |

Builder rc 0 reports `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 1b's `MAKEFLAGS += -e` mutation has no effect under this Make 4.3, and gate 11 lacks the mf48 utilization report/build tree. Neither arm is counted as passed. The ordinary datapath shape summaries likewise report 1, 1 and 5 guarded checks not run in those respective shapes.

### R3.7 Execution and evidence limits

Commands run unpiped with separate log, rc and elapsed-time receipts. Independent suites, campaigns and builds run concurrently. Make uses `-j16`; the scratch simulator wrapper forwards to the pinned executable, limiting compilation to three concurrent invocations with at most three build workers each. No hardware parameter or stimulus changes. NVM quick receives `--jobs 3` through its Make variable; the datapath simulation pool receives `--jobs=2` from its default `SIM_JOBS` setting. The render leg-defect mode rejects `--jobs`; that option applies only to its separate boundary diagnostic. The parser runs alone after heavy jobs, under the shared lock.

The first background parser wait ended before lock acquisition without an rc/elapsed receipt; its cause is unknown and no OOM was reported. Its header-only `r3/logs/p09_xvlog_unfinished_wait.log` is NOT RUN and excluded from passing evidence. The replacement uses `r3/parser_attempt.py` with a bounded foreground lock wait: initially 45 seconds, then five minutes to retain queue position longer. A busy lock returns status 75 without starting the gate or creating a gate-result receipt. The final parser receipt measures the actual gate execution after lock acquisition, separately from these waits. `r3/parser-wait-note.txt` and `r3/parser-lock-attempts.jsonl` record the interruption and bounded attempts; no source change or other suite rerun is involved.

Environment identities and entry hashes/sizes are in `r3/environment.json`: simulator 5.050 (entry SHA256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`), Make 4.3, waveform renderer 2.0.3.post3, diagram CLI 11.16.0, standalone SVG renderer 2.62.4. Packages, binaries, generated images and raw build logs stay outside the output packet. Its manifest records sizes and SHA256 rather than copying artifacts over 200 KB.

All 24 required command receipts are rc 0. Processor results: 33 suites and 1,021,627 runner-reported checks, zero failing; 41 lint targets; 42 synthesis tops plus the Xilinx mapping check. Parent source-list self-test: 50/50. Shadow: 311 checks. NVM quick: 62 cases, 315 checks. Datapath: nine RESULT: PASS markers, four render mutants caught (six controls including the positive modes), and six grandmaster-step controls including five caught defects. Render: 65 and 245 positive checks; the leg-defect campaign passes 5/5, comprising two positive controls and three caught defects. The parser ran after every other command finished, under the shared lock; its two existing findings match the ratchet.

`r3/final-audit.log` records all 556 tracked blob byte/mode identities, equal HEAD/index trees, clean processor status including ignored files, the original source-base ancestry, unchanged remote main, and the one-line commit message. The generated processor build outputs were removed only after the suite runner finished (`r3/cleanup.log`). The same audit reconstructs c8, p2-p1, c10 and 232 in order with a temporary index, records each patch's size/SHA256, verifies the patched parent worktree, and checks every initialized submodule root before each git command. The non-processor pins match dev; the processor pin and checkout match this head. Parent HEAD remains `fea346e7` and was neither committed nor pushed.

The observed service memory peak is 5,327,597,568 bytes against the 12,884,901,888-byte cap, with no OOM events. `ROUND3-VALIDATION-RECEIPTS.tsv` records the log, control, measurement, environment and audit artifact sizes/SHA256 under the scratch root; `r3/results.json` records each final command and rc. No dependency installation, build tree, tree export or artifact over 200 KB is copied into the output packet. Hosted acceptance belongs to the manager after pushing. Physical calibration and hardware access were not run.
