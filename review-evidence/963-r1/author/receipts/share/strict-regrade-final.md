# aecp-largest-notice at 8x8/1if graded strictly, base dd163e41 against the final firmware 25d3dd7a

`run.py --regrade` on each run's log without `--record-share-findings`, so a work pass over THE SHARE fails the run; the rc is the run's exit status. The head's images are `50d3f10e`'s too (it changes a test only).

## base dd163e41, answering-ports: rc 1

    SHARE aecp-largest-notice: 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles); the longest 222,104 (2.221 ms)
    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## base dd163e41, declaring-outputs: rc 1

    SHARE aecp-largest-notice: 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles); the longest 227,112 (2.271 ms)
    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## head 25d3dd7a, answering-ports: rc 0

    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 0 of 106 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## head 25d3dd7a, declaring-outputs: rc 0

    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 0 of 106 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

