"""txcommit.py TREE: attempt 2's mailbox cut in TREE's mbx.c: mbx_tx_begin ends the record before its own through the
commit's body inline, so the transmit of a notice's recipient calls nothing and saves no registers. Scratch writer."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl/mbx/mbx.c'; t = p.read_text()
old_head = "bool mbx_tx_commit(unsigned ch)\n{\n\tstruct tx_ring *t = &tx[ch];"
new_head = ("// A record's commit: its payload's move judged, then its head advanced (mbx_tx_commit). Mbx_tx_begin ends the\n"
            "// record before its own through it inline, so a transmit calls nothing and saves no registers for a call (#665:\n"
            "// a notice's recipients each paid for both).\n"
            "static inline bool tx_commit(unsigned ch)\n{\n\tstruct tx_ring *t = &tx[ch];")
assert t.count(old_head) == 1
t = t.replace(old_head, new_head)
end_marker = "\tmbx_bus_write32(ch_reg(ch, MBX_CH_REG_TX_HEAD), t->head);\n\treturn true;\n}\n"
assert t.count(end_marker) == 1
t = t.replace(end_marker, end_marker + "\nbool mbx_tx_commit(unsigned ch)\n{\n\treturn tx_commit(ch);\n}\n")
old_call = "\tif (!mbx_tx_commit(ch)) {\n\t\treturn MBX_STATUS_LOST;\n\t}\n"
assert t.count(old_call) == 1
t = t.replace(old_call, "\tif (!tx_commit(ch)) {\n\t\treturn MBX_STATUS_LOST;\n\t}\n")
p.write_text(t)
print('tx_commit inline')
