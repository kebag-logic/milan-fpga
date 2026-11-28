[A855]

## Status

The two repository gate repairs are ready for review. Merge remains blocked on the [100 Mb/s egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645): #1004 supplies the queue replay grader first, then this change adds the injected-frame and handshake terms. Board acceptance and attachment integration remain open.

## Description

The USB network path copies permitted frames and injects rate-limited best-effort traffic while preserving endpoint priority. Arty status LEDs follow the [fabric-level ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880). LD2 indicates any media-locked input or open output transmit gate. LD3 indicates internal selection, or a locked selected source; a selected stream also requires its input to be media-locked. There is no firmware LED register or LED code in the control image.

This update aligns the interface guide's Contents descriptions and corrects its service-budget section link. The octet-qualified receive-length parameter and every use were already present and remain unchanged. No firmware, gateware, scheduling row or owner bound changes.

## Validation

Both complete repository gate sequences pass. USB-network tests pass 92,755 checks, four clock-source command cases and all 72 named planted defects. Fresh Arty and both ALINX control ELFs and map headers are byte-identical to the #1004 comparison at identical dependency pins. Regenerated logic, constraints and memory initialization preserve the existing route evidence. The retained same-pin census remains CPU evidence only; it does not establish the pending wire-egress bound.

## Remaining acceptance

The 100 Mb/s grader and injected-path proof, physical controller/stream operation, LED observations, attachment integration, broader candidate gates and independent review remain outstanding. Existing whole-image crossing and external-I/O limitations remain. No physical release or issue completion is claimed.

Relates to #1011
Relates to #1018
