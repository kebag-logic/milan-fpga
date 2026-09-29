[A441] REVIEW READY
Commit: `931c3edfced972e01356cd989b5092a1672de5a3` (branch `b1-bench-0929`, one commit on `f9eab5bf`, one-line subject, no body, no trailers; local, not pushed)
Changed: `docs/findings/387_SOFTWARE_GM_STEP.md` (+71/-11) and `docs/findings/599_394_E1_LINK_CYCLES.md` (+72/-11), prose and two new saved-state tables only. Docs and packet only; no bench access. The redacted round-2 packet is ready for `review-evidence/b1-r1/author-r2/` on `b1-review-evidence`.

Per ruling of the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885377252):

1. **#387 acceptance 4 is PARTLY MET** (`387:12`, `:186-194`, `:196-234`).
   - Met: ten PHC steps of +9.99/-10.00 ms on a locked CRF stream, no `mr` change, MEDIA_RESET flat, neither listener unlocked, `A_MCSRV_STAT` LOCKED.
   - Not met, each a departure from the one-counted-event contract:
     - `tu` was signalled 2-3 times per step instead of one counted event;
     - asCapable was lost for 2.0 s after every step (#621);
     - DUT GPTP_GM_CHANGED rose by 3 at nine of ten edges against one grandmaster change.
   - Not observable on this bench shape: the counted render re-base, because there is no AAF stream and its count has no register. It would need an AAF stream bound into the DUT's render stage across each step and the stage's recentre count published on a register or console command (`387:110-115`).
   - The bound sentence is now "Item 2 sets no time bound", consistent with the contract check.
   - The measurement tables are byte-identical: a table-line diff `f9eab5bf..931c3edf` shows only the #387 verdict row changed and the two saved-state tables added. Result: 0 measurement, contract or hash tables changed.
2. **Raw retention and claims.**
   - 213 raw files (176,644,961 B) were copied, not moved, to private cold storage. 213/213 match the index, and **100/100 page raw-artifact rows match their retained copy**. A per-file MANIFEST (SHA-256 and page row) is on the storage and in the packet, and `sha256sum -c` gives rc 0.
   - Both pages state private cold storage keyed by their tables' hashes, and name the public packet location (`599:335-349`, `387:303-307`).
   - Extraction scripts plus outputs reproduce all four claims from hash-checked inputs, all REPRODUCED:
     - peer delay 0 ns at takeovers, 4,039-4,701 ns at releases, 373-389 ns in every other sample;
     - 7,520 console rounds, all agreeing;
     - alignment-test GPTP_GM_CHANGED 22/60 before, after and at run 1;
     - the `asl` seed CRC `809fcffa` from the seed build directory.
3. **Redacted packet.**
   - The round-1 packet is republished redacted under `r1/`, with the redaction record. Packet captures and bytecode are excluded.
   - A private-token scan over the whole packet finds 0 hits.
   - R403-1 `scrub_packet.py` gives rc 0: pages 0 findings, packet 0 findings. No interface name, account name, host MAC or home path is reported; the only MACs are the public loopback, DUT and peer ones.
4. **Saved-state layer**, recorded in both restore sections (`599:287-331`, `387:266-291`):
   - slots 227/228 then 229/230;
   - commits ok 0 then 2;
   - PP_STAT `nvm_pend` 0 then 1;
   - `PP_NVM_STAT` `0xc30000e4` then `0xc34000e4`.

   The cause comes from the captures. `nvm_pend` rose exactly across the setup, which issued the only state-changing commands before the restore. The setup's bind committed image 229 and the restore's unbind committed image 230; binding records are the only ones with a writer. The two SET_CLOCK_SOURCE writes set the sticky dynamic-state source and committed nothing. The persisted content was not compared with the found state. The pending flag cannot be cleared without a reset, which this lane may not do.

   **Separate sticky-`nvm_pend` report: it matches the contract.** Clock source has no record writer and reports "nvm_pend 1 until reset" (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11 and `:277`, "No acknowledgement touches it"). The writer commits on `nvm_dirty` only. `CHANGELOG.md` release `0x0002_0060` says those sources clear only at reset. The gap behind it is the unimplemented materializer (#70, D3). The lane now on the bench inherits pend 1 until a reset.
5. **R402-1 S1 taken** (`599:100-102`, `:219-221`): the physical edge may precede the published bracket by up to the 250 ms publication bound.

Validation, all rc 0 at `931c3edf`, foreground, not piped, physical `/data` path:
- Pinned Markdown environment:
  - `docs_check.py`: 0 findings;
  - `check_doc_style.py`: OK;
  - `gen_toc.py --check`: OK;
  - `check_em_dash.py --base 13eda870`: 0 findings over 792 added lines;
  - `check_doc_paths.py`: OK, 854 paths.
- `ci_scope.py --selftest`: PASS.
- `check_baremetal_only.py --check`: 0 findings.
- `check_feature_status.py --self-test`: 46/46.
- `git diff --check`: clean, also for `13eda870..HEAD` and `f9eab5bf..HEAD`.
- Reviewer re-derivations at the new head: R402-1 `rederive.py` pass=483 fail=0; R403-1 `rederive.py` DIFFS none.

Acceptance criteria:
- #599 acceptance 4: PASS, unchanged.
- #394 acceptance 2, e1: PASS, unchanged.
- #387 acceptance 4: PARTLY MET. The one counted `tu` event is not met (#621), and the render re-base leg stays owed.

Open risks/questions:
- The public packet commit is to be pinned by the manager at archive time.
- The sticky-`nvm_pend` issue decision rests with the manager.
- The `asl` build directory is tied to `13eda870` by name only.
- R403-1 S1, S3 and S4 and R402-1 S2 were not taken; they are outside the rulings.
