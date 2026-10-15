[R635] NEGATIVE - exact head 480c5e916f8bf711c47e1985ba3efe2b2471bdda

Round R635-1, external independent review of issue #645 / PR #747. Tree `5841131ff2c6d46a1c96ebfcc0ff9445e62825e7`; base `9ef717727e6fdac11ee7f01672fefae948452343`. All five lenses applied. One MAJOR evidence finding remains. The counter results and restore reproduce; the installed-image provenance cannot be verified from the published receipts.

## Scope and authorities

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and public rulings, the linked design and register contract, then the exact diff/history and public receipts. The diff is one commit adding 315 lines to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, including its Contents entry. No source, test, build configuration, or submodule changes.

The [close ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217) records the earlier switch acceptance as delivered and leaves the INTERNAL bind residual open. The [acceptance assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6199691564) requires the installed dev image identity first, unchanged B17 method, ten binds graded by unchanged SLIP_LB, separate treatment of #743, and restoration. `docs/design/MEDIA_CLOCK_FOLLOWING.md:1264` defines the bind arm and limits; `docs/reference/REGISTER_MAP.md:1878` defines cumulative, saturating slip counters, whose recentre action is excluded. CONTRIBUTING.md section 6 governs privacy. REQ-VER-04/05 distinguish documentary evidence and booted-board evidence.

Evidence examined: [B18 packet](https://github.com/kebag-logic/milan-fpga/tree/2e9135196430eb73fb9c2ca414a17f111d61028d/review-evidence/645-b18-r1), and the author, author-r2 and author-r3 portions of [B17 packet](https://github.com/kebag-logic/milan-fpga/tree/bdb96b6685751a424fbbdc952726f33efd17282a/review-evidence/645-b17-r1). No other review report was read before writing this independent verdict and ledger.

## Finding

**R635-1-F1 | MAJOR | Conformance, Tests, Docs**

Artifact: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5035` and `:5016`; public packet `MANIFEST.json`, `author/identity/identity-verdict.txt`, `author/identity/console-identity.txt`, and the PR's Image/close-condition claims.

Authority/evidence: acceptance item 1 requires identification of the installed dev `9ef71772` image. The page expressly says VERSION and AEM CRC are unchanged from `5603c353`, and therefore makes the manager's flash record the image proof. The supplied public packet lists 90 files, all hash-verified, but contains no flash or cold-power-cycle receipt, build-to-bitstream identity, or cold-boot log. The public `author/HANDOFF.md:27` specifically identifies the missing record as `build-9ef71772/flash.log`, SHA-256 `a1539c67fc8c6490034332976024248decf3046fdc8da72a9c867762e09d9d46`, and calls it "outside the packet". That is a useful retrieval key, but the log bytes and their image attribution are unavailable for this review. Its live identity script verifies ENTITY/CONFIGURATION, CSR version and AEM CRC; none distinguishes the old gateware from the new gateware. The public assignment states FLASH_RC=0, POWERCYCLE_RC=0 and the boot values, but supplies no linked executable receipt for those assertions. The issue and PR evidence available for this independent pass do not fill that gap. See `evidence-inventory.txt`, `public-scope.json`, and `replay.txt`.

Impact: ten held binds are supported as observations, but a cold reviewer cannot establish that those observations were taken on the image containing PR #742. The unqualified image-identity PASS and #645 close claim therefore exceed the published proof. This is an acceptance/evidence defect, not wording residue, and does not assert that the wrong image was actually installed.

Required outcome: publish and link the existing sanitized build/image and installation receipts that associate the bitstream with dev `9ef717727e6fdac11ee7f01672fefae948452343`, establish the verified flash pair and successful cold boot with no fallback before the measurement, and connect that boot to the lane's identity reads. Include the relevant image hashes and return codes. If that provenance cannot be recovered, retain the measured counter result but withhold the image-specific close claim until it is demonstrated. No new bench operation is prescribed if the existing records establish the chain.

Verification: independently follow source revision -> image hash -> verified flash -> cold boot -> identity reads -> cycle start using public receipts; then re-evaluate identity and closure at the reviewed head.

## Results by lens

[R635] PASS RTL - `hdl/milan/milan_datapath.sv:6626`, `:6833`, `hdl/common/csr/milan_csr.sv:2438`, and the exact one-file diff - the findings describe the existing first-accepted-PDU arm at INTERNAL, 2,048-tick dwell, and unexported recentre count correctly. The register projection carries fill, prefill, convergence and rails, not recentres. No RTL/interface/CDC/reset implementation changes occur. Existing source-comment lane wording is outside this delta and remains under #746; this PR introduces no source-comment instance.

[R635] PASS Robustness - `author/cycles/c01/poll.jsonl` through `c10/poll.jsonl`, each corresponding events receipt, `author/restore/census-{start,end}.jsonl`, and findings `:5246` - all reads are present, counters are unsaturated zero, unbind/rebind and end-state checks succeed, and no clock-source write occurs. Restore equality is independently checked rather than inferred from the summary. The early arming-window and following-mode limitations are explicit; no #743 correction or physical calibration is claimed.

Conformance applied: all ten observed cycles satisfy the assignment's held predicate; no +1 residual or +2 class-(c) event occurs. Earlier switch acceptance is taken from the public ruling, not re-proven here. F1 prevents acceptance of the image-specific closure.

Tests applied: verified every publication-manifest hash and the 13 evidence-file sizes/hashes in the page. Independently decoded all 800 polls, all cycle event/state records and changed GET_COUNTERS fields; regenerated both tables independently. B17's ten raw logs each show a +2 dup transition; B18's show none. Replayed the public identity and summary programs offline: identity verdict and all five summary products are byte-identical. Planted +1 dup, +2 dup, skip and saturation controls are rejected by the independent held check. F1 leaves the measurement's gateware attribution unproved.

Docs applied: the two per-cycle tables, ten capture hash rows, counter digest, restore exception and limitation figures agree with the receipts. The added text and PR body use neutral roles for private equipment; the DUT's declared project identity is the expected identity gate. No private host, instrument or reference-peer product is named in the added prose. F1 remains an unsupported identity/closure claim.

## Reproduced results

- Poller SHA-256 `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7`, grader `299d4f55441e147bf6d27b5b51242d3384157e4905d27f6ed1064398f05f9468`: byte-equal to B17. Peer-gap reader also matches. Cycle runner AST equals B17 after exactly three path substitutions; two explanatory comments are the remaining text change. All ten start receipts record the stated runner/poller hashes.
- Ten cycles, 80 readable polls each; both slip words zero throughout and at both baselines. Raw-log digest `2c5e8d6ff8220cb16a9a3d0535279dfd7f04b5642c9aee2d9f97cdefcd939bdb` reproduced. Only RENDER_STAT changes among polled words. DUT clock source 0 and peer source 1 at both ends of every cycle. Every unbind/bind answers success, formats match without a set, and every end binding matches the as-found binding.
- Identical 32-second hold and polling schedule. Measured final poll endpoints are +31.700514 to +31.881568 seconds; B17's are +31.750712 to +31.926824. They are not identical timestamps: the unchanged asynchronous polling method and cumulative baseline/next-cycle reads cover the tails. The page reports the actual shorter endpoints rather than repeating B17's numbers.
- First-burst peaks 24.918 to 28.989 us. First burst minus the design firing time ranges from 32.735333 to 4557.171333 ms, reproducing the stated minimum 32.7 ms and maximum 4.56 s. Thus the first qualifying bursts do not exercise the 42.7 ms arming window. These timing calculations use published tap-derived summaries, not an independently replayed raw capture.
- Restore: 45/46 census records equal after removing only transaction timestamps/sequence fields; the single difference is live propagation delay 382 -> 388 ns. Bindings, maps, formats and clock sources match. NVM sequence 315 -> 335 and successful commits 0 -> 20 with pend=0; peer start/stop increments are +1 per cycle, +10 total.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Assignment/ruling; findings :5016/:5035; identity and cycles receipts; design :1264; register map :1878 | R635-1 | 480c5e916f8bf711c47e1985ba3efe2b2471bdda |
| RTL | CLEAN | Exact one-file diff; milan_datapath.sv :6626/:6833; milan_csr.sv :2438 | R635-1 | 480c5e916f8bf711c47e1985ba3efe2b2471bdda |
| Robustness | CLEAN | All ten raw poll/event pairs; baseline/census restore; findings :5246; audit controls | R635-1 | 480c5e916f8bf711c47e1985ba3efe2b2471bdda |
| Tests | UNCLEAN (F1) | Publication manifest; raw polls/events; B17 method bytes; summary/identity replay; missing installation receipts | R635-1 | 480c5e916f8bf711c47e1985ba3efe2b2471bdda |
| Docs | UNCLEAN (F1) | Added findings section, PR body, artifact hashes, public evidence inventory | R635-1 | 480c5e916f8bf711c47e1985ba3efe2b2471bdda |

## Validation and prior findings

`audit_receipts.py` and `replay_public.py` exit 0; raw output is in `audit.txt` and `replay.txt`, with explicit `.rc` receipts. `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 9ef71772` (315 added lines, zero findings), and `git diff --check 9ef71772 HEAD` pass. Initial TOC/em-dash attempts refused with rc 2 because the pinned renderer dependency was absent; these attempts are retained in `focused-gates.json`. An isolated environment under scratch, installed from the repository's hash-pinned Markdown requirements, produced the passing `markdown-gates.json` receipts. No shared installation was changed.

After the independent verdict and ledger above were written, the public PR comment, review and inline-review endpoints were checked again. They contained two review-start comments and no prior public findings or verdicts to resolve or retain. See `prior-review-inventory.json`. No other review report was consulted.

Reproduction uses the two immutable evidence commits linked above. Extract only B18's packet and B17's `author`, `author-r2` and `author-r3` directories into scratch. Run:

```text
python3 audit_receipts.py REPO B18_ROOT B17_AUTHOR B17_AUTHOR_R2
python3 replay_public.py B18_AUTHOR B17_AUTHOR SCRATCH_DIR
python3 verify_checkout.py REPO 480c5e916f8bf711c47e1985ba3efe2b2471bdda
```

`B18_ROOT` contains `MANIFEST.json` and `author/`; the replay's disposable copy belongs under scratch. No bench access is required. All publishable receipts are listed in `MANIFEST.sha256`; scratch is excluded.

## Limits and pending duties

This is a findings-only review with offline receipt checks, not a bench run or a fresh RTL proof. Raw tap captures are explicitly retained outside the public packet; their hashes and published reduced data were checked, not the underlying frames. No recentre firing is observed by a CSR. Counter timestamps cannot resolve an approximately 3 ms residual. Ten 32-second binds on one setup do not establish all phases, following-mode binds, the arming window, or release soak requirements. Physical calibration NOT RUN and field skips are not hardware proof.

There is no manager source-head bank claim in this review. Source-head gate evidence is the author's published `author/gates/gates.txt`; the manager still owns hosted/act acceptance and the current-dev candidate builder/native banks at the merge turn, with receipts linked then. No full banks, hardware, privileged operations, source changes, commits, pushes, or GitHub writes were performed. Required submodule gitlinks and exact tracked bytes/modes/index are checked in `checkout.txt`; submodules are uninitialized, so no submodule execution is claimed. Resolve F1, obtain the independent completion bar, validate the live-dev merge candidate, and perform authorized merge/containment before issue completion.

R635-1 FINISHED
