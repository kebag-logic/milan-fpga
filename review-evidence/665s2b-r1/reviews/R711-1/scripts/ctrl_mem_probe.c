// Exhaustive reference check of sw/firmware/ctrl/plat/ctrl_mem.c (renamed with
// -D at compile time): every offset pair and length up to MAXN, overlap both
// ways, guard bytes either side, and reads that stop at a PROT_NONE page.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/mman.h>
#include <unistd.h>
void *kl_memcpy(void *restrict, const void *restrict, size_t);
void *kl_memmove(void *, const void *, size_t);
void *kl_memset(void *, int, size_t);
int kl_memcmp(const void *, const void *, size_t);
#define MAXN 200
static unsigned char buf[4096], ref[4096];
static long fails;
static int sgn(int v) { return (v > 0) - (v < 0); }
int main(void)
{
	long cases = 0;
	for (int i = 0; i < 4096; ++i) buf[i] = ref[i] = (unsigned char)(i * 7 + 3);
	// memcpy, disjoint
	for (int so = 0; so < 8; ++so) for (int dof = 0; dof < 8; ++dof) for (int n = 0; n <= MAXN; ++n) {
		for (int i = 0; i < 4096; ++i) buf[i] = ref[i] = (unsigned char)(i * 13 + n);
		unsigned char *d = buf + 64 + dof, *s = buf + 1024 + so;
		void *r = kl_memcpy(d, s, (size_t)n);
		memcpy(ref + 64 + dof, ref + 1024 + so, (size_t)n);
		if (r != d || memcmp(buf, ref, 4096)) { if (fails++ < 5) printf("memcpy so=%d do=%d n=%d\n", so, dof, n); }
		cases++;
	}
	// memmove, overlapping both directions, every shift up to 40
	for (int so = 0; so < 8; ++so) for (int sh = -40; sh <= 40; ++sh) for (int n = 0; n <= MAXN; ++n) {
		for (int i = 0; i < 4096; ++i) buf[i] = ref[i] = (unsigned char)(i * 5 + n + sh);
		unsigned char *s = buf + 1024 + so, *d = s + sh;
		void *r = kl_memmove(d, s, (size_t)n);
		memmove(ref + 1024 + so + sh, ref + 1024 + so, (size_t)n);
		if (r != d || memcmp(buf, ref, 4096)) { if (fails++ < 5) printf("memmove so=%d sh=%d n=%d\n", so, sh, n); }
		cases++;
	}
	// memset
	for (int dof = 0; dof < 8; ++dof) for (int c = 0; c < 3; ++c) for (int n = 0; n <= MAXN; ++n) {
		int v = c == 0 ? 0 : c == 1 ? 0xA5 : 0x1FF;
		for (int i = 0; i < 4096; ++i) buf[i] = ref[i] = (unsigned char)(i * 3 + n);
		void *r = kl_memset(buf + 64 + dof, v, (size_t)n);
		memset(ref + 64 + dof, v, (size_t)n);
		if (r != buf + 64 + dof || memcmp(buf, ref, 4096)) { if (fails++ < 5) printf("memset do=%d v=%x n=%d\n", dof, v, n); }
		cases++;
	}
	// memcmp: equal, and a single differing byte at every position, both signs
	for (int ao = 0; ao < 8; ++ao) for (int bo = 0; bo < 8; ++bo) for (int n = 0; n <= 80; ++n) for (int pos = -1; pos < n; ++pos) for (int dir = 0; dir < 2; ++dir) {
		unsigned char *a = buf + 64 + ao, *b = buf + 1024 + bo;
		for (int i = 0; i < n; ++i) a[i] = b[i] = (unsigned char)(i * 11 + 1);
		if (pos >= 0) { a[pos] = dir ? 0xF0 : 0x01; b[pos] = dir ? 0x01 : 0xF0; }
		if (sgn(kl_memcmp(a, b, (size_t)n)) != sgn(memcmp(a, b, (size_t)n)) || (pos >= 0 && kl_memcmp(a, b, (size_t)n) != (int)a[pos] - (int)b[pos])) {
			if (fails++ < 5) printf("memcmp ao=%d bo=%d n=%d pos=%d\n", ao, bo, n, pos);
		}
		cases++;
	}
	// bounds: source and destination end at a PROT_NONE page, and start right after one
	long pg = sysconf(_SC_PAGESIZE);
	unsigned char *m = mmap(NULL, (size_t)pg * 5, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	mprotect(m, (size_t)pg, PROT_NONE);
	mprotect(m + 2 * pg, (size_t)pg, PROT_NONE);
	mprotect(m + 4 * pg, (size_t)pg, PROT_NONE);
	unsigned char *lo = m + pg, *hi = m + 3 * pg;   // two writable pages, each fenced both sides
	for (int n = 0; n <= MAXN; ++n) for (int so = 0; so < 8; ++so) for (int dof = 0; dof < 8; ++dof) {
		unsigned char *s_end = lo + pg - so, *d_end = hi + pg - dof;          // end at the fence
		kl_memcpy(d_end - n, s_end - n, (size_t)n);
		kl_memmove(d_end - n, s_end - n, (size_t)n);
		kl_memcpy(hi + dof, lo + so, (size_t)n);                              // start after the fence
		kl_memmove(hi + dof, lo + so, (size_t)n);
		kl_memset(d_end - n, 1, (size_t)n);
		kl_memset(hi + dof, 1, (size_t)n);
		(void)kl_memcmp(d_end - n, s_end - n, (size_t)n);
		(void)kl_memcmp(hi + dof, lo + so, (size_t)n);
		// overlapping inside one fenced page, near both fences
		if (n <= 100) { kl_memmove(lo + so, lo + so + 3, (size_t)n); kl_memmove(lo + pg - n - 3, lo + pg - n - 3 - (so % 4 + 1), (size_t)n);
			kl_memmove(lo + pg - n, lo + pg - n - (so + 1), (size_t)n); kl_memmove(lo + (dof), lo + dof + so + 1, (size_t)n); }
		cases += 12;
	}
	printf("ctrl_mem probe: %ld cases, %ld failures\n", cases, fails);
	return fails != 0;
}
