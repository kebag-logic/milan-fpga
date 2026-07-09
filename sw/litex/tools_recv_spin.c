#define _GNU_SOURCE
/* Busy-polling TCP receiver: real recv() copies (or MSG_TRUNC), no sleep-wake in the
 * drain loop, optional SO_RCVBUF cap (bounded residency for warm-copy tests).
 * usage: recv_spin ip port [cport] [secs] [rcvbuf] [trunc]
 *   rcvbuf 0 = kernel default/autotune; else setsockopt(SO_RCVBUF, rcvbuf) pre-connect.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#define _GNU_SOURCE2
#include <sched.h>
int main(int c, char **v)
{
	if (c < 3) { fprintf(stderr, "usage: %s ip port [cport] [secs] [rcvbuf] [trunc] [cpu] [rdsz]\n", v[0]); return 1; }
	if (c > 7 && atoi(v[7]) >= 0) {
		cpu_set_t s; CPU_ZERO(&s); CPU_SET(atoi(v[7]), &s);
		sched_setaffinity(0, sizeof(s), &s);
	}
	int fd = socket(AF_INET, SOCK_STREAM, 0);
	if (c > 3 && atoi(v[3])) {
		struct sockaddr_in l = {0}; l.sin_family = AF_INET; l.sin_port = htons(atoi(v[3]));
		int o = 1; setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &o, sizeof o);
		bind(fd, (void *)&l, sizeof l);
	}
	int rb = c > 5 ? atoi(v[5]) : 0;
	if (rb > 0) setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &rb, sizeof rb);
	int trunc = (c > 6 && atoi(v[6])) ? MSG_TRUNC : 0;
	struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(atoi(v[2]));
	inet_pton(AF_INET, v[1], &a.sin_addr);
	if (connect(fd, (void *)&a, sizeof a)) { perror("connect"); return 1; }
	double secs = c > 4 ? atof(v[4]) : 8.0;
	static char buf[262144];
	size_t rdsz = sizeof buf;
	if (c > 8 && atoi(v[8]) > 0 && (size_t)atoi(v[8]) <= sizeof buf)
		rdsz = atoi(v[8]);
	long tot = 0, spins = 0, reads = 0;
	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);
	for (;;) {
		ssize_t n = recv(fd, buf, rdsz, MSG_DONTWAIT | trunc);
		if (n > 0) { tot += n; reads++; }
		else if (n < 0 && errno == EAGAIN) { if ((++spins & 1023) != 0) continue; }
		else break;
		clock_gettime(CLOCK_MONOTONIC, &t1);
		double dt = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
		if (dt >= secs) {
			int ab = 0; socklen_t sl = sizeof ab;
			getsockopt(fd, SOL_SOCKET, SO_RCVBUF, &ab, &sl);
			printf("SPIN%s RX: %.1f Mbit/s (%ld MB / %.2fs) reads=%ld avg=%ldB rcvbuf=%d\n",
			       trunc ? "-TRUNC" : "", tot * 8.0 / dt / 1e6, tot >> 20, dt,
			       reads, reads ? tot / reads : 0, ab);
			break;
		}
	}
	return 0;
}
