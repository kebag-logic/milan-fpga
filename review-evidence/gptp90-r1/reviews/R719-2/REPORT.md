[R719] NEGATIVE - exact head 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e

# R719-2 independent review: FPGA-gPTP PR #92 (issues #89, #90, #91)

- **Under review:** repository Mister-M-alt/FPGA-gPTP, PR #92.
  - Head `4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e`, tree `f7731898626419ec3bdb9a025077c39992d00b75`.
  - Source base: main `55680bff`.
  - Previously reviewed head: `d27a1654` (R719-1 and R720-1).
- **Role:** internal independent reviewer, cleared context, round R719-2. Lenses: Conformance, RTL, Robustness, Tests, Docs.
- **Scope:**
  - issue bodies #89, #90 and #91;
  - the round-1 assignments (#90 issuecomment-6434675577, #89 issuecomment-6434676256, and the two scope additions);
  - the round-2 assignment (#90 issuecomment-6442857175);
  - the PR body at this head;
  - `git diff 55680bff..4d8fb902`, whose delta since the last review (`d27a1654..4d8fb902`) is three commits;
  - the published author evidence at milan-fpga `004088f6` `review-evidence/gptp90-r1/author-r2`.
- **Process inputs:** this repository has no AGENTS.md or CONTRIBUTING.md. I used README.md, docs/README.md (truth order: RTL and generated microcode, then executable tests, then guides) and docs/TEST_DEVELOPER.md.
- **Authorities:**
  - IEEE 802.1AS-2011 with Cor1 and Cor2: 10.3.11 and Figure 10-13; Figure 10-4; gmPresent (10.2.3.13, 10.3.12); 10.6.3.1; 11.2.13; 11.2.15.3 and Figure 11-8.
  - Milan v1.2 Table 4.2.
  - This repository's #84 rule for the synchronization verdict (`docs/INTEGRATION.md:540-563`).

## Verdict

NEGATIVE, on one open MINOR (F1).

The round-2 delta fixes all three round-1 protocol findings at their cause:

- an expiry found in the master role now marks the port;
- mastership keeps both Sync watches;
- Sync ageing honours gmPresent, through one priority-threshold compare.

Each fix has named checks and a planted control. I re-executed all seven new controls, and each was caught on every check it names. At head, the engine suite gives 1,805 checks per shipping pass and 57 in the priority1 255 pass, matching the author's receipts. The parent companion patch now carries the corrected parent docs and figure.

The gmPresent fix leaves one path where the timeout has no effect at all (F1). A slave of a priority1 255 grandmaster whose Sync stops is now neither aged nor stripped of sync-ok. It therefore publishes "synchronized" (flags bit 3, from which the parent derives tu) indefinitely, with no Sync.

- At base, that expiry cleared sync-ok within one second.
- At round 1, it aged the grandmaster.

The probe was executed and its receipts are attached. The delta also adds two review-round labels in source comments (R1, RESIDUE).

## Findings

### F1 - MINOR - A slave of a priority1 255 grandmaster keeps sync-ok after its Sync stops

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Location:**
  - `hdl/ucode/gen_gptp_ucode.py:2157-2168` (`prog_leg_srto`). The expiry writes the aged mark, then branches to BECGATE only for an elected peer whose grandmaster has priority1 below 255. Every other case reaches `END` and leaves the flags untouched.
  - Base's leg cleared `FL_SYNCOK_C` on every expiry outside mastership (the "v4 rule", retired at `:18-19`). Round 1 always aged an elected peer. At this head, neither happens for a priority1 255 grandmaster.
  - `FL_SYNCOK_C` is set on each consumed pair (`:1029`). It is cleared only by:
    - BTCA's grandmaster change (`:1792`);
    - the Pdelay loss and bad-verdict paths (`:1618`, `:1670`, `:2119`);
    - BECGATE's drop (`:1854`).
  - None of those runs while a parent refresh keeps the same grandmaster.
- **Authority:**
  - `docs/INTEGRATION.md:431`: "`pub_flags_o` bit 3 publishes the synchronization verdict". `:551`: "The parent derives tu from bit 3".
  - `docs/INTEGRATION.md:301-303`, `:398` and `:583` all state that a 375 ms Sync receipt timeout ends synchronization to the grandmaster:
    - "A 375 ms Sync receipt timeout ages the grandmaster instead";
    - "Missing Sync; 375 ms receipt timeout | Ages the grandmaster";
    - "So do 375 ms without a usable Sync pair", under "Departure of the elected peer".
  - syncReceiptTimeout is 375 ms (Milan v1.2 Table 4.2). Under 802.1AS-2011 10.3.11, ageing on that timeout needs gmPresent, which is why no ageing applies here. Nothing in the clause, however, makes the port's Sync count as still received.
  - Round-2 assignment item 3 requires "no ageing on sync receipt timeout" under a priority1 255 grandmaster. It does not ask for the synchronization verdict to stay set.
- **Evidence (executed):**
  - Reviewer probe `scripts/probe_p255_syncok.py`, with receipts `receipts/probe-p255-syncok/{base,r1,head}.log`. In disposable copies, it appends one phase to the end of the priority1 255 pass:
    1. From mastership, elect a better priority1 255 peer.
    2. Feed that peer's usable Sync/Follow_Up pairs every 125 ms for 2 s, with one Announce each second.
    3. Stop Sync while the Announces continue.
  - At base `55680bff`: `flags=d` (sync-ok set) while Sync runs. At 1, 2, 3 and 4 s after Sync stops, `flags=5` (sync-ok clear).
  - At round 1 `d27a1654`: the plane ages the peer and is master (`flags=e`). This is the case R720-1 F1 raised.
  - At head: `flags=d`, `syncok=1` at 1, 2, 3 and 4 s after Sync stops. The peer stays elected, which is correct per gmPresent. The published verdict, however, claims synchronization with no Sync for the whole window.
  - Each pass's own checks were unaffected: 53/53, 53/53 and 57/57, all rc 0.
  - No check covers this case. Phase 41 (`tb/verilator/engine/sim_main.cpp:5718-5751`) elects a priority1 255 grandmaster that never sends Sync, so sync-ok never rises there.
- **Impact:**
  - **Wrong verdict.** In the supported `--p1 255` (not grandmaster-capable) build, a slave keeps sync-ok set after its priority1 255 grandmaster stops sending Sync. It holds until that grandmaster's Announces stop (the 3 s announce receipt timeout), and indefinitely while they continue. The parent's tu stays clear, and the qualification hook stays satisfied, with no time transfer.
  - **Regression.** Base did not do this. The round-2 gmPresent fix introduced it.
  - **Docs.** The documented Sync receipt timeout behaviour (`INTEGRATION.md:301-303`, `:398`, `:583`) is false for this input. The new paragraph at `:629-637` describes ageing but says nothing about the verdict.
  - **Default build unaffected.** The shipping priority1 248 image cannot elect such a peer.
- **Required outcome:** either (a) or (b).
  - (a) A sync receipt timeout that does not age, on a slave of an elected peer, clears sync-ok. This is the base rule, kept for gmPresent FALSE. A master still keeps sync-ok (#84).
    - Add a named check in the priority1 255 pass. A priority1 255 grandmaster's usable Sync raises sync-ok, and when its Sync stops, sync-ok clears within syncReceiptTimeout while the peer stays elected.
    - Add a planted control that fails that check.
    - Regenerate the four images through the generator and keep the ROM inside budget.
  - (b) Record an owner or manager decision that the verdict may stand without Sync under a priority1 255 grandmaster. Then correct `INTEGRATION.md:301-303`, `:398` and `:583`, and the PR body's gmPresent bullet, to say so.
- **Verification:**
  - Rerun `python3 -I scripts/probe_p255_syncok.py <disposable-tree> <pinned-verilator>`. By 1 s after Sync stops, expect `syncok=0` with `gm=0000000000000105`, which means the peer is still elected.
  - The engine suite and the mutation arm pass, with the new control caught on its named check.

### R1 - RESIDUE - Two new source comments name review rounds

- **Lens:** Docs (comment wording only, under the owner comment rule).
- **Location:** `tb/verilator/engine/receipt_mutants.py`. Both lines are new in this delta, in a new file.
  - `:66`: "# the round-1 rule, one word longer: ..."
  - `:144`: "# BECOME as round 1 shipped it: one word longer each, ..."
- **Exact fix:** this matches the file's existing idiom at `:40`, "the leg as main 55680bff shipped it".
  - `:66` becomes "# the rule at d27a1654, one word longer: only an expiry that ages an elected".
  - `:144` becomes "# BECOME as d27a1654 had it: one word longer each, which the ROM holds".
- **Verification:** a search of the added source lines for `round` finds no match. Both lines are comments, so `make -C tb/verilator/engine mutants` behaves the same.

### Suggestions (no effect on the verdict)

- **S1 (Docs):** `docs/INTEGRATION.md:607` reads "So an expiry found in the master role ages too." A master is only marked: it keeps sync-ok and its own information, and only later Announces are aged. Consider "So an expiry found in the master role marks the port aged too."
- **S2 (Conformance, Docs):** the watch combines two editions of the standard.
  - Adoption starts it (`gen:1804-1810`), as 802.1AS-2020 Figure 10-14 SUPERIOR_MASTER_PORT does.
  - On a marked port, though, a new superior grandmaster's Announce is aged until a usable pair is heard. That is the 802.1AS-2011 reading.
  - Recovery stays automatic, one Announce interval after the first pair. Consider one sentence near `INTEGRATION.md:609` saying that a new grandmaster on a marked port also waits for its first usable pair.
- **S3 (Robustness; carried from R719-1 S3):** the master role now pairs every Sync on an asCapable port. An own-port filter on Sync receipt (IEEE 1588-2008 9.5.2.2) would keep a reflected own Sync/Follow_Up from counting as usable Sync.
- **S4 (Conformance; carried from R719-1 S2):** Figure 11-8 WAITING_FOR_PDELAY_RESP also resets on a Pdelay_Resp with the wrong sequenceId or the wrong requester. This is outside #91; file an issue.
- **S5 (Tests; carried from R720-1 F3):** add a two-responder shape in which the second responder also sends its own Follow_Up, and check that no exchange completes.
- **S6 (Docs):** the round-2 edit at `tb/verilator/engine/sim_main.cpp:5525` left one comment line far longer than its neighbours. Reflow it.

## Prior public findings at this head

I resolved each item below after finishing my own independent pass over the delta.

| Prior item | State at 4d8fb902 | Evidence |
|---|---|---|
| R719-1 F1 (master-role expiry forgotten) | RESOLVED | `gen:2158-2159` writes `SRTO_PASSED_C` on every expiry. Phase 40 adds "#89 a lone pair heard as master: a later Announce elects nothing" and two more named checks. The control "only an expiry that ages a slave marks the port" was caught in my rerun (`receipts/spot-mutants/m1.log`) and in the author log. The author's unchanged rerun of the R719-1 probe (hash-verified) re-elected on 0 of 3 late Announces; the control round still re-elects. |
| R719-1 F2 (BECOME drops the parked Sync's FU watch) | RESOLVED | `gen:1885-1889`: BECOME no longer writes timer slots 4 and 5. Phase 40 adds "#89 parked Sync: a Follow_Up 200 ms after it pairs with nothing" and "... 60 ms after it, after the takeover, is heard". Controls "mastership stops the Sync receipt watch", "mastership stops the Follow_Up watch" and "mastership voids the parked Sync" were all caught (`m5`-`m7`). The author's probe rerun gives `PROBE parked ... elected_by_next_announce=0`. |
| R719-1 F3 (parent companion docs) | RESOLVED (pending landing) | Patch `b53944d52a51323b267b0a91dbfd6bd1aeaabcacf26d31b246b19318d56a1b7a` matches its recorded sha256. It changes `docs/design/GPTP_PLANE.md:130` to "fifth" and `:134` to "fourth". It changes `docs/testing/TESTING.md:187` to "17.992742740 simulated seconds over 899637137 cycles", the figure of the patched head run (`consumer-head/final-b/01.log`). Parent `docs_check.py` rc 0 (`final-a`). |
| R719-1 R1 / R720-1 F2 (dangling pronoun) | RESOLVED | `docs/TEST_DEVELOPER.md:132` reads "Clears sync-ok on every handover to a peer." |
| R719-1 S1 (gmPresent approximation) | SUPERSEDED | Superseded by the R720-1 F1 fix. |
| R719-1 S2, S3 | Carried as S4, S3 | Suggestions only. |
| R720-1 F1 (Sync ageing ignores gmPresent) | RESOLVED as specified (option a) | `gen:1098-1101` and `:2160-2167`. Phase 41 adds four named checks. Controls "sync receipt ageing ignores gmPresent", "an aged port refuses a priority1 255 grandmaster" and "an aged Announce is dropped rather than aged" were caught (`m2`-`m4`). The author's unchanged rerun of the R720-1 probe shows the plane staying slave of the priority1 255 peer for all 6 s. The fix opens F1 above. |
| R720-1 F3 (two-responder FU shape) | Carried as S5 | Suggestion only; the delta does not address it. |

## Lens evidence

### Conformance

- **Ageing on Announce receipt** (`prog_rx_announce`, `gen:1091-1101`, after qualifyAnnounce):
  - The compared value is `{p1, clockClass, clockAccuracy}`: bank word 8, shifted left 16 and then right 40. It is compared unsigned against `S_SRTO`.
  - With `S_SRTO = 0xFF0000`, the value is below exactly when priority1 < 255, which is gmPresent for the received grandmaster (10.2.3.13). With `S_SRTO = 0`, nothing compares below.
  - Every priority1 < 255 vector beats every priority1 255 vector. On this single port, "selected, then aged at once" is therefore the same as "aged at once".
  - BECGATE then keeps or makes the plane master, which matches Figure 10-13 (Cor1) as the PR reads it.
- **Ageing on expiry** (`prog_leg_srto`): `(flags & 1) - 1` is 0 for an elected peer and all ones otherwise. OR-ed into `S_BESTPV >> 40`, the result compares below the mark exactly for an elected peer whose grandmaster has priority1 < 255. The rest of the leg is F1.
- **The Sync watch:** `prog_leg_srwatch` restarts slot 4 on every usable pair in either role, and clears the mark. Phase 40 checks the 10.3.11 timing: an Announce 624 ms after a pair is aged, and one 124 ms after a pair is elected.
- **The Follow_Up watch:** the 11.2.13 watch is now kept across mastership. `prog_leg_futo` only voids the pending Sync, so a master's sync-ok is untouched (#84).
- **#90/#91:** the delta does not change `_tmr_pdelay_request`, `_pdresp_arm_the_pairing` or the PDPOST verdict. Their round-1 verdict stands (both R719-1 and R720-1 found them met), and their controls are still caught in the head mutation log.

### RTL

- No `.sv` file changed. There is no top-level port, parameter or register-map change. The only new scratch use is the existing cell 46.
- `KL_gptp_ucpu.sv:197-205`: CMP is an unsigned 32-bit compare on the formatted operands, so both new branch-free compares are exact.
- The rewritten asCapable gate in `prog_rx_sync` (`gen:868-873`) is equivalent to the `e_flag_gate` it replaces.
- ROM: the shipping image uses 1,021 of 1,024 words (base 1,015). The seeded images use 1,022 and the priority1 255 image 1,021. `FUTO@254`. All match `docs/MANAGER.md:103-117`.
- All four tracked images regenerate byte-identically with each consumer's own arguments: engine `49def116…`, microCPU and OOC `739fc585…`, tsngen `b589f065…`.
- The F1 path is microcode behaviour.

### Robustness

- **Warm reset:** `S_SRTO` is read only behind the asCapable gate, and the only asCapable rise clears it (`gen:2115`). A retained mark cannot reach a live port.
- **Incapable port:** an incapable port with an elected peer reaches BECGATE's drop path, the same as through the asCapable-fall hook.
- **Relapse:** a lone pair followed by another lapse re-marks the port, so there is no re-election storm.
- **Worse peer as master:** a master that hears a worse peer's transient Sync is marked 375 ms later. That mark affects only Announces with priority1 < 255, which a master keeps or rejects identically either way.
- **Open:** F1.

### Tests

- **Re-executed by me**, with pinned Verilator 5.050 (`receipts/tool_identity.txt`):
  - Unmutated shipping and priority1 255 passes: 1,862 = 1,805 + 57, all PASS (`receipts/spot-mutants/clean.log`).
  - All seven round-2 controls, through the arm's own `run_mutant`, which requires every named check to fail: each one caught (`m1`-`m7`).
  - microCPU suite 768/768, plus `make contract`, `make docs` and `make lint`: all rc 0 (`receipts/quick-gates/`).
- **Author receipts, hash-verified** (`receipts/evidence_verify.txt`): all 142 author-r2 files match their `published_sha256`, none redacted and none unlisted. Every head gate is rc 0 with `head_unchanged: true`:
  - engine: 1,805 in each of the three shipping-image passes, plus 57 in the priority1 255 pass;
  - mutation arm: the clean control plus 98 of 98 controls caught (I counted 98 `[PASS]` lines; base has 72);
  - parser, gaskets, tsngen, bench, lint, docs, diagrams, the OOC self-test and the full `make`.
- **New phases read against their helpers:**
  - I read the phase 40 and phase 41 assertions (`sim_main.cpp:5612-5751`), the queued-expiry check at `:4008` and the asCapable-gate Announce at `:5355` against the timing helpers. The harness runs at 2 MHz, and `s39_interval` sends its pair at the start of each 125 ms interval.
  - The figures in the comments (125 ms, 339 ms, 36 ms, 200 ms, 60 ms, 4 s) match the stimulus.
- **Gap:** F1. No check covers sync-ok when a priority1 255 grandmaster's Sync stops.

### Docs

- **Read:** the delta to these guides:
  - HDL_DEVELOPER (`:188-230`);
  - INTEGRATION (`:599-637`);
  - MANAGER (ROM figures verified);
  - SOURCE_EVIDENCE (`#L984` resolves to `prog_leg_slew`; two new rows);
  - TEST_DEVELOPER (`:122-132`).
  
  I also read the generator header and the leg docstrings.
- **Unclean through F1:** `INTEGRATION.md:301-303`, `:398` and `:583` misdescribe the priority1 255 case.
- **Comment rule:** the only new instances are R1. The "manager's ruling" phrases predate the delta and are tracked by #746.
- **PR body figures**, all verified: checks 1,703 → 1,805; priority1 255 pass 53 → 57; controls 72 → 98; ROM 1,015 / 1,018 / 1,021 words; seeded images 1,022.

## Hosted evidence

The head has 0 check runs, and its combined status is `pending` with 0 contexts. No hosted job ran at this head, so this review relies on none. The manager owns hosted and act acceptance.

## Ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `gen_gptp_ucode.py` SRTO, RX Announce/Sync/Follow_Up, SRWATCH, BECOME, BECGATE, BTCA adoption, FUTO; 802.1AS-2011+Cor1/Cor2 10.3.11, Fig 10-4, Fig 10-13, 10.2.3.13, 11.2.13; Milan v1.2 Table 4.2; #90/#91 legs unchanged (round-1 verdict kept) | R719-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| RTL | UNCLEAN (F1) | microcode delta, `KL_gptp_ucpu.sv` compare path, four images regenerated byte-identical, ROM packing (1,021/1,022), no `.sv` delta | R719-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| Robustness | UNCLEAN (F1) | aged-mark lifecycle (warm reset, asCapable rise and fall, master-role expiry, lone-pair relapse), parked-Sync FU watch, priority1 255 probe at base, round 1 and head | R719-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| Tests | UNCLEAN (F1 uncovered) | `sim_main.cpp` phases 40/41 and the `:4008`/`:5355` edits, `receipt_mutants.py`, `mutants.py` grading; reran the clean harness (1,862/1,862) and the seven round-2 controls; author gate receipts hash-verified | R719-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |
| Docs | UNCLEAN (F1; R1 is residue) | HDL_DEVELOPER, INTEGRATION, MANAGER, SOURCE_EVIDENCE, TEST_DEVELOPER, generator comments, PR body, parent companion patch doc hunks | R719-2 | 4d8fb9024c7ed4ce4b6e70912721c3cfb03e729e |

## Real limits

- **Standards texts:** 802.1AS-2011, Cor1, Cor2 and Milan v1.2 were not available locally. Clause readings follow the issues, the assignments and the reviewer's reading of the figures.
- **Evidence signature:** the hosting API reports the evidence commit `004088f6` as unsigned (`verified=false`, reason `unsigned`). I verified integrity file by file against its `MANIFEST.json`, not by signature.
- **Mutation arm:** I did not rerun the full arm. I spot-checked 7 of the 98 controls; the other 91 rest on the hash-verified author log.
- **Gates not rerun:** the seeded engine passes, parser, gaskets, tsngen, bench, diagrams and the full `make` rest on author receipts. I ran the shipping and priority1 255 passes, the microCPU suite, contract, docs and lint.
- **Parent:** I re-executed no parent gate, and I inspected the companion patch without applying it. `gptp_plane` at this gitlink rests on the author's exploration log, which used the round-1 test hunks; the round-2 patch changed only doc hunks.
- **No synthesis, OOC run or hardware.** Physical calibration NOT RUN, and field skips are not hardware proof.
- **No manager source bank** ran at this head; none is claimed or inferred.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn against live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`, and link the receipts on the PR.
- Hosted and act acceptance.
- Land the parent companion change (sha256 `b53944d5…`) with the gitlink bump, together with the donor deep-link pins for `check_gptp_docs.py --with-submodule`.
- Carry R1 to the residue checklist.
- Decide between F1's routes (a) and (b), and whether to file issues for S3-S5.

## Workspace restore

I never modified the review clone. All builds and probes ran on `git archive` extractions under the packet's `scratch/`. At the end of the review:

- HEAD is `4d8fb902…` and the tree is `f7731898…`.
- `git status --porcelain --ignored` is empty, and so is `diff-index`.
- All 108 tracked blobs and their modes match `git ls-tree -r HEAD`.
- There are 0 submodule gitlinks; the repository has none.

The receipt is `receipts/restore_check.txt`.

## Receipts

`MANIFEST.sha256` lists every published file:

- `receipts/probe-p255-syncok/`: the F1 probe at base, round 1 and head, with rc files.
- `receipts/spot-mutants/`: the clean harness run and the seven round-2 controls.
- `receipts/quick-gates/`: the contract, docs, lint and microCPU logs.
- `receipts/evidence_verify.txt`, `receipts/restore_check.txt` and `receipts/tool_identity.txt`.
- `scripts/probe_p255_syncok.py`, `scripts/spot_mutants.py` and `scripts/verify_evidence.py`. Each takes tree and work paths as arguments.

Host paths in the logs are replaced by placeholders.

R719-2 FINISHED
