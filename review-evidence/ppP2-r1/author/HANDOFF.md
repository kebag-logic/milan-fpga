# [A498] Lane P2 (NVM port robustness): HANDOFF

**Status: REVIEW READY** (#15 comment 5955151206); implemented under the ruling, every gate in §3 rc 0. Branch `p2-nvm-port-robustness`,
from main `2ebd4fe8d31e88c44559e934bd624e1c50515ad5`. Head `70bf017d62d60b4401126c7b1bb087f4cb115c5a`. Five commits:

| Commit | Subject | Items |
|---|---|---|
| `5425dc2` | Bound the NVM port's device waits with MEM_TIMEOUT_CYC_P, cause DEADLINE, owed-command containment and short-command refusal, graded under four handshake device models in tb/nvm_port | 1, 2, 3 (port), 4 (the cause) |
| `899d086` | Bind NVM_MEM_TMO_CYC_P = CLK_HZ_P at the top and document the port deadline, DEADLINE cause and owed-command quarantine in F01.5, F08.1, 02 §8, 07 §5.3, 08 §2, the integrator guide and diagram 21 | 2, 4 (07 §5.3) |
| `20a711c` | Grade a zero-byte DEADLINE and the amended alarm path in a second tb/acmp_nvm build, and a reset mid-flush in group R | 3 (manager), 4 |
| `82db3a2` | Say in the integrator guide's tie-off row that only a command the NVM face accepted stays owed | 2 (docs) |
| `70bf017` | Keep tb/nvm_port's functions under 100 lines and the cause port's comment free of a unit word, as the parent's idiom and naming ratchets require | the parent gates |

Each commit is self-consistent (the port and its suite; the top parameter and its
documents; the manager-side suite; a one-sentence docs fix; a refactor for the parent's
ratchets that changes no check). Every gate in §3 ran at the head.

Assignment: processor issue #15, comment 5951891343. Issues #15, #18, #19, #20, #21.
Posted on #15: TAKEN (5951917009); STOP (5952358239, the design, `STOP-COMMENT.md` here);
the ruling (5952386396, "authorized as designed"); REVIEW READY (5955151206). Every
`file:line` is at the head unless it names main `2ebd4fe8` or the parent (milan-fpga dev
`cdf49d1a`, read-only).

## 0. The ruling, and where each decision is carried

| Ruling | Carried by |
|---|---|
| `MEM_TIMEOUT_CYC_P` on the port and `NVM_MEM_TMO_CYC_P` at the top; a watchdog that counts only cycles where the device owes its next event; cause 3 = DEADLINE; no new port; no manager RTL change | `hdl/packet_engine/KL_pp_nvm_port.sv:121`, `:246-306`; `hdl/top/protocol_processor_top.sv:161-173`, `:2885-2887`; no port changed on any module; `KL_acmp_nvm_shadow.sv` and `KL_aecp_nvm_writer.sv` untouched |
| (a) `CLK_HZ_P` (1,000 ms) at the top, 100,000,000 on the port, stated in F01.5 and F08.1 as a derivation | `docs/architecture/01_overview.md:179`; `docs/architecture/08_timing.md:46`, `:67`; the port's parameter comment `:114-121`; the top's `:161-172` |
| (b) the abandoned WRITE is contained, ending only with the device's own terminal or a reset; the manager's error, retry and alarm path reports it | the owed command, `KL_pp_nvm_port.sv:283-306`; T24's contained arms; `tb/acmp_nvm` N12b |
| (c) criterion 2: busy falls at the DEADLINE pulse; every later request answered within the bound, served if the device has ended the abandoned command, else one err DEADLINE; both branches graded; the reading stated in the PR body | `tb/nvm_port` T24, served branch and DEADLINE branch (`the_next_request_after_a_deadline`); PR body, item 2 |
| (d) the parent's saved-state contract amended (three failed attempts and `nvm_alarm_o`, which revokes `nvm_backed` and drops the pending bit; quarantine never released by time alone), by a docs-only `parent-adoption-p2-cdf49d1a.patch` applied after the c4c6 patch | `parent-adoption-p2-cdf49d1a.patch` in this directory (§5 item 4); graded processor-side by `tb/acmp_nvm` N12b |
| #20: close with the STOP's proof plus one DEADLINE arm in `tb/acmp_nvm` | N12a-e, the second `tb/acmp_nvm` build (§1.4) |
| the out-of-context cost at the default and at the smallest legal value | §4 |

## 1. The design as implemented, per item

### 1.1 Item 1 (#21 and #19): the handshake models and the mutations they redden

**The line the README draws** ("Where a check may read from", and the new "The handshake
models"): a model of a contract FREEDOM must leave every check green; a model of a BROKEN
backend is graded on what the port owes it, never on service. Each model is one arming of
the harness's own backend left on for the whole run (`tb/nvm_port/sim_main.cpp`, the
`Harness` flags `unsol_model`, `done_on_last_byte`, `short_model`, `silent_model`),
applied by a `MODELS` row of `measure_figures.py`, beside the four array models:

| model | the device | the port's clause | class | result (326 checks) |
|---|---|---|---|---|
| unsolicited completion | one `done` per operation for no command, in a window the bus names (a commit's header still streaming in, a restore's being handed up) | refusal (c), `KL_pp_nvm_port.sv:52-62` | freedom | **326 PASS, 0 FAIL** |
| coincident completion | `done` on the edge that moves a command's final byte | the latch `:319-323`, the window `:233-244` | freedom | **326 PASS, 0 FAIL** |
| short read | every other READ it accepts ends with `done` after three eighths of its bytes (3 of a header's 8) | refusal (d), `:63-67` | broken backend | 251 PASS, 75 FAIL, service only |
| silent | every command granted, then nothing more | the deadline, `:69-108` | broken backend | 110 PASS, 216 FAIL, service only |

The array models keep their rows: pristine, half-page and page-buffered NOR 326/0; lazy
erase and lazy + page-buffered 325/1, only the pre-existing T1. (The page-buffered model
now discards its buffer when it takes a new command, as a real NOR's does; before the
deadline no WRITE was ever left unfinished without an err.)

**The run-wide checks, RW1-RW9**, close the run: every operation answered, none past
`run_op`'s guard; none answered twice; no device request while the backend owed one; no
DEADLINE where the device was not silent; every device error answered DEVICE; every READ
ended short answered with one err DEVICE and never done; under silence one err, never
done and never DEVICE; and witnesses that the unsolicited and short models fired.
`measure_figures.py` requires every RW check to PASS under every model, by name, so a
broken backend's FAIL count is service, never the port's side of the contract.

Harness changes, all on the bus side: a REGISTERED grant (the backend takes the request
on the edge that samples it and grants a cycle later, whether or not the request is still
up, as the parent's backend does, parent `hdl/milan/KL_nvm_backend.sv:851`, `:896`);
armed silence of one grant, byte or completion (`arm_silence`); a WRITE ended short
(`wshort_after`); a READ or WRITE ended on its own grant (`gnt_done_on_data`); a backend
whose busy reads idle while it owes (`busy_never`); strays during an ungranted request
(`stray_every`); a reset of the port alone (`port_forgot`); and orphan attribution, so the
late end of an abandoned command is credited to no operation.

**Issue #21's four mutations under their models, #19's four, the deadline's and refusal
(d)'s**, every row a measured row of the figures gate:

| row | mutation | model | fails | the first check it reddens |
|---|---|---|---:|---|
| M2-lo | the low magic byte compare forced true (`(hdr_r[1] == MAGIC_LO_C)` to 1) | pristine | 5 of 326 | `T26a the LOW magic byte: a commit framed 0x17FF is refused with one err, cause UNFRAMED` |
| M7 | the payload bound weakened `<=` to `<` | pristine | 4 of 326 | `T26c the payload bound's legal edge: the largest legal record` |
| done_seen_r/pristine | the latch set line deleted | pristine | 21 of 326 | `T21 the sticky done_seen_r latch: the commit takes a completion that rode the grant, rc=1` |
| done_seen_r/coincident | the latch set line deleted | coincident completion | 200 of 326 | `T1 commit completes with done, rc=1` |
| M8 | the header read's short-read defence off | pristine | 22 of 326 | `T23 c the short-read defence: the header read ended short at 5 bytes: one err, nothing for` |
| M8/short | the header read's short-read defence off | short read | 146 of 326 | `T2 restore completes with done, rc=1` |
| M6 | the latch armed in every state (#14's defect) | pristine | 50 of 326 | `T19a the commit still completes with done, byte-exact on the bus` |
| M6/unsolicited | the latch armed in every state (#14's defect) | unsolicited completion | 222 of 326 | `T1 commit completes with done, rc=1` |
| D1 | the deadline verdict forced false (#15's defect) | pristine | 52 of 326 | `T24 S_WEREQ: an event 101 cycles late ends the operation, one err, cause DEADLINE, never d` |
| D1/silent | the deadline verdict forced false (#15's defect) | silent | 267 of 326 | `T1 commit completes with done, rc=-1` |
| D2 | the verdict one cycle early | pristine | 33 of 326 | `T24 S_WEREQ: an event 100 cycles late is tolerated, done and byte-exact` |
| D3 | the verdict one cycle late | pristine | 35 of 326 | `T24 S_WEREQ: an event 101 cycles late ends the operation, one err, cause DEADLINE, never d` |
| D4 | progress does not restart the count | pristine | 27 of 326 | `T6 exactly one done for the one op` |
| D5 | a stalled manager counted in the commit payload pump | pristine | 3 of 326 | `T24 a manager stalling 300 cycles on every commit byte is never charged to the device: don` |
| D6 | a stalled manager counted in the restore payload pump | pristine | 2 of 326 | `T24 ...nor on every restore byte: done, byte-exact` |
| D7 | a done for no command counted as progress | pristine | 9 of 326 | `T24 dones for no command during an ungranted request do not hold the deadline off` |
| D8 | the verdict named DEVICE | pristine | 27 of 326 | `T24 S_WEREQ: an event 101 cycles late ends the operation, one err, cause DEADLINE, never d` |
| D9 | a deadline leaves nothing owed (timeout to idle) | pristine | 29 of 326 | `T24 S_RHCOLL: the next commit and restore are served byte-exact` |
| D10 | the late registered grant ignored | pristine | 23 of 326 | `T24 S_RHREQ: the next commit and restore are served byte-exact` |
| D11 | a late grant whose done rode it made owed | pristine | 2 of 326 | `T24 nothing was owed after a late grant that carried its done: the next commit is served` |
| D12 | the owed state released at the next deadline (by time) | pristine | 4 of 326 | `T24 ...and the owed READ is still drained after that deadline: the device moved its late b` |
| D13 | the owed state released when busy reads idle | pristine | 3 of 326 | `T24 contained: commit 0 after it ends DEADLINE, no command, no byte` |
| D14 | a request issued over an owed command | pristine | 5 of 326 | `T24 served branch: the next restore is served byte-exact once the device has ended the aba` |
| D15 | the owed READ not drained | pristine | 23 of 326 | `T24 S_RHREQ: the next commit and restore are served byte-exact` |
| D16 | a later deadline overwrites the owed kind | pristine | 3 of 326 | `T24 ...and the owed READ is still drained after that deadline: the device moved its late b` |
| D17 | the owed terminal latched as the next operation's | pristine | 8 of 326 | `T24 served branch: the next restore is served byte-exact once the device has ended the aba` |
| S1 | refusal (d) off in S_WHPUMP | pristine | 7 of 326 | `T27 d the WRITE ended after 5 header bytes` |
| S2 | refusal (d) off in S_WDPUMP | pristine | 5 of 326 | `T27 e the WRITE ended after 20 of 48 bytes` |
| S3 | refusal (d) off in S_RPPUMP | pristine | 15 of 326 | `T27 a the payload READ ended after 10 of 40 bytes` |
| S4 | S_RHCOLL reads only the live done (the pre-#15 defence) | pristine | 13 of 326 | `T27 b the header READ completed on its own grant` |

Under a model the first failing names are the model's own service failures; the
discriminating checks are the RW ones: M6 under the unsolicited model fails RW3 and RW4;
D1 under the silent model RW1 (the wedge), RW3 and RW7; M8 under the short-read model
RW4 and RW6; the latch deletion under the coincident model RW4.

**#19's four mechanisms each fail a check that names them:** the low magic byte (T26a,
T26b, "the LOW magic byte"), the payload bound at its legal edge (T26c, T26d, "the
payload bound's legal edge", a record of exactly `MAX_PAYLOAD_P`), the sticky latch
(T21, T22a-c, "the sticky done_seen_r latch"), the short-read defence (T23c, "the
short-read defence").

### 1.2 Item 2 (#15): the deadline

`hdl/packet_engine/KL_pp_nvm_port.sv`, no port changed (+174/-16):

| Change | Where | Contract it serves |
|---|---|---|
| banner: refusal (d); the Deadline paragraph; the owed command and the contained WRITE; `dev_gnt_i` means acceptance, at most one cycle after the edge that sampled the request | `:63-108` | the device face's one timing obligation, stated where 02 §8 leaves the face free |
| `MEM_TIMEOUT_CYC_P` (100,000,000) and `TMO_W_C`, counted at 33 bits so an out-of-range value still elaborates far enough to be named | `:114-126` | class E's name and idiom (`KL_aecp_resp_buf.sv:103-111`, `KL_aecp_desc_store.sv:176-183`) |
| `nvm_err_cause_o` code 3 DEADLINE | `:150-152`, `:546`, `:561` | 02 §8's reserved code, now produced |
| the elaboration guard, refused outside 1 to 2^31 - 1, naming the parameter | `:185-190` | R55-2 F2 on #15 (`N + 1` wraps at 2^32 - 1) |
| `owe_w` (the device owes its next event), `prog_w` (a grant, a byte, an err, or a done of ours or of the owed command; a done for nobody is no progress), the count and the verdict `dl_w` | `:246-282` | a no-progress bound: manager stalls are never charged, and an event on the verdict's own cycle wins |
| the owed command: set by a deadline in an owned state, or by a grant in the cycle after a deadline withdrew a request unless its terminal rides it; cleared only by its done or err, or reset; its kind taken only while nothing is owed | `:283-306` | containment for an untagged port; nothing released on time |
| the request states blocked while owed | `:354`, `:373`, `:426`, `:482`, `:581` | no device command over an owed one |
| refusal (d) in `S_WHPUMP`, `S_WDPUMP`, `S_RHCOLL` (the latched completion too), `S_RPPUMP` | `:385-390`, `:403-408`, `:446-450`, `:495-500` | a short command is a DEVICE error at once; a short payload read, or a READ completed on its grant, used to wedge the port |
| the deadline's transition | `:529-534` | one err, never done, busy low at the pulse |
| the owed READ's drain on `dev_rready_o` | `:586-589` | the device can end an abandoned READ |

The top, `hdl/top/protocol_processor_top.sv:161-173`: `NVM_MEM_TMO_CYC_P = CLK_HZ_P` with
its derivation, bound to the port at `:2885-2887`. `KL_pp_nvm_mgr_arb.sv:38-56`: the
banner now says the quarantine is the port's; no RTL change.

**The default, as a derivation** (F01.5 `P-NVM-MEM-TMO-CYC`, F08.1
`T-NVM-PORT-DEADLINE`): 20 times the parent backend's longest legal stall, its 50 ms
mutating-grant hold (parent `KL_nvm_backend.sv:142-145`, `:842-852`): 1,000 ms; equal to
`T-NVM-RS-AGGREGATE`, and 50 times the walks' 20 ms per-wait deadline, so the walks still
fail first. 100,000,000 clocks at 100 MHz, 50,000,000 at the product's 50 MHz.

**What `err` and busy do.** One `nvm_err_o`, cause DEADLINE, never done; `nvm_busy_o` low at
the pulse, exactly `MEM_TIMEOUT_CYC_P` + 2 clocks after the last handshake on either face
(T24, in all twelve owed states). **Why a slow but valid device never trips it:** the
count runs only in a cycle in which the device owes an event and gives none, every grant,
byte and terminal restarts it, and a manager stall owes nothing (T24: every owed event
`TMO` cycles late over more than forty deadlines' worth; manager stalls of three
deadlines on every byte, both directions).

**Criterion 2, as ruled.** Busy falls at the err, and every later request is answered
within the bound: served once the device has ended the abandoned command (T24 served
branch: a payload READ resumed 60 cycles after the verdict; the next restore waits, issues
nothing over it, and is served byte-exact from scratch), and one err DEADLINE, no command,
while the device stays silent (T24 DEADLINE branch: an ERASE whose done comes three
deadlines late; the request after the device's done is served). An owed READ is still
drained after a later deadline, and strays during an ungranted request hold nothing off.

**Elaboration controls** (`tb/nvm_port/elab_bounds.sh`, run by `make` before the build):
refused by name at 0, 2^31 and 2^32 - 1; built clean at 1 and 2^31 - 1.

### 1.3 Item 3 (#18): a reset mid-commit

`tb/nvm_port` T25 (`reset_mid_commit_at_six_stages`): `rst_n` at six stages named on the
bus (the header streaming; the ERASE requested and ungranted; the ERASE granted, not done;
the WRITE's header pump after 5 bytes; its payload pump after 9 bytes of the 32-byte
record, the reviewer's case on #18; its completion window), port and device both reset.
After release: no pulse, no request, no byte; the neighbour restores byte-exact; the torn
record is refused at its header (UNFRAMED) or forwarded whole and refused by the suite's
crc16, unless the old record (or, at the completion window, the new one) survived, and
the branch agrees with the stored header; where nothing reached the device the old record
restores; the next commit is byte-exact. Two resets of the port alone
(`reset_of_the_port_alone_mid_commit`): the device's late completion is discarded and
the port serves once the device has ended. **Who refuses a torn image that restores as
well-formed: the manager, by the crc16** (`KL_acmp_nvm_shadow.sv:391-395` `rrec_ok_w`;
`KL_aecp_nvm_writer.sv:482-485` `frame_ok_w`), documented in the README's "A reset
mid-commit". `tb/acmp_nvm` group R grades it on the real binding manager: R1, the ERASE
granted and not done; R2, 12 bytes into the WRITE (the port forwards the torn record
whole, header then payload READ, and the crc16 refuses it). The walk completes, the other
sinks restore, sink 3 answers its default, and the change made again persists. The crc
gate forced true fails R2. **README wording:** "Power-cut coverage" is now "Torn commits:
a device err (T15-T18) and a reset (T25)", saying which phases do which; the harness's T15
heading no longer says power cut; the "No phase asserts rst_n" limit is gone.

### 1.4 Item 4 (#20): a dying flash is not a blank region

At main, with no RTL change: a DEVICE err with zero bytes fails the whole walk, cause 2
(`KL_acmp_nvm_shadow.sv:584-586`), pinned by N1a-d; the blank path (a clean done, or an
UNFRAMED err) is the record's default, pinned by A2/A2b, F4, N2a-b, N9c, with G2 green; B02
(#20's defect, both edits) killed (README mutation record). Added: the port's third
zero-byte err, DEADLINE, in a second `tb/acmp_nvm` build whose port deadline (1,000) is
below the walk's (3,000). **N12a** a header read granted and never answered: the port
answers DEADLINE with nothing forwarded and the whole walk fails with cause 2, never an
empty record, before the walk's own deadline; **N12d** a face that never grants, likewise;
**N12e** an erased face: done, not failed, blank, no alarm, no deadline. Planted
defects: a zero-byte DEADLINE read as blank fails N12a and N12d; the deadline removed
fails N12a-d; nothing owed after a deadline fails N12c; the first build stays green
under all three. 07 §5.3's DEVICE row reads "DEVICE ... or DEADLINE"
(`07_memory_maps.md:639`), and so does the D3 table (`:701`).

### 1.5 Item 5: the parent-visible list

§5.

## 2. What main carried (read and measured at `2ebd4fe8`, before any code)

- The port named its cause: 1 DEVICE, 2 UNFRAMED, "3 is reserved for a port deadline and
  never produced here" (main `KL_pp_nvm_port.sv:87-94`).
- #20's split was already in the binding manager (main `KL_acmp_nvm_shadow.sv:584-594`)
  and the D3 writer (`KL_aecp_nvm_writer.sv:476-479`): each reads a zero-byte err whose
  cause is not UNFRAMED as a device failure, so DEADLINE needs no manager change.
- Completion ownership (#14) was scoped, and T21/T22 covered the latch.
- #19's mutations at main (pristine model, 136 checks): the low magic byte forced true
  failed only T23h, which does not name it; the payload bound `<=` to `<` was GREEN; the
  latch deleted failed 9; the header short-read defence off failed 10.

## 3. Gates at the head

Head `70bf017d62d60b4401126c7b1bb087f4cb115c5a`. Pinned Verilator 5.050. Every processor
command ran on a `git archive` export of the head under the lane's scratch area, except
the figures gate, which reads pinned git revisions and ran in the lane tree (the tree
stayed clean, ignored files included). Logs and rc files in the scratch area; none is
in this directory.

**Processor, all rc 0:**

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map gate (61 constants, 89 entry points), M9 opcode gate (30); **37 suites, 1,019,328 checks, 0 failing**: `nvm_port` 326 (136 at main), `acmp_nvm` 388 = 372 + 16 over its two builds (360 at main), `pp_top` 9,151 (unchanged: the top's `NVM_MEM_TMO_CYC_P` is 1,000,001 clocks there, beyond every case); 934 s |
| `./scripts/lint_hdl.sh` | 0 | 41 modules, LINT OK |
| `make check` | 0 | 41 mermaid + 18 WaveDrom blocks; links 1,045; REQ matrix 115 rows, 17 GAP; module matrix 94 rows, 0 untested (`gen_matrix.py --check`); parameters 28 = 28 = 28; diagram exports not stale |
| `make -C tb/nvm_port figures` (lane tree) | 0 | 76 builds (1 + 12 arms + 49 mutations and probes + 9 models + 5 matrix); baseline 326/326; **all measured figures agree with the tree**; RW checks pass under every model; one waiver (2 illustrative phrasings) |
| `make -C tb/nvm_port` elaboration guard (`elab_bounds.sh`, inside the suite run) | 0 | refused by name at 0, 2^31, 2^32 - 1; clean at 1, 2^31 - 1 |
| `./syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| `make -C tb/srp_top mutants` | 0 | 78 of 78 killed, 11 controls pass, assertion coverage 65/65 |
| `make -C tb/maap mutants` | 0 | 29 of 29 killed, 3 controls pass |
| `make -C tb/adp_engine mutants` | 0 | 30 of 30 killed, 2 controls pass |
| `make -C tb/pp_top aecp-mutants` | 0 | 55 of 55 killed, 5 controls pass |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 35 of 35 killed, 3 controls pass |
| `python3 tb/pp_top/d3_mutants.py --jobs 3` | 0 | goldens pass (`tb/acmp_nvm` in its two builds, `pp_top`, `rx_validator`); **83 of 83 KILLED** by their named checks; 1,960 s |
| `tb/nvm_port` mutations (the figures gate's 49 rows, §1.1 table) | - | every row killed, each count equal to the README |
| `tb/acmp_nvm` planted defects (scratch probes, §1.3, §1.4) | - | a zero-byte DEADLINE read as blank: N12a, N12d fail; the port deadline removed: N12a-d fail; nothing owed after a deadline: N12c fails; the crc gate forced true: R2, F5, F10, F14, F15 fail; the first build green under the first three |

Not run: the other mutation drivers outside CI (`notify_mutants.py`, `acmp_mutants.py`,
`gsi_mutants.py`, `retry_mutants.py`, `srp_admission/mutants.py`, `name_wr_mutant.py`);
they plant edits in modules this lane does not change, and the `pp_top` and `acmp_talker`
suites they drive pass unchanged above. Hosted CI and Docker/act: not run here.

**Parent consumer set, the 16 commands,** at milan-fpga dev `cdf49d1a` in a scratch copy: a
`git archive` of the trusted checkout; gptp-processor and verilog-axis exported at their
recorded pins (`5dce647a`, `48ff7a7e`); the processor exported at the head, each
submodule directory a repository at its recorded commit; the index read from the trusted
HEAD (984 entries) with only the processor gitlink moved to the head;
`parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-p2-cdf49d1a.patch` applied
(`git apply --check` clean, in that order). The copy's porcelain was empty before the
gates.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | every ratchet within budget (long function 0 <= 0, after the refactor commit `70bf017`) |
| 3, 4 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `check_port_contracts.py` | 0 | processor 1,757 ports (unchanged: no new top port), undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 96 candidates, all recorded; 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8, 9 | `docs_check.py`, `xvlog_gate.py --check` | 0, 0 | 0 findings over 185 md + 956 files (the p2 patch's edits included); 4 findings == ratchet, the same four |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local mf48 build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS; the mutant arms pass |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms caught |

Two parent gates failed at the earlier head `82db3a2` on this lane's own code, and
`70bf017` fixed both: the C++ idiom ratchet (`sample_dev` and the reset phase over 100
lines; split, behaviour unchanged, every figure re-measured green) and the naming ratchet
(the cause port's comment gained the word "cycles"; reworded).

## 4. Out-of-context cost

`KL_pp_nvm_port` as its own top: sv2v v0.0.13, then Yosys 0.66 `synth_xilinx -family xc7
-flatten` (the baseline's recipe; no Vivado on this host):

| Configuration | LUT | FF | CARRY4 | MUXF7 | MUXF8 | vs main |
|---|---:|---:|---:|---:|---:|---|
| main `2ebd4fe8` | 197 | 118 | 14 | 15 | 6 | - |
| head with the deadline verdict tied off (refusal (d) and structure only) | 228 | 119 | 14 | 12 | 3 | +31 LUT, +1 FF |
| **head at the default**, `MEM_TIMEOUT_CYC_P` = 100,000,000 (a 27-bit count) | 257 | 148 | 21 | 25 | 9 | **+60 LUT, +30 FF, +7 CARRY4** |
| **head at the smallest legal value**, 1 (a 1-bit count) | 249 | 122 | 14 | 14 | 5 | **+52 LUT, +4 FF** |
| head at 125,000,000 (a 125 MHz `CLK_HZ_P`) | 250 | 148 | 21 | 24 | 9 | +53 LUT, +30 FF, +7 CARRY4 |
| head at the largest legal value, 2^31 - 1 (a 31-bit count) | 244 | 152 | 22 | 27 | 8 | +47 LUT, +34 FF, +8 CARRY4 |

The watchdog and the owed command alone (head minus the tied-off verdict): +29 LUT, +29 FF,
+7 CARRY4 at the default; +21 LUT, +3 FF at 1. The FF figures are exact (the count's width
plus `owed_r`, `owed_rd_r` and `lg_r`); the LUT figures move by a few with ABC's mapping,
which is why the largest value maps smaller than the default.

## 5. The parent-visible list

1. **`KL_pp_shadow` instance: no edit.** It binds `CLK_HZ_P` and leaves the NVM times to
   the top on purpose (parent `hdl/milan/KL_pp_shadow.sv:1098-1105`), and
   `NVM_MEM_TMO_CYC_P` follows the clock the same way. No new top port, so the
   port-contract gate's count is unchanged. That comment names three NVM parameters it
   leaves unbound; a fourth now exists, which the pin-adoption lane may add to the comment
   (an RTL comment, so not in this docs-only patch).
2. **Consumer gates.** `nvm_cosim` instantiates `KL_pp_nvm_port` directly, unparameterised
   (parent `tb/verilator/nvm_cosim/cosim_top.sv:374`), at 1 MHz: the module default is
   100 s there, beyond every case, so D4c-D4e do not change (the ruling: re-grading them
   under the top's derivation is not this lane's). `pp_shadow`'s unanswered window is
   about 4.0 M cycles, below the top's 10^8 at 100 MHz. The 16 commands were re-run (§3).
3. **Persistence behaviour on the board.** A healthy device: none. A device face that
   stops answering for `NVM_MEM_TMO_CYC_P` (1 s): the abandoned operation ends with err
   DEADLINE; a later change is attempted three times, each ended DEADLINE with no device
   command, then `nvm_alarm_o` rises and the change's pending bit drops, which revokes
   `nvm_backed` through the backend's alarm input. Before: busy and pending for ever. The
   device is still never reused before it ends the abandoned command, or a reset.
4. **`parent-adoption-p2-cdf49d1a.patch`** (this directory; sha256 `3dda850924ffe4150aa33703ac82c0784035e3387070b7c9b5fc537a7467d08b`, 9,728 bytes;
   `git apply` after `parent-adoption-c4c6-ea3fb388.patch`, sha256
   `67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c`, unchanged). Docs
   only, one file, `docs/design/SAVED_STATE_MATERIALIZATION.md`: §8.8 ("The abandoned
   read"; "Command availability and persistence availability"), the W13 row and the
   sentence after the W table, and §15 item 4 (now AMENDED), as ruled; plus two
   consequential sentences that would otherwise contradict them, §6.4's "keeps the port
   QUARANTINED for ever: every later change reads pending" and the stage table's
   release-notes line. The negative control "release quarantine by time alone" is
   untouched.
5. **Processor documents the parent reads:** 02 §8 (code 3 and the deadline paragraph,
   anchor `sec-02-nvm-deadline`) and §8.2 (the drain row), 07 §5.3, 08 §2 (the F08.1 row,
   the saved-state table, the quarantine paragraph), F01.5, the integrator guide (§2 row
   and NVM tie-off row), diagram 21's inventory (28 parameters) and its PNG.

## 6. What remains

- Hosted CI on the PR, and the reviewers' rounds.
- The parent adopts both patches when it moves its processor pin past this head.
- Three of the twelve `if (dev_err_i)` arms stay uncovered, as at main: the request arms of
  the ERASE, the WRITE and the payload READ, where an err replaces a grant (`gnt_err` is
  armed only for the header READ). The randomized cut points of `09_verification.md:56`
  are still owed; T15-T18 and T25 cut at fixed points.
- Re-grading the parent's `nvm_cosim` D4c-D4e under the top's derivation (ruled out of
  this lane).
