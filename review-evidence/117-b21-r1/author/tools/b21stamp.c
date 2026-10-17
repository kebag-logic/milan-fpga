/* Lane B21: the per-read timing record of lane B5's reader (run_a.py's Reader), for the SoC board,
 * which has no Python. Reads arecord's raw output on stdin with 64 KiB reads, exactly as that reader
 * does: after every read it stamps the frames delivered so far and the board's clocks, as
 * <q frames_after_read, d realtime_s, q monotonic_ns> (the same 24-byte record). Whole frames only;
 * a partial frame waits for the next read.
 *
 * The kept slots go through a RAM ring to a writer thread, so a slow storage write never
 * back-pressures arecord. A full ring drops data and counts it (reported, never silent).
 *
 * usage: b21stamp <channels> <bytes_per_sample> <keep: all|none|i,j,...> <data_out> <ts_out> <ring_MiB>
 * Prints one summary line on stderr at the end of input.
 * Build: aarch64-linux-gnu-gcc -O2 -static -pthread -o b21stamp b21stamp.c
 */
#include <errno.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static unsigned char *ring;
static size_t ring_sz, head, tail; /* head: producer total, tail: consumer total (monotone byte counts) */
static size_t ring_max_fill;
static unsigned long long dropped;
static int done;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cv = PTHREAD_COND_INITIALIZER;
static FILE *dout;

static void *writer(void *arg)
{
	(void)arg;
	for (;;) {
		pthread_mutex_lock(&mu);
		while (head == tail && !done)
			pthread_cond_wait(&cv, &mu);
		size_t h = head, t = tail;
		int d = done;
		pthread_mutex_unlock(&mu);
		if (h == t && d)
			break;
		size_t off = t % ring_sz, n = h - t;
		if (n > ring_sz - off)
			n = ring_sz - off;
		if (fwrite(ring + off, 1, n, dout) != n) {
			fprintf(stderr, "b21stamp: data write failed: %s\n", strerror(errno));
			exit(3);
		}
		pthread_mutex_lock(&mu);
		tail += n;
		pthread_mutex_unlock(&mu);
	}
	return NULL;
}

static void put(const unsigned char *p, size_t n)
{
	pthread_mutex_lock(&mu);
	size_t fill = head - tail;
	if (fill + n > ring_sz) {
		dropped += n;
		pthread_mutex_unlock(&mu);
		return;
	}
	for (size_t i = 0; i < n; i++)
		ring[(head + i) % ring_sz] = p[i];
	head += n;
	if (head - tail > ring_max_fill)
		ring_max_fill = head - tail;
	pthread_cond_signal(&cv);
	pthread_mutex_unlock(&mu);
}

int main(int argc, char **argv)
{
	if (argc != 7) {
		fprintf(stderr, "usage: b21stamp <channels> <bytes_per_sample> <keep> <data_out> <ts_out> <ring_MiB>\n");
		return 2;
	}
	int nch = atoi(argv[1]), bps = atoi(argv[2]);
	int keep[64], nkeep = 0;
	if (!strcmp(argv[3], "all")) {
		for (int c = 0; c < nch; c++)
			keep[nkeep++] = c;
	} else if (strcmp(argv[3], "none")) {
		char *s = strdup(argv[3]);
		for (char *tok = strtok(s, ","); tok && nkeep < 64; tok = strtok(NULL, ","))
			keep[nkeep++] = atoi(tok);
	}
	dout = fopen(argv[4], "wb");
	FILE *ts = fopen(argv[5], "wb");
	if (!dout || !ts) {
		fprintf(stderr, "b21stamp: open failed: %s\n", strerror(errno));
		return 2;
	}
	ring_sz = (size_t)atoi(argv[6]) << 20;
	ring = malloc(ring_sz);
	if (!ring)
		return 2;
	pthread_t th;
	pthread_create(&th, NULL, writer, NULL);

	size_t fb = (size_t)nch * bps;
	static unsigned char buf[(1 << 16) + 4096], out[(1 << 16) + 4096];
	size_t rem = 0;
	long long total = 0, reads = 0;
	for (;;) {
		ssize_t r = read(0, buf + rem, 1 << 16);
		if (r < 0 && errno == EINTR)
			continue;
		if (r <= 0)
			break;
		struct timespec rt, mo;
		clock_gettime(CLOCK_REALTIME, &rt);
		clock_gettime(CLOCK_MONOTONIC, &mo);
		size_t have = rem + (size_t)r, n = have / fb;
		if (n == 0) {
			rem = have;
			continue;
		}
		if (nkeep) {
			size_t o = 0;
			for (size_t f = 0; f < n; f++)
				for (int k = 0; k < nkeep; k++) {
					memcpy(out + o, buf + f * fb + (size_t)keep[k] * bps, bps);
					o += bps;
				}
			put(out, o);
		}
		rem = have - n * fb;
		memmove(buf, buf + n * fb, rem);
		total += (long long)n;
		reads++;
		int64_t q = total, m = (int64_t)mo.tv_sec * 1000000000LL + mo.tv_nsec;
		double d = (double)rt.tv_sec + rt.tv_nsec / 1e9;
		fwrite(&q, 8, 1, ts);
		fwrite(&d, 8, 1, ts);
		fwrite(&m, 8, 1, ts);
	}
	pthread_mutex_lock(&mu);
	done = 1;
	pthread_cond_signal(&cv);
	pthread_mutex_unlock(&mu);
	pthread_join(th, NULL);
	fclose(dout);
	fclose(ts);
	fprintf(stderr, "b21stamp: frames=%lld reads=%lld kept_slots=%d ring_max_fill=%zu dropped_bytes=%llu partial_bytes=%zu\n",
		total, reads, nkeep, ring_max_fill, dropped, rem);
	return dropped ? 4 : 0;
}
