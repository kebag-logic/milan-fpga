"""Compile an empty source with each GCC driver spelling that defines a macro (run under ctrl_capture.py)."""
import shutil
import subprocess
import os
REAL = shutil.which("gcc", path=os.pathsep.join(os.environ["PATH"].split(os.pathsep)[1:]))
FORMS = (["-Wp,-DCTRL_R584_WP"], ["-Xpreprocessor", "-DCTRL_R584_XP"], ["--define-macro=CTRL_R584_LONG"],
         ["--define-macro", "CTRL_R584_LONG2"], ["@planted.rsp"], ["-imacros", "modes.h"])
for form in FORMS:
    res = subprocess.run(["cc", *form, "-E", "-dM", "planted.c"], capture_output=True, text=True, check=False)
    print(" ".join(form), "->", sorted(w for w in res.stdout.split() if w.startswith("CTRL_R584")), "rc", res.returncode)
res = subprocess.run(REAL + " -DCTRL_R584_SHABS -E -dM planted.c", shell=True, capture_output=True, text=True)
print("shell abs ->", sorted(w for w in res.stdout.split() if w.startswith("CTRL_R584")), "rc", res.returncode)
