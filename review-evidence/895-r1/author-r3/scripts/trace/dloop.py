#!/usr/bin/env python3
"""dloop.py ELF...: for each split image, the data cache lines (8 KiB, 64 B lines, 128 sets, direct-mapped) that
each MAAP poll's per-source loop touches (refresh_demand -> acmp_declaring -> the source ports), and every pair of
distinct lines that share a set. Frames from each function's first 'addi sp,sp,-N'; the chain _start, main,
ctrl_loop_run, ctrl_loop_step, ctrl_loop_service, maap_mbx poll, refresh_demand, acmp_declaring. Read-only."""
import re, subprocess, sys
BIN = '$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-'
def syms(elf):
    out = {}
    for l in subprocess.run([BIN + 'nm', '-S', elf], capture_output=True, text=True).stdout.splitlines():
        f = l.split()
        if len(f) >= 3:
            out.setdefault(f[-1], []).append((int(f[0], 16), int(f[1], 16) if len(f) == 4 else 0, f[-2]))
    return out
def dis(elf, a, n):
    return subprocess.run([BIN + 'objdump', '-d', f'--start-address={a:#x}', f'--stop-address={a + n:#x}', elf],
                          capture_output=True, text=True).stdout
def frame(elf, a, n):
    m = re.search(r'addi\s+sp,sp,-(\d+)', dis(elf, a, n))
    return int(m.group(1)) if m else 0
def text(s, name, size_hint=None):
    c = [x for x in s.get(name, []) if x[2] in 'tT']
    if size_hint is not None:
        c = [x for x in c if x[1] == size_hint] or c
    return c
for elf in sys.argv[1:]:
    s = syms(elf)
    top = s['_stack_top'][0][0]
    chain = [('main', None), ('ctrl_loop_run', None), ('ctrl_loop_step', None), ('ctrl_loop_service', None)]
    sp = top; frames = []
    for name, _ in chain:
        a, n, _t = text(s, name)[0]; f = frame(elf, a, n); sp -= f; frames.append((name, f))
    # maap_mbx's poll: the poll whose code calls refresh_demand
    rd = text(s, 'refresh_demand')[0]
    polls = [p for p in text(s, 'poll') if f'<refresh_demand>' in dis(elf, p[0], p[1])]
    pa, pn, _ = polls[0]; f = frame(elf, pa, pn); sp -= f; frames.append(('maap poll', f)); poll_sp = sp
    f = frame(elf, rd[0], rd[1]); sp -= f; frames.append(('refresh_demand', f)); rd_sp = sp
    ad = text(s, 'acmp_declaring')[0]; f = frame(elf, ad[0], ad[1]); sp -= f; frames.append(('acmp_declaring', f))
    ad_sp = sp
    app = s['image_app'][0][0]; bridge = s['image_aecp_bridge'][0][0]
    # ctrl_app_srp's source: lui a5,K; add a0,a0,a5; lw a5,OFF(a0) -> app->acmp_owner
    srcs = [x for x in text(s, 'source') if x[1] == 24]
    d = dis(elf, srcs[0][0], 24)
    hi = int(re.search(r'lui\s+a5,0x([0-9a-f]+)', d).group(1), 16) << 12
    lo = int(re.search(r'lw\s+a5,(-?\d+)\(a0\)', d).group(1))
    owner = app + hi + lo
    lines = {}
    def add(addr, n, what):
        for ln in range(addr >> 6, (addr + n - 1 >> 6) + 1):
            lines.setdefault(ln, set()).add(what)
    add(ad_sp, 64, 'acmp_declaring frame'); add(rd_sp, rd_sp - ad_sp if False else 16, 'refresh_demand frame')
    add(owner, 4, 'app->acmp_owner'); add(bridge + 16, 4, 'bridge acmp_owner (c+16)')
    add(app + 0x908, 4, 'acmp+0'); add(app + 0x908 + 76, 4, 'acmp n_sources'); add(app + 0x908 + 100, 4, 'acmp env')
    for k in range(8):
        add(app + 0x908 + 0x1000 + 108 + 8 * k, 1, f'acmp per-source {k}')
    add(app + 0x908 + 0x1000 + 241, 1, 'acmp busy byte')
    if 'image_env' in s:
        add(s['image_env'][0][0], 24, 'image_env')
    by_set = {}
    for ln, w in lines.items():
        by_set.setdefault(ln & 127, []).append((ln, w))
    print(f"== {elf}\n   stack_top {top:#x} frames {frames} acmp_declaring sp {ad_sp:#x} app {app:#x} bridge {bridge:#x} owner {owner:#x}")
    clash = [(st, v) for st, v in sorted(by_set.items()) if len(v) > 1]
    for st, v in clash:
        print(f"   CONFLICT set {st}: " + ' | '.join(f"{ln << 6:#x} {sorted(w)}" for ln, w in v))
    if not clash:
        print('   no conflict among the loop lines')
