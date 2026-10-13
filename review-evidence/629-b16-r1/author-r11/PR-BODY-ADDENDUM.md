[A603] Refs #629. Proposed Round 11 addition for the manager.

## Round 11: composition, packet only

Under the [Round 11 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6144924772), this packet answers [R624-11-F1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6144894638). The PR head remains `f1b2489f5b1c929e81eeae79a469b2b27c47e340`. No page, index, repository code, bench result or acceptance item changes.

The two checks have distinct bindings:

- `author-r10/tools/check_b16_figures.py`, published at evidence commit `5775cfa78dc9250ea1b689fc2cfa8e20c41281bb`, remains bound to the source page blob `844ff7fb2e958ebb12368d22fa620dc094dd5888` at PR head `f1b2489f`.
- `author-r11/tools/check_b16_figures.py` binds the merged page blob `cdd3121f567e3a37784f98b962713db3de5c7687` at candidate `ada26e56ac42ee5de311aef84cb86c8435b97cee`. It is regenerated from the unchanged `r10_figures_spec.py` and `r10_figures_build.py` using that page. Exactly 1,934 page-row locators move by seven; README locators, keys, precision, receipt paths, identifier rules and checker logic are unchanged.

| Run | rc | Rows OK / BAD | Uncovered digits | MARKUP |
|---|---|---|---|---|
| Source page, source check | 0 | 1,960 / 0 | 0 | 0 |
| Candidate page, old source check (negative control) | 1 | 53 / 1,907 | 12,779 | 0 |
| Candidate page, regenerated check | 0 | 1,960 / 0 | 0 | 0 |

The passing runs cover 15,597 digits: 12,988 by receipt rows and 2,609 by identifiers. The new candidate stdout, rows and coverage equal R624-11's +7 probe byte for byte. `author-r11/tools/reproduce.sh` step 1 uses the new check for `cand` and exits 0. Regeneration is byte-equal; normalizing candidate page locators by -7 gives the source rows and coverage byte for byte.

Every earlier runner retains its outcome: rounds 3 through 10 return 5/5, 7/8, 21/22, 38/39, 48/50, 73/73, 97/97 and 117/117. The historical failures remain those superseded by [decision 6132293481](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481). All 172 self-probes, 59 parser cases and 15 parser-output mutation cases retain their outcomes; the rule-isolation comparison is equal too.

All 15 earlier review-probe outcomes are retained. Twelve probe originals run unchanged. Three also have explicitly relocated copies: the two row selectors move 3008/3174/3200 to 3015/3181/3207, and R624-6's attribution anchor moves 3244 to 3251. Their original candidate runs are retained: the old row selectors select nothing, and the old attribution anchor refuses before running the check. Only the listed locators change in the reruns; no mutation or expected outcome changes. Other diagnostic page locators move by seven, including 18 to 25, 19 to 26, 2301/2302 to 2308/2309 and 4604 to 4611; `README.md:15` stays. Detailed before/after locators and comparisons are in `author-r11/receipts/`.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| Source check | 199,268 | `a9f36f9d9ff3bfd6c7f7ce86f64ef1ac9531f1cf594d68d3a06437f8e8d0e540` |
| Candidate check | 199,268 | `49d3d0692941ac42c009a2abd3e1bec7f3ab85d027eddaf4845e1f5fb1e44944` |
| Spec | 167,841 | `407817bdd7a516d297141a430f69c6b63f0c38c416da8b4b52c586c5e57a4816` |
| Build | 6,603 | `d2075750721d7acfbb475d66f0dc60b9141aabec2ae1d1cd6faf465331c47005` |
| Source page, retained outside packet | 330,109 | `bb5da487a811cae3c92f8ea6ededd498268113765977fb9444efa94717401a1f` |
| Candidate page, retained outside packet | 330,604 | `cba50df490ef053fe2d55cf4ed8e057ff8a97105353f89d44e8672f9934d0c33` |

Packet: `629-b16-a603/author-r11/`, for publication beside `author-r10/` on `629-b16-review-evidence`. It depends on the unchanged receipts in `author-r10/`; it does not duplicate them. `MANIFEST.sha256` binds the new packet. The earlier source packet and source check remain unchanged.

All 14 required local gate entries are rc 0 at `f1b2489f`, recorded in `author-r11/gates/results.json`. There was no bench action, lock acquisition, commit, push or PR edit. The manager applies this PR-body text, publishes the packet and requests R624-12 at `ada26e56`. As decided in the assignment, the page-binding wording belongs on the #495 residue list; the findings page stays unchanged. The source-head wording residue R624-10-R1 is corrected in this proposed body. Refs #629.
