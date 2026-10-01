#!/bin/sh
# Disposable mutants of the published b6_thdn.py; each must make `controls` exit non-zero.
# usage: mutate_controls.sh <dir holding b6_tone.py and b6_thdn.py> <work dir>
set -u
src=$1; work=$2
run() {  # name, python expression applied to the source text
  d="$work/$1"; mkdir -p "$d"; cp "$src/b6_tone.py" "$d/"
  python3 -c "import sys; s=open('$src/b6_thdn.py').read(); t=$2; assert t!=s, 'mutation did not apply'; open('$d/b6_thdn.py','w').write(t)" || { echo "$1 NOT-APPLIED"; return; }
  ( cd "$d" && timeout 900 python3 b6_thdn.py controls out.json > log.txt 2>&1 ); rc=$?
  if [ $rc -ne 0 ]; then echo "$1 KILLED (controls rc $rc; $(grep -c '"pass": false' "$d/out.json" 2>/dev/null) failing case(s))"; else echo "$1 SURVIVED"; fi
}
run sign_flip        "s.replace('kind=\"skip\" if e[j] > 0 else \"repeat\"', 'kind=\"repeat\" if e[j] > 0 else \"skip\"')"
run size_off_by_one  "s.replace('frames=int(abs(e[j]))', 'frames=int(abs(e[j])) + 1')"
run event_frame_late "s.replace('ev.append(dict(frame=int(idx[j + 1])', 'ev.append(dict(frame=int(idx[j + 1]) + 1')"
run no_freq_refine   "s.replace('def sine_fit(x, f0, iters=6):', 'def sine_fit(x, f0, iters=0):')"
run band_one_sided   "s.replace('w = np.where((f[m] == 0) | (f[m] == FS / 2), 1.0, 2.0)', 'w = np.ones_like(f[m])')"
run drop_repeats     "s.replace('for j in np.flatnonzero(e != 0):', 'for j in np.flatnonzero(e > 0):')"
run block_count_off  "s.replace('ne = int(((ev_frames >= a + 1) & (ev_frames < b)).sum())', 'ne = 0')"
run decode_one_word  "s.replace('ordn = T.decode(c0, c1, tab)', 'ordn = T.decode(c0, c0, tab)')"
