# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_shim.py - the recorder every compiler of a capture runs, and how a compiler's arguments read (#697).

THE RECORDER. ctrl_capture.py compiles RECORDER, with the real C compiler,
into the capture's bin/, and puts a wrapper there for every compiler name
(gcc, g++, cc, c++, clang, clang++, cpp, the RV32 compiler and their prefixed
and versioned names) that runs

    <recorder> <capture> <name> <real compiler> <argument>...

It appends one record to <capture>/records.jsonl and then executes the real
compiler with the same arguments, so what it compiles and writes is what it
would have without the capture. A record holds the name the compiler was
called by, the real compiler, the arguments, the working directory, every
source with its language as parse() reads it (and, for C++, the digest of its
text), the files it reads first (-include, -imacros) as the compiler finds
them, the builder files on the Python stack of the process that started it
(CTRL_CAPTURE_FROM, set by ctrl_capture's audit hook), the builder file of the
command the capture ran it under (CTRL_CAPTURE_RUN, set by ctrl_capture.run),
and the digest of the map of texts kept beside it. The text of every C++
source, of a file a C++ compile reads first outside the checkout, and of every
header outside the checkout a C++ source reaches in a builder's own
directories (the temporary directory, the compile's, the source's) by its
#include lines read as text in every branch, is kept under <capture>/text/ by
its SHA-256, so a source a builder writes and deletes is still read. It is C
so that a compile costs the capture about a millisecond.

A record that cannot be written stops the compile (exit 2, the reason on
standard error): a capture never misses an invocation silently.

THE ARGUMENTS. parse() reads an invocation's arguments as the recorder does:
the capture's reader takes the -D and -U flags and the directories searched
from it.
"""

from __future__ import annotations

import re

#: Options whose value is the next argument (GCC's and Clang's drivers), when not joined to it.
SEPARATE = frozenset("""-o -x -I -D -U -include -imacros -isystem -iquote -idirafter -iprefix -iwithprefix
    -iwithprefixbefore -isysroot --sysroot -MF -MT -MQ -L -l -T -Xlinker -Xassembler -Xpreprocessor -Xclang
    -aux-info -dumpbase -dumpdir -wrapper -arch -target --target -e -u -z --param -A -B -G -imultilib
    -iframework""".split())
#: The options that name a directory searched for headers, and those that name a file read first.
DIRS = ("-I", "-iquote", "-isystem", "-idirafter")
FORCED = ("-include", "-imacros")
#: A source's language from its suffix, as the driver reads it.
SUFFIX = {".c": "c", ".i": "c", ".h": "c", ".cc": "c++", ".cp": "c++", ".cxx": "c++", ".cpp": "c++",
          ".CPP": "c++", ".c++": "c++", ".C": "c++", ".ii": "c++", ".hh": "c++", ".hpp": "c++", ".hxx": "c++",
          ".H": "c++", ".tcc": "c++", ".s": "assembler", ".S": "assembler", ".sx": "assembler"}
#: The -x languages that are C or C++.
LANGUAGES = {"c": "c", "c-header": "c", "cpp-output": "c", "c++": "c++", "c++-header": "c++",
             "c++-cpp-output": "c++", "objective-c": "c", "objective-c++": "c++"}
#: A driver that compiles a C source as C++.
CXX_DRIVER = re.compile(r"(?:^|[-/])(?:g\+\+|c\+\+|clang\+\+)(?:-[\d.]+)?$")


def parse(name: str, args: list[str]) -> dict:
    """What one invocation's arguments say: each source with its language (C or C++ only; anything else is
    `other`), its -D and -U flags in order (joined), the directories it searches, the files it reads first.
    RECORDER reads them alike."""
    sources, flags, dirs, forced = [], [], [], []
    language = None
    cxx = bool(CXX_DRIVER.search(name))
    at = 0
    while at < len(args):
        arg = args[at]
        value = args[at + 1] if at + 1 < len(args) else ""
        if arg in SEPARATE:
            if arg in ("-D", "-U"):
                flags.append(arg + value)
            elif arg in DIRS:
                dirs.append([arg, value])
            elif arg in FORCED:
                forced.append(value)
            elif arg == "-x":
                language = None if value == "none" else value
            at += 2
            continue
        if arg.startswith(("-D", "-U")):
            flags.append(arg)
        elif arg.startswith(DIRS):
            option = next(o for o in sorted(DIRS, key=len, reverse=True) if arg.startswith(o))
            dirs.append([option, arg[len(option):]])
        elif arg.startswith("-x") and len(arg) > 2:
            language = None if arg[2:] == "none" else arg[2:]
        elif arg == "-" or not arg.startswith("-"):
            name = arg.rpartition("/")[2]
            suffix = name[name.rfind("."):] if name.rfind(".") > 0 else ""
            lang = LANGUAGES.get(language, "other") if language else SUFFIX.get(suffix, "other")
            if cxx and lang == "c" and not language and suffix != ".i":
                lang = "c++"
            sources.append([arg, lang])
        at += 1
    return {"sources": sources, "flags": flags, "dirs": dirs, "forced": forced}


#: The recorder (see THE RECORDER), C11 and POSIX.
RECORDER = r'''/* ctrl_shim.py's recorder (#697): <recorder> <capture> <name> <real> <argument>... */
#define _GNU_SOURCE
#include <fcntl.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define CLOSURE 256 /* how many headers one compile keeps beside its sources */

typedef struct { char *data; size_t len, cap; } Buf;
typedef struct { char *path; char hex[65]; } Kept;
typedef struct { Kept items[CLOSURE + 64]; int count; } Map;

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
    if (has(m, path) || m->count >= (int)(sizeof m->items / sizeof m->items[0]))
        return;
    m->items[m->count].path = strdup(path);
    keep(capture, data, len, m->items[m->count].hex);
    m->count++;
}

/* ---- the arguments, as ctrl_shim.parse reads them ---- */

static const char *const SEPARATE[] = {"-o", "-x", "-I", "-D", "-U", "-include", "-imacros", "-isystem",
    "-iquote", "-idirafter", "-iprefix", "-iwithprefix", "-iwithprefixbefore", "-isysroot", "--sysroot", "-MF",
    "-MT", "-MQ", "-L", "-l", "-T", "-Xlinker", "-Xassembler", "-Xpreprocessor", "-Xclang", "-aux-info",
    "-dumpbase", "-dumpdir", "-wrapper", "-arch", "-target", "--target", "-e", "-u", "-z", "--param", "-A", "-B",
    "-G", "-imultilib", "-iframework", NULL};
static const char *const DIRS[] = {"-idirafter", "-isystem", "-iquote", "-I", NULL}; /* longest first */
static const char *const CXX_SUFFIXES[] = {".cc", ".cp", ".cxx", ".cpp", ".CPP", ".c++", ".C", ".ii", ".hh",
                                           ".hpp", ".hxx", ".H", ".tcc", NULL};
static const char *const ASM_SUFFIXES[] = {".s", ".S", ".sx", NULL};

static int one_of(const char *s, const char *const *list)
{
    for (int i = 0; list[i] != NULL; i++)
        if (strcmp(s, list[i]) == 0)
            return 1;
    return 0;
}

/* A C++ driver's name: g++, c++ or clang++, after a start, a '-' or a '/', and before an optional -<version>. */
static int cxx_driver(const char *name)
{
    static const char *const drivers[] = {"clang++", "g++", "c++", NULL};
    for (const char *p = name; *p; p++) {
        if (p != name && p[-1] != '-' && p[-1] != '/')
            continue;
        for (int i = 0; drivers[i] != NULL; i++) {
            size_t n = strlen(drivers[i]);
            if (strncmp(p, drivers[i], n) != 0)
                continue;
            const char *q = p + n;
            if (*q == '\0')
                return 1;
            if (*q == '-' && q[1] != '\0' && strspn(q + 1, "0123456789.") == strlen(q + 1))
                return 1;
        }
    }
    return 0;
}

/* A path's suffix, as parse() reads it: from the last '.' of its last part, unless that '.' begins it. */
static const char *suffix_of(const char *path)
{
    const char *base = strrchr(path, '/');
    base = base ? base + 1 : path;
    const char *dot = strrchr(base, '.');
    return dot != NULL && dot != base ? dot : "";
}

static const char *language(const char *given, const char *arg, int cxx)
{
    if (given != NULL) {
        if (!strcmp(given, "c") || !strcmp(given, "c-header") || !strcmp(given, "cpp-output") ||
            !strcmp(given, "objective-c"))
            return "c";
        if (!strcmp(given, "c++") || !strcmp(given, "c++-header") || !strcmp(given, "c++-cpp-output") ||
            !strcmp(given, "objective-c++"))
            return "c++";
        return "other";
    }
    const char *s = suffix_of(arg);
    if (one_of(s, CXX_SUFFIXES))
        return "c++";
    if (!strcmp(s, ".c") || !strcmp(s, ".h"))
        return cxx ? "c++" : "c";
    if (!strcmp(s, ".i"))
        return "c";
    return one_of(s, ASM_SUFFIXES) ? "assembler" : "other";
}

/* ---- the headers a C++ source reaches outside the checkout ---- */

static int outside_root(const char *path, const char *root) { return !under(path, root); }

static void closure(Map *kept, const char *capture, const char *root, char *const *tops, int ntops,
                    const char *source, char *data, size_t len, char **dirs, int ndirs)
{
    char *queue_path[CLOSURE + 8];
    char *queue_data[CLOSURE + 8];
    size_t queue_len[CLOSURE + 8];
    int queued = 0;
    queue_path[queued] = strdup(source);
    queue_data[queued] = data;
    queue_len[queued++] = len;
    while (queued > 0 && kept->count < CLOSURE) {
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
                                if (queued < CLOSURE + 8) {
                                    queue_path[queued] = hit;
                                    queue_data[queued] = hit_data;
                                    queue_len[queued++] = hit_len;
                                } else {
                                    free(hit);
                                    free(hit_data);
                                }
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
    int nargs = argc - 4, cxx = cxx_driver(name);
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof cwd) == NULL)
        fail("cannot read the working directory", NULL);
    char **dirs = calloc((size_t)nargs + 1, sizeof *dirs), **forced = calloc((size_t)nargs + 1, sizeof *forced);
    char **sources = calloc((size_t)nargs + 1, sizeof *sources);
    const char **langs = calloc((size_t)nargs + 1, sizeof *langs);
    int ndirs = 0, nforced = 0, nsources = 0;
    if (dirs == NULL || forced == NULL || sources == NULL || langs == NULL)
        fail("out of memory", NULL);
    const char *given = NULL;
    for (int at = 0; at < nargs; at++) {
        const char *arg = args[at], *value = at + 1 < nargs ? args[at + 1] : "";
        if (one_of(arg, SEPARATE)) {
            if (one_of(arg, DIRS))
                dirs[ndirs++] = joined(cwd, value, 1);
            else if (!strcmp(arg, "-include") || !strcmp(arg, "-imacros"))
                forced[nforced++] = (char *)value;
            else if (!strcmp(arg, "-x"))
                given = strcmp(value, "none") ? value : NULL;
            at++;
            continue;
        }
        if (!strncmp(arg, "-D", 2) || !strncmp(arg, "-U", 2))
            continue;
        int dir = 0;
        for (int k = 0; DIRS[k] != NULL && !dir; k++)
            if (!strncmp(arg, DIRS[k], strlen(DIRS[k]))) {
                dirs[ndirs++] = joined(cwd, arg + strlen(DIRS[k]), 1);
                dir = 1;
            }
        if (dir)
            continue;
        if (!strncmp(arg, "-x", 2) && arg[2] != '\0') {
            given = strcmp(arg + 2, "none") ? arg + 2 : NULL;
            continue;
        }
        if (!strcmp(arg, "-") || arg[0] != '-') {
            sources[nsources] = (char *)arg;
            langs[nsources++] = language(given, arg, cxx);
        }
    }
    char *temp = realpath(getenv("TMPDIR") && *getenv("TMPDIR") ? getenv("TMPDIR") : "/tmp", NULL);
    char *here = realpath(cwd, NULL);
    Map kept = {0};
    Buf r = {0};
    int any_cxx = 0;
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
    for (int i = 0; i < nsources; i++) {
        char *full = strcmp(sources[i], "-") ? joined(cwd, sources[i], 1) : strdup("-");
        char hex[65] = "";
        size_t len = 0;
        char *data = NULL;
        if (!strcmp(langs[i], "c++")) {
            any_cxx = 1;
            if (strcmp(full, "-") && regular(full) && (data = slurp(full, &len)) != NULL) {
                keep(capture, data, len, hex);
                char *dir = strdup(full), *slash = strrchr(dir, '/');
                if (slash != NULL)
                    *slash = '\0';
                char *tops[3] = {temp ? temp : "/tmp", here ? here : cwd, dir};
                closure(&kept, capture, root, tops, 3, full, data, len, dirs, ndirs);
                free(dir);
                free(data);
            }
        }
        text(&r, i ? ", [" : "[");
        quoted(&r, full);
        text(&r, ", ");
        quoted(&r, langs[i]);
        text(&r, ", ");
        quoted(&r, hex);
        text(&r, "]");
        free(full);
    }
    text(&r, "], \"forced\": [");
    for (int i = 0; i < nforced; i++) {
        char *full = NULL;
        for (int b = -1; b < ndirs && full == NULL; b++) {
            char *hit = joined(b < 0 ? cwd : dirs[b], forced[i], 1);
            if (regular(hit))
                full = hit;
            else
                free(hit);
        }
        if (full == NULL)
            full = joined(cwd, forced[i], 1);
        size_t len = 0;
        char *data = NULL;
        if (any_cxx && regular(full) && outside_root(full, root) && (data = slurp(full, &len)) != NULL) {
            add(&kept, capture, full, data, len);
            free(data);
        }
        text(&r, i ? ", " : "");
        quoted(&r, full);
        free(full);
    }
    text(&r, "], \"kept\": ");
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
