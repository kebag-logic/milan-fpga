# [A661] processor #193: shared Listener declaration on unbind of one of two sinks

**Status: STOP at item 1 of the assignment.** The measurement found two Listener
declarations on the wire for one attribute value. The assignment's STOP branch applies:
"That needs the one-applicant-per-StreamID redesign, which is a manager decision."
Items 2-4 were not started. The tree is unchanged: no commits, no edits, nothing pushed.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin confirmed)
- Branch: `193-shared-listener-leave` (local only, never pushed)
- Base: `21601694880efdfc4be3028afa3525fbc8f29c03` (processor main; remote main still there at 2026-10-20T11:37Z)
- Head: `21601694880efdfc4be3028afa3525fbc8f29c03` (= base, 0 commits)
- Assignment: issue #193 comment 6289596705 ([A10]), read in full
- Posted on #193: `[A661] TAKEN` (comment 6289893976); `[A661] STOP` with the head (comment 6289991979)
- Receipts: `receipts/` with `receipts/INDEX.md` (generated from the files present)

## 1. Item 1: the measurement

**Question (assignment item 1).** With two settled sinks on one StreamID, does an MRPDU
from the DUT carry ONE Listener declaration for that attribute value, or two? (IEEE
802.1Q-2018 10.7.7.)

**Method.** A scratch copy of the srp_top suite, outside the tree. `hdl/`, `tb/common` and
every other `tb/srp_top` file are identical to HEAD (`diff -r`, no output). The only
difference is one extra measurement group `m193` in `sim_main.cpp`
(`receipts/m193-measure-scratch.patch`, 86 lines). It makes no CHECKs: it only prints.
The bench is the suite's end-to-end one: the real KL_srp_top (decoder, listener FSMs,
encoder) and the real KL_pp_tx_slots. Frames are read off the slot serializer, and the
processor top passes those bytes unchanged:
- the encoder's slot writes go to the shared pool write mux
  (`hdl/top/protocol_processor_top.sv:2597-2609`, `:4358`);
- its slot handle goes to the arbiter's SRP lane (`:4582`, `:4593`).

So the suite bytes are the wire bytes.

The scenario:
1. Reset, then link up.
2. DECLARE_LISTENER (Ready) on sink 0, then on sink 1, both for the same
   {stream_id 1122334455660001, DA 91E0F0112233, VID 2}.
3. The peer sends one Talker Advertise JoinIn for that triple.
4. Capture the next four MSRP frames that carry a Listener value for the stream_id.
5. WITHDRAW_LISTENER on sink 0 alone, then capture three more.

Reproduce (from an empty scratch directory holding a copy of `hdl/` and `tb/`):

```
patch -p1 < m193-measure-scratch.patch
cd tb/srp_top
make run RUN_ARGS=m193
```

**Result** (`receipts/m193-measure.log`, decode in `receipts/frame-decode.md`). Both
sinks register the Advertise (tk_reg {1,1}, registrar {IN, IN}), and both declare Ready
(ls_decl {2,2}). Every frame in which both applicants transmit carries **two**
VectorAttributes with the same FirstValue:

```
frame 0 @403 ms (47 B):
01 80 c2 00 00 0e 0a 0b 0c 0d 0e 0f 22 ea 00 03 08 00 1a
00 01 11 22 33 44 55 66 00 01 00 80      <- Listener New, Ready, stream_id ...0001
00 01 11 22 33 44 55 66 00 01 00 80      <- the same value again
00 00 00 00
```

- Frame 1 (@603 ms) is identical: both applicants send New again from AN.
- Frame 2 (@803 ms) carries two JoinMt (`6c 80`), one per applicant.
- Frame 3 (@1003 ms) is a periodic frame with a single JoinMt. That is a cadence phase:
  that walk found one applicant still QA. It is not a merge.
- The independent builder's one-declaration frame for the value is 35 B:
  `... 00 03 08 00 0e 00 01 11 22 33 44 55 66 00 01 00 80 00 00 00 00`.

**Answer: two declarations go on the wire for one value.** The transmit path does not
merge them:

- each sink owns a Table 10-3 applicant (`hdl/srp/KL_srp_listener_fsm.sv:365-374`);
- the tick walk pushes one encoder event per sink that has a message (`:731-736`);
- the encoder folds only +1 successors into a run (`hdl/srp/KL_srp_encoder.sv:186-214`,
  `:388-391`), so an equal FirstValue breaks the run and goes out as a second
  VectorAttribute in the same Listener message (`:641-659`).

The same run also reproduces the issue in simulation. After sink 0 alone is unbound:

- the next frame (@1402 ms) carries only Lv, Ready (`b4 80`) for the value that sink 1
  still declares;
- sink 1 next declares the value with the periodic JoinMt at @2003 ms;
- so a Milan peer registrar (Milan v1.2 4.2.7.2.2: IN / rLv! -> MT) holds no
  registration for about 0.6 s.

## 2. Why this is a STOP

The assignment, item 1: "If two declarations go on the wire for one value: STOP and
report. That needs the one-applicant-per-StreamID redesign, which is a manager
decision." The clauses behind it:

- IEEE 802.1Q-2018 10.7.7: "A full MRP Participant maintains a single instance of the
  Applicant state machine (Table 10-3) for each Attribute value". Here there is one
  instance per sink, so N sinks on one StreamID give N instances for one value.
- IEEE 802.1Q-2018 10.2: one Participant per application in an end station. Both
  applicants send through the same MSRP participant, in the same MRPDU.
- IEEE 802.1Q-2018 35.2.6 NOTE: the rule "ensures that there is at most one Listener
  Declaration … for any given value of StreamID on any given port". The DUT sends two.
- IEEE 802.1Q-2018 35.1.2.2: a Listener withdraws its declaration with
  MAD_Leave.request only for "Streams that are no longer wanted". With one applicant per
  sink, a reference count on Lv! alone (item 2) would still leave two declarations per
  value, so item 2 cannot be met on this structure.

The issue's source line references are from processor 2cbed0a9. At 21601694 the same
code is at:

- `KL_srp_listener_fsm.sv:352-374`: per-sink applicant registers and `app_declaring_f`;
- `KL_srp_listener_fsm.sv:525-528`: the teardown arm that applies Lv! with no
  same-StreamID check.

## 3. Changes

None. No file in the tree was edited and no commit was made (head = base).

## 4. New checks and planted mutants

None. Item 3 was not started (STOP). The scratch `m193` group has no CHECKs and is not
a suite case.

## 5. Gates (base and head)

None run: no file changed, so no processor gate or campaign builds a changed file. The
only build was the scratch measurement (`receipts/m193-build.txt`):

- `make run RUN_ARGS=m193`, rc 0;
- one PINCONNECTEMPTY warning, from the unmodified `srp_top_wrap.sv`.

## 6. Scratch-parent consumer gates

The scratch parent (milan-fpga dev e26f1816 plus the three adoption patches plus this
head as the gitlink) was **not built**. There is no head change to consume, and the
lane stopped at item 1.

| Consumer gate | Base | Head | Status |
|---|---|---|---|
| (all) | not run | not run | not applicable: STOP at item 1, head = base |

## 7. Posts on #193

- `[A661] TAKEN`: comment 6289893976.
- `[A661] STOP`: comment 6289991979. It gives the head, the measured frame bytes and the
  clauses, and returns the decision to the manager.

## 8. For the manager decision (by reading only, nothing designed or verified)

One applicant per StreamID would replace the per-sink applicant plane in
`KL_srp_listener_fsm.sv` with:

- a table of at most N applicants, each keyed by stream_id;
- for each entry, the set (or count) of settled sinks that reference it.

Its behaviour would be:

- A15 joins a sink to an existing entry or allocates a new one.
- A8 applies Lv! only when the last referencing sink leaves.
- The declared FourPacked becomes the combination over the referencing sinks' registrar
  views (Ready / Ready Failed / Asking Failed, 35.1.2.2 a-c, carried in place per 35.2.6).
- The #188 leave copy and park move from the sink to the entry.

The per-sink class-D outputs (`lstn_decl_state_o`, `dbg_app_state_o`) look derivable
from each sink's entry. So no top-level port, parameter or register-map change is
evident, but that has not been designed or checked.

## 9. Housekeeping

- Scratch: one directory outside the tree and the output directory. It holds the
  measurement copy, the full make log (12746 B, sha256 af92e0d6…, kept out of here
  because it carries host paths) and extracted standards text. Its build products were
  removed after the receipts were taken.
- No toolchain, virtualenv, package, tree export or file over 200 KB is in this
  directory.
