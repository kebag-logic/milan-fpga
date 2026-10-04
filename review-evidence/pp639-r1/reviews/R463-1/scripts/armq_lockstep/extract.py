#!/usr/bin/env python3
"""Cut the timer arm-port mux block out of a protocol_processor_top.sv, byte for byte,
and wrap it as a standalone module whose ports are the eight engine arm faces, the arm
port and the drop counter.

Usage: extract.py TOP_SV MODULE_NAME OUT_SV [--mutate NAME]

The block runs from the '// ====' line above 'timer arm-port priority mux (banner)' to
the line before the '// ====' line above 'PRNG draw-port owner mux (banner)'.
--mutate plants one named control into the cut block (the candidate's ring only).
"""
import hashlib
import sys

FACES = ["lstn", "tkr", "adp", "srp", "org", "maapeng", "ntfy", "ntfy_mon"]

# controls: (needle, replacement); each needle must occur exactly once in the block
MUTANTS = {
    # the issue's six lockstep controls, re-derived here
    "wr_at_head": ("assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];",
                   "assign wr_ix_w = armq_hd_r[g];"),
    "wr_at_mid": ("assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];",
                  "assign wr_ix_w = armq_hd_r[g] + armq_mid_w[g][1:0];"),
    "head_stuck": ("armq_hd_r[i]         <= armq_hd_r[i] + 2'd1;",
                   "armq_hd_r[i]         <= armq_hd_r[i];"),
    "read_tail": ("assign armq_hd_w[g] = mem_r[armq_hd_r[g]];",
                  "assign armq_hd_w[g] = mem_r[wr_ix_w];"),
    "write_refused": ("if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];",
                      "if (armq_in_vld_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];"),
    "ring_of_three": ("armq_hd_r[i]         <= armq_hd_r[i] + 2'd1;",
                      "armq_hd_r[i]         <= (armq_hd_r[i] == 2'd2) ? 2'd0 : armq_hd_r[i] + 2'd1;"),
    # reviewer's own: the same-cycle read/write of one entry (full queue, pop and push)
    # read write-first, i.e. the leaving head returns the arm written over it
    "read_write_first": ("assign armq_hd_w[g] = mem_r[armq_hd_r[g]];",
                         "assign armq_hd_w[g] = (armq_push_ok_w[g] && (wr_ix_w == armq_hd_r[g]))"
                         " ? armq_in_w[g] : mem_r[armq_hd_r[g]];"),
    # reviewer's own: a full queue that pops refuses the push (depth 3 while draining)
    "full_pop_refuses": ("armq_push_ok_w[i] = armq_in_vld_w[i] && (armq_mid_w[i] != 3'd4);",
                         "armq_push_ok_w[i] = armq_in_vld_w[i] && (armq_cnt_r[i] != 3'd4);"),
    # reviewer's own: the drop counter not saturating (wraps at 0xFFFF)
    "drop_wraps": ("if (arm_drop_r != 16'hFFFF) arm_drop_r <= arm_drop_r + 16'd1;",
                   "arm_drop_r <= arm_drop_r + 16'd1;"),
    # reviewer's own probe (expected equivalent): the head index not reset
    "probe_head_unreset": ("      armq_hd_r  <= '0;\n", ""),
}


def cut(text: str) -> str:
    lines = text.splitlines(keepends=True)
    a = next(i for i, l in enumerate(lines) if "timer arm-port priority mux (banner)" in l)
    b = next(i for i, l in enumerate(lines) if "PRNG draw-port owner mux (banner)" in l)
    assert lines[a - 1].lstrip().startswith("// ====") and lines[b - 1].lstrip().startswith("// ====")
    return "".join(lines[a - 1:b - 1])


def main() -> int:
    top, name, out = sys.argv[1:4]
    mut = sys.argv[5] if len(sys.argv) > 5 and sys.argv[4] == "--mutate" else None
    block = cut(open(top, encoding="utf-8").read())
    sys.stderr.write(f"{name}: block sha256 {hashlib.sha256(block.encode()).hexdigest()} "
                     f"({block.count(chr(10))} lines)\n")
    if mut:
        needle, repl = MUTANTS[mut]
        assert block.count(needle) == 1, (mut, block.count(needle))
        block = block.replace(needle, repl)
    ports = ["    input  wire clk_i,", "    input  wire rst_n,"]
    for f in FACES:
        ports += [f"    input  wire              in_{f}_valid,",
                  f"    input  wire              in_{f}_cancel,",
                  f"    input  wire [AW-1:0]     in_{f}_slot,",
                  f"    input  wire [7:0]        in_{f}_owner,",
                  f"    input  wire [31:0]       in_{f}_deadline,"]
    ports += ["    output logic             o_valid,",
              "    output logic             o_cancel,",
              "    output logic [AW-1:0]    o_slot,",
              "    output logic [7:0]       o_owner,",
              "    output logic [31:0]      o_deadline,",
              "    output logic [15:0]      o_drop"]
    decl = ["  localparam int unsigned TMR_AW_C = AW;",
            "  localparam int unsigned PP_TIMER_OWNER_W_C = 8;",
            "  logic        tmr_arm_valid_w, tmr_arm_cancel_w;",
            "  logic [TMR_AW_C-1:0] tmr_arm_slot_w;",
            "  logic [PP_TIMER_OWNER_W_C-1:0] tmr_arm_owner_w;",
            "  logic [31:0] tmr_arm_deadline_w;"]
    for f in FACES:
        if f.startswith("ntfy"):
            continue  # the block declares the two notify faces itself
        decl += [f"  logic {f}_arm_valid_w, {f}_arm_cancel_w;",
                 f"  logic [TMR_AW_C-1:0] {f}_arm_slot_w;",
                 f"  logic [7:0] {f}_arm_owner_w;",
                 f"  logic [31:0] {f}_arm_deadline_w;"]
    tail = []
    for f in FACES:
        for s in ("valid", "cancel", "slot", "owner", "deadline"):
            tail.append(f"  assign {f}_arm_{s}_w = in_{f}_{s};")
    tail += ["  assign o_valid = tmr_arm_valid_w;", "  assign o_cancel = tmr_arm_cancel_w;",
             "  assign o_slot = tmr_arm_slot_w;", "  assign o_owner = tmr_arm_owner_w;",
             "  assign o_deadline = tmr_arm_deadline_w;", "  assign o_drop = arm_drop_r;"]
    sv = (f"// generated by extract.py from {top}\n"
          f"module {name} #(parameter int unsigned AW = 6) (\n" + "\n".join(ports) + "\n);\n"
          + "\n".join(decl) + "\n" + block + "\n".join(tail) + "\nendmodule\n")
    open(out, "w", encoding="utf-8").write(sv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
