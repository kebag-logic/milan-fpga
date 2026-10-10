"""Scratch only: make the host mailbox model append every SRP-channel TX record to a per-arm file.

Usage: python3 apply_dump.py CHECKOUT. The file is $SRP_TX_DUMP/<arm directory>.txt, where the arm
directory is the parent directory of the running executable. RESET lines delimit model resets (tests).
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / 'sw/firmware/ctrl/host/mbx_model.c'
text = path.read_text()
hook = r'''
#include <stdio.h>
#include <stdlib.h>
static FILE *srp_dump_file(void)
{
	static FILE *file;
	static int tried;
	if (!tried) {
		char exe[4096] = {0}, name[4352];
		const char *dir = getenv("SRP_TX_DUMP");
		FILE *cmd = fopen("/proc/self/cmdline", "rb");
		tried = 1;
		if (dir && cmd) {
			char *slash, *arm;
			size_t n = fread(exe, 1, sizeof exe - 1, cmd);
			exe[n] = 0;
			slash = strrchr(exe, '/');
			if (slash) { *slash = 0; }
			arm = strrchr(exe, '/');
			snprintf(name, sizeof name, "%s/%s.txt", dir, arm ? arm + 1 : exe);
			file = fopen(name, "a");
		}
		if (cmd) { fclose(cmd); }
	}
	return file;
}
'''
anchor = '#include "mbx_wire.h"\n'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + hook)
old = '\tm->tx_sent++;\n}\n'
assert text.count(old) == 1
new = ('\tif (c == MBX_CH_SRP && srp_dump_file()) {\n'
       '\t\tfprintf(srp_dump_file(), "TX if=%u ms=%u len=%u hex=", f->interface, (unsigned)f->now_ms, f->len);\n'
       '\t\tfor (uint32_t k = 0; k < f->len; ++k) fprintf(srp_dump_file(), "%02x", f->bytes[k]);\n'
       '\t\tfputc(10, srp_dump_file());\n\t\tfflush(srp_dump_file());\n\t}\n' + old)
text = text.replace(old, new)
old = 'void mbx_model_reset(struct mbx_model *m)\n{\n'
assert text.count(old) == 1
text = text.replace(old, old + '\tif (srp_dump_file()) { fputs("RESET\\n", srp_dump_file()); fflush(srp_dump_file()); }\n')
path.write_text(text)
print('instrumented', path)
