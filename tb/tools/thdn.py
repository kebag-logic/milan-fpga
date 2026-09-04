# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! THD+N on a coherently-sampled pilot tone.
#!
#! **NO WINDOW.** The pilot tone is exact-period - 48 samples = 1 kHz at
#! 48 kHz - so a capture truncated to an integer number of periods is
#! coherently sampled and its FFT has no leakage to suppress. Applying a window
#! to a coherent tone spreads the fundamental across neighbouring bins, which
#! the residual then counts as distortion: it does not clean up the
#! measurement, it MANUFACTURES the number it is supposed to measure. The
#! reference result on this bench is -147.99 dBFS; a windowed analysis of the
#! same capture cannot reach it.
#!
#! The method is therefore: truncate to whole periods, un-windowed real FFT,
#! remove DC and the fundamental bin (plus the two bins either side, which hold
#! only the fundamental's own numerical skirt), and take the residual RMS
#! against the fundamental's amplitude.
#!
#! `numpy` is required here and nowhere else in this analyser. Protocol and
#! identity checks can run without it; only the measured THD+N step needs it.

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

# PEP 563 is in force above, so this name is wanted by a type checker and never
# at run time - numpy stays imported inside the two functions that need it.
if TYPE_CHECKING:
    from numpy.typing import ArrayLike


class ThdnError(Exception):
    pass


@dataclass(frozen=True)
class ThdnResult:
    channel: int
    thdn_dbfs: float          # residual RMS relative to the fundamental, dB
    fundamental_dbfs: float   # fundamental level relative to full scale, dB
    f0_hz: float
    bins_used: int
    samples_used: int
    periods: int
    dc_dbfs: float
    clipped: bool

    def as_dict(self) -> dict:
        """The measurement flattened for serialisation, conditions included.

        Every field travels, not just `thdn_dbfs`: a number reported without
        the periods, bins and clipping flag it was taken under cannot be
        compared with the next run's.
        """
        return asdict(self)


def decode_s32be(raw: bytes, channels: int) -> "list":
    """De-interleave S32_BE PCM into per-channel float arrays in [-1, 1).

    The capture card produces S32_BE and cannot use a WAV container, so there
    is no header to parse and no format to sniff: the caller states the layout
    and this asserts the length is consistent with it.
    """
    import numpy as np

    if channels < 1:
        raise ThdnError("channels must be >= 1")
    frame = 4 * channels
    if len(raw) < frame:
        raise ThdnError(f"capture is {len(raw)} bytes, shorter than one frame")
    usable = (len(raw) // frame) * frame
    arr = np.frombuffer(raw[:usable], dtype=">i4").astype(np.float64)
    arr = arr.reshape(-1, channels) / 2147483648.0
    return [arr[:, c] for c in range(channels)]


def analyse(samples: ArrayLike, *, rate_hz: int, f0_hz: int,
            channel: int = 0) -> ThdnResult:
    """THD+N of one channel. `samples` is a 1-D float array in [-1, 1)."""
    import numpy as np

    x = np.asarray(samples, dtype=np.float64)
    if x.ndim != 1:
        raise ThdnError("analyse() takes one channel at a time")
    if rate_hz % f0_hz:
        raise ThdnError(
            f"{rate_hz} Hz / {f0_hz} Hz is not an integer number of samples per "
            f"period - the tone is not exact-period, so the capture is not "
            f"coherently sampled and this un-windowed method does not apply")
    period = rate_hz // f0_hz
    periods = len(x) // period
    if periods < 8:
        raise ThdnError(
            f"only {periods} whole tone periods in the capture; need >= 8 for a "
            f"meaningful residual")
    n = periods * period
    x = x[:n]

    clipped = bool(np.max(np.abs(x)) >= 0.99999)

    # Un-windowed real FFT. Coherent sampling puts the fundamental entirely in
    # bin `periods`, with no window and no leakage correction.
    spec = np.fft.rfft(x)
    mag = np.abs(spec)
    k0 = periods
    if k0 >= len(mag):
        raise ThdnError("fundamental bin lies outside the spectrum")

    # Scale so a full-scale sine reads 0 dBFS.
    scale = 2.0 / n
    fund = mag[k0] * scale
    dc = mag[0] / n

    resid = mag.copy()
    # DC, the fundamental, and one bin either side (pure numerical skirt of the
    # fundamental itself - keeping them would report the FFT's own rounding as
    # distortion).
    for k in (0, k0 - 1, k0, k0 + 1):
        if 0 <= k < len(resid):
            resid[k] = 0.0

    # Parseval on the one-sided spectrum: interior bins count twice.
    power = resid[0] ** 2 + resid[-1] ** 2 if n % 2 == 0 else resid[0] ** 2
    power += 2.0 * float(
        np.sum(resid[1:len(resid) - (1 if n % 2 == 0 else 0)] ** 2))
    resid_rms = math.sqrt(power) / n * math.sqrt(2.0)

    if fund <= 0.0:
        raise ThdnError(
            "no fundamental found - is the pilot tone enabled (TONE_CTRL[0])?")

    thdn_db = 20.0 * math.log10(max(resid_rms, 1e-300) / fund)
    return ThdnResult(
        channel=channel,
        thdn_dbfs=thdn_db,
        fundamental_dbfs=20.0 * math.log10(max(fund, 1e-300)),
        f0_hz=float(f0_hz),
        bins_used=len(mag),
        samples_used=n,
        periods=periods,
        dc_dbfs=20.0 * math.log10(max(dc, 1e-300)),
        clipped=clipped,
    )


def analyse_capture(raw: bytes, *, rate_hz: int, f0_hz: int,
                    channels: int) -> list[ThdnResult]:
    """Every channel of one raw S32_BE capture."""
    return [analyse(ch, rate_hz=rate_hz, f0_hz=f0_hz, channel=i)
            for i, ch in enumerate(decode_s32be(raw, channels))]


def verdict(results: list[ThdnResult], accept_dbfs: float) -> tuple[bool, str]:
    """Pass/fail over all channels, worst channel named."""
    if not results:
        return (False, "no channels analysed")
    worst = max(results, key=lambda result: result.thdn_dbfs)
    if worst.clipped:
        return (False, f"channel {worst.channel} is clipped - the measurement is invalid")
    ok = worst.thdn_dbfs <= accept_dbfs
    return (ok, f"worst channel {worst.channel}: {worst.thdn_dbfs:.2f} dBFS "
                f"(accept <= {accept_dbfs:.2f})")
