# A180 commands and raw results

All commands ran from the assigned donor lane. Raw output is retained without RTK filtering.
The inner command in each entry is run by `rtk proxy python3 run.py <tag> ...`.
`CONTEXT.md` describes pre-harness read-only discovery and apply_patch evidence edits.

| Tag | UTC start | Seconds | Exit | Raw log |
|---|---|---:|---:|---|
| issue102 | 2026-09-22T18:36:55.515153+00:00 | 0.501 | 0 | [log](logs/issue102.log) |
| issue102-comments | 2026-09-22T18:36:56.082088+00:00 | 0.448 | 0 | [log](logs/issue102-comments.log) |
| taken-post | 2026-09-22T18:37:23.487406+00:00 | 1.700 | 0 | [log](logs/taken-post.log) |
| parent-policy | 2026-09-22T18:37:25.250283+00:00 | 0.166 | 0 | [log](logs/parent-policy.log) |
| donor-build-policy | 2026-09-22T18:37:25.252839+00:00 | 0.192 | 0 | [log](logs/donor-build-policy.log) |
| original-finding | 2026-09-22T18:37:25.269266+00:00 | 0.548 | 0 | [log](logs/original-finding.log) |
| fixture-issues | 2026-09-22T18:37:25.263736+00:00 | 1.953 | 0 | [log](logs/fixture-issues.log) |
| donor-guide | 2026-09-22T18:37:58.421744+00:00 | 0.020 | 0 | [log](logs/donor-guide.log) |
| selector-inspect | 2026-09-22T18:37:58.431182+00:00 | 0.042 | 0 | [log](logs/selector-inspect.log) |
| verifier-policy | 2026-09-22T18:37:58.434076+00:00 | 0.165 | 0 | [log](logs/verifier-policy.log) |
| verilator-identity | 2026-09-22T18:38:23.916327+00:00 | 0.279 | 0 | [log](logs/verilator-identity.log) |
| real-binary-identity | 2026-09-22T18:39:01.542577+00:00 | 0.151 | 0 | [log](logs/real-binary-identity.log) |
| baseline-cflags | 2026-09-22T18:39:01.817817+00:00 | 0.062 | 0 | [log](logs/baseline-cflags.log) |
| source-base | 2026-09-22T18:39:53.360346+00:00 | 0.242 | 0 | [log](logs/source-base.log) |
| source-tested | 2026-09-22T18:39:53.664032+00:00 | 0.284 | 0 | [log](logs/source-tested.log) |
| focused-cflags | 2026-09-22T18:40:57.964000+00:00 | 0.142 | 2 | [log](logs/focused-cflags.log) |
| focused-cflags-only | 2026-09-22T18:41:20.548170+00:00 | 0.109 | 0 | [log](logs/focused-cflags-only.log) |
| hdl-lint | 2026-09-22T18:41:20.555615+00:00 | 10.179 | 0 | [log](logs/hdl-lint.log) |
| precise-diff | 2026-09-22T18:41:36.266557+00:00 | 0.022 | 0 | [log](logs/precise-diff.log) |
| diff-check | 2026-09-22T18:41:36.271662+00:00 | 0.035 | 0 | [log](logs/diff-check.log) |
| upc-map | 2026-09-22T18:41:36.289320+00:00 | 0.061 | 0 | [log](logs/upc-map.log) |
| doc-check | 2026-09-22T18:41:20.558453+00:00 | 30.241 | 0 | [log](logs/doc-check.log) |
| documentation-tool-identity | 2026-09-22T18:42:05.178152+00:00 | 0.492 | 0 | [log](logs/documentation-tool-identity.log) |
| runtime-progress | 2026-09-22T18:42:38.186639+00:00 | 0.135 | 0 | [log](logs/runtime-progress.log) |
| documentation-environment | 2026-09-22T18:42:38.188265+00:00 | 0.144 | 0 | [log](logs/documentation-environment.log) |
| pp-top-full | 2026-09-22T18:40:58.164944+00:00 | 187.217 | 0 | [log](logs/pp-top-full.log) |
| build-results | 2026-09-22T18:45:03.791544+00:00 | 0.053 | 0 | [log](logs/build-results.log) |
| precommit-integrity | 2026-09-22T18:45:35.696740+00:00 | 0.651 | 0 | [log](logs/precommit-integrity.log) |
| stage-fix | 2026-09-22T18:45:36.420244+00:00 | 0.018 | 0 | [log](logs/stage-fix.log) |
| staged-diff | 2026-09-22T18:45:36.516298+00:00 | 0.022 | 0 | [log](logs/staged-diff.log) |
| commit | 2026-09-22T18:45:36.621241+00:00 | 0.028 | 0 | [log](logs/commit.log) |
| source-final | 2026-09-22T18:45:36.792149+00:00 | 0.290 | 0 | [log](logs/source-final.log) |
| final-integrity | 2026-09-22T18:47:38.392632+00:00 | 0.326 | 0 | [log](logs/final-integrity.log) |
| unpublished-remote-proof | 2026-09-22T18:48:24.864008+00:00 | 0.623 | 0 | [log](logs/unpublished-remote-proof.log) |
| handoff-post | 2026-09-22T18:48:38.783497+00:00 | 1.515 | 0 | [log](logs/handoff-post.log) |

## issue102

```sh
rtk proxy gh api repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/102
```

## issue102-comments

```sh
rtk proxy gh api --paginate repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/102/comments
```

## taken-post

```sh
rtk proxy gh issue comment 102 --repo Mister-M-alt/protocol-processor-control-plane-avb-milan --body-file $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/TAKEN.md
```

## parent-policy

```sh
rtk proxy git -C $VALIDATION_STORAGE/lanes/trusted-dev-20260922-512 show 483a133ed08867ea0d300d2b4a027b5b48a4282f:CONTRIBUTING.md
```

## donor-build-policy

```sh
rtk proxy cat .github/workflows/hdl.yml tb/pp_top/Makefile scripts/lint_hdl.sh scripts/run_suites.sh
```

## original-finding

```sh
rtk proxy gh api repos/kebag-logic/milan-fpga/issues/comments/5781426819
```

## fixture-issues

```sh
rtk proxy python3 -c 'import subprocess,json; repo="Mister-M-alt/protocol-processor-control-plane-avb-milan"; [(print("ISSUE",n),print(subprocess.check_output(["rtk","proxy","gh","api",f"repos/{repo}/issues/{n}","--jq","{number,title,body,html_url,state}"],text=True)),print("COMMENTS",n),print(subprocess.check_output(["rtk","proxy","gh","api","--paginate",f"repos/{repo}/issues/{n}/comments","--jq",".[] | {id,body,html_url}"],text=True))) for n in (95,97)]'
```

## donor-guide

```sh
rtk proxy cat docs/guides/hdl-engineer.md hdl/README.md
```

## selector-inspect

```sh
rtk proxy python3 -c 'from pathlib import Path; import os,hashlib; p=Path("$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator"); print("selector",p,"resolved",p.resolve(),"mode",oct(p.lstat().st_mode)); print("sha256",hashlib.sha256(p.read_bytes()).hexdigest()); print(p.read_text()); print("inherited tool env",{k:v for k,v in os.environ.items() if k in ("VERILATOR","VERILATOR_ROOT","VERILATOR_BIN","MAKEFLAGS","CXX","CC","PATH")})'
```

## verifier-policy

```sh
rtk proxy python3 -c 'from pathlib import Path; import subprocess,hashlib,json; root=Path("$VALIDATION_STORAGE/lanes/trusted-dev-20260922-512"); ref="483a133ed08867ea0d300d2b4a027b5b48a4282f"; dest=Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/context"); files=["CONTRIBUTING.md","docs/development/CODE_QUALITY.md","scripts/check_cpp_idiom.py"]; records=[]; env=dict(__import__("os").environ,GIT_NO_REPLACE_OBJECTS="1");
for f in files:
 data=subprocess.check_output(["rtk","proxy","git","-C",str(root),"show",ref+":"+f],env=env); out=dest/Path(f).name; out.write_bytes(data); oid=subprocess.check_output(["rtk","proxy","git","-C",str(root),"rev-parse",ref+":"+f],env=env,text=True).strip(); actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest(); assert actual==oid; record=dict(path=f,git_blob=oid,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data));
 if f=="scripts/check_cpp_idiom.py":
  disk=(root/f).read_bytes(); assert disk==data; record["checkout_bytes_match"]=True
 records.append(record)
(dest/"parent-policy-identity.json").write_text(json.dumps(dict(commit=ref,files=records),indent=2)+"\n"); print(json.dumps(records,indent=2)); print("CONTRIBUTING sections 1-2:"); print((dest/"CONTRIBUTING.md").read_text().split("## 3.")[0]); print("C++ policy:"); content=(dest/"CODE_QUALITY.md").read_text(); a=content.find("## Rule 11"); b=content.find("## Rule 12",a+1); print(content[a:b]); print("checker:"); print((dest/"check_cpp_idiom.py").read_text())'
```

## verilator-identity

```sh
rtk proxy python3 -c 'import pathlib,subprocess,hashlib,json,os,shlex; selector=pathlib.Path("$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator"); words=shlex.split(selector.read_text().splitlines()[1]); root=pathlib.Path(words[2].split("=",1)[1]); front=pathlib.Path(words[3]); binary=root/"bin/verilator_bin"; paths=[selector,front,binary]; records=[];
for p in paths:
 d=p.read_bytes(); records.append(dict(path=str(p),resolved=str(p.resolve()),size=len(d),mode=oct(p.lstat().st_mode),sha256=hashlib.sha256(d).hexdigest()))
print(json.dumps(records,indent=2)); print("VERILATOR_ROOT",root); print(subprocess.check_output(["rtk","proxy",str(selector),"--version"],text=True)); print(subprocess.check_output(["rtk","proxy",str(binary),"--version"],env=dict(os.environ,VERILATOR_ROOT=str(root)),text=True)); print(subprocess.check_output(["rtk","proxy",str(selector),"-V"],text=True)); print(subprocess.check_output(["rtk","proxy","file",str(binary.resolve())],text=True)); print(subprocess.check_output(["rtk","proxy","g++","--version"],text=True)); print(subprocess.check_output(["rtk","proxy","make","--version"],text=True)); pathlib.Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/context/tool-identity.json").write_text(json.dumps(dict(verilator_root=str(root),files=records),indent=2)+"\n")'
```

## real-binary-identity

```sh
rtk proxy python3 -c 'import pathlib,json,hashlib,subprocess,os; p=pathlib.Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/context/tool-identity.json"); obj=json.loads(p.read_text()); real=pathlib.Path(obj["files"][1]["path"]).with_name("verilator_bin"); data=real.read_bytes(); assert data[:4]==b"\x7fELF"; obj["files"].append(dict(path=str(real),resolved=str(real.resolve()),bytes=len(data),mode=oct(real.stat().st_mode),sha256=hashlib.sha256(data).hexdigest(),kind="ELF")); print(json.dumps(obj["files"][-1],indent=2)); print(subprocess.check_output(["rtk","proxy",str(real),"--version"],env=dict(os.environ,VERILATOR_ROOT=obj["verilator_root"]),text=True)); print(subprocess.check_output(["rtk","proxy","file",str(real)],text=True)); print(subprocess.check_output(["rtk","proxy","readelf","-n",str(real)],text=True)); p.write_text(json.dumps(obj,indent=2)+"\n")'
```

## baseline-cflags

```sh
rtk proxy python3 -B -c 'import importlib.util,pathlib,hashlib; p=pathlib.Path("$VALIDATION_STORAGE/lanes/trusted-dev-20260922-512/scripts/check_cpp_idiom.py"); data=p.read_bytes(); assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()=="1d9ccd7fa1fded549f8988149397ff10bc12b0d5"; spec=importlib.util.spec_from_file_location("parent_cpp",p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); make=pathlib.Path("tb/pp_top/Makefile").read_text(); result=mod.cflags_missing(make); print("baseline cflags_missing:",result); assert result==["-Wall","-Wextra"]; pathlib.Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/context/Makefile.before").write_text(make)'
```

## source-base

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/snapshot.py base
```

## source-tested

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/snapshot.py tested
```

## focused-cflags

```sh
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/check_flags.py
```

## focused-cflags-only

```sh
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/check_flags.py
```

## hdl-lint

```sh
rtk proxy python3 -B -c 'import os,subprocess,sys; env=dict(os.environ); env["PATH"]="$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:"+env["PATH"]; print("PATH="+env["PATH"],flush=True); sys.exit(subprocess.run(["rtk","proxy","bash","scripts/lint_hdl.sh"],env=env).returncode)'
```

## precise-diff

```sh
rtk proxy git diff -- tb/pp_top/Makefile
```

## diff-check

```sh
rtk proxy git diff --check
```

## upc-map

```sh
rtk proxy python3 scripts/check_upc_map.py
```

## doc-check

```sh
rtk proxy make -j1 check
```

## documentation-tool-identity

```sh
rtk proxy python3 -B -c 'import importlib.metadata as m,sys,shutil,pathlib,hashlib,subprocess,json; records={"python":sys.version,"executables":[],"packages":{}};
for name in ["python3","g++","make","mmdc","node","rtk","git"]:
 path=shutil.which(name); p=pathlib.Path(path); rec=dict(name=name,path=path,resolved=str(p.resolve()),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),mode=oct(p.lstat().st_mode)); records["executables"].append(rec)
for name in ["wavedrom","svgwrite","six"]:
 try: records["packages"][name]=m.version(name)
 except m.PackageNotFoundError: records["packages"][name]="not installed in system Python"
print(json.dumps(records,indent=2)); pathlib.Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/context/host-tools.json").write_text(json.dumps(records,indent=2)+"\n"); print(subprocess.check_output(["rtk","proxy","mmdc","--version"],text=True)); print(subprocess.check_output(["rtk","proxy","node","--version"],text=True))'
```

## runtime-progress

```sh
rtk proxy python3 -B -c 'from pathlib import Path; import subprocess; p=Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/logs/pp-top-full.log"); t=p.read_text(); print("raw log bytes",p.stat().st_size); print("\n".join(line for line in t.splitlines() if "fixture guard" in line or "test_compiler" in line or "checks:" in line)); print(subprocess.check_output(["rtk","proxy","ps","-C","Vpp_top_sim,Vpp_top_vid","-o","pid,etime,time,pcpu,stat,args"],text=True))'
```

## documentation-environment

```sh
rtk proxy python3 -B -c 'from pathlib import Path; import subprocess,json,hashlib; p=Path(".venv-wavedrom"); print("venv exists",p.exists(),"symlink",p.is_symlink(),"resolved",p.resolve());
if p.exists():
 print((p/"pyvenv.cfg").read_text()); print(subprocess.check_output(["rtk","proxy",str(p/"bin/python"),"-c","import sys,importlib.metadata as m; print(sys.version); print({x:m.version(x) for x in (\"wavedrom\",\"svgwrite\",\"six\")})"],text=True))
p=Path("$WORKSPACE_HOME/.local/lib/node_modules/@mermaid-js/mermaid-cli/package.json"); print("mermaid-cli package",p,"sha256",hashlib.sha256(p.read_bytes()).hexdigest()); print("mermaid-cli version",json.loads(p.read_text())["version"])'
```

## pp-top-full

```sh
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/build.py
```

## build-results

```sh
rtk proxy python3 -B -c 'import json,hashlib; from pathlib import Path; root=Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author"); t=(root/"logs/pp-top-full.log").read_text(); print("\n".join(line for line in t.splitlines() if "fixture guard" in line or "[build " in line or "checks:" in line or "test_compiler" in line)); assert "[build default, SRP_DOM_DEF_VID_P 0x0002] 1391 checks, 0 failures" in t; assert "[build fixture, SRP_DOM_DEF_VID_P 0x5a3c] 20 checks, 0 failures" in t; assert "1411 checks: 1411 PASS, 0 FAIL" in t; records=[];
for rel in ["tb/pp_top/obj_dir/Vpp_top_sim","tb/pp_top/obj_vid/Vpp_top_vid","tb/pp_top/obj_dir/build_tally.txt","tb/pp_top/ltn_rom.hex","tb/pp_top/ucode.hex"]:
 p=Path(rel); data=p.read_bytes(); records.append(dict(path=rel,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),mode=oct(p.lstat().st_mode)))
print(json.dumps(records,indent=2)); print("tally bytes:",Path("tb/pp_top/obj_dir/build_tally.txt").read_text()); (root/"build-artifacts.json").write_text(json.dumps(records,indent=2)+"\n"); (root/"build-tally.txt").write_bytes(Path("tb/pp_top/obj_dir/build_tally.txt").read_bytes())'
```

## precommit-integrity

```sh
rtk proxy python3 -B -c 'import json,hashlib,subprocess,os; from pathlib import Path; root=Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author"); obj=json.loads((root/"source-manifest-tested.json").read_text());
for e in obj["entries"]:
 p=Path(e["path"]); assert oct(p.lstat().st_mode)==e["filesystem_mode"]; assert not p.is_symlink(); assert hashlib.sha256(p.read_bytes()).hexdigest()==e["sha256"],p
assert subprocess.check_output(["rtk","proxy","git","diff","--numstat"],text=True)=="1\t1\ttb/pp_top/Makefile\n"; assert subprocess.check_output(["rtk","proxy","git","ls-files","--others","--exclude-standard"],text=True)==""; flags=subprocess.check_output(["rtk","proxy","git","ls-files","-v"],text=True); assert all(line.startswith("H ") for line in flags.splitlines());
for e in json.loads((root/"context/tool-identity.json").read_text())["files"]:
 assert hashlib.sha256(Path(e["path"]).read_bytes()).hexdigest()==e["sha256"]
for e in json.loads((root/"context/checker-inputs.json").read_text()):
 assert hashlib.sha256((Path("$VALIDATION_STORAGE/lanes/trusted-dev-20260922-512")/e["path"]).read_bytes()).hexdigest()==e["sha256"]
patch=subprocess.check_output(["rtk","proxy","git","diff","--binary","--full-index"]); (root/"source.patch").write_bytes(patch); print("224 tested source byte sequences and filesystem modes unchanged; only 1 insertion/1 deletion in tb/pp_top/Makefile; no untracked files, hidden index flags, tool or checker drift")'
```

## stage-fix

```sh
rtk proxy git add -- tb/pp_top/Makefile
```

## staged-diff

```sh
rtk proxy git diff --cached --check
```

## commit

```sh
rtk proxy git commit -m 'Repeat warning flags in pp_top VID fixture CFLAGS group'
```

## source-final

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/snapshot.py final
```

## final-integrity

```sh
rtk proxy python3 -B -c 'from pathlib import Path; import json,subprocess,hashlib,os; root=Path("$WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author"); tested=json.loads((root/"source-manifest-tested.json").read_text()); final=json.loads((root/"source-manifest-final.json").read_text()); assert final["head"]=="e0c43b03f31d6c1220dd05a110e4bb30029233a0"; assert final["tree"]=="0547903adc17449dfb4f0c2610a23e6adb4ff6a2"; assert not final["dependency_pins"]; assert len(tested["entries"])==len(final["entries"])==224;
for a,b in zip(tested["entries"],final["entries"]):
 for key in ("path","sha256","filesystem_kind","filesystem_mode","size"):
  assert a[key]==b[key], (a["path"],key)
 assert b["matches_head_bytes"] and b["matches_head_kind_mode"]
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1"); git=lambda *a:subprocess.check_output(["rtk","proxy","git",*a],env=env); assert git("status","--porcelain")==b""; assert git("rev-parse","HEAD^").decode().strip()==tested["head"]; msg=git("show","-s","--format=%B").decode().strip(); assert msg=="Repeat warning flags in pp_top VID fixture CFLAGS group"; assert git("diff","HEAD^","HEAD","--numstat")==b"1\t1\ttb/pp_top/Makefile\n"; assert git("diff","HEAD^","HEAD","--binary","--full-index")== (root/"source.patch").read_bytes(); (root/"commit.txt").write_bytes(git("show","--format=fuller","--stat","HEAD")); print("Committed head/tree, all tested source bytes/kinds/modes/index, no dependency pins, exact one-line patch, one-line no-trailer commit and clean worktree verified."); print(git("status","--porcelain=v2","--branch").decode()); print(git("show","--format=fuller","--stat","HEAD").decode())'
```

## unpublished-remote-proof

```sh
rtk proxy git ls-remote --heads origin refs/heads/102-pp-fixture-warning-flags
```

## handoff-post

```sh
rtk proxy gh issue comment 102 --repo Mister-M-alt/protocol-processor-control-plane-avb-milan --body-file $WORKSPACE_HOME/milan-fpga-management/2026-09-22/pp102-author/ISSUE-HANDOFF.md
```
