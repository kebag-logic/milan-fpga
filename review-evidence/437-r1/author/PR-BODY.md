[A168]

## Status

Ready for independent review at `65df1df50a80cd5f540a93d8f0cfabc97da3da75`. The 25 focused author gates pass. Manager-owned full verification and review bars remain outstanding.

## Description

After a blank line in a list item, the Contents walk treated text at the item's content column as a top-level paragraph. A following lone HTML tag could then leave an invisible heading listed and grant its copied label an em-dash exemption. Preserve the item's column and paragraph context so these tags hide the heading as GitHub GFM does.

Keep the selected five setext/container heading omissions and document their direction in the walk and CONTRIBUTING 6.1. No heading addition, provenance-policy change, RTL, workflow or dependency change.

Closes #437

## How to reproduce

The public renderer receipt contains exact synthetic Markdown and GitHub response HTML for 47 fixtures, including 11 reconstructed escape cases and all measured boundary categories. Original historical JSON artifacts were not publicly available; byte identity with those files is not claimed.

## How to validate

```sh
rtk proxy python3 -B scripts/gen_toc.py --selftest
rtk proxy python3 -B scripts/gen_toc.py --check
rtk proxy python3 -B scripts/gen_toc.py --verify-anchors
rtk proxy python3 -B scripts/check_em_dash.py --selftest
rtk proxy python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
rtk proxy python3 -B scripts/docs_check.py
rtk proxy python3 -B scripts/check_py_idiom.py
```

The complete 25-command list and mutation/corpus evidence are published in the validation receipt. Selftest results are evidence; they should also be copied into a PR comment by the manager after creating the PR.

## DoD

- [x] Selected implementation and documented-limitation paths implemented.
- [x] Tracked Markdown classifications unchanged on both base/head corpora.
- [x] Existing corpus and #507 controls preserved; no ratchet widened.
- [x] Focused author gates, negative controls and mutation evidence published.
- [ ] Independent R237/R238 reviews and reviewer-owned clean lens coverage.
- [ ] Full native, trusted-dev act and required hosted evidence.
- [ ] Current candidate validation, authorized merge and containment.

- Decision: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775771538
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775813779
- Renderer fixtures/results: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775985191
- Validation/mutations/preservation: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5776027743
- Original R85-4: https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5644713074
- Original R86-5: https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5644834363
