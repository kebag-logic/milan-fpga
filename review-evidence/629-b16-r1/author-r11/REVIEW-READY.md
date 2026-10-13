[A603] REVIEW READY

Round 11: composition, packet only, under [assignment 6144924772](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6144924772). Answers [R624-11-F1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6144894638).

PR head: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, unchanged.
Candidate: `ada26e56ac42ee5de311aef84cb86c8435b97cee`.
Packet: `629-b16-a603/author-r11/`, ready for publication beside `author-r10/` on `629-b16-review-evidence`.

The check was regenerated using the merged page and byte-identical copies of the published spec and build. Exactly 1,934 page-row locators move by +7. No receipt, precision, identifier rule or checker logic changes. The source packet's check stays unchanged.

| Binding | Page Git blob | Check SHA-256 |
|---|---|---|
| Source, author-r10 at evidence commit `5775cfa7` | `844ff7fb2e958ebb12368d22fa620dc094dd5888` | `a9f36f9d9ff3bfd6c7f7ce86f64ef1ac9531f1cf594d68d3a06437f8e8d0e540` |
| Candidate, author-r11 | `cdd3121f567e3a37784f98b962713db3de5c7687` | `49d3d0692941ac42c009a2abd3e1bec7f3ab85d027eddaf4845e1f5fb1e44944` |

| Run | rc | Rows OK / BAD | Uncovered digits | MARKUP |
|---|---|---|---|---|
| Source page, source check | 0 | 1,960 / 0 | 0 | 0 |
| Candidate page, source check: negative control | 1 | 53 / 1,907 | 12,779 | 0 |
| Candidate page, regenerated check | 0 | 1,960 / 0 | 0 | 0 |
| `reproduce.sh` step 1, `cand`, regenerated check | 0 | 1,960 / 0 | 0 | 0 |

All three baseline runs match R624-11's corresponding stdout, rows and coverage byte for byte. The candidate passes with 15,597 digits covered: 12,988 by receipt rows, 2,609 by identifiers. Rebuilding reproduces the new check byte for byte. Normalizing candidate page locators by -7 gives the source rows and coverage byte for byte; the stdout is equal without normalization.

| Earlier runner | Passing controls | rc | Comparison |
|---|---|---|---|
| Round 3 | 5 / 5 | 0 | Retained |
| Round 4 | 7 / 8 | 1 | Retained |
| Round 5 | 21 / 22 | 1 | Retained |
| Round 6 | 38 / 39 | 1 | Retained |
| Round 7 | 48 / 50 | 1 | Retained |
| Round 8 | 73 / 73 | 0 | Retained |
| Round 9 | 97 / 97 | 0 | Retained |
| Round 10 | 117 / 117 | 0 | Retained |
| Additional self-probes | 172 / 172 | 0 | Retained |
| Parser audit | 59 / 59 | 0 | Equal |
| Parser-output mutations | 15 / 15 | 0 | Equal |
| Rule-isolation comparison | All cases | 0 | Equal after locator normalization |

Historical control failures remain exactly those covered by [decision 6132293481](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481); they are not counted as wholly green.

| Review probe | Candidate result compared with Round 10 |
|---|---|
| R624-4 escape forms | 8 / 8 detected, retained |
| R625-4 coverage | 12 / 12 detected, retained |
| R625-3 coverage | 7 / 7 detected, retained |
| R624-5 LOCKED row mutation | Original selector empty; +7 copy names the expected MISMATCH at line 3207 |
| R624-5 escape forms | 21 / 25 detected, recorded limits retained |
| R625-5 comments | Statuses 0 / 1 / 1 retained |
| R625-6 rendered comments | Statuses 0 / 1 / 1 / 1 / 1 / 1 retained; probe's historical rc 1 retained |
| R625-6 followers | All 22 outcomes retained |
| R624-6 escape forms | Original fixed anchor refuses at 3244; +7 copy at 3251 retains all 37 outcomes, including the same four not-meeting cases |
| R624-6 poll-count mutation | Original selector empty; +7 copy names the expected MISMATCH at line 3207 |
| R624-7 Markdown forms | All 17 outcomes retained |
| R624-7 invisible characters | All 10 outcomes retained |
| R625-7 markup | All 25 outcomes retained; both receipts written, no exception |
| R624-8 block extents | Every outcome retained |
| R624-9 autolinks | Every outcome retained |

Twelve public probe originals run unchanged. Three additional copies change only fixed locators: 3008/3174/3200 to 3015/3181/3207, or attribution anchor 3244 to 3251. Their unchanged original candidate results are retained too. Diagnostic page locators move by +7, including 18 to 25, 19 to 26, 2301/2302 to 2308/2309 and footnote 4604 to 4611. `README.md:15` stays. `control-comparison.json` and `probe-comparison.json` retain the detailed comparisons; all comparisons pass.

Spec SHA-256: `407817bdd7a516d297141a430f69c6b63f0c38c416da8b4b52c586c5e57a4816`.
Build SHA-256: `d2075750721d7acfbb475d66f0dc60b9141aabec2ae1d1cd6faf465331c47005`.
Candidate page SHA-256: `cba50df490ef053fe2d55cf4ed8e057ff8a97105353f89d44e8672f9934d0c33` (330,604 bytes; kept outside the packet).
The packet records hashes and sizes, reuse provenance for 31 scripts, setup corrections, all run receipts, and `MANIFEST.sha256`. No packet file exceeds 200,000 bytes.

All 14 required local gate entries are rc 0 at the unchanged head: documentation, style, Contents and anchors, em-dash against `e8454e27`, paths, scope self-test, bare-metal check/self-test, feature-status self-test, and both diff checks. Exact commands are in `gates/results.json`.

`PR-BODY.md` supplies the full proposed body with both bindings and the R624-10-R1 wording correction. The manager applies it and publishes this packet. The page-binding wording goes to the #495 residue list as assigned; the page and index remain unchanged. Ready for R624-12 at `ada26e56`.

No bench action or lock acquisition, commit, push, PR edit or new checkout. Existing restore evidence stands. Refs #629; its earlier acceptance limitations remain open.
