[A582] STOP
Head: 7c1b52bee26b497080ee22b1c1986109f80a5ee7
Branch: 665-int-split. No repository edits or commits; worktree clean.

The equal-wire acceptance conflicts with preserving the assigned default image. The pinned fabric UNBIND_RX_RESPONSE echoes nonzero talker_entity_id and talker_unique_id (`protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:672`). F3 zeroes them under Milan v1.2 Table 5.36 (`sw/firmware/ctrl/acmp/acmp.c:825`). The existing differential explicitly normalizes LD1 before comparing bytes (`sw/firmware/ctrl/test/acmp_walk.cpp:433`). This is already assigned to processor #168 under #665 comment 6030067436.

Reproduction: the unchanged F3 walk passes 127 tests. Removing only LD1 normalization in a scratch copy yields eight named byte-comparison failures, one per listener state. A scratch echo mutation passes all eight raw comparisons and fails all eight maintained conformance checks. The unchanged pinned listener RTL suite passes 3,111 checks. Both diagnostic drivers return 0 for these exact expected outcomes; no datapath-level equivalence pass is claimed.

Correcting the fabric here would change default shipping behavior and inputs, triggering assignment 6087047553's STOP. Making F3 echo the fields would violate its accepted clause behavior. I have not silently treated normalized comparisons as equal wire behavior. Please record whether F-INT carries the documented F3 differences explicitly, or provide a corrected adopted base with matching differentials before strict equality is required.

HANDOFF.md and PR-BODY.md, reproducible diagnostics, the test-to-defect table, coverage/gate tables, and artifact size/hash receipts are prepared in the assigned output directory. No selected image, two-placement simulation, linked-size result, resource route, timing result or full acceptance-gate pass is claimed. No default, register map, pin or generated source changed. Independent review remains pending. No push, PR operation, hardware operation or resource re-record was performed.
