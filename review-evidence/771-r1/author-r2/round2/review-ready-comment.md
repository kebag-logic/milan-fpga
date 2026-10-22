[A662] REVIEW READY
Commit: 1098978f4a931a667e147b68a791520eb141c917 (PR #772, round 2; three new commits on a97aea01, no rebase, no amend)

Round 2 answers [A10]'s assignment (PR #772 issuecomment-6342664760), R683-1 (issuecomment-6342652024) and R684-1 (issuecomment-6341299778).

**Item 1: case (a). The production firmware follows processor #189; only the walk's test adapter was stale.** tsn-c-stack is unchanged.
- The production path:
  - The SRP delivery (`sw/firmware/ctrl/app/ctrl_app_srp.c:90-100`) hands a SETTLED_RSV_OK Advertise/Failed swap to `acmp_tk_kind_changed`.
  - That entry (`third_party/tsn-c-stack/src/acmp.c:1176-1187`) sets the kind with no arc. Then `finish()` notifies once (`:495-515`, with REGISTERING_FAILED in the compared view at `:441-448`).
  - GET_RX_STATE carries the new kind (`:891-892`).
- The walk sent the event to `acmp_tk_registered` instead, which refuses outside SETTLED_NO_RSV.
- `b6fc1590` makes the walk deliver the event as the firmware does. The adopted oracle is untouched.
- Results:
  - `acmpwalk` goes from 127 / 1 at `a97aea01` to 127 / 0 at the head.
  - Control `acmp-kind-lost` (the swap drops the kind) is KILLED by `AcmpCore.KindChangesOnlyTheSettledView` and walk `TK_REG_SOK` "registered state".
  - Control `acmp-kind-not-notified` (new; only the notification is lost) is KILLED by "kind change notifies once" and walk `TK_REG_SOK` "notified exactly when a Table 5.22 item moved". That is the walk's only failing check under this control.
  - Both controls are in the control campaign's table, which reports `521 of 521 caught`.
- A probe on the composed production firmware (`ctrl_app` with SRP, real mailbox MSRP vectors, real ACMP wire; `SrpFeedback.*` at 1 and 2 interfaces) adds a check that each swap notified:
  - unchanged firmware: 19 / 0;
  - with the glue call dropped: state, wire and notification fail;
  - with the stack's swap muted: only the notification checks fail.
- The firmware digest the capture pins (`milan_baremetal.c`, `497845e6...`) is unchanged, so the capture is not re-measured.

**Item 2** (`bbdd24d0`): `REGISTER_MAP.md`, `SUBMODULES.md` and `CHANGELOG.md` name the bound. At 8 or more received entries, the served path is the first eight received entries, the count stays 8, and thisClock is not appended (donor #86).

**Item 3** (`1098978f`): `KL_gptp_shadow.sv`, `milan_datapath.sv`, `KL_pp_shadow.sv` (`gsi_asp_chg_i`), `README.md` and `REGISTER_MAP.md` give the #85 meaning:
- 0 is an absent PathTrace;
- count one is `{thisClock}` before a peer (#82);
- an explicit one-entry `[GM]` PathTrace is count two (#85).

The three `.sv` hunks are `//!` comment lines only.

**Item 4:** round 1b's "every local gate green" was wrong. The firmware gate set had not run, and it failed at `a97aea01`. PR-BODY now lists what ran.

Validation at 1098978f, all rc 0 unless stated:
- **RV32 toolchain:** the pinned SDK, installed from its digest-checked archive with `scripts/ci_rv32_sdk.py` and passing `--verify-only`. The binary that ran: `MILAN_RV32_CC=<lane scratch>/rv32-sdk/host/bin/riscv32-linux-gcc` (Bootlin `riscv32-ilp32d--glibc--stable-2025.08-1`, gcc 14.3.0; `.br_real` SHA-256 `f2f6ec09...`). The host's default SDK location holds an unreceipted Buildroot tree, refused by `--verify-only`, and was not used. GoogleTest 1.14.0; Clang 18.1.3.
- `fw_rv32_selftest.py --require-rv32`: passes.
- `tally_selftest.py --mutants`: passes.
- `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4`: PASS.
  - 1,593 checks over 66 arm tallies, 0 failures.
  - Control mutants: 521 of 521 caught.
  - AECP and SRP campaigns: 358 caught, 0 escaped.
- `test_ctrl_firmware_shards.py`: 941 invocations, each in exactly one shard.
- `test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`: 435 tests; 109 of 109 planted defects caught.
- `fw_coverage.py --selftest`: 29 / 29. `fw_coverage.py --check`: PASS, 30 files.
- `ctrl_boundary.py --require-rv32 --selftest`: PASS. It ran under a LiteX interpreter at `litex_pins.txt`'s seven revisions. Under the host python3 it is refused (rc 2): `test_ctrl_memory.py` needs migen, which the hosted job installs first.
- Sweep: 63 / 63 suites, 2,189,520 checks, 0 in-suite failures, 0 timed out.
- Physical gPTP leg: 209 checks, 0 failures.
- `syn/yosys/run.sh`: 58 / 58 tops, 0 unjustified tied inputs.
- behave: 406 scenarios.
- xvlog: 0 findings.
- Quick gates: lint, port contracts, naming, test evidence, hygiene, `pp_resource_gate.py check-baseline`, `check` at all three endpoints, ROM ledger byte-identical, submodule and gPTP docs, capture check, both diagrams, docs_check, feature_status.
- Hosted docs-check steps under GNU Make 4.3: 44 steps; 42 run, all rc 0; 2 skipped by rule. Builder leg 1 rerun with the LiteX interpreter: rc 0.

Acceptance criteria:
- #771 acceptance 4 ("every parent gate and suite passes") is met at this head for every gate listed above.
- The hosted contexts at this head are the manager's.
- Acceptance 1 to 3 and 5 are unchanged from round 1b.

Open risks/questions:
1. `python3 scripts/ci_events.py --firmware-census` (`CI_WORKFLOWS.md:3183`, after the assigned block) exits 1 at this head. It does the same on dev `d77a8afd`'s own inputs, with byte-identical output, and this PR changes none of its inputs. Its baseline lacks the job-budget, package-cache and evidence-recording setup lines; no test command is missing. It needs its own Issue.
2. Carried from round 1b:
   - the 8x8 share under the owner exception;
   - the image build's reduced Vivado thread count;
   - processor #190's CRF item, which stays open after #190 closes.
3. R683-1-R1 (comment wording from the supplied TSpec patch) is left to the residue checklist. R683-1-S1 is not taken.
4. Physical calibration NOT RUN; no hardware.

Receipts: the lane's `round2/` directory, indexed by `MANIFEST.sha256` and `INDEX.md`. HANDOFF.md section R2 has the item-by-item detail.
