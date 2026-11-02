### A save in a composed window, and both links at once

This subsection is the record of 2026-11-02 (#665, round 13); the one above is the record of round 12's head, `c954b8a9`.
Two passes the round 12 groups never staged were over the share at that head.
In a pass that also carried a composed window's heaviest work, the saved-state store's flash step took the pass to {x_save} ms (`backlog`'s window, 3 of 6 tick phases over) and {y_save} ms (`backlog-adp`'s, 7 of 8 over).
With both links changing together, SRP built both interfaces in one pass of {y_links} ms.
No row missed its bound in either: the closest was the last SRP record, {y_save_srp} ms against 18.

**The store's steps on the product SoC.**
One save with no other load (`save_window.py`'s `save` group), the CPU on `sys` at 100 MHz, through the product's uncached flash window and its command master, CPU cycles a step:

{steps_table}

A read-back step reads 128 bytes through the uncached window, one SPI read a byte; a program step issues one page, 261 bytes through the command master one at a time.
The program's issue is the longest step, {program_max} cycles at 8x8.
Beside the heaviest pass the other slices make, {heaviest} ms at 8x8/2if, any of the flash steps took a pass past the share, so no smaller read-back fixes it alone.

**THE STEP.**
The loop now owns the pass's time (`ctrl_loop.h`, THE STEP): it reads the store's clock once as a pass starts, and after the polls hands the store's step the clock's value at which the pass has spent the share.
The store's centisecond consumer only owes a step; the step is taken only while `NVM_STEP_US`, 1.0 ms, is left before that deadline, so a pass that carries a step has at most 1.0 ms of other work and at most the step's own cost, the program's {program_ms} ms at its longest.
A step without room stays owed, the loop passes again at once, and the first pass with room takes it; the centiseconds that pass meanwhile owe it once, so the store never takes two steps in one pass or catches up in a burst.
The harness now holds every pass to the share, those that write nothing to the mailbox too, by their run's longest, since a deferred step can be all such a pass does.

**A save in each flash phase.**
`save_window.py` opens `backlog-adp`'s window, the heaviest the harness stages, during each flash phase of a save, at eight phases of that phase's heavy step: 1.25 ms apart across the 10 ms tick for the blank check and the verify, 2.5 ms apart across the program phase's 20 ms.
Each phase starts at a flash event of the save itself, and `grade.save_phase` refuses a window that did not open inside it.
The 24 windows ran at both points, in both arms, with the two drafts staged and without them: {save_share}
The longest pass that carries a flash step in any of them is {step_pass} ms.
Their rows (ms, arm A / arm B, bold over the row's own bound):

{save_rows}

{save_rows_text}

**The planted store step.**
`--mutation store-step-unbounded` hands the step a deadline no pass reaches, so the store steps in whatever pass owes it, as before THE STEP.
At 8x8 it puts {ctl_over} passes over the share, the longest {ctl_longest} ms, while every row fits its bound, the last SRP record {ctl_srp} ms against 18, and the run prints `CONTROL store-step-unbounded caught`.

**A save from the change to durable.**
The time from a SET_NAME to the read-back that moves the authority, at 8x8, one save with no other load, on the harness's flash model, which has no busy time: {durable_before} at round 12's head, {durable_after} at this head.
At 1x1 it is {durable_1x1}.
The first 1,000 ms are DR2a's first-dirty window; the read-back is 128 bytes a step, {readback_ticks} ticks at 8x8 for the blank check and the verify together, where a whole page a step took half as many.
A real part's erase and page-program waits add to it; the store polls them, a step a tick.
The owner's 0.5 s ([#823](https://github.com/kebag-logic/milan-fpga/issues/823)) is the append-only design's in Mark II, not this image's, and this round does not claim it.

**Both links at once.**
A poll now builds one interface at most (`srp_bounds.h`): the other is built on the next pass, and the interface whose build waited goes first after that.
`y-links`, both links dropping under `backlog-adp`'s load, and `x-links-same` under `backlog`'s, at 8x8 in both arms: {links}

**The rows at this head.**
The four backlog windows, every leg rebuilt at this head (ms, arm A / arm B, bold over the row's own bound):

{rows}

{share}

**The boot simulation's flash window.**
The split boot simulation now builds the product's uncached flash window, and refuses an export without it.
At round 12's head the window alone moves the boot to ready from 24.660 to 25.413 ms at 1x1 and from 64.271 to 65.026 ms at 8x8; at this head it is {boot_1x1} and {boot_8x8} ms ([the boot simulation](../../tb/verilator/ctrl_split_boot/README.md#results)).
