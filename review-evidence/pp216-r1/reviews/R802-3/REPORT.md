[R802] POSITIVE - exact head 03862f75c89e5c1d84baa4735eff1c1c6f796e25

# R802-3: external independent review of processor issue #216 / PR #218, round 3 (docs-only delta)

- Exact head `03862f75c89e5c1d84baa4735eff1c1c6f796e25`, tree `dec0f2f79439b89af8686f87bd1db6653a0585fd`. The PR's `headRefOid` was this head at review time. Source base `044cb25f`.
- Delta reviewed: `84f6d6a..03862f7`. One commit, two files, both under `docs/`: `docs/00_MILAN_COMPLIANCE_REVIEW.md` +12 -1 and `docs/architecture/10_srp_engine.md` +11 -6.
- Authority: the round 3 ruling (issue #216, issuecomment-6751398007): option (a) of R802-2-F1, R802-2's exact fixes R1 and R2, docs only. Supporting sources: R802-2 (PR #218 issuecomment-6750781415), the author's round-3 receipts at kebag-logic/milan-fpga `6c2007ae`, `review-evidence/pp216-r1/author-r3/`, and the manager's comments on the PR.
- Token economy: the tree outside `docs/` is byte-identical to `84f6d6a`, so the round 2 RTL, test, campaign, area and scratch-parent results stand unchanged. Lenses that the delta does not reach keep their R802-2 verdict.

## Verdict

POSITIVE. All three ruling items are done at this head:

1. **F1.** The text no longer calls Flush! "a Registrar event only". The basis is now Table 10-3's missing Flush! row. The text discloses that 10.7.5.2 also signals leavealltimer! and that this engine does not.
2. **GAP-19.** It records the omission, its clauses and an owner.
3. **R1 and R2.** Both are taken word for word.

The gates pass on my run at this head:

- `make check`: rc 0.
- `gen_matrix --check`: rc 0.
- `git diff --check 044cb25f HEAD`: empty.

The RTL fact GAP-19 rests on also holds. `link_up_i` goes only to `u_domain`, `u_vlan` and `u_listener`. No LeaveAll driver in `KL_srp_top` reads a link edge.

Open items: two RESIDUE items and one SUGGESTION, none of which blocks.

- **R1.** GAP-19's owner cell and the PR body still say "owed, not filed". The manager filed #221 after this commit.
- **R2.** One reflow artefact in 10 §6.2.
- **S1.** The LINK_UP (Begin!) half that #221 also tracks.

## Ruling items and prior findings at this head

| Item | Severity at R802-2 | Status | Evidence |
|---|---|---|---|
| R802-2-F1: "Flush! is a Registrar event only (§10.7.5.2)" | MINOR | RESOLVED | `10_srp_engine.md:525-529` now says: "Table 10-3 has no Flush! row, so LINK_DOWN leaves the Applicants as they are … §10.7.5.2 also signals leavealltimer! to the LeaveAll state machine at a Flush!; this engine's LINK_DOWN does not, on either participant, since issue #216 changes no MRP timers ([00 GAP-19])". This is option (a) as I proposed it. The author's clause record (`author-r3/STANDARDS.txt`, hash checked against the evidence manifest) quotes the 10.7.5.2 second paragraph and the 10.7.5.22 and Table 10-5 rows behind the new sentence. The sentence also agrees with the existing 10 §6.5 text at `:1016-1019` ("leavealltimer! enters … or a Flush! on a topology change (§10.7.5.2)"). No other text in `docs/`, `hdl/` or `tb/` still calls Flush! Registrar-only (`grep -i "registrar event\|flush! is\|flush!.*only"` finds only code-section banners). |
| Ruling (1), the RTL basis | – | MET | `hdl/srp/KL_srp_top.sv:399,476,670`: `link_up_i` goes only to `u_domain` (`KL_srp_domain`), `u_vlan` (`KL_srp_vlan`) and `u_listener` (`KL_srp_listener_fsm`). The MSRP and MVRP LeaveAll machines live in `KL_srp_top`. Three things drive them (`:1138-1139,1201-1234,1309-1333`): a slot expiry (`CAD_LA_*`), a received LeaveAll (`dec_la_*`) and the tx! that sends `sLA`. A fresh draw (`need_draw_r`) is set only by an expiry or an rLA!. No link edge reaches any of them. So GAP-19's "leaves each on the `T-MRP-LEAVEALL` cycle it was on" is correct. |
| Ruling (2), GAP-19 and its owner | – | MET, with R1 | `00_MILAN_COMPLIANCE_REVIEW.md:384-392` (finding), `:546` (REQ-SRP-001 now also cites GAP-19, which the matrix gate needs; `matrix: 115 REQ rows, 19 GAP findings, OK`), `:609` (F00.2 row). **Owner judgement:** "owed, not filed" was correct at the commit. The head commit is dated 2026-11-09T22:14Z. When I searched, the only open issues on leavealltimer, LeaveAll, Flush or LINK_DOWN were #216, #220 (MSRP stream Applicants at LINK_UP, not LeaveAll) and #221. GAP-04's #78 and GAP-07's #81 are closed. The ruling said "If no open issue owns it, write 'owed, not filed' and I file it". The manager then filed #221 at 2026-11-10T00:03:38Z. #221 covers both link edges, and its done-means requires GAP-19's owner cell to link it. So no further filing is needed. The cell is now stale (R1). |
| R802-2-R1: "(below)" pointed at nothing about a link change | RESIDUE | RESOLVED | `10_srp_engine.md:536-537` matches the exact fix: "A link change does not reset `vid_sent_o`, the talker's streaming licence of [Join before the stream](#sec-10-join-before-stream) below." The anchor exists at `:554`. |
| R802-2-R2: one unwrapped 142-character line | RESIDUE | RESOLVED | `10_srp_engine.md:509-510` now breaks after "never JoinIn without IN.", with no other change. |
| R802-2-S1, S2, S3 | SUGGESTION | RETAINED, not this round | The ruling sends S1 and S2 to the merge residue checklist. S3 predates this PR. None of the three is affected by the delta. |

## Findings

### R1 - RESIDUE - GAP-19's owner reads "owed, not filed", but #221 now owns it

- Lenses: Docs.
- Where:
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:609`, last cell `owed, not filed`.
  - The PR #218 body, section "Known, recorded, not changed here", last bullet: "Recorded as GAP-19 in `docs/00_MILAN_COMPLIANCE_REVIEW.md`, owed and not filed."
  - The PR #218 body, section "Round 3 (docs only)", second bullet: "its F00.2 disposition row (owner: owed, not filed)".
- Evidence: #221, "MRP: link edges do not reach the LeaveAll and PeriodicTransmission machines (802.1Q-2018 10.7.5.1, 10.7.5.2)", is open. It was created 2026-11-10T00:03:38Z, after the head commit, and its body says "GAP-19's owner cell … links this issue".
- Impact: a tracking pointer is out of date. It changes no measurement, figure, verdict, test, code, generated artefact or clause claim. The text was right when it was written, as the ruling directed.
- Exact fix:
  - In `00:609`, replace `owed, not filed` with `[#221](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/221)`.
  - In the PR body, replace "owed and not filed" with "owned by #221", and "(owner: owed, not filed)" with "(owner: #221)".
- Verification: `make check` rc 0, with the links gate counting one more link.

### R2 - RESIDUE - reflow artefact in 10 section 6.2

- Lenses: Docs.
- Where: `docs/architecture/10_srp_engine.md:529-531`. Line 530 is just "over a received value of its clock," (35 characters), between lines of about 95 characters. The new sentence was inserted without re-wrapping the paragraph.
- Impact: source layout only. The rendered Markdown is unchanged.
- Exact fix: re-wrap `:529-532` at about 95 columns with no change to the words. For example, end `:529` at "...#gap-19))." and continue with "A link change wins over a received value of its clock, as on the Domain and the listener registrars, and comes before..." wrapped to the paragraph's width.
- Verification: `make check` rc 0, and `git diff --word-diff` shows no word change.

### S1 - SUGGESTION - the LINK_UP (Begin!) half that #221 tracks is not in GAP-19, and 10 §6.5 "from Begin!" can be misread

- Lenses: Conformance, Docs.
- Where:
  - `00_MILAN_COMPLIANCE_REVIEW.md:384`: the GAP-19 title and body cover LINK_DOWN only.
  - `10_srp_engine.md:518`: "This engine maps … LINK_UP to Begin!".
  - `10_srp_engine.md:1155`: "the MVRP participant sends a LeaveAll every `T-MRP-LEAVEALL` … from Begin!".
- Evidence: #221 says 10.7.5.1 Begin! would also restart the LeaveAll timer (Table 10-5) and the PeriodicTransmission timer (Table 10-6), and that this engine restarts neither at LINK_UP. It asks for that to be confirmed against the clause text, or for a reason why this half is not owed. The RTL agrees that no link edge reaches those machines (see the ruling (1) row above).
- Impact: the ruling scoped this round to Flush!, and an open issue now tracks the Begin! half, so this is not a defect at this head. But 6.2 calls LINK_UP a Begin!, so "every `T-MRP-LEAVEALL` from Begin!" in 6.5 can be read as "restarted at every LINK_UP", which the engine does not do.
- Suggested: when R1 links #221, either widen GAP-19 to "LINK_DOWN (Flush!) and LINK_UP (Begin!) do not reach the LeaveAll and PeriodicTransmission machines", or leave GAP-19 as it is and let #221 settle the scope. In 6.5, "from Begin!" could read "from reset (Begin!)" until #221 lands.

## The five lenses

- **Conformance.**
  - The new clause claims match the author's quoted clause record and the repo's own 6.5 text:
    - 10.7.5.2 second paragraph;
    - 10.7.5.22;
    - Table 10-5 leavealltimer! leads to "Start leavealltimer, Active", and Active's tx! is sLA;
    - Table 10-3 has no Flush! row.
  - GAP-19 is filed under REQ-SRP-001 (Milan Table 4.3 MRP timers), which is the right requirement. Its Cov value is unchanged, so it makes no new grading claim, and "none: the omission is not graded" says so.
  - Clean. S1 is optional.
- **RTL.**
  - No change: `hdl/` is tree `e9f53705` at both `84f6d6a` and `03862f7`, and the stat outside `docs/` is empty.
  - Statically re-checked the RTL fact behind GAP-19: the `link_up_i` fan-out and the LeaveAll drivers.
  - The R802-2 RTL verdict stands.
- **Robustness.**
  - No behaviour change.
  - The disclosed effect is bounded: at most one LeaveAll cycle keeps its old phase across a bounce. That matches #221's "at most one early or late own LeaveAll".
  - The R802-2 verdict stands.
- **Tests.**
  - No change: `tb/` is tree `a572a4c1` at both heads and `scripts/` is `0359d032` at both, so the round 2 suites, campaigns and probes stand.
  - Hosted run at this exact head: `docs-gates` and `portability` completed with success. `suites` was still `in_progress` when I checked, so it is not evidence here; the manager owns hosted acceptance.
- **Docs.**
  - The delta checked line by line against the ruling, both anchors (`#gap-19` at `00:384`, `#sec-10-vid-link` at `10:516`), and the PR body's claims about the round.
  - `make check` rc 0 on my run: `links: 1334 checked, OK`; `matrix: 115 REQ rows, 19 GAP findings, OK`; `req-tags: … OK`; ids, figures and AECP gates OK. Its log matches the author's published `make_check.log` apart from a pip notice.
  - `gen_matrix --check` rc 0: `matrix: OK (94 rows, 0 untested)`.
  - Comment rule: no source comment is added. The added docs lines carry no lane label, lane name, review round, reviewer ID or comment ID.
  - The PR body no longer gives 10.7.5.2 as the reason for the Applicants' behaviour: the `KL_srp_vlan.sv` bullet and the "Known, recorded, not changed here" bullet both cite Table 10-3.
  - Clean. R1 and R2 are RESIDUE only.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 optional) | 10 §6.2 new basis sentence against 10.7.5.2, 10.7.5.22, Table 10-3 and Table 10-5 (as quoted in `author-r3/STANDARDS.txt`) and 10 §6.5 `:1016-1019`; GAP-19 and its REQ-SRP-001 link; unchanged rows keep R802-2's verdict | R802-3 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| RTL | CLEAN | `hdl/` tree identical to `84f6d6a`; `KL_srp_top.sv` `link_up_i` fan-out (`:147,399,476,670`) and LeaveAll pending and draw drivers (`:1138-1333`), checked statically | R802-3 (static), R802-2 (behaviour) | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Robustness | CLEAN | no behaviour delta; the disclosed effect of the omission is bounded to one LeaveAll phase | R802-3, R802-2 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Tests | CLEAN | `tb/` and `scripts/` trees identical to `84f6d6a`; hosted check-runs at the head (docs-gates and portability success, suites in progress); R802-2 suites, campaigns and probes stand | R802-3, R802-2 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Docs | CLEAN (R1, R2 residue) | the full delta in 00 and 10; anchors; `make check`, `gen_matrix --check` and `git diff --check`; the author's round-3 receipts (15 files hash-verified against the evidence manifest; the published patch equals the local diff); the PR body's round 3 and known-limits text; the comment rule over the delta | R802-3 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |

## Commands and receipts

All runs were on the review clone at the exact head and tree:

- `make check`: rc 0, `receipts/make-check.log`.
- `python3 scripts/gen_matrix.py --check`: rc 0, `receipts/gen-matrix-check.log`.
- `git diff --stat 84f6d6a..03862f7 -- . ':(exclude)docs'`: 0 bytes, `receipts/nondocs-diff-stat.txt`.
- `git diff --check 044cb25f 03862f7`: empty.

The published evidence check is in `receipts/evidence-verify.txt`. `scripts/reproduce.sh <clone> <out>` re-runs everything above.

Restore: `make check` creates an ignored `.venv-wavedrom/` in the clone, and I removed it. Afterwards:

- `git status --porcelain --ignored` is empty;
- `git write-tree` = `dec0f2f79439b89af8686f87bd1db6653a0585fd`;
- the head tree has no gitlinks (no submodules to check).

Receipt: `receipts/restore-check.txt`. No probes or mutations were needed: every claim in the delta could be settled statically or by the gates.

## Real limits

- I did not read the IEEE 802.1Q-2018 text itself. The clause content comes from the author's published, hash-verified clause record and the repo's own docs, which agree with each other.
- No suite, campaign or Verilator build was re-run, because the tree outside `docs/` is byte-identical to `84f6d6a`. Round 2's executed results are carried forward, not re-executed.
- No manager source bank runs at this head, and I do not claim one. The hosted `suites` job had not finished when I looked.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry R1 (link #221 in GAP-19's owner cell and in the PR body) and R2 (the reflow) to the merge residue checklist, along with R802-2 S1 and S2 as ruled. S1 here belongs with #221.
- Hosted and act acceptance at this head, including the `suites` job that was in progress.
- At the merge turn, the current-dev merge candidate build: builder and native banks against live dev `123f57a922bf07476cd69f91867f3b6f07080804` from source base `044cb25f`, with receipts linked on the PR.

R802-3 FINISHED
