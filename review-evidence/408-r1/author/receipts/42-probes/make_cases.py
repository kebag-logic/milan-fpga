import json
from pathlib import Path
F = Path("$LANES/408-409-boot-gate-retire/sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
def rep(s, old, new, count=1):
    assert s.count(old) >= 1, old
    return s.replace(old, new, count)
VG = "#if defined(SPIFLASH_BASE) && defined(MILAN_AEM_FLASH_OFFSET)\n"
STUBFALSE = "#if defined(SPIFLASH_BASE) && defined(MILAN_AEM_FLASH_OFFSET) && !defined(MILAN_CENSUS_SOC)\n"
CMP = "\tif (got != MILAN_AEM_IMAGE_CRC32) {"
OKP = "\tprintf(\"Milan baremetal: AEM %u B copied"
UT = "\tprint_tod(gettime_ns());\n}"
AL = "static int aem_loaded;"
cases = {}
cases["H1a verifier condition false in the stub tree"] = rep(F, VG, STUBFALSE)
bypass = rep(rep(F, CMP, "\tgoto crc_ok;\n" + CMP), OKP, "crc_ok:\n" + OKP)
cases["H1b goto CRC bypass alone"] = bypass
cases["H1c verifier condition false in the stub tree + goto CRC bypass"] = rep(bypass, VG, STUBFALSE)
cases["H2 define inside the verifier first arm"] = rep(F, VG, VG + "#define MILAN_AEM_TRACE 1\n")
cases["H2b define inside the verifier other arm"] = rep(F, "#else\n\tprintf(\"Milan baremetal: no QSPI", "#else\n#define MILAN_AEM_TRACE 1\n\tprintf(\"Milan baremetal: no QSPI")
cases["H3 product-only arm redefining MILAN_ADP_CTRL"] = rep(F, "#define MILAN_ADP_CTRL       0x600u\n", "#ifdef CSR_UART_BASE\n#define MILAN_ADP_CTRL       0x604u\n#else\n#define MILAN_ADP_CTRL       0x600u\n#endif\n")
five = "".join(f"#ifdef MILAN_DEBUG_{k}\n#define MILAN_TRACE_{k} 1\n#endif\n" for k in range(5))
cases["H4 five independent groups (32 selections)"] = rep(F, AL, five + "\n" + AL)
cases["H5 whole store value hidden in a read accessor macro, UART handler"] = rep(rep(F, UT, "\tmilan_write(MILAN_ADP_CTRL, MILAN_ADP_ON_WORD());\n" + UT), AL, "#define MILAN_ADP_ON_WORD() (milan_read(MILAN_ADP_CTRL) | 1u)\n\n" + AL)
cases["H6 identity forged through a read accessor macro"] = rep(rep(F, "\tuint32_t id = milan_read(MILAN_ID);", "\tuint32_t id = MILAN_ID_READ();"), AL, "#define MILAN_ID_READ() (milan_read(MILAN_ID) * 0u + MILAN_ID_MAGIC)\n\n" + AL)
cases["A1 graded #ifdef/#else choosing a #define"] = rep(rep(F, AL, "#ifdef MILAN_DEBUG_BOOT\n#define MILAN_BOOT_TRACE 1\n#else\n#define MILAN_BOOT_TRACE 0\n#endif\n\n" + AL), UT, "\tif (MILAN_BOOT_TRACE)\n\t\tprintf(\"trace: tod\\n\");\n" + UT)
Path("cases.json").write_text(json.dumps(cases, indent=1))
print(len(cases))
