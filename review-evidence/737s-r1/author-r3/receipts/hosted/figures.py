"""Every round 3 elaboration figure from the component maxima, under the ruling on the STOP (#737, option (d))."""
rows = {  # member verdict rows in a LiteX leg on a worker of its own (receipts / job logs)
    "41583428850": dict(cpu=70, ctrl=280, gmii=0, gptp=461, boot=25, mem=14, retained=331, soc=240),
    "41678609075 a1": dict(cpu=72, ctrl=224, gmii=0, gptp=246, boot=25, mem=15, retained=336, soc=369),
    "41678609075 a3": dict(cpu=71, ctrl=284, gmii=0, gptp=462, boot=25, mem=14, retained=333, soc=510),
}
largest = {k: max(r[k] for r in rows.values()) for k in rows["41583428850"]}
legs = [["gptp"], ["cpu", "gmii", "boot", "mem", "retained"], ["ctrl", "soc"]]
held = [sum(largest[m] for m in leg) for leg in legs]
JOB, HEAD, SETUP, VERILATOR, SELFTEST = 2700, 600, 485, 431, 3
LEG0, LEG1 = 1130, 1119
budget = JOB - HEAD - SETUP - VERILATOR - SELFTEST
agg = 19 + 85; allowance = agg + 149 + 120 + 25
print("largest", largest)
print("LEG_BUDGET", budget, "legs at largest", held, "fit", all(h <= budget for h in held))
proj = {"elaborate-gates-0": SETUP + LEG0, "elaborate-gates-1": SETUP + LEG1}
for i, h in enumerate(held):
    proj[f"elaborate-gates-{i + 2} (cold)"] = SETUP + VERILATOR + SELFTEST + h
for k, v in proj.items():
    print(f"{k:28} {v:5} against {JOB}, margin {JOB - v}")
print("warm LiteX", [SETUP + SELFTEST + h for h in held])
print("aggregate", agg, "margin under 180:", 180 - agg, "allowance", allowance)
warm = max(proj["elaborate-gates-0"], proj["elaborate-gates-1"], *(SETUP + SELFTEST + h for h in held))
cold = max(proj.values())
print("workflow warm", warm + allowance, f"({(warm + allowance) / 60:.2f} min)", "cold", cold + allowance,
      f"({(cold + allowance) / 60:.2f} min)", "with the former 338 allowance", warm + 338)
