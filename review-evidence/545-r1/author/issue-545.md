# 545 CRF servo integrates a policy-legal 100 us PHC slew at 200 ppm and drops to ACQUIRE
[A10] Found by [A227] while fixing #539 (simulation, not yet bench).

## Observed
Under the owner step policy (#387 5794731090 with FPGA-gPTP#68 ruling 5798089412), a locked offset up to 100 us is slewed at the 200 ppm clamp. With CRF selection, a 100 us slew at 200 ppm moves the CRF servo integrator from +30.62 to +80.66 ppm, and the servo drops to ACQUIRE. A slew is not a step, so neither the #539 step discard nor the 1024 ppm guard sees it. Traces are in the A227 packet (PR for #539).

## Authority
#387 decision part (b): return to steady state through one bounded, counted event, with no multi-minute walk. Milan v1.2 Annex B.1.1 (+-100 ppm media clock).

## Acceptance
1. Decide the intended coupling: the media clock follows a gPTP slew (then the servo must not treat it as an error or lose lock), or the slew rate is bounded so the servo stays locked. Record it on #387.
2. Implement it with a simulation of the 100 us / 200 ppm slew and a failing arm; the servo stays LOCKED (or the decided state) and the integrator returns within a stated bound.
3. Gates green.

Relations: #387, #539. Backlog.

https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5816509756
[A10] Acceptance 1 is decided at https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816509317: discard and count the slew-overlapped windows, and stay LOCKED. The slew-active indication comes from the gPTP plane. ASSIGNMENT [A263]: executor, base dev `57456af9`.

https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5816629893
[A263] REVIEW READY

**STOPPED: the pinned gPTP processor exports no slew-active indication. No implementation is ready.** This follows the assignment's explicit stop condition.

Head: `57456af96b3127b9d309a995bbbd35a6113ce52d`, unchanged on `545-crf-servo-slew`. Working tree and index are clean; no commits or RTL changes.

The processor pin is `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`. Its [PHC interface](https://github.com/Mister-M-alt/FPGA-gPTP/blob/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/hdl/top/KL_gptp_engine.sv#L101) exports only addend write/data and step write/data. The [slew branch](https://github.com/Mister-M-alt/FPGA-gPTP/blob/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/hdl/ucode/gen_gptp_ucode.py#L828) computes PI trim without publishing slew state. The [interface contract](https://github.com/Mister-M-alt/FPGA-gPTP/blob/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/docs/INTEGRATION.md#L272) explicitly says synchronization is asserted while a slew may still be in progress.

**Exact signal needed:** a registered, `clk_i`-synchronous one-bit level, provisionally `phc_slew_active_o`, covering the plane's transient policy correction through the rate path, with explicit start and completion semantics that distinguish ordinary frequency tracking. It must cover the intervals between Sync pairs and define reset, loss of synchronization, and replacement-step behavior. The parent must carry it through `KL_gptp_shadow` and `milan_datapath`, aligned with the effective PHC rate and the servo's staged sample. Every partly overlapped window must be discarded, including the tail after deassertion. The combined addend, its write pulse, `S_LOCK`, synchronization flag, and measured offset cannot substitute for that state.

There is also a duration conflict to resolve: the new decision calls 0.5 s a maximum, while the [pinned contract](https://github.com/Mister-M-alt/FPGA-gPTP/blob/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/docs/INTEGRATION.md#L260) and `docs/design/TIME_SYNC.md:99` say 0.5 s or more. The prescribed 100 us / 200 ppm trace does not establish a maximum for the real PI loop. No timer or inferred slew detector was introduced.

Validation: pin and relevant source blob checks passed; `git diff --check` and both base/index empty-diff checks returned 0. The requested suites, mutant, documentation gates and area synthesis were **NOT RUN** after the explicit prerequisite stop. Area source delta is zero; no new measurement is claimed. Acceptance 2 and 3 are unmet.

`HANDOFF.md` and the blocked `PR-BODY.md`, with source references, test/mutant/gate tables and the archived #539 trace, are in the assigned A263 output packet. A reviewed processor export and completion contract are required before this lane can resume. No push, PR action, merge, other checkout, delegation, or hardware action occurred.


https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5816653226
[A10] [A263] stopped correctly: the pinned gPTP processor exports no slew-active level. The prerequisite is filed as Mister-M-alt/FPGA-gPTP#75, with [A263]'s exact signal contract, and [A265] is assigned to it. #545 resumes when that lands: a parent change pins the new gPTP head, carries the level through `KL_gptp_shadow` to the servo, and implements the discard.

https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5827358783
[A10] #545 resumes. FPGA-gPTP PR #76 merged as `5dce647a` and exports a registered `phc_slew_active_o` level (contract in its `docs/INTEGRATION.md`). #546 has landed on dev (`5b73d3f4`).

Citation correction to decision 5816509317 (issue #387): the ±100 ppm bound is IEEE 802.1AS Annex B.1.1 (LocalClock), not Milan Annex B.1.1. The media-source bound is Milan v1.2 Section 7.4 (±50 ppm). The decision is otherwise unchanged.

Scope for [A303], on dev `5b73d3f4`:
1. Pin `gptp-processor` at `5dce647a`. Re-record the ROM digests with the repository tool, and update SUBMODULES, the pin text and the CHANGELOG.
2. Carry `phc_slew_active_o` through `KL_gptp_shadow` to the CRF servo in the same clock-domain discipline the plane's other levels use (state the crossing, if any).
3. `KL_mmcm_drp_servo` discards and counts every rate window that overlaps the slew, as it does the #539 step window. It holds its integrator and stays LOCKED, and trusts windows again when the slew ends, with no ACQUIRE. Expose the count wherever the #539 step discard is counted, or say why it shares that tally.
4. Tests:
   - `tb/verilator/mmcm_servo`: the 100 µs / 200 ppm slew from the #539 packet keeps the servo LOCKED, with the integrator within a stated bound.
   - Mutants: removing the slew discard fails; tying the level low fails.
   - A `milan_dp` leg (or the `gptp_shadow` bench) proves the level reaches the servo from the real plane.
5. Docs: `TIME_SYNC.md` loop table and step policy, `GM_LOSS_RECOVERY.md` rows (the CRF servo and media grid aligner rows now say #545 is closed), and `REGISTER_MAP.md` for any tally.
6. Area delta for the RTL change. Keep the redundancy path open: no single-port assumption.

Reviewers: [R300] internal, [R301] external.

