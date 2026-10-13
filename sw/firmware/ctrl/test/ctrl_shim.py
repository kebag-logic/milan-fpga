# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_shim.py - the recorder every compiler of a capture runs (#697).

THE RECORDER. ctrl_capture.py compiles RECORDER, with the real C compiler,
into the capture's bin/, and puts a wrapper there for every compiler name
(gcc, g++, cc, c++, clang, clang++, cpp, the RV32 compiler and their prefixed
and versioned names) that runs

    <recorder> <capture> <name> <real compiler> <argument>...

It has the real compiler expand the invocation (THE EXPANSION), has it list
what each source's compile reads (THE DEPENDENCY PASS), runs the real
compiler with the same arguments and waits for it, so what it compiles and
writes is what it would have without the capture, appends one record to
<capture>/records.jsonl, and exits as the compiler did (a signal the
recorder takes meanwhile is passed on to the compiler, and a signal that ends
the compiler ends the recorder). A record holds the name the compiler was
called by, the real compiler, the arguments, the working directory, every
input with the
language the compiler's expansion gave it and, for a source it compiles (C,
C++ or preprocessed assembler), the digest of its dependency pass's kept
list or why the pass gave none, the digest of the expansion's report, the
builder files on the Python stack of the process that started it
(CTRL_CAPTURE_FROM, set by ctrl_capture's audit hook) and the builder file of
the command the capture ran it under (CTRL_CAPTURE_RUN, set by
ctrl_capture.run), and the compile's exit status. It is C so that a compile
costs the capture little more than its own dependency pass.

A record that cannot be written fails the invocation (exit 2, the reason on
standard error), even when the compile passed: a capture never misses an
invocation silently.

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

THE DEPENDENCY PASS. For each source the expansion says it compiles, the
recorder runs the real compiler once more, in the invocation's directory and
environment (LC_ALL=C, so its messages are read in English), with the
invocation's own arguments: its output and dependency options dropped as the
expansion drops them, every other input left out (one source per pass), and
-M -MF <file> -MT dependencies -H -fpch-preprocess added (and
-Qunused-arguments for a driver the expansion found to be Clang, as it adds).
The compiler writes the rule of every file the compile reads (-M: the source,
what the command line reads first, what the source includes, the system
headers too) and, on its standard error, the tree of the files the source's
own #include lines read, each at its depth (-H; GCC and Clang print neither a
file the command line reads first nor what that file reads). -fpch-preprocess
has GCC read a precompiled header the compile reads first, as the compile
does, rather than the header's text; the rule then leaves out what the header
read, which the record of the compile that made it holds (ctrl_capture's
reader adds it). Every name is resolved from the directory
while the files are there. The list (the source aside) and the tree, as
indexes into it, are kept under <capture>/text/ by their SHA-256. A pass
gives none, and the record says why, when the compiler fails (but on #error
or #warning directives alone, after which it still lists every file it read),
writes no rule, names first a file that is not the source, names a file that
does not exist, or prints a tree entry the rule does not hold, and for a
source read from standard input, which a pass cannot read again.
"""

#: The recorder (see THE RECORDER), C11 and POSIX.
RECORDER = r'''/* ctrl_shim.py's recorder (#697): <recorder> <capture> <name> <real> <argument>... */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;

/* The compile the recorder waits for, which each of PASSED it takes is passed on to. */
static volatile pid_t compiling;
static const int PASSED[] = {SIGINT, SIGTERM, SIGHUP};

static void pass_on(int sig)
{
    if (compiling > 0)
        kill(compiling, sig);
}

typedef struct { char *data; size_t len, cap; } Buf;

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
    int rc, fresh, valid, clang;
    const char **lang;
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
        } else if (!strncmp(line, "dir ", 4))
            holds &= stat(line + 4, &st) == 0 && S_ISDIR(st.st_mode);
        else if (!strncmp(line, "nodir ", 6))
            holds &= stat(line + 6, &st) != 0;
        else if (!strncmp(line, "file ", 5))
            holds &= unchanged(line + 5);
        else if (!strcmp(line, "driver clang"))
            e->clang = 1;
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
    text(&b, "ctrl-expand 2\n");
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

/* ---- the dependency pass (see THE DEPENDENCY PASS) ---- */

typedef struct { char **path; int count, cap; } List;

/* The index of a path in the list, added when it is not there yet. */
static int indexed(List *l, const char *path)
{
    for (int i = 0; i < l->count; i++)
        if (strcmp(l->path[i], path) == 0)
            return i;
    if (l->count == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 64;
        l->path = realloc(l->path, (size_t)l->cap * sizeof *l->path);
        if (l->path == NULL)
            fail("out of memory", NULL);
    }
    l->path[l->count] = strdup(path);
    return l->count++;
}

static int find(const List *l, const char *path)
{
    for (int i = 0; i < l->count; i++)
        if (strcmp(l->path[i], path) == 0)
            return i;
    return -1;
}

/* The prerequisites of a dependency rule, unescaped as GCC and Clang write them: a line continuation is a blank,
 * "\ " a space, "\#" a '#', "$$" a '$'. Each is written into `rule` in place; their count, or -1 with no rule. */
static int prerequisites(char *rule, char ***out)
{
    char *colon = strstr(rule, "dependencies:");
    if (colon != rule)
        return -1;
    char *src = rule + strlen("dependencies:"), *dst = src, *start = NULL;
    int count = 0, cap = 0;
    char **words = NULL;
    for (;; src++) {
        int blank = *src == '\0' || *src == ' ' || *src == '\t' || *src == '\n' || *src == '\r';
        if (*src == '\\' && (src[1] == '\n' || (src[1] == '\r' && src[2] == '\n'))) {
            src += src[1] == '\r' ? 2 : 1;
            blank = 1;
        }
        if (blank) {
            if (start != NULL) {
                *dst++ = '\0';
                if (count == cap) {
                    cap = cap ? cap * 2 : 64;
                    words = realloc(words, (size_t)cap * sizeof *words);
                    if (words == NULL)
                        fail("out of memory", NULL);
                }
                words[count++] = start;
                start = NULL;
            }
            if (*src == '\0')
                break;
            continue;
        }
        if (start == NULL)
            start = dst;
        if (*src == '\\' && (src[1] == ' ' || src[1] == '#'))
            src++;
        else if (*src == '$' && src[1] == '$')
            src++;
        *dst++ = *src;
    }
    *out = words;
    return count;
}

/* The dependency pass of input `self` (its argument at `at[self]`): the digest of its kept list and tree in `hex`,
 * or why it gives none in `error`. */
static void dependencies(const char *capture, const char *real, char **args, int nargs, const int *at, int ninputs,
                         int self, int clang, const char *cwd, char hex[65], char error[400])
{
    static int passes;
    char *depfile = NULL;
    hex[0] = error[0] = '\0';
    if (!strcmp(args[at[self]], "-")) {
        snprintf(error, 400, "it compiles its standard input, which a dependency pass cannot read again");
        return;
    }
    if (asprintf(&depfile, "%s/deps/%ld.%d.d", capture, (long)getpid(), passes++) < 0)
        fail("out of memory", NULL);
    char **argv = calloc((size_t)nargs + 10, sizeof *argv);
    if (argv == NULL)
        fail("out of memory", NULL);
    int n = 0, input = 0;
    argv[n++] = (char *)real;
    for (int i = 0; i < nargs; i++) {
        char *arg = args[i];
        if (one_of(arg, SEPARATE)) {
            if (!one_of(arg, OUTPUTS) && i + 1 < nargs) {
                argv[n++] = arg;
                argv[n++] = args[i + 1];
            }
            i++;
            continue;
        }
        if (arg[0] == '-' && arg[1] != '\0' && output(arg))
            continue;
        if (input < ninputs && at[input] == i) {
            if (input++ != self)
                continue;
        }
        argv[n++] = arg;
    }
    const char *tail[] = {"-M", "-MF", depfile, "-MT", "dependencies", "-H", "-fpch-preprocess"};
    for (size_t i = 0; i < sizeof tail / sizeof tail[0]; i++)
        argv[n++] = (char *)tail[i];
    if (clang)
        argv[n++] = "-Qunused-arguments";
    int pipefd[2];
    if (pipe(pipefd) != 0)
        fail("cannot make a pipe for a dependency pass", NULL);
    pid_t pid = fork();
    if (pid == 0) {
        int null = open("/dev/null", O_RDWR);
        if (null >= 0) {
            dup2(null, 0);
            dup2(null, 1);
        }
        dup2(pipefd[1], 2);
        close(pipefd[0]);
        close(pipefd[1]);
        setenv("LC_ALL", "C", 1);
        execv(real, argv);
        _exit(127);
    }
    close(pipefd[1]);
    Buf err = {0};
    put(&err, "", 0);
    char chunk[65536];
    ssize_t got;
    while ((got = read(pipefd[0], chunk, sizeof chunk)) > 0 || (got < 0 && errno == EINTR))
        if (got > 0)
            put(&err, chunk, (size_t)got);
    close(pipefd[0]);
    int status = 0;
    if (pid < 0)
        fail("cannot start a dependency pass of", args[at[self]]);
    while (waitpid(pid, &status, 0) < 0 && errno == EINTR)
        ;
    free(argv);
    /* the compiler's verdict: a failure on #error or #warning directives alone still lists every file it read */
    int said = 0, stops = 0;
    char first[300] = "";
    for (char *line = err.data; line != NULL && *line; ) {
        char *end = strchr(line, '\n'), *mark = NULL;
        if (end != NULL)
            *end = '\0';
        if ((mark = strstr(line, "error: ")) != NULL) {
            mark += strlen("error: ");
            said++;
            stops += !strncmp(mark, "#error", 6) || !strncmp(mark, "#warning", 8);
            if (!first[0])
                snprintf(first, sizeof first, "%s", mark);
        }
        if (end != NULL)
            *end = '\n';
        line = end != NULL ? end + 1 : NULL;
    }
    int ok = WIFEXITED(status) && WEXITSTATUS(status) == 0;
    if (!ok && !(WIFEXITED(status) && said > 0 && said == stops)) {
        if (first[0])
            snprintf(error, 400, "its dependency pass failed: %s", first);
        else
            snprintf(error, 400, "its dependency pass failed (%s %d)", WIFEXITED(status) ? "exit" : "signal",
                     WIFEXITED(status) ? WEXITSTATUS(status) : WTERMSIG(status));
        unlink(depfile);
        free(depfile);
        free(err.data);
        return;
    }
    size_t len = 0;
    char *rule = slurp(depfile, &len), **words = NULL;
    unlink(depfile);
    free(depfile);
    int count = rule != NULL ? prerequisites(rule, &words) : -1;
    List deps = {0};
    char *source = joined(cwd, args[at[self]], 1);
    if (count < 1) {
        snprintf(error, 400, "its dependency pass wrote no rule naming what it read");
    } else {
        char *main_file = joined(cwd, words[0], 1);
        if (strcmp(main_file, source) != 0)
            snprintf(error, 400, "its dependency rule names %.150s first, not the source", words[0]);
        free(main_file);
    }
    indexed(&deps, source);
    for (int i = 1; !error[0] && i < count; i++) {
        char *name = joined(cwd, words[i], 0), *resolved = realpath(name, NULL);
        if (resolved == NULL)
            snprintf(error, 400, "its dependency rule names %.250s, which is no file", words[i]);
        else
            indexed(&deps, resolved);
        free(resolved);
        free(name);
    }
    /* the tree: each line of -H is dots (its depth), a blank and the file's name; '!' or 'x' marks a precompiled
     * header the compiler tried, which the rule lists by its header */
    Buf tree = {0};
    put(&tree, "", 0);
    for (char *line = err.data; !error[0] && line != NULL && *line; ) {
        char *end = strchr(line, '\n');
        if (end != NULL)
            *end = '\0';
        size_t dots = strspn(line, ".");
        if (dots > 0 && line[dots] == ' ') {
            char *named = joined(cwd, line + dots + 1, 0), *resolved = realpath(named, NULL);
            int k = resolved != NULL ? find(&deps, resolved) : -1;
            free(named);
            if (k < 0) {
                snprintf(error, 400, "its include tree names %.250s, which its dependency rule does not",
                         line + dots + 1);
            } else {
                char item[48];
                snprintf(item, sizeof item, "%s[%zu, %d]", tree.len > 0 ? ", " : "", dots, k - 1);
                text(&tree, item);
            }
            free(resolved);
        }
        line = end != NULL ? end + 1 : NULL;
    }
    if (!error[0]) {
        Buf kept = {0};
        text(&kept, "{\"deps\": [");
        for (int i = 1; i < deps.count; i++) {
            text(&kept, i > 1 ? ", " : "");
            quoted(&kept, deps.path[i]);
        }
        text(&kept, "], \"tree\": [");
        text(&kept, tree.data);
        text(&kept, "]}");
        keep(capture, kept.data, kept.len, hex);
        free(kept.data);
    }
    for (int i = 0; i < deps.count; i++)
        free(deps.path[i]);
    free(deps.path);
    free(tree.data);
    free(words);
    free(rule);
    free(source);
    free(err.data);
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "ctrl_shim: usage: <recorder> <capture> <name> <real> <argument>...\n");
        return 2;
    }
    const char *capture = argv[1], *name = argv[2], *real = argv[3];
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
    int *input_at = calloc((size_t)nargs + 1, sizeof *input_at);
    if (exp == NULL || inputs == NULL || kept_real == NULL || input_at == NULL)
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
            input_at[ninputs] = at;
            inputs[ninputs++] = arg;
            exp[nexp++] = arg;
        } else if (arg[0] == '-' || arg[0] == '@') {
            exp[nexp++] = arg;
            reusable &= plain(arg);
        } else if (pch) {
            if (asprintf(&kept_real[nreal++], "%d=%s", ninputs, arg) < 0)
                fail("out of memory", NULL);
            exp[nexp++] = arg;
            input_at[ninputs] = at;
            inputs[ninputs++] = arg;
        } else {
            exp[nexp++] = stand_in(capture, ninputs, arg);
            input_at[ninputs] = at;
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
        char hex[65] = "", error[400] = "";
        if (!strcmp(lang, "c") || !strcmp(lang, "c++") || !strcmp(lang, "assembler"))
            dependencies(capture, real, args, nargs, input_at, ninputs, i, e.clang, cwd, hex, error);
        text(&r, i ? ", [" : "[");
        quoted(&r, full);
        text(&r, ", ");
        quoted(&r, lang);
        text(&r, ", ");
        quoted(&r, hex);
        text(&r, ", ");
        quoted(&r, error);
        text(&r, "]");
        free(full);
    }
    text(&r, "], \"output\": ");
    quoted(&r, output_path);
    text(&r, expanded ? ", \"expanded\": true, \"expansion\": " : ", \"expanded\": false, \"expansion\": ");
    quoted(&r, e.valid ? e.report : "");
    text(&r, ", \"expand_error\": ");
    quoted(&r, e.valid || !expanded ? e.error : "the capture's expansion helper wrote no entry it could read back");
    text(&r, ", \"from\": ");
    quoted(&r, getenv("CTRL_CAPTURE_FROM") ? getenv("CTRL_CAPTURE_FROM") : "");
    text(&r, ", \"run\": ");
    quoted(&r, getenv("CTRL_CAPTURE_RUN") ? getenv("CTRL_CAPTURE_RUN") : "");
    /* the compile itself, waited for: a signal the recorder takes is passed on to it, and its exit status (a signal's
     * as 128 and its number) is recorded with the invocation and is then the recorder's own */
    struct sigaction pass;
    memset(&pass, 0, sizeof pass);
    pass.sa_handler = pass_on;
    sigemptyset(&pass.sa_mask);
    for (size_t i = 0; i < sizeof PASSED / sizeof PASSED[0]; i++)
        sigaction(PASSED[i], &pass, NULL);
    argv[3] = (char *)real;
    pid_t pid = fork();
    if (pid == 0) {
        execv(real, argv + 3);
        perror("ctrl_shim: cannot run the compiler");
        _exit(127);
    }
    if (pid < 0)
        fail("cannot start the compiler", real);
    compiling = pid;
    int status = 0;
    while (waitpid(pid, &status, 0) < 0 && errno == EINTR)
        ;
    int rc = WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
    char closing[48];
    snprintf(closing, sizeof closing, ", \"rc\": %d}\n", rc);
    text(&r, closing);
    char *path = NULL;
    if (asprintf(&path, "%s/records.jsonl", capture) < 0)
        fail("out of memory", NULL);
    int fd = open(path, O_WRONLY | O_APPEND | O_CREAT, 0644);
    if (fd < 0 || write(fd, r.data, r.len) != (ssize_t)r.len || close(fd) != 0)
        fail("cannot append to", path);
    if (WIFSIGNALED(status)) {
        signal(WTERMSIG(status), SIG_DFL);
        raise(WTERMSIG(status));
    }
    return rc;
}
'''
