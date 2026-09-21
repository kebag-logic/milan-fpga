<!-- Draft by A151. Recorded on kebag-logic/milan-fpga #495 (the review-leftovers checklist). Documentation only. -->

# Docs: the saved-state page's area table for KL_nvm_backend predates the #484 contract

## Observed

`docs/design/SAVED_STATE_FASTCONNECT.md` section 8.3 lists `KL_nvm_backend`
at 772 LUT and 377 FF at the 1x1 bound (`N_NAME_P` 30). At dev `07294a76` the
tracked recipe returns 1,030 LUT, 0 LUTRAM, 468 FF, 6 DSP, 114 CARRY4 for the
same parameters:

    OOC_CHPARAM="N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_SPORT_IN_P=1 N_SPORT_OUT_P=1 \
                 N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1 N_NAME_P=30" syn/yosys/ooc.sh KL_nvm_backend

The snapshot-ownership contract of #484 grew the module (its page section 18
priced the prototype at 1,051 LUT and 476 FF). The shipped shapes also moved:
1x1 now carries 38 names (1,051 LUT, 476 FF) and 8x8 99 (1,476 LUT with 128
LUTRAM, 515 FF).

## Acceptance

Section 8.3's rows restated at the current source and the current name
bounds, with the recipe; the "above the candidate's bound" paragraph
re-derived.
