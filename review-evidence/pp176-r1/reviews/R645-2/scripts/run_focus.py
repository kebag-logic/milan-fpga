#!/usr/bin/env python3
"""Run two bounded exact-head spot checks in disposable extracts, never the source checkout.

Usage: python3 run_focus.py SOURCE_CHECKOUT PACKET_DIRECTORY
Requires the scoped simulator path below and make/C++/Python/git on PATH.
All children are awaited; two builds use eight workers each, total at most sixteen.
"""
import concurrent.futures
import difflib
import io
import pathlib
import subprocess
import sys
import tarfile

source = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(sys.argv[2]).resolve()
scratch = packet / 'scratch' / 'focus'
receipts = packet / 'receipts'
scratch.mkdir(parents=True, exist_ok=True)
receipts.mkdir(exist_ok=True)
sim = '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
head = '26ddcba423a204e75238d737ef41e6cb6e30ebc3'
assert subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() == head
identity = subprocess.check_output([sim, '--version'], text=True)
assert '5.050' in identity and 'rev v5.050' in identity
(receipts / 'compiler-identity.txt').write_text(identity)
archive = subprocess.check_output(['git', '-C', str(source), 'archive', head])
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(scratch, filter='data')

# The existing W24 assertions are unchanged. Only the disposable bench's
# entry point is replaced with a booted, stopped-output setup and extra probes.
main = scratch / 'tb/pp_top/sim_main.cpp'
original = main.read_text()
focus = r'''
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<Vpp_top_wrap> model;
  H h(model.get());
  Suite setup(h);
  setup.load_descriptor_image();
  h.reset();
  setup.boot_restore_over_blank_nvm();
  h.d->link_up_i = 1;
  h.d->entity_enable_i = 1;
  h.idle(1000);
  h.flush_all();
  ReadSidePhase phase{h, setup.image_ents};
  phase.w24_set_stream_info();
  std::printf("Existing W24: %d checks, %d failures\n", h.checks, h.fails);
  uint32_t expected_offset = 1000000;
  for (int len : {59, 60, 61, 95, 96, 97, 100, 140, 511}) {
    std::vector<uint8_t> p(size_t(len) - 12, 0);
    putbe(&p[0], 0x0006, 2);
    putbe(&p[4], 0x20000000u, 4);
    putbe(&p[24], uint32_t(600000 + len), 4);
    for (size_t i = 46; i < p.size(); ++i) p[i] = uint8_t(0xC1 + 7*i);
    const bool accepted = len == 60 || len == 96;
    if (accepted) expected_offset = 600000 + len;
    const unsigned writes = h.d->dbg_dyn_writes_o;
    const auto marks = h.nvm_marks;
    const auto notifications = h.notify_enqs;
    auto f = phase.ask(AEM_SET_STREAM_INFO, p, uint16_t(0x7E00 + len));
    std::vector<uint8_t> body(84, 0);
    if (len == 96) body = p;
    else if (len == 60) std::copy(p.begin(), p.begin()+46, body.begin());
    else putbe(&body[0], 0x0006, 2);
    auto expected = aecp_frame(CTLR_MAC, OWN_MAC, 1,
        accepted ? AECP_SUCCESS : AECP_BAD_ARGUMENTS, EID, CTLR_EID,
        uint16_t(0x7E00 + len), AEM_SET_STREAM_INFO, body);
    bool ok = f == expected && h.d->aecp_pt_offset_o.at(0) == expected_offset;
    if (!accepted) ok = ok && h.d->dbg_dyn_writes_o == writes
        && h.nvm_marks == marks && h.notify_enqs == notifications;
    std::printf("Boundary cdl %d status %d response_cdl %d offset %u writes %u: %s\n",
        len, f.empty() ? -1 : phase.st(f), phase.cdl(f),
        unsigned(h.d->aecp_pt_offset_o.at(0)),
        unsigned(h.d->dbg_dyn_writes_o - writes), ok ? "PASS" : "FAIL");
    if (!ok) ++h.fails;
  }
  AvbInfoPhase{h, h.d}.dispatch_cases();
  std::printf("Focused result: %d failures\n", h.fails);
  return h.fails ? 1 : 0;
}
'''
main.write_text(original[:original.index('int main(int argc, char** argv) {')] + focus)
(receipts / 'focus-bench.diff').write_text(''.join(difflib.unified_diff(
    original.splitlines(keepends=True), main.read_text().splitlines(keepends=True),
    fromfile='a/tb/pp_top/sim_main.cpp', tofile='b/tb/pp_top/sim_main.cpp')))

def run(name, cmd, cwd):
    # Build transcripts contain host support paths; only their hashes and
    # the unfiltered runtime receipts are publishable.
    directory = packet / 'scratch' if name.endswith('-build') else receipts
    with (directory / (name + '.log')).open('w') as log:
        rc = subprocess.run(cmd, cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
    (receipts / (name + '.rc')).write_text(str(rc) + '\n')
    print(name, 'rc', rc, flush=True)
    return rc

def campaign(suite, target, binary):
    cwd = scratch / 'tb' / suite
    mk = cwd / 'Makefile'
    mk.write_text(mk.read_text().replace('--build -j 0', '--build -j 8'))
    rc = run(suite + '-build', ['make', '-j16', target, 'VERILATOR=' + sim], cwd)
    if rc:
        return rc
    return run(suite + '-run', binary, cwd)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    tasks = [pool.submit(campaign, 'pp_top', 'gsi-build', ['./obj_dir/Vpp_top_sim']),
             pool.submit(campaign, 'aecp_cmds', 'build',
                 ['bash', '-c', './obj_dir/Vaecp_cmds obj_dir/observed.json && python3 -B check_observed.py obj_dir/observed.json'])]
    codes = [task.result() for task in tasks]
raise SystemExit(any(codes))
