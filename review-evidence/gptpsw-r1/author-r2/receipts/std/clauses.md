# Clauses confirmed against the standards (round 2)

IEEE 802.1AS-2011, Annex B.2.3 Pdelay turnaround time:
> B.2.3 Pdelay turnaround time
> 
> The pdelay turnaround time is the duration of the interval between the receipt of a Pdelay_Req message by a
> port of a time-aware system, and the sending of the corresponding Pdelay_Resp message.
> 
> The pdelay turnaround time of a time-aware system, measured relative to the TAI frequency (see 8.2), shall
> be less than or equal to 10 ms.

Milan v1.2 (Consolidated, 2023-11-30), 4.2.6.2.6 Pdelay Turnaround Time:
> 4.2.6.2.6 Pdelay Turnaround Time
> 
> Per [802.1AS, Annex B.2.3], Pdelay turnaround time must be less than or equal to 10 ms. This requirement shall
> be relaxed by 50% resulting in a maximum Pdelay turnaround time of 15 ms.

Milan v1.2, 8.3.4 gPTP:
> 8.3.4 gPTP
> 
>    • The R-PAAD shall implement two gPTP time-aware end stations, one on the Primary AVB Interface and
>      another on the Secondary AVB Interface.
>    • The R-PAAD shall not implement a gPTP time-aware bridge between the Primary and Secondary AVB
>      Interfaces.
