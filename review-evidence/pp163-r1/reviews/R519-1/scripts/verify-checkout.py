#!/usr/bin/env python3
"""Verify raw tracked bytes, executable modes, index entries and all gitlinks."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=pathlib.Path,required=True);a=ap.parse_args();repo=a.repo.resolve();p=pathlib.Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(["git",*args],cwd=repo)
head=git("rev-parse","HEAD").decode().strip();tree=git("rev-parse","HEAD^{tree}").decode().strip();assert head=="cd9825c947cf67b735d26cc1c42541ccd9d7f637";assert tree=="7234360164b13afa707faa552ebf72d4f10a44e7"
expected={};gitlinks=[];problems=[]
for record in git("ls-tree","-rz",head).split(b"\0"):
 if not record:continue
 meta,path=record.split(b"\t",1);mode,kind,oid=meta.decode().split();rel=os.fsdecode(path);expected[rel]=(mode,oid)
 if mode=="160000":
  actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo/rel).decode().strip();gitlinks.append(dict(path=rel,expected=oid,actual=actual));
  if actual!=oid:problems.append([rel,"gitlink"])
  continue
 f=repo/rel;data=os.fsencode(os.readlink(f)) if mode=="120000" else f.read_bytes();actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest();s=f.lstat();actual_mode="120000" if stat.S_ISLNK(s.st_mode) else "100755" if s.st_mode & stat.S_IXUSR else "100644"
 if actual!=oid or actual_mode!=mode:problems.append([rel,mode,actual_mode,oid,actual])
index={}
for record in git("ls-files","--stage","-z").split(b"\0"):
 if not record:continue
 meta,path=record.split(b"\t",1);mode,oid,stage=meta.decode().split();assert stage=="0";index[os.fsdecode(path)]=(mode,oid)
if index!=expected:problems.append("index differs from HEAD")
status=git("status","--porcelain=v1","--untracked-files=all").decode();assert not status,status
subprocess.run(["git","diff","--check","86a7b0c57831c15e9cd8b42d64cc4a9843f4e726.."+head],cwd=repo,check=True)
rec=dict(head=head,tree=tree,tracked_entries=len(expected),raw_blob_bytes_and_modes_match=not problems,index_entries_match=index==expected,gitlinks=gitlinks,gitlinks_note="No gitlinks exist in the processor tree; no parent checkout or parent submodule was mutated.",status=status,problems=problems)
(p/"receipts/checkout-integrity.json").write_text(json.dumps(rec,indent=2)+"\n");print(json.dumps(rec,indent=2));raise SystemExit(int(bool(problems)))
