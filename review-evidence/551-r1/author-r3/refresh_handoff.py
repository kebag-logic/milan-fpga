from pathlib import Path
import json,shlex
out=Path(__file__).resolve().parent
records=[json.loads(l) for l in (out/"gates.jsonl").read_text().splitlines()]
latest={r["name"]:r for r in records}
names=[("Full behaviour suite","behave"),("Licence leg","crflic"),("Licence mutation campaign","crflic_mutants"),("Default datapath sweep","milan_dp_default"),("Documentation, Git inventory","docs_git_final"),("Documentation, filesystem inventory","docs_no_git_final"),("Added-line em dash","em_dash_final"),("Documentation style","doc_style_final"),("Contents","gen_toc"),("Cited paths","doc_paths"),("Generated matrices","module_matrix"),("Syntax analysis","xvlog"),("RTL source lists","rtl_source_lists"),("Python idiom","py_idiom"),("C++ idiom","cpp_idiom"),("Whitespace","diff_check")]
lines=["## Validation","","Every gate runs in the foreground without a pipeline. Commands below use repository root, except `behave` in `tests`. Raw commands, working directories, exit codes and durations are in `gates.jsonl`. The negative control is recorded separately above.","","| Gate | Command | Result | Evidence |","|---|---|---|---|"]
for label,key in names:
 r=latest.get(key)
 if r:
  cmd=r["command"] if isinstance(r["command"],str) else shlex.join(r["command"])
  lines.append(f"| {label} | `{cmd}` | rc {r['rc']} | `{r['log']}` |")
 else: lines.append(f"| {label} | Pending | Running / not complete | Pending |")
lines.extend(["","Initial attempts: `em_dash.log` judged the pre-merge HEAD (the script reads committed HEAD), and `doc_style.log` found three overlong changelog sentences. The merge commit and the shortened sentences are covered by the successful final receipts above. No unrelated dev text was edited to address those pre-merge diagnostics.","","Syntax analysis actually ran: zero first-party findings and four unchanged pinned-processor findings at the existing ratchet. The filesystem documentation run explicitly skips its Git inventory-parity arm only.","","Gate environment: pinned simulator 5.050 from the existing shared prefix and the existing hash-locked Markdown environment, both outside the output directory. No toolchains, SDK copies, virtual environments, installed packages or source-tree exports are stored in the output directory.",""])
p=out/"HANDOFF.md"; s=p.read_text();a=s.index("## Validation");b=s.index("## Final state",a);p.write_text(s[:a]+"\n".join(lines)+"\n"+s[b:])
