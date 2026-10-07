#!/usr/bin/env python3
"""probe_composition.py TREE OUT [NAME ...] - reviewer fault probes of the
three-way composition (ADP, ACMP, MAAP) of PR #688 at 13e71513.

TREE is an exported copy of the head (never the review clone). Each probe is
one exact text substitution in a copy of TREE/sw/firmware/ctrl; the arms
acmp, acmpif2, maap and maap_if2 are run on it and every [FAIL] line is
recorded. A probe is CAUGHT when any of those arms exits 1 with a [FAIL]
line, ESCAPED when every arm passes, BROKEN when a build or run refuses.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
ONLY = set(sys.argv[3:])
sys.path.insert(0, str(TREE / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(TREE / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

APP_H = "app/ctrl_app.h"
APP_C = "app/ctrl_app.c"

PROBES = (
    # The three-way bound with MAAP's share dropped: the analytical bound
    # understated by 568 accesses, still above the observed worst pass.
    ("pass-bound-drops-maap-share", APP_H,
     "#define CTRL_APP_PASS_MAX (ACMP_MBX_PASS_MAX + CTRL_APP_MAAP_PASS_SHARE)",
     "#define CTRL_APP_PASS_MAX (ACMP_MBX_PASS_MAX)"),
    # MAAP's slots overlapping ACMP's last interface only (visible at two).
    ("maap-slots-overlap-acmp-by-one", APP_H,
     "#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ACMP_FIRST_SLOT + MBX_N_IF)",
     "#define CTRL_APP_MAAP_FIRST_SLOT (CTRL_APP_ACMP_FIRST_SLOT + MBX_N_IF - 1u)"),
    # MAAP claiming one address whatever the entity declares.
    ("maap-count-one", APP_C,
     "\tuint16_t count = cfg->entity->talker_stream_sources;\n\tuint64_t preferred",
     "\tuint16_t count = 1u;\n\tuint64_t preferred"),
    # MAAP started without the configured preferred range.
    ("maap-start-drops-preferred", APP_C,
     "\t\t(void)maap_mbx_start(&app->maap, cfg->maap_preferred);",
     "\t\t(void)maap_mbx_start(&app->maap, 0u);"),
    # MAAP's allocation context lost on the composition.
    ("maap-ctx-dropped", APP_C,
     "cfg->maap_allocation, cfg->maap_ctx) &&",
     "cfg->maap_allocation, NULL) &&"),
    # MAAP started before the open (the channels and interrupts not yet up).
    ("maap-start-before-open", APP_C,
     "\tif (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {",
     "\tif (cfg->maap_allocation != NULL) {\n\t\t(void)maap_mbx_start(&app->maap, cfg->maap_preferred);\n\t}\n"
     "\tif (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {"),
    # A per-interface MAC for MAAP (k added), not the entity's one MAC.
    ("maap-mac-per-interface", APP_C,
     "\t\tmac[k] = cfg->entity->mac;\n",
     "\t\tmac[k] = cfg->entity->mac + k;\n"),
    # The explicit F2 entry ignoring its ctx.
    ("entry-drops-ctx", APP_C, "\twith.maap_ctx = ctx;\n", "\t(void)ctx;\n"),
    # MAAP composed even when ACMP refused (refusal after MAAP attaches).
    ("acmp-refusal-after-maap", APP_C,
     "\treturn cfg->maap_allocation == NULL || maap_compose(app, cfg);\n}",
     "\treturn cfg->maap_allocation == NULL || maap_compose(app, cfg) || true;\n}"),
    # The preferred range check gone only above (start below the pool kept).
    ("preferred-upper-unchecked", APP_C,
     "\t    preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE - count)) {",
     "\t    false)) {"),
)

ARMS = (("acmp", ctrl_arms.arm_acmp), ("acmpif2", ctrl_arms.arm_acmpif2),
        ("maap", ctrl_arms.arm_maap), ("maap_if2", ctrl_arms.arm_maap_if2))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    build = fw_gtest.Build(jobs=4)
    # the processor slices, cut beforehand from the review clone's pinned
    # submodule (ctrl_reuse.cut_reuse needs a git checkout; TREE is an export)
    base = Tree(CTRL, OUT / "base" / "build", OUT / "reuse", build)
    if not (base.reuse / "pp_adp_reuse.inc").exists():
        cut_reuse(base.reuse)
    for name, path, old, new in PROBES:
        if ONLY and name not in ONLY:
            continue
        copy = OUT / name / "ctrl"
        if copy.parent.exists():
            shutil.rmtree(copy.parent)
        shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
        target = copy / path
        text = target.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"[BROKEN] probe {name}: fixture occurs {text.count(old)} times in {path}", flush=True)
            continue
        target.write_text(text.replace(old, new), encoding="utf-8")
        tree = Tree(copy, OUT / name / "build", base.reuse, build)
        verdicts = []
        fails: list[str] = []
        broken = False
        for arm, fn in ARMS:
            try:
                o = fn(tree)
            except Refusal as exc:
                verdicts.append(f"{arm}=refused")
                broken = True
                print(f"    {arm} refused: {exc}"[:400], flush=True)
                continue
            f = [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]
            fails += [f"{arm}: {ln}" for ln in f]
            verdicts.append(f"{arm}=rc{o.rc}/{len(f)}fail")
            if o.rc not in (0, 1):
                broken = True
        status = "CAUGHT" if fails else ("BROKEN" if broken else "ESCAPED")
        print(f"[{status}] probe {name}: {' '.join(verdicts)}", flush=True)
        for ln in fails[:4]:
            print(f"    {ln[:300]}", flush=True)
        shutil.rmtree(OUT / name, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
