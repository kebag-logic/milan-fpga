#!/usr/bin/env python3
"""body.py R5_BODY OUT SELFTEST_RESULT: round 5's PR body with the head paragraph moved to the sync merge, the stale
dev-soft-core paragraph replaced by the sync note, one commit-table row, and this round's evidence rows."""
import sys
from pathlib import Path

src, out, selftest = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
body = src.read_text(encoding="utf-8")


def swap(old, new):
    global body
    if body.count(old) != 1:
        raise SystemExit(f"expected exactly one occurrence of: {old[:80]!r}")
    body = body.replace(old, new)


HEAD = "2b98e219a5e2b0681f76be90083fc05e47a8f6c0"

swap(
    "Head `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570`. It is one commit on `507bce7f`, the merge of `dev-soft-core`\n"
    "`2509db68` (the flip train, PR #988) into the lwSRP `d1bb4f4e` pin `30796098`. That commit restates the held-egress\n",
    f"Head `{HEAD}`, the merge of `dev-soft-core` `e608f8d8` into `67838b37` (below). `67838b37` is\n"
    "one commit on `507bce7f`, the merge of `dev-soft-core`\n"
    "`2509db68` (the flip train, PR #988) into the lwSRP `d1bb4f4e` pin `30796098`. That commit restates the held-egress\n",
)

swap(
    "`dev-soft-core` is now `2f2a8152` (PR #1001: CI and harness-build speed-ups, no firmware or pin change). This branch\n"
    "does not merge it. The head merges with it without conflict (`git merge-tree`), and the merge candidate composes it.\n",
    "**Synced onto dev-soft-core `e608f8d8`.** The head merges `dev-soft-core` `e608f8d8` into `67838b37`. That brings\n"
    "in PR #1001 (CI and harness-build speed-ups: Verilator probe lists, ccache, the budget testbench at `-O3`) and PR #995\n"
    "(the FPGA-gPTP pin `1213ac5b`). The two sides conflicted only in the generated submodule diagram\n"
    "(`submodule_boundaries.drawio`, its PNG and its `PNG_MANIFEST.json` entry), because each regenerated it for its own\n"
    "pin. It was regenerated at the merge by `docs/diagrams/submodule_boundaries.gen.py`, not edited, and it names both\n"
    "pins: gptp-processor `1213ac5b` and lwSRP `d1bb4f4e`. Against each parent, the drawio and SVG differ by the other\n"
    "side's pin token only.\n"
    "\n"
    "- `git diff e608f8d8 HEAD` lists exactly this PR's 21 paths. Every path outside them equals `e608f8d8`'s.\n"
    "- `git diff 67838b37 HEAD` lists exactly `dev-soft-core`'s 37 paths since `2509db68`. Outside the diagram files and\n"
    "  `docs/reference/SUBMODULES.md`, each path's change is byte-identical to `dev-soft-core`'s. `SUBMODULES.md`, which\n"
    "  both sides changed, is git's clean three-way merge (`git merge-file`, 0 conflicts). Against `e608f8d8` it differs\n"
    "  by this PR's lwSRP row only.\n"
    "- Every control firmware ELF, `.bin` and AEM image is byte-identical to `67838b37`'s (20 of 28 files built by\n"
    "  `plat_ledger.py --build-dir`), the 8x8/1if harness image `eed56acc…` and the 1x1/1if `79c5326c…` among them. The\n"
    "  other 8 are the copies of `gptp_ucode.hex`, which `gptp-processor/hdl/ucode/gen_gptp_ucode.py` generates and which\n"
    "  change with #995's pin. So the firmware, gate and harness figures below hold at this head. The routed 8x8/1if\n"
    "  figures under Images are `507bce7f`'s. They do not include #995's fabric change, which carries its own evidence.\n",
)

swap(
    "| Restate the held-egress ledger at 8x8/1if at the flip train's and the lwSRP pin merge's measurements |",
    "| Merge dev-soft-core e608f8d8 (PRs #1001 and #995, the FPGA-gPTP 1213ac5b pin) into the lwSRP d1bb4f4e pin "
    "| the sync merge onto `e608f8d8`, above: the submodule diagram regenerated with both pins, nothing else of this "
    "PR's changed |\n"
    "| Restate the held-egress ledger at 8x8/1if at the flip train's and the lwSRP pin merge's measurements |",
)
# Keep the commit table in commit order: move the new row after the ledger row.
lines = body.split("\n")
i = next(n for n, line in enumerate(lines) if line.startswith("| Merge dev-soft-core e608f8d8"))
row = lines.pop(i)
j = next(n for n, line in enumerate(lines) if line.startswith("| Restate the held-egress ledger"))
lines.insert(j + 1, row)
body = "\n".join(lines)

swap(
    "| `docs.yml` steps, at `67838b37` |",
    f"| Image identity, at `{HEAD[:8]}` | `plat_ledger.py --build-dir` PASS at every point (0 findings). 20 of 28 files "
    "byte-identical to `67838b37`'s: every `ctrl_app.elf`, `.bin` and `aem_desc.bin`, the 8x8/1if mapped ELF "
    "`eed56acc…` among them. The 8 others are `gptp_ucode.hex` (#995's pin) |\n"
    f"| Docs gates, at `{HEAD[:8]}` | rc 0 each, porcelain 0 before and after: `docs_check.py` (0 findings, 223 Markdown "
    "files), `check_doc_style.py`, `docs_inventory.py --check`, `submodule_boundaries.gen.py --check` and `--selftest`, "
    "`timesync_chain.gen.py` and `DOC_MAP.gen.py` `--check` and `--selftest`, `check_submodule_docs.py` (6 exact "
    "gitlinks), `check_diagram_pngs.py` and its `--selftest` (28 mutation controls) |\n"
    f"| `egress_ledger.py --selftest`, at `{HEAD[:8]}` | PASS, rc 0: 72 of 72 controls, 18 of 18 mutants caught. The "
    "output is identical to `67838b37`'s |\n"
    f"| Harness self-test (`run.py --self-test`), at `{HEAD[:8]}` | {selftest} |\n"
    "| `docs.yml` steps, at `67838b37` |",
)

out.write_text(body, encoding="utf-8")
print(f"wrote {out}: {len(body.encode())} B")
