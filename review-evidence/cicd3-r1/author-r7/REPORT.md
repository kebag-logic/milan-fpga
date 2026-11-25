# [A839] CICD improvement, round 7: the cause of `milan_dp`'s differing `gptp` receipts (#1003)

**Summary.** The `[#207]` line is deterministic for a given input. Neither the change nor any nondeterminism
moved it. **The two hosted runs tested different inputs.** A `pull_request` run tests the PR head merged into
the base branch's tip at that moment. Between run 45481508309 and run 45528738040, `dev-soft-core` merged PR
#995, which re-pins the gPTP processor (`gptp-processor` `1616fc8f` → `1213ac5b`). That merge landed 18
minutes before run 45528738040 started.

The line follows the gPTP pin and nothing else. That held in 40 runs of the two cases (18 on the old pin, 22 on
the new) across six trees:

- the base alone, the head and the pre-change head, each at both bases;
- both deals, and three CPU loads.

Every local output's sha256 equals the hosted receipt's `output_sha256` for the same pin. Held at one base, the
receipts are identical with and without the change, under either deal. So neither branch of the ruling applies
as written:

- **Not (a).** The line is not nondeterministic, at the base or anywhere else. No issue was filed, and nothing is
  masked.
- **Not (b).** The change does not cause it. Nothing needed fixing, so nothing was committed or pushed.

#998 acceptance 1 reads "byte-identical suite output … against its base". For `milan_dp` that now holds at one
base, locally, and the hosted run at the head reproduces those receipts exactly.

| # | Item | Result |
|---:|---|---|
| 1 | What the two hosted runs tested | Run 45481508309: `45d5c35a` merged into `2509db68` (merge `dd5cf579`). Run 45528738040: `9c625393` merged into `e608f8d8` (merge `241f036e`). The receipts' own `head` fields record both merges |
| 2 | What differs between those inputs | The PR's own 18 files, plus 25 files of #995. The only non-document ones are the `gptp-processor` gitlink, `syn/yosys/rom_digests.tsv` and the `gptp_shadow` testbench |
| 3 | Is the line deterministic? | Yes. Each pin gives one output per case in every run: 7 direct runs per case per pin, under three loads, plus 12 runs inside CI pieces |
| 4 | Does the deal change it? | No. The 4-leg and 8-leg pieces print the same line at each base, with the same `output_sha256` for every case they share |
| 5 | Does the change? | No. The `gptp`/`gptp-lat` binaries and all their inputs are byte-identical between the base alone, the pre-change head and the head, at each base |
| 6 | Round 6's other unexplained difference | `gptp_shadow`'s verdict lines (11 → 15) are #995's too: its new #106/#107 phases (326 → 424 checks, four new mutants caught) |
| 7 | Finding 1 (manager's ruling) | Written into the PR body with the #1008 link |

Head: milan-fpga `cicd-3` = `9c62539365fea8316dae2b9fd7c68defeff5cb31`, unchanged this round. No commit, no push,
nothing posted.

Host: the 96-vCPU VM. `cpu_ranges.py pick` returned no free range (rc 1, host load 62-108). So, as in rounds 4-6,
every arm ran in the session pool 64-95, which was nearly idle (two foreign simulations, on CPUs 67 and 75). Builds
went through the shared compiler cache (`OBJCACHE=ccache`, the host's single `cache_dir`). Units:
`milan-cicd-a839r7-*` (builds, `q-*`, `m-*`, `l-*`, `piece-*`), all finished.

## 1. What the line prints (`tb/verilator/milan_dp/sim_gptp.cpp:1850-1903`)

- Phase (b) of `prove_the_three_drop_counters_through_the_csr` (#207) holds the gPTP engine's four-deep event queue
  full around one valid Sync. It does this by forcing `evq_lvl_r` to 4 every cycle.
- Before the window it waits for `s1`'s response claim (`resp_claim_valid_r`), then for `s1b` to wait at the head
  (`evq_lvl_r != 0`). It then records `lvl0`, `rp0 = evq_rp_r` and `wp0 = evq_wp_r`. After 400 cycles it records
  `rp1` and `wp1`.
- It prints `[#207] full-queue window: level lvl0, rp rp0->rp1, wp wp0->wp1`.
- The check is relative: `rp1 == rp0 && wp1 == wp0`, "the full-queue window pops and pushes no event". It passes in
  every run on both pins.
- The pointers are 2-bit counters reset to 0 (`KL_gptp_engine.sv`: `evq_wp_r <= evq_wp_r + 2'd1`). So `wp0` is
  the number of events the engine queued since reset, modulo 4, and `rp0` the number it took.
- The printed absolute values therefore show the engine's whole event history before this arm. Any change to what
  the gPTP program queues before it moves them. #995's `1213ac5b` changes that program and the engine: "Send a new
  master's first Announce in the handler that takes the role" (`c5b4f8c`), and "Run each mastership on this
  oscillator" (`d0a0e3b`). At the window, the queue has taken one more event modulo 4 (`rp 0` → `1`, `wp 1` → `2`,
  level 1 in both).
- The harness reads no environment, clock, random source or argument. The loops before the window count
  simulated cycles. Its only runtime inputs are files: the shipping AEM image (built at run time from
  `configs/endstation_ax7101_1x1_tdm8.yaml`) and the `$readmemh` images (`gptp_ucode.hex` or `gptp_lat_ucode.hex`,
  `ucode.hex`, `ltn_rom.hex`). Its temporary paths carry the PID, but none is printed: every run's output is
  byte-identical for its pin.

## 2. The two hosted runs' inputs (receipts/hosted/)

- **The merge commits.** Each worker's checkout step prints the merge it tested
  (`merge-commits-from-worker-logs.txt`):
  - 45481508309 (2026-11-24 20:51Z): `HEAD is now at dd5cf57 Merge 45d5c35a… into 2509db68…`;
  - 45528738040 (2026-11-25 02:06Z): `HEAD is now at 241f036 Merge 9c625393… into e608f8d8…`.

  The receipts record the same: every `milan_dp` receipt of the first run has `head dd5cf579…, tree 23af3e5f…`,
  and every one of the second `head 241f036e…, tree af158eaa…` (`milan_dp-runA-vs-runB.txt`). Round 6 compared
  them without reading those fields.
- **What moved the base.** `e608f8d8` is `Merge PR #995: Pin FPGA-gPTP 1213ac5b`, committed 2026-11-25 02:33:46
  +01:00 (01:33Z). Run 45528738040 was created at 01:51Z.
- **The difference between the two merge trees** (`merge-trees-diff.txt`) is 43 files: the PR's own 18
  (`45d5c35a..9c625393`) and 25 others, every one of them changed by #995. Apart from documents and diagrams,
  those 25 are:
  - the `gptp-processor` gitlink;
  - `syn/yosys/rom_digests.tsv`;
  - `tb/verilator/gptp_shadow/{sim_main.cpp, gptp_shadow_wrap.sv, mutants.py, test_mutant_lifecycle.py, README.md}`.

  The PR's 18 files include no RTL and no `milan_dp` harness source.

## 3. The local matrix (receipts/local/)

**Trees** (`trees.txt`). Each is a clone of the lane, with the head merged into the base as GitHub's
`refs/pull/1003/merge` does:

| Tree | Base | Head | gPTP pin | Tree id |
|---|---|---|---|---|
| B0 | `2509db68` | (the base alone) | `1616fc8f` | `3b1a7562` |
| H0 | `2509db68` | `9c625393` (round-5 deal, 8 legs) | `1616fc8f` | `bbbe38c7` |
| O0 | `2509db68` | `45d5c35a` (old deal, 4 legs) | `1616fc8f` | `23af3e5f` = hosted `dd5cf579`'s |
| B1 | `e608f8d8` = `dev-soft-core` now | (the base alone) | `1213ac5b` | `1c9db59a` |
| H1 | `e608f8d8` | `9c625393` (round-5 deal) | `1213ac5b` | `af158eaa` = hosted `241f036e`'s |
| O1 | `e608f8d8` | `45d5c35a` (old deal) | `1213ac5b` | `dd97ab58` |

So O0 is exactly run 45481508309's input and H1 exactly run 45528738040's (the tree ids equal those of the hosted
merges, which were fetched by SHA). The piece trees P4O0, P8H0, P4B1, P8B1, P4H1 and P8H1 are further clones of
O0, H0, B1, B1, H1 and H1.

**The binaries** (`build-sha256.txt`). `make ci-prepare build-gptp build-gptp-lat` was run in each of the six
trees. Within each base, all six artefacts are byte-identical across the base, the head and the pre-change head:
the two Verilator outputs, both binaries and both gPTP images.

| | `gptp_ucode.hex` | `Vmilan_dp_gptp` | `Vmilan_dp_gptplat` | `ucode.hex`, `ltn_rom.hex` |
|---|---|---|---|---|
| B0 = H0 = O0 | `8333beee…` | `af48d3bf…` | `0876e6db…` | `264fbb03…`, `23cc67ee…` |
| B1 = H1 = O1 | `38d4506a…` | `1c0bc0c2…` | `22e318c5…` | the same |

The change touches neither binary nor any of its inputs. The gPTP pin changes both binaries and the gPTP image.

**Direct runs** (`direct-runs.txt`). These are the CI driver's own command, `make -s -C tb/verilator/milan_dp
exec-<case>`, in each tree. They ran under three loads:

| Round | Trees | Load | Walls |
|---|---|---|---|
| Q | all six | one simulation per CPU, twelve at once on 76-87 (SMT neighbours) | 948-1061 s |
| M | B0, B1, H0, H1 | one per CPU on 80-87, beside round L, four pieces and two foreign jobs | 951-1034 s |
| L | B0, B1, H0, H1 | two simulations per CPU (`gptp` and `gptp-lat` of one tree on one CPU) on 76-79 | 1922-2033 s |

Rounds M and L kept stdout and stderr apart, as the driver does (stderr was empty), so each output's sha256 is the
receipt's `output_sha256`.

| Pin | Case | Runs | Every output's sha256 | `[#207]` |
|---|---|---:|---|---|
| `1616fc8f` | `gptp` | 7 | `767854b00c58fb0b` | `rp 0->0, wp 1->1` |
| `1616fc8f` | `gptp-lat` | 7 | `699262f363514f8c` | `rp 0->0, wp 1->1` |
| `1213ac5b` | `gptp` | 7 | `fded66ab69042994` | `rp 1->1, wp 2->2` |
| `1213ac5b` | `gptp-lat` | 7 | `691b82a4fe5abcda` | `rp 1->1, wp 2->2` |

Every run printed `212 checks: 212 PASS, 0 FAIL` and exited 0. Two loads that double the wall give the same bytes.

**Pieces, under each deal** (`pieces/`, `receipts-old-pin.txt`, `receipts-new-pin.txt`). Each piece ran as a
hosted worker runs it: `make clean`, then `ci_make_cases.py --suite milan_dp --shard L/T --jobs 2` on four CPUs,
with the driver's build and longest-first start. `gptp` is in leg 0 and `gptp-lat` in leg 1 under both deals
(`names[L::T]`). Their neighbours differ:

- 4 legs: leg 0 also holds `counters-1-frames crflic dynmap nxn4c aclk bootsa`; leg 1 holds `counters-8-frames
  tspec8 nxn nolpf maprec8 render-mutants`.
- 8 legs: leg 0 holds `crflic nxn4c bootsa`; leg 1 holds `tspec8 nolpf render-mutants`.

| Piece tree | Base | Code | Deal | `[#207]` (legs 0 and 1) |
|---|---|---|---|---|
| P4O0 | `2509db68` | `45d5c35a` | 0/4, 1/4 | `rp 0->0, wp 1->1` both |
| P8H0 | `2509db68` | `9c625393` | 0/8, 1/8 | `rp 0->0, wp 1->1` both |
| P4B1 | `e608f8d8` | base | 0/4, 1/4 (the base's own) | `rp 1->1, wp 2->2` both |
| P8B1 | `e608f8d8` | base | 0/8, 1/8 | `rp 1->1, wp 2->2` both |
| P4H1 | `e608f8d8` | `9c625393` | 0/4, 1/4 | `rp 1->1, wp 2->2` both |
| P8H1 | `e608f8d8` | `9c625393` | 0/8, 1/8 | `rp 1->1, wp 2->2` both |

All twelve pieces exited 0.

## 4. Hosted = local, per pin

`receipts-old-pin.txt` sets hosted run 45481508309's 26 `milan_dp` cases beside P4O0 and P8H0, case by case.
`receipts-new-pin.txt` sets run 45528738040's 26 beside P4B1, P8B1, P4H1 and P8H1. Each cell is (outcome,
returncode, `output_sha256`).

- **Every case each local piece ran (14 at four legs, 8 at eight) has the hosted receipt of the run with the same
  pin.** That includes `gptp` and `gptp-lat`. There are 0 differences in either table.
- **At one base, the change and the deal change no receipt.** On `e608f8d8`, the base under its own deal (P4B1),
  the base under the new deal (P8B1), and the head under both (P4H1, P8H1) agree on every case they share. On
  `2509db68`, the pre-change head (P4O0) and the head (P8H0) agree likewise.
- So the only `milan_dp` receipts that differed between the two hosted runs are explained by the base's re-pin. At
  either pin they are identical with and without the change. Nothing is masked or excepted: no line was removed
  or normalised in any comparison here.

## 5. What this means for the receipt comparison (#998 acceptance 1)

- Comparing two hosted PR runs compares two merges. When the base moved between them, each suite whose inputs the
  base changed is compared across different inputs. Equality there is not evidence, and a difference is not a
  defect.
- Between these two runs the base changed:
  - the gPTP processor, which reaches every suite that elaborates the gPTP plane (`milan_dp`'s `gptp`,
    `gptp-lat`, `bootsa` and the gmstep build, `gptp_plane`, `gptp_txts`, `gptp_shadow`, `milan_dp_gm_steps` and
    others);
  - the `gptp_shadow` testbench;
  - the Yosys ROM digests.

  Of those, only `gptp_shadow` (its verdict lines) and `milan_dp` (`gptp` and `gptp-lat`) printed anything
  different. Both are now explained.
- **The comparison that answers acceptance 1 holds the base**: the head against its base, at one base. For
  `milan_dp` that is §4: identical receipts at `e608f8d8` and at `2509db68`. Hosted run 45528738040 at the head
  reproduces the same-base local receipts exactly.
- I have no hosted run of the pre-change head (or of the base) at `e608f8d8`: `dev-soft-core` has no push run of
  rtl-full, and the only later PR run on that base was cancelled. Getting one would need a push or a re-run,
  which this round's rules allow only under (b). The local same-base result stands in for it, and it is tied to
  the hosted runs by the identical tree ids and output digests above.
- **Round 6's suite comparison, corrected.**
  - Its "verdict lines identical for 63 of 65 suites" explained `capture_coherence` (per-leg tallies by
    construction) but not `gptp_shadow`. `gptp_shadow`'s eleven verdict lines became fifteen because #995 added
    its #106/#107 phases: `326 checks` → `424 checks`, and four new mutants caught
    (`gptp_shadow-verdicts-runA-vs-runB.txt`).
  - Its receipt result "identical for 5 of 6 suites" stands, and `milan_dp` is now explained. With these two
    corrections every difference between the two runs is accounted for: by construction (`capture_coherence`'s
    tallies), by #995 (`gptp_shadow`; `milan_dp`'s `gptp`, `gptp-lat`), or by new case suites (`follow_ring`,
    `media_phase`).

## 6. Finding 1, as ruled

The manager ruled that #998 acceptance 2, for this PR, means two things. Every job the PR touches is within the
bound with margin, which is already done for the Verilator workers and `firmware-boundary`. And no job gets
slower. The jobs this PR does not touch are #1008, and the four fail-fast watchers span their run by design, a
documented exception. #1008 records both exceptions, the watchers and rtl-full's nightly physical gPTP job.

The PR body now says this:

- in Status;
- in a new Review-findings row;
- in Known limitations, where the untouched jobs' list is replaced by the #1008 link. The table stays in #1008.
- The "no job gets slower" evidence is stated from the hosted runs at the head. The touched jobs are each within
  their earlier spans: the workers' slowest 27.7 minutes, and `firmware-boundary` 13.2/14.1/5.5 against 25.5.
  The untouched jobs run unchanged steps; their minutes there are runner variance (`firmware-control-mutants`
  0.99 × its slowest earlier window).
- One stated exception: the first run after a workflow change rebuilds the cached Yosys, as before. "Prepare pinned
  Yosys" took 12.7 minutes once.

## 7. Said plainly

- **A unit started and stopped.** I first started round L as four sequential units, then stopped them within a
  second to start it as eight units, two per CPU. The stopped units had begun to write the same output files; the
  new units truncated and rewrote them before any run ended. No progress line came from the stopped units, and
  every round-L output is complete (212 checks, rc 0).
- **The compiler cache.** Builds used the shared cache, so each took about 15 s. A cache is keyed by content and
  cannot change a model. The binaries' own digests are what §3 compares.
- **Scratch.** `/data-2/milan/tmp/cicd-a839/r7` holds 9.2 GB in twelve trees, kept for re-runs; the lane's scratch
  totals about 19 GB of 40. `/data-2` is at 93 %. Nothing was removed under `/data` or `/data-2` this round. A
  stray copy of a script that I had just written in my own output directory under `/home` was removed after a
  `cmp`.
- **The lane.** Still clean at `9c625393`. One `git fetch origin dev-soft-core` updated the lane's
  remote-tracking ref, and nothing else.
- Not run, as in round 6: the act replay, the full serial sweep.

## 8. Status of #998's acceptance for this PR

1. **Identical outputs against the base:** `milan_dp` is identical at one base (§4). Every other difference
   between the two hosted runs is accounted for (§5). No masking.
2. **The 30-minute bound:**
   - every job the PR touches is within it with margin, except leg A, which is stated (#737);
   - the untouched jobs are #1008;
   - the watchers and the nightly physical job are #1008's documented exceptions.
