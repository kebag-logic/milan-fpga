#!/usr/bin/env python3
"""f1_probe.py - grade a subset of the F1 store's planted defects, and run
independent reviewer probes, at the shipping 1x1 shape.

usage: python3 f1_probe.py TREE WORK [--named a,b,...] [--probes] [--jobs N]

TREE is a checkout of the reviewed head (its copy is planted, never TREE
itself). --named grades the tree's own mutants of those names exactly as
test_ctrl_nvm.py --self-test does (each named test must fail). --probes plants
each PROBE below into a copy, builds the 1x1 binaries, runs every binary's
whole suite, and prints the tests that failed (a probe with none SURVIVED).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

#: (name, file relative to sw/firmware/ctrl_nvm, exact text, replacement)
PROBES = (
    ("p01_legacy_slot_a_only", "nvm_store.c",
     "\tfor (i = 0; i < 2u; ++i)\n\t\tif (f->read(f->ctx, NVM_LEGACY_A",
     "\tfor (i = 0; i < 1u; ++i)\n\t\tif (f->read(f->ctx, NVM_LEGACY_A"),
    ("p02_frame_id_high_byte_zero", "nvm_klj2.c", "\trec[4] = (uint8_t)(r.id >> 8);", "\trec[4] = 0u;"),
    ("p03_decode_id_low_byte_only", "nvm_klj2.c", "\tid = ((unsigned int)p[4] << 8) | p[5];", "\tid = p[5];"),
    ("p04_frame_reserved_byte_set", "nvm_klj2.c", "\trec[3] = 0u;", "\trec[3] = 1u;"),
    ("p05_erase_same_block_twice", "nvm_store.c",
     "nvm_slot_addr(nvm.target) + nvm.block * NVM_ERASE_BLOCK)", "nvm_slot_addr(nvm.target))"),
    ("p06_container_cap_64k", "nvm_shape.h", "#define NVM_KLJ3_MAX       NVM_SLOT_BYTES",
     "#define NVM_KLJ3_MAX       65536u"),
    ("p07_legacy_any_nonblank_header", "nvm_store.c", "nvm_rd32le(nvm_chunk) == NVM_KLJ2_MAGIC)",
     "nvm_rd32le(nvm_chunk) != 0xffffffffu)"),
    ("p08_ver_overrides_own_refusal", "nvm_store.c",
     "if (nvm.st.last_verdict == NVM_VD_BLANK && nvm.st.legacy)", "if (nvm.st.legacy)"),
    ("p09_open_words_short", "nvm_store.c", "#define NVM_WORDS ((NVM_ID_SPACE + 31u) / 32u)",
     "#define NVM_WORDS (NVM_ID_SPACE / 32u)"),
    ("p10_klj2_header_written", "nvm_klj2.c", "\tnvm_wr32le(img + 0, NVM_KLJ3_MAGIC);",
     "\tnvm_wr32le(img + 0, NVM_KLJ2_MAGIC);"),
    ("p11_layout_word_2", "nvm_klj2.c", "\tnvm_wr32le(img + 36, NVM3_LAYOUT);", "\tnvm_wr32le(img + 36, 2u);"),
    ("p12_legacy_b_wrong_place", "nvm_shape.h",
     "#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE / 2u)",
     "#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE)"),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--named", default="")
    ap.add_argument("--probes", action="store_true")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default="", help="probe names to run (default: all)")
    args = ap.parse_args()
    sys.path.insert(0, str(args.tree.resolve() / "sw/firmware/ctrl_nvm/test"))
    import test_ctrl_nvm as t  # noqa: E402  (sets the suite's own import paths)
    import fw_gtest  # noqa: E402
    import nvm_mutants as nm  # noqa: E402

    work = args.work.resolve()
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    print(f"tree {args.tree}", flush=True)
    stem = t.SELF_TEST_SHAPE
    shape = t.prepare(t.ROOT / "configs" / f"{stem}.yaml", work / "shape")
    shared = fw_gtest.Build(jobs=1)
    print(f"prepared {stem}", flush=True)
    bad = 0
    names = [n for n in args.named.split(",") if n]
    if names:
        listing = t.build(shape, work / "listing", fw_gtest.Build(jobs=args.jobs, cache=shared.cache))
        held = t.suite_tests(listing, shape)
        chosen = [m for m in nm.MUTANTS if m.name in names]
        missing = sorted(set(names) - {m.name for m in chosen})
        if missing:
            print(f"NO SUCH MUTANT: {missing}")
            bad += len(missing)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futs = [pool.submit(t.plant_and_grade, m, shape, held, work / "mutants", shared) for m in chosen]
            for fut in as_completed(futs):
                v = fut.result()
                if v:
                    print(v, flush=True)
                    bad += 1
        print(f"named mutants graded: {len(chosen)}, not caught or not built: {bad}")
    if args.probes:
        def probe(p):
            name, rel, old, new = p
            m = nm.Mutant(name, ((rel, old, new),), ())
            tree = work / "probes" / name / "tree"
            try:
                nm.plant(m, tree)
            except Exception as exc:  # the seam did not match
                return f"PROBE {name}: NOT PLANTED ({exc})"
            try:
                exes = t.build(shape, work / "probes" / name, shared, tree)
            except Exception as exc:
                return f"PROBE {name}: does not build -> CAUGHT at compile ({str(exc)[-160:]!r})"
            failed, crashed = [], []
            for binary in t.binaries(shape):
                ok, log = t.run_suite(exes[binary.name], t.fixture_of(shape, binary))
                failed += fw_gtest.failed_tests(log)
                if not ok and not fw_gtest.failed_tests(log):
                    crashed.append(binary.name)
            shutil.rmtree(tree, ignore_errors=True)
            if failed or crashed:
                return (f"PROBE {name}: CAUGHT by {sorted(set(failed))[:6]} ({len(set(failed))} tests)"
                        f"{'; binary failed without a [FAIL] line: ' + ','.join(crashed) if crashed else ''}")
            return f"PROBE {name}: SURVIVED (no test failed)"
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            only = [n for n in args.only.split(",") if n]
            chosen_p = [p for p in PROBES if not only or p[0] in only]
            for fut in as_completed([pool.submit(probe, p) for p in chosen_p]):
                print(fut.result(), flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
