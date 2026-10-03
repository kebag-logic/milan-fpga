tb/nvm_port/README.md:100-101 citations vs the cited lines
`:90-92`; the D3 writer gates its records the same way (`frame_ok_w`,
`hdl/aecp/KL_aecp_nvm_writer.sv:482-485`). The shadow is
instantiated at `hdl/top/protocol_processor_top.sv:2714` and pinned by
ddb3119d frame_ok_w lines: 482-485; KL_acmp_nvm_shadow instance line: 2727
f4167536 frame_ok_w lines: 482-485; KL_acmp_nvm_shadow instance line: 2725
c066dd83 frame_ok_w lines: 546-549; KL_acmp_nvm_shadow instance line: 2729
5960d8fc frame_ok_w lines: 549-552; KL_acmp_nvm_shadow instance line: 2730
PR body 'Seen, not fixed' note:
395:**Seen, not fixed in this round.** Two citations at `tb/nvm_port/README.md:100-101`
396-point at the wrong lines: `KL_aecp_nvm_writer.sv:482-485` (`frame_ok_w`, right at
397-`ddb3119d`, at `:550-553` since the name stage) and `protocol_processor_top.sv:2714`
398-(the binding shadow's instance, already at `:2727` on `main`, `:2730` at the head).
frame_ok_w declaration line through the PR: ddb3119d:482 a1f5cd5:546 53e1474:546 c066dd83:546 219cd67:549 5960d8fc:549 
=> the decl+assign span cited as 482-485 at ddb3119d is 546-549 from a1f5cd5 (the name stage) to c066dd83, and 549-552 at the head; no commit puts it at 550-553.
