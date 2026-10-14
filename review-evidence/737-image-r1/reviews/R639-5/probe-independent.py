import pathlib,sys,os,shutil,json,subprocess,contextlib,io
root=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(root/'scripts'))
import ci_tool_inventory as inv
import yaml
os.environ['CI_IMAGE_SHFMT']=str(p/'scratch/shfmt')
cases=[
('make_target_override','make SCRIPT=hidden.sh',{'Makefile':'all: SCRIPT=benign.sh\nall: ; bash $(SCRIPT)\n'}),
('make_environment_memo','TOOL=echo make; TOOL=brand_new_command make',{'Makefile':'TOOL ?= echo\nall: ; $(TOOL) okay\n'}),
('shell_script_environment_memo','TOOL=echo bash bootstrap.sh; TOOL=brand_new_command bash bootstrap.sh',{'bootstrap.sh':'"$TOOL" okay\n'}),
('make_pattern_directory','make sub/task.out',{'Makefile':'%.out: ; bash $*.sh\n','sub/task.sh':'brand_new_command\n','task.sh':'echo okay\n'}),
('make_suffix_stem','make task.sh',{'Makefile':'task.sh: ; bash $*.py\n','task.py':'brand_new_command\n','.py':'echo okay\n'}),
('shell_new_construct','coproc echo okay',{}),
('make_new_construct','make',{'Makefile':'.ONESHELL:\nall: ; echo okay\n'}),
('python_new_construct','python3 bootstrap.py',{'bootstrap.py':'async def f(): pass\n'}),
('trap_new_construct',"trap 'coproc echo okay' EXIT",{}),
('startup_variable','BASH_ENV=hidden.sh bash benign.sh',{}),
('source_unlisted','source hidden.sh',{}),
]
results=[]
for name,command,files in cases:
 d=p/'scratch'/'probes'/name;d.mkdir(parents=True,exist_ok=True)
 for rel in ('command-table.json','syntax-census.json','sources.lock.json'):
  dest=d/'ci/image'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/'ci/image'/rel,dest)
 files={'hidden.sh':'brand_new_command\n','benign.sh':'echo okay\n',**files}
 for rel,body in files.items():
  dest=d/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(body)
 workflow=d/'.github/workflows/probe.yml';workflow.parent.mkdir(parents=True,exist_ok=True)
 workflow.write_text(yaml.safe_dump({'jobs':{'probe':{'steps':[{'run':command}]}}}))
 row={'case':name,'run':command,'files':files,'census_modified':False,'table_modified':False}
 for mode in ('--write','--check'):
  sys.argv=['ci_tool_inventory.py','--root',str(d),mode];out=io.StringIO()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):rc=inv.main()
  row[mode]={'rc':rc,'output':out.getvalue()}
 # Execute only safe sentinels in this disposable tree; unknown command cannot install.
 if name in ('make_target_override','make_environment_memo','shell_script_environment_memo','make_pattern_directory','make_suffix_stem'):
  r=subprocess.run(['bash','-c',command],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  row['real_tool']={'rc':r.returncode,'output':r.stdout.replace(str(d),'<probe>')}
 results.append(row);print(name,row['--write'],row.get('real_tool',''),flush=True)
(p/'independent-probes.json').write_text(json.dumps(results,indent=2)+'\n')
