.\" SPDX-FileCopyrightText: 2026 Kebag Logic
.\" SPDX-License-Identifier: CERN-OHL-W-2.0
.TL
[OBSOLETE + 2026-08-16]
.AU
Historical AEM and AECP fabric design
.PP
This PDF preserves the retired four-level fabric AEM memory and AECP state
machine design. It is not the current architecture or descriptor authority.
.PP
Current descriptor generation and deployment are documented in
docs/ENDSTATION_BUILDER.md. The protocol processor serves READ_DESCRIPTOR
from a builder-generated flat DRAM image that aemi-load verifies and writes
before entity enable.
.PP
Current implementation status and remaining Milan v1.2 gaps are recorded in
docs/testing/MILAN_V12_AUDIT_2026-08-16.md.
