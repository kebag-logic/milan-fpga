#!/usr/bin/env python3
"""Write the round-4 gate-1b probe set as JSON (see patch_probe_hook.py)."""
import json, sys
V = "static int aem_loaded;\n"
O = "static void nvm_boot(void)\n{\n"
def pre(decl, stmt):
    return ["sub", [[V, decl + V], [O, O + stmt]]]
def nvm(macro, stmt):
    return ["nvm", macro, stmt]
N = "static int milan_nbr;\n"
probes = [
 # the stated limit's two examples (R412-3 shapes, rebuilt from the limit's words)
 ["pre_overrun_sscanf", *pre("static char milan_pre[4];\n",
   '\t(void)sscanf("AAAAAAA", "%s", milan_pre);\n')],
 ["nbr_runtime_sscanf", *nvm(N,
   '\t(void)sscanf("\\001", "%c", (char *)&milan_nbr - (int)(milan_read(MILAN_ID) & 7u));\n')],
 # F2: every interior byte folded into the relocation, and the two outside neighbours
 ["nbr_fold_byte1", *nvm(N, '\t(void)sscanf("\\001", "%c", (char *)(&milan_nbr - 1) + 1);\n')],
 ["nbr_fold_byte2", *nvm(N, '\t(void)sscanf("\\001", "%c", (char *)(&milan_nbr - 1) + 2);\n')],
 ["nbr_fold_byte3", *nvm(N, '\t(void)sscanf("\\001", "%c", (char *)(&milan_nbr - 1) + 3);\n')],
 ["nbr_fold_byte0", *nvm(N, '\t(void)sscanf("\\001", "%c", (char *)(&milan_nbr - 1));\n')],
 ["nbr_fold_own", *nvm(N, '\t(void)sscanf("\\001", "%c", (char *)&milan_nbr);\n')],
 ["pre_fold_byte2", *pre("static int milan_pre_i;\n",
   '\t(void)sscanf("\\001", "%c", (char *)(&milan_pre_i + 1) + 2);\n')],
 # the unit's own stores through a neighbour's address (limit's third sentence)
 ["own_store_fold", *nvm(N, '\t(&milan_nbr)[-1] = 1;\n')],
 ["own_store_localptr", *nvm(N, '\t{ int *p = &milan_nbr; p[-1] = 1; }\n')],
 ["own_store_pre_array_local", *pre("static char milan_pre[4];\n",
   '\t{ char *p = milan_pre; p[4] = 1; }\n')],
 ["own_store_runtime", *nvm(N,
   '\t(&milan_nbr)[-(int)(milan_read(MILAN_ID) & 1u)] = 1;\n')],
 ["own_store_bounded_loop", *pre("static char milan_pre[4];\n",
   '\t{ unsigned int i; for (i = 0; i < 8u; i++) milan_pre[i] = 0; }\n')],
 # addresses with no relocation that are neither a literal nor another object's
 ["csr_pointer_sscanf", *nvm("",
   '\t(void)sscanf("\\001", "%c", (char *)(uintptr_t)milan_read(MILAN_ID));\n')],
 ["parsed_pointer_sscanf", *nvm("",
   '\t{ char *q = (char *)strtoul("0x40000000", 0, 0); (void)sscanf("\\001", "%c", q); }\n')],
 ["literal_sscanf", *nvm("",
   '\t(void)sscanf("\\001", "%c", (char *)0x40001000u);\n')],
 # unplanted
 ["stack_runtime_sscanf", *nvm("",
   '\t{ char loc[4]; (void)sscanf("\\001", "%c", loc + (int)milan_read(MILAN_ID)); }\n')],
 ["unplanted", *nvm("", "\t;\n")],
]
json.dump(probes, open(sys.argv[1], "w"), indent=1)
print(len(probes), "probes")
