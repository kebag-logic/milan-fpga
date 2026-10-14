# Included by r638_4_probes.py: literal dollar text in a Make directory operand.
def s8(f):
    common(f)
    f.file('sub$x/Makefile', 'all:\n\tbrand_new_command\n')
    f.run("make -C 'sub$x'")


probe('S8', "literal single-quoted 'sub$x' make -C directory treated as runtime residue", 'REFUSED', s8)
