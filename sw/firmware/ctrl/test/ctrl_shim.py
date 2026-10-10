# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_shim.py - the recorder every compiler of a capture runs (#697).

THE RECORDER. ctrl_capture.py compiles RECORDER, with the real C compiler,
into the capture's bin/, and puts a wrapper there for every compiler name
(gcc, g++, cc, c++, clang, clang++, cpp, the RV32 compiler and their prefixed
and versioned names) that runs

    <recorder> <capture> <name> <real compiler> <argument>...

It has the real compiler expand the invocation (THE EXPANSION), appends one
record to <capture>/records.jsonl, and then executes the real compiler with
the same arguments, so what it compiles and writes is what it would have
without the capture. A record holds the name the compiler was called by, the
real compiler, the arguments, the working directory, every input with the
language the compiler's expansion gave it (and, for C++, the digest of its
text), the digest of the expansion's report, the builder files on the Python
stack of the process that started it (CTRL_CAPTURE_FROM, set by ctrl_capture's
audit hook), the builder file of the command the capture ran it under
(CTRL_CAPTURE_RUN, set by ctrl_capture.run), and the digest of the map of
texts kept beside it. The text of every C++ source, and of every header
outside the checkout a C++ source reaches in a builder's own directories (the
temporary directory, the compile's, the source's) by its #include lines read
as text in every branch against the directories the compiler reported, is
kept under <capture>/text/ by its SHA-256, so a source a builder writes and
deletes is still read. A C++ source outside the checkout, the temporary
directory and the compile's that was there before the capture began (its
inode changed earlier than the capture's start marker's, CTRL_CAPTURE_START)
is an installed tool's own (Verilator's runtime, which its builds compile):
its digest is recorded as "installed", and nothing of it is kept or followed.
A file a builder writes or copies anywhere is its own. It is C so that a
compile costs the capture about a millisecond.

A record that cannot be written stops the compile (exit 2, the reason on
standard error), and so does a C++ source that reaches more headers than one
compile keeps (CLOSURE): a capture never misses an invocation, or a header,
silently.

THE EXPANSION (ctrl_expand.py). Before it records, the recorder has the real
compiler expand the invocation: the expansion's arguments are the
invocation's, each input it takes for a source or a linker input replaced by
an empty stand-in of the same suffix (<capture>/expand/in/<n><suffix>), the
output and dependency options dropped, and -E -dD -v -fpch-preprocess added;
a compile whose output is a precompiled header (.gch) keeps its real inputs.
It reuses an expansion from <capture>/expand/ for the same expansion
arguments, directory, environment and compiler while every file and
directory it reported is unchanged, and only when every argument is one of
the plain forms (PLAIN in RECORDER) and none holds a response file (@);
otherwise it runs ctrl_expand.py's helper (CTRL_CAPTURE_EXPAND), which runs
the compiler, keeps its report and writes the entry the recorder reads back.
"""

#: The recorder (see THE RECORDER), C11 and POSIX.
RECORDER = r'''/* ctrl_shim.py's recorder (#697): <recorder> <capture> <name> <real> <argument>... */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

#define CLOSURE 1024 /* how many headers one compile keeps beside its sources; more refuses the compile */

extern char **environ;

typedef struct { char *data; size_t len, cap; } Buf;
typedef struct { char *path; char hex[65]; } Kept;
typedef struct { Kept items[CLOSURE]; int count; } Map;

static void fail(const char *what, const char *detail)
{
    fprintf(stderr, "ctrl_shim: cannot record into the capture: %s %s\n", what, detail ? detail : "");
    exit(2);
}

static void put(Buf *b, const void *s, size_t n)
{
    if (b->len + n + 1 > b->cap) {
        b->cap = (b->len + n + 1) * 2;
        b->data = realloc(b->data, b->cap);
        if (b->data == NULL)
            fail("out of memory", NULL);
    }
    memcpy(b->data + b->len, s, n);
    b->len += n;
    b->data[b->len] = '\0';
}

static void text(Buf *b, const char *s) { put(b, s, strlen(s)); }

/* A JSON string: quotes, backslashes and control characters escaped, every other byte as it is. */
static void quoted(Buf *b, const char *s)
{
    char esc[8];
    text(b, "\"");
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) {
        if (*p == '"' || *p == '\\') {
            esc[0] = '\\';
            esc[1] = (char)*p;
            put(b, esc, 2);
        } else if (*p < 0x20) {
            snprintf(esc, sizeof esc, "\\u%04x", *p);
            text(b, esc);
        } else {
            put(b, p, 1);
        }
    }
    text(b, "\"");
}

/* ---- SHA-256 (FIPS 180-4) ---- */

static const uint32_t K[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};

static uint32_t rotr(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }

static void block(uint32_t h[8], const unsigned char *p)
{
    uint32_t w[64], a, b, c, d, e, f, g, k, t1, t2;
    for (int i = 0; i < 16; i++)
        w[i] = (uint32_t)p[4 * i] << 24 | (uint32_t)p[4 * i + 1] << 16 | (uint32_t)p[4 * i + 2] << 8 | p[4 * i + 3];
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }
    a = h[0]; b = h[1]; c = h[2]; d = h[3]; e = h[4]; f = h[5]; g = h[6]; k = h[7];
    for (int i = 0; i < 64; i++) {
        t1 = k + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i];
        t2 = (rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c));
        k = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += k;
}

static void sha256(const unsigned char *data, size_t len, char hex[65])
{
    uint32_t h[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab,
                     0x5be0cd19};
    unsigned char tail[128] = {0};
    size_t full = len / 64 * 64, rest = len - full;
    for (size_t at = 0; at < full; at += 64)
        block(h, data + at);
    memcpy(tail, data + full, rest);
    tail[rest] = 0x80;
    size_t blocks = rest < 56 ? 1 : 2;
    uint64_t bits = (uint64_t)len * 8;
    for (int i = 0; i < 8; i++)
        tail[blocks * 64 - 1 - i] = (unsigned char)(bits >> (8 * i));
    for (size_t i = 0; i < blocks; i++)
        block(h, tail + 64 * i);
    for (int i = 0; i < 8; i++)
        snprintf(hex + 8 * i, 9, "%08x", h[i]);
}

/* ---- files ---- */

static char *slurp(const char *path, size_t *len)
{
    int fd = open(path, O_RDONLY);
    if (fd < 0)
        return NULL;
    Buf b = {0};
    char chunk[65536];
    ssize_t n;
    put(&b, "", 0);
    while ((n = read(fd, chunk, sizeof chunk)) > 0)
        put(&b, chunk, (size_t)n);
    close(fd);
    if (n < 0) {
        free(b.data);
        return NULL;
    }
    *len = b.len;
    return b.data;
}

static int regular(const char *path)
{
    struct stat st;
    return stat(path, &st) == 0 && S_ISREG(st.st_mode);
}

/* Whether a resolved path is `top` or under it. */
static int under(const char *path, const char *top)
{
    size_t n = strlen(top);
    while (n > 1 && top[n - 1] == '/')
        n--;
    if (n == 1 && top[0] == '/')
        return 1;
    return strncmp(path, top, n) == 0 && (path[n] == '\0' || path[n] == '/');
}

/* base/name resolved (name as it is when absolute), or base/name joined when it resolves to nothing. */
static char *joined(const char *base, const char *name, int resolve)
{
    char *path = NULL, *real = NULL;
    if (asprintf(&path, "%s%s%s", name[0] == '/' ? "" : base, name[0] == '/' ? "" : "/", name) < 0)
        fail("out of memory", NULL);
    if (resolve && (real = realpath(path, NULL)) != NULL) {
        free(path);
        return real;
    }
    return path;
}

/* A text kept under text/ by its digest, written once. */
static void keep(const char *capture, const char *data, size_t len, char hex[65])
{
    char *path = NULL, *part = NULL;
    sha256((const unsigned char *)data, len, hex);
    if (asprintf(&path, "%s/text/%s", capture, hex) < 0 || asprintf(&part, "%s.%ld", path, (long)getpid()) < 0)
        fail("out of memory", NULL);
    if (access(path, F_OK) != 0) {
        int fd = open(part, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd < 0 || write(fd, data, len) != (ssize_t)len || close(fd) != 0 || rename(part, path) != 0)
            fail("cannot keep a text at", path);
    }
    free(path);
    free(part);
}

static int has(const Map *m, const char *path)
{
    for (int i = 0; i < m->count; i++)
        if (strcmp(m->items[i].path, path) == 0)
            return 1;
    return 0;
}

static void add(Map *m, const char *capture, const char *path, const char *data, size_t len)
{
    if (has(m, path))
        return;
    if (m->count >= CLOSURE)
        fail("a C++ source reaches more headers than the capture keeps for one compile:", path);
    m->items[m->count].path = strdup(path);
    keep(capture, data, len, m->items[m->count].hex);
    m->count++;
}

/* ---- the arguments: which are inputs, which are outputs, which leave an expansion reusable ---- */

/* Options whose value is the next argument (GCC's and Clang's drivers), when not joined to it. */
static const char *const SEPARATE[] = {"-o", "-x", "-I", "-D", "-U", "-include", "-imacros", "-isystem",
    "-iquote", "-idirafter", "-iprefix", "-iwithprefix", "-iwithprefixbefore", "-isysroot", "--sysroot", "-MF",
    "-MT", "-MQ", "-MJ", "-L", "-l", "-T", "-Xlinker", "-Xassembler", "-Xpreprocessor", "-Xclang", "-aux-info",
    "-dumpbase", "-dumpbase-ext", "-dumpdir", "-wrapper", "-arch", "-target", "--target", "-e", "-u", "-z",
    "--param", "-A", "-B", "-G", "-imultilib", "-iframework", "--define-macro", "--undefine-macro",
    "--include-directory", "--include-directory-after", "--include-prefix", "--include-with-prefix",
    "--include-with-prefix-after", "--include-with-prefix-before", "--include", "--imacros", "--language",
    "--output", "--assert", "--dumpbase", "--dumpdir", "--for-linker", "--force-link", "--library-directory",
    "--prefix", "--specs", "-isystem-after", "-cxx-isystem", "-iwithsysroot", "-include-pch", "-ivfsoverlay",
    "-working-directory", "-resource-dir", "-gcc-toolchain", "-mllvm", NULL};
/* Of those, the outputs: dropped from an expansion with their value. */
static const char *const OUTPUTS[] = {"-o", "--output", "-MF", "-MT", "-MQ", "-MJ", NULL};
/* Output and dependency options with no value, dropped from an expansion. */
static const char *const FORMATS[] = {"-M", "-MM", "-MD", "-MMD", "-MP", "-MG", "-P", NULL};
/* The plain forms: an argument of one of these kinds reads no file the expansion does not report. */
static const char *const PLAIN_PREFIX[] = {"-D", "-U", "-I", "-iquote", "-isystem", "-idirafter", "-include",
    "-imacros", "-std=", "-O", "-W", "-f", "-m", "-g", "-x", "-l", "-L", "--sysroot", "-isysroot", "-print-",
    "-dump", "--param", NULL};
static const char *const PLAIN[] = {"-c", "-S", "-E", "-v", "-w", "-H", "-C", "-CC", "-pipe", "-pthread",
    "-pedantic", "-pedantic-errors", "--coverage", "-shared", "-static", "-pie", "-no-pie", "-rdynamic",
    "-nostdlib", "-nostartfiles", "-nodefaultlibs", "-nostdinc", "-nostdinc++", "-undef", "-ansi", "-p", "-pg",
    "-s", "--version", "-Xlinker", "-Xassembler", NULL};

static int one_of(const char *s, const char *const *list)
{
    for (int i = 0; list[i] != NULL; i++)
        if (strcmp(s, list[i]) == 0)
            return 1;
    return 0;
}

static int prefixed(const char *s, const char *const *list)
{
    for (int i = 0; list[i] != NULL; i++)
        if (strncmp(s, list[i], strlen(list[i])) == 0)
            return 1;
    return 0;
}

/* An output or format option with its value joined (-ofile, --output=file, -MFfile), or a -d letters option. */
static int output(const char *arg)
{
    if (one_of(arg, FORMATS))
        return 1;
    if (arg[1] == 'o' && arg[2] != '\0' && strncmp(arg, "-objc", 5) != 0 && strncmp(arg, "-object", 7) != 0)
        return 1;
    if (!strncmp(arg, "--output=", 9))
        return 1;
    if ((!strncmp(arg, "-MF", 3) || !strncmp(arg, "-MT", 3) || !strncmp(arg, "-MQ", 3) || !strncmp(arg, "-MJ", 3))
        && arg[3] != '\0')
        return 1;
    if (arg[1] == 'd' && arg[2] >= 'A' && arg[2] <= 'Z' && strspn(arg + 2, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") ==
        strlen(arg + 2))
        return 1;
    return 0;
}

static int plain(const char *arg)
{
    if (strchr(arg, '@') != NULL || !strncmp(arg, "-fplugin", 8))
        return 0;
    return one_of(arg, PLAIN) || prefixed(arg, PLAIN_PREFIX);
}

/* A path's suffix: from the last '.' of its last part, unless that '.' begins it; "" when it holds more than
 * letters, digits, '+' and '_' (a stand-in's name). */
static const char *suffix_of(const char *path)
{
    const char *base = strrchr(path, '/');
    base = base ? base + 1 : path;
    const char *dot = strrchr(base, '.');
    if (dot == NULL || dot == base)
        return "";
    for (const char *p = dot + 1; *p; p++)
        if (!(*p == '+' || *p == '_' || (*p >= '0' && *p <= '9') || (*p >= 'a' && *p <= 'z') ||
              (*p >= 'A' && *p <= 'Z')))
            return "";
    return dot;
}

/* An output, as a later compile names it: its directory resolved (it exists when the compile runs), then its name. */
static char *produced(const char *cwd, const char *out)
{
    char *path = joined(cwd, out, 0), *slash = strrchr(path, '/'), *dir = NULL, *full = NULL;
    if (slash == NULL || slash == path)
        return path;
    *slash = '\0';
    dir = realpath(path, NULL);
    if (dir == NULL) {
        *slash = '/';
        return path;
    }
    if (asprintf(&full, "%s/%s", dir, slash + 1) < 0)
        fail("out of memory", NULL);
    free(dir);
    free(path);
    return full;
}

/* The empty stand-in of input `n`, of its suffix, made once per capture and read-only, so a compiler that would
 * write its output there (a positional output) fails instead. */
static char *stand_in(const char *capture, int n, const char *arg)
{
    char *path = NULL;
    if (asprintf(&path, "%s/expand/in/%d%s", capture, n, suffix_of(arg)) < 0)
        fail("out of memory", NULL);
    int fd = open(path, O_WRONLY | O_CREAT | O_EXCL, 0444);
    if (fd >= 0)
        close(fd);
    else if (errno != EEXIST)
        fail("cannot make a stand-in at", path);
    return path;
}

/* ---- the expansion's entry: what the helper found, and whether it still holds ---- */

typedef struct {
    char report[65];
    int rc, fresh, valid;
    const char **lang;
    char **dirs;
    int ndirs;
    char error[400];
} Entry;

static int64_t nanos(struct timespec t) { return (int64_t)t.tv_sec * 1000000000 + t.tv_nsec; }

/* One "file <dev> <ino> <size> <mtime ns> <ctime ns> <path>" line: whether that file is unchanged. */
static int unchanged(const char *line)
{
    unsigned long long dev, ino;
    long long size, mtime, ctime;
    int at = 0;
    struct stat st;
    if (sscanf(line, "%llu %llu %lld %lld %lld %n", &dev, &ino, &size, &mtime, &ctime, &at) != 5 || at == 0)
        return 0;
    return stat(line + at, &st) == 0 && (unsigned long long)st.st_dev == dev &&
           (unsigned long long)st.st_ino == ino && (long long)st.st_size == size && nanos(st.st_mtim) == mtime &&
           nanos(st.st_ctim) == ctime;
}

/* The entry at `path`, read for `ninputs` inputs; `valid` when every file and directory it reported holds and it
 * may be reused (a fresh one only right after the helper wrote it). */
static void load(const char *path, int ninputs, int accept_fresh, Entry *e)
{
    size_t len = 0;
    char *data = slurp(path, &len);
    memset(e, 0, sizeof *e);
    e->lang = calloc((size_t)ninputs + 1, sizeof *e->lang);
    if (data == NULL || e->lang == NULL)
        return;
    int holds = 1, count = 0;
    for (char *line = data; line != NULL && *line; ) {
        char *end = strchr(line, '\n');
        if (end != NULL)
            *end = '\0';
        count++;
        struct stat st;
        if (!strncmp(line, "report ", 7))
            snprintf(e->report, sizeof e->report, "%s", line + 7);
        else if (!strncmp(line, "rc ", 3))
            e->rc = atoi(line + 3);
        else if (!strncmp(line, "lang ", 5)) {
            int k = atoi(line + 5);
            char *l = strchr(line + 5, ' ');
            if (k >= 0 && k < ninputs && l != NULL)
                e->lang[k] = strdup(l + 1);
        } else if (!strncmp(line, "dir ", 4)) {
            char **more = realloc(e->dirs, (size_t)(e->ndirs + 1) * sizeof *more);
            if (more == NULL)
                fail("out of memory", NULL);
            e->dirs = more;
            e->dirs[e->ndirs++] = strdup(line + 4);
            holds &= stat(line + 4, &st) == 0 && S_ISDIR(st.st_mode);
        } else if (!strncmp(line, "nodir ", 6))
            holds &= stat(line + 6, &st) != 0;
        else if (!strncmp(line, "file ", 5))
            holds &= unchanged(line + 5);
        else if (!strcmp(line, "fresh"))
            e->fresh = 1;
        else if (!strncmp(line, "error ", 6))
            snprintf(e->error, sizeof e->error, "%s", line + 6);
        line = end != NULL ? end + 1 : NULL;
    }
    free(data);
    e->valid = count > 0 && holds && (!e->fresh || accept_fresh) && (e->report[0] != '\0' || e->error[0] != '\0');
}

static int by_text(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

/* The expansion's cache key: the compiler (and its file), the directory, the expansion's arguments and the
 * environment (but the capture's own attribution, which no compiler reads). */
static void cache_key(const char *real, const char *cwd, char **exp, int nexp, char hex[65])
{
    Buf b = {0};
    struct stat st;
    char line[160];
    if (stat(real, &st) != 0)
        memset(&st, 0, sizeof st);
    text(&b, "ctrl-expand 1\n");
    text(&b, real);
    snprintf(line, sizeof line, "\n%llu %llu %lld %lld\n", (unsigned long long)st.st_dev,
             (unsigned long long)st.st_ino, (long long)st.st_size, (long long)nanos(st.st_mtim));
    text(&b, line);
    text(&b, cwd);
    for (int i = 0; i < nexp; i++) {
        put(&b, "", 1);
        text(&b, exp[i]);
    }
    int nenv = 0;
    while (environ[nenv] != NULL)
        nenv++;
    char **env = calloc((size_t)nenv + 1, sizeof *env);
    if (env == NULL)
        fail("out of memory", NULL);
    memcpy(env, environ, (size_t)nenv * sizeof *env);
    qsort(env, (size_t)nenv, sizeof *env, by_text);
    text(&b, "\nenv");
    for (int i = 0; i < nenv; i++) {
        if (!strncmp(env[i], "CTRL_CAPTURE_FROM=", 18) || !strncmp(env[i], "CTRL_CAPTURE_RUN=", 17))
            continue;
        put(&b, "", 1);
        text(&b, env[i]);
    }
    sha256((const unsigned char *)b.data, b.len, hex);
    free(env);
    free(b.data);
}

/* Run the helper (ctrl_expand.py expand) for this expansion; it writes the entry at `path`. `real` lists the inputs
 * the expansion keeps as they are (a precompiled header's), as "<index>=<argument>". */
static void helper(const char *capture, const char *path, int fresh, int stdin_k, char **real, int nreal, char **exp,
                   int nexp)
{
    const char *python = getenv("CTRL_CAPTURE_PYTHON"), *shim = getenv("CTRL_CAPTURE_EXPAND");
    if (python == NULL || shim == NULL)
        return;
    char index[16];
    snprintf(index, sizeof index, "%d", stdin_k);
    char **argv = calloc((size_t)(nexp + nreal) + 12, sizeof *argv);
    if (argv == NULL)
        fail("out of memory", NULL);
    const char *head[] = {python, "-I", "-S", shim, "expand", capture, path, fresh ? "fresh" : "reuse", index};
    int n = 0;
    for (size_t i = 0; i < sizeof head / sizeof head[0]; i++)
        argv[n++] = (char *)head[i];
    for (int i = 0; i < nreal; i++)
        argv[n++] = real[i];
    argv[n++] = "--";
    for (int i = 0; i < nexp; i++)
        argv[n++] = exp[i];
    pid_t pid = fork();
    if (pid == 0) {
        int null = open("/dev/null", O_RDWR);
        if (null >= 0) {
            dup2(null, 0);
            dup2(null, 1);
            dup2(null, 2);
        }
        execv(python, argv);
        _exit(127);
    }
    int status = 0;
    if (pid > 0)
        while (waitpid(pid, &status, 0) < 0 && errno == EINTR)
            ;
    free(argv);
}

/* ---- the headers a C++ source reaches outside the checkout ---- */

static int outside_root(const char *path, const char *root) { return !under(path, root); }

/* Whether a file is the builder's: in the checkout, the builder's temporary directory or the compile's working
 * directory, or written (or copied) since the capture began, its inode changed no earlier than the capture's start
 * marker's (`start`, CTRL_CAPTURE_START). Only a file elsewhere that was there before is an installed tool's own (a
 * runtime the tool compiles into the build). */
static int own(const char *path, const char *root, const char *temp, const char *here, const struct stat *start)
{
    struct stat st;
    if (under(path, root) || under(path, temp) || under(path, here))
        return 1;
    if (start == NULL || stat(path, &st) != 0)
        return 1;
    return st.st_ctim.tv_sec > start->st_ctim.tv_sec ||
           (st.st_ctim.tv_sec == start->st_ctim.tv_sec && st.st_ctim.tv_nsec >= start->st_ctim.tv_nsec);
}

static void closure(Map *kept, const char *capture, const char *root, char *const *tops, int ntops,
                    const char *source, char *data, size_t len, char **dirs, int ndirs)
{
    char *queue_path[CLOSURE + 1];
    char *queue_data[CLOSURE + 1];
    size_t queue_len[CLOSURE + 1];
    int queued = 0;
    queue_path[queued] = strdup(source);
    queue_data[queued] = data;
    queue_len[queued++] = len;
    while (queued > 0) {
        queued--;
        char *path = queue_path[queued], *body = queue_data[queued];
        size_t n = queue_len[queued];
        Buf flat = {0};
        put(&flat, "", 0);
        for (size_t i = 0; i < n; i++) {
            if (body[i] == '\\' && i + 1 < n && body[i + 1] == '\n') {
                i++;
                continue;
            }
            put(&flat, body + i, 1);
        }
        char *dir = strdup(path), *slash = strrchr(dir, '/');
        if (slash != NULL)
            *slash = '\0';
        for (char *line = flat.data; line != NULL && *line; ) {
            char *end = strchr(line, '\n'), *p = line;
            if (end != NULL)
                *end = '\0';
            p += strspn(p, " \t\r\f\v");
            if (*p == '#') {
                p++;
                p += strspn(p, " \t\r\f\v");
                if (!strncmp(p, "include", 7)) {
                    p += 7;
                    if (!strncmp(p, "_next", 5))
                        p += 5;
                    p += strspn(p, " \t\r\f\v");
                    if (*p == '<' || *p == '"') {
                        int quote = *p == '"';
                        char *name = ++p;
                        size_t len_name = strcspn(name, ">\"");
                        if (len_name > 0 && name[len_name] != '\0') {
                            name[len_name] = '\0';
                            for (int b = quote ? -1 : 0; b < ndirs; b++) {
                                char *hit = joined(b < 0 ? dir : dirs[b], name, 1);
                                int ours = 0;
                                for (int t = 0; t < ntops; t++)
                                    ours |= under(hit, tops[t]);
                                size_t hit_len = 0;
                                char *hit_data = NULL;
                                if (has(kept, hit) || !outside_root(hit, root) || !ours || !regular(hit) ||
                                    (hit_data = slurp(hit, &hit_len)) == NULL) {
                                    free(hit);
                                    continue;
                                }
                                add(kept, capture, hit, hit_data, hit_len);
                                if (queued >= CLOSURE)
                                    fail("a C++ source reaches more headers than the capture keeps for one compile:",
                                         source);
                                queue_path[queued] = hit;
                                queue_data[queued] = hit_data;
                                queue_len[queued++] = hit_len;
                                break;
                            }
                        }
                    }
                }
            }
            line = end != NULL ? end + 1 : NULL;
        }
        free(flat.data);
        free(dir);
        free(path);
        if (body != data)
            free(body);
    }
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "ctrl_shim: usage: <recorder> <capture> <name> <real> <argument>...\n");
        return 2;
    }
    const char *capture = argv[1], *name = argv[2], *real = argv[3];
    const char *root = getenv("CTRL_CAPTURE_ROOT") ? getenv("CTRL_CAPTURE_ROOT") : "/";
    char **args = argv + 4;
    int nargs = argc - 4;
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof cwd) == NULL)
        fail("cannot read the working directory", NULL);
    /* the output (-o), resolved as far as it exists: a precompiled header's maker (a .gch, or one in a .gch
     * directory, as GCC finds one) is expanded over its real inputs, which later compiles read first */
    const char *out = "";
    for (int at = 0; at < nargs; at++) {
        if ((!strcmp(args[at], "-o") || !strcmp(args[at], "--output")) && at + 1 < nargs)
            out = args[++at];
        else if (args[at][0] == '-' && args[at][1] == 'o' && args[at][2] != '\0' && output(args[at]))
            out = args[at] + 2;
        else if (!strncmp(args[at], "--output=", 9))
            out = args[at] + 9;
        else if (one_of(args[at], SEPARATE))
            at++;
    }
    char *output_path = *out ? produced(cwd, out) : strdup("");
    size_t out_len = strlen(output_path);
    int pch = (out_len > 4 && !strcmp(output_path + out_len - 4, ".gch")) || strstr(output_path, ".gch/") != NULL;
    /* the expansion's arguments: each input its stand-in (or itself, for a precompiled header's maker), the
     * outputs dropped, then -E -dD -v -fpch-preprocess */
    char **exp = calloc((size_t)nargs + 8, sizeof *exp), **inputs = calloc((size_t)nargs + 1, sizeof *inputs);
    char **kept_real = calloc((size_t)nargs + 1, sizeof *kept_real);
    if (exp == NULL || inputs == NULL || kept_real == NULL)
        fail("out of memory", NULL);
    int nexp = 0, ninputs = 0, nreal = 0, stdin_k = -1, reusable = !pch, files = 0;
    exp[nexp++] = (char *)real;
    for (int at = 0; at < nargs; at++) {
        char *arg = args[at], *value = at + 1 < nargs ? args[at + 1] : "";
        files |= arg[0] == '@';
        if (one_of(arg, SEPARATE)) {
            if (!one_of(arg, OUTPUTS)) {
                exp[nexp++] = arg;
                exp[nexp++] = value;
                reusable &= plain(arg) && strchr(value, '@') == NULL;
            }
            at++;
            continue;
        }
        if (arg[0] == '-' && arg[1] != '\0' && output(arg))
            continue;
        if (!strcmp(arg, "-")) {
            stdin_k = ninputs;
            inputs[ninputs++] = arg;
            exp[nexp++] = arg;
        } else if (arg[0] == '-' || arg[0] == '@') {
            exp[nexp++] = arg;
            reusable &= plain(arg);
        } else if (pch) {
            if (asprintf(&kept_real[nreal++], "%d=%s", ninputs, arg) < 0)
                fail("out of memory", NULL);
            exp[nexp++] = arg;
            inputs[ninputs++] = arg;
        } else {
            exp[nexp++] = stand_in(capture, ninputs, arg);
            inputs[ninputs++] = arg;
        }
    }
    exp[nexp++] = "-E";
    exp[nexp++] = "-dD";
    exp[nexp++] = "-v";
    exp[nexp++] = "-fpch-preprocess";
    /* an invocation that names no input and no response file compiles nothing (--version, -print-*): no expansion */
    int expanded = ninputs > 0 || files;
    char key[65], *entry = NULL;
    cache_key(real, cwd, exp, nexp, key);
    if (asprintf(&entry, reusable ? "%s/expand/%s" : "%s/expand/%s.%ld", capture, key, (long)getpid()) < 0)
        fail("out of memory", NULL);
    Entry e;
    load(entry, ninputs, 0, &e);
    if (expanded && !e.valid) {
        helper(capture, entry, !reusable, stdin_k, kept_real, nreal, exp, nexp);
        load(entry, ninputs, 1, &e);
    }
    if (!reusable)
        unlink(entry);
    char *temp = realpath(getenv("TMPDIR") && *getenv("TMPDIR") ? getenv("TMPDIR") : "/tmp", NULL);
    char *here = realpath(cwd, NULL);
    const char *temp_dir = temp ? temp : "/tmp", *here_dir = here ? here : cwd;
    struct stat begun;
    const char *marker = getenv("CTRL_CAPTURE_START");
    const struct stat *start = marker != NULL && stat(marker, &begun) == 0 ? &begun : NULL;
    Map kept = {0};
    Buf r = {0};
    text(&r, "{\"tool\": ");
    quoted(&r, name);
    text(&r, ", \"real\": ");
    quoted(&r, real);
    text(&r, ", \"args\": [");
    for (int i = 0; i < nargs; i++) {
        text(&r, i ? ", " : "");
        quoted(&r, args[i]);
    }
    text(&r, "], \"cwd\": ");
    quoted(&r, cwd);
    text(&r, ", \"sources\": [");
    for (int i = 0; i < ninputs; i++) {
        char *full = strcmp(inputs[i], "-") ? joined(cwd, inputs[i], 1) : strdup("-");
        const char *lang = e.valid && e.lang[i] != NULL ? e.lang[i] : "other";
        char hex[65] = "";
        size_t len = 0;
        char *data = NULL;
        if (!strcmp(lang, "c++")) {
            if (strcmp(full, "-") && regular(full) && !own(full, root, temp_dir, here_dir, start)) {
                /* an installed tool's own source (a runtime it compiles into the build): not the builder's */
                snprintf(hex, sizeof hex, "installed");
            } else if (strcmp(full, "-") && regular(full) && (data = slurp(full, &len)) != NULL) {
                keep(capture, data, len, hex);
                char *dir = strdup(full), *slash = strrchr(dir, '/');
                if (slash != NULL)
                    *slash = '\0';
                char *tops[3] = {(char *)temp_dir, (char *)here_dir, dir};
                closure(&kept, capture, root, tops, 3, full, data, len, e.dirs, e.ndirs);
                free(dir);
                free(data);
            }
        }
        text(&r, i ? ", [" : "[");
        quoted(&r, full);
        text(&r, ", ");
        quoted(&r, lang);
        text(&r, ", ");
        quoted(&r, hex);
        text(&r, "]");
        free(full);
    }
    text(&r, "], \"output\": ");
    quoted(&r, output_path);
    text(&r, expanded ? ", \"expanded\": true, \"expansion\": " : ", \"expanded\": false, \"expansion\": ");
    quoted(&r, e.valid ? e.report : "");
    text(&r, ", \"expand_error\": ");
    quoted(&r, e.valid || !expanded ? e.error : "the capture's expansion helper wrote no entry it could read back");
    text(&r, ", \"kept\": ");
    if (kept.count > 0) {
        Buf map = {0};
        char hex[65];
        text(&map, "{");
        for (int i = 0; i < kept.count; i++) {
            text(&map, i ? ", " : "");
            quoted(&map, kept.items[i].path);
            text(&map, ": ");
            quoted(&map, kept.items[i].hex);
        }
        text(&map, "}");
        keep(capture, map.data, map.len, hex);
        quoted(&r, hex);
        free(map.data);
    } else {
        quoted(&r, "");
    }
    text(&r, ", \"from\": ");
    quoted(&r, getenv("CTRL_CAPTURE_FROM") ? getenv("CTRL_CAPTURE_FROM") : "");
    text(&r, ", \"run\": ");
    quoted(&r, getenv("CTRL_CAPTURE_RUN") ? getenv("CTRL_CAPTURE_RUN") : "");
    text(&r, "}\n");
    char *path = NULL;
    if (asprintf(&path, "%s/records.jsonl", capture) < 0)
        fail("out of memory", NULL);
    int fd = open(path, O_WRONLY | O_APPEND | O_CREAT, 0644);
    if (fd < 0 || write(fd, r.data, r.len) != (ssize_t)r.len || close(fd) != 0)
        fail("cannot append to", path);
    argv[3] = (char *)real;
    execv(real, argv + 3);
    perror("ctrl_shim: cannot run the compiler");
    return 127;
}
'''
