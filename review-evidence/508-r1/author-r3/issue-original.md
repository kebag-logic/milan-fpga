[A10] PP (protocol processor) integration tracking. Backlog until the donor interface is settled; no implementation has started.

## Objective and observed evidence

Make the parent product report the listener's actual probing/ACMP status and registered MSRP failure bridge ID through GET_STREAM_INFO, including unsolicited responses.

At parent dev `b17580b91deb11f3441dfc5d7f9fafe539d929b8`, [the stream-info gather](https://github.com/kebag-logic/milan-fpga/blob/b17580b91deb11f3441dfc5d7f9fafe539d929b8/hdl/milan/milan_datapath.sv#L4730) returns zero for a sink failure bridge ID. [Selector 7](https://github.com/kebag-logic/milan-fpga/blob/b17580b91deb11f3441dfc5d7f9fafe539d929b8/hdl/milan/milan_datapath.sv#L4737) derives DISABLED/PASSIVE/COMPLETED from bound/settled and fixes acmpsta to zero. PP owns the actual state but does not yet make all these values available to the parent.

Donor implementation contracts:

- PP failure bridge export: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43
- PP probing/ACMP status publication or response ownership: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/49

This is an integration gap, not an assertion that either PP correction has landed.

## Authority and boundaries

Milan v1.2 sections 5.3.8.6, 5.3.8.8, and 5.4.5.2/Table 5.22; PP `docs/architecture/02_interfaces.md` F02.10 and `06_aecp_engine.md` F06.13; parent `REQUIREMENTS.md` sections 1/2/8; `docs/reference/SUBMODULES.md`; the GET_STREAM_INFO gather in `hdl/milan/milan_datapath.sv` and PP wrapper in `hdl/milan/KL_pp_shadow.sv`.

PP owns the listener/SRP state and its public face. This repository owns adoption of the reviewed donor revision, adaptation through the wrapper, the parent gather/event path, and product evidence. If PP resolves the status internally instead of adding outputs, record that seam and adapt the parent accordingly; do not duplicate the state owner.

Closed #69 is notification integration history. Closed #472/#490 and residue #495 concern other SRP status encodings/cleanup. They do not own these missing fields. Release qualification stays in #76.

## Scope and acceptance

1. Record the final PP-owned interface and merged donor revision. A cold reviewer can follow each field from its PP state owner to a controller response.
2. With real PP/root wiring, GET_STREAM_INFO reports DISABLED after unbind, PASSIVE after bind, ACTIVE with the specified ACMP failure after probe timeout, and COMPLETED after successful settle. acmpsta is zero outside the state where Milan permits it.
3. A registered Talker Failed carries the injected code and full 64-bit bridge ID for the correct sink; withdrawal/replacement clears or changes them per the PP validity contract. Test two distinct sink values in a supported multi-sink shape, plus reset and a missing descriptor.
4. Solicited and unsolicited responses use the same current values. The notification path detects these changes, excludes the requester where required, and does not announce a fabricated transition.
5. Tying each new field to zero, selecting the wrong sink, and retaining the current probing approximation each fail a completed-scenario assertion. Existing output-stream status and parent SRP status-word behavior remain covered.
6. Update the authoritative integration/status limitations only after executable evidence exists.

Out of scope: implementing the donor state machines in the parent; unrelated SRP timing, NVM state, redundancy, or broad notification redesign.

## Validation

Run the new real-wiring cases through `make -C tb/verilator/pp_shadow` and the relevant `tb/verilator/milan_dp` response/notification path. Expected: correct byte-exact replies at every named transition; all negative controls fail their named property. Record exact commands, configuration, donor pin and results. Complete the donor gates, the parent `scripts/run_all_suites.sh <fresh-log-directory>`, `syn/yosys/run.sh`, lint/xvlog and required local/hosted gates on the candidate, as CONTRIBUTING requires. Review every applicable lens before merging.

## Dependencies, readiness and roles

Depends on settled PP43/49 interfaces and their reviewed donor delivery, then a separately validated parent pin/integration. Conflicts with other owners of `KL_pp_shadow.sv`, the stream-info gather and its tests; assign one lane before edits. Executor: unassigned. Independent reviewers: unassigned. Remains Backlog until the donor seam and candidate integration base are recorded. No existing issue's criteria change.
