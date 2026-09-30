#!/usr/bin/env python3
"""The round-3 probe shapes exactly as the published R412-3 report describes
them (pre_overrun_sscanf, nbr_runtime_sscanf, nbr_byte_sscanf), as JSON for
patch_probe_hook.py."""
import json, sys
V = "static int aem_loaded;\n"
O = "static void nvm_boot(void)\n{\n"
probes = [
 ["r3_pre_overrun_sscanf", "sub", [[V, "static char r412_line[4];\n" + V],
   [O, O + '\t(void)sscanf("abcd\\001", "%s", r412_line);\n']]],
 ["r3_nbr_runtime_sscanf", "sub", [[V, V + "static int r412_pad;\n"],
   [O, O + '\t{ volatile int k = -1; (void)sscanf("\\001", "%c", (char *)(&r412_pad + k)); }\n']]],
 ["r3_nbr_byte_sscanf", "sub", [[V, V + "static int r412_pad;\n"],
   [O, O + '\t(void)sscanf("\\001", "%c", (char *)&r412_pad - 3);\n']]],
]
json.dump(probes, open(sys.argv[1], "w"), indent=1)
print(len(probes), "probes")
