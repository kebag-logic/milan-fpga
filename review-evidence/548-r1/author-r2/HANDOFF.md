[A285]

# Issue #548 / PR #556: Round 2 handoff

Branch: `548-ctlr-diag-zero`.
Head: `8544472a19a4b4d3853d64b15dea22f999372a32`.
Tree: `b7a11e8d2ac0d88826925877180806ee145208d8`.
Parent: `e41703b2948ef53e5cb0dd01a1e13c5632637615`.
Comparison base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
Commit: `Correct CTLR_DIAG structural-zero comments`.

The commit has one subject line, no body and no trailers.
The worktree and index are clean. The branch is one local commit ahead.

## Authority and disposition

- [Round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/548#issuecomment-5822084957).
- [Recorded STRUCTURAL ZERO decision](https://github.com/kebag-logic/milan-fpga/issues/548#issuecomment-5821224656).
- [R308-1 F1](https://github.com/kebag-logic/milan-fpga/pull/556#issuecomment-5821998048): MINOR, Conformance/RTL/Docs.
- [R309-1 F1](https://github.com/kebag-logic/milan-fpga/pull/556#issuecomment-5822082470): MAJOR, Conformance/RTL/Docs.

Both findings identify the same two comments. Their requested correction is implemented; independent delta review remains pending. Their original severities and lenses are retained here.

## Assigned items 1-3

1. Corrected only `hdl/common/csr/milan_csr.sv` comments at lines 761-765 and 2397-2401. Both blocks say the word is STRUCTURAL ZERO, reads zero because its source was deleted, the processor owns the monitor, and the address is retained for the ABI. Both reject treating zero as a measurement. The reserved `0x6F8`/`0x6FC` note remains verbatim. The Round 2 delta is 10 added and 8 removed comment lines; see [round2.patch](round2.patch).
2. Repeated the tracked-tree search below. No remaining current statement describes `CTLR_DIAG` or `0x6F4` as a live count. The surrounding paragraph qualifies the #117 read at line 471 as STRUCTURAL ZERO. The register-map gloss names other live registers while explicitly classifying this word as STRUCTURAL ZERO. `docs/history` is excluded and unchanged. The search covers all tracked parent-tree text, including code, tests and hidden directories; it does not recurse into gitlinks.
3. Proved comment-free identity against `573f0052a0e4412e81f0845438fcec2086ce5d55` across all 137 tracked `.sv`, `.svh`, `.v` and `.vh` files. Two differ only in comments; 135 are byte-identical. An independent diff check accepts only added/removed `//!` lines. An in-memory nonzero diagnostic tie is detected as DIFFERENT. All four gitlinks are unchanged. The Round 2 test harness, Makefile, tie and read decode are unchanged.

## Tree-wide search

Run from the candidate repository root. Exit status: 0 (matches found).
The complete output follows, without filtering.

```sh
rtk proxy git grep -nI -i -E "CTLR_DIAG|0x6F4|'h6F4|eviction count|probes sent|replies seen|controllers shed" -- . ':!docs/history/**'
```

```text
docs/findings/117_GPTP_SILICON_EVIDENCE.md:471:  `CTLR_DIAG` read 0 at 13:13 UTC.
docs/findings/117_GPTP_SILICON_EVIDENCE.md:524:- **DUT.** The grader passed 10 of 10 at 14:13 UTC. The console read the switch as grandmaster, `CLKV_STAT` `0x00010002`, `CRFT_CTRL` `0x3`, drop counters 0, `CTLR_DIAG` 0 (STRUCTURAL ZERO, not a measurement), `LINKG_STAT` `0x83` and `RST_EPOCH` 1. A 22 s tap capture around that read carried no AVTP stream.
docs/reference/REGISTER_MAP.md:188:  - [0x6A4  -  ACMP listener SM  (Milan v1.2 Section 5.5 listener, FR-CONN-01)](#0x6a4-----acmp-listener-sm--milan-v12-section-55-listener-fr-conn-01) -- **`ACMPL_STATE` no longer tracks PROBING/SETTLED -- take `bound` as the truth.** The processor publishes a bind record, not a state machine, so the ladder fields, the bound talker id, the counters and the walker forensics are structural zeros; bound, active and the CRF-sink bit are real. The Milan Table 7-156 stream counters, MAAP status, pilot tone, playback rails and ts_delta in this group are untouched and still live. **CTLR_DIAG (0x6F4) is STRUCTURAL ZERO; never read it as a measurement.** The departing-controller monitor lives in the protocol processor.
docs/reference/REGISTER_MAP.md:1244:| `0x6F4` | `CTLR_DIAG` | RO | 🔴 **STRUCTURAL ZERO**. Reads `0`; never read it as a measurement. The deleted local monitor's probe, reply and eviction counters have no replacement source for this word. The departing-controller monitor lives in the protocol processor |
docs/reference/REGISTER_MAP.md:1248:`CTLR_DIAG` (0x6F4) is **STRUCTURAL ZERO**. Its source was deleted;
docs/reference/REGISTER_MAP.md:1254:The processor exports no probe, reply or eviction count.
docs/reference/REGISTER_MAP.md:1255:The parent ties `aecp_ctlr_diag` to `32'd0`, preserving the address.
hdl/common/csr/milan_csr.sv:309:  //! CTLR_DIAG (RO 0x6F4): STRUCTURAL ZERO in milan_datapath (#548).
hdl/common/csr/milan_csr.sv:312:  //! but exports no probe, reply or eviction count. Zero is no measurement.
hdl/common/csr/milan_csr.sv:313:  input  wire [31:0]             i_ctlr_diag,
hdl/common/csr/milan_csr.sv:761:    //! CTLR_DIAG (RO 0x6F4): STRUCTURAL ZERO (#548).
hdl/common/csr/milan_csr.sv:768:    A_CTLR_DIAG   = 'h6F4,
hdl/common/csr/milan_csr.sv:2397:      //! CTLR_DIAG (RO 0x6F4): STRUCTURAL ZERO (#548).
hdl/common/csr/milan_csr.sv:2402:      A_CTLR_DIAG:  live_mux = i_ctlr_diag;
hdl/milan/milan_datapath.sv:1500:  //! CTLR_DIAG (0x6F4): STRUCTURAL ZERO, retained for the CSR ABI (#548).
hdl/milan/milan_datapath.sv:1502:  //! and KL_aecp_ca_originator; no probe, reply or eviction count is exported.
hdl/milan/milan_datapath.sv:1503:  wire [31:0]              aecp_ctlr_diag;
hdl/milan/milan_datapath.sv:2535:    .i_ctlr_diag          (aecp_ctlr_diag),
hdl/milan/milan_datapath.sv:3206:  assign aecp_ctlr_diag = 32'd0;
tb/verilator/milan_dp/sim_nxn.cpp:1596:        ck("[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic",
tb/verilator/milan_dp/sim_nxn.cpp:1597:           axi_read(0x6F4), 0);
```

## RTL identity proof

`PACKET` denotes this handoff directory; run from the candidate root.
The reproducer preserves strings and escaped names while removing comments, then drops blank lines and trailing whitespace. Its independent diff check additionally proves that every added/removed RTL line is `//!` prose.

```sh
rtk proxy python3 "$PACKET/rtl_comment_free_identity.py" 573f0052a0e4412e81f0845438fcec2086ce5d55 8544472a19a4b4d3853d64b15dea22f999372a32
```

Exit status: 0. Complete output:

```text
IDENTICAL hdl/common/csr/milan_csr.sv: base/head comment-free sha256 f0db9ee4568821b18140884344ce846e2be7e37ccbe9f5a8abebbed9c9a080fd
IDENTICAL hdl/milan/milan_datapath.sv: base/head comment-free sha256 240bdc8461fe69d92b22a7331261ea12b1cd1f45887d26ca5cb3a157aa2a3778
CONTROL: nonzero diagnostic tie is DIFFERENT (memory only)
DIFF: every added/removed RTL line is a //! comment
IDENTICAL: 137 tracked RTL files; 2 comment-only changes; 135 raw byte-identical files
Base: 573f0052a0e4412e81f0845438fcec2086ce5d55
Head: 8544472a19a4b4d3853d64b15dea22f999372a32
```

## Required gates

All commands ran in the foreground, without shell pipelines. Each gate had a 7,200-second wrapper timeout. The source bytes validated before the commit are exactly the committed bytes; committing changed no gate input. The em-dash and full-range diff gates ran after the commit.

| Command | rc | Result | Receipt |
|---|---|---|---|
| `rtk proxy python3 scripts/xvlog_gate.py --check` | 0 | PASS; 4 existing processor findings match the ratchet; 0 in parent RTL | [xvlog.log](xvlog.log) |
| `rtk proxy python3 scripts/check_rtl_source_lists.py` | 0 | 103 closure files; 4/4 consumer lists complete; existing 6 processor omissions recorded | [source-lists.log](source-lists.log) |
| `rtk proxy python3 scripts/check_sv_idiom.py` | 0 | 124 files; all idiom counts within their zero ratchets | [sv-idiom.log](sv-idiom.log) |
| `rtk proxy python3 scripts/lint_rtl.py --check` | 0 | PASS; 90 existing violations match ratchet 90; 17 waived | [lint.log](lint.log) |
| `rtk proxy python3 scripts/docs_check.py` | 0 | 0 findings; 165 Markdown files; 858 text files; scrub 23/23; routing 4/4 | [docs-git.log](docs-git.log) |
| `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | 0 findings; 165 Markdown files; 863 text files; scrub 22/22; routing 4/4 | [docs-no-git.log](docs-no-git.log) |
| `rtk proxy python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | 0 | 0 findings; 339/339 arms; 20 added lines in 2 Markdown pages | [em-dash.log](em-dash.log) |
| `rtk proxy git diff --check` | 0 | No whitespace errors | [diff-worktree.log](diff-worktree.log) |
| `rtk proxy git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD` | 0 | No whitespace errors across the complete PR delta | [diff-check.log](diff-check.log) |

The no-Git run sets `GIT_DIR=/dev/null` only for that command. This activates the same filesystem inventory used by the no-Git CI mode without removing this worktree's metadata or creating another checkout. Its one skipped inventory-parity arm requires Git; the Git-mode run passes that arm.

The em-dash gate used the hash-locked Markdown dependencies from `tools/markdown/requirements.txt` in temporary scratch space outside this packet. Reproduction setup:

```sh
rtk proxy python3 -m venv "$A285_MARKDOWN_VENV"
rtk proxy "$A285_MARKDOWN_VENV/bin/python3" -m pip install --require-hashes -r tools/markdown/requirements.txt
rtk proxy env PATH="$A285_MARKDOWN_VENV/bin:$PATH" python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55
```

Set `A285_MARKDOWN_VENV` to a disposable directory outside the packet. No toolchain, SDK, virtual environment or tree export is stored in this packet.

## Handoff state

[final-state.txt](final-state.txt) records the clean head, changed path and unchanged gitlinks. [PR-BODY.md](PR-BODY.md) contains the full current public body fetched through `gh pr view 556 --json body`, with the author prefix, status and short Round 2 section updated. `Closes #548` is retained. The public PR body was not edited.

The behavioral sweep and mutation results in that body are retained Round 1 evidence. This round ran only the assigned gates and identity control. No hardware or new behavioral campaign ran. No push, PR edit, merge, sub-agent or other checkout was used.

The manager owns publication and subsequent acceptance. Delta reviews by [R308] and [R309] remain pending under the assignment; this handoff grants no review verdict or completion ledger. No open implementation question remains within items 1-3.
