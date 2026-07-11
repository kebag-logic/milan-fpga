/* AF_PACKET TPACKET_V3 mmap RX ring — the zero-copy consumer lane (AVTP substrate).
 * Taps post-GRO, so TCP arrives as coalesced units (avg size printed = GRO unit).
 * usage: recv_ring <ifname> <secs> [cpu]
 * Counts tp_len (true wire+GRO length); blocks: 8 x 256 KB, 4 ms retire timeout.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <poll.h>
#include <sched.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <linux/if_packet.h>
#include <linux/if_ether.h>
#include <net/if.h>
#include <arpa/inet.h>

#define BLK_SZ  (256 * 1024)
#define BLK_NR  8

int main(int argc, char **argv)
{
	if (argc < 3) { fprintf(stderr, "usage: %s <ifname> <secs> [cpu]\n", argv[0]); return 1; }
	double secs = atof(argv[2]);
	if (argc > 3 && atoi(argv[3]) >= 0) {
		cpu_set_t s; CPU_ZERO(&s); CPU_SET(atoi(argv[3]), &s);
		sched_setaffinity(0, sizeof(s), &s);
	}
	int fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_IP));
	if (fd < 0) { perror("socket"); return 1; }
	int v = TPACKET_V3;
	if (setsockopt(fd, SOL_PACKET, PACKET_VERSION, &v, sizeof v)) { perror("version"); return 1; }
	struct tpacket_req3 req = {
		.tp_block_size = BLK_SZ, .tp_block_nr = BLK_NR,
		.tp_frame_size = 2048, .tp_frame_nr = BLK_SZ / 2048 * BLK_NR,
		.tp_retire_blk_tov = 4,          /* ms */
	};
	if (setsockopt(fd, SOL_PACKET, PACKET_RX_RING, &req, sizeof req)) { perror("ring"); return 1; }
	void *map = mmap(NULL, (size_t)BLK_SZ * BLK_NR, PROT_READ | PROT_WRITE,
			 MAP_SHARED | MAP_LOCKED, fd, 0);
	if (map == MAP_FAILED) { perror("mmap"); return 1; }
	struct sockaddr_ll ll = { .sll_family = AF_PACKET,
				  .sll_protocol = htons(ETH_P_IP),
				  .sll_ifindex = (int)if_nametoindex(argv[1]) };
	if (bind(fd, (void *)&ll, sizeof ll)) { perror("bind"); return 1; }

	struct pollfd pfd = { .fd = fd, .events = POLLIN };
	unsigned blk = 0;
	unsigned long long bytes = 0, pkts = 0, blocks = 0;
	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);
	for (;;) {
		struct tpacket_block_desc *bd =
			(void *)((char *)map + (size_t)blk * BLK_SZ);
		if (!(bd->hdr.bh1.block_status & TP_STATUS_USER)) {
			poll(&pfd, 1, 100);
			clock_gettime(CLOCK_MONOTONIC, &t1);
			if ((t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9 >= secs)
				break;
			continue;
		}
		unsigned n = bd->hdr.bh1.num_pkts;
		struct tpacket3_hdr *h =
			(void *)((char *)bd + bd->hdr.bh1.offset_to_first_pkt);
		for (unsigned k = 0; k < n; k++) {
			bytes += h->tp_len;               /* true (GRO-unit) length */
			pkts++;
			h = (void *)((char *)h + h->tp_next_offset);
		}
		blocks++;
		bd->hdr.bh1.block_status = TP_STATUS_KERNEL;   /* release */
		blk = (blk + 1) % BLK_NR;
		clock_gettime(CLOCK_MONOTONIC, &t1);
		if ((t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9 >= secs)
			break;
	}
	double dt = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
	struct tpacket_stats_v3 st; socklen_t sl = sizeof st;
	getsockopt(fd, SOL_PACKET, PACKET_STATISTICS, &st, &sl);
	printf("RING RX: %.1f Mbit/s (%llu MB / %.2fs) units=%llu avg=%lluB blocks=%llu ringdrops=%u\n",
	       bytes * 8.0 / dt / 1e6, bytes >> 20, dt, pkts,
	       pkts ? bytes / pkts : 0, blocks, st.tp_drops);
	return 0;
}
