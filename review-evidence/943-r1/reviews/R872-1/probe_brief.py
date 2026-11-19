#!/usr/bin/env python3
"""Show the published declaring-face fixture's effect on a brief bridge read."""
import ast
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
patch = packet / 'scratch/review-evidence/943-r1/author-r1/receipts/budget/declaring-face.patch.txt'
line = next(x[1:].strip() for x in patch.read_text().splitlines() if x.startswith('+') and 'memset(v,' in x)
body = ast.literal_eval(line)
source = r'''
#include "ctrl_app_aecp.c"
#include <stdio.h>
static unsigned calls;
bool acmp_view(const struct acmp *a, unsigned sink, struct acmp_sink_view *view)
{ (void)a; (void)sink; (void)view; return false; }
static void own_source(void *ctx, unsigned n, struct acmp_source_state *v)
{ (void)ctx; (void)n; ++calls; v->dest_mac_valid = true; v->stream.dest_mac = 0x91e0f0000100ULL; }
static bool b_stream(void *ctx, unsigned i, uint16_t t, uint16_t n, struct aecp_stream_info *v)
BODY
int main(void)
{
    struct ctrl_app app = {0};
    app.acmp.acmp.cfg.n_sources = 1;
    struct acmp_env owner = {.source = own_source};
    struct aecp_ports environment = {.stream = b_stream};
    struct ctrl_app_aecp bridge = {.app = &app, .environment = &environment, .acmp_owner = &owner};
    struct aecp_stream_info v = {.brief = true};
    bool ok = stream(&bridge, 0, 6, 0, &v);
    printf("answered=%u input_brief=1 returned_brief=%u source_calls=%u dest=%012llx\n",
           ok, v.brief, calls, (unsigned long long)v.dest_mac);
    return !(ok && calls == EXPECTED);
}
'''
work = packet / 'scratch/brief-probe'
work.mkdir(parents=True, exist_ok=True)
inc = [repo / 'sw/firmware/ctrl' / d for d in ('app', 'aecp', 'mbx', 'loop', 'port', 'adp', 'acmp', 'maap', 'srp')]
inc += [repo / 'sw/firmware/ctrl_nvm', repo / 'third_party/tsn-c-stack/include', repo / 'third_party/lwSRP/src/include']
generated = packet / 'scratch/focused-1x1-if1/aecp-mailbox-endstation_ax7101_1x1_tdm8-if1'
inc += [generated / 'gen']
for name, implementation, expected in [('published', body, 1), ('brief-preserved-control', body.replace('memset(v, 0, sizeof *v);', 'bool brief = v->brief; memset(v, 0, sizeof *v); v->brief = brief;'), 0)]:
    c = work / (name + '.c')
    c.write_text(source.replace('BODY', implementation).replace('EXPECTED', str(expected)))
    command = ['cc', '-std=c11', '-O2', '-ffunction-sections', '-fdata-sections', '-include', str(generated / 'srp_entity_gen.h'), *['-I' + str(p) for p in inc], str(c), '-Wl,--gc-sections', '-o', str(work / name)]
    subprocess.run(command, check=True)
    print(name + ':', flush=True)
    subprocess.run([str(work / name)], check=True)
