#!/usr/bin/env python3
"""Probe-copy only: make the host mailbox model log every SRP-channel TX record.

Usage: python3 -I r597_dump_hook.py <probe checkout>
Each process appends to $R597_DUMP/<pid>.txt; the first line names the executable
(argv[0] from /proc/self/cmdline), then 'R' at each model reset and 'T <if> <ms> <hex>' per frame.
"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / "sw/firmware/ctrl/host/mbx_model.c"
s = p.read_text()
hook = r'''
#include <stdio.h>
#include <stdlib.h>
static FILE *r597_file(void)
{
	static FILE *fp;
	static int once;
	if (!once) {
		const char *dir = getenv("R597_DUMP");
		once = 1;
		if (dir) {
			char exe[4096] = {0}, pid[32] = {0}, name[4400];
			FILE *f = fopen("/proc/self/cmdline", "rb");
			if (f) { size_t n = fread(exe, 1, sizeof exe - 1, f); exe[n] = 0; fclose(f); }
			f = fopen("/proc/self/stat", "r");
			if (!f || fscanf(f, "%31s", pid) != 1) { pid[0] = 'x'; }
			if (f) fclose(f);
			snprintf(name, sizeof name, "%s/%s.txt", dir, pid);
			fp = fopen(name, "w");
			if (fp) { fprintf(fp, "E %s\n", exe); fflush(fp); }
		}
	}
	return fp;
}
'''
anchor = '#include "mbx_wire.h"\n'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + hook)
old = "\tm->tx_sent++;\n}\n"
assert s.count(old) == 1
new = ("\tif (c == MBX_CH_SRP && r597_file()) {\n"
       "\t\tfprintf(r597_file(), \"T %u %u \", f->interface, (unsigned)f->now_ms);\n"
       "\t\tfor (uint32_t k = 0; k < f->len; ++k) fprintf(r597_file(), \"%02x\", f->bytes[k]);\n"
       "\t\tfputc('\\n', r597_file()); fflush(r597_file());\n\t}\n" + old)
s = s.replace(old, new)
old = "void mbx_model_reset(struct mbx_model *m)\n{\n"
assert s.count(old) == 1
s = s.replace(old, old + "\tif (r597_file()) { fputs(\"R\\n\", r597_file()); fflush(r597_file()); }\n")
p.write_text(s)
print("hooked", p)
