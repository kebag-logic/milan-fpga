# Lane 190 (processor #190, CRF Talker Advertise MaxFrameSize) — HANDOFF, author [A654]

**Outcome: STOP.** I made no tree change and no commit. The branch `190-crf-maxframesize` is still at dev
`e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` with a clean worktree (receipt `receipts/r01-repo-state.txt`).

## 1. What the assignment asked, and the result for each item

| # | Assignment item | Result |
|---|---|---|
| 1 | Cite the CRF TSpec MaxFrameSize that the specs give | **29**: Milan v1.2 4.3.3.2 Table 4.4, row "CRF, 1 ts/pdu" (28 + 1, MaxIntervalFrames 1, 5632 kbps). Milan v1.2 7.3.2 and Table 7.1 set the DUT's CRF format to one timestamp per PDU. The Milan Base Audio Formats v1.1 specification covers only AAF (its clause 5, Tables 1 and 4) and assigns nothing for CRF. |
| 2 | Derive it from the PDU the DUT sends | **28-octet AVTPDU**: the IEEE 1722-2016 10.4.1 header is 20 octets, plus 8 octets per timestamp (10.4.13) × 1 (the DUT sends `crf_data_length` 8, `KL_crf_tx.sv:194`). This matches the DUT's `CRF_PDU_C = 28` (`KL_crf_tx.sv:197`). The Table 4.4 note adds one octet, giving 29. That covers the largest frame sent (802.1Q-2018 35.2.2.8.4). Receipt `receipts/r04-derivation.txt`. |
| 3 | Set the declared value to it, derived from the format parameters | **Not possible in milan-fpga alone. This is the STOP** (section 2). |
| 4 | Suite case and planted mutant | Not done, because item 3 is blocked. |
| 5 | Gates | No tree change, so no gate applies (section 5). |
| 6 | STOP if derived ≠ specified and the difference cannot be traced | **Not triggered.** Derived = specified = 29. The only difference from the raw PDU is the +1, and the Table 4.4 note accounts for it. |

## 2. Why the lane stops: the fix crosses the processor interface

The assignment says "the fix is therefore a milan-fpga PR". The code at the pinned processor `2cbed0a9`
says otherwise. Receipt `receipts/r03-code-trace.txt` has every line:

- `hdl/milan/milan_datapath.sv:5641-5643` computes `tctx_maxf_w` = 24 + 1 + 24·chans. This is the
  **AAF** row of Table 4.4. At `TALKER_WIRE_CHANS_P = 8` it is 217, exactly the value the issue
  observed.
- `hdl/milan/milan_datapath.sv:8201` hands `tctx_maxf_w[0]` to the processor as the **single** 16-bit
  `cfg_tspec_max_frame_i`. `:8192` enables every source, including the CRF source at index
  `CRF_TUID_C = N_STREAMS`.
- `hdl/milan/KL_pp_shadow.sv:300,1161` pass that scalar straight through.
  `protocol-processor/hdl/top/protocol_processor_top.sv:300` declares it as one scalar. At `:2689-2701`,
  **every** source's engine-driven `gate_open` captures that same scalar as `mfs`. The SRP core stores
  the TSpec per source (`KL_srp_top.sv:844,910`), but its only feed is that one scalar.
- The other per-request MaxFrameSize input, the service DECLARE path, is tied off at
  `KL_pp_shadow.sv:1285-1293`.
- The processor's current `origin/main` still has the same scalar port and the same capture.

So the parent has one number for all sources. It cannot make the CRF source declare 29 while the AAF
sources keep 24·N + 25. I considered four ways around this and rejected all of them:

| Alternative | Why it is rejected |
|---|---|
| Drive the scalar with 29 | Every AAF talker would declare 29 instead of 217. That under-reserves the AAF streams, the opposite violation of 35.2.2.8.4 / Table 4.4. |
| Switch the scalar per source in the parent | The parent cannot see which source a `gate_open` belongs to (`tkr_gate_src_w` is internal to the processor top). |
| Re-declare the CRF source through the service path | The engine would first put the wrong TSpec (217) on the wire, then the re-declare would race the engine's own open and close. That is a transient non-conformance plus a race. |
| Edit the processor submodule in this lane | The processor is another repository with its own review lane. This lane cannot push there, so the parent pin would point at an unpublished commit. |

Under AGENTS.md section 2, a conflict between the Issue/assignment and the implementation is published and
marked as needing a decision. I did not resolve it privately.

## 3. Decision needed (for the maintainer)

1. Approve a **processor** change that makes the engine-driven TSpec MaxFrameSize per source, for
   example `cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-1:0]` indexed by `tkr_gate_src_w` at
   `protocol_processor_top.sv:2700`, in the same shape as `cfg_stream_id_i`. Its suites would pin
   the captured `mfs` per source.
2. A milan-fpga lane would then adopt that pin. It would drive the AAF slots with `tctx_maxf_w[s]` and the CRF slot
   with a value derived from the CRF format parameters: header 20 + 8 × timestamps_per_pdu + 1,
   taken from the `KL_crf_tx` constants and not mirrored as a literal. It would add a suite case that
   pins the declared CRF TSpec against the emitted PDU length, with a planted mutant, for example one
   that feeds the AAF value to the CRF slot.
3. That lane should also correct the stale comment at `hdl/ieee1722/crf/KL_crf_tx.sv:206-211`. The comment names
   a deleted `CRF_SRP_MAXF_C` and claims 42 (the padded MSDU), but Table 4.4 says 29. The admission
   arithmetic already applies the Table 4.4 note's 68-octet floor
   (`protocol-processor/hdl/srp/KL_srp_admission.sv:127` + clamp), so 29 still reserves the CRF frame's
   real 5.632 Mb/s.

## 4. Changes

None. I added no checks and no mutants, and no RTL changed, so there is no resource or route-timing
delta.

## 5. Gate table

| Gate | Run | Result |
|---|---|---|
| — | none | No file in the tree changed, so no gate is touched. The worktree is clean at e9cbb676. |

## 6. Public trail

- TAKEN: processor #190 comment 6256534843.
- STOP: processor #190 comment 6256554371, head `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
- No push, no PR. `PR-BODY.md` is written as "Relates to" for the record only.

## 7. Receipts

See `INDEX.md`, which is generated from the files present.
