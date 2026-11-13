#!/bin/bash
# The harness at the final head, for the dispatcher: each leg's fresh build on its own clean clone at the head, one
# sample group, the image and the sample's log compared with the leg's build (8x8: 6c284a97's; 1x1: the sample build
# whose image is da1869a3's), then every recorded group of the leg regraded on the fresh build (sample33.sh); and the
# four cost controls run again at the head. usage: harness_queue34.sh HEAD > QUEUE
set -u
H=$1 T=/data-2/milan/tmp/665s2b-a683zo S=/data-2/milan/tmp/665s2b-a683zo/scripts
B=$T/builds
echo "X-GA8 10G /bin/bash $S/sample33.sh $T/L34-GA8 X-GA8 8x8 aecp $B/F-GA8 $B/F-GA8/results-merged"
echo "X-GN8 10G /bin/bash $S/sample33.sh $T/L34-GN8 X-GN8 8x8 notice-every-0 $B/F-GN8 $B/F-GN8/results --variant answering-every-port"
echo "X-GB8 8G /bin/bash $S/sample33.sh $T/L34-GB8 X-GB8 8x8 aecp $B/F-GB8 $B/F-GB8/results --groups aecp --variant answering-ports"
echo "X-GA1 8G /bin/bash $S/sample33.sh $T/L34-GA1 X-GA1 1x1 aecp $B/S-GA1 $B/S-GA1/results-head"
echo "X-GN1 8G /bin/bash $S/sample33.sh $T/L34-GN1 X-GN1 1x1 notice-every-0 $B/S-GN1 $B/S-GN1/results-head --variant answering-every-port"
echo "X-GB1 8G /bin/bash $S/sample33.sh $T/L34-GB1 X-GB1 1x1 aecp $B/S-GB1 $B/S-GB1/results-head --groups aecp --variant answering-ports"
echo "X-CTL1 8G /bin/bash $S/ctl.sh $T/L34-CTL1 $H notice-fan-out-as-it-was"
echo "X-CTL4 8G /bin/bash $S/ctl.sh $T/L34-CTL4 $H srp-compared-by-memcmp --variant answering-every-port"
echo "X-CTL2 8G /bin/bash $S/ctl.sh $T/L34-CTL2 $H polls-rebuild-in-the-base"
echo "X-CTL3 8G /bin/bash $S/ctl.sh $T/L34-CTL3 $H polls-rebuild-twice"
