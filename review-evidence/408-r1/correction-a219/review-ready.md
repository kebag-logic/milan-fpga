[A219] REVIEW READY
Commit: ef9034578f97ebc2951801d867b7c57f8196423d
Branch: 408-409-boot-gate-retire (PR #535), three commits on the reviewed head a13b6e2e, base dev 759da623. Not pushed; the PR is not edited. The replacement PR body, the handoff and every receipt are in the A219 packet for the manager to archive (`receipts/README.md` indexes them).
Authoritative references: #408 and #409 (acceptance 4 "No reduction"), the assignment https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5802875987, R272-1 https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5802602464, R273-1 https://github.com/kebag-logic/milan-fpga/pull/535#issuecomment-5802871665.
Interpreted scope: fix every R272-1 and R273-1 finding under its own severity and lens, and restore a retired rule where its replacement cannot carry what it refused. The splice and `##` bans are restored inside the six boot-path bodies for that reason; nothing else needed restoring.

Changed: `sw/builder/test_builder.py` (gate 1b) and `docs/integration/BAREMETAL_FIRMWARE.md`.

| Finding (severity, lens as the reviewer filed it) | Fix | Controls that fail when the fix is removed |
|---|---|---|
| R272 F1 BLOCKER (Conformance, Robustness, Tests, Docs) | One lexer, `c_lexed()`, built to the pinned GCC 14.3 `-std=gnu99` as measured: LF, CRLF and lone-CR line ends; form feed, vertical tab and NUL are whitespace before and after `#`; comments before `#` on one or several lines; splices in comments, literals and directive names. Every C directive reader shares its view and one anchor: the conditional readers, `#error`, the directive-set closure, the include pin, `#undef`, the keyed-condition reader, the surviving-directive check. Every definition reader, the macro-body rule included, reads the phase-3 text. `spliced()` rejoins a name a splice splits. Trigraphs are not translated, as under gnu99, and are refused anywhere. A 55-spelling corpus recorded from the pinned GCC is read by the readers on every run and re-measured on the compiler. The `0 &&` product-only arm is refused behind a form feed, a vertical tab or lone CRs. | 15 table entries with the SDK, 9 without, plus the corpus, which fails on its own sentence. The name rejoin has the spliced-`#else` arm and the corpus. |
| R272 F2 MAJOR (Conformance, Robustness, Tests, Docs) | The token-joining splice ban and the `##` ban are KEPT inside the six boot-path bodies and every macro they name at any depth. The `-E` retirement is narrowed, and the site, the page and the gate print say so. Outside the six bodies both stay retired onto the resolver. | 13 entries in both modes: the ten old splice and paste entries re-pinned onto the kept bans, and the identity sample forged by a splice, a paste and a nested paste. `-E` keeps an entry it answers first: a boot step erased by a macro of its own name. |
| R272 F3 MINOR (Conformance, Docs) | Groups asking only whether one macro is defined are graded together, as the builds that exist. The selection sentence now reads `graded as a firmware of its own` and no longer claims the product builds that combination. The remaining cost is in the page and the gate print, with its remedy. | The two correlated debug edits are accepted cases, GREEN in both modes and refused with the relating removed. A store in the second of two groups on `CSR_UART_BASE` is still refused. |
| R272 F4 MINOR (Robustness, Docs) | An open literal ends at its line end, as in GCC. An open literal, a raw string and a trigraph are refused before any reader runs. The "every conditional is graded" claim is bounded to the measured lexer at the site and in the page. | 4 entries in both modes. |
| R273 F1 MINOR (Conformance, Robustness, Tests, Docs) | (a) One `#define` per name on every machine, which refuses H6 and H7; the macro-body rule's reason is restated. (b) The registered NOT RUN text, the verdict's first clause and the page's compiler-absent section now name the splice and `##` outside the six bodies, and the reach ban's compiler half (`0 &&`). | 4 entries in both modes. |

Validation (receipts in the packet, all at `ef903457`, Verilator 5.050, SDK verified with `--verify-only`):
- `python3 -B sw/builder/test_firmware_compiler.py --sdk-destination <sdk>`: exit 0. 255/255 mutations, 29/29 firmware and 4/4 Makefile edits accepted, 55/55 lexer spellings re-measured, 0 NOT RUN.
- `... --absent`: exit 0. 198/198, 29/29 and 4/4, one registered NOT RUN (33 census and resolver entries plus 24 retired-rule entries skipped). Dev: 217 and 182, with 17 and 4 accepted.
- Whole `sw/builder/test_builder.py`, SDK mapped with `--require-rv32`: exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no local Vivado report).
- The same with every cross compiler hidden: exit 0, `EXCEPT 2 NOT RUN`.
- 38 static commands exit 0: `docs_check`, `check_em_dash --base 759da623`, doc style, TOC, doc paths, `check_baremetal_only --check`/`--selftest`, `test_firmware_compiler --selftest`, hygiene, `check_py_idiom`, the naming, fail-fast, test-evidence, control-flow and cohesion ratchets, and `git diff --check`.
- Every R272-1 and R273-1 case (51 hostile, 19 accepted) and R272-1's four listed pre-existing gaps were graded at dev, at `a13b6e2e` and at `ef903457`, each with and without the compiler.
  - With the compiler, nothing dev refused is accepted here. Twelve cases dev accepted are refused, H7, H9, H12-H14 and V4 among them.
  - Every accepted case is GREEN in both modes.
  - Without a compiler, the 21 cases dev refused and this head accepts are exactly the shapes whose replacement needs the compiler (the registered NOT RUN, now named where R273 asked).
- Disconnect matrix over the 43 round-two controls: nothing fails connected, and each fix's controls fail with it removed (table above; `disconnect/final/TABLE.md`).

Acceptance criteria: #408 1, 3 and 5 are met. #408 2 is met: 564 and 585 are narrowed rather than retired, with their accepted cases still GREEN. #408 4 is met: the count is 255 with the SDK and 198 without, and every entry is re-pinned on the rule that answers it. #409 1 to 5 are met as in round one; #409 acceptance 4 was judged satisfied by both reviews and is unchanged.

Open risks/questions:
1. The lexer is pinned by a fixed corpus, not by a per-firmware compiler oracle. Two oracles were measured and rejected. `-fdirectives-only` does not honour a NUL before `#`, which normal preprocessing does. Normal `-E` is not line-aligned across a multi-line macro invocation. A spelling outside the corpus that GCC reads differently is outside the measurement.
2. New costs, disclosed in the page and the gate print:
   - a second `#define` of any name, an identical one included;
   - an open literal (an apostrophe in an `#if 0` block included) and a raw string;
   - a trigraph anywhere;
   - a continued macro body naming `milan_write()` or `milan_reg()`;
   - a helper split across two conditionals that are not both a bare `defined` test of one macro.
3. Pre-existing and not fixed; both reviews ask for a public Issue:
   - a plain function-like macro forging the identity sample (R272 r3, R273 V2c). It is stated as a bound in the page row.
   - R273-S3 (H8) is also unchanged.
