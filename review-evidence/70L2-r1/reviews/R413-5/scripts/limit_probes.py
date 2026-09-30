#!/usr/bin/env python3
"""Plant one callee-class probe into the SHIPPING firmware of a tree COPY,
at the opening of nvm_boot()'s body (the same site gate 1b's breaks use).
Each writes the verdict's bytes, if at all, through a pointer carrying no
relocation on them; the stated limit says gate 1b does not see it, so the
expected outcome is that the gate PASSES with aem_loaded's slot kept.

usage: limit_probes.py <tree> <probe>
  L1_csr_pointer      sscanf() handed a CSR read cast to a pointer
  L2_frame_runtime    sscanf() handed a frame local's address plus a CSR read
  L3_callee_return    sscanf() handed a C-library callee's returned pointer
  L4_literal          sscanf() handed a literal address
  L5_before_overrun   sscanf("%s") overrunning a 4-byte static declared
                      just before the verdict
  L6_nbr_runtime      sscanf() handed &neighbour + k, k a CSR read
  L7_unit_literal     this unit stores through a literal address
  L8_unit_csr_pointer this unit stores through a CSR read cast to a pointer
  L9_unit_frame_rt    this unit stores to a frame buffer at a CSR-read index
  L10_unit_callee_ret this unit stores through a callee's returned pointer
  L11_unit_stack_far  this unit stores to a frame buffer at a constant index
                      far outside it (placed on the stack), expected accepted
  I2_interior_b2      gate 1b's +2 break shape planted in the shipping firmware
  I3_interior_b3      gate 1b's +3 break shape planted in the shipping firmware
The interior probes I2/I3 are expected REFUSED naming the escape pin only.
The unit-store probes L8-L10 are expected REFUSED by rule 1b, as a store the
census cannot place (BAREMETAL_FIRMWARE.md); L7 is expected accepted, a store
placed at a number.
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
text = path.read_text()
OPEN = "static void nvm_boot(void)\n{\n"
DECL = "static int aem_loaded;\n"
CSR = "milan_read(MILAN_PP_STAT)"
probes = {
    "L1_csr_pointer": ("", f"\t(void)sscanf(\"\\001\", \"%c\", "
                           f"(char *)(uintptr_t){CSR});\n"),
    "L2_frame_runtime": ("", "\t{\n\t\tchar probe_buf[4];\n\n"
                             f"\t\t(void)sscanf(\"\\001\", \"%c\", "
                             f"probe_buf + {CSR});\n\t}}\n"),
    "L3_callee_return": ("", "\t(void)sscanf(\"\\001\", \"%c\", "
                             "(char *)strtoul(\"0\", NULL, 0));\n"),
    "L4_literal": ("", "\t(void)sscanf(\"\\001\", \"%c\", "
                       "(char *)0x40001234u);\n"),
    "L5_before_overrun": ("static char milan_probe_before[4];\n",
                          "\t(void)sscanf(\"abcdefg\", \"%s\", "
                          "milan_probe_before);\n"),
    "L6_nbr_runtime": ("static int milan_probe_nbr;\n",
                       "\t(void)sscanf(\"\\001\", \"%c\", "
                       f"(char *)(&milan_probe_nbr + {CSR}));\n"),
    "L7_unit_literal": ("", "\t*(volatile int *)0x40001234u = 0;\n"),
    "L8_unit_csr_pointer": ("", f"\t*(volatile char *)(uintptr_t){CSR} = 0;\n"),
    "L9_unit_frame_rt": ("", "\t{\n\t\tvolatile char probe_buf[4];\n\n"
                             f"\t\tprobe_buf[{CSR}] = 0;\n\t}}\n"),
    "L10_unit_callee_ret": ("", "\t*(volatile char *)strtoul(\"0\", NULL, 0)"
                                " = 0;\n"),
    "L11_unit_stack_far": ("", "\t{\n\t\tvolatile char probe_buf[4];\n\n"
                               "\t\tprobe_buf[-4096] = 0;\n\t}\n"),
    **{f"I{k}_interior_b{k}": ("static int milan_verdict_next;\n",
                               "\t(void)sscanf(\"\\001\", \"%c\", "
                               f"(char *)(&milan_verdict_next - 1) + {k});\n")
       for k in (2, 3)},
}
before, statement = probes[kind]
if kind.startswith("I"):  # after the verdict, as gate 1b's in_nvm_boot() does
    assert text.count(DECL) == 1
    text = text.replace(DECL, DECL + before, 1)
    before = ""
assert text.count(OPEN) == 1 and text.count(DECL) == 1
if before:
    text = text.replace(DECL, before + DECL, 1)
text = text.replace(OPEN, OPEN + statement, 1)
# milan_read() is defined before nvm_boot(); nothing moves.
path.write_text(text)
print(f"planted {kind} in {path}")
