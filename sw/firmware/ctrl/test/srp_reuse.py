# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Cut the processor's SRP wire builders and table oracle from verified blobs."""
from pathlib import Path
from ctrl_build import PP, Refusal
from ctrl_reuse import git, cut

FILES=("tb/srp_top/sim_main.cpp","tb/srp_stream_fsms/sim_main.cpp")

def cut_srp(dest: Path) -> Path:
    """Verify both suite blobs and extract their wire and table fixtures."""
    record=git("ls-files","-s","--","protocol-processor").split()
    if len(record)!=4 or record[0]!="160000" or record[2]!="0":
        raise Refusal("processor is not one stage-0 gitlink")
    pin=record[1]
    if git("rev-parse","HEAD",cwd=PP)!=pin:
        raise Refusal("processor is not at its pin")
    out=["// SPDX-License-Identifier: CERN-OHL-W-2.0",
         "// Generated from the pinned processor suites; do not edit.",
         "#pragma GCC diagnostic push", '#pragma GCC diagnostic ignored "-Wunused-function"',
         "namespace processor_wire {"]
    for name in FILES:
        blob=git("ls-tree",pin,name,cwd=PP).split()
        if len(blob)!=4 or git("hash-object",name,cwd=PP)!=blob[2]:
            raise Refusal(f"SRP stimulus differs from its pinned blob: {name}")
        out.append(f"// {name}: commit {pin}, blob {blob[2]}")
        lines=(PP/name).read_text().splitlines()
        if name==FILES[0]:
            out+=cut(lines,"SRP constants and independent wire builders",
                     "constexpr int         MS_CYC", "struct H {",False)
        else:
            out+=cut(lines,"SRP applicant table and messages","constexpr int VO =", "constexpr const char* SN",False)
    out += ["}","#pragma GCC diagnostic pop", ""]
    dest.mkdir(parents=True,exist_ok=True)
    p=dest/"pp_srp_reuse.inc";p.write_text("\n".join(out));return p
