#!/usr/bin/env python3
"""Shadow lockstep for KL_pp_acmp_listener.

usage: gen_shadow.py REF_SV DUT_SV OUT_DIR [--mutant NAME]
Writes OUT_DIR/KL_pp_acmp_listener.sv, a module with the listener's own name,
parameters and ports that holds main's listener (renamed _ref) and the head's
(renamed _dut) side by side on the same inputs.  The DUT drives the outputs; at
every rising edge every output of the two, and the working record rec_r, the
walk state xs_r and the record read bus rec_rd_w, are compared.  A final block
prints `LOCKSTEP: <edges> edges, <n> mismatching edges (first at edge E: names),
<latch> X_LATCH and <ap> X_STRT_AP record reads`.  Any suite that builds the
listener by this file name runs both in lockstep under its own stimulus.
"""
import re
import sys

MUTANTS = {
    # the read sampled in X_IDLE: the stale read the author's bench also plants
    "read_in_idle": (
        "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[sink_r]);\n",
        "  logic [ACMP_REC_W_C-1:0] rec_idle_r;\n"
        "  always_ff @(posedge clk_i) if (xs_r == X_IDLE) rec_idle_r <= rec_ram_r[sink_r];\n"
        "  assign rec_rd_w     = acmp_rec_t'(rec_idle_r);\n"),
    # the read register restored but read one state late (a lost issue cycle)
    "read_write_first": (
        "  assign rec_rd_w     = acmp_rec_t'(rec_ram_r[sink_r]);\n",
        "  assign rec_rd_w     = acmp_rec_t'((recwr_en_w && recwr_addr_w == sink_r) ? recwr_data_w : rec_ram_r[sink_r]);\n"),
}


def header(text: str) -> str:
    m = re.search(r"^module KL_pp_acmp_listener\b.*?^\);\n", text, re.S | re.M)
    return m.group(0)


def ports(head: str) -> list[tuple[str, str]]:
    out = []
    for line in head.splitlines():
        code = line.split("//")[0].rstrip()
        m = re.match(r"\s*(input|output)\b.*?\b(\w+)\s*,?\s*$", code)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def main() -> None:
    ref_sv, dut_sv, out = sys.argv[1:4]
    mutant = sys.argv[5] if len(sys.argv) > 5 and sys.argv[4] == "--mutant" else None
    ref = open(ref_sv).read()
    dut = open(dut_sv).read()
    assert header(ref) == header(dut), "port headers differ"
    if mutant:
        old, new = MUTANTS[mutant]
        assert dut.count(old) == 1
        dut = dut.replace(old, new, 1)
    hdr = header(dut)
    xl = re.search(r"X_LATCH\s*=\s*(5'd\d+)", dut).group(1)
    xa = re.search(r"X_STRT_AP\s*=\s*(5'd\d+)", dut).group(1)
    plist = ports(hdr)
    params = re.findall(r"parameter\s+\w+(?:\s+\w+)?\s+(\w+)\s*=", hdr)
    def rename(text: str, new: str) -> str:
        text = re.sub(r"^module KL_pp_acmp_listener\b", f"module {new}", text, count=1, flags=re.M)
        return re.sub(r"endmodule\s*:\s*KL_pp_acmp_listener\b", f"endmodule : {new}", text)
    open(f"{out}/lsn_ref.sv", "w").write(rename(ref, "KL_pp_acmp_listener_ref"))
    open(f"{out}/lsn_dut.sv", "w").write(rename(dut, "KL_pp_acmp_listener_dut"))
    pmap = ", ".join(f".{p}({p})" for p in params)
    outs = [n for d, n in plist if d == "output"]
    decl = []
    # the reference's outputs: same types, from the header's own declaration lines
    for line in hdr.splitlines():
        code = line.split("//")[0].rstrip()
        m = re.match(r"(\s*)output\s+(logic\s*.*?)\b(\w+)\s*,?\s*$", code)
        if m:
            decl.append(f"  {m.group(2)} r_{m.group(3)};")
    conn_ref = ", ".join(f".{n}(r_{n})" if d == "output" else f".{n}({n})" for d, n in plist)
    conn_dut = ", ".join(f".{n}({n})" for d, n in plist)
    cmp_terms = " ||\n        ".join(f"({n} !== r_{n})" for n in outs)
    names = "\n".join(f'      if ({n} !== r_{n}) $write(" {n}");' for n in outs)
    body = hdr + f"""
{chr(10).join(decl)}
  KL_pp_acmp_listener_ref #({pmap}) u_ref ({conn_ref});
  KL_pp_acmp_listener_dut #({pmap}) u_dut ({conn_dut});

  // the walk state, for benches that observe it through the listener's own name
  logic [4:0] xs_r;
  assign xs_r = 5'(u_dut.xs_r);

  longint unsigned ls_edges = 0, ls_bad = 0, ls_first = 0, ls_latch = 0, ls_ap = 0, ls_rst = 0;
  logic ls_int_bad;
  assign ls_int_bad = (u_ref.rec_r !== u_dut.rec_r) || (u_ref.xs_r !== u_dut.xs_r)
                   || (((u_dut.xs_r == {xl}) || (u_dut.xs_r == {xa}))
                       && (u_ref.rec_rd_w !== u_dut.rec_rd_w));
  always @(posedge clk_i) begin
    ls_edges <= ls_edges + 1;
    if (!rst_n) ls_rst <= ls_rst + 1;
    if (u_dut.xs_r == {xl}) ls_latch <= ls_latch + 1;
    if (u_dut.xs_r == {xa}) ls_ap <= ls_ap + 1;
    if (ls_int_bad ||
        {cmp_terms}) begin
      if (ls_bad == 0) begin
        ls_first <= ls_edges;
        $write("LOCKSTEP FIRST MISMATCH at edge %0d:", ls_edges);
{names}
        if (ls_int_bad) $write(" (internal rec_r/xs_r/rec_rd_w)");
        $write("\\n");
      end
      ls_bad <= ls_bad + 1;
    end
  end
  final $display("LOCKSTEP: %0d edges, %0d mismatching edges (first at edge %0d), %0d X_LATCH and %0d X_STRT_AP record reads, %0d reset edges",
                 ls_edges, ls_bad, ls_first, ls_latch, ls_ap, ls_rst);
endmodule
"""
    open(f"{out}/KL_pp_acmp_listener.sv", "w").write(body)


if __name__ == "__main__":
    main()
