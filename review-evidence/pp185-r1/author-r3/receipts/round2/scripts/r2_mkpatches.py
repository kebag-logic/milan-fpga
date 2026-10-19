"""Round 2: write the dispatch-campaign patches the IDENTIFY test adds or moves,
from exact edits on a tree (each edit must match once)."""
import difflib, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = root / "tb/pp_top/aecp_dispatch_mutations"
U = "hdl/aecp/ucode/gen_ucode.py"
PRO = """    u('DESC_ADDR', ra=14, imm=RGN_LOCATE),       # requested CONTROL[index]
    u('BR_STATUS', cnd=0, imm=E_RDSTUB),
    u('READ_ST', rd=8, imm=RGN_LEN),
    u('COMPARE', ra=8, fmt=FMT_W, imm=CT_CUR_TAIL),
"""
PRO_UNSET = """    u('DESC_ADDR', ra=14, imm=RGN_LOCATE),       # requested CONTROL[index]
    u('BR_STATUS', cnd=0, imm=E_RDSTUB),
    u('READ_ST', rd=3, imm=RGN_DYNV + SEL_IDENT),
    u('COMPARE', ra=3, fmt=FMT_D, imm=0),
    u('BR_STATUS', cnd=2, imm=E_RDESC),
    u('READ_ST', rd=8, imm=RGN_LEN),
    u('COMPARE', ra=8, fmt=FMT_W, imm=CT_CUR_TAIL),
"""
VT_BR = "    u('BR_STATUS', cnd=3, imm=E_RDESCID),        # one octet, linear\n"
CHK = "    u('CHECK_ARG', ra=6, rb=9, fmt=FMT_W, cnd=REL_EQ, imm=E_RDESCID + 12),\n"
def nop(line):
    return "    u('NOP'),  # planted: " + line.strip().split("#")[0].strip() + "\n"
W82 = "    u('SHIFT_R', rd=6, ra=5, imm=32),            # [15:0] = @82..@83\n" + CHK
W84 = "    u('SHIFT_R', rd=6, ra=5, imm=16),            # [15:0] = @84..@85\n" + CHK
W86 = "    u('CHECK_ARG', ra=5, rb=12, fmt=FMT_W, cnd=REL_EQ, imm=E_RDESCID + 12),  # @86..@87\n"
W88 = "    u('SHIFT_R', rd=6, ra=4, imm=48),            # [15:0] = @88..@89\n" + CHK
OKST = "    u('SET_STATUS', imm=ST_OK),                  # E_RDESCID + 12: another\n"
ARMS = {
    "rdc-unset-image": [
        (U, PRO, PRO_UNSET),
        (U, "    u('BR_STATUS', cnd=2, imm=E_RDESCCT + 12),\n",
            "    u('BR_STATUS', cnd=2, imm=E_RDESCCT + 15),\n"),
        (U, "    u('BRANCH', imm=E_RDESCCT + 17),             # the IDENTIFY: overlaid\n",
            "    u('BRANCH', imm=E_RDESCCT + 20),             # the IDENTIFY: overlaid\n"),
        (U, "assert rom[E_RDESCCT + 12] ==", "assert rom[E_RDESCCT + 15] =="),
        (U, "assert rom[E_RDESCCT + 17] ==", "assert rom[E_RDESCCT + 20] =="),
    ],
    "rdc-vtype-uint8-only": [
        (U, "    u('COMPARE', ra=5, fmt=FMT_W, imm=CT_LINEAR_INT16),\n" + VT_BR,
            "    u('COMPARE', ra=5, fmt=FMT_W, imm=0x0001),\n"
            "    u('BR_STATUS', cnd=2, imm=E_RDESCID),        # one octet, linear\n")],
    "rdc-ctype-any": [
        (U, VT_BR, "    u('BR_STATUS', cnd=3, imm=E_RDESCCT + 17),   # one octet, linear\n")],
    "rdc-ctype-w82-nop": [(U, W82, W82.replace(CHK, nop(CHK)))],
    "rdc-ctype-w84-nop": [(U, W84, W84.replace(CHK, nop(CHK)))],
    "rdc-ctype-w86-nop": [(U, W86, nop(W86))],
    "rdc-ctype-w88-nop": [(U, W88, W88.replace(CHK, nop(CHK)))],
    "rdc-ctype-status-kept": [
        (U, OKST, nop(OKST)),
        (U, "assert rom[E_RDESCID + 12] == u('SET_STATUS', imm=ST_OK)\n",
            "assert rom[E_RDESCID + 12] == u('NOP')\n")],
}
for arm, edits in ARMS.items():
    files = {}
    for rel, old, new in edits:
        text = files.get(rel) or (root / rel).read_text(encoding="utf-8")
        assert text.count(old) == 1, (arm, rel, old[:60], text.count(old))
        files[rel] = text.replace(old, new, 1)
    chunks = []
    for rel, new in files.items():
        old = (root / rel).read_text(encoding="utf-8")
        chunks += difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                       "a/" + rel, "b/" + rel, n=3)
    (out / f"{arm}.patch").write_text("".join(chunks), encoding="utf-8")
    print(arm, len("".join(chunks)))
