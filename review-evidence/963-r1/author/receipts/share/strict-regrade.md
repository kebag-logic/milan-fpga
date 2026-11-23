# aecp-largest-notice at 8x8/1if graded strictly

`run.py --regrade` on each run's log without `--record-share-findings`, so a work pass over THE SHARE fails the run; the rc is the run's exit status.

## base dd163e41, answering-ports: rc 1

    SHARE aecp-largest-notice: 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles); the longest 222,104 (2.221 ms)
    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## base dd163e41, declaring-outputs: rc 1

    SHARE aecp-largest-notice: 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles); the longest 227,112 (2.271 ms)
    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 2 of 108 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## head b63c4179, answering-ports: rc 0

    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 0 of 106 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## head b63c4179, declaring-outputs: rc 0

    1 groups graded, 0 refusals, 0 budget misses (0 of 5 probe instances, 0 of 5 paths), 0 of 107 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

