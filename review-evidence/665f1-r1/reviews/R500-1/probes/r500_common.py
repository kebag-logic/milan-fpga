# R500-1 review probes: shared setup. Builds the reviewed store (or a planted
# copy of it) for one shipped shape with the lane's own bench helpers, so the
# store, the ports and the models compile exactly as the lane's suite builds them.
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

#: The checkout under review (exact head 215c3c0b): $R500_CLONE, else the cwd.
CLONE = Path(os.environ.get("R500_CLONE", os.getcwd()))
PACKET = Path(__file__).resolve().parents[1]
SCRATCH = PACKET / "scratch"
sys.path.insert(0, str(CLONE / "sw/firmware/ctrl_nvm/test"))

import nvm_bench  # noqa: E402
from nvm_bench import TREE, make_bench, shape_inputs  # noqa: E402

_INPUTS: dict[str, object] = {}


def inputs(stem: str):
    """The builder's shape and identity for one shipped config (cached on disk)."""
    if stem not in _INPUTS:
        work = SCRATCH / "shape" / stem
        work.mkdir(parents=True, exist_ok=True)
        _INPUTS[stem] = shape_inputs(CLONE / "configs" / f"{stem}.yaml", work)
    return _INPUTS[stem]


def planted_tree(name: str, seams: list[tuple[str, str, str]]) -> Path:
    """A copy of the reviewed tree with exact-once text replacements."""
    dest = SCRATCH / "trees" / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(TREE, dest, ignore=shutil.ignore_patterns("__pycache__"))
    for rel, old, new in seams:
        p = dest / rel
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{name}: seam found {n} times in {rel}: {old!r}")
        p.write_text(text.replace(old, new))
    return dest


def bench(stem: str, name: str, tree: Path = TREE):
    work = SCRATCH / "bench" / name / stem
    if work.exists():
        shutil.rmtree(work)
    return make_bench(inputs(stem), work, tree)


#: Harness-only seams: a PHC offset in the LiteSPI CSR model and a script word
#: to move it. The store, the codec and both flash ports stay byte-identical.
PHC_SEAMS = [
    ("host/litespi_model.c",
     "static uint32_t lm_csr[LM_CSR_WORDS];\n",
     "static uint32_t lm_csr[LM_CSR_WORDS];\nlong long r500_phc_offset_ns;\n"),
    ("host/litespi_model.c",
     "\tuint64_t ns = nvm_fmodel_now_us() * 1000u;\n",
     "\tuint64_t ns = (uint64_t)((long long)(nvm_fmodel_now_us() * 1000u) + r500_phc_offset_ns);\n"),
    ("test/nvm_test.c",
     "\telse if (strcmp(a, \"--flip\") == 0)\n",
     "\telse if (strcmp(a, \"--phc-shift-ms\") == 0) {\n"
     "\t\textern long long r500_phc_offset_ns;\n"
     "\t\tr500_phc_offset_ns += strtoll(v, NULL, 0) * 1000000LL;\n"
     "\t} else if (strcmp(a, \"--flip\") == 0)\n"),
]
