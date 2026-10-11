#!/usr/bin/env python3
"""instrument_model.py MBX_MODEL_C: add the SRP TX dump hook to the host mailbox model.

Each SRP-channel frame becomes one line "F <interface> <now_ms> <len> <hex>" and
each mbx_model_reset() one line "R", appended to $R596_DUMP/<argv0 with '/' -> '_'>.txt.
Standard C only (the host model builds with -std=c11 -pedantic -Werror).
"""
import sys
from pathlib import Path

HOOK = r'''
#include <stdio.h>
#include <stdlib.h>
static FILE *r596_dump(void)
{
	static FILE *out;
	if (!out) {
		const char *dir = getenv("R596_DUMP");
		char argv0[512] = {0}, name[1200];
		if (!dir) {
			return NULL;
		}
		FILE *cmd = fopen("/proc/self/cmdline", "rb");
		if (cmd) {
			size_t n = fread(argv0, 1, sizeof argv0 - 1u, cmd);
			argv0[n] = 0;
			fclose(cmd);
		}
		for (char *c = argv0; *c; ++c) {
			if (*c == '/') {
				*c = '_';
			}
		}
		snprintf(name, sizeof name, "%s/%s.txt", dir, argv0);
		out = fopen(name, "a");
	}
	return out;
}
'''

CAPTURE_END = "\tm->tx_sent++;\n}\n\nstatic void tx_drain"
CAPTURE_NEW = ('\tif (c == MBX_CH_SRP && r596_dump()) {\n'
               '\t\tfprintf(r596_dump(), "F %u %lu %u ", (unsigned)f->interface, (unsigned long)f->now_ms, (unsigned)f->len);\n'
               '\t\tfor (uint32_t k = 0; k < f->len; ++k) {\n'
               '\t\t\tfprintf(r596_dump(), "%02x", (unsigned)f->bytes[k]);\n'
               '\t\t}\n'
               '\t\tfputc(\'\\n\', r596_dump());\n'
               '\t\tfflush(r596_dump());\n'
               '\t}\n'
               "\tm->tx_sent++;\n}\n\nstatic void tx_drain")
RESET_OLD = "void mbx_model_reset(struct mbx_model *m)\n{\n"
RESET_NEW = RESET_OLD + '\tif (r596_dump()) {\n\t\tfputs("R\\n", r596_dump());\n\t\tfflush(r596_dump());\n\t}\n'
ANCHOR = "// ---- the TX merge"


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text()
    for old in (CAPTURE_END, RESET_OLD, ANCHOR):
        if text.count(old) != 1:
            sys.exit(f"instrument_model: anchor not unique: {old!r}")
    text = text.replace(ANCHOR, HOOK + "\n" + ANCHOR)
    text = text.replace(CAPTURE_END, CAPTURE_NEW).replace(RESET_OLD, RESET_NEW)
    path.write_text(text)
    print(f"instrument_model: {path}: hooked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
