module automatic
  KL_t_auto (input wire clk_i);
endmodule
module /* c */ KL_t_cmt (input wire clk_i);
endmodule
module // line comment
  KL_t_cmt2 (input wire clk_i);
endmodule
macromodule KL_t_macro (input wire clk_i);
endmodule
module static KL_t_static (input wire clk_i);
endmodule
interface r449_if; logic a; endinterface
module KL_t_ifport (r449_if i);
endmodule
module KL_t_typ #(parameter type T = logic) (input T x);
endmodule
`ifdef R449_NEVER
module KL_t_ifdef (input wire clk_i);
endmodule
`endif
(* blackbox *) module KL_t_attr2 (input wire clk_i);
endmodule
module KL_t_dollar$x (input wire clk_i);
endmodule
module \KL_t_esc+ (input wire clk_i);
endmodule
