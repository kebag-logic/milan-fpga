# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Bracket the shipping capture, including its record walk, on the product CPU."""
from pathlib import Path

TIMER = '''
static uint32_t probe_start_cycles;
static uint32_t probe_elapsed_cycles;

static uint32_t probe_timer_read(void)
{
    timer0_update_value_write(1);
    return timer0_value_read();
}

'''

DRIVER = '''
static void capture_probe_init(void)
{
    unsigned int capture;
    unsigned int i;
    unsigned int mismatches;
    unsigned int open;
    struct nvm_cap cap;

    milan_init();
    set_idle_hook(0);
    printf("CAPTURE_BOOT ready=%d raw=%u records=%u sys_hz=%u\\n",
           nvm_ready, (unsigned int)NVM_AREA_RAW, (unsigned int)NVM_N_REC,
           CONFIG_CLOCK_FREQUENCY);
    if (!nvm_ready || !(milan_read(MILAN_PP_CTRL) & 1u)) {
        printf("CAPTURE_FAILED boot\\n");
        return;
    }
    timer0_en_write(0);
    timer0_reload_write(0xffffffffu);
    timer0_load_write(0xffffffffu);
    timer0_en_write(1);
    probe_enable_write(1);
    for (capture = 0; capture < PROBE_CAPTURES; ++capture) {
        probe_elapsed_cycles = 0;
        cap = nvm_capture();
        mismatches = 0;
        open = 0;
        for (i = 0; i < NVM_OWN_WORDS; ++i)
            open |= nvm_word_read(NVM_W_OWN0 + i);
        for (i = 0; i < NVM_AREA_RAW; ++i) {
            if (NVM_STG[KLJ2_HDR + i] != NVM_IMG[KLJ2_HDR + i])
                ++mismatches;
        }
        printf("CAPTURE index=%u ok=%d sys_cycles=%lu raw=%u records=%u "
               "mismatches=%u open=%u requests=%lu responses=%lu reads=%lu\\n",
               capture, cap.ok, (unsigned long)probe_elapsed_cycles,
               (unsigned int)NVM_AREA_RAW, (unsigned int)NVM_N_REC, mismatches, open,
               (unsigned long)probe_requests_read(), (unsigned long)probe_responses_read(),
               (unsigned long)probe_reads_read());
        milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
    }
    probe_enable_write(0);
    printf("CAPTURE_DONE\\n");
}

define_init_func(capture_probe_init);
'''


def prepare(root: Path, destination: Path, mutation: str) -> Path:
    """Copy, never edit, product firmware; reject drift of instrumentation anchors."""
    destination.mkdir(parents=True, exist_ok=True)
    source = (root / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()
    replacements = (
        ('static struct nvm_cap nvm_capture(void)', TIMER + 'static struct nvm_cap nvm_capture(void)'),
        ('\tnvm_prefill_stage();',
         '\tnvm_prefill_stage();\n'
         '\t/* Poison every byte before timing so equality proves the copy ran. */\n'
         '\tfor (i = 0; i < NVM_AREA_RAW; ++i)\n'
         '\t\tNVM_STG[KLJ2_HDR + i] = NVM_IMG[KLJ2_HDR + i] ^ 0xffu;\n'
         '\tprobe_start_cycles = probe_timer_read();'),
        ('\trec = nvm_rec_after(-1);\n\twhile (rec.ok)',
         '\tprobe_active_write(1);\n\trec = nvm_rec_after(-1);\n\twhile (rec.ok)'),
        ('\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ATTEST);',
         '\tprobe_active_write(0);\n\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ATTEST);'),
        ('\tcap.ok = 1;\n\treturn cap;',
         '\tcap.ok = 1;\n\tprobe_elapsed_cycles = probe_start_cycles - probe_timer_read();\n\treturn cap;'),
        ('define_init_func(milan_init);', ''),
    )
    for before, after in replacements:
        if source.count(before) != 1:
            raise RuntimeError('capture instrumentation anchor is not unique: ' + before)
        source = source.replace(before, after)
    if mutation == 'skip-copy':
        store = 'NVM_STG[KLJ2_HDR + i] = NVM_IMG[KLJ2_HDR + i];'
        if source.count(store) != 1:
            raise RuntimeError('copy mutation anchor is not unique')
        source = source.replace(store, '(void)NVM_IMG[KLJ2_HDR + i];')
    driver = DRIVER.replace('probe_enable_write(1);', 'probe_enable_write(0);') if mutation == 'no-traffic' else DRIVER
    (destination / 'milan_baremetal.c').write_text(source + driver)
    (destination / 'Makefile').write_bytes((root / 'sw/firmware/milan_baremetal/Makefile').read_bytes())
    return destination
