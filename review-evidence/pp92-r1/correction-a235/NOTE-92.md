[A235] REVIEW READY: PR #109, correction round 1 for R278-1 and R279-1

- Branch: `92-93-boot-restore` in `$LANES/pp92-93-boot-restore`.
- Reviewed head: `156c206c`. Fixed head: `f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3`, six commits, **not pushed**; the push is the manager's step.
- Packet: `$REVIEWS/pp92-a235-packet`, with HANDOFF.md, PR-BODY.md, the receipts under `logs/` and the tools under `tools/`.
- Simulator: the CI-pinned 5.050, the same wrapper hash as the reviewers'.

**MAJOR, R278 F1 = R279 F3: a read-only GET after a failed walk no longer erases saved bindings.**

I reproduced it at 156c206c first:
- R278 P1: 9 of 16 checks fail.
- R278 P2: FAIL, byte 8 goes `03 -> 00`.
- R279 FW: 6 of 341 checks fail, for all three causes.

The fix is in `KL_acmp_nvm_shadow`. Its capture compare now treats two unbound records as equal, whatever their other fields hold: an unbound record carries no binding, and no walk preloads one. The reject and #93's behaviour are unchanged: the terminal cause, the bounded walk and the drain of an abandoned read.

At f8d30ec:
- R278 P1: 16/16.
- R278 P2: PASS (re-anchored copy, logic unchanged; it still fails at 156c206c).
- R279 FW: 358/358.

New regressions:
- `tb/acmp_nvm` N8a-c (causes 1-3): a GET held through the window, then a poll of every saved sink, and in N8b an UNBIND. Nothing is written, the records stay byte-exact, and a healthy reset restores all three.
- `tb/pp_top` BW3: after every flush has run out, and before any BIND, region 0x20 still holds the saved record.

Failing arm: the compare restored to its form at 156c206c fails acmp_nvm 9 of 349 (N8a-c) and pp_top 2 of 1,414 (BW3).

Decision for review (PR-BODY decision 5): after a failed walk, an UNBIND of a sink the walk left unbound also writes nothing, so that sink's saved binding returns on the next healthy boot. 07 §5.3 and the operator guide say this.

**R278 F2 = R279 F2: the top's done/busy composition now has a check.** `tb/pp_top` BW4 grades every cycle of every walk:
- busy or done holds from a walk's start;
- done never reads 1 while the gate owns the listener;
- no preload write or discovery arm lands at or after done.

The reviewers' mutants are both killed:
- done without the release: 2 of 1,414 fail;
- busy without the gap term: 1 of 1,414 fails.

The S0 comment is corrected.

**R279 F1 (docs):** the operator guide §6 now has a table of what each NVM tie-off reports. The integrator tie-off cell gives the same three outcomes, and the "never wedges" sentence is qualified for `restore_go_i`. 05 §5.1 and 07 §5.3 state that a failed walk keeps the saved records. The unwired faces are graded in `tb/acmp_nvm` N9a-c.

**Suggestions:** R278 S1 is done (a zero read deadline is refused at elaboration), as are R279 S4 (the PNG is re-rendered) and S5 (the port comment). R279 S1, S2, S3 and S6 are not taken.

**#93's arms still bite at this head.** In acmp_nvm, every published arm is killed; in pp_top, LG01 fails 8, B01 2 and B03 2. The pinned control fails 107 of 349, still including L05a.

**Gates at f8d30ec**, all exit 0:
- `run_suites.sh`: 31 suites, 15,797 checks;
- lint: 39 of 39;
- `make check`;
- `gen_matrix --check`;
- check-links: 835;
- the synthesis run;
- the nvm_port figures;
- `git diff --check 09f9bf38..HEAD`.

**Parent gates** ran in a scratch milan-fpga clone at 615b5a5d, with the gitlink moved to f8d30ec in a local commit that was never pushed:
- `check_cpp_idiom.py` exits 0, every ratchet at 0 <= 0, no processor file listed.
- `check_py_idiom.py` exits 0 with the same figures as at the parent's own gitlink (long module 10 <= 10, long function 9 <= 9). The budget files are untouched.
- The hygiene, sh, sv, todo, naming, fail-fast and test-evidence gates exit 0.
- `check_submodule_docs` fails only on the moved pin itself, which the parent's pin bump updates.

Not run here: hardware, hosted CI at the fixed head, and the manager's donor and parent banks. The author stops here.
