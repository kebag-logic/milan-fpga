# Third-party dependencies

Git submodules provide imported RTL.

Gitlinks define their exact revisions.

## Contents

- **[Submodules](#submodules)** — Identify imported ownership.
- **[Generated C](#generated-c)** — Identify generated trace sources.
- **[Working safely](#working-safely)** — Preserve reproducible imports.

## Submodules

| Path | Upstream | License | Root use |
|---|---|---|---|
| `external` | `kebag-logic/fpga-avb-ethernet` | See submodule | Legacy Ethernet top only |
| `gptp-processor` | `Mister-M-alt/FPGA-gPTP` | CERN-OHL-W-2.0 | Fabric gPTP engine |
| `protocol-processor` | `Mister-M-alt/protocol-processor-control-plane-avb-milan` | CERN-OHL-W-2.0 | ADP, ACMP, AECP, and SRP |
| `third_party/verilog-axis` | `alexforencich/verilog-axis` | MIT | AXI-Stream primitives |

Use the [verified submodule map](docs/reference/SUBMODULES.md).

That map records every exact Gitlink.

It also records root integration boundaries.

The [historical migration plan](docs/history/v1/integration/OPEN_SOURCE_MIGRATION.md) preserves earlier decisions.

## Generated C

| Path | Upstream | License | Verification |
|---|---|---|---|
| `sw/trace/generated/barectf.c` | barectf 3.1.2 | MIT | Trace round-trip gate |
| `sw/trace/generated/barectf.h` | barectf 3.1.2 | MIT | Trace round-trip gate |
| `sw/trace/generated/barectf-bitfield.h` | barectf 3.1.2 | MIT | Trace round-trip gate |
| `sw/trace/generated/metadata` | barectf 3.1.2 | MIT | Python decoder gate |

Generated files remain committed.

This keeps basic gates self-contained.

Regenerate them from `sw/trace/milan_trace.yaml`.

Use the [trace guide](sw/trace/README.md).

## Working safely

```sh
git clone --recurse-submodules <repository>
git submodule update --init --recursive
python3 scripts/check_submodule_docs.py
```

- Never copy imported RTL into root code.
- Review upstream changes before pin updates.
- Run donor suites before root suites.
- Commit only intentional Gitlink changes.
- Keep every submodule clean during validation.
