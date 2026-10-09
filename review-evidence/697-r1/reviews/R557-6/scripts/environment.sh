# Source this file from Bash. All dependencies and temporary files remain in the packet.
review_packet=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
review_sdk="$review_packet/scratch/dependencies"
mkdir -p "$review_packet/scratch/bin" "$review_packet/scratch/temp"
cat > "$review_packet/scratch/bin/clang-18" <<WRAPPER
#!/bin/sh
LD_LIBRARY_PATH="$review_sdk/llvm18/usr/lib/x86_64-linux-gnu" exec "$review_sdk/llvm18/usr/lib/llvm-18/bin/clang" "\$@"
WRAPPER
chmod +x "$review_packet/scratch/bin/clang-18"
export PATH="$review_packet/scratch/bin:$PATH"
export TSN_CLANG="$review_packet/scratch/bin/clang-18"
export CPLUS_INCLUDE_PATH="$review_sdk/gtest14/include"
export LIBRARY_PATH="$review_sdk/gtest14/lib"
export PKG_CONFIG_PATH="$review_sdk/gtest14/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$review_sdk/gtest14"
export TMPDIR="$review_packet/scratch/temp"
export PYTHONDONTWRITEBYTECODE=1
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1
export UBSAN_OPTIONS=halt_on_error=1
export REVIEW_ORIGINAL_PATH="${REVIEW_ORIGINAL_PATH:-$PATH}"
export REVIEW_COMPILER_LOCKS="$review_packet/scratch/compiler-locks"
mkdir -p "$review_packet/scratch/compiler-bin" "$REVIEW_COMPILER_LOCKS"
for review_compiler in gcc g++ clang clang++ riscv64-elf-gcc; do
  ln -sf ../../scripts/compiler_limit.py "$review_packet/scratch/compiler-bin/$review_compiler"
done
export PATH="$review_packet/scratch/compiler-bin:$PATH"
