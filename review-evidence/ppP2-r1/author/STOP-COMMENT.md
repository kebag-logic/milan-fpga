[A498] STOP

Head `2ebd4fe8d31e88c44559e934bd624e1c50515ad5`: branch `p2-nvm-port-robustness` is unchanged, with no code written and no commits. The design is complete and is in the lane's HANDOFF. It needs a new parameter, new registers and a persistence change the parent can see, so as the assignment requires I am stopping for a ruling before any code.

**What main already has**
- The port's `nvm_err_cause_o` already keeps code 3 "for a port deadline" (`KL_pp_nvm_port.sv:87-94`, 02 §8). So the question of telling "the device said nothing" from "the device said no" needs no new port.
- #20's split landed with #93. A DEVICE `err` with zero bytes fails the whole walk with `restore_cause_o` 2. A clean `done`, or an UNFRAMED `err`, with zero bytes is the per-record default (`KL_acmp_nvm_shadow.sv:584-594`). `tb/acmp_nvm` pins this in N1a-d, A2/A2b, F4 and N2/N9c, and G2 is green. Its mutation record kills #20's defect as B02 (12 of 349).
- #19 at main, measured on the pristine model:
  - The low-magic mutation goes red only through T23h, no check names it, and nothing reaches the commit side.
  - Weakening `payload_length <=` to `<` stays green (136/0).
  - Deleting the latch two ways turns 9 checks red (T21, T22, idle).
  - Turning off the header short-read defence turns 10 red (T23c).

**Proposed parameters, ports and defaults**

| item | proposal | default |
|---|---|---|
| `KL_pp_nvm_port` parameter | `MEM_TIMEOUT_CYC_P`, using class E's name and idiom (`KL_aecp_resp_buf.sv:103-111`, `:245`, `:384-385`). The width is `$clog2(N+1)`. The counter clears on any cycle the port is not waiting on the device, and the verdict comes at N. The legal range is 1 to 2^31 − 1; elaboration refuses anything outside it with an error that names the parameter. | 100,000,000 (1,000 ms at 100 MHz) |
| `protocol_processor_top` parameter | `NVM_MEM_TMO_CYC_P`, bound to the port and derived the way `NVM_RS_TMO_CYC_P` is. New rows: F01.5 `P-NVM-MEM-TMO-CYC` and F08.1 `T-NVM-PORT-DEADLINE`. | `CLK_HZ_P` (1,000 ms) |
| registers, in the port only | the watchdog counter (27 bits at the default), `owed_r`, `owed_rd_r`, and a one-cycle late-grant check | 0 at reset |
| ports | None on any module. `nvm_err_cause_o` code 3 becomes DEADLINE. | n/a |

**Behaviour**
- **What the watchdog counts.** It counts only cycles in which the device owes its next handshake event and does not give it. That event is a grant, the byte the port presents, the byte the port accepts while the manager is ready, or the terminal. Every grant, byte or terminal restarts the count. `S_WHDR`, `S_RHFWD` and manager stalls never count, so a slow device that keeps moving never trips it.
- **Why 1,000 ms.** It is 20 times the parent backend's longest legal stall, its 50 ms mutating-grant hold (`KL_nvm_backend.sv:119-123`, `:143-145`). It equals `T-NVM-RS-AGGREGATE`. It is far above the walks' 20 ms per-wait deadline, so restores do not change.
- **On expiry.** The port gives one `err` with cause 3 (DEADLINE) and never `done`. `nvm_busy_o` falls at the pulse and the next request is accepted.
  - Both managers already treat a zero-byte `err` that is not UNFRAMED as a device failure (`KL_acmp_nvm_shadow.sv:584-585`, `KL_aecp_nvm_writer.sv:478-479`). They also already take any write `err` into DR2c. So no manager RTL changes.
  - F07.9's err, bounded retry, then alarm path becomes reachable for a silent device.
- **No reuse before the device ends the abandoned command.** `owed_r` blocks every device request. It drains the late bytes of an abandoned READ and discards them. Only that command's own `done` or `err`, or a reset, clears it.
  - The late grant: a grant presented in the cycle after a request was withdrawn on its deadline counts as an acceptance and sets `owed_r`. This is the backend's registered grant (`:851`, `:896`).
  - A request that arrives meanwhile waits with the watchdog running. It is served if the device ends the old command. Otherwise it ends with one `err` DEADLINE.
  - Nothing is released on time, so "release quarantine by time alone" stays a valid negative control.
- **Short commands.** In all four data phases, a completion seen before the final byte moves ends the operation with `err` DEVICE. Today only the header read does this; a short payload read, or a READ completed on its own grant, wedges the port.
- **The abandoned WRITE.** If the device then waits for its next byte for ever (`KL_nvm_backend.sv:962-966`), the WRITE is contained, not recovered, until reset.

**Parent impact**
1. **`KL_pp_shadow`.** No edit is needed. It binds `CLK_HZ_P` and leaves the NVM times to the top (`KL_pp_shadow.sv:1098-1105`). There is no new top port, so the port-contract count does not change.
2. **Consumer gates.**
   - `nvm_cosim` instantiates the port directly, with no parameters, at 1 MHz (`cosim_top.sv:64`, `:374`). The module default is 100 s there, so nothing changes.
   - If the parent makes it transcribe the new top derivation (1 s at 1 MHz), D4c, D4d and D4e (memory silent through an accepted WRITE for 3.5 s) would see port errors and DR2c retries inside their windows. Re-grading them is the parent's.
   - `pp_shadow` section K's silent window is about 4.0 M cycles at 100 MHz, below 10^8, so it does not change.
   - All 16 commands are to be re-run on the implementation.
3. **Board.**
   - With a healthy device, nothing changes.
   - If the device face goes silent for 1 s, the abandoned operation ends with `err`. Each later change fails its three attempts at the port's deadline without any device command. Then `nvm_alarm_o` rises, which revokes `nvm_backed`, and the change's pending bit drops.
   - Today the port stays busy and the change stays pending for ever: SAVED_STATE_MATERIALIZATION W13, §8.8 and §15 item 4. That page would need amending.
4. **Processor documents the parent reads.** 02 §8 and §8.2, 07 §5.3, 08 §2 (`:66`, `:87-90`), F01.5 and F08.1, the integrator guide's parameter table and its tie-off row (`:359`), and diagram 21.

**Decisions requested**
- (a) The default.
- (b) The abandoned WRITE. The options are:
  - containment (proposed);
  - padding it to its length, which the parent can see because the backend would close the record;
  - an abort face, which is an interface change.
- (c) Whether this meets "serves the next request": the request is served once the device has ended the abandoned command, and answered with a bounded `err` DEADLINE while the device stays silent.
- (d) The parent D3 contract amendment in impact item 3.

Items 1, 3 and 4 (the #21 and #19 models and named checks, the #18 reset phases and README wording, and the #20 proof plus one DEADLINE arm) need no new parameter, port or register. The assignment stops before any code, so they follow in order after the ruling.
