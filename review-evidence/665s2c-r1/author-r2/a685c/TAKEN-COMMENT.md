[A685c] TAKEN

Branch: `665-s2c-icache` (local, not pushed), round-1 head `a611785f` (PR #796, base `dev-soft-core`, stacked on PR #792 at `f58d049b`). New commits go on top; the manager pushes.

Authoritative references: this round's assignment (issuecomment-6433542516); R713-1 (PR #796 issuecomment-6433539808) and R714-1 (PR #796 issuecomment-6433362127); the S2c assignment (issuecomment-6421463860); `docs/reference/FR_NFR.md` NFR-SCOUT-01 and 3.4.1 (T_svc = 10 ms).

Interpreted scope:
- R713-1-F1: the six unbounded rows in the two "Paths that still miss T_svc" tables carry S2's labels ("at least X, never answered" or "at least X, never released") in both ms columns, and their cycles cells are marked the same way.
- R713-1-F2 and R714-1-F2: the README states the measured block-RAM rate: one tile for each 4 KiB of data, half a tile of tags, and half a tile more for each extra way.
- R713-1-F3: every S2 reproduction command on the README page (the controls, the fixture regeneration and the Results block) selects `--fetch-l1 none`, so each command matches the cacheless figure printed beside it.
- R713-1-F4: a self-test check drives `run.main()` on a temporary attested `build.json` that records another fetch L1 or arm, and asserts the refusal. A second check runs `build.build()` with its toolchain steps replaced and checks what `build.json` records for `fetch_l1` and `xip`. Each part has a mutant, and both reviewer source mutants are replayed on a disposable copy, where they must be killed.
- R714-1-F1: `test_soc_options.py` pins the split CPU's options literally (64 sets, 1 way, no LSU L1), and planted geometry changes are killed controls.
- Residue: R714-1 RES1 and RES2, and R713-1 RS1 to RS4, as written. The two reviews give different exact text for `build.py:149`. I apply RES1's "(#665, decision D3)", which keeps the D3 citation on line 153. R713-1's alternative is recorded in the handoff.
- No new measurement, no measured cycle count changed, no firmware, mailbox or product change.

Validation plan: `run.py --self-test` (all checks pass, every mutant caught); the reviewer mutants replayed on disposable copies; `sw/builder/test_soc_options.py` with the geometry probes; `scripts/check_baremetal_only.py --check`; the docs gates; `cd tests && behave`. Every gate runs in the foreground, unpiped, and must return rc 0.

Blockers: none.
