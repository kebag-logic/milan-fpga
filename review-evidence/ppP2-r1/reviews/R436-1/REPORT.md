[R436] NEGATIVE - exact head 70bf017d62d60b4401126c7b1bb087f4cb115c5a

# R436-1: internal independent review of PR #145 (lane P2, NVM port robustness)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #145. It closes #15, #18, #19, #20 and #21.
- Exact head `70bf017d62d60b4401126c7b1bb087f4cb115c5a`, tree `529d9a3779fe8503fd5c7c9798df16c2df11a689`. Base `main` `2ebd4fe8d31e88c44559e934bd624e1c50515ad5`, five commits.
- Round R436-1, cleared context, own detached clone. After all probes the clone was verified byte-identical to the head (`receipts/clone_integrity.txt`). The repository has no gitlinks.

## Verdict

**NEGATIVE.** Two MINOR findings stay open, so the Conformance and Tests lenses are unclean.

- **F1:** three planted defects in the owed-command logic pass all 326 checks of the PR's suite.
- **F2:** #21's fourth acceptance item is not met, and the PR still closes #21.

The RTL itself held up under every probe I ran:
- the watchdog;
- the owed command and the late registered grant;
- refusal (d) in all four data phases;
- the elaboration guard;
- the top binding.

The parent patch is docs-only, as ruled, and applies cleanly. There is one wording RESIDUE.

## How the review was reconstructed

Read in the order assigned:
1. `README.md` and `docs/README.md` (there is no AGENTS.md or CONTRIBUTING.md in the tree).
2. The bodies and acceptance lists of issues #15, #18, #19, #20 and #21.
3. On #15:
   - the maintainer's scope and reachability corrections (5355168983, 5355231359);
   - the readiness assignment (5573417155);
   - the lane assignment (5951891343);
   - the author's design STOP (5952358239);
   - the manager's ruling (5952386396);
   - the review-ready note (5955151206).
4. The PR body.
5. The authorities:
   - the port banner;
   - 02 §8 and §8.2, 07 §5.3, 08 §2, F01.5 and F08.1;
   - the `tb/nvm_port` README's freedom and broken-backend line;
   - class E's idiom (`KL_aecp_resp_buf.sv:103-111`, `:245`, `:384-385`).
6. The full diff `2ebd4fe8..70bf017d` and its history.
7. The public evidence at milan-fpga `d56e2227` `review-evidence/ppP2-r1`:
   - the manifest;
   - both parent patches (sha256 verified against the manifest);
   - the PR body, which is identical to the live one.
8. The parent's public sources at dev `cdf49d1a`, read-only:
   - `KL_nvm_backend.sv`, for the registered grant (`:851`, `:887`, `:896`, `:1047`) and the 50 ms hold (`:119-123`, `:143-145`);
   - `SAVED_STATE_MATERIALIZATION.md` and `SAVED_STATE_FASTCONNECT.md`.

What I did not read:
- the September proposal-stage review reports on #15, which reviewed a donor proposal, not this PR;
- the author's HANDOFF and STOP files.

**Prior public review findings on PR #145: none.** The only PR comments at this head are the two review-start notices. There is nothing to resolve or retain.

## Executed evidence (exact head; receipts listed in MANIFEST.sha256)

The simulator is the pinned Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`).

| Run | rc | Result | Receipt |
|---|---:|---|---|
| `make -C tb/nvm_port run`, which includes `elab_bounds.sh` | 0 | 326/326. ELAB OK at 1 and 2^31-1. GUARD OK at 0, 2^31 and 2^32-1, each refused by name | `receipts/base_nvm_port.log` |
| `make -C tb/acmp_nvm run` (two builds) | 0 | 372 + 16 = 388/388 | `receipts/base_acmp_nvm.log` |
| `make -C tb/nvm_port figures` | 0 | 76 builds, "all measured figures agree with the tree" | `receipts/base_figures.log` |
| `scripts/lint_hdl.sh` | 0 | 41 modules LINT OK | `receipts/head_lint.log` |
| `make check` | 0 | 41 mermaid, 18 wavedrom, 1,045 links, matrices (94 rows, 0 untested), parameters 28 = 28 = 28 | `receipts/head_check.log` |
| `make -C tb/pp_top run` | 0 | 9,151/9,151 | `receipts/head_pptop.log` |
| `tb/pp_top/d3_mutants.py --jobs 8` | 0 | goldens PASS; 83 of 83 KILLED by their named checks. A redundant partial re-run killed 44 of 44 | `receipts/head_d3.log`, `receipts/head_d3_part2.log` |
| reviewer probe campaign (`scripts/probe.py`) | - | 73 builds: planted defects, model runs, directed checks, TMO variants | `receipts/probes*/` |
| out-of-context cost (`scripts/ooc_cost.sh`: sv2v, then Yosys `synth_xilinx -flatten`) | 0 | see the RTL lens | `receipts/ooc/` |
| parent patch check | - | docs only, base blob matches, `git apply --check` clean | `receipts/parent_patch_check.txt` |

The figures gate's model rows, as measured:
- pristine, half-page, page-buffered NOR, coincident completion and unsolicited completion: 326/0 each;
- lazy erase and lazy erase + page-buffered: 325/1 each (T1);
- short read: 251/75;
- silent: 110/216.

The RW checks pass by name under all nine.

## Reviewer probes (planted defects; each a fresh `git archive` copy, exact-anchor edits)

All runs are against the PR's own 326 checks under the pristine model unless the model column says otherwise. "Killed" means the suite turned red.

**The watchdog**

| ID | Planted defect | Result (fails of 326) |
|---|---|---|
| W1 | verdict one cycle early | 33 |
| W2 | verdict one cycle late | 35 |
| W25 | an event in the verdict cycle ignored | 31 |
| W26 | watchdog removed | 52; 267 under silent, RW1 among them |
| W3 | an unowned done counts as progress | 9; also 9 under unsolicited |
| W4b | a manager write stall charged to the device | 3 |
| W5 | a manager read stall charged to the device | 2 |
| W17 | the verdict never ends S_RPWAIT | 2 |
| W18 | S_RHWAIT not owed | 2 |
| W19 | DEADLINE reported as DEVICE | 27 |
| W20 | busy held while a command is owed | 8 |
| W6 | the count paused rather than cleared on unowed cycles | **0**, and 0 with the directed checks below. Behaviour-equivalent for any contract-legal device; see S1 |

**The owed command**

| ID | Planted defect | Result (fails of 326) |
|---|---|---|
| W7 | a deadline in an owned state leaves nothing owed | 29 |
| W24 | S_RPWAIT dropped from the ownership window | 1 |
| W8 | late registered grant not owed | 23 |
| W9 | late grant owed even when its terminal rides it | 2 |
| W10 | quarantine released at a later deadline (release by time) | 4 |
| W27 | quarantine released at a deadline in a request state | 4 |
| W11 | an owed command ended by done only, never by err | 2 |
| W12 | owed READ never drained | 23 |
| W13 | owed kind overwritten by a later deadline | 3 |
| W14 | `dev_req_o` not gated by the owed command | 5 |
| **W15** | `S_RHREQ` not gated by `owed_r`: the owed command's err is credited to the waiting restore | **0 (survives)** |
| **W15b** | the same in `S_WEREQ` | **0 (survives)** |
| **W16** | drained owed-READ bytes are not progress | **0 (survives)**; also no change under silent |

**Refusal (d)**

| ID | Planted defect | Pristine | Coincident | Short |
|---|---|---|---|---|
| W21 | off in S_WDPUMP | 5 | 5 | 79 |
| W22 | off in S_RPPUMP | 15 | 15 | 166 |
| W23 | off in S_WHPUMP | 7 | 7 | 81 |

The PR's suite kills 24 of these 28 planted RTL defects.

**#19 and #21 mutations, rebuilt independently**

| ID | Mutation | Result (fails of 326) | Checks that name the mechanism |
|---|---|---|---|
| X1 | low magic byte | 5 | T26a/b |
| X2 | `<=` weakened to `<` | 4 | T26c/d |
| X3 | latch deleted | 21 pristine; 200 coincident | T21/T22 |
| X4 | latch armed in every state | 50 pristine; 222 unsolicited | T19a/T20a, RW3 |
| X5 | header short-read defence off | 22 pristine; 146 short | T23c, RW6 |

Every figure matches the PR body and the README.

**tb/acmp_nvm**

| ID | Planted defect | Result |
|---|---|---|
| A1 | a zero-byte DEADLINE read as blank | 2nd build: N12a, N12d fail (3) |
| A2 | the binding manager's crc16 term forced true | 1st build: R2 fails, with F5, F10, F14, F15 (6) |
| A3 | port deadline removed | 2nd build: N12a-d fail (5) |
| A4 | the deadline leaves nothing owed | 2nd build: N12c fails (1) |

**Directed reviewer checks** (`R436a-c`, injected into probe copies only, never proposed as the PR's code):
- **R436a:** an owed payload READ is ended by the device's err while a later restore waits in S_RHREQ. The restore must be served.
- **R436b:** an owed ERASE is ended by err while a later commit waits in S_WEREQ. The commit must be served.
- **R436c:** an owed READ drains one byte per TMO/2 for more than 4×TMO cycles while a restore waits. The restore must be served, never refused.

Results:
- The head passes all three: **333/333** (`receipts/probes2/H0__rtest.log`).
- W15 fails R436a, W15b fails R436b, and W16 fails R436c ("served after 133 cycles (rc 1 cause 3)").
- W6 still passes.

**Parametric variants, with no defect.** The harness constant `TMO` and `-GMEM_TIMEOUT_CYC_P` were moved together:
- to 37: 4 fails;
- to 1000: 3 fails.

Reading the harness timing, these are harness artefacts, not port defects:
- At 37, the fixed 40-cycle `op_delay` and silence windows exceed the deadline. A device that slow is illegal at that TMO.
- At 1000, `3*TMO` manager stalls × 48 bytes exceed `kOpTimeoutCycles` (100,000).

The suite is evidence only at its pinned TMO = 100 (S2).

## Findings

### F1 - MINOR - Tests

The owed command's "credited to no operation" end, and the restart of the count by drained bytes, are unpinned. Three planted defects pass all 326 checks.

- **Where:**
  - The guards are `hdl/packet_engine/KL_pp_nvm_port.sv:354` (`S_WEREQ: if (!owed_r)`) and `:426` (`S_RHREQ: if (!owed_r)`). The term is `:271` (`|| (dev_rvalid_i && dev_rready_o)`, where `dev_rready_o` carries the drain at `:589`).
  - The suite's owed-command phases are `tb/nvm_port/sim_main.cpp:1919-1998` (`the_next_request_after_a_deadline`) and `:2000-2051` (`an_abandoned_write_is_contained`).
- **Authority:**
  - Port banner `KL_pp_nvm_port.sv:77-79`: "Every grant, byte and terminal restarts the count, so a device that is slow but moving is never refused".
  - Banner `:85-93`: the device's "next done or err as that command's end, credited to no operation. A request that arrives meanwhile ... served once the device has ended the abandoned command".
  - The same in 02 §8 (`docs/architecture/02_interfaces.md:536`, `:542`).
  - 09 §8.5 (`docs/architecture/09_verification.md:304-305`) lists these properties as covered by T24 and D4-D17.
  - Assignment focus (1), "drained READ bytes". #19's own defect class: an RTL mechanism whose mutation leaves the suite green.
- **Evidence:**
  - W15, W15b and W16 are each 326/326 PASS (`receipts/probes/W15__pristine.log`, `W15b__pristine.log`, `W16__pristine.log`); under silent, W16 is identical to the baseline.
  - The head passes reviewer checks R436a-c, and each mutant fails its own one (`receipts/probes2/`).
  - The suite's served branch ends the owed command only with a `done` (`sim_main.cpp:1927-1940`). Its only err-ended owed command (`:2026`) is ended with no request waiting. Its drains complete inside one TMO.
- **Impact:** a regression of this kind ships green.
  - W15/W15b: the abandoned command's err is reported as the next operation's DEVICE failure. Both managers turn that into a failed walk (cause 2) or a failed write attempt toward `nvm_alarm_o`, against a device that then works.
  - W16: a contract-legal, slow but moving device is refused DEADLINE while it drains.
- **Required outcome:** add standing checks that:
  - (a) end an owed command with `err` while a later request waits, for both a restore (S_RHREQ) and a commit (S_WEREQ), and require that request served;
  - (b) drain an owed READ slowly across more than TMO cycles while a request waits, and require it served.
  Record W15, W15b and W16 (or equivalents) in the README's mutation record so the figures gate measures them.
- **Verification:** with the new checks, each of W15, W15b and W16 fails a check that names the mechanism, the head stays green under every contract-legal model, and `make -C tb/nvm_port figures` agrees.

### F2 - MINOR - Conformance, Tests

#21's acceptance item 4 is not met, and the PR closes #21. Check T1 stays red under the lazy-erase model, which is a contract freedom.

- **Where:**
  - The check is `tb/nvm_port/sim_main.cpp:888`, `CHECK(h.store[3][f1.size()] == 0xFF, "T1 erase visible past the record")`.
  - The model table is `tb/nvm_port/README.md:883-884`: lazy erase is 325 PASS, 1 FAIL, "only the pre-existing `T1`".
  - The PR body says "Closes #21".
- **Authority:**
  - #21, acceptance item 4: "The existing 83 checks stay green under every model the port is contractually required to tolerate."
  - Lazy erase is such a model. The port's banner allows it: `KL_pp_nvm_port.sv:33-34`, "backends without erase semantics answer ERASE with done at once". The README calls it "real" (`README.md:810-817`).
  - The README's own rule (`README.md:822-829`) is to assert after a `done` only on what the port put in the array. It names T1 as the one remaining violation and leaves it "as it is".
  - The assignment (5951891343): "The PR closes each issue whose acceptance it meets in full, and relates to the rest."
- **Evidence:**
  - The figures gate at the head measures lazy erase at 325/1 and lazy erase + page-buffered at 325/1 (`receipts/base_figures.log`, model rows).
  - T1 is one of the original checks.
- **Judgement on the author's call:** the author is right that this assertion measures the backend's side effect, not the port. That diagnosis is the reason to fix or condition the check in this lane, not a reason to call the item met. As shipped, the literal criterion fails under a model the port must tolerate.
- **Required outcome:** either:
  - (a) make T1's array assertion model-neutral, so both lazy-erase rows read 326 PASS, 0 FAIL, the README table and prose say so, and the figures gate agrees. For example, rely on the bus-level ERASE pins T1 already has (`sim_main.cpp:881-883`, `:886`) and drop or condition the array side effect; or
  - (b) change "Closes #21" to a relation, naming item 4 as unmet.
- **Verification:** `make -C tb/nvm_port figures` model rows, or the PR body's closing keywords.

### R1 - RESIDUE - Docs (wording only)

`tb/nvm_port/README.md:794-797`, added by this PR, is a sentence fragment: "The first of those, coincident completion -- the device raises `dev_done_i` on the same edge that moves a pump's final byte, which `KL_pp_nvm_port.sv:319-323` says the sticky `done_seen_r` latch exists for."

**Exact fix:** "The first of those is coincident completion: the device raises `dev_done_i` on the same edge that moves a pump's final byte, which `KL_pp_nvm_port.sv:319-323` says the sticky `done_seen_r` latch exists for."

### S1 - SUGGESTION - Robustness

The watchdog clears, rather than pauses, on any cycle the device owes nothing (`KL_pp_nvm_port.sv:280`).

- In S_WDPUMP and S_RPPUMP, a manager that dropped `wvalid` or `rready` at least once every TMO cycles would therefore keep a silent device from ever reaching the deadline.
- This cannot happen today. Both in-tree managers hold them for the whole stream (`KL_acmp_nvm_shadow.sv:963`, `:966`; `KL_aecp_nvm_writer.sv:1092`, `:1094`), and so does the arbiter (`KL_pp_nvm_mgr_arb.sv:178-182`, where the drain holds `rready` high).
- Pausing the count (probe W6) passes every check, mine included, and closes the gap.
- Either adopt it, or state the manager-face hold requirement beside the banner's "it owes nothing while ... the manager holds the operation".

### S2 - SUGGESTION - Tests

The harness constants are fixed numbers:
- `op_delay` 40 and the 40-cycle windows in T25;
- the 30-cycle drain;
- `kOpTimeoutCycles`;
- the `3*TMO` stalls.

None is derived from `TMO`, so the suite is only evidence at its pinned `-GMEM_TIMEOUT_CYC_P=100`; the variants at 37 and 1000 fail for harness reasons. `elab_bounds.sh` covers elaboration at the extremes, not behaviour. Deriving the constants from `TMO` would let one more build grade a second bound.

## Issue-by-issue acceptance

| Issue | Item | Status | Evidence |
|---|---|---|---|
| #15 | 1. A silent device: one err within a bounded time | MET | T24 in all twelve owed states, at TMO (tolerated) and TMO+1 (DEADLINE, gap TMO+2); RW7 under silent; W1/W2/W25/W26 killed |
| #15 | 2. Busy low, and the next request served | MET on ruling (c) | busy low at the pulse (W20 killed); the served branch and the DEADLINE branch are both graded; the err-terminal variant of the served branch is unpinned (F1) |
| #15 | 3. The bound is a parameter named as in class E | MET | `MEM_TIMEOUT_CYC_P`, `TMO_W_C` and `tmo_hit_w`, with the same clear-when-not-waiting idiom as `KL_aecp_resp_buf.sv:103-111`, `:245`, `:384-385`; bound at the top as `NVM_MEM_TMO_CYC_P = CLK_HZ_P` (`protocol_processor_top.sv:173`, `:2885-2887`) |
| #15 | 4. A silent-device standing model | MET | the `silent` model; figures row 110/216; RW checks pass |
| #18 | 1. `rst_n` mid-commit at more than one stage, state pinned after release | MET | T25a-f (six stages named on the bus); T25g-h (port alone) |
| #18 | 2. The torn well-formed image refused, or documented as the manager's by crc16 | MET | `README.md:571-581` names `rrec_ok_w` and `frame_ok_w`; `tb/acmp_nvm` R2 grades it on the real binding manager; A2 (crc forced true) fails R2 |
| #18 | 3. README wording on "power cut" | MET | `README.md:63-69`: T15-T18 are a device err, T25 a reset |
| #19 | 1. Each of the four mutations reddens, with a named message | MET | X1-X5 above |
| #19 | 2. Coincident and short-read standing models | MET | figures rows |
| #19 | 3. The payload bound at both edges | MET | T26c/d (`== MAX_PAYLOAD_P`); T11/T13 (`+1`) |
| #20 | 1. A zero-byte device err distinguishable from blank | MET | `KL_acmp_nvm_shadow.sv:584-594`; N1a-d (main); N12a/N12d add DEADLINE; A1 killed |
| #20 | 2. Blank first boot yields defaults with no alarm | MET | A2/A2b and N12e |
| #20 | 3. `tb/acmp_nvm` pins both; A2, F4 and G2 stay green | MET | 388/388; d3 goldens; B02 killed |
| #21 | 1. Four handshake models, standing, documented | MET | `README.md:582-616` |
| #21 | 2. Each justified against the contract | MET | the class column cites refusal (c), the latch window, refusal (d) and the deadline |
| #21 | 3. The four mutations redden under their model | MET | 222, 200, 146 and 267 fails, reproduced |
| #21 | 4. The existing checks green under every required model | **NOT MET** | T1 under lazy erase (F2) |

## Lens results

### Conformance (UNCLEAN: F2)

The design is as ruled in 5952386396:
- the port parameter and the top derivation, stated as a derivation in F01.5 (`01_overview.md:179`) and F08.1 (`08_timing.md:46`);
- cause 3 = DEADLINE;
- no new port, and no manager RTL change (the arbiter diff is comments only);
- containment of an abandoned WRITE, never padding;
- nothing released by time (W10 and W27 killed);
- both branches of criterion 2 graded.

The parent's 50 ms hold and its registered grant are as cited in the parent source. The only conformance defect is the #21 closure (F2).

### RTL (CLEAN)

I traced every owed state, `owe_w`/`prog_w`, the verdict timing (TMO+1 owed cycles, pulse at TMO+2), and the owed set and clear paths:
- set on a verdict in an owned state;
- set on a late grant whose terminal does not ride it;
- the owed kind is latched only while nothing is owed;
- cleared only by `done`, `err` or reset.

Also traced: the request gating, the drain, the cause priority, and the reset of every new register. The elaboration guard is `:187-190`, with a 33-bit width calculation at `:125-126`.

There is no wedge path:
- every state in which the port can wait indefinitely is held by the manager (S_IDLE, S_WHDR, S_RHFWD, and the manager-stalled pumps);
- every device wait is owed;
- the verdict forces S_FIN (`:531-534`).

Out-of-context cost, reproduced exactly (main: 197 LUT, 118 FF, 14 CARRY4):

| Setting | Cost |
|---|---|
| default | +60 LUT, +30 FF (27-bit counter + `owed_r` + `owed_rd_r` + `lg_r`), +7 CARRY4 |
| `MEM_TIMEOUT_CYC_P = 1` | +52 LUT, +4 FF |
| 2^31-1 (extra point) | +47 LUT, +34 FF |

Lint is clean over 41 modules.

### Robustness (CLEAN; S1 advisory)

- **A slow but valid device, or a stalled manager, never trips the deadline.** T24 covers both; W4b and W5 are killed; and by construction a contract-legal device presents each owed event within TMO.
- **The late registered grant is handled.** That is the parent backend's `gnt_r` (W8 and W9 killed).
- **Drained READ bytes restart the count** in the RTL (R436c passes at the head).
- **Reset clears every new register.** A port-only reset leaves the device's late terminal to refusal (c) (T25g/h).
- **A device that stays silent after a port-only reset mid-data-phase is contained**, not wedged: every later request ends DEADLINE.
- **One residual risk is unreachable in-tree** (S1).

### Tests (UNCLEAN: F1, F2)

- 326 checks, of which 190 are new, across T24-T27 and RW1-RW9.
- Nine models.
- 49 mutations and probes gated by the figures tool.
- My 73-build campaign confirms every PR figure it touches.
- The three meaningful survivors define F1; W6 is benign (S1).
- T1 under lazy erase is F2.

### Docs (CLEAN; R1 residue)

These read consistently with the RTL:
- 02 §8 and §8.2, 07 §5.3 (the DEVICE-or-DEADLINE row, and what the walk deadline does not do), 08 §2;
- F01.5 and F08.1;
- the integrator guide's parameter and tie-off rows;
- diagram 21 (the parameter list, with the PNG regenerated);
- 09 §8.5;
- the top comment and the arbiter banner.

`make check` agrees, with parameters 28 = 28 = 28. Line citations in the PR body and the README were spot-checked, and the ones checked were correct (the banner's `:52-62`, `:63-67`, `:69-108`, `:121`, `:185-190`, `:246-282`, `:283-306`, `:319-323`; the top's `:161-173`, `:2885-2887`; the shadow's `:391-395` and `:584-586`; the writer's `:482-485`).

**Parent patch `parent-adoption-p2-cdf49d1a.patch`:**
- sha256 `3dda850924ffe4150aa33703ac82c0784035e3387070b7c9b5fc537a7467d08b`, 9,728 bytes;
- docs only: one file, `docs/design/SAVED_STATE_MATERIALIZATION.md`, 7 hunks;
- the base blob `21dc772` matches dev `cdf49d1a`, and `git apply --check` is clean;
- the files are disjoint from the c4c6 patch.

It amends W13, §8.8 and §15 item 4 as ruled, plus the §6.4 paragraph and the stage release notes, both disclosed. There is no gate, script or RTL change, and the DR1a register row is untouched. "(the saved-state page's section 9.2)" follows the page's own usage for `SAVED_STATE_FASTCONNECT.md`, whose §9.2 covers the `nvm_alarm` revocation of `nvm_backed`.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issues #15 and #18-#21 (acceptance lists); #15 comments 5355168983, 5355231359, 5573417155, 5951891343, 5952358239, 5952386396, 5955151206; PR body; F01.5, F08.1, 02 §8; parent `KL_nvm_backend.sv` and saved-state pages at `cdf49d1a` | R436-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| RTL | CLEAN | `KL_pp_nvm_port.sv` (all 612 lines), `KL_pp_nvm_mgr_arb.sv`, `protocol_processor_top.sv` (the diff and the port instance), the managers' cause and stream drivers; lint over 41 modules; OOC stats | R436-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| Robustness | CLEAN (S1 advisory) | watchdog, owed command, late grant, drain, reset; 28 planted RTL defects; TMO variants | R436-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| Tests | UNCLEAN (F1, F2) | `tb/nvm_port` (`sim_main.cpp`, README, `measure_figures.py`, `elab_bounds.sh`, Makefile); `tb/acmp_nvm` (`sim_main.cpp` groups R and N12, wrap, Makefile, README); `tb/pp_top`; `d3_mutants` | R436-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |
| Docs | CLEAN (R1 residue) | 01, 02, 07, 08 and 09 diffs; integrator guide; diagram 21 (SVG and PNG); `tb/nvm_port` and `tb/acmp_nvm` READMEs; parent patch | R436-1 | 70bf017d62d60b4401126c7b1bb087f4cb115c5a |

## Real limits

- Home-directory prefixes in the raw logs are redacted to `$HOME`; nothing else in the receipts is edited.
- No Vivado run. The OOC cost is sv2v plus Yosys `synth_xilinx`, the same instrument the PR body names, not a Vivado utilization report.
- Not run here:
  - the full `run_suites.sh` bank;
  - the five CI mutation campaigns (`srp_top`, `maap`, `adp_engine`, and `pp_top`'s aecp and aecp-dispatch);
  - `syn/yosys/run.sh`;
  - any parent gate.
  I ran only the suites the diff touches (`nvm_port`, `acmp_nvm`, `pp_top`), lint, `make check`, the figures gate and `d3_mutants`.
- The parent patch was checked for applicability on the cdf49d1a blob and read in full. The parent consumer set was not executed.
- The PR's own D1-D17 and S1-S4 mutation definitions were measured only through the figures gate, which agreed. My W/X probes were designed independently.
- The TMO=37 and TMO=1000 failures were attributed to harness constants by reading the harness timing, not by a rebuilt harness.
- I did not locate public receipts for the manager's source static, builder and native banks at this head beyond the PR body's table; the manager owns them.
- Physical calibration NOT RUN. No hardware. Field skips are not hardware proof.
- I did not inspect hosted CI.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at this head, with `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-p2-cdf49d1a.patch`.
- Hosted CI and act acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- Build the final current-dev candidate at the merge turn (source base `2ebd4fe8`, live dev `cdf49d1a`).
- Carry R1 to the residue checklist.
- Route F1 and F2 to the author. Re-review the fix head, re-running probes W15, W15b and W16 (`scripts/probe.py ... W15 W15b W16`) and the figures gate.

R436-1 FINISHED
