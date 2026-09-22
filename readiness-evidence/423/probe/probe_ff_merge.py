from pathlib import Path
import importlib.util,json,os,subprocess,tempfile,sys
trusted=Path(sys.argv[1]).resolve()
spec=importlib.util.spec_from_file_location('trusted_containment',trusted)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
root=Path(tempfile.mkdtemp(prefix='milan-423-readiness-'))
os.chdir(root)
def git(*args):
 return subprocess.run(['git','--no-replace-objects',*args],check=True,capture_output=True,text=True).stdout.strip()
def commit(message):
 git('add','.');git('commit','--quiet','-m',message);return git('rev-parse','HEAD')
git('init','--quiet');git('config','user.name','Readiness fixture');git('config','user.email','fixture@example.invalid');git('config','commit.gpgsign','false')
(root/'feature.txt').write_text('before\n');(root/'other.txt').write_text('before\n');O=commit('Base')
git('checkout','--quiet','-b','incoming');(root/'feature.txt').write_text('after\n');A=commit('Original A')
git('checkout','--quiet','-b','candidate',O);git('merge','--quiet','--no-ff','incoming','-m','Redundant merge');M=git('rev-parse','HEAD');(root/'other.txt').write_text('after\n');C=commit('Original C')
git('checkout','--quiet','-b','target',O);git('cherry-pick',A);git('commit','--quiet','--amend','-m','Replay A');AP=git('rev-parse','HEAD');git('cherry-pick',C);git('commit','--quiet','--amend','-m','Replay C');CP=git('rev-parse','HEAD');(root/'feature.txt').write_text('after\nlater extension\n');D=commit('Later extension')
rows=[]
for name,base in [('exact_replay_then_extension',D)]:
 rows.append({'case':name,'base':base,'candidate':C,'current_verdict':module.contained(C,base),'existing_linear_proof':module._linear_patches_contained(C,base)})
git('checkout','--quiet','-b','reverted',CP);git('revert','--no-edit',AP);R=git('rev-parse','HEAD');rows.append({'case':'replay_then_exact_reversion','base':R,'candidate':C,'current_verdict':module.contained(C,R),'existing_linear_proof':module._linear_patches_contained(C,R)})
parents=git('show','-s','--format=%P',M).split();tree=git('rev-parse',M+'^{tree}');ancestor=subprocess.run(['git','merge-base','--is-ancestor',*parents],capture_output=True).returncode==0
record={'fixture':str(root),'objects':{'O':O,'A':A,'M':M,'C':C,'A_replay':AP,'C_replay':CP,'D_extension':D,'R_revert':R},'merge':{'parents':parents,'first_parent_ancestor_of_second':ancestor,'same_tree_as_second':tree==git('rev-parse',parents[1]+'^{tree}')},'cases':rows,'claim':'This probes existing helpers only; no production change or proof adoption.'}
print(json.dumps(record,indent=2))
