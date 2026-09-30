[R413] POSITIVE - exact head 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4

Round R413-3, external independent review of PR #623 (issue #70, lane 2).
Exact published head 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4, tree
47a0b44682dee2817b131da935a9e2dffd42bd53. Two commits on the round-2 head
943a3dac: a033bfd8 (item 2, service grader) and 0a80abcb (item 1, the
address-decided census). Reconstructed from AGENTS.md/CONTRIBUTING.md,
docs/README, the frozen #70 acceptance and public scope, the round-3
assignment (#70 comment 5905511808), the executor STOP (5906387036) and the
manager ruling (5906400668, option 1), then the diff
79c36963..0a80abcb and the two round-3 commits, then the public evidence.

All five lenses were applied independently against artifact-specific evidence
at this exact head, with disposable fault/mutation probes. My two standing
round-2 findings (F1 MAJOR, F2 MINOR) are both resolved at this head, verified
independently. No open BLOCKER, MAJOR or MINOR remains. Verdict: POSITIVE.

The scope excludes any firmware, RTL or bitstream change; the round-3 commits
touch only docs, the builder gate and the service-budget bench. The final
current-dev candidate, the full source bank's acceptance, the exact-head hosted
Verilator/Yosys contexts, and the physical calibration remain the manager's to
own; they are recorded under "real limits and pending manager duties" and do
not fall to this reviewer.

================================================================================
1. What was verified this round
================================================================================

1.1 Round-3 scope (Conformance/RTL/Docs; receipts/round3_scope.txt,
    receipts/clone_integrity.log)
- git diff --name-only 943a3dac..0a80abcb is exactly six files: CHANGELOG.md,
  docs/findings/397_SERVICE_BUDGET.md, docs/integration/BAREMETAL_FIRMWARE.md,
  sw/builder/test_builder.py, tb/verilator/fw_service_budget/README.md,
  tb/verilator/fw_service_budget/run.py. No hdl/*.sv, no sw/firmware, no
  syn/, no submodule gitlink among the round-3 commits.
- The review clone is pristine at the published head: working tree clean,
  tree 47a0b446..., protocol-processor gitlink b2db3a97 (the pinned
  processor), gptp/verilog-axis gitlinks unchanged. milan_baremetal.c sha256
  a73ecc25...0eb3 equals the capture receipt's and is byte-identical at
  597dba85, 943a3dac and 0a80abcb. So this round makes NO firmware change,
  matching the ruling's constraint.
- check_nvm_capture and the capture receipt are unchanged 943a3dac..0a80abcb.

1.2 F1 (MAJOR, standing from R413-2 / R412-2) — the address-decided census
    RESOLVED at 0a80abcb.
The ruling (option 1) moved the verdict pins off names and spellings onto the
linked image of a second `-no-pie` compile of the same source (the product's
code model), read by address. I re-ran every probe I hold plus a new one, on a
disposable copy of the head tree, with the RV32 compiler present
(riscv32-linux-gcc.br_real 14.3.0, Buildroot 2026.05):

- Baseline (receipts/gate1b_head_none.log, ...none_forget.log): the shipping
  firmware is ACCEPTED with kept=['aem_loaded']; force-forgetting the slot
  REFUSES the same base. Acceptance depends on the kept slot, not a naive
  read-back — the vacuity trap is closed.
- The two spellings that defeated the 943a3dac gate are now refused, each
  naming the pin: alias_sscanf and weakref_sscanf both hit the escape pin
  ("the full address formed in a register (%lo on an addi) ... in nvm_boot()
  (R_RISCV_LO12_I)") AND the name pin ("another symbol of the linked image is
  on aem_loaded's storage (milan_r413_alias / milan_r413_ref)")
  (receipts/gate1b_head_alias_sscanf.log, ...weakref_sscanf.log).
- Every earlier plant stays refused, each on its class: plain/splice/paste/
  macro writes and alias_write on the store pin; asm_label_sscanf,
  inline_asm_la, block_extern_sscanf, m_macro_addr, m_macro_addr_sscanf on the
  escape/address pins (receipts/gate1b_head_*.log, twelve logs).
- A NEW adversarial probe the gate's own controls do not spell —
  `lui %hi; addi %lo(aem_loaded)` formed in inline asm and handed to sscanf(),
  a real R_RISCV_LO12_I on an addi with no C `&` — is refused on the escape pin
  (receipts/gate1b_head_asm_hilo_sscanf.log, probes/plants2.py). The premise
  holds against address formation the C-level plants do not reach.
- The full gate (receipts/gate1b_head_full.log, elapsed 871 s) ACCEPTS the
  shipping firmware, reports the six references to aem_loaded's storage as each
  the upper part or a load/store in place (milan_init() upper/store/upper/load,
  milan_status_handler() upper/load), refuses 14/14 in-gate planted pin breaks
  each naming its pins, and states the literal-address limit.

Independent confirmation of the ruling's premise, not through the gate's own
reader (receipts/nopie_image_readelf.log; SDK binutils readelf/objdump 2.45.1
over the `-no-pie` ELF the gate reads, dumped by wrapping rv32_image() in
probes/dump_nopie_elf.py): each of the two product arms shows aem_loaded as a
LOCAL OBJECT of size 4, ELF flags 0x0 (no compressed extension), and exactly
six relocations on its bytes — 3x R_RISCV_HI20 (the upper part on `lui`),
1x R_RISCV_LO12_S on a `sw` (milan_init()'s store), 2x R_RISCV_LO12_I on `lw`
(milan_init()'s read-back and milan_status_handler()'s read). No `%lo` on an
`addi`, no GOT_HI20, no R_RISCV_32 data word, no bare AUIPC. This matches the
gate exactly and shows, by address, that for the firmware translation unit's
own compiled references nothing forms the verdict's full address to carry it
into a call, a surviving register or a store.

Judging the ruling's premise ("nothing else can write it") on my own: the
`-no-pie` census establishes it for every RELOCATED reference the one linked
image shows, to the accepted literal-address limit. The reference detector is
fail-closed and keyed on the target address, not on recognising a relocation
kind: any relocation whose symbol+addend lands on the four bytes is reported,
and any role other than upper/load-in-place/store-in-place (an addi %lo, a GOT
entry, a data word, an unpaired %pcrel_lo, or any unknown kind/opcode) is an
escape. A bare AUIPC anywhere refuses conservatively; a compressed image
refuses. Cross-unit naming is blocked by the retained source pins (aem_loaded
is a file-scope static with internal linkage; no other Makefile-linked unit's
source names it) reinforced by the image locality pin. The only residue is a
store through a hard-coded numeric address, which carries no relocation — this
is the manager-accepted #495 limit, documented in the rule comment,
BAREMETAL_FIRMWARE.md and the CHANGELOG. The premise is sound within that
stated limit; no finding.

1.3 F2 / S1 (MINOR, standing from R413-2) — the W6 sentence and its control
    RESOLVED at a033bfd8.
- The fw_service_budget self-test passes with 52 grading checks and 14 flash
  checks, 0 failures (receipts/service_selftest_head.log), matching
  397_SERVICE_BUDGET.md:318 and the bench README's "Five self-test controls".
- Grader W-mutants (receipts/grader_mutants_w0_w6.log): W0 (identity) survives;
  W1-W6 are all killed; W6 is killed BY NAME with the message "an
  unarmed-start command's UART allowance left its armed bound" — the fifth
  armed control a033bfd8 added (S1).
- W6 direction (receipts/w6_direction.log): the head rule gives
  armed_period_bound_ms=505 and reports the over-budget tick stretch; the W6
  rule gives 495 and drops that finding. W6 is the MORE LENIENT rule, not
  stricter — the substance of R413-2 F2.
- The live PR #623 body now states this correctly ("W6, the armed bound
  without the UART allowance ... is more lenient than the rule, not stricter",
  and documents the a033bfd8 control under item 2); the earlier "stricter"
  wording is gone.

1.4 Docs (BAREMETAL_FIRMWARE.md, CHANGELOG.md)
The rule comment (test_builder.py:1631f), BAREMETAL_FIRMWARE.md:919f and
:1602, and the CHANGELOG state only what the census proves: the pins decided
by address on the `-no-pie` image; the four image pins enumerated as
implemented; a 14-row planted-break table whose pins match the code and the
gate's "14/14"; and the literal-address limit stated plainly and tied to #495.
No claim exceeds the evidence.

================================================================================
2. Findings
================================================================================

No open findings. For the record, the standing findings and their resolution:

F1 (was MAJOR; Conformance, RTL, Robustness, Tests, Docs) — RESOLVED at
0a80abcb. A GNU alias or weakref of aem_loaded handed to sscanf() defeated the
943a3dac name/spelling pins. Fixed by deciding the pins by address on the
`-no-pie` linked image (ruling option 1). Evidence: receipts/gate1b_head_*.log
(alias/weakref/12 earlier/asm_hilo all refused naming the pin; base accepted,
force-forget refused), gate1b_head_full.log (14/14, six in-place refs),
nopie_image_readelf.log (independent readelf: six in-place relocations, local
object, no escape). Verification: the two named controls are refused with the
escape and name pins; the shipping firmware passes with the slot kept.

F2 (was MINOR; Tests, Docs) — RESOLVED at a033bfd8. PR body called the W6
grader mutant stricter; it is more lenient. Fixed: PR body corrected and a
fifth armed control (S1) kills W6 by name. Evidence:
receipts/grader_mutants_w0_w6.log, w6_direction.log, service_selftest_head.log,
and the live PR body. Verification: W6 killed by name; self-test 52 checks;
PR body reads "more lenient ... not stricter".

================================================================================
3. Reviewer-owned lens coverage ledger
================================================================================

| lens | verdict | examined artifacts (at this head) | covering round | head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling option 1 vs test_builder.py rv32_image()/rv32_image_references()/verdict_image_pins()/aem_verdict_pins(); alias_sscanf+weakref_sscanf+12 earlier+asm_hilo plants refused each naming its pin; 14/14 in-gate breaks; shipping firmware accepted, slot kept; base refused with no pin read; service self-test 52 checks; W6 killed by name; #70 acceptance | R413-3 | 0a80abcb |
| RTL | CLEAN | round-3 commits touch no hdl/*.sv, no sw/firmware, no syn/, no gitlink (round3_scope.txt); processor pin b2db3a97 and milan_baremetal.c sha256 a73ecc25 unchanged; the `-no-pie` image census reads the psABI relocation/opcode encodings correctly (independent readelf: HI20 on lui, LO12_I on lw, LO12_S on sw), fail-closed on addi/GOT/data-word/bare-AUIPC/RVC | R413-3 | 0a80abcb |
| Robustness | CLEAN | rv32_image() asserts ELF32-LE, refuses SHT_REL; references keyed on target address so unknown reloc kinds and unpaired %pcrel_lo report as escape/reference; bare AUIPC and compressed image refuse; verdict_image_take() fail-closed on a failed build; 12 external + 1 novel asm escape plants all refused; force-forget vacuity guard refuses the base | R413-3 | 0a80abcb |
| Tests | CLEAN | fw_service_budget self-test 52/14, 0 fail; W0 survives, W1-W6 killed (W6 by name); w6_direction shows the lenient direction; 14 in-gate verdict controls each fail for their class; base accept-only-with-slot and refuse-with-no-pin non-vacuity; my mutation probes confirm each control can fail | R413-3 | 0a80abcb |
| Docs | CLEAN | BAREMETAL_FIRMWARE.md:919-1002 and :1602, CHANGELOG.md, 397_SERVICE_BUDGET.md:318, bench README; claims match code and gate output; 14-row break table matches verdict_pin_breaks; literal-address limit stated and tied to #495; PR body W6 sentence corrected | R413-3 | 0a80abcb |

All five lenses CLEAN at exact head 0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4.

================================================================================
4. Real limits of this review, and pending manager duties
================================================================================

- Firmware digest / scope: this round changes no firmware, RTL or bitstream;
  the substantive #70 implementation (real NVM backend, restore walk, RTL) is
  in earlier lane commits reviewed in prior rounds and is unchanged here
  (gitlink b2db3a97, milan_baremetal.c a73ecc25 identical). This report does
  not re-open that earlier work; it confirms it is untouched.
- The census reads ONE translation unit compiled and linked ALONE at the
  product's code model, not the product image (the SDK cannot link LiteX's BIOS
  libraries). It proves the pins for that unit's own relocated references;
  cross-unit naming is blocked by internal linkage. A store through a hard-coded
  numeric product address of aem_loaded carries no relocation and is outside the
  pins — the manager-accepted stated limit on the #495 residue checklist,
  documented. Not a blocker for this lane.
- The gate-1b compiled census needs the RV32 compiler; I ran the
  compiler-present arm (--require-rv32). The compiler-hidden arm marks that
  census NOT RUN by design. The manager's full source static/builder bank (with
  the compiler present and hidden) is the public covering run and is reported
  passed at this head.
- Physical calibration was NOT RUN; hardware/field contexts are skipped and are
  not hardware proof. The physical power-cycle soak of the eight saved items is
  acceptance evidence the manager owns, on silicon.
- The final current-dev candidate (source base 79c36963, live dev tip
  ccdd07b5) is built by the manager at the merge turn; source validation here is
  distinct from that candidate. Exact-head hosted Verilator/Yosys acceptance and
  hosted/act orchestration remain the manager's.
- Per section 7, coverage is banked against this exact head; any later commit to
  an artifact in a lens's scope un-covers that lens and needs re-coverage.

Probe environment: disposable copies under
$REVIEWS/70L2-r413-3-packet/scratch (never published); the review
clone was never edited and is verified pristine at the exact head
(receipts/clone_integrity.log). All commands ran in the foreground.

R413-3 FINISHED
