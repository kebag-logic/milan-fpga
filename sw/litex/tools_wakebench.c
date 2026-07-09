/* wakebench — cross-hart wakeup latency via pipe ping-pong.
 * usage: wakebench <cpuA> <cpuB> [iters]   (RTT/2 ~ one wake+schedule)
 * Build: $CROSS-gcc -O2 -static -o wakebench tools_wakebench.c
 */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static void pin(int cpu)
{
	cpu_set_t s;
	CPU_ZERO(&s);
	CPU_SET(cpu, &s);
	if (sched_setaffinity(0, sizeof(s), &s))
		perror("setaffinity");
}

static long long now_ns(void)
{
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);
	return ts.tv_sec * 1000000000LL + ts.tv_nsec;
}

static int cmp(const void *a, const void *b)
{
	long long x = *(const long long *)a, y = *(const long long *)b;
	return x < y ? -1 : x > y;
}

int main(int argc, char **argv)
{
	int cpua = argc > 1 ? atoi(argv[1]) : 0;
	int cpub = argc > 2 ? atoi(argv[2]) : 1;
	int iters = argc > 3 ? atoi(argv[3]) : 400;
	int p2c[2], c2p[2];
	char b = 0;
	long long *rtt = calloc(iters, sizeof(*rtt));

	if (pipe(p2c) || pipe(c2p))
		return 1;
	if (fork() == 0) {
		pin(cpub);
		while (read(p2c[0], &b, 1) == 1)
			if (write(c2p[1], &b, 1) != 1)
				break;
		_exit(0);
	}
	pin(cpua);
	usleep(50000);
	for (int i = 0; i < iters; i++) {
		long long t0 = now_ns();
		if (write(p2c[1], &b, 1) != 1 || read(c2p[0], &b, 1) != 1)
			return 1;
		rtt[i] = now_ns() - t0;
		usleep(3000); /* let both sides go idle between samples */
	}
	qsort(rtt, iters, sizeof(*rtt), cmp);
	printf("wake %d->%d rtt us: min=%.1f p50=%.1f p90=%.1f p99=%.1f max=%.1f\n",
	       cpua, cpub, rtt[0] / 1e3, rtt[iters / 2] / 1e3,
	       rtt[iters * 9 / 10] / 1e3, rtt[iters * 99 / 100] / 1e3,
	       rtt[iters - 1] / 1e3);
	close(p2c[1]);
	return 0;
}
