#!/bin/bash
# Usage: mutants2.sh <probe-tree> <receipt-dir>: the second batch, with mutants.sh's mut() (sourced).
T=$1; R=$2
source <(sed -n '/^mut() {/,/^}/p' "$(dirname "$0")/mutants.sh")
cd "$T" || exit 2
mut MF-ring-512-words sw/mailbox/gen_mailbox.py 'return max(acmp.tx_words, 1 << max(0, need - 1).bit_length())' 'return max(acmp.tx_words, 512)'
mut MG-shape-findings-off sw/mailbox/gen_mailbox.py '    if acmp_tx_records(variant) < sinks:' '    if False:'
