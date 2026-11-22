# flexPTP (kebag-logic fork, branch gptp, d116d3d) compiled for the split CPU's ISA

riscv32-buildroot-linux-gnu-gcc 14.3.0 -march=rv32im -mabi=ilp32 -Os -ffunction-sections -fdata-sections, FLEXPTP_OSLESS, every port hook an extern stub (inc/flexptp_options.h below), each src/flexptp/*.c, servo/pid_controller.c and port/osless/*.c compiled alone (objects, not linked).

```
   text	   data	    bss	    dec	    hex	filename
     20	      0	      0	     20	     14	ptp_defs.o
     64	      0	      0	     64	     40	event.o
     68	      0	      0	     68	     44	cli_cmds.o
    220	      0	      0	    220	     dc	tlv.o
    267	     32	      0	    299	    12b	profiles.o
    296	    108	      0	    404	    194	logging.o
    334	      0	      0	    334	    14e	format_utils.o
    468	    220	      0	    688	    2b0	ptp_profile_presets.o
    588	      0	      0	    588	    24c	fifo.o
    620	      0	      0	    620	    26c	clock_utils.o
    636	      0	      0	    636	    27c	gptp_signaling.o
    708	      0	      0	    708	    2c4	stats.o
    716	      0	      0	    716	    2cc	config.o
    784	      0	      0	    784	    310	gptp_settings.o
    848	      1	     16	    865	    361	pid_controller.o
   1044	      0	    136	   1180	    49c	gptp_status.o
   1120	      0	      0	   1120	    460	gptp_rsync.o
   1136	      0	      0	   1136	    470	msg_buf.o
   1293	      0	      0	   1293	    50d	gptp_msg.o
   1328	      0	      0	   1328	    530	bmca.o
   1500	      0	      0	   1500	    5dc	gptp.o
   1904	      0	   1544	   3448	    d78	ptp_core.o
   1966	      0	      0	   1966	    7ae	timeutils.o
   1976	      0	      0	   1976	    7b8	settings_interface.o
   2232	      0	    408	   2640	    a50	common.o
   2864	      0	      0	   2864	    b30	msg_utils.o
   3004	      0	      0	   3004	    bbc	gptp_bmca.o
   3216	      0	   6773	   9989	   2705	task_ptp.o
   3232	      0	      0	   3232	    ca0	gptp_pdelay.o
   3656	      0	    648	   4304	   10d0	master.o
   3740	      0	      0	   3740	    e9c	slave.o
  41848	    361	   9525	  51734	   ca16	(TOTALS)
```

Undefined soft-float and libm symbols the objects reference (count of objects):

```
      5          U __muldf3
      5          U __divdf3
      3          U __subdf3
      3          U __adddf3
      2          U __truncdfsf2
      2          U exp
      1          U __ltdf2
      1          U log2
      1          U llround
      1          U __gtsf2
      1          U __gtdf2
      1          U __fixdfdi
      1          U __extendsfdf2
```

Global state: src/flexptp/ptp_core.c:37 `PtpCoreState gPtpCoreState;`, used through `#define S (gPtpCoreState)` in each core file (bmca.c:17, gptp.c:18, gptp_pdelay.c:26, ...).

The stub options header:

```c
/* bare-metal size probe: every port hook a no-op extern, no OS, no CLI */
#ifndef FLEXPTP_OPTIONS_H_
#define FLEXPTP_OPTIONS_H_
#include <stdint.h>
#include <stdio.h>
#define FLEXPTP_OSLESS (1)
extern void probe_lock(int);
#define FLEXPTP_OSLESS_LOCK (probe_lock)
#define PTP_ADDEND_INTERFACE
#define FLEXPTP_SNPRINTF(...) snprintf(__VA_ARGS__)
#define MSG(...) ((void)0)
#define CLILOG(en, ...) do { } while (0);
#define SPRINTF(str, n, ...) snprintf(str, n, __VA_ARGS__)
extern void probe_hw_init(uint32_t, uint32_t); extern void probe_set_clock(int32_t, int32_t);
extern void probe_set_addend(uint32_t); extern void probe_update_clock(int32_t, int32_t); extern void probe_get_time(void *);
#define PTP_MAIN_OSCILLATOR_FREQ_HZ (50000000)
#define PTP_INCREMENT_NSEC (20)
#define PTP_HW_INIT(i, a) probe_hw_init(i, a)
#define PTP_SET_CLOCK(s, ns) probe_set_clock(s, ns)
#define PTP_SET_ADDEND(a) probe_set_addend(a)
#define PTP_UPDATE_CLOCK(s, ns) probe_update_clock(s, ns)
#define PTP_HW_GET_TIME(pt) probe_get_time(pt)
#include <flexptp/servo/pid_controller.h>
#define PTP_SERVO_INIT() pid_ctrl_init()
#define PTP_SERVO_DEINIT() pid_ctrl_deinit()
#define PTP_SERVO_RESET() pid_ctrl_reset()
#define PTP_SERVO_RUN(d, pscd) pid_ctrl_run(d, pscd)
#endif
```
