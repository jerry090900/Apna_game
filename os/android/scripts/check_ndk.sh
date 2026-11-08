#!/bin/bash
# Validate both the selected NDK and the compiler recorded by an existing CMake build.
set -euo pipefail
: "${ANDROID_NDK:?ANDROID_NDK must point to Android NDK r29}"
case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) host=windows-x86_64; clang=clang++.exe ;;
  Darwin) host=darwin-x86_64; clang=clang++ ;;
  *) host=linux-x86_64; clang=clang++ ;;
esac
python - "$ANDROID_NDK" "${ANDROID_NDK_HOME:-$ANDROID_NDK}" "$host" "$clang" "${1:-}" <<'PY'
import pathlib, re, sys
ndk, home, host, clang, build = sys.argv[1:]
ndk, home = pathlib.Path(ndk).resolve(), pathlib.Path(home).resolve()
def fail(message):
    sys.exit('NDK preflight: ' + message)
if ndk != home:
    fail('ANDROID_NDK and ANDROID_NDK_HOME refer to different directories')
properties = ndk / 'source.properties'
if not properties.is_file() or not re.search(r'^Pkg\.Revision\s*=\s*29\.0\.14206865\s*$', properties.read_text(), re.MULTILINE):
    fail(f'{properties} is missing or does not specify 29.0.14206865')
toolchain = ndk / 'build/cmake/android.toolchain.cmake'
compiler = ndk / 'toolchains/llvm/prebuilt' / host / 'bin' / clang
if not toolchain.is_file() or not compiler.is_file():
    fail(f'missing NDK CMake toolchain or compiler: {toolchain}, {compiler}')
if build:
    directory = pathlib.Path(build)
    cache = directory / 'CMakeCache.txt'
    if not cache.is_file(): fail(f'missing {cache}; configure the build first')
    match = re.search(r'^CMAKE_TOOLCHAIN_FILE:[^=]*=(.+)$', cache.read_text(), re.MULTILINE)
    if not match or pathlib.Path(match.group(1)).resolve() != toolchain.resolve():
        fail('CMake cache uses a different or missing Android toolchain; use a clean build directory')
    compiler_files = list((directory / 'CMakeFiles').glob('*/CMakeCXXCompiler.cmake'))
    if len(compiler_files) != 1: fail('missing or ambiguous configured C++ compiler metadata')
    match = re.search(r'^set\(CMAKE_CXX_COMPILER "([^"]+)"\)', compiler_files[0].read_text(), re.MULTILINE)
    if not match or pathlib.Path(match.group(1)).resolve() != compiler.resolve():
        fail('CMake configured a different C++ compiler; use a clean build directory')
print(f'NDK preflight: {ndk}; CMake toolchain: {toolchain}; C++ compiler: {compiler}')
PY
"$ANDROID_NDK/toolchains/llvm/prebuilt/$host/bin/$clang" --version | head -n 1
