Reviewer citation assessment at parent ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5.

Each occurrence was checked in its donor-page context. Resolution is mechanical; the support judgments below come from inspection of the cited source and linked requirements.

| Exact parent target | Occurrences | Assessment | Result |
|---|---:|---|---|
| [hdl/milan/milan_datapath.sv:73](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/hdl/milan/milan_datapath.sv#L73) | 5 | Enabled default is an executable parameter value. | Supports claim |
| [docs/design/GPTP_PLANE.md:6](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/design/GPTP_PLANE.md#L6) | 5 | Explicit fabric ownership of product time synchronization. | Supports claim |
| [docs/design/GPTP_PLANE.md:49](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/design/GPTP_PLANE.md#L49) | 3 | Option-off elaboration is restricted to verification. | Supports claim |
| [docs/design/GPTP_PLANE.md:48](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/design/GPTP_PLANE.md#L48) | 1 | One atomic bank supplies every public consumer. | Supports claim |
| [docs/design/GPTP_PLANE.md:43-44](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/design/GPTP_PLANE.md#L43-L44) | 2 | Product configurations enable the plane; disabled product configurations are rejected. | Supports claim |
| [docs/ARCHITECTURE_HW_SW_SPLIT.md:165](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/ARCHITECTURE_HW_SW_SPLIT.md#L165) | 1 | Option-off has no product image. | Supports claim |
| [README.md:167-170](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/README.md#L167-L170) | 5 | Ownerless option-off publishes zero identity/path/delay/health, uncertain time, and inert writes. | Supports claim |
| [hdl/milan/milan_datapath.sv:7614-7624](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/hdl/milan/milan_datapath.sv#L7614-L7624) | 1 | Disabled generate branch wires control TX through in both data and ready directions. | Supports claim |
| [hdl/milan/milan_datapath.sv:2850-2858](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/hdl/milan/milan_datapath.sv#L2850-L2858) | 1 | Disabled rate and phase selections choose CSR inputs. | Supports claim |
| [hdl/milan/milan_datapath.sv:2850-2852](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/hdl/milan/milan_datapath.sv#L2850-L2852) | 1 | Absolute settime stays at the CSR face independently of plane selection. | Supports claim |
| [docs/ARCHITECTURE_HW_SW_SPLIT.md:165-175](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/ARCHITECTURE_HW_SW_SPLIT.md#L165-L175) | 3 | Verification-only ownerless boundary and safe failure publications are explicit. | Supports claim |
| [docs/guides/gptp/MANAGER.md:33-35](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/guides/gptp/MANAGER.md#L33-L35) | 1 | Calibration and reference-peer physical acceptance remain incomplete. | Supports claim |
| [docs/design/GPTP_PLANE.md:350-366](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/design/GPTP_PLANE.md#L350-L366) | 1 | The v1.2 boundary excludes asymmetry, retains one correction owner, and excludes live product tuning. | Supports claim |
| [docs/design/GPTP_PLANE.md:363-366](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/docs/design/GPTP_PLANE.md#L363-L366) | 1 | Two per-board constants are applied once; donor compensation and live tuning are outside the product contract. | Supports claim |

Total: 31 occurrences, 14 exact targets in five parent files. REQUIREMENTS.md is an additional authority, verified as a sixth parent source file.

Issue #13 provenance: its final public author comment (5379946471) explicitly records the earlier default-off integration. The historical forward note is therefore supported by the issue discussion even though its initial issue body described the proposed transition.

No certification or completed physical-calibration inference follows from these documentation and source checks.
