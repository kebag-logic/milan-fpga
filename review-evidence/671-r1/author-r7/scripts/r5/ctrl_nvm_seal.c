/* The ctrl_nvm store's boot (nvm_store.c, unchanged) on its host flash
 * model, with the first COUNT whole-container reads of slot A answered with
 * byte AT XORed by 1, 2, ... and the CRC-32 trailer closed over the faulty
 * bytes: distinct refused containers whose CRC passes. Then a console commit
 * and a clean reboot. Prints each boot's status.
 * Usage: ctrl_nvm_seal SLOT_A_FILE AT COUNT */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "nvm_fmodel.h"
#include "nvm_klj2.h"
#include "nvm_smodel.h"
#include "nvm_store.h"

static unsigned int faulty;
static unsigned int at;
static unsigned int k;

static int seal_read(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len)
{
	int r = nvm_fmodel_read(ctx, addr, dst, len);
	uint32_t crc;
	unsigned int i;

	if (r == 0 && addr == NVM_SLOT_A && len > NVM_KLJ2_HDR && at < len - 4u && faulty) {
		faulty--;
		dst[at] ^= (uint8_t)++k;
		crc = ~nvm_crc32_update(0xffffffffu, dst, len - NVM_KLJ2_TRAILER);
		for (i = 0; i < 4u; ++i)
			dst[len - 4u + i] = (uint8_t)(crc >> (8u * i));
		printf("PROBE sealed container read %u of slot A: byte %u ^ %u, %u B\n", k, at, k, len);
	}
	return r;
}

static void show(const char *what)
{
	const struct nvm_status *s = nvm_store_status();

	printf("%s: verdict_a=%d seq_a=%u verdict_b=%d seq_b=%u auth=%d seq=%u unread=%u read_faults=%u "
	       "phase=%d commits_ok=%u\n", what, (int)s->verdict_a, (unsigned int)s->seq_a, (int)s->verdict_b,
	       (unsigned int)s->seq_b, s->auth, (unsigned int)s->seq, s->unread, s->read_faults,
	       (int)s->phase, s->commits_ok);
}

int main(int argc, char **argv)
{
	struct nvm_flash port = nvm_fmodel_port;
	FILE *f;
	size_t n;
	unsigned int i;

	if (argc != 4)
		return 2;
	nvm_fmodel_power_on();
	nvm_fmodel_blank();
	f = fopen(argv[1], "rb");
	if (!f)
		return 2;
	n = fread(nvm_fmodel_mem + NVM_SLOT_A, 1, NVM_SLOT_BYTES, f);
	fclose(f);
	printf("PROBE slot A %zu B, slot B blank\n", n);
	at = (unsigned int)strtoul(argv[2], NULL, 0);
	faulty = (unsigned int)strtoul(argv[3], NULL, 0);
	port.read = seal_read;
	nvm_smodel_reset();
	nvm_smodel_ready(1);
	nvm_store_boot(&port, &nvm_smodel_port);
	show("faulty boot");
	if (nvm_store_status()->phase == NVM_P_HELD) {
		printf("PROBE the store held; nothing persists\n");
		return 0;
	}
	if (!nvm_store_commit_now())
		printf("PROBE the console commit was refused\n");
	for (i = 0; i < 200000u && nvm_store_status()->phase != NVM_P_IDLE; ++i) {
		nvm_store_service();
		nvm_fmodel_advance_us(100);
	}
	show("after commit");
	nvm_smodel_reset();
	nvm_smodel_ready(1);
	nvm_store_boot(&nvm_fmodel_port, &nvm_smodel_port);
	show("clean reboot");
	return 0;
}
