"""Write the per-finding intermediate states of the engine and generator.

usage: make_states.py <lane> <out dir>
<out>/final/ holds the lane's working-tree versions; <out>/A and <out>/B
hold the engine and generator after the first and second fix commits. Each
step is a set of exact replacements, applied to the final text, that must
each match once.
"""
import shutil
import sys
from pathlib import Path

lane, out = Path(sys.argv[1]), Path(sys.argv[2])
ENG = "hdl/top/KL_gptp_engine.sv"
GEN = "hdl/ucode/gen_gptp_ucode.py"
for f in (ENG, GEN):
    (out / "final" / f).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(lane / f, out / "final" / f)


def undo(text, pairs):
    for final, earlier in pairs:
        assert text.count(final) == 1, final
        text = text.replace(final, earlier)
    return text


# ---- the third fix (R730-F3 = R729-F1): the reference sample -------------
ENG_C = [
    ("""    //! low the port is NOT_ENABLED (Figure 11-8): it starts no frame, owes
    //! no egress stamp and completes no Pdelay exchange. Each change after
    //! the first sample since reset clears asCapable and the Milan v1.2
    //! 4.2.6.2.5 cease; a rise also sends a Pdelay_Req at once (#94).
""", """    //! low the port is NOT_ENABLED (Figure 11-8): it starts no frame, owes
    //! no egress stamp and completes no Pdelay exchange. Each change after
    //! the first enable since reset clears asCapable and the Milan v1.2
    //! 4.2.6.2.5 cease; a rise also sends a Pdelay_Req at once (#94).
"""),
    ("""  //! before its first byte. port_ref_r marks the first sample since reset
  //! as the reference level, so only a later change is an edge: a port
  //! enabled at release raises nothing, the boot cadence serving it, and a
  //! port disabled at release raises both events at its rise (Figure 11-8:
  //! BEGIN enters NOT_ENABLED whatever scratch retained). Each edge owes a
  //! slot-6 timer event, the microcode's NOT_ENABLED leg, which dispatches
  //! ahead of every other event; a rise then owes the queue a slot-0 one,
  //! the request beat (INITIAL_SEND_PDELAY_REQ).
  localparam logic [2:0] PE_SLOT_C = 3'd6;
  logic port_en_r, port_ref_r;
""", """  //! before its first byte. port_seen_r marks the first enable since
  //! reset, which the boot cadence already serves, so only later edges
  //! raise events. Each edge owes a slot-6 timer event, the microcode's
  //! NOT_ENABLED leg, which dispatches ahead of every other event; a rise
  //! then owes the queue a slot-0 one, the request beat
  //! (INITIAL_SEND_PDELAY_REQ).
  localparam logic [2:0] PE_SLOT_C = 3'd6;
  logic port_en_r, port_seen_r;
"""),
    ("""  //! #94: the portEnabled level and the events its edges owe. The first
  //! sample after release is the reference, whatever its level. A later
  //! edge re-raises NOT_ENABLED; a fall withdraws an owed beat.
""", """  //! #94: the portEnabled level and the events its edges owe.
  //! A later edge re-raises NOT_ENABLED; a fall withdraws an owed beat.
"""),
    ("      port_ref_r  <= 1'b0;\n", "      port_seen_r <= 1'b0;\n"),
    ("      port_ref_r  <= 1'b1;\n", "      port_seen_r <= port_seen_r || port_en_r;\n"),
    ("      if (port_ref_r && (port_enabled_i != port_en_r)) begin\n",
     "      if (port_seen_r && (port_enabled_i != port_en_r)) begin\n"),
]
GEN_C = [
    ("""    well as on its 5-minute countdown. Each portEnabled change after the
    first sample since reset raises timer slot 6 (NOTEN), so a port that
    is disabled at a warm reset's release ends a retained cease at its
    rise. NOTEN clears the cease, its countdown and streak, the asCapable
    ladder and asCapable, and commits: Figure 11-8 (Cor1, Cor2) leaves
    NOT_ENABLED only through INITIAL_SEND_PDELAY_REQ, with lostResponses =
    0 and asCapable = FALSE. It also disarms the outstanding exchange, so
    no Follow_Up heard while the port is disabled pairs or publishes.
""", """    well as on its 5-minute countdown. Each portEnabled edge after the
    first enable since reset raises timer slot 6 (NOTEN). It clears the
    cease, its countdown and streak, the asCapable ladder and asCapable,
    and commits: Figure 11-8 (Cor1, Cor2) leaves NOT_ENABLED only through
    INITIAL_SEND_PDELAY_REQ, with lostResponses = 0 and asCapable = FALSE.
    It also disarms the outstanding exchange, so no Follow_Up heard while
    the port is disabled pairs or publishes.
"""),
]
# ---- the second fix (R730-F2 = R729-F2): NOT_ENABLED disarms -------------
ENG_B = [
    ("""    //! low the port is NOT_ENABLED (Figure 11-8): it starts no frame, owes
    //! no egress stamp and completes no Pdelay exchange. Each change after
    //! the first enable since reset clears asCapable and the Milan v1.2
    //! 4.2.6.2.5 cease; a rise also sends a Pdelay_Req at once (#94).
""", """    //! low the port is NOT_ENABLED (Figure 11-8): it starts no frame and
    //! owes no egress stamp. Each change after the first enable since
    //! reset clears asCapable and the Milan v1.2 4.2.6.2.5 cease; a rise
    //! also sends a Pdelay_Req at once (#94).
"""),
]
GEN_B = [
    ("""    INITIAL_SEND_PDELAY_REQ, with lostResponses = 0 and asCapable = FALSE.
    It also disarms the outstanding exchange, so no Follow_Up heard while
    the port is disabled pairs or publishes.
""", """    INITIAL_SEND_PDELAY_REQ, with lostResponses = 0 and asCapable = FALSE.
"""),
    ("""    same flags; NOTEN's disarm adds one word.""",
     """    same flags, so the ROM keeps its size."""),
    ("""    NOT_ENABLED takes no Pdelay_Resp_Follow_Up, so both edges also disarm
    the outstanding exchange: S_RSPSEQ zero refuses its Follow_Up in
    PDPOST, and S_PDGOT set refuses a later response's arm until the next
    request. A pair already frozen for its t1 cannot complete either: the
    stamp finds no claim while the port is disabled (KL_gptp_engine.sv),
    and the next request cancels the pair.

""", ""),
    ("    for s in (S_CEASE, S_CEASECNT, S_MULTI, S_RSPSEQ):\n",
     "    for s in (S_CEASE, S_CEASECNT, S_MULTI):\n"),
]

eng_c = (out / "final" / ENG).read_text()
gen_c = (out / "final" / GEN).read_text()
eng_b = undo(eng_c, ENG_C)
gen_b = undo(gen_c, GEN_C)
eng_a = undo(eng_b, ENG_B)
gen_a = undo(gen_b, GEN_B)
for tag, eng, gen in (("A", eng_a, gen_a), ("B", eng_b, gen_b)):
    for f, text in ((ENG, eng), (GEN, gen)):
        p = out / tag / f
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
print("states written")
