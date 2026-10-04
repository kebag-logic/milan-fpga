cfg-read-live                            got=  1 readme=1 OK
cfg-dependent-field                      got= 14 readme=14 OK
cfg-dependent-field-top                  got=  9 readme=9 OK
cfg-frozen-at-top                        got=  4 readme=4 OK
cfg-overlay-only                         got=  6 readme=6 OK
cfg-nonzero-for-valid                    got=  3 readme=3 OK
cfg-valid-not-sticky                     got=  7 readme=7 OK
cfg-valid-any-selector                   got=  1 readme=1 OK
cfg-valid-ucpu-bus                       got=  3 readme=3 OK
cfg-valid-hard-reset                     got=  2 readme=2 OK
cfg-valid-no-reset                       got=  9 readme=5 DIFF
gate-enable-dropped                      got= 30 readme=30 OK
gate-enable-dropped-top                  got=  7 readme=3 DIFF
walk-down-answers-discover               got= 16 readme=16 OK
walk-delay-ignores-link-down             got=  4 readme=4 OK
walk-down-answers-gm-change              got=  8 readme=8 OK
walk-down-shutdown-departs               got=  1 readme=1 OK
walk-delay-answers-discover              got=  9 readme=9 OK
walk-delay-shutdown-silent               got=  4 readme=4 OK
walk-stale-draw-arms                     got=  4 readme=4 OK
walk-departing-keeps-index               got=  6 readme=6 OK
walk-foreign-discover-answered           got=  8 readme=8 OK
walk-link-down-keeps-timer               got=  3 readme=3 OK
disc-fresh-checks-gm                     got=  3 readme=3 OK
disc-not-discovered-checks-index         got= 14 readme=14 OK
disc-not-discovered-checks-interface     got=  3 readme=3 OK
disc-restart-not-rediscovered            got=  4 readme=4 OK
disc-departing-ignores-interface         got=  3 readme=3 OK
disc-stray-noadp-departs                 got=  2 readme=2 OK
disc-unbind-keeps-timer                  got=  2 readme=2 OK
arc-bind-keeps-discovered                got= 46 readme=46 OK
arc-discover-no-noadp-arm                got= 13 readme=13 OK
arc-not-discovered-no-guard              got= 14 readme=14 OK
arc-fresh-no-rearm                       got=  5 readme=5 OK
arc-restart-detector-off-by-one          got= 10 readme=10 OK
arc-restart-skips-guard                  got= 12 readme=12 OK
arc-departing-silent                     got=  4 readme=4 OK
arc-noadp-expiry-silent                  got=  4 readme=4 OK
36 of 38 arms match their README row
Reviewer note: the two DIFF rows are an artefact of reading only the leading number.
README row cfg-valid-no-reset states "(9 since lane P1's AD8 and AD9)" and row
gate-enable-dropped-top states "At the head of lane P1 it fails 7"; the campaign got
9 and 7. Result: 38 of 38 arms agree with their README rows.
