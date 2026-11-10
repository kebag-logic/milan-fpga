#!/bin/sh
# usage: refusal_probe.sh TREE WORK -- the build-time refusal at src/acmp.c:35 with gcc and clang-18 (C11, -Werror):
# the head as committed at several sink counts, then three narrowed masks planted into include/acmp.h.
TREE=$1 W=$2
. "$(dirname "$0")/../env.sh"
mkdir -p "$W"
cc1() { "$1" -std=c11 -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT -DACMP_MAX_SINKS=$2u -I"$3/include" -c "$3/src/acmp.c" -o /dev/null > "$W/out.txt" 2>&1; r=$?
  printf '%-44s %-8s N=%-4s rc=%s %s\n' "$4" "$1" "$2" "$r" "$(grep -o 'static assert[^"]*"[^"]*"' "$W/out.txt" | head -1)"; }
for cc in gcc clang-18; do for n in 1 16 31 32 33 64 65 254 255; do cc1 $cc $n "$TREE" head-as-committed; done; done
plant() { rm -rf "$W/$1"; mkdir -p "$W/$1"; cp -r "$TREE/include" "$TREE/src" "$W/$1/"; python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();assert s.count(sys.argv[2])==1;open(p,'w').write(s.replace(sys.argv[2],sys.argv[3]))" "$W/$1/include/acmp.h" "$2" "$3"; }
plant one-word 'uint32_t release[ACMP_RELEASE_WORDS];' 'uint32_t release[1];'
plant floor-words '((ACMP_MAX_SINKS + 31u) / 32u)' '(ACMP_MAX_SINKS / 32u + 0u * 31u)'
plant u16-words 'uint32_t release[ACMP_RELEASE_WORDS];' 'uint16_t release[ACMP_RELEASE_WORDS];'
for cc in gcc clang-18; do for p in one-word floor-words u16-words; do for n in 16 32 33 64; do cc1 $cc $n "$W/$p" "plant $p"; done; done; done
