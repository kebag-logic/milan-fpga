"""Reviewer-planted mutants for FPGA-gPTP PR #92 at d27a1654.

Same 5-tuple shape as tb/verilator/engine/mutants.py MUTATIONS:
(name, file under hdl/, exact pattern, replacement, breaks). `breaks` is
"" so the verdict is the plain suite verdict (any failing check, or a
non-zero exit, counts as caught). Each probe asks whether the suite
notices one specific behaviour of the delta that no author control names.
"""
GENERATOR = "ucode/gen_gptp_ucode.py"

REVIEWER_MUTATIONS = [
    # #89: the asCapable rise no longer clears the aged mark. The delta's
    # only defence against a mark carried over a warm reset or a capability
    # lapse (docs/INTEGRATION.md: "An asCapable rise also clears that aged
    # state")
    ("R1 an asCapable rise keeps the aged mark", GENERATOR,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_SRTO, fmt=FMT_Q)\n"
     "    p.emit(\"BR\", label=\"done\")\n",
     "    p.emit(\"BR\", label=\"done\")\n",
     ""),
    # #89: a usable pair does not clear the aged mark
    ("R2 a usable pair keeps the aged mark", GENERATOR,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_SRTO, fmt=FMT_Q)     # not aged\n",
     "",
     ""),
    # #89: the timeout ages the port but records no mark (oscillation)
    ("R3 the timeout records no aged mark", GENERATOR,
     "    p.emit(\"WRST\", ra=RT, imm=RG_SCR | S_SRTO, fmt=FMT_Q)\n"
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=ROLE_SLAVE_C)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=LB[\"BECOME\"])\n",
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=ROLE_SLAVE_C)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=LB[\"BECOME\"])\n",
     ""),
    # #90: a completed exchange no longer restarts the loss count
    # (non-consecutive losses accumulate)
    ("R4 a completed exchange keeps the loss count", GENERATOR,
     "    p.emit(\"ALU\", rd=RC, ra=RC, rb=RB, cnd=ALU_AND)\n",
     "    p.emit(\"ALU\", rd=RC, ra=RC, rb=0, cnd=ALU_OR, imm=0)\n",
     ""),
    # #90: the init leg does not mark its own first request answered, so
    # boot judges a request that was never sent (expected benign)
    ("R5 init leaves the first request unjudged-guard off", GENERATOR,
     "    p.emit(\"WRST\", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n"
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=3000)\n",
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=3000)\n",
     ""),
    # #91: only a second response from the SAME responder resets; another
    # responder re-arms the pairing as before (doc claim "from either
    # responder")
    ("R6 only a same-source second response resets", GENERATOR,
     "    p.emit(\"RDST\", rd=RU, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)\n"
     "    p.emit(\"ALU\", rd=RT, ra=RT, rb=RU, cnd=ALU_ADD)\n",
     "    p.emit(\"RDST\", rd=RU, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)\n"
     "    p.emit(\"RDST\", rd=RV, imm=RG_SCR | S_RSPSRC, fmt=FMT_Q)\n"
     "    p.emit(\"CMP\", ra=RV, rb=RC, fmt=FMT_Q)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"r6_same\")\n"
     "    p.emit(\"MOVE\", rd=RU, ra=0, imm=0)\n"
     "    p.label(\"r6_same\")\n"
     "    p.emit(\"ALU\", rd=RT, ra=RT, rb=RU, cnd=ALU_ADD)\n",
     ""),
    # #89: the aged-mark Announce gate compares against the master value
    # (the mark is never honoured for a slave-found timeout)
    ("R7 the Announce gate tests the wrong role", GENERATOR,
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=ROLE_SLAVE_C)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"out\")\n",
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=ROLE_MASTER_C)\n"
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"out\")\n",
     ""),
    # #89: the master's pair does not restart the watch (only clears)
    # -- SRWATCH skipped for the slave; the slave's SVRATE tail ends early
    ("R8 a slave pair does not restart the watch", GENERATOR,
     "    p.emit(\"COMMIT\")\n"
     "    p.emit(\"BR\", label=LB[\"SRWATCH\"])\n",
     "    p.emit(\"COMMIT\")\n"
     "    p.emit(\"END\")\n",
     ""),
    # #90: the clearing beat leaves S_PDOK standing, so recovery after a
    # fifth loss needs fewer than two good exchanges (Milan 4.2.6.2.4)
    ("R9 the fifth loss keeps the recovery ladder", GENERATOR,
     "    p.emit(\"BRS\", cnd=BRS_LT, label=\"pd_go\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n",
     "    p.emit(\"BRS\", cnd=BRS_LT, label=\"pd_go\")\n",
     ""),
]
