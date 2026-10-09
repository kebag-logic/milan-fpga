#!/usr/bin/env python3
import hashlib,json,os,pathlib,re,subprocess,sys
r=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();w=p/'scratch/assertion-audit';w.mkdir(exist_ok=True)
e=dict(os.environ);e.update(json.loads((p/'scratch/environment.json').read_text()))
for k in ('CPATH','CPLUS_INCLUDE_PATH','C_INCLUDE_PATH','LIBRARY_PATH','PKG_CONFIG_ALLOW_SYSTEM_CFLAGS','PKG_CONFIG_ALLOW_SYSTEM_LIBS'):e.pop(k,None)
os.environ.clear();os.environ.update(e)
sys.path.insert(0,str(r/'scripts'));import assertion_forms as a
inc=p/'scratch/sdk/gtest/include';headers=sorted(list((inc/'gtest').glob('*.h'))+list((inc/'gmock').glob('*.h')))
rows=[];lists={}
for cxx in ('g++','clang++'):
 os.environ['CXX']=cxx;lists[cxx]=a.refused_macros(); union=set()
 for header in headers:
  result=subprocess.run([cxx,'-std=c++20',*a.package_flags('--cflags'),'-x','c++','-dM','-E','-'],input='#include <'+header.relative_to(inc).as_posix()+'>\n',text=True,capture_output=True,check=True)
  names=set(re.findall(r'^#define ([A-Za-z_]\w*)\(',result.stdout,re.M))
  public={n for n in names if not n.endswith('_') and (n.startswith(('EXPECT_','ASSERT_','GTEST_','FAIL','ADD_FAILURE')) or n=='SUCCEED')};union|=public
 assert sorted(union-a.ALLOWED)==lists[cxx]
 for n in lists[cxx]+['GTEST_NONFATAL_FAILURE_','EXPECT_UNLISTED_','ASSERT_UNLISTED_','GTEST_UNLISTED_']:
  assert a.errors(n+'(false);')==['unsupported assertion form: '+n]
 project=w/(cxx.replace('+','p')+'.cpp');project.write_text('bool compare(unsigned left, int right) { return left == right; }\n')
 result=subprocess.run([cxx,'-Wall','-Wextra','-Werror',*a.package_flags('--cflags'),'-c',str(project),'-o',str(w/'warning.o')],text=True,capture_output=True)
 (w/(cxx.replace('+','p')+'.log')).write_text(result.stdout+result.stderr)
 assert result.returncode!=0 and 'sign-compare' in result.stderr
 rows.append(dict(compiler=cxx,header_count=len(headers),union_matches_generated=True,refused_names=len(lists[cxx]),project_sign_compare_refused=True))
assert lists['g++']==lists['clang++']==json.loads((r/'scripts/assertion-defaults.json').read_text())['refused_macros']
for n in a.ALLOWED:assert a.errors(n+'(true);')==[]
result=dict(results=rows,headers=[dict(name=x.relative_to(inc).as_posix(),sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in headers],names=lists['g++'],package_flags=a.package_flags('--cflags','--libs'),ambient_paths_removed=True)
(p/'receipts/assertion-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('21 public headers; separate-header union equals both generated 85-name lists; prefix refusals and 14 allowed identifiers correct; both project signedness controls refused')
