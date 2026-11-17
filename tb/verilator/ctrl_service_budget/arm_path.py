# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The answering-ports arm's GET_AS_PATH port (#897): build.py puts it in the face's `path` port, as the arm puts its
other observation ports there, so the aecp group's GET_AS_PATH row times the record of a GET_AS_PATH the product
answers (the product's ports answer, as this arm's do).

It reads what aecp_face.c's `path` reads, through the AVB interface's own GSI window, kind 2: the count at selector 0,
then each entry at selector 8 by its ordinal, at most ENTRIES of them, the shipped datapath's most (KL_gptp_engine.sv
clamps the pathTrace count to 8), and it answers ENTRIES entries. The test SoC never answers a window, so each read
runs to the contract's whole bound (MBX_WIN_GSI_WAIT_CYCLES), the slowest answer the contract allows; only an
answer's two data words, which a read with no answer does not fetch, are not read.
"""

#: The entries the port answers: the shipped datapath's most.
ENTRIES = 8
#: The fixture's includes the port needs: the window read and the contract's field placement.
INCLUDES = '#include "mbx.h"\n#include "mbx_wire.h"\n'
#: The port, C source for the fixture's scratch copy.
B_PATH = (
    'static bool b_path(void *ctx, unsigned i, uint16_t n, uint64_t *v, size_t cap, size_t *count)\n'
    '{\n'
    '    (void)ctx;\n'
    '    uint32_t q[4] = {mbx_place(9u, MBX_GSI_REQ_TYPE_LSB, MBX_GSI_REQ_TYPE_WIDTH) |\n'
    '                     mbx_place(n, MBX_GSI_REQ_INDEX_LSB, MBX_GSI_REQ_INDEX_WIDTH),\n'
    '                     mbx_place(2u, MBX_GSI_SEL_KIND_LSB, MBX_GSI_SEL_KIND_WIDTH), 0u, 0u};\n'
    '    uint64_t w = 0;\n'
    '    (void)mbx_win_read(i, MBX_WIN_GSI, q, &w);\n'
    f'    size_t k = cap < {ENTRIES}u ? cap : {ENTRIES}u;\n'
    '    for (size_t e = 0; e < k; ++e) {\n'
    '        q[1] = mbx_place(2u, MBX_GSI_SEL_KIND_LSB, MBX_GSI_SEL_KIND_WIDTH) |\n'
    '               mbx_place(8u, MBX_GSI_SEL_SEL_LSB, MBX_GSI_SEL_SEL_WIDTH) |\n'
    '               mbx_place((uint32_t)e, MBX_GSI_SEL_ORD_LSB, MBX_GSI_SEL_ORD_WIDTH);\n'
    '        (void)mbx_win_read(i, MBX_WIN_GSI, q, &w);\n'
    '        v[e] = 0x001bc5fffe000000ull | ((uint64_t)i << 16) | e;\n'
    '    }\n'
    '    *count = k;\n'
    '    return true;\n'
    '}\n')
