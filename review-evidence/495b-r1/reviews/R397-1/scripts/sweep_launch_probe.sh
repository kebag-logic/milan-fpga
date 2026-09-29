#!/bin/bash
# Item 2: drive sweep_extra.sh's real (non-dry-run) launch path with a stub
# setsid that records argv and a no-op sleep, under a scratch HOME with a
# stub Vivado settings file, so nothing launches. Usage:
#   sweep_launch_probe.sh <clone> <scratch-dir>
set -u
C=$1; S=$2
rm -rf "$S"; mkdir -p "$S/bin" "$S/home/Xilinx/2026.1/Vivado" "$S<home-path>/work"
cat > "$S/bin/setsid" <<'STUB'
#!/bin/bash
{ printf 'ARGC=%d\n' "$#"; for a in "$@"; do printf '[%s]\n' "$a"; done; echo ---; } >> "$FAKE_LOG"
STUB
printf '#!/bin/sh\nexit 0\n' > "$S/bin/sleep"; chmod +x "$S/bin/"*
echo 'echo settings-sourced' > "$S/home/Xilinx/2026.1/Vivado/settings64.sh"
cd "$C" && env -u SWEEP_CFG HOME="$S/home" FAKE_LOG="$S/argv.log" PATH="$S/bin:$PATH" \
  PYTHONDONTWRITEBYTECODE=1 bash sw/litex/sweep_extra.sh ax7101 probe; echo "rc=$?"
sed -n '1,/^---$/p' "$S/argv.log"
git -C "$C" status --porcelain --untracked-files=no | sed 's/^/TRACKED CHANGE: /'
