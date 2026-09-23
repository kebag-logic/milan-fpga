[A209] Retire gate 1b's text rules onto per-selection grading, `-E`, `-H` and the resolved store census (#408, #409)

## Contents

- **[Status](#status)** -- Tally, compiler environments and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The two issues this closes, executor and reviewers.
- **[Description](#description)** -- The rule-by-rule ledger: retired, narrowed or kept, with the replacing instrument, the accepted case and the hostile controls.
- **[Authoritative references](#authoritative-references)** -- Issues, prior PRs and the page this edits.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules, pinned SDK.
- **[How to validate](#how-to-validate)** -- Commands and expected results in both compiler environments.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What stays a cost, and what a runner without the compiler does not get.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN locally at `a13b6e2e461695cdb8d978444ae499a5a6745429`, one commit on dev `759da623`. `408-409-boot-gate-retire` -> `dev`.

| Run | Pinned RV32 SDK mapped (`--require-rv32`) | Every cross compiler hidden |
|---|---|---|
| gate 1b, `sw/builder/test_firmware_compiler.py` | exit 0, 228/228 mutations, 27/27 firmware + 4/4 Makefile edits accepted, 0 NOT RUN | exit 0, 167/167 mutations, 27/27 + 4/4, 1 registered NOT RUN |
| dev `759da623`, same driver | 217/217, 17/17 + 4/4 | 182/182, 17/17 + 4/4 |
| whole `sw/builder/test_builder.py` | exit 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, no Vivado report here, as on dev) | exit 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's compiler arm, gate 11) |

## Linked Issue / roles

Closes #408
Closes #409

Executor: `[A209]`
Internal cleared-context reviewer: assigned by the maintainer
External reviewer: assigned by the maintainer

## Description

#504 made both hosted builder consumers require the pinned RV32 SDK, so the instruments PR #498 added beside the text refusals now answer wherever a merge is graded. This retires the refusals #408 and #409 name onto those instruments, rule by rule, with no fallback arm: a retired rule is gone on every machine. Where no RV32 compiler answers, its replacement is a registered `NOT RUN` and its mutations are counted as skipped, never as coverage.

One new instrument carries the conditional-reach ban. **Every preprocessor conditional is graded one arm selection at a time**: each group is resolved to each arm (and to no arm without an `#else`), and each resulting text is graded by the whole gate as a firmware of its own. The product builds one of the graded firmwares whatever its headers select. That closes what PR #498's arm BOUND could not: `if (\n#ifdef CSR_UART_BASE\n0 &&\n#endif\n!verified) return;` in the choke point names nothing the file defines and moves no boot token. It is now refused in the selection that takes the arm. The verifier's QSPI-slot group and `#error` guards are left as written; the verifier's other arm is pinned to a literal `printf` and `return 0;`.

Accepted cases were measured RED at `759da623` on the retired rule's own sentence, with and without the compiler, and are GREEN in the gate's accepted-case loop in both environments. "Disconnected" is the same mutation subset run with the replacement patched out, at `a13b6e2e`.

| Rule (page row at 7fd04d45) | Verdict | Replacing instrument | Accepted case | Hostile controls | Disconnected |
|---|---|---|---|---|---|
| no `#if` reaching the six boot-path bodies (565) | RETIRED | per-selection grading: text rules everywhere, `-E`, census and resolver with RV32 | "an #ifdef around a debug printf INSIDE milan_init()"; "a benign statement in an arm the census tree drops, inside configure_fabric()" | 15 (6 without RV32), each pinned on the selection's sentence AND the property | all 15/6 fail their pin; 4 pass the whole gate (the `0 &&` choke-point arm, product-only pasted enable, fifth cast, `lui` store), 1 without RV32 (pre-AEM clear) |
| a conditional carrying `#define`/`#include` (565) | NARROWED to the verifier group and `#error` guards | per-selection grading elsewhere | "an #ifdef/#else choosing a #define, read in a UART command handler" | `#define` in the verifier group (GREEN on dev, RED now); ADP_CTRL's name moved by a product-only arm | kept half is a text rule |
| token-joining backslash-newline (564) | RETIRED | `-E` comparison in the boot-path bodies, resolved census elsewhere | "a token-joining backslash-newline inside a macro body" | five phase-2 splices, three in arms, one in a UART handler, a spliced `PP_CTRL` redefinition | `-E` + census + resolver: 12/12 pass; `-E` alone: 10/10 still refused, by the resolver |
| `##` (585) | RETIRED | the same two | "a ## token paste building a call outside the boot path" | pasted call name; pasted in a dropped arm; pasted in a product-only UART arm | in the 12/12 above |
| `%:` / `??` (585) | KEPT | none | none: no edit anybody writes; the address model's `#define` reader does not translate them | digraph-pasted call name; digraph and trigraph includes | none |
| read-only `#define` accessor (584) | NARROWED: macro bodies may not name `milan_write()`/`milan_reg()` | the read rules fail closed | "a read-only #define accessor over milan_read()" | macro hiding the store; store value built in a read macro; identity forged through a read macro | text rules |
| `#pragma`/`#line`/`#undef`/`#include_next`/extra `#error` (566) | KEPT, reason restated | none | none | existing directive mutations | none |
| directory listing pin (568) | RETIRED | `-H`: the path opened and the file it reached | a `README` and a `notes.txt` beside the firmware | `command.h`, `init.h`, a LINK to a file outside the repository | 3/3 pass |
| `#include` name set (567) | KEPT (name pin), `-H` caveat at site and page | none | none: an unresolvable name cannot be measured by `-H` | unchanged | none |
| ordered pointer-cast set (563) | RETIRED | resolver store census | "a fifth cast to a pointer, resolving outside the window" | widened, reordered, local-pointer casts; fifth cast in a product-only arm | census + resolver: 10/10 pass |
| ordered pointer-store set (563) | RETIRED | the same | "a fifth store through a pointer, resolving outside the window" | the same, plus the census- and resolver-only shapes | as above |
| ordered-list comparison, reorder (583) | RETIRED | the same | "parse_u64() and seconds_to_ns() exchanged, with nothing added or removed" | the sets' entries | as above |
| inline-`asm` set (563) | RETIRED | the same, reading the template | "a fifth inline-asm statement, a fence in a UART command handler" | `asm` store by literal address; `lui` template; `lui` in a product-only arm | as above |

`assert_rejected` now takes a tuple of reasons that must all be carried, with a negative control proving one missing reason fails. The `-H` measurement now judges the path opened as well as the file reached, which closes a link planted beside the firmware to a file outside the repository. `docs/integration/BAREMETAL_FIRMWARE.md` carries the ledger in the #153 pattern, the caveats of `-E` and `-H`, and the weaker no-compiler statement. `docs/testing/CI_WORKFLOWS.md` no longer says every text refusal remains active.

## Authoritative references

- #408 and #409, their bodies and the remaining-scope comments after PR #498.
- PR #498 and its reviews: R213 and R214 on `1540fe97` (B8, B9, B10, the forced fallback arm), R213 on `f8b8c0fe` (the literal-argument arm), both POSITIVE on `02c47cf0`.
- #504 / PR #521: the pinned Bootlin RV32 SDK, `--require-rv32` on both hosted builder consumers, and the compiler-absent docs control.
- PR #241: the #153 retirement pattern.
- `docs/integration/BAREMETAL_FIRMWARE.md`: editing contract, cost table, and "Text rules retired onto instruments".

## How to get into the same state

```sh
git fetch origin 408-409-boot-gate-retire && git checkout a13b6e2e461695cdb8d978444ae499a5a6745429
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination <sdk-dir> --verify-only   # the pinned SDK
```

## How to validate

```sh
python3 sw/builder/test_firmware_compiler.py --sdk-destination <sdk-dir> --audit /tmp/sdk.jsonl
python3 sw/builder/test_firmware_compiler.py --absent --audit /tmp/absent.jsonl
python3 sw/builder/test_builder.py --require-rv32        # with the SDK at the selector
python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest
python3 -B scripts/docs_check.py && python3 scripts/check_em_dash.py --base 759da623
```

Expected result / pass criteria: exit 0 everywhere. Gate 1b reports 228/228 with the SDK and 167/167 without it, 27/27 and 4/4 in both. Without the compiler the verdict reads `TEXT RULES ONLY, AND WEAKER`, with one registered NOT RUN naming the three instruments.

## Known limitations / out of scope

- Without an RV32 compiler nothing refuses a token-joining splice, a `##` paste, a file beside the firmware, or a cast, store or `asm` the resolver would place in the window. That is a registered `NOT RUN`; the hosted builder jobs require the compiler.
- #409 acceptance 4, the two stores planted inside the address helper: the whole-gate entries are pinned on the helper's return-provenance rule. That surviving text rule answers first on every machine, including without a compiler. The resolver's refusal of the same two, on `STORES into the Milan CSR window`, is asserted on every compiler run by the blindness control. This lane reads that as meeting "move to the census's message"; the reviewers decide.
- Kept costs: `%:`/`??`; the directive set; the include name pin; the verifier's no-QSPI arm; more than 16 arm selections; a disabled `#if 0` block graded as code. Factoring the accessors and hoisting the enable mask stay costs, as #409 scopes them.
- Measured, pre-existing, not changed here: a plain second `#define` of a register name passes the text rules without a compiler, on dev too; the resolver refuses it.
- The `-E` caveat: a macro whose definition differs between the census stub tree and the product is outside the comparison.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (see the ledger; #409 acceptance 4 as stated above)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
