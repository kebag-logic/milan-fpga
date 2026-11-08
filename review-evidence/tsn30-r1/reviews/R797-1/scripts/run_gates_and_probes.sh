#!/usr/bin/env bash
# Gate runs and disposable mutation/fault probes for tsn-c-stack PR #30.
# Usage: run_gates_and_probes.sh <review-clone> <packet-dir> [clang-18 path]
# Every tree it touches is a fresh local clone under <packet-dir>/scratch.
set -u
SRC=$1; PKT=$2; CLANG=${3:-clang-18}
HEAD_ID=0cfa8423cbdde8ed6b679a022afa6401f6d62899
MAIN_ID=d7e6a2a19a57a8277cd26042557a8c99f2ee5496
SCR=$PKT/scratch/runs; OUT=$PKT/receipts
rm -rf "$SCR"; mkdir -p "$SCR" "$OUT"
LOG=$OUT/gates-and-probes.log; : > "$LOG"
say() { printf '%s\n' "$*" | tee -a "$LOG"; }
clone_at() { git clone -q --no-hardlinks "$SRC" "$1" && git -C "$1" checkout -q --detach "$2"; }
run() { local dir=$1; shift; say "\$ (cd $(basename "$dir") && $*)"; (cd "$dir" && "$@") >>"$LOG" 2>&1; local rc=$?; say "rc=$rc"; return 0; }

say "== identity"
say "head=$(git -C "$SRC" rev-parse HEAD) tree=$(git -C "$SRC" rev-parse HEAD^{tree})"
say "python=$(python3 --version 2>&1) git=$(git --version)"
say "clang=$("$CLANG" --version | head -1)"

say "== gates at exact head"
clone_at "$SCR/head" "$HEAD_ID"
run "$SCR/head" python3 -I scripts/check_privacy.py --selftest
run "$SCR/head" python3 -I scripts/check_privacy.py
run "$SCR/head" python3 -I scripts/check_license.py --selftest
run "$SCR/head" python3 -I scripts/check_license.py
run "$SCR/head" env TSN_CLANG="$CLANG" python3 -I scripts/check_comments.py
run "$SCR/head" env TSN_CLANG="$CLANG" python3 -I scripts/check_comments.py --selftest --work "$SCR/head/build-comment-controls"

say "== main (d7e6a2a1) without the change"
clone_at "$SCR/main" "$MAIN_ID"
run "$SCR/main" python3 -I scripts/check_privacy.py --selftest
run "$SCR/main" python3 -I scripts/check_privacy.py

say "== delta scope"
run "$SRC" git diff --stat "$MAIN_ID" "$HEAD_ID"
run "$SRC" git diff --raw "$MAIN_ID" "$HEAD_ID"
run "$SRC" git show -s --format='%H%n%an <%ae>%n%cn <%ce>%n%P%n%B' "$MAIN_ID"
run "$SRC" git show -s --format='%H%n%an <%ae>%n%cn <%ce>%n%P%n%B' "$HEAD_ID"

# Each probe edits scripts/check_privacy.py in its own clone with python, then runs the gate.
probe() {
  local name=$1 code=$2; shift 2
  local dir=$SCR/probe-$name
  clone_at "$dir" "$HEAD_ID"
  say "== probe $name"
  python3 -I - "$dir/scripts/check_privacy.py" "$code" <<'EOF' >>"$LOG" 2>&1
import sys
path, code = sys.argv[1], sys.argv[2]
text = open(path).read()
old, new = code.split("|||")
assert text.count(old) == 1, ("anchor not unique", old)
open(path, "w").write(text.replace(old, new))
print("applied:", repr(old), "->", repr(new))
EOF
  run "$dir" git diff --stat
  run "$dir" python3 -I scripts/check_privacy.py --selftest
  run "$dir" python3 -I scripts/check_privacy.py
}

probe M1-drop-exemption 'and commit not in TWO_LINE_MERGES and len|||and len'
probe M2-exempt-identity-too 'if commit != OWNER_SQUASH and not identity_ok|||if commit != OWNER_SQUASH and commit not in TWO_LINE_MERGES and not identity_ok'
probe M3-exempt-every-commit 'and commit not in TWO_LINE_MERGES and len|||and False and len'
probe M4-prefix-match 'and commit not in TWO_LINE_MERGES and len|||and commit[:8] not in {c[:8] for c in TWO_LINE_MERGES} and len'
probe M5-controls-use-other-id '        commit = next(iter(TWO_LINE_MERGES)) if name.startswith("two-line-merge") else commit
|||'
probe M6-skip-scan-for-exempt '        errors += scan(commit, data)|||        errors += [] if commit in TWO_LINE_MERGES else scan(commit, data)'
probe P1-scan-reaches-exempt-body 'PATTERNS += [re.compile(r"gh[pousr]|||PATTERNS += [re.compile("no 64-bit shift per byte")]
PATTERNS += [re.compile(r"gh[pousr]'
probe P2-identity-reaches-exempt 'WEB_FLOW = ["hackerman-kl <161579364+Mister-M-alt@users.noreply.github.com>", "GitHub <noreply@github.com>"]|||WEB_FLOW = ["hackerman-kl <161579364+Mister-M-alt@users.noreply.github.com>", "GitHub <other@github.com>"]'

say "== direct boundary calls on the head gate"
python3 -I - "$SCR/head/scripts" <<'EOF' >>"$LOG" 2>&1
import sys
sys.path.insert(0, sys.argv[1])
import check_privacy as g
exempt = next(iter(g.TWO_LINE_MERGES))
flip = exempt[:-1] + ("7" if exempt[-1] != "7" else "8")
body = g.WEB_FLOW + ["Merge (#29)", "", "Body"]
cases = [
    ("exempt id, web-flow, two lines", exempt, body),
    ("exempt id, holder pair, two lines", exempt, [g.IDENTITY, g.IDENTITY, "Merge (#29)", "", "Body"]),
    ("exempt id, reversed web-flow, two lines", exempt, [g.WEB_FLOW[1], g.WEB_FLOW[0], "Merge", "", "Body"]),
    ("exempt id, empty message", exempt, g.WEB_FLOW + []),
    ("abbreviated id d7e6a2a1", "d7e6a2a1", body),
    ("upper-case exempt id", exempt.upper(), body),
    ("last digit changed", flip, body),
    ("exempt id with trailing newline", exempt + "\n", body),
    ("zero id", "0" * 40, body),
    ("parent 70936b77 of the merge", "70936b77dc41981e192438388cd0aced69954f18", body),
    ("owner squash, foreign, two lines", g.OWNER_SQUASH, ["x <x@y.z>", "x <x@y.z>", "S", "", "B"]),
]
print("TWO_LINE_MERGES =", sorted(g.TWO_LINE_MERGES), "OWNER_SQUASH =", g.OWNER_SQUASH)
for label, commit, lines in cases:
    print(f"{label}: {g.commit_errors(commit, lines)}")
EOF
say "rc=$?"
say "== done"
