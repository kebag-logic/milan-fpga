# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Allocator selection for this directory's Yosys flows, sourced by run.sh
# (portability) and ooc.sh (area). It defines functions and sets one variable
# (TRUE_BIN); it starts nothing and changes no directory, so a caller may
# source it before or after its own `cd`.
#
# It is NOT sourced on run.sh's `--list` path. syn/yosys/check_list_hermetic.sh
# proves `--list` reads nothing but run.sh and scripts/yosys_shards.py, in a
# tree built to hold only those two files (#190), and an unconditional source
# here would break that contract rather than the other way round.
#
# RULE 13'S STRICT-MODE RATCHET IS DECLINED HERE, all three of it, and this
# comment is the record rather than an assumption a later reader has to
# reconstruct. `set -euo pipefail` in a SOURCED fragment does not configure
# this file; it reconfigures the CALLER's shell, from the line the caller
# sourced it on to the end of that script, which is a shell option neither
# caller asked for and no reader of run.sh or ooc.sh would find here. The
# concrete failure: run.sh sources this at its line 109 and then counts a
# failing top rather than dying on it, so an errexit switched on from inside
# this file turns its per-top `( ... yosys ... ) > log` sweep into an abort on
# the first red top, and its report into a crash; `pipefail` would likewise
# change the meaning of the `grep -oE 'ERROR:.*' | head -1` that produces the
# reason column. The trio belongs to whoever owns the shell, so both callers
# set it themselves, and this file is written to be correct under it: every
# `a && b && { c; }` here sits where errexit exempts it, no loop body ends on
# a bare failing test, and `select_malloc` returns 0 with an empty answer on
# the machine with no jemalloc - the documented default, and the one arm that
# would otherwise take the whole gate down with it.

# THESE FLOWS ARE ALLOCATION-BOUND, NOT PARSE-BOUND (#286, #288). On the heaviest
# top Yosys spends about three quarters of its time in the `opt*` family and
# 0.5% in `read_verilog`, and a large share of that is glibc's allocator:
# preloading jemalloc takes milan_datapath from 656 s to 361 s and the whole
# eight-way sharded gate from 616 s to 358 s, on the same machine, with all 46
# tops still passing.
#
# It is a SPEED knob and never a correctness one: `write_rtlil` after this
# script's own program is BYTE-IDENTICAL under glibc, tcmalloc, jemalloc and
# mimalloc (#286). So it is optional in both directions - the documented tool
# requirement stays "yosys and sv2v on PATH" (README "Tooling") and a machine
# without jemalloc runs exactly as it did before, with no warning to silence.
#
#   YOSYS_MALLOC=<path>   preload that library
#   YOSYS_MALLOC=none     run yosys under the system allocator
#   unset                 use jemalloc when it is installed
#
# A NAMED library that is absent REFUSES rather than falling back. Falling back
# would let a run that was asked to reproduce one allocator quietly report
# another one's timing, which is the measurement defect this whole lane exists
# to remove.
ldconfig_path() {
  local p
  for p in ldconfig /usr/sbin/ldconfig /sbin/ldconfig; do
    command -v "$p" >/dev/null 2>&1 && { printf '%s\n' "$p"; return 0; }
  done
  return 1
}

# EVERY PATH IS MADE ABSOLUTE BEFORE IT IS BELIEVED. yosys runs after `cd
# "$TMP"`, so a relative LD_PRELOAD the caller checked from their own directory
# resolves against $TMP instead, where it is not there: the loader drops it and
# the header line reports an allocator that never ran.
abs_path() {
  local p="$1" out d b
  if out="$(readlink -f -- "$p" 2>/dev/null)" && [ -n "$out" ]; then
    printf '%s\n' "$out"
    return 0
  fi
  d="$(cd -- "$(dirname -- "$p")" 2>/dev/null && pwd)" || return 1
  b="$(basename -- "$p")"
  printf '%s/%s\n' "$d" "$b"
}

# EXISTING IS NOT LOADABLE. The loader takes an unusable LD_PRELOAD by IGNORING
# it: the process still exits 0 and the complaint goes to stderr, which for a
# yosys child lands in that top's log and is never read - so `/etc/hosts` was
# accepted, the gate passed, and the header named it. The test is therefore
# "stderr stayed empty", never "the command succeeded".
TRUE_BIN="$(type -P true 2>/dev/null || printf '')"
preload_is_usable() {
  local lib="$1" err
  [ -n "$TRUE_BIN" ] && [ -x "$TRUE_BIN" ] || return 1
  err="$(LD_PRELOAD="$lib" "$TRUE_BIN" 2>&1 >/dev/null)" || return 1
  [ -z "$err" ]
}
preload_refusal() {
  [ -n "$TRUE_BIN" ] && [ -x "$TRUE_BIN" ] || { printf 'no external true(1) to probe with\n'; return 0; }
  LD_PRELOAD="$1" "$TRUE_BIN" 2>&1 >/dev/null | head -1
}

select_malloc() {
  local want="${YOSYS_MALLOC-}" cand lc abs
  case "$want" in
    none) return 0 ;;
    "")   ;;
    *)    # Existence is checked BEFORE canonicalisation so a relative request
          # is judged against the caller's directory, which is where they meant
          # it, and so the message says what is actually wrong.
          [ -e "$want" ] || {
            echo "YOSYS_MALLOC=$want: no such file" >&2
            return 2
          }
          abs="$(abs_path "$want")" || {
            echo "YOSYS_MALLOC=$want: cannot be resolved to an absolute path" >&2
            return 2
          }
          preload_is_usable "$abs" || {
            echo "YOSYS_MALLOC=$want: the loader will not preload it ($abs)" >&2
            echo "  $(preload_refusal "$abs")" >&2
            return 2
          }
          printf '%s\n' "$abs"
          return 0 ;;
  esac
  # ldconfig answers for the loader's own search path, which is the only
  # authority on where a distribution put the library - multiarch layouts
  # included, which is why no such path is spelled below. The literal list is
  # only the fallback for a machine whose ldconfig a normal user cannot run,
  # and an empty answer is a valid one: the gate then runs unchanged.
  # A candidate that the loader will not take is SKIPPED here rather than
  # refused: the documented default is "use jemalloc when it is installed", and
  # a broken one is simply not installed. An explicit request is refused above,
  # because there the caller named it and is owed an answer.
  if lc="$(ldconfig_path)"; then
    while IFS= read -r cand; do
      [ -e "$cand" ] && preload_is_usable "$cand" && { printf '%s\n' "$cand"; return 0; }
    done < <("$lc" -p 2>/dev/null | sed -n 's/^.* => //p' | grep -F libjemalloc.so.2)
  fi
  for cand in /usr/lib/libjemalloc.so.2 /usr/lib64/libjemalloc.so.2 \
              /usr/local/lib/libjemalloc.so.2; do
    [ -e "$cand" ] && preload_is_usable "$cand" && { printf '%s\n' "$cand"; return 0; }
  done
  return 0
}

# THE ONLY PLACE that decides what a yosys child sees, so the self-test below
# exercises the same code the gate runs. An EMPTY selection must actively UNSET
# LD_PRELOAD rather than merely decline to set it: a caller who already exported
# one would otherwise have it inherited while the header line said "system",
# which is the same silent misattribution the refusal above exists to prevent -
# and it would invalidate any with-versus-without comparison run in that shell.
apply_malloc_env() {
  local lib="${1-}"
  if [ -n "$lib" ]; then
    export LD_PRELOAD="$lib"
  else
    unset LD_PRELOAD
  fi
}

# The interesting case is the machine WITHOUT jemalloc, because that is the one
# the documented tool requirement covers and the one nobody runs by accident.
# This self-test needs neither jemalloc, nor yosys, nor sv2v, nor a submodule.
selftest_alloc() {
  local rc=0 skipped=0 out probe found dir base

  out="$(YOSYS_MALLOC=none select_malloc)" || rc=1
  [ -z "$out" ] || { echo "selftest: YOSYS_MALLOC=none selected '$out'" >&2; rc=1; }

  # An EXISTING file the loader will not take must be refused, not reported as
  # the allocator in effect. An empty temp file is exactly that case.
  probe="$(mktemp)"
  if out="$(YOSYS_MALLOC="$probe" select_malloc 2>/dev/null)"; then
    echo "selftest: an unloadable YOSYS_MALLOC was accepted as '$out'" >&2; rc=1
  fi
  if out="$(YOSYS_MALLOC="$probe.absent" select_malloc 2>/dev/null)"; then
    echo "selftest: a missing YOSYS_MALLOC was accepted as '$out'" >&2; rc=1
  fi
  rm -f "$probe"

  # The default never names something the loader would drop.
  found="$(unset YOSYS_MALLOC; select_malloc)" || rc=1
  if [ -n "$found" ]; then
    { [ -e "$found" ] && preload_is_usable "$found"; } || {
      echo "selftest: the default selected an unusable '$found'" >&2; rc=1
    }
    # A RELATIVE request must come back absolute, because yosys runs from $TMP.
    dir="$(dirname -- "$found")"; base="$(basename -- "$found")"
    out="$(cd "$dir" && YOSYS_MALLOC="./$base" select_malloc)" || rc=1
    [ "$out" = "$found" ] || {
      echo "selftest: relative path resolved to '$out', expected '$found'" >&2; rc=1
    }
  else
    echo "selftest: SKIPPED the relative-path and usable-default arms" \
         "(no preloadable jemalloc on this machine)"
    skipped=1
  fi

  # The child environment, through the same function the per-top run uses.
  out="$(export LD_PRELOAD=/inherited/from/the/caller.so
         apply_malloc_env ""; printf '%s' "${LD_PRELOAD-<unset>}")"
  [ "$out" = "<unset>" ] || {
    echo "selftest: an inherited LD_PRELOAD survived an empty selection as '$out'" >&2; rc=1
  }
  out="$(unset LD_PRELOAD; apply_malloc_env /x/y.so; printf '%s' "${LD_PRELOAD-<unset>}")"
  [ "$out" = "/x/y.so" ] || {
    echo "selftest: a selected library did not reach the child env ('$out')" >&2; rc=1
  }

  [ "$rc" -eq 0 ] && echo "allocator selection self-test: PASS$([ "$skipped" -eq 1 ] && echo ' (with skips)')"
  return "$rc"
}

