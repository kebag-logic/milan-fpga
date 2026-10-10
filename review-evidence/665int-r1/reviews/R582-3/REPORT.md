[R582] NEGATIVE - exact head 232d466312890c978cd6f74e38550a176650fe55

# R582-3: internal independent review of PR #704 (issue #665, lane F-INT PR 1 of 2)

- Exact head `232d466312890c978cd6f74e38550a176650fe55`, tree `3e21bd325e634732436df43f2c08d1bc3eb74f3f`.
- Base `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. Delta reviewed: `25bbe4d9..232d4663`, 14 commits. That is
  the ten round-3 commits up to `b2aa3ccf` and the four round-4 commits after it (`cc4e54e0`, `e5af02e8`,
  `0bffed69`, `232d4663`).
- The review ran in a cleared-context detached clone. It is reconstructed from AGENTS.md, CONTRIBUTING.md,
  the issue body, rulings 6088423771, 6092086337 and 6094461419, the PR body and the diff.
- Prior public findings were read only after my own pass and draft verdict
  (`receipts/ledger_draft_before_prior_findings.txt`, timestamped).
- No other round-3 review was read.

**Verdict: NEGATIVE.** The round-3 and round-4 work is sound:

- each sink's started level and each source's Talker declarations are in the block;
- their writers are ordered before what promises them;
- the RTL, model twin and plants are in place;
- the census fails closed over the population, as ruled.

Every prior finding is resolved at this head. Three new MINOR findings leave four lenses unclean. All three
are in the checks, not in the shipped behaviour: at this head no classification is wrong and no writer is
wrong.

- **F1:** the census's cone, which clears a status or answer-face read, is not fail-closed one hop past the
  population.
- **F2:** the ACMP adapter's new `SID_VALID` derivation, on a move that carries no stream, is untested.
- **F3:** `TALKER_DECL` across a Domain adoption is untested.

## Findings

### R582-3-F1 - MINOR - Conformance, Tests, Robustness, Docs - `sw/mailbox/publication_census.py:50-55`, `:462-468`, `:483-495`, `:697-707`; `docs/design/MAILBOX_SPLIT.md:886-887`; PR body "Every read is mapped" - the census clears status and answer-face reads by a cone that is not fail-closed: such a read routed to the wire through a form the parser does not follow passes

- **Authority:**
  - Ruling 6092086337 item 3 requires a standing check under which "every wire-affecting read of a processor
    class-D output ... must map to a block field or a named, ruled exclusion".
  - Ruling 6094461419 asks for a census that fails closed "by construction, not by covering parser forms one
    at a time".
  - The census docstring (`:54-55`) says: "the cone over-approximates: a path it cannot rule out counts as
    reaching the wire".
  - `MAILBOX_SPLIT.md:886-887` and the PR body say a status read that reaches the wire fails the suite.
- **Evidence:**
  - The fail-closed accounting (`:697-707`) covers only occurrences of population wires. A status or
    processor read is then cleared by `cone()`, over `net.edges`. Those edges are built only from
    right-hand sides, the parentheses of `if`/`case`/`for`, and named port connections (`:462-468`,
    `:483-495`).
  - A consumer's own downstream use in a positional port, an implicit `.name` port, a case item label or a
    function's `return` adds no edge. The cone therefore stops short, and the read is accepted as status.
  - `census_cone_probe.py` part 1 (`receipts/census_cone_probe.log`) routes each of these at this head's
    datapath onto the CRF talker's `vlan_en_i`, which is on the wire:
    - the status consumer `lwsrp_talker_declared`, CENSUS row "status";
    - the processor consumer `gsi_tkdcl_w`, row "processor".
  - All 8 arms report 0 findings, PASS.
  - The plain-`assign` control of each is refused ("counted as status, but it reaches the wire").
  - A planted copy on disk passes too (`receipts/census_cone_probe_part2_control.log`, "control: tracked
    head -> 0 finding(s)").
  - These are the very forms ruling 6094461419 made the census refuse for the population, one hop later.
- **At this head:** no classification is wrong.
  - Part 2 of the probe lists every occurrence of the 37 intermediate nodes the status and processor cones
    traverse. It finds 0 that the netlist neither reads, targets nor declares.
  - Its control finds the planted positional route.
  - I also traced `lwsrp_talker_declared`, `lwsrp_idle_slope`, `lwsrp_lstn_reg0_w` (through
    `listener_observed_w` to `i_tlk_lobs_v`), `acmpl_vlan_w`, `adp_available_index` and `lwsrp_res_active`
    by hand. Each ends in `milan_csr` read-back.
- **Impact:**
  - PR 2 rewires this same file. A status or answer-face consumer that it routes to egress through one of
    these forms would pass the mailbox suite while the block lacks the value. That is the round-1 failure the
    census exists to stop.
  - The docstring and the design page claim an over-approximation the code does not have.
- **Required outcome:**
  - Every non-comment occurrence of every node a status or processor cone traverses is accounted for: a
    declaration, an assignment target, or a read the netlist recorded. Anything else fails, as for the
    population.
  - Equivalently, the census refuses the 8 probe arms by name.
  - Self-test plants cover at least the positional and case-label forms.
  - The docstring, MAILBOX_SPLIT.md and the PR body stay true. Alternatively, they state this limit
    explicitly, with a ruling accepting it.
- **Verification:**
  - `python3 -I census_cone_probe.py <tree>` part 1 shows 0 escaping arms.
  - `publication_census.py --check --selftest` passes at the head with the new arms refused.

### R582-3-F2 - MINOR - Tests - `sw/firmware/ctrl/acmp/acmp_mbx.c:78`; `sw/firmware/ctrl/test/test_acmp_mbx.cpp:610`, `:688`; `sw/firmware/ctrl/test/ctrl_mutants.py:614` - the adapter's `SID_VALID` on a bound or started move with no stream is untested; a stale stream_id can reach the datapath unseen

- **Authority:**
  - The contract (`mailbox.yaml`, BINDING) says `SID_VALID` "says SID_LO and SID_HI hold the stream_id the
    sink settled on".
  - AGENTS.md section 6, Tests: positive, negative and boundary behaviour covered. Each test can fail for
    the defect it claims to detect.
- **Evidence:**
  - Round 3 added `mbx_pub_sink_binding`. For a move whose stream did not change, the adapter passes
    `stream_id != 0u` as `SID_VALID` (`acmp_mbx.c:78`).
  - The author plants only the `false` polarity (`pub-acmp-adapter-drops-sid-valid`, killed by B12). B12
    exercises only a settled sink, where the stream is non-zero.
  - I planted the `true` polarity (`r582-adapter-sid-valid-always`). It escapes every arm that links the
    adapter:
    - `acmp`, `acmpif2`, `acmpnvm`, `acmpwalk`, `walk`, `entity`;
    - all six SRP suites at one and two interfaces, `test_acmp_mbx.cpp` with the SRP composition included.
  - Evidence: rc 0 everywhere (`receipts/r582_fw_demo_run1_partA.log`, Part A; `receipts/r582_fw_probes.log`).
  - The 100 % branch ratchet cannot see it, because the expression is an argument, not a branch.
  - The consequence is observable. A sink settles on stream X, is unbound, and is bound again. That bind
    moves bound and started but not the stream (0 to 0). With the plant it sets `SID_VALID` over the stale
    `SID_LO`/`SID_HI`, so the datapath takes X for a sink that settled on nothing.
  - A disposable demonstration test, `AcmpMailbox.R582DemoNoStaleStreamAfterRebind`, appended in a scratch
    clone, shows this:
    - it passes unplanted;
    - it fails planted at both interfaces, on "a re-bound sink with no settled stream carries no stream_id"
      (`receipts/r582_fw_demo.log`, Part B).
- **Impact:** a regression of this one expression would let the split datapath accept a stream the firmware
  never settled on. That is a wire-affecting error in PR 2, and no gate would notice it.
- **Required outcome:**
  - A named adapter test covers a bound or started move with no settled stream after a stream was published,
    for example settle, unbind, bind again. It requires `SID_VALID` clear and no stream_id on the datapath.
  - The `true`-polarity plant (or an equivalent) joins `ctrl_mutants.py` and is killed by that test on its
    words.
- **Verification:** `test_ctrl_firmware.py --self-test` lists the plant as caught by the named test at both
  interfaces.

### R582-3-F3 - MINOR - Tests - `sw/firmware/ctrl/srp/srp_mbx.c:189`, `:653`; `sw/firmware/ctrl/test/srp_mbx.cpp:157`; `docs/design/MAILBOX_SPLIT.md:824`, `:976` - `TALKER_DECL` across a Domain adoption is untested; a writer that drops it there passes every SRP suite

- **Authority:**
  - The design page says `TALKER_DECL` is written before "the declarations it describes, at participant
    creation and Domain adoption" (`:824`).
  - Its Verification table (`:976`) says the host tests check "its Domain, slope and Talker declarations
    before every MRPDU that carries them, read at each record's commit".
  - Ruling 6092086337 item 2 asks for the same checks as the other values.
  - AGENTS.md section 6, Tests.
- **Evidence:**
  - `PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst` reads `TALKER_DECL` at commits after startup
    and a link restart only. No test adopts a Domain and then reads `TALKER_DECL`.
  - `PubDomainPrecedesEveryDeclarationThatCarriesIt` adopts a Domain but checks only `SR_DOMAIN`.
  - First plant: clearing `TALKER_DECL` after the adoption's `declare_sources` (`:653`). It is caught only
    by the publication-term access count, because it adds a write (`receipts/r582_fw_demo_run1_partA.log`).
  - Count-neutral plant `r582-declarations-zero-at-adoption`: `declare_sources` (`:189`) publishes 0 while an
    adoption is owed. It escapes all six SRP suites at one and two interfaces, rc 0
    (`receipts/r582_fw_demo.log`, Part A).
  - Demonstration test `Srp.R582DemoTalkerDeclHeldAcrossAdoption` passes unplanted. It fails planted at both
    interfaces, on "every Talker MRPDU after a Domain adoption left with TALKER_DECL set" (Part B).
- **Impact:**
  - The split datapath's CRF C-TAG interlock reads this level (`milan_datapath.sv:5677-5678`, `:6225`).
  - A regression would untag the CRF stream after the adoption that changes its VID, exactly when the tag
    matters.
  - The Verification table claims a coverage the suite does not have.
- **Required outcome:**
  - A named SRP test reads `TALKER_DECL` at each Talker-carrying commit after a Domain adoption, and holds
    it after.
  - A plant on the adoption path (the count-neutral one above, or an equivalent) is killed by it on its
    words.
- **Verification:** `test_ctrl_firmware.py --self-test` lists the plant caught by the named test at both
  interface counts.

RESIDUE: none. SUGGESTION: none new. R583-1-S1/S3 and R582-2-S1 = R583-2-S1 (the 32-source mask) remain
optional and are not taken. I agree they do not affect coverage.

## Prior public findings at this head

| Finding | Status at `232d4663` | Evidence (this round) |
|---|---|---|
| R582-1-F1 (MAJOR), the started level | **Resolved** | <ul><li>`BINDING.STARTED` [2] on `pub_started_o` (`KL_mbx.sv:71`, `:301`, `:317`).</li><li>Written by `publish()` before any frame (`acmp.c:205-209`, `transmit` `:288`) and in `finish` before the notifier (`:490`). `acmp_set_started` publishes before it returns (`:1196-1206`).</li><li>A started-only move is one `BINDING` write that keeps `SID_VALID` (`acmp_mbx.c:71-80`).</li><li>RTL P1 to P3: mbx `make` passes 402/447/32/404/449/389. RTL plants `top-pub-started-*` are caught within 175/175.</li><li>Model twin plant caught. The author's moved, wrong-field and skipped plants plus 2 adapter plants are caught (ctrl 34/34).</li><li>My own plants (unbind keeps started, restore drops started, driver puts STARTED on SID_VALID, model reads STARTED from BOUND) are each caught.</li><li>F2 is a new, separate gap.</li></ul> |
| R582-1-F2 = R583-1-F1, the Talker declarations | **Resolved** | <ul><li>`TALKER_DECL.DECLARED` on `pub_talker_decl_o`.</li><li>Set once every source joined, before any MRPDU (`srp_mbx.c:183`, `:189`). Withdrawn before destroy and reset (`:355`, `:743`).</li><li>RTL and model plants are caught, and the 7 SRP plants are caught (SRP 23/23 publication table).</li><li>My wrong-interface plants for the set and the withdrawal are caught.</li><li>Census row `pp_cd_srp_tk_decl_state_w -> crft_class_a_w` maps to `TALKER_DECL.DECLARED`.</li><li>F3 is a new, separate gap.</li></ul> |
| R582-1-F3, `DA_GATE` | **Resolved** (recorded choice, ruling 6092086337 item 4) | <ul><li>The contract text no longer claims equivalence (`mailbox.yaml`, `KL_mbx_pkg.sv:303`, `mbx_contract.h`, `MAILBOX_CONTRACT.md`).</li><li>The design page's choices name the egress consequence and F3b. Census row DA_GATE: "DA validity only".</li></ul> |
| R583-1-F2, the gate's interface | **Resolved** | <ul><li>`DaGateOpensOnTheAcquiringInterfaceAloneBeforeItsReport` and `DaGateOfEveryInterfaceOpensBeforeItsOwnReport` (`test_maap_mbx.cpp:152`, `:168`).</li><li>`rv-maap-gate-on-interface-0` is caught in `maap_if2` by both tests (10 failed checks, `receipts/r582_pub_plants.log`).</li></ul> |
| R583-1-F3, `idle_slope_bps` | **Resolved** | <ul><li>`mbx_model.h:168` and `frames.hpp:31`, plus every user.</li><li>No unqualified `.idle_slope` field remains under `tb/verilator/mbx` or `sw/firmware/ctrl`.</li></ul> |
| R582-2-F1 = R583-2-F1, the census fails closed | **Resolved as ruled** (population derived from the instance; every occurrence accounted for) | <ul><li>Census at head: 25 wires, 89 occurrences, 25 + 25 + 39, `selftest: 0 of 35 arm(s) failed`.</li><li>R582-2 `census_probes.py` rerun: `probes: 6, unexpected: 0`.</li><li>R583-2 `census_escape_probe.py` rerun: all 5 refused.</li><li>`census_textual_crosscheck.py`: 25/25/39, 0 unaccounted.</li><li>Six further forms of mine refused (`receipts/census_extra_forms.log`).</li><li>The next hop is F1, new.</li></ul> |
| R582-2-R1 (RESIDUE) | **Applied** | `mbx_model.h:162-163` and `mbx_model.c:27` carry the exact wording. |
| R583-2-S2 (required now) | **Resolved** | <ul><li>`srpcmp` arm (`ctrl_arms.py:417-434`, `test_ctrl_firmware.py:186`).</li><li>The comparator self-test reports 5 controls PASS and 18 plants (`receipts/srp_wire_compare_selftest.json`).</li><li>Named in MAILBOX_SPLIT.md Verification and the ctrl README.</li></ul> |
| R583-1-S1, S2, S3; R582-2-S1 = R583-2-S1 | Optional, not taken | No effect on coverage. |

R583-1's `consumer_census.py` rerun at this head (`receipts/r583-1_consumer_census_at_head.txt`):

- Its read counts are identical to its round-1 receipt.
- Every one of its 30 read lines is a census read (`receipts/census_vs_r583-1.txt`).
- The census adds 9 reads that script does not see: 7 declaration initialisers (`:1765`, `:4912-4920`,
  `:7327`) and the started level's 2 reads (`:4952`, `:5376`).

## Focus items (round-3 assignment and this round's brief)

- **BINDING.STARTED.**
  - Written before the BIND_RX response that echoes STREAMING_WAIT (`bind()` sets `started = !sw` before
    `bind_response`, whose transmit publishes first), and before the notifier and the return to the AECP side
    (`acmp_set_started`).
  - A started-only change keeps `SID_VALID` (B12; D14 "a stop with the stream unchanged").
  - Unbind clears it (`acmp.c:857`), and a restore restores it.
  - The datapath consumes `bound & ~started` (`milan_datapath.sv:5375-5376`), so STARTED while unbound has
    no effect, and the firmware keeps it 0.
  - RTL checks, model twin, ordering test and the three plants are present and caught.
- **TALKER_DECL.**
  - Written before any declaration leaves: `declare_sources` runs before the transmit loop.
  - Cleared before reset or destroy removes the participants.
  - A creation that fails publishes nothing, and the earlier withdrawal leaves it at 0, the untagged
    direction.
  - The CRF interlock (`:5677-5678`, `:6225`) maps to it in the census.
  - The timing choice (declared from creation, the processor only once its DA gate opens) is public on the
    design page. Its F3b question is pending a manager decision (below).
- **Census:**
  - Runs first in the mbx `make` (`all: census ...`).
  - 39 reads: 10 field, 14 status, 15 answer face.
  - Self-test 35 arms, 0 failed. A planted unmapped read is refused three ways.
  - Population-level fail-closed holds: the round-2 probes plus six further forms
    (`receipts/census_extra_forms.log`: generate-if, `let`, sensitivity list, macro body, ternary,
    concatenation lvalue) are all refused.
  - Cone-level, see F1.
- **DA_GATE:** documented as address validity with its egress consequence. The analysis "with policing on,
  the gates agree" holds: LICENCE already needs a registered Listener, which implies the processor's
  probe-or-Listener term.
- **Two-interface MAAP tests:** present. `rv-maap-gate-on-interface-0` is killed by both. Harness fields are
  `idle_slope_bps`.
- **All-fabric default.**
  - By construction, no input of the default build changed. `sw/litex/milan_soc.py`'s three hunks are all
    inside `CtrlMailbox`, which only `--ctrl-mailbox` (default off, `:3345`) instantiates.
  - `KL_mbx*` is referenced by no other build input. No default-image firmware source is touched
    (`receipts/changed_files_base_to_head.txt`).
  - I did not rerun the export. The byte-identity proof is the author's export at `bafd6a36`, and round 4
    changed no SoC, RTL or image source (`git diff --stat b2aa3ccf..HEAD`).
- **Firmware size:** 81,680 B (35.6 %) and 124,176 B (54.1 %) of 229,376 B. The +1,312 B and +1,504 B
  deltas are arithmetically consistent. No RV32 image source changed after `b2aa3ccf`. Not re-measured (see
  limits).
- **Mailbox area (measurement only):** the +1,168 FF equals the block's storage exactly. Per interface:
  - `DA_GATE`, `LICENCE`, `TALKER_DECL`: 16 each;
  - `IDLE_SLOPE`: 32;
  - `SR_DOMAIN`: 16;
  - 16 sinks of 67: 1,072.

  The +483 LUT and the WNS are the author's out-of-context figures, not re-measured. Nothing is re-recorded.

## Lens results (artifact-specific, at the exact head)

```text
[R582] MINOR Conformance - sw/mailbox/publication_census.py:50-55, :697-707 - R582-3-F1 (ruling 6092086337 item 3's standing guarantee does not hold one hop past the population)
[R582] PASS RTL - hdl/milan/mailbox/KL_mbx.sv:62-72, :159-176, :262-321, :351-358; KL_mbx_pkg.sv:300-370; generated == tracked (gen_mailbox --check/--crosscheck/--selftest rc 0) - TALKER_DECL decode/mask/reset/read-back, BINDING widened to 3 bits with STARTED, every pub_* output width, sid gating left to the reader; milan_soc.py CtrlMailbox binds the 11 pub ports; lint_rtl --check --self-test 90<=90; mbx make 402/447/32/404/449/389; mutants.py 175 of 175
[R582] MINOR Robustness - sw/mailbox/publication_census.py:462-468, :483-495 - R582-3-F1 (unparsed downstream forms under-approximate the cone)
[R582] MINOR Tests - acmp_mbx.c:78 / test_acmp_mbx.cpp:688; srp_mbx.c:189,:653 / srp_mbx.cpp:157; publication_census.py - R582-3-F1, F2, F3
[R582] MINOR Docs - publication_census.py:54-55; docs/design/MAILBOX_SPLIT.md:886-887; PR body - R582-3-F1 (claimed over-approximation)
```

What each lens examined, clean parts included:

- **Conformance.**
  - Rulings 6088423771, 6092086337 (items 1-6) and 6094461419 (F1 items 1-4, S2, R1), checked against
    `mailbox.yaml`, publication section.
  - Writer order in `acmp.c:196-212`, `:285-300`, `:486-495`, `:805-865`, `:1196-1206`; `acmp_mbx.c:66-80`;
    `srp_mbx.c:73-83`, `:156-191`, `:631-656`, `:725-760`, `:335-360`.
  - Milan v1.2 5.3.8.7 against `milan_datapath.sv:5375-5376`, `:6265-6270`, `:5880-5890`. 802.1Q 35.1.2
    against `:5677-5678`, `:6225`.
  - Clean except F1's standing guarantee.
- **RTL:** as the PASS line above. There is no CDC, since the block is single-clock `clk_i`. The decode adds
  one compare and one register. The reset clears all.
- **Robustness.**
  - Partial strobe, holes, absent interface and reset (P4/P5, plants).
  - `acmp_set_started` on an unbound sink refuses.
  - `mbx_pub_sink_binding` refuses an out-of-range interface or sink (D14).
  - SRP creation failure leaves `TALKER_DECL` 0. A reset whose re-creation fails is funded (bounds
    `SRP_MBX_PUB_POLL_MAX` 40, `EVENT_MAX` 6; pass bounds 3,346 / 4,235 = +19 / +22, consistent).
  - The census raises `CensusError` (rc 2) on unbalanced brackets, no `milan_csr`, or a second wrapper.
  - Unclean on F1.
- **Tests:**
  - The author's plants:
    - full tables: ctrl 505/505, SRP 261/261, RTL 175/175;
    - the publication subsets again on their own: ctrl 34/34, SRP 23/23.
  - My firmware plants: 6 of 8 caught by named checks, plus the count-neutral E2b. Two escapes (F2, F3) are
    confirmed with demonstration tests.
  - Coverage ratchet: 22 files, writers at 100 %.
  - Unclean on F1, F2 and F3.
- **Docs.**
  - `ARCHITECTURE_HW_SW_SPLIT.md:88-92`; `MAILBOX_SPLIT.md:804-1000`, `:1142-1170`; `MAILBOX_CONTRACT.md`
    (generated); the ctrl, srp, maap and mbx READMEs; the Makefile; the PR body.
  - `docs_check` rc 0; `check_em_dash --base 7c1b52be` 0 findings over 494 lines; `gen_toc --check` OK;
    `check_py_idiom`, `gen_module_matrix --check`, `measure_naming --check`, `check_hygiene --check` and
    `git diff --check` all rc 0.
  - Figures cross-checked: 39 = 10 + 14 + 15, 33 plants = 31 text + 2 table, 25/89, the access bounds and
    the FF arithmetic.
  - Unclean on F1. F3's Verification-table claim is carried by F3's test fix.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | rulings 6088423771, 6092086337, 6094461419; `mailbox.yaml`; writer code in `acmp.c`, `acmp_mbx.c`, `srp_mbx.c`, `maap_mbx.c`; `milan_datapath.sv:5375-5376`, `:5677-5678`, `:6225`, `:6265-6270`; census rows | R582-3 | 232d466312890c978cd6f74e38550a176650fe55 |
| RTL | CLEAN | `KL_mbx.sv`, `KL_mbx_pkg.sv`, `mailbox_skeleton.py`, `gen_mailbox.py`, `tb_mbx_top.sv`, `milan_soc.py` `CtrlMailbox`; lint, mbx `make`, `mutants.py` 175/175 | R582-3 | 232d466312890c978cd6f74e38550a176650fe55 |
| Robustness | UNCLEAN (F1) | P4/P5; refusal paths in `mbx.c`, `acmp.c`, `srp_mbx.c`; SRP bounds; census failure modes and cone probe | R582-3 | 232d466312890c978cd6f74e38550a176650fe55 |
| Tests | UNCLEAN (F1, F2, F3) | `suite.hpp`, `test_acmp.cpp`, `test_acmp_mbx.cpp`, `test_maap_mbx.cpp`, `srp_mbx.cpp`, `test_unit_driver.cpp`, `ctrl_mutants.py`, `srp_pub_mutants.py`, `census_plants.py`; author plants rerun; own plants; 2 demos | R582-3 | 232d466312890c978cd6f74e38550a176650fe55 |
| Docs | UNCLEAN (F1) | the docs, READMEs, Makefile and PR body above; docs gates | R582-3 | 232d466312890c978cd6f74e38550a176650fe55 |

## Executed evidence (source head; reviewer clone, scratch export and disposable clone)

Every command ran at `232d4663`. The environment is in `env.sh`: pinned Verilator 5.050 (wrapper sha256
`905795b9...`, `--version` "Verilator 5.050 2026-07-01 rev v5.050"), the pinned RV32 SDK installed into
scratch by `ci_rv32_sdk.py` from the pinned archive (digest verified), GoogleTest/GMock 1.14.0, and lwSRP at
its pin `9197193e`.

| Receipt (`receipts/`) | Command | Result |
|---|---|---|
| `census.log` | `publication_census.py --check --selftest` | rc 0; 39 checks, 0 failures; 25 wires, 25/25/39; selftest 0 of 35 failed |
| `census_list.txt`, `census_vs_r583-1.txt`, `r583-1_consumer_census_at_head.txt` | `--list`; R583-1 script rerun and compared | superset, no read missed |
| `rerun_R582-2_census_probes.log`, `rerun_R583-2_census_escape_probe.log`, `rerun_R583-2_census_textual_crosscheck.log` | the round-2 reviewers' scripts, unmodified | 6/6 as expected; 5/5 refused; 0 unaccounted |
| `census_extra_forms.log` | `census_extra_forms.py` | 6 of 6 refused |
| `census_cone_probe.log`, `census_cone_probe_part2_control.log` | `census_cone_probe.py` | F1: 8 arms escape; part 2: 0 gaps at head, the planted gap found |
| `genmbx.log` | `gen_mailbox.py --check`, `--crosscheck`, `--selftest` | rc 0 |
| `mbx_make.log` | `make -C tb/verilator/mbx` (scratch export, Verilator 5.050, `VBUILD_JOBS=4`) | rc 0; 402, 447, 32, 404, 449, 389 checks, 0 failures; quick plants 6 of 6 |
| `mbx_mutants.log` | `tb/verilator/mbx/mutants.py` (scratch export) | rc 0; 175 of 175 caught |
| `ctrl_fw.log` | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --lwsrp <pin>` | 52 arms `[ok]`, `srpcmp` and the 20 shape/RV32 arms included; `mutants: 505 of 505 caught`; then stopped by me in its SRP tail (see the note below the table) |
| `r582_srp_campaign.log` | the gate's SRP tail, the same functions | rc 0; 193 + 68 = 261 SRP plants caught; both lwSRP pin arms refused |
| `r582_pub_plants.log` | the author's publication plants through the gate's own campaigns | rc 0; ctrl 34 of 34, SRP 23 of 23 |
| `r582_fw_probes.log` | own plants plus unplanted controls | controls clean; 6 caught; `r582-adapter-sid-valid-always` (F2) escaped; `r582-declarations-cleared-at-adoption` passed srp_mbx.cpp (caught only by the access count, see next row) |
| `r582_fw_demo_run1_partA.log` | E1 against 6 ctrl arms and 12 SRP suite runs; the adding plant against 12 SRP suite runs | E1 escapes all, rc 0. The adding plant is caught by the access count only. This run's Part B is void: the arms compile tests from the checkout's test directory, not the planted copy. |
| `r582_fw_demo.log` | E2b against 12 SRP suite runs; demos in a disposable clone | E2b escapes all; both demos pass unplanted and fail planted at both interfaces |
| `fw_coverage.log` | `fw_coverage.py --selftest`, `--check --lwsrp <pin> --jobs 4` | rc 0; 28 of 28; PASS, 22 files |
| `srp_wire_compare_selftest.json` | `srp_wire_compare.py --self-test` | rc 0; 5 controls PASS, 18 plants |
| `lint_rtl.log` | `lint_rtl.py --check --self-test` (Verilator 5.050) | rc 0; 90 <= 90 |
| `docs_gates.log` | docs gates (renderer-dependent ones in the pinned Markdown venv) | all rc 0 (two first attempts without the renderer exited 2 and were rerun) |
| `restore_check.txt` | post-probe integrity of the review clone | see file |

**Note on the firmware gate.** The full gate completed its 52 arms and its 505-plant ctrl campaign. To save
wall time, its SRP plant tail ran in parallel in `r582_srp_campaign.py`: the gate's own `srp_mutants.campaign`
over the full table at two interfaces, the one-interface subset and `lwsrp_pin_arms`, imported from the same
checkout. That run passed, so I stopped the gate inside its duplicate SRP tail, and it wrote no final verdict
line or rc (`ctrl_fw.rc` says so). A first attempt failed to compile only because my bench exposed the
GoogleTest headers as non-system includes. It was rerun with system-include semantics, and no source was
involved.

## Real limits

- **Not run** (these are the manager's merge-turn banks, or need external inputs):
  - the full 64-suite sweep;
  - Yosys `syn/yosys/run.sh`;
  - the `xvlog` front end (Vivado);
  - the builder and LiteX banks;
  - the all-fabric export comparison;
  - `ctrl_srp_image.py` (needs externally provisioned Picolibc, compiler-rt and LiteX sources);
  - the out-of-context area run;
  - `test_ctrl_nvm.py`;
  - `act`.
- **Author receipts only:** the byte-identity of the default build, the firmware size and the area figures
  rest on the author's receipts plus my structural check. I re-measured none of them.
- **Bench:** the firmware gate ran with host GCC 16.2.1 and GoogleTest 1.14.0. CI uses the runner's
  distribution packages.
- **Census analysis:** F1's part-2 analysis is textual and covers `milan_datapath.sv`. A `bind` or
  hierarchical reference from another file is outside it, as the PR states.
- **No hardware:** physical calibration NOT RUN. No hardware, no bitstream, and no hosted job inspected.
- **No manager bank inferred:** no manager source bank ran at this head, and none is inferred.

## Pending manager duties

- Rule on F1-F3 and the next round. Each fix is local:
  - F1: account for cone-node occurrences in `publication_census.py` and add plants;
  - F2: one adapter test and one plant;
  - F3: one SRP test and one plant.
- Answer the open F3b question from REVIEW READY 6094106295: does F3b also take `TALKER_DECL`'s timing
  (declared from creation, against the processor's declaration only once its DA gate opens)?
- At the merge turn:
  - the current-dev candidate (source base `7c1b52be`, live dev `554e61d2`): builder and native banks;
  - the all-fabric byte-identity at the candidate;
  - hosted and act acceptance;
  - publication of this packet.

R582-3 FINISHED
