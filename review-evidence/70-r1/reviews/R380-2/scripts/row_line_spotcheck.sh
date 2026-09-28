#!/bin/sh
# Print the processor lines that new D3 section 15.2 rows and the FASTCONNECT
# status row cite, at the pinned processor. Run from the parent repository root.
set -u
PP=protocol-processor
echo "## processor $(git -C $PP rev-parse HEAD)"
show() { echo "=== $1:$2"; sed -n "$2" "$PP/$1" | cut -c1-170; }
show docs/architecture/02_interfaces.md '532,536p'
show docs/architecture/05_acmp_engine.md '160,161p'
show docs/architecture/08_timing.md '42,43p'
show docs/architecture/01_overview.md '100,107p;170p'
show docs/architecture/04_adp_engine.md '159p'
show docs/guides/integrator.md '334,336p'
show docs/guides/integrator.md '355p;377p'
show docs/guides/operator.md '202,206p'
show docs/diagrams/21-integration-faces.svg '31p'
show docs/diagrams/24-adp-acmp-states.svg '114p'
show hdl/top/protocol_processor_top.sv '124,130p;1645p;2523p;2540,2546p;4200p'
show hdl/acmp/KL_acmp_nvm_shadow.sv '14p;30,31p;119,120p;864,873p;885,893p'
show hdl/packet_engine/KL_pp_nvm_port.sv '9,12p'
show hdl/aecp/KL_aecp_desc_mem_guard.sv '18,21p;54p'
show hdl/aecp/KL_aecp_dyn_state.sv '123p'
show docs/guides/hdl-engineer.md '137p'
