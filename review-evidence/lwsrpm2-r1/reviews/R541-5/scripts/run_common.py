# SPDX-License-Identifier: Apache-2.0
import os, sys, json, subprocess, pathlib, concurrent.futures
PACKET = pathlib.Path(__file__).resolve().parents[1]
ROOT = pathlib.Path(os.environ.get("REVIEW_SOURCE", os.getcwd())).resolve()
SCRATCH = PACKET / "scratch"
RECEIPTS = PACKET / "receipts"
def run(label, args, cwd=ROOT, env=None, timeout=540):
    result = subprocess.run(list(map(str,args)), cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    output = result.stdout.replace(str(ROOT), "$REVIEW_SOURCE").replace(str(PACKET), "$REVIEW_PACKET")
    (RECEIPTS/(label+".log")).write_text(output)
    (RECEIPTS/(label+".rc")).write_text(str(result.returncode)+"\n")
    print(label, "rc",result.returncode,flush=True)
    return result.returncode, output
if __name__ == "__main__":
    def dependency():
        source=SCRATCH/"cgreen"; build=SCRATCH/"cgreen-build"; prefix=SCRATCH/"prefix"
        assert run("dependency-configure", ["cmake","-S",source,"-B",build,"-DCMAKE_INSTALL_PREFIX="+str(prefix),"-DCGREEN_WITH_UNIT_TESTS=OFF","-DCGREEN_WITH_STATIC_LIBRARY=OFF"])[0]==0
        assert run("dependency-build",["make","-C",build,"-j16"])[0]==0
        assert run("dependency-install",["cmake","--install",build])[0]==0
    def docs():
        for name,script,options in [("sentences","check_sentences.py",[]),("references","check_references.py",[]),("references-self","check_references.py",["--self-test"]),("links","check_links.py",["--github-auth"])]:
            run(name,[sys.executable,"doc/tools/"+script]+options)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        fs=[pool.submit(dependency),pool.submit(docs)]
        for f in fs: f.result()
