"""Build-time capture instrumentation; the shipping translation unit is input."""
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
    struct nvm_cap cap;

    milan_init();
    set_idle_hook(0);
    printf("CAPTURE_BOOT ready=%d raw=%u records=%u sys_hz=%u\\n",
           nvm_ready, (unsigned int)NVM_AREA_RAW, (unsigned int)NVM_N_REC,
           CONFIG_CLOCK_FREQUENCY);
    if (!nvm_ready) {
        printf("CAPTURE_FAILED boot\\n");
        return;
    }
    timer0_en_write(0);
    timer0_reload_write(0xffffffffu);
    timer0_load_write(0xffffffffu);
    timer0_en_write(1);
    for (capture = 0; capture < 1; ++capture) {
        probe_elapsed_cycles = 0;
        cap = nvm_capture();
        mismatches = 0;
        for (i = 0; i < NVM_AREA_RAW; ++i) {
            if (NVM_STG[KLJ2_HDR + i] != NVM_IMG[KLJ2_HDR + i])
                ++mismatches;
        }
        printf("CAPTURE index=%u ok=%d sys_cycles=%lu raw=%u records=%u mismatches=%u traffic=none\\n",
               capture, cap.ok, (unsigned long)probe_elapsed_cycles,
               (unsigned int)NVM_AREA_RAW, (unsigned int)NVM_N_REC, mismatches);
        milan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);
    }
    printf("CAPTURE_DONE\\n");
}

define_init_func(capture_probe_init);
'''


def prepare(root: Path, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    source = (root / 'sw/firmware/milan_baremetal/milan_baremetal.c').read_text()
    for before, after in (
        ('static struct nvm_cap nvm_capture(void)',
         TIMER + 'static struct nvm_cap nvm_capture(void)'),
        ('\tnvm_prefill_stage();',
         '\tnvm_prefill_stage();\n\tprobe_start_cycles = probe_timer_read();'),
        ('\tcap.ok = 1;\n\treturn cap;',
         '\tcap.ok = 1;\n\tprobe_elapsed_cycles = probe_start_cycles - probe_timer_read();\n\treturn cap;'),
        ('define_init_func(milan_init);', ''),
    ):
        if source.count(before) != 1:
            raise RuntimeError('capture instrumentation anchor is not unique: ' + before)
        source = source.replace(before, after)
    (destination / 'milan_baremetal.c').write_text(source + DRIVER)
    (destination / 'Makefile').write_bytes((root / 'sw/firmware/milan_baremetal/Makefile').read_bytes())
    return destination
