#!/usr/bin/env python3
"""Plant one round-4 reviewer probe into a tree copy's shipping firmware.

usage: r413_plants.py <tree> <probe>

Same placement as the prior round's plants: a file-scope line just after
`static int aem_loaded;` (or just before it, for the BEFORE set) and a
statement first in nvm_boot()'s body. The shipping firmware is AEM-first,
so an accepted probe keeps the verdict's slot across nvm_boot().

Probes (each asks one sentence of the round-4 bounded claim):
  own_local_under_store  a local pointer to a static declared after the
      verdict, indexed -1 by a constant: the unit's own store, placed by
      the resolver on the neighbour (limit 2, "nor is a store this unit
      makes ... such as a local pointer to the neighbour indexed outside it")
  own_folded_store       `(&nbr)[-1] = 0;` whose constant the compiler folds
      into the relocation ("an offset the compiler folds ... is refused by
      address")
  own_runtime_store      `(&nbr)[k] = 0;` with k a volatile local ("a store
      through an offset known only at run time is refused by rule 1b")
  own_callee_store       a unit-defined callee writing p[-1] through the
      neighbour's address handed to it (a callee this unit defines is
      resolved on its own)
  data_word_nbr_store    the neighbour's address held in a static data word,
      indexed -1 in the unit
  data_word_nbr_sscanf   the same address handed to sscanf() one int back
  interior_b2_sscanf     the round-4 break shape moved to byte +2
  interior_b3_sscanf     the round-4 break shape moved to byte +3
  interior_b1_store      a one-byte store in the unit at byte +1 through a
      folded neighbour address (store in place on an interior byte)
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
fw = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
text = fw.read_text()
decl = "static int aem_loaded;\n"
opening = "static void nvm_boot(void)\n{\n"
body_first = ("\tuint32_t seq_a;\n\tuint32_t seq_b;\n\tuint32_t chosen;\n"
              "\tuint32_t stat;\n\tunsigned int verdict;\n"
              "\tunsigned int tries = 0;\n\tint loaded = 0;\n"
              "\tint live = 0;\t\t\t/* the window went live */\n\n")
assert text.count(decl) == 1 and text.count(opening + body_first) == 1
NBR = "static int r413_nbr;\n"
PROBES = {
    "own_local_under_store": (NBR, "\t{\n\t\tint *r413_p = &r413_nbr;\n\n"
                                   "\t\tr413_p[-1] = 0;\n\t}\n"),
    "own_folded_store": (NBR, "\t(&r413_nbr)[-1] = 0;\n"),
    "own_runtime_store": (NBR, "\t{\n\t\tvolatile int r413_k = -1;\n\n"
                               "\t\t(&r413_nbr)[r413_k] = 0;\n\t}\n"),
    "own_callee_store": (NBR + "static void r413_clear(int *p)\n{\n"
                               "\tp[-1] = 0;\n}\n",
                         "\tr413_clear(&r413_nbr);\n"),
    "data_word_nbr_store": (NBR + "static int *r413_word = &r413_nbr;\n",
                            "\tr413_word[-1] = 0;\n"),
    "data_word_nbr_sscanf": (NBR + "static int *r413_word = &r413_nbr;\n",
                             "\t(void)sscanf(\"1\", \"%d\", r413_word - 1);\n"),
    "interior_b2_sscanf": (NBR, "\t(void)sscanf(\"\\001\", \"%c\", "
                                "(char *)(&r413_nbr - 1) + 2);\n"),
    "interior_b3_sscanf": (NBR, "\t(void)sscanf(\"\\001\", \"%c\", "
                                "(char *)(&r413_nbr - 1) + 3);\n"),
    "interior_b1_store": (NBR, "\t*((volatile char *)(&r413_nbr - 1) + 1) = 1;\n"),
}
macro, stmt = PROBES[kind]
text = text.replace(decl, decl + macro, 1)
text = text.replace(opening + body_first, opening + body_first + stmt, 1)
fw.write_text(text)
print(f"planted {kind} in {fw}")
