#!/usr/bin/env python3
"""Add independent map-status and malformed-record oracles in a disposable tree."""
import difflib
import os
from pathlib import Path
import shutil
import subprocess

p = Path(__file__).resolve().parent
src = p / 'scratch/source'
work = p / 'scratch/probe'
if not work.exists():
    shutil.copytree(src, work, symlinks=True)
path = work / 'tb/verilator/milan_dp/sim_nxn.cpp'
old = (src / 'tb/verilator/milan_dp/sim_nxn.cpp').read_text()
body = r'''
    void review_map_records() {
        const MapSet in = {{0, 6, 0, 0}, {0, 0, 3, 0}, {0, 1, 5, 0}};
        const MapSet out = {{0, 0, 7, 0}, {0, 4, 2, 0}};
        const MapSet id = identity_set(8);
        std::string why;
        bring_the_datapath_out_of_reset();
        axi_write(A_ADP_EIDHI, 0x020000FF);
        axi_write(A_ADP_EIDLO, 0xFE000001);
        ck("[REVIEW] initialize erased record window",
           static_cast<unsigned long>(load_the_saved_state_window(AEMI_CFG_C, {}, &why)), 1);
        std::vector<uint8_t> saved;
        std::map<uint32_t, std::pair<uint32_t, uint32_t>> at;
        ck("[REVIEW] codec frames valid saved maps",
           static_cast<unsigned long>(maprec_codec_window(
               {map_record(0x60, in, maprec_in_entries()),
                map_record(0x70, out, maprec_out_entries())}, &saved, &at)), 1);
        if (!at.count(0x60) || !at.count(0x70)) return;
        auto status = [&](const char* tag, bool failed, bool blank) {
            const uint32_t s = axi_read(A_PP_STAT);
            printf("[REVIEW-STATUS] %s PP_STAT=%08x done=%u fail=%u blank=%u map_fail=%u\n",
                   tag, s, (s >> 2) & 1u, (s >> 3) & 1u, (s >> 7) & 1u,
                   static_cast<unsigned>(dut->rootp->milan_datapath__DOT__amr_rs_fail_r));
            ck("[REVIEW] public restore failure agrees with map outcome", (s >> 3) & 1u,
               static_cast<unsigned>(failed));
            ck("[REVIEW] public blank agrees with records restored or lost", (s >> 7) & 1u,
               static_cast<unsigned>(blank));
        };
        nmem = saved;
        maprec_power_cycle("review saved maps", false);
        maprec_grade_both("review saved maps", in, out);
        status("saved", false, false);
        nm_err_lo = ((NVM_AREA_BASE + at[0x70].first) & ~7u) + 8u;
        nm_err_hi = (NVM_AREA_BASE + at[0x70].first + 8 + at[0x70].second) & ~7u;
        nmem = saved;
        maprec_power_cycle("review map device error", false);
        ck("[REVIEW] fault affected the parent map walk",
           static_cast<unsigned>(dut->rootp->milan_datapath__DOT__amr_rs_fail_r), 1);
        maprec_grade_both("review map device error", id, id);
        status("device-error", true, false);
        nm_err_lo = nm_err_hi = 0;

        const MapSet hole = {{0, 6, 0, 0}, {65535,65535,65535,65535}, {0,0,3,0}};
        const MapSet range = {{0, 6, 0, 0}, {0,8,3,0}};
        const MapSet duplicate = {{0, 6, 0, 0}, {0,1,0,0}};
        auto malformed = [&](const char* tag, const MapSet& set) {
            std::vector<uint8_t> area;
            std::map<uint32_t, std::pair<uint32_t, uint32_t>> offsets;
            ck("[REVIEW] codec frames malformed value with a valid CRC",
               static_cast<unsigned long>(maprec_codec_window(
                   {map_record(0x60, set, maprec_in_entries()),
                    map_record(0x70, out, maprec_out_entries())}, &area, &offsets)), 1);
            nmem = area;
            maprec_power_cycle(tag, false);
            maprec_grade_both(tag, id, out);
        };
        malformed("review hole refusal", hole);
        malformed("review range refusal", range);
        malformed("review duplicate refusal", duplicate);
        // A well-framed saved set may be illegal against a restored format.
        uint64_t fin = 0;
        current_channels(0x0005, 0, &fin);
        const uint64_t narrow = (fin & ~(0x3FFull << 22)) | (4ull << 22);
        char format_record[40];
        snprintf(format_record, sizeof format_record, "0x30=%016llx",
                 static_cast<unsigned long long>(narrow));
        std::vector<uint8_t> area;
        std::map<uint32_t, std::pair<uint32_t, uint32_t>> offsets;
        ck("[REVIEW] codec frames narrower format and incompatible saved map",
           static_cast<unsigned long>(maprec_codec_window(
               {format_record, map_record(0x60, in, maprec_in_entries()),
                map_record(0x70, out, maprec_out_entries())}, &area, &offsets)), 1);
        nmem = area;
        maprec_power_cycle("review refused ADD put-back", false);
        maprec_grade_both("review refused ADD put-back", identity_set(4), out);
    }

'''
text = old.replace('        dynmap_power_on_and_adaptation_section();', '')
text = text.replace('        dynmap_map_records_section();', '        review_map_records();')
needle = '    void dynmap_map_records_section() {'
assert text.count(needle) == 1
text = text.replace(needle, body + needle)
path.write_text(text)
(p / 'receipts/probe-harness.diff').write_text(''.join(difflib.unified_diff(
    old.splitlines(True), text.splitlines(True), fromfile='original/sim_nxn.cpp',
    tofile='probe/sim_nxn.cpp')))
env = dict(os.environ, TMPDIR=str(p / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
compiler = env.get('REVIEW_VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
command = ['make', '-j16', '-C', 'tb/verilator/milan_dp', 'dynmap',
           'VERILATOR=' + compiler, 'VERILATOR_JOBS=12']
with (p / 'receipts/probe-maps.log').open('w') as log:
    rc = subprocess.run(command, cwd=work, env=env, stdout=log,
                        stderr=subprocess.STDOUT, check=False).returncode
(p / 'receipts/probe-maps.rc').write_text(str(rc) + '\n')
print('Independent map probes rc', rc, flush=True)
