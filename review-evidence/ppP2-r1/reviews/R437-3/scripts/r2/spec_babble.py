# Broken-backend probe (not a contract freedom): after a deadline abandons a
# payload READ, the device keeps presenting bytes past the READ's length for
# ever. A restore issued meanwhile waits in S_RHREQ; every drained byte is
# progress, so the deadline never ends it.
PROBES = {"BABBLE": [("SIM", "  a_short_command_is_a_device_error();\n  every_operation_got_what_it_was_owed();",
    "  a_short_command_is_a_device_error();\n  {\n"
    "    fresh_reset();\n    h.deadline_ok = true;\n"
    "    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x26));\n"
    "    CHECK(h.commit(2, rec) == 0, \"BABBLE setup\");\n"
    "    int rc = silenced(false, rec, SIL_BYTE, 1, -1, 10);\n"
    "    h.sil_block = false; h.d_cur.len = 1 << 30; h.rstall = TMO / 2;   // the abandoned READ now never ends\n"
    "    const int w0 = h.wedges;\n"
    "    rc = h.restore(2);\n"
    "    CHECK(rc != -1, \"BABBLE a restore behind an owed READ that streams past its length for ever \"\n"
    "          \"is answered within run_op's guard (rc %d, %d drained, wedged %d)\", rc, h.dev_rd, h.wedges - w0);\n"
    "    printf(\"BABBLE-INFO rc=%d cause=%d drained=%d d_busy=%d d_st=%d ops=%zu\\n\", rc, h.last_cause, h.dev_rd, int(h.d_busy), h.d_st, h.ops.size());\n"
    "    h.wedges = w0; h.rstall = 0;\n    h.quiesce_model();\n    fresh_reset();\n    h.deadline_ok = false;\n"
    "  }\n  every_operation_got_what_it_was_owed();")]}
RUNS = [("BABBLE", "pristine", 100)]
