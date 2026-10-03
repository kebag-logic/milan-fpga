Independent pass, written before reading the R448-1 or R449-1 findings (exact head cd08ca7b3d962ab040d8aaa023c57e7b0e010a6d).

Draft verdict: NEGATIVE (one open MINOR).

N1 MINOR Conformance, Robustness, Tests, Docs: syn/yosys/run.sh:166-169 (census) and :245 (parse_site)
  The census reads `^module[[:space:]]+...` from sv2v's all.v. sv2v keeps a module's attribute instance on the
  header line (`(* keep_hierarchy = "yes" *) module NAME`), so an attributed module is not counted: planted with a
  fault, on the same line or its own line, the gate is rc 0 (receipts/census/c-attr-same, c-attr-own). Round 1's
  .sv-text census caught the own-line form (r1-attr-own rc 1). Listed in tops, a clean attributed module is refused
  as "no longer exist under hdl/" (c-attr-own-top-clean rc 1), so such a module can be neither omitted nor added.
  An `ifdef`-guarded module is also no longer counted (c-ifdef rc 0, r1-ifdef rc 1). parse_site names
  `automatic` for `module automatic X` and the previous module for an attributed one (census_unit).
  run.sh:163-164's and the PR body's "however its source lays the header out" is not true for attributes.

Lens draft: RTL CLEAN (KL_pp_nvm_port.sv:111-113,192-200 bound derived; netlists identical r1/base vs head at 1024 and
65527; lint 41/41). Conformance, Robustness, Tests, Docs UNCLEAN by N1 only.
Verified clean in the pass: F1 parent gate 3 + self-test rc 0 (50/50) with c8+p2+amended c10; planted stale record and
unrecorded omission red live; verdict()/compare_tops() mutants all red; six-record pin 631eeb34 self-test 50/50;
check_sh_idiom rc 0 (r1 run.sh rc 1); elab_bounds mutants 12 of 12 killed, 3 expected equivalents survive; citations
:244-255, :350-354, :446-449, :376, :390, ARMS +10, top :2726 all correct; unchanged round-1 gate probes identical.
