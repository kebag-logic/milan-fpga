<!-- SPDX-License-Identifier: Apache-2.0 -->
The full delta contains C sources, host tests, build descriptions, and documentation.
No HDL, timing constraint, or hardware interface changes occur.
Both embedded source lists link and dispatch on the host; both freestanding checks pass.
No simulator was needed or invoked.
Parent reservation requirements keep hardware admission and bandwidth programming in integration scope.
The mailbox contract permits serialized event handling followed by receive and polling before another tick.
The review probes use serialized calls, no callback reentry, and no retained source output.
Normative assessment follows frozen public scope and interfaces; the complete standards texts were not available from the publisher landing pages.
