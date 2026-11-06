## Scope

Move the `protocol-processor` gitlink from `a9e84b66` to processor main `92100657`, which carries processor #212 / PR #213. The SRP Listener applies a Talker Advertise or Talker Failed registered before the sink's ACMP settle, and on a re-bind (Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4; IEEE 802.1Q-2022 10.7). The per-port and sink registrars go to MT on LINK_DOWN and LINK_UP (Table 10-4).

## Required in the parent

1. Re-record the ROM digests through their recorder.
2. Re-run the parent gates that read the SRP listener (milan_dp, the SRP campaigns, rtl-fast) and `check_cpp_idiom.py`. Re-record any campaign count the new rows move, through its own recorder.
3. Update the pin page, the CHANGELOG and the integrator-facing text: the pre-settle path's reach with the shipping N, and the link-change behaviour.
4. The parent route was measured on the manager's scratch parent: 52,497 LUT, +503; slices 15,780 of 15,850; WNS +0.198 ns. Re-measure it at this PR's head under the Vivado slot and record it.

## Acceptance

The full sweep, the firmware self-test, the builder, behave, the docs gates and the docs inventory are green. The route meets the WNS floor.
