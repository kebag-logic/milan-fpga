#!/usr/bin/env python3
"""[R238] end-to-end em-dash gate worker: run ONE revision's shipped gate.

Usage: e2e_gate_worker.py <scripts-dir> <shapes.json> <out.json>

The worker imports `check_em_dash` (and through it `gen_toc`) from the given
scratch scripts directory, builds one real Git repository with the gate's own
fixture helpers, commits every base page carrying a synthetic shape with the
heading `## Old <U+2014> heading` where each probe puts `## Old`, then a head
commit whose page shows that heading and carries the generated Contents
block, and asks `judge_page` for each page. Nothing outside a temporary
directory is written except the result file.
"""
import json
import sys
import tempfile
from pathlib import Path

scripts = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(scripts))
import check_em_dash as gate  # noqa: E402
import gen_toc  # noqa: E402

EM = "—"
HEADING = f"## Old {EM} heading\n"
TAIL = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"


def main() -> int:
    shapes = json.loads(Path(sys.argv[2]).read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="r238.e2e.") as tmp:
        repo = Path(tmp)
        gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
        bases = {}
        for i, row in enumerate(shapes):
            body = row["page"].replace("## Old\n", HEADING, 1)
            text = f"# Page\n\n{body}{TAIL}"
            bases[i] = text
            (repo / f"page{i}.md").write_text(text, encoding="utf-8")
        base = gate._commit(repo, "r238 base")
        heads = {}
        for i in range(len(shapes)):
            shown = "# Page\n\n" + HEADING + TAIL
            new = gen_toc.apply(repo / f"page{i}.md", shown)
            heads[i] = new
            (repo / f"page{i}.md").write_text(new, encoding="utf-8")
        gate._commit(repo, "r238 head")
        for i, row in enumerate(shapes):
            verdict = gate.Verdict()
            path = f"page{i}.md"
            gate.judge_page(repo, base, gate.Change(path, path), verdict)
            results.append({"id": row["id"], "base_page": bases[i],
                            "head_page": heads[i],
                            "base_headings": [h[1] for h in gen_toc.headings(bases[i])],
                            "findings": verdict.findings,
                            "exempt": verdict.exempt,
                            "judged": verdict.judged})
    Path(sys.argv[3]).write_text(json.dumps(results, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
