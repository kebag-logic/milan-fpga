"""R720-1's R3 probe, adapted to the round-2 sync receipt timeout leg: the
timeout ages the port but records no aged mark. Same 5-tuple shape and the
same empty `breaks` (plain suite verdict) as reviewer_probes.py."""
GENERATOR = "ucode/gen_gptp_ucode.py"

REVIEWER_MUTATIONS = [
    ("R3' the timeout records no aged mark", GENERATOR,
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=SRTO_PASSED_C)\n"
     "    p.emit(\"WRST\", ra=RT, imm=RG_SCR | S_SRTO, fmt=FMT_Q)\n",
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=SRTO_PASSED_C)\n",
     ""),
]
