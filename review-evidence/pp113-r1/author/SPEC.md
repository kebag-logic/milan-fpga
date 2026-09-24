[A280]

Directly checked Milan Specification, Consolidated v1.2, Final Approved 2023-11-30, Section 5.4.5.2 (printed page 62, PDF page 69) and Table 5.22 (printed page 63, PDF page 70).

The GET_STREAM_INFO row explicitly includes changes of MSRP accumulated latency for Stream Inputs. Its excerpt is quoted in PR-BODY.md.

Section 5.4.5.2 requires Table 5.22 notifications asynchronously when entity state changes. The one-per-descriptor-per-second restriction is in the GET_COUNTERS row, not GET_STREAM_INFO.

Source: the local standards PDF, Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf. Read its actual pages with pdftotext; no secondary interpretation used.
