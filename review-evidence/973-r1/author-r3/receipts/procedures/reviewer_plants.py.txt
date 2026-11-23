# Reviewer-owned planted defects for #973 (independent of the author's srp_link_mutants.py), in srp_mutants.Defect
# form: name, the named test that must fail, the exact source line replaced, its replacement, the needle the failing
# test's diagnostic must contain, and the suite holding the test.
POLL = "        links[n] = mbx_link_up(n) && m->ifs[n].link_carried;\n"
RESET_IN_SINK = "        if (i->link_seen || !event->link_up) {\n            reset_interface(i);\n"
POLL_RESET = "        if (i->link != link) {\n            reset_interface(i);\n"


def defects(kind):
    return (
        # R1: the carried level ORed with the register: a DOWN the register reads while its record is held no longer
        # fails closed (802.1Q 10.7: a port that is not operational declares nothing)
        kind("rv-poll-or-instead-of-and", "Srp.LinkLevelLossAndFirstDownEventAreFailClosed", POLL,
             "        links[n] = mbx_link_up(n) || m->ifs[n].link_carried;\n", "adapter.ifs[0].active[0]"),
        # R2: the poll also writes the carried level when it resets on a register DOWN: a DOWN whose record is elided
        # (the level back up before posting, KL_mbx_evt posted_up_r) can then never recover from the register
        kind("rv-poll-clears-carried", "Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive", POLL_RESET,
             POLL_RESET + "            i->link_carried = link;\n", "level recovery resumes declarations"),
        # R3: a repeated UP (or a DOWN) that resets the interface twice in the sink
        kind("rv-sink-double-reset", "SrpLinkPass.InTheEvents", RESET_IN_SINK,
             RESET_IN_SINK + "            reset_interface(i);\n", "resets the interface once",
             suite="srp_link_pass.cpp"),
        # R4: the poll takes the register's UP only while a carried UP exists, but resets the interface on any
        # register UP edge regardless (the original defect reached by another site): the poll's reset ignores link
        kind("rv-poll-resets-on-register-up", "SrpLinkPass.AfterTheEventsBeforeSrpsPoll", POLL_RESET,
             "        if (i->link != link || (mbx_link_up(n) && !i->link)) {\n            reset_interface(i);\n",
             "SRP's poll reset the interface on a level no LINK had carried", suite="srp_link_pass.cpp"),
    )
