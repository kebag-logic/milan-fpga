"""ccinline.py TREE: CTRL_CC_INLINE in TREE's plat/ctrl_cc.h (GNU always_inline; plain inline with 0), and mbx.c's
tx_commit declared with it, so mbx_tx_begin calls nothing (txcommit.py writes tx_commit). Scratch writer."""
import sys
from pathlib import Path
T = Path(sys.argv[1])
p = T / 'sw/firmware/ctrl/plat/ctrl_cc.h'; t = p.read_text()
reps = [
("""//   CTRL_CC_NOINLINE   a function kept out of line, so the hot code that
//                      calls it stays small (GNU noinline); nothing with 0.
""",
 """//   CTRL_CC_NOINLINE   a function kept out of line, so the hot code that
//                      calls it stays small (GNU noinline); nothing with 0.
//   CTRL_CC_INLINE     a function inlined where it is called, so a hot caller
//                      saves no registers for a call (GNU always_inline);
//                      plain inline with 0.
"""),
("#define CTRL_CC_NOINLINE __attribute__((noinline))\n", "#define CTRL_CC_NOINLINE __attribute__((noinline))\n#define CTRL_CC_INLINE inline __attribute__((always_inline))\n"),
("#define CTRL_CC_NOINLINE\n", "#define CTRL_CC_NOINLINE\n#define CTRL_CC_INLINE inline\n"),
]
for a, b in reps:
    assert t.count(a) == 1, a[:40]
    t = t.replace(a, b)
p.write_text(t)
m = T / 'sw/firmware/ctrl/mbx/mbx.c'; u = m.read_text()
a = "static inline bool tx_commit(unsigned ch)\n"
assert u.count(a) == 1
u = u.replace(a, "static CTRL_CC_INLINE bool tx_commit(unsigned ch)\n")
a = '#include "mbx_wire.h"\n'
assert u.count(a) == 1
u = u.replace(a, '#include "mbx_wire.h"\n#include "../plat/ctrl_cc.h"\n')
m.write_text(u)
print('CTRL_CC_INLINE on tx_commit')

d = T / 'sw/firmware/ctrl/plat/mbx_dma.h'; w = d.read_text()
a = "static inline bool mbx_dma_wait(void)\n"
assert w.count(a) == 1
w = w.replace(a, "static CTRL_CC_INLINE bool mbx_dma_wait(void)\n")
inc = w.index('#include')
w = w[:inc] + '#include "ctrl_cc.h"\n' + w[inc:]
d.write_text(w)
print('CTRL_CC_INLINE on mbx_dma_wait')
