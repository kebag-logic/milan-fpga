# SPDX-License-Identifier: Apache-2.0
"""Write the reviewer plant specs used by plants.py into the given directory."""
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
B = "tests/features/switch_bindings.c"
E = "tests/features/environment.py"
A = "src/modules/sim_adapter.c"
EN = "    return shlan_port_enable(sw, port_id);"
DI = "    return shlan_port_disable(sw, port_id);"
CO = "    return shlan_connect(sw);"
DC = "    shlan_disconnect(sw);"
author = [
 ("a-disable-dispatch", B, DI, "    return shlan_port_enable(sw, port_id);"),
 ("a-disable-mapping", E, 'getattr(lib, f"shlan_test_{name}")', 'getattr(lib, "shlan_test_" + name.replace("disable", "enable"))'),
 ("a-disable-port", B, DI, "    return shlan_port_disable(sw, (uint8_t)(port_id + 1u));"),
 ("a-enable-dispatch", B, EN, "    return shlan_port_disable(sw, port_id);"),
 ("a-connect-noop", B, CO, "    (void)sw;\n    return 0;"),
 ("a-connect-dispatch", B, CO, "    shlan_disconnect(sw);\n    return 0;"),
 ("a-disconnect-dispatch", B, DC, "    (void)shlan_connect(sw);"),
]
mine = [
 ("r-disable-calls-enable", B, DI, "    int rc = shlan_port_enable(sw, port_id);\n    return rc;"),
 ("r-connect-noop", B, CO, "    return sw ? 0 : -1;"),
 ("r-enable-noop", B, EN, "    (void)sw;\n    (void)port_id;\n    return 0;"),
 ("r-disable-noop", B, DI, "    (void)sw;\n    (void)port_id;\n    return 0;"),
 ("r-enable-xor-port", B, EN, "    return shlan_port_enable(sw, (uint8_t)(port_id ^ 1u));"),
 ("r-enable-wraps-range", B, EN, "    return shlan_port_enable(sw, (uint8_t)(port_id % 48u));"),
 ("r-enable-accepts-oor", B, EN, "    if (port_id >= 48u) {\n        return 0;\n    }\n    return shlan_port_enable(sw, port_id);"),
 ("r-enable-rc-lie", B, EN, "    (void)shlan_port_enable(sw, port_id);\n    return -1;"),
 ("r-connect-rc-lie", B, CO, "    (void)shlan_connect(sw);\n    return 1;"),
 ("r-connect-enables-last", B, CO, "    int rc = shlan_connect(sw);\n    (void)shlan_port_enable(sw, 47u);\n    return rc;"),
 ("r-disconnect-disables-all", B, DC, "    shlan_disconnect(sw);\n    for (uint8_t i = 0; i < 48u; i++) {\n        (void)shlan_port_disable(sw, i);\n    }"),
 ("r-env-connect-to-disconnect", E, 'getattr(lib, f"shlan_test_{name}")', 'getattr(lib, "shlan_test_" + {"connect": "disconnect"}.get(name, name))'),
 ("r-env-enable-to-disable", E, 'getattr(lib, f"shlan_test_{name}")', 'getattr(lib, "shlan_test_" + name.replace("enable", "disable"))'),
 # Declared limits: expected to survive.
 ("lim-disconnect-noop", B, DC, "    (void)sw;"),
 ("lim-disable-reconnects", B, DI, "    (void)port_id;\n    return shlan_connect(sw);"),
 ("lim-disable-all", B, DI, "    for (uint8_t i = 0; i < 48u; i++) {\n        (void)shlan_port_disable(sw, i);\n    }\n    return port_id < 48u ? 0 : -1;"),
 # Adapter layout probes.
 ("lay-field-after", A, "    int port_state[SIM_MAX_PORTS]; /* 1 = enabled, 0 = disabled */\n};", "    int port_state[SIM_MAX_PORTS]; /* 1 = enabled, 0 = disabled */\n    int connected;\n};"),
 ("lay-field-before", A, "struct sim_priv {\n", "struct sim_priv {\n    long generation;\n"),
 ("lay-narrow-type", A, "    int port_state[SIM_MAX_PORTS];", "    unsigned char port_state[SIM_MAX_PORTS];"),
 ("lay-count-64", A, "#define SIM_MAX_PORTS 48", "#define SIM_MAX_PORTS 64"),
 ("lay-count-paren", A, "#define SIM_MAX_PORTS 48", "#define SIM_MAX_PORTS (48)"),
 ("unmodified", None, None, None),
]
def spec(rows):
    return [dict(label=l, file=f, old=o, new=n) for l, f, o, n in rows]
(out / "spec-head.json").write_text(json.dumps(spec(author + mine), indent=1))
(out / "spec-base.json").write_text(json.dumps(spec(author + mine[:2] + [mine[-1]]), indent=1))
