# backlog-owed.service.aecp.last.if0 at 8x8/1if: where its 0.1 ms went (64a473be, round 3's run; a6323318, this round's)

Both runs' backlog-owed.log (sha256 in round 3's and this round's 8x8-1if/LOGS.md). Cycles are 10 ns (100 MHz).

## 64a473be

Milestones (MARK lines): booted 6367484; composed 276803993; room 282809928; composed_end 283323572; 

The first four work passes after the release (`room`): pass, start less the release, cycles, gPTP modules' cycles:

    15897 -496 47784 none
    15898 47288 156753 gptp:1207 gptp_mbx:1127 
    15899 204041 36963 none
    15900 241004 32802 none

Run totals from the PASS lines (module, passes holding it, cycles):

    gptp 282 262879
    gptp_mbx 626 149287

## a6323318

Milestones (MARK lines): booted 6361863; composed 276808273; room 282814208; composed_end 283337806; 

The first four work passes after the release (`room`): pass, start less the release, cycles, gPTP modules' cycles:

    15879 6121 50020 gptp:835 gptp_mbx:1344 
    15880 56141 9802 none
    15881 65943 148126 none
    15882 214069 36899 none

Run totals from the PASS lines (module, passes holding it, cycles):

    gptp 282 271145
    gptp_mbx 626 214320

## Calls

The six functions the harness traces with CALL lines are called as often in both runs, and the passes that hold gptp (282) and gptp_mbx (626) are as many; gptp_mbx.c is unchanged between the heads, so its 65,033 more cycles are its placement against the caches, not more work.

## Placement

Text symbols (nm -n -S of image/ctrl_app.elf), the gPTP port and its adapter:

    gptp_port_rx: 00017f08 size 0000080c -> 00017f50 size 00000824
    gptp_port_ts: 00018714 size 00000310 -> 00018774 size 00000374
    gptp_port_tick: 00018a24 size 000002ec -> 00018ae8 size 000002ec
    gptp_mbx_words: 00018e94 size 00000058 -> 00018f58 size 00000058
    gptp_mbx_changes: 00018eec size 000000c8 -> 00018fb0 size 000000c8
    gptp_mbx_attach: 000194f4 size 000000fc -> 000195b8 size 000000fc
