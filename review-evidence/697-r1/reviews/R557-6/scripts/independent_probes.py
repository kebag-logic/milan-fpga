#!/usr/bin/env python3
import argparse,json,pathlib,subprocess,sys
p=argparse.ArgumentParser(); p.add_argument("tree",type=pathlib.Path); p.add_argument("work",type=pathlib.Path); a=p.parse_args(); a.tree=a.tree.resolve(); a.work=a.work.resolve(); a.work.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(a.tree/"scripts"))
from assertion_forms import errors
from needle_audit import assertion_literals
from check_comments import check
cases={"allowed-control":"EXPECT_TRUE(false)","rejected-control":"EXPECT_NEAR(1.0, 2.0, 0.1)","unlisted-fail":"GTEST_FAIL()","unlisted-comparison":"GTEST_ASSERT_LT(2, 1)"}
rows=[]
for name,line in cases.items():
 text="// SPDX-License-Identifier: MIT\n#include <gtest/gtest.h>\n// REQ: PORT-01\nTEST(Review, Control) { "+line+" << \"review diagnostic\"; }\n"
 source=a.work/(name+".cpp"); source.write_text(text); binary=a.work/name
 command=["g++","-std=c++20","-Wall","-Wextra","-Werror",str(source),"-lgtest_main","-lgtest","-pthread","-o",str(binary)]
 result=subprocess.run(command,capture_output=True,text=True); (a.work/(name+"-build.log")).write_text(result.stdout+result.stderr)
 row={"case":name,"form":line,"compile_rc":result.returncode,"assertion_form_errors":errors(text),"comment_errors":check(text,language="c++",path="tests/test_review.cpp")}
 if result.returncode==0:
  report=a.work/(name+".xml"); run=subprocess.run([str(binary),"--gtest_output=xml:"+str(report)],capture_output=True,text=True); (a.work/(name+"-run.log")).write_text(run.stdout+run.stderr); row["execution_rc"]=run.returncode
  tree=a.work/(name+"-tree"); (tree/"tests").mkdir(parents=True,exist_ok=True); (tree/"tests/test_review.cpp").write_text(text)
  try: row["inventory"]=assertion_literals(tree); row["source_gate"]="accepted"
  except ValueError as e: row["source_gate"]="refused"; row["error"]=str(e)
 rows.append(row)
print(json.dumps(rows,indent=2))
(a.work/"results.json").write_text(json.dumps(rows,indent=2)+"\n")
assert all(x["compile_rc"]==0 and x["execution_rc"]==1 for x in rows)
assert rows[0]["source_gate"]=="accepted" and rows[1]["source_gate"]=="refused"
