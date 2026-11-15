#!/usr/bin/env python3
"""Scrub host paths from round 9's receipts, then write receipts/INDEX.md from the files present (lane 895 round 9):
each file's size and sha256, grouped by directory, with what each directory holds. The index is written after the
scrub, and then checked: a second scrub changes no file, and every listed hash is the file's bytes. Refuses a receipt
over 200 KB."""
import hashlib
import sys
from pathlib import Path

R = Path('$MANAGEMENT/2026-09-23/895-a775/round9/receipts')
SUBS = [('/data-2/milan/tmp/895-a775/r9', '<scratch>'), ('/data-2/milan/tmp/895-a775', '<scratch>'),
        ('$LANES/895-talker', '<tree>'), ('$MANAGEMENT', '<mgmt>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE/scratch', '<tools>'), ('$WORKSPACE_HOME/litex-milan', '<litex>'),
        ('$WORKSPACE_HOME/br-milan-rv32', '<sdk>'), ('$LANES', '<lanes>'), ('$VALIDATION_STORAGE', '<data>'),
        ('/data-2/milan', '<data2>'), ('$WORKSPACE_HOME', '<home>')]
WHAT = {
    'identity': "image_sha.py: sha256 of each ELF's loadable bytes and every linked object of every image ledger.sh "
                "links, at round 8's 73388996 (the legs' image), the sync merge 663b519b, 449d29d2 (THE TRANSMIT's "
                "figure) and the final head 056d619d; compare_images.py between each, with the objdump -d / -s lines "
                "of every differing file (12 two-interface files, one instruction each)",
    'ledger-merge': "the ROM ledger at the sync merge 663b519b (ledger.sh on its clean clone): plat_ledger.py at every "
                    "point (rc 1: 8x8/1if's ctrl_plat 18,240 B against the recorded 18,176), the fixture and the two "
                    "8x8/2if harness arms",
    'ledger-head': "the ROM ledger at 449d29d2 (the record fixed): plat_ledger.py rc 0",
    'ledger-final': "the ROM ledger at the final head 056d619d: plat_ledger.py rc 0",
    'arms': "the firmware suite's Talker arms (talker: srp_talker.cpp at 1x1/1if and 8x8/2if, SrpGate at 8x8/2if) and "
            "srp-acmp-if2 on a clean clone of 449d29d2 (arms.py)",
    'legs': "the CPU budget harness's 8x8/2if valid-destinations leg R9-W8 on a clean clone of 449d29d2, its summary "
            "beside round 8's R8-W8 (legs_summary.py), and its results file by file against R8-W8's",
    'graders': "per-pass-threshold.txt (per_pass_threshold.py on an export of 449d29d2: every 1x1/1if row's margin and "
               "the per-pass cost at which the last queued notice passes 140 ms); g-item1 = the worktree at item 1 "
               "before its commit; precheck = every check_*.py the workflows name, on the worktree at c772b1e5; "
               "g-final = a clean clone of the final head (flip_grade.py --check 1x1/1if, rows_tiers.py --selftest, "
               "tier_grid.py, load_grade.py --check, the slice rule and tx_statements)",
    'merge': "the sync merge 663b519b: merge_words.py's resolution of section 13's three conflicting hunks, replayed "
             "on the saved conflicted file (the replay byte-identical to the commit)",
    'merge2': "the sync merge 056d619d: hunk 1 resolved by hand (this branch's sizes where #902 states its head's), "
              "hunk 2 by merge_words.py",
    'units': "each unit's log and rc (head and range first): the ledgers, the arms, the leg",
    'incident': "the leg R9-W8's first start, refused at once by run.py (point 8x8/2if; run.py takes 8x8)",
    'gates': "the full pass at the final head 056d619d, each job on its own fresh clean clone: verify-table.md "
             "(verify_wf.py), campaigns.txt, every workflow job's driver log, step rcs and tree after (workflows), "
             "the lane gates' summary, rcs and trees after (lane)",
    'sweep': "the full Verilator sweep at 056d619d, four shards (sweep_shard.py, each on its own pick8 range): each "
             "shard's spec, run log and completion; the spec; launched.txt; tsn_fuzz's field campaign lines; shard "
             "3's TEST_RESULTS.md date-stamp diff (restored)",
    'pass1-c772b1e5': "the full pass's first run at c772b1e5: the same gates, whose lane gate harness_selftest failed "
                      "2 checks (lane/harness_selftest-failures.txt), fixed in 249a3823; its sweep (and the two "
                      "starts that failed at once on the runner's path, sweep/failed-start); its units",
}


def scrub() -> list[Path]:
    """Scrub every text receipt; the files it changed."""
    changed = []
    for f in sorted(R.rglob('*')):
        if not f.is_file() or f.name == 'INDEX.md' or f.stat().st_size > 200_000:
            continue
        try:
            t = f.read_text()
        except UnicodeDecodeError:
            continue
        u = t
        for a, b in SUBS:
            u = u.replace(a, b)
        if u != t:
            f.write_text(u)
            changed.append(f)
    return changed


over = [f for f in R.rglob('*') if f.is_file() and f.stat().st_size > 200_000]
if over:
    sys.exit('REFUSED: over 200 KB: ' + ', '.join(str(p.relative_to(R)) for p in over))
scrub()
lines = ['# Receipts, lane 895 round 9 ([A775])', '',
         'Generated by round9/scripts/index.py from the files present, after the host-path scrub '
         '(placeholders: ' + ', '.join(sorted({b for _, b in SUBS})) + '), and checked after it: a second scrub '
         'changes no file and every hash below is its file\'s bytes.', '']
listed = {}
for d in sorted({p.parent for p in R.rglob('*') if p.is_file() and p.name != 'INDEX.md'}):
    rel = d.relative_to(R).as_posix() if d != R else '.'
    lines += [f'## {rel}', '', WHAT.get(rel, WHAT.get(rel.split('/')[0], '')), '', '| File | Bytes | sha256 |',
              '|---|---:|---|']
    for f in sorted(p for p in d.iterdir() if p.is_file() and p.name != 'INDEX.md'):
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        listed[f] = h
        lines.append(f'| {f.name} | {f.stat().st_size} | `{h}` |')
    lines.append('')
(R / 'INDEX.md').write_text('\n'.join(lines))
again = scrub()
bad = [f for f, h in listed.items() if hashlib.sha256(f.read_bytes()).hexdigest() != h]
if again or bad:
    sys.exit(f'INDEX check FAILED: a second scrub changed {len(again)}, {len(bad)} hash(es) differ')
print(f'INDEX.md: {len(listed)} files, the scrub idempotent, every hash its file\'s bytes')
