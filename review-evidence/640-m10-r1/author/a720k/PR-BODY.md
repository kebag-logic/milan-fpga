[A720k]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, documentation only -- every run step of the docs workflow exits 0 on a clean clone of head `3f8ed303e01285f1bad0641f4ebc05764f162467`, including both builder legs (54 recorded steps, all rc 0), and `git diff --check` against the merge base `503bc97c` is clean -- `640-charter-followup` -> `dev`.

A small follow-up to the Mark II charter (PR #828, merged as `503bc97c`). Four Markdown pages change; no RTL, firmware, generator, gate or configuration file.

`docs/design/AREA_BUDGET.md` and `docs/design/MAILBOX_SPLIT.md` are gate-read pages (`scripts/ci_scope.py`), so CI does not classify this PR as docs-only. Their readers pass at the head: `pp_resource_gate.py check-baseline` ("baseline PASS: 3 endpoints") and the `ctrl_service_bounds` arm (47 checks, 0 failures). Neither reads a changed line.

## Linked Issue / roles

Relates to #640
Relates to #495

Executor: `[A720j]`, then `[A720k]` for the second pass
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

Five items, one commit each, all in `docs/design/MARK_II_AREA_PLAN.md` except the last. A second pass then adds two commits on the same page, from the manager's answer on #640 (issuecomment-6575277828).

| # | Item | What changed |
|---|---|---|
| 1 | Lever 4 accounting | `MilanSoC` under `--ctrl-mailbox` has always built one hart, so the owner's 34.2k start counted the split CPU (3,948 LUTs) on top of the SoC CPU the 52,008 basis already holds (3,249). Without the double count the start is 30,974 (derived). Lever 4 saves 0: it is an accounting correction. After lever 4 both chains reach 27,224 (derived). The owner's middle 3.55k overstated the 3,249 by about 0.3k, so the central totals from lever 4 on rise about 0.3k: the six levers reach about 21.0k and the 32x32 estimate about 21.75k (was 21.45k). Each derived figure is marked and names its netlist rows. |
| 2 | LiteX block census | A short table of every LiteX block the shipping 1x1 SoC builds, from the basis build's module tree and `milan_soc.py`, with the stage that removes it and its fate: removed with nothing in its place, replaced by a named first-party block, or replaced by a donor core under the owner's stage 2 decision. Placed rows are cited where the hierarchy has them; the LiteX top is one flat row. The owner's 2026-11-02 decisions are recorded as D18 to D20, linked to the comment on #640 that records them. |
| 3 | Console UART | A small first-party UART, transmit and receive only, no RTS/CTS. Receive is polled once per pass. At 115,200 baud a character takes 86.806 µs. The stage 1 probe's 16-byte FIFO lost characters on 17 of 300 22-character lines and none of 300 14-character lines. One pass fits the 2.0 ms per-pass share, in which 24 characters can arrive, so the buffer is 32 bytes (covers 2.778 ms). Console loss beyond that bound is accepted; console work never stretches a service bound. |
| 4 | LiteX stage 1 | The boot loader copies the firmware image from QSPI flash into Block RAM (owner, 2026-11-02); the image has its own flash slot (D21, below). Masters use the SoC bus, never the CPU's DMA port: the stage 1 probe measured that route hanging (3 reads issued, none answered; 311 of 311 on the SoC bus). The cause is not established, and the page says it is a measurement, not a diagnosis. |
| 5 | #828 residue listed on #495 | `AREA_BUDGET.md`: "the accepted target"; the acceptance bar adds Block RAM and timing. `MAILBOX_SPLIT.md`: the placement pointer "defines the transition and end state"; the event record's grandmaster source and the fabric paragraph say "until #665 lane F6". `docs/findings/README.md`: the stale gap is the gap to NFR-RES-01's former 60 % target. Where the exact text broke the 10-word sentence or 20-word paragraph limit, the paragraph is split with the same content. |


Second pass:

| # | Item | What changed |
|---|---|---|
| 6 | D18 to D20 links | The three decision rows link to issuecomment-6575277828, which records the owner's 2026-11-02 decisions. |
| 7 | Firmware flash slot | The manager's decision of 2026-11-02 is recorded as D21: the firmware image gets its own flash slot, sized for the image, in a free erase-aligned range that is neither reserved (`journal`, `user`) nor used. The bitstream and AEM slots keep their offsets and budgets. The image does not go in the bitstream slot's tail, which would tie its offset to the bitstream's size. Open decision 4 and every statement that the layout stays as is are removed: the stage 1 table row and text, the D18 consequence, the stage 1 lane's dependency. The offset and budget are not chosen here: the stage 1 lane states them in `FLASHBOOT_LAYOUT` and the generated layout page. `QSPI_FLASHBOOT.md` still describes the shipping layout, unchanged until stage 1 lands. |

## Authoritative references

- #640's body and its comments from 2026-10-31 on: the target (issuecomment-6545523624), the lever order (issuecomment-6545540394), the LiteX stages (issuecomment-6545999204), the core survey (issuecomment-6551164172), the stage 1 probes (issuecomment-6555550136, issuecomment-6556743957).
- The owner's decisions of 2026-11-02 07:21 (stage 1 copies the firmware from QSPI flash into Block RAM; every LiteX peripheral removed) and 07:22 (a first-party UART, transmit and receive only, no RTS/CTS). Recorded on #640 (issuecomment-6575277828).
- The manager's decision of 2026-11-02 on where the copied firmware sits in flash (#640 issuecomment-6575277828).
- #665: one hart under `--ctrl-mailbox` and the split CPU's netlist rows (issuecomment-6569635407); T_svc = 20 ms (issuecomment-6495692075); the 2.0 ms per-pass share (issuecomment-6514866239).
- #495: the #828 residue (issuecomment-6573412222).
- `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/MARK_II_STREAM_ENGINES.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/AREA_BUDGET.md`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/integration/QSPI_FLASHBOOT.md` at `503bc97c`; NFR-RES-01 and NFR-SCOUT-03 in `docs/reference/FR_NFR.md`.

## How to get into the same state

```sh
git fetch origin
git checkout 640-charter-followup
git rev-parse HEAD        # 3f8ed303e01285f1bad0641f4ebc05764f162467
git merge-base HEAD origin/dev   # 503bc97cd4f24ad07596c17e7188f2024617972d
git submodule update --init gptp-processor protocol-processor third_party/tsn-c-stack third_party/verilog-axis
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 503bc97c
python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest
python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
git diff --check 503bc97c HEAD
python3 syn/ooc/pp_resource_gate.py check-baseline
# every changed prose block of the four pages against the style limits:
python3 - <<'EOF'
import re, subprocess, sys
sys.path.insert(0, "scripts"); import check_doc_style as c
for page in ["docs/design/MARK_II_AREA_PLAN.md", "docs/design/AREA_BUDGET.md",
             "docs/design/MAILBOX_SPLIT.md", "docs/findings/README.md"]:
    diff = subprocess.run(["git", "diff", "-U0", "503bc97c", "--", page], capture_output=True, text=True).stdout
    added = set()
    for m in re.finditer(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M):
        added.update(range(int(m.group(1)), int(m.group(1)) + int(m.group(2) or 1)))
    text = open(page).read(); lines = text.splitlines()
    for f in c.analyze(text):
        end = f.line
        while end < len(lines) and lines[end].strip() and not lines[end].lstrip().startswith(("#", "|", "-", "```")):
            end += 1
        if any(f.line <= n <= end for n in added):
            print(page, f.line, f.reason)
EOF
```

Expected result / pass criteria: every command exits 0, the style probe prints nothing, and `check-baseline` prints "baseline PASS: 3 endpoints". The full docs workflow, both builder legs included, is in the author's evidence.

## Known limitations / out of scope

- **The firmware slot's offset and budget are not chosen.** D21 fixes where the image goes in principle; the stage 1 lane states the numbers in `FLASHBOOT_LAYOUT`. `QSPI_FLASHBOOT.md` is not edited: it describes the shipping layout.
- **The console buffer rests on the 2.0 ms per-pass share,** which the S2b lane (PR #810) carries and dev does not yet publish. At 32x32 the S2b estimates exceed the share; console loss is then accepted by rule.
- **The SPI flash donor is not chosen.** The fate is the owner's stage 2 decision; the core survey found no AXI core with both 7-series use and an active maintainer.
- **#640's body still shows the owner's 34.2k chain.** The plan corrects it; the issue body is not part of this PR.
- Not taken from the #495 list: the optional `SYSTEM_INTEGRATOR.md:95` and `BUILD_FLASH_BOOT.gen.py:44` items, PR #828's body, and the round-10 evidence prose.
- No figure is re-measured: every number is a recorded measurement or derived from one.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
