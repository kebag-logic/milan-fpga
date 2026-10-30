// Reviewer probe: a received line carrying a NUL byte where a command's name ends ("milan_status\0..."),
// through ctrl_plat_console_poll on a host UART, under AddressSanitizer.
#include <stdint.h>
#include <stdio.h>
#include "ctrl_plat_console.h"
#include "ctrl_plat_io.h"
#define UART 0xf0001800u
static const uint8_t line[] = {'m','i','l','a','n','_','s','t','a','t','u','s',0,'X','Y','Z','\r'};
static unsigned at;
uint32_t ctrl_plat_io_read32(uintptr_t a)
{
	if (a == UART + 0x8u) return at >= sizeof line;
	if (a == UART + 0x0u) return line[at];
	return 0u;
}
void ctrl_plat_io_write32(uintptr_t a, uint32_t v)
{
	if (a == UART + 0x10u) { ++at; return; }
	if (a == UART + 0x0u) putchar((int)v);
}
int main(void)
{
	struct ctrl_plat_uart u = {UART, UART + 0x4u, UART + 0x8u, UART + 0x10u};
	static struct ctrl_plat_console c;
	ctrl_plat_console_init(&c, &u, 0x90000000u);
	for (unsigned pass = 0; pass < 50; ++pass) (void)ctrl_plat_console_poll(&c);
	fprintf(stderr, "\ncommands %u refused %u\n", c.commands, c.refused);
	return 0;
}
