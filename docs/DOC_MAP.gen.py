#!/usr/bin/env python3
"""Generate the milan-fpga documentation map ("where do I start?") as both an
editable .drawio and a rendered .svg. Four persona lanes, each an ordered
reading journey; a universal entry at the top and shared references at the
bottom. Style matches SYSTEM_DOMAIN_MAP.gen.py (pastel fill + darker stroke,
rounded, header + subtitle). Render PNG with: rsvg-convert -w 2000 DOC_MAP.svg -o DOC_MAP.png
"""
import html, sys

# palette (fill, stroke, accent-for-number-chip)
BLUE   = ("#E3F2FD", "#1565C0")
GREEN  = ("#E8F5E9", "#2E7D32")
ORANGE = ("#FFF3E0", "#EF6C00")
PURPLE = ("#F3E5F5", "#6A1B9A")
GREY   = ("#ECEFF1", "#455A64")
GOLD   = ("#FFF8E1", "#F9A825")

def esc(s): return html.escape(s, quote=True)

# ---- each persona: (name, who-you-are, your-goal, colour, [ (doc, blurb) ... ]) ----
PERSONAS = [
 ("Developer", "you write RTL / gateware / firmware",
  "add or change a module in the fabric", BLUE, [
   ("SYSTEMS_ENGINEER_GUIDE.md", "orient: what the system is + the doc map"),
   ("overview/ARCHITECTURE.md", "the developer guide — §8 'where to change things'"),
   ("ARCHITECTURE_HW_SW_SPLIT.md", "does your feature belong in fabric or the softcore?"),
   ("fpga/FPGA_DESIGN.md", "the hdl/ module map + which TB verifies each"),
   ("reference/REGISTER_MAP.md", "the CSR/AXI-Lite ABI shared by RTL + driver + DT"),
   ("testing/TESTING.md  +  tb/verilator/", "build + run the unit TBs for your change"),
 ]),
 ("System Engineer", "you reason about the whole system",
  "understand it + assess compliance & roadmap", GREEN, [
   ("SYSTEMS_ENGINEER_GUIDE.md", "the single best starting doc — read first"),
   ("ARCHITECTURE_HW_SW_SPLIT.md", "normative plan of record: fabric vs softcore"),
   ("overview/SYSTEM_DOMAIN_MAP.md", "every module by domain/language, one picture"),
   ("SPEC_TRACEABILITY.md", "IEEE/Milan clause → module → test, with status"),
   ("MILAN_COMPLIANCE_GAPS.md", "what is + isn't compliant, honest gaps"),
   ("GitHub Issues", "the live roadmap + open gaps, tracked as issues"),
 ]),
 ("Integrator", "you make it RUN on hardware",
  "build → flash → bring up the board", ORANGE, [
   ("sw/README.md", "toolchain: riscv64-elf, jdk+sbt, the litex venv"),
   ("integration/BUILDING.md", "build.sh: configs, parallel discipline, gates"),
   ("litex/LITEX_SOC.md  §4", "the mandatory, non-obvious build flags + why"),
   ("integration/QSPI_FLASHBOOT.md", "flash layout, COMPRESS, matched image set"),
   ("findings/BENCH_TOPOLOGY.md", "reach the boards · power · taps · recovery"),
   ("limitations/TROUBLESHOOTING.md", "when boot / flash / link goes wrong"),
 ]),
 ("Tester / Validator", "you run the suites + validate",
  "prove it works, per spec", PURPLE, [
   ("testing/TESTING.md", "the test taxonomy: TB · behave · CERT/bench"),
   ("tb/verilator/README.md", "run every Verilator TB (ls = 41 suites)"),
   ("tests/README.md", "run the behave/tsn_gen fixtures (venv + TSAGEN_DIR)"),
   ("testing/BEHAVE_TEST_PLAN.md", "the tag taxonomy, tiers, @bench / CERT"),
   ("SPEC_TRACEABILITY.md", "read the pass / partial / fail matrix (204 rows)"),
   ("MILAN_COMPLIANCE_GAPS.md", "what is validated vs pending"),
 ]),
]

# ---- geometry ----
X0, Y0 = 40, 150
COLW, COLGAP = 430, 26
HDR = 92                    # persona header height (name / who / goal stacked)
SH, SGAP = 62, 26          # step box height / vertical gap (gap holds the arrow)
TOP_H = 60                  # universal-entry banner height
NUMR = 15                   # number chip radius

ncols = len(PERSONAS)
maxsteps = max(len(p[4]) for p in PERSONAS)
col_x = lambda i: X0 + i*(COLW+COLGAP)
W = col_x(ncols-1) + COLW + X0
steps_top = Y0 + TOP_H + 34 + HDR + SGAP
bottom_y = steps_top + maxsteps*(SH+SGAP) + 20
H = bottom_y + 150

def svg():
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">']
    o.append(f'<rect width="{W}" height="{H}" fill="#FAFAFA"/>')
    # title
    o.append(f'<text x="{X0}" y="56" font-size="30" font-weight="bold" fill="#263238">milan-fpga documentation — where do I start?</text>')
    o.append(f'<text x="{X0}" y="88" font-size="15" fill="#546E7A">Pick your lane. Each column is an ordered reading journey, top to bottom. Boxes are clickable doc paths under <tspan font-weight="bold">docs/</tspan> (or the repo).</text>')
    o.append(f'<text x="{X0}" y="112" font-size="15" fill="#546E7A">New to the project? Read the universal entry first, then follow your lane.</text>')

    # universal entry banner
    bx, bw = X0, W-2*X0
    o.append(f'<rect x="{bx}" y="{Y0}" width="{bw}" height="{TOP_H}" rx="10" fill="{GOLD[0]}" stroke="{GOLD[1]}" stroke-width="2.5"/>')
    o.append(f'<text x="{bx+22}" y="{Y0+26}" font-size="16" font-weight="bold" fill="#212121">★ Everyone starts here — docs/SYSTEMS_ENGINEER_GUIDE.md</text>')
    o.append(f'<text x="{bx+22}" y="{Y0+48}" font-size="13.5" fill="#5D4037">what the system is + a journey-ordered map of the whole doc set. Then jump into your lane below. Unsure of a term? → docs/GLOSSARY.md</text>')

    def numchip(cx, cy, n, stroke):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{NUMR}" fill="{stroke}"/>')
        o.append(f'<text x="{cx}" y="{cy+5}" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">{n}</text>')

    for i,(name,who,goal,(fill,stroke),steps) in enumerate(PERSONAS):
        x = col_x(i)
        # header
        hy = Y0 + TOP_H + 34
        o.append(f'<rect x="{x}" y="{hy}" width="{COLW}" height="{HDR}" rx="10" fill="{stroke}" stroke="{stroke}" stroke-width="2"/>')
        o.append(f'<text x="{x+20}" y="{hy+31}" font-size="21" font-weight="bold" fill="#ffffff">{esc(name)}</text>')
        o.append(f'<text x="{x+20}" y="{hy+55}" font-size="13" fill="#ffffff" fill-opacity="0.92">{esc(who)}</text>')
        o.append(f'<text x="{x+20}" y="{hy+79}" font-size="13.5" fill="#ffffff"><tspan font-style="italic" fill-opacity="0.85">goal:  </tspan><tspan font-weight="bold">{esc(goal)}</tspan></text>')
        # steps
        for j,(doc,blurb) in enumerate(steps):
            sy = steps_top + j*(SH+SGAP)
            # connector arrow from previous box
            if j>0:
                ax = x+COLW//2; ay0 = sy-SGAP; ay1 = sy
                o.append(f'<path d="M{ax} {ay0} L{ax} {ay1-3}" stroke="{stroke}" stroke-width="2" marker-end="url(#arr)"/>')
            o.append(f'<rect x="{x}" y="{sy}" width="{COLW}" height="{SH}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
            numchip(x+26, sy+SH//2, j+1, stroke)
            o.append(f'<text x="{x+52}" y="{sy+25}" font-size="14.5" font-weight="bold" fill="#212121">{esc(doc)}</text>')
            o.append(f'<text x="{x+52}" y="{sy+46}" font-size="12.8" fill="#37474F">{esc(blurb)}</text>')

    # arrow marker
    o.insert(1, '<defs><marker id="arr" markerWidth="12" markerHeight="12" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#607D8B"/></marker></defs>')

    # shared-references footer
    fy = bottom_y
    o.append(f'<rect x="{X0}" y="{fy}" width="{W-2*X0}" height="96" rx="10" fill="{GREY[0]}" stroke="{GREY[1]}" stroke-width="2"/>')
    o.append(f'<text x="{X0+22}" y="{fy+28}" font-size="16" font-weight="bold" fill="#212121">Shared references — every lane comes back to these</text>')
    refs = ["reference/REGISTER_MAP.md — the CSR ABI", "GLOSSARY.md — every term",
            "SPEC_TRACEABILITY.md — clause→module→test", "findings/ — dated bug post-mortems",
            "DOC_AUDIT.md — doc freshness tracker"]
    rw = (W-2*X0-44)//len(refs)
    for k,r in enumerate(refs):
        rx = X0+22+k*rw
        o.append(f'<rect x="{rx}" y="{fy+42}" width="{rw-14}" height="38" rx="6" fill="#ffffff" stroke="{GREY[1]}" stroke-opacity="0.6"/>')
        d,b = r.split(" — ")
        o.append(f'<text x="{rx+12}" y="{fy+60}" font-size="12" font-weight="bold" fill="#212121">{esc(d)}</text>')
        o.append(f'<text x="{rx+12}" y="{fy+75}" font-size="11.5" fill="#546E7A">{esc(b)}</text>')

    o.append('</svg>')
    return "\n".join(o)

def drawio():
    cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']; cid=[1]
    def add(x,y,w,h,label,fill,stroke,fs=13,fw=0,align="left",font="#212121"):
        cid[0]+=1; i=cid[0]
        style=(f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
               f"fontSize={fs};align={align};verticalAlign=top;spacingLeft=10;spacingTop=6;fontColor={font};"
               + ("fontStyle=1;" if fw else ""))
        cells.append(f'<mxCell id="n{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return f"n{i}"
    add(X0,20,1100,34,"milan-fpga documentation — where do I start?","none","none",22,1)
    add(X0,Y0,W-2*X0,TOP_H,"★ Everyone starts here — docs/SYSTEMS_ENGINEER_GUIDE.md\n(what the system is + a journey-ordered doc map; then follow your lane)",GOLD[0],GOLD[1],14,1)
    for i,(name,who,goal,(fill,stroke),steps) in enumerate(PERSONAS):
        x=col_x(i); hy=Y0+TOP_H+34
        add(x,hy,COLW,HDR,f"{name}\n{who}  ·  goal: {goal}",stroke,stroke,15,1,font="#ffffff")
        for j,(doc,blurb) in enumerate(steps):
            sy=steps_top+j*(SH+SGAP)
            add(x,sy,COLW,SH,f"{j+1}.  {doc}\n{blurb}",fill,stroke,13,0)
    add(X0,bottom_y,W-2*X0,96,"Shared references — every lane comes back to these\n\nreference/REGISTER_MAP.md · GLOSSARY.md · SPEC_TRACEABILITY.md · findings/ · DOC_AUDIT.md",GREY[0],GREY[1],13,1)
    body="\n".join(cells)
    return (f'<mxfile host="app.diagrams.net"><diagram name="doc-map">'
            f'<mxGraphModel dx="1400" dy="1000" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" '
            f'math="0" shadow="0"><root>{body}</root></mxGraphModel></diagram></mxfile>')

base=sys.argv[1] if len(sys.argv)>1 else "DOC_MAP"
open(base+".svg","w").write(svg())
open(base+".drawio","w").write(drawio())
print("wrote", base+".svg", "and", base+".drawio")
