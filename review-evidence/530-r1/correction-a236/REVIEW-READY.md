[A236] REVIEW READY
Commit: `446e79b977640d13fa1e5dc0f9896d6c5a70391d` on branch `530-crf-talker-licence` (tree `9f1c9511`). This is docs-only correction round 1 for PR #549, answering R284-1 and R285-1 F1/F2 (the same two MINORs). It adds five one-line commits on the reviewed head `c593cbef`, ten in all on `50e78097`. Nothing is pushed, and the PR is not edited. The replacement PR body (starts `[A236]`, "Relates to #530"), the handoff and the receipts are in the `530-a236` packet.

Changed (comments and Markdown only; no RTL logic line, harness, Makefile, BDD step or gitlink):
- **F1, `9f607f7d`, `a018575e`, `446e79b9`.** The `milan_datapath.sv` SRP block now says that no shaper reads the raw verdict or the slope sum in this wrapper.
  - They reach one status word each: `lwsrp_slope_en` goes to `LWSRP_STATUS[9]`, and `lwsrp_idle_slope` to `LWSRP_SLOPE` `0x698`.
  - The bandwidth gate's "no stream transmits against an unbudgeted slope" invariant is scoped to the retained, uninstantiated chain. A later shaping lane must not inherit it.
  - The opening-edge corner is stated as its real effect. With a Listener Ready already registered at a fresh declaration, the gates and `LWSRP_STATUS[8]` can rise up to three admission rounds (`N_SOURCES` cycles each) before `[9]` and `0x698` include the stream. If the round refuses, ACTIVE falls inside the window and the declaration swaps to Talker Failed.
  - The same correction reaches the CHANGELOG line, the t>0 AAF SRP term (now named ACTIVE), the class-D face's consumer list, and the CRF row-map note that said the class-A queue budgets the CRF slope.
- **F2, `c08d7c09`, `1ac86025`.**
  - `ieee8021q.md` Q-9 names `srp_active_o` as the stream gate; `srp_sr_admitted_o` appears only as "the gate until #530".
  - `EGRESS_QUEUE_MAP.md` "Credit-based shaping" is scoped to the uninstantiated chain and gives the ACTIVE caveat.
  - The same stale claims are corrected where they recur on authoritative pages:
    - `ieee8021q.md`: the class-D summary line, the ordering bullet and Q-10;
    - `FR_NFR.md`: FR-SRP-01/02/03, which said the admission bit drives the AAF gate, and FR-CONN-01/02;
    - `REGISTER_MAP.md`: the slope-ordering paragraph, the LIVE list, `0x680[4:2]`, `0x694[9]` and `0x698`.
- The R285-1 S2 wording (the t>0 "bandwidth gate", `ieee8021q.md:35`) is taken with these fixes. The other suggestions sit in the Tests scope and are not taken, so that scope stays as banked at `c593cbef`.

Validation, all at `446e79b9` with a clean tree:
- `receipts/01-quick-gates.txt`, all rc 0:
  - `docs_check`, and `check_em_dash --base 50e78097` (0 findings);
  - `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_doc_paths` and `check_feature_status`;
  - `gen_module_matrix --check`, `DOC_MAP.gen --check`, `check_hygiene --check` and `check_wire_accountability`;
  - `check_rtl_source_lists`, `check_sv_idiom`, `measure_naming --check`, `check_port_contracts`, `measure_fail_fast --check`, `measure_test_evidence --check` and `check_todo_ownership`;
  - `git diff --check 50e78097 HEAD`.
- `receipts/02-xvlog-gate.txt`: `xvlog_gate.py --check` PASS, 4 findings == ratchet, 0 in `hdl/`.
- `receipts/03-hdl-comment-only.txt` (script `scripts/hdl_comment_only.py`):
  - `git diff -U0 c593cbef 446e79b9 -- hdl/` has 83 changed lines, and all 83 are `//` comments;
  - `milan_datapath.sv` with `//` comments stripped is byte-identical at both heads (sha256 prefix `ffabcf91a0d986e0` both sides). The built image is unaffected.
- `receipts/04-behave.log`: 317 scenarios passed, 0 failed. Those steps read `REGISTER_MAP.md` and the gate's source text.
- `receipts/05-scope.txt`: only `CHANGELOG.md`, five `docs/` pages and `milan_datapath.sv` change. There are 0 files under `tb/ tests/ scripts/ syn/ sw/`, the gitlinks are unchanged, and the commit bodies are empty.
- `receipts/06-claim-search.txt`: the reviewers' search at the new head. Every `sr_admitted`/raw-verdict hit is historical ("until #530", "read") or a status-only statement. Every slope-mux/unbudgeted hit is a "no shaper" statement, the retained chain in past tense, or the dated 2026-07-26 bench warning (below).
- `receipts/07-diff-c593cbef-to-head.patch`: the full correction diff.
- No simulation was rerun, because no logic changed. The `c593cbef` tallies (`crflic` 85/0, `crflic-mutants` 4/4, both failing arms) carry over.

Acceptance criteria:
- F1 (R284-1 and R285-1): met. No text claims that a shaper budgets or consumes the raw verdict or the slope in the shipping datapath. The real consumers and the corner's real effect are stated, and the RTL does not change.
- F2 (R284-1 and R285-1): met. No current-tense claim remains that `sr_admitted` is the stream gate, and the EGRESS_QUEUE_MAP sentence is scoped, with the caveat.
- #530 items 1 to 3: unchanged from `c593cbef`. The silicon rerun is pending and belongs to the manager.

Open risks/questions:
- The `[A229] REVIEW READY` comment on this issue still carries the superseded wording ("the CBS slope enable keeps the raw verdict", "before the slope joins the shaper's sum"). The corrected text is in the PR body and in this comment.
- Seen, not changed: `REGISTER_MAP.md` "Bench warning (2026-07-26 silicon)" still says the CBS slope mux disengages with the engine off. It is a dated silicon observation that predates the shaper's removal, not a claim about the raw verdict or the gate.
- Re-review: RTL and Docs at `446e79b9`. Conformance, Robustness and Tests were banked at `c593cbef`. The correction touches nothing in their scope (the RTL logic, the leg, the mutants, the Makefile and the BDD step).
- Not run: act/Docker, hosted CI, simulation, `syn/yosys`, hardware.
