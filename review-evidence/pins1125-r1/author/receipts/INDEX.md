# Receipts (generated)

77 files, none at 200 KB; host paths and the host name are placeholders.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `docs/docs-workflow-steps.log` | 9,116 | `88213d629a525398` | # every run: step of docs.yml's gate jobs at a6864a49293ba3d0df37029abfa581468ef78dce (docs_steps.py) |
| `docs/py-idiom-with-and-without-donor-fix.log` | 1,072 | `4049b6d9e4531443` | # the Python idiom gate on a clean clone of the merge |
| `docs/ratchet-steps.log` | 1,458 | `67c7b6e33b73a647` | # the test evidence and Python idiom steps at a6864a49293ba3d0df37029abfa581468ef78dce (both rc 0), each step's last lines |
| `donor-idiom-fix.patch` | 6,075 | `2553a8962f768053` | diff --git a/tb/verilator/engine/pass_run.py b/tb/verilator/engine/pass_run.py |
| `engine/eng-j1.log` | 218 | `95ea31e94fb2f884` | # gptp-processor at 3009f9a2, tb/verilator/engine: MAKEFLAGS=-j1 make run |
| `engine/eng-j8.log` | 6,358 | `fbc57112f737508b` | # gptp-processor at 3009f9a2, tb/verilator/engine: MAKEFLAGS=-j8 make run, then make passes-test |
| `engine/eng-js.log` | 274 | `1c69e6d352ff9ec8` | # gptp-processor at 3009f9a2, tb/verilator/engine: a parent make -j4 whose recipe is +$(MAKE) -C engine run, beside one other job |
| `engine/passes-test-with-donor-fix.log` | 6,165 | `c27439fbfe2ea273` | # make passes-test with receipts/donor-idiom-fix.patch applied to 3009f9a2 |
| `firmware/boundary-only-verilator.log` | 8,819 | `8644d68616908d08` | # ctrl_boundary.py --require-rv32 --selftest --only verilator at d0483d08e6722404b54f3ce4aa13b885001c500b (compiler cache off); last 60 lines |
| `firmware/boundary-pre-merge-refusal.txt` | 3,066 | `73b8516efc25e9ac` | # ctrl_boundary.py --require-rv32 --selftest (every builder) at 1a76c9de2b684be5ed3e1f9a068020937f8d7d6b, compiler cache on: refused on a precompiled  |
| `firmware/boundary-without-verilator.log` | 8,805 | `61c6367ad114cdc0` | # ctrl_boundary.py --require-rv32 --selftest --without verilator at d0483d08e6722404b54f3ce4aa13b885001c500b; last 60 lines |
| `firmware/shard-0.log` | 3,660 | `fd6c27806a1a2d2f` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 at d0483d08e6722404b54f3ce4aa13b885001c500b (clean clone); verdict lines |
| `firmware/shard-1.log` | 105,047 | `299b9a13299d8aa9` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4 at d0483d08e6722404b54f3ce4aa13b885001c500b (clean clone); verdict lines |
| `firmware/shard-2.log` | 274 | `cc9ce7511f0892ba` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4 at d0483d08e6722404b54f3ce4aa13b885001c500b (clean clone); verdict lines |
| `firmware/shard-3.log` | 274 | `9fb23d0b708cdeb5` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4 at d0483d08e6722404b54f3ce4aa13b885001c500b (clean clone); verdict lines |
| `gptp/gptp_plane.log` | 7,307 | `f6984475a33e070e` | # make -C tb/verilator/gptp_plane (run, phc-step, link-delay) and gptp_shadow lifecycle at d0483d08e6722404b54f3ce4aa13b885001c500b |
| `gptp/gptp_shadow-run-prelim.log` | 2,682 | `d365fbdee6c883bc` | # gptp_shadow run, mutants and lifecycle at 1a76c9de2b684be5ed3e1f9a068020937f8d7d6b (before the merge) |
| `gptp/gptp_shadow.log` | 7,482 | `b9b3b1fd6e437022` | # make -C tb/verilator/gptp_shadow (lifecycle and the 14-control campaign) at d0483d08e6722404b54f3ce4aa13b885001c500b |
| `gptp/gptp_tables-txts.log` | 395 | `af91d2d4f2a6b68e` | # make -C tb/verilator/gptp_tables and gptp_txts at d0483d08e6722404b54f3ce4aa13b885001c500b |
| `gptp/milan_dp-gptp-legs.log` | 1,379 | `f9f9fd3c21259b40` | # make -C tb/verilator/milan_dp gptp && gptp-lat at d0483d08e6722404b54f3ce4aa13b885001c500b |
| `gptp/milan_dp_gm_steps.log` | 859 | `7a876726f923870e` | # make -C tb/verilator/milan_dp_gm_steps at d0483d08e6722404b54f3ce4aa13b885001c500b |
| `gptp/milan_dp_gptp-physical.log` | 6,115 | `92d45890990981af` | # make -C tb/verilator/milan_dp_gptp (the physical leg) at d0483d08e6722404b54f3ce4aa13b885001c500b |
| `gptp/old-generator-red.log` | 4,521 | `bda18e0f87cdc94f` | # the new phases against the 1213ac5b generator |
| `gptp/probe-clamp-removed.log` | 868 | `a23309281be00669` | # disposable probe at 1a76c9de2b684be5ed3e1f9a068020937f8d7d6b: clamp-removed planted, gptp_shadow run; every FAIL line |
| `gptp/probe-floor-removed.log` | 578 | `5e647d97c1e71888` | # disposable probe at 1a76c9de2b684be5ed3e1f9a068020937f8d7d6b: floor-removed planted, gptp_shadow run; every FAIL line |
| `gptp/probe-old-80-floor.log` | 1,464 | `c3f7b7187dfbff0f` | # disposable probe at 1a76c9de2b684be5ed3e1f9a068020937f8d7d6b: old-80-floor planted, gptp_shadow run; every FAIL line |
| `gptp/tsn_fuzz.log` | 1,702 | `7f6115500704786e` | # make -C tb/verilator/tsn_fuzz at d0483d08e6722404b54f3ce4aa13b885001c500b, TSN_GEN_ROOT set; last 40 lines |
| `ledgers/egress-ledger-base.log` | 5,012 | `d5161879e5e0c1af` | # CPU-budget harness backlog-owed,srp-bound at 8x8-1if, then egress_ledger.py --point 8x8-1if and --selftest, at c34e7d8b06739a22cc79997a9a1f4cbcd9bd0 |
| `ledgers/egress-ledger-head.log` | 5,012 | `20bf576797c178d7` | # CPU-budget harness backlog-owed,srp-bound at 8x8-1if, then egress_ledger.py --point 8x8-1if and --selftest, at d0483d08e6722404b54f3ce4aa13b885001c5 |
| `ledgers/plat-ledger-base.log` | 4,984 | `cf13a101645f524d` | # plat_ledger.py at c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350: points and image digests |
| `ledgers/plat-ledger-head.log` | 4,984 | `8d5d4900389f415a` | # plat_ledger.py at d0483d08e6722404b54f3ce4aa13b885001c500b: points and image digests |
| `pin/image-inputs.txt` | 1,028 | `90aacaa5667325f0` | # the ruled pin against the routed gitlink |
| `pin/rdp.log` | 752 | `b63ce0c7e2360b1d` | # make -C tb/verilator/milan_dp gptp && make gptp-lat at a6864a49293ba3d0df37029abfa581468ef78dce (gPTP 3ce71b76) |
| `pin/rplane.log` | 2,109 | `c4b324d78cd92099` | # make -C tb/verilator/gptp_plane at a6864a49293ba3d0df37029abfa581468ef78dce (gPTP 3ce71b76) |
| `pin/rshadow.log` | 2,198 | `86de2d5f085f1deb` | # make -C tb/verilator/gptp_shadow at a6864a49293ba3d0df37029abfa581468ef78dce (gPTP 3ce71b76) |
| `routes/base-1x1-ExtraPostPlacementOpt-identity.txt` | 174 | `a6906aa35fc3b2f9` | # base identity-1x1-ExtraPostPlacementOpt: check_image_identity.py |
| `routes/base-1x1-ExtraPostPlacementOpt-signoff.txt` | 437 | `3eeb6c7090d25fbb` | # base (c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350) signoff-1x1-ExtraPostPlacementOpt: signoff corners |
| `routes/base-1x1-ExtraPostPlacementOpt-utilization.txt` | 465 | `0fffac46f6d908e8` | # base 1x1 build_ExtraPostPlacementOpt: placed utilization |
| `routes/base-8x8-ExtraPostPlacementOpt-identity.txt` | 174 | `3d1ba2d2e363ec10` | # base identity-8x8-ExtraPostPlacementOpt: check_image_identity.py |
| `routes/base-8x8-ExtraPostPlacementOpt-signoff.txt` | 399 | `a5aee3dad236ee1e` | # base (c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350) signoff-8x8-ExtraPostPlacementOpt: signoff corners |
| `routes/base-8x8-ExtraPostPlacementOpt-utilization.txt` | 469 | `b2b7c9570c03c34a` | # base 8x8 build_ExtraPostPlacementOpt: placed utilization |
| `routes/base-8x8-ExtraTimingOpt-identity.txt` | 167 | `830b70f117720564` | # base identity-8x8-ExtraTimingOpt: check_image_identity.py |
| `routes/base-8x8-ExtraTimingOpt-signoff.txt` | 466 | `5c99293ddd5e2f9f` | # base (c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350) signoff-8x8-ExtraTimingOpt: signoff corners |
| `routes/base-8x8-ExtraTimingOpt-utilization.txt` | 462 | `5e6e299f4bb63cc9` | # base 8x8 build_ExtraTimingOpt: placed utilization |
| `routes/chain.log` | 2,327 | `469fdd097f223ac0` | # route chains: head then base |
| `routes/head-1x1-ExtraPostPlacementOpt-identity.txt` | 174 | `5e5d0fc2197c6886` | # head identity-1x1-ExtraPostPlacementOpt: check_image_identity.py |
| `routes/head-1x1-ExtraPostPlacementOpt-signoff.txt` | 437 | `0eaf911915ae79b3` | # head (d0483d08e6722404b54f3ce4aa13b885001c500b) signoff-1x1-ExtraPostPlacementOpt: signoff corners |
| `routes/head-1x1-ExtraPostPlacementOpt-utilization.txt` | 497 | `5ee5e0de37fe3ecb` | # head 1x1 build_ExtraPostPlacementOpt: placed utilization |
| `routes/head-8x8-AltSpreadLogic_high-identity.txt` | 172 | `24bc92ae5fe982ad` | # head identity-8x8-AltSpreadLogic_high: check_image_identity.py |
| `routes/head-8x8-AltSpreadLogic_high-signoff.txt` | 471 | `4e087d2d70ec285d` | # head (d0483d08e6722404b54f3ce4aa13b885001c500b) signoff-8x8-AltSpreadLogic_high: signoff corners |
| `routes/head-8x8-AltSpreadLogic_high-utilization.txt` | 497 | `7b31415f4c8a9177` | # head 8x8 build_AltSpreadLogic_high: placed utilization |
| `routes/head-8x8-ExtraPostPlacementOpt-identity.txt` | 174 | `0195d9e4e3f45b9c` | # head identity-8x8-ExtraPostPlacementOpt: check_image_identity.py |
| `routes/head-8x8-ExtraPostPlacementOpt-signoff.txt` | 399 | `e4968823cb473b7b` | # head (d0483d08e6722404b54f3ce4aa13b885001c500b) signoff-8x8-ExtraPostPlacementOpt: signoff corners |
| `routes/head-8x8-ExtraPostPlacementOpt-utilization.txt` | 501 | `195af992b167746d` | # head 8x8 build_ExtraPostPlacementOpt: placed utilization |
| `routes/head-8x8-ExtraTimingOpt-identity.txt` | 167 | `542a7c21d6476d2b` | # head identity-8x8-ExtraTimingOpt: check_image_identity.py |
| `routes/head-8x8-ExtraTimingOpt-signoff.txt` | 466 | `0f17f3591e4f82c4` | # head (d0483d08e6722404b54f3ce4aa13b885001c500b) signoff-8x8-ExtraTimingOpt: signoff corners |
| `routes/head-8x8-ExtraTimingOpt-utilization.txt` | 487 | `94167dd43dffc780` | # head 8x8 build_ExtraTimingOpt: placed utilization |
| `routes/oom-first-attempt.txt` | 531 | `a9417c3c88ad6c39` | # the first chains at 9b40757e, ended at 21:10 by the unit's 12 GB memory cap (oom-kill); not used |
| `tools/boot.sh.txt` | 478 | `f9d310a4034e8e37` | # route tool boot.sh |
| `tools/chain.sh.txt` | 2,446 | `bcc5c7eb2bc6c38f` | # route tool chain.sh |
| `tools/chain_base.sh.txt` | 2,457 | `d42b7c82db7d7b0e` | # route tool chain_base.sh |
| `tools/docs_steps.py.txt` | 7,457 | `f7050addd31431a8` | # lane tool docs_steps.py |
| `tools/eg.sh.txt` | 748 | `254948f8fbbb4466` | # lane tool eg.sh |
| `tools/fwgate.sh.txt` | 577 | `07628d1a3fe8b0de` | # lane tool fwgate.sh |
| `tools/gbuild.sh.txt` | 1,982 | `af2b92741b74a46b` | # route tool gbuild.sh |
| `tools/gprep.sh.txt` | 2,326 | `8ecdb018ae8409a5` | # route tool gprep.sh |
| `tools/ledger.sh.txt` | 459 | `ff858eb08bd05d22` | # lane tool ledger.sh |
| `tools/mkclone.sh.txt` | 757 | `7a5de903c0b9c7d9` | # lane tool mkclone.sh |
| `tools/oldred.sh.txt` | 651 | `1aab78f84dd8968b` | # lane tool oldred.sh |
| `tools/one.sh.txt` | 1,282 | `f5bd01ad3331e074` | # route tool one.sh |
| `tools/package.py.txt` | 8,380 | `073a118824bf7d20` | # lane tool package.py |
| `tools/probe.py.txt` | 1,580 | `e3d2c6bd4f2bce9f` | # lane tool probe.py |
| `tools/probes.sh.txt` | 278 | `49d5e906ec603dbf` | # lane tool probes.sh |
| `tools/signoff.py.txt` | 1,348 | `98f611541f57a087` | # route tool signoff.py |
| `tools/u.sh.txt` | 523 | `4c6f70809da71785` | # lane tool u.sh |
| `tools/util.py.txt` | 2,137 | `6d03347e078baae2` | # route tool util.py |
| `tools/w.sh.txt` | 329 | `41638927511004ff` | # lane tool w.sh |
