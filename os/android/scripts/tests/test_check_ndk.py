#!/usr/bin/env python3
"""Exercise the NDK guard without downloading toolchains or running a build."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'check_ndk.sh'


class NdkPreflightTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ndk = self.root / 'ndk'
        (self.ndk / 'build/cmake').mkdir(parents=True)
        (self.ndk / 'build/cmake/android.toolchain.cmake').touch()
        self.bin = self.ndk / 'toolchains/llvm/prebuilt/linux-x86_64/bin'
        self.bin.mkdir(parents=True)
        self.clang = self.bin / 'clang++'
        self.clang.write_text('#!/bin/sh\necho fake clang\n')
        self.clang.chmod(0o755)
        (self.ndk / 'source.properties').write_text('Pkg.Revision = 29.0.14206865\n')
        self.build = self.root / 'build'
        compiler = self.build / 'CMakeFiles/3.31.6/CMakeCXXCompiler.cmake'
        compiler.parent.mkdir(parents=True)
        self.compiler = compiler
        self.compiler.write_text(f'set(CMAKE_CXX_COMPILER "{self.clang}")\n')
        self.cache = self.build / 'CMakeCache.txt'
        self.cache.write_text(f'CMAKE_TOOLCHAIN_FILE:FILEPATH={self.ndk}/build/cmake/android.toolchain.cmake\n')

    def check(self, build=True, home=None):
        env = dict(os.environ, ANDROID_NDK=str(self.ndk), ANDROID_NDK_HOME=str(home or self.ndk))
        return subprocess.run(['bash', str(SCRIPT), *([str(self.build)] if build else [])], env=env, capture_output=True, text=True)

    def test_valid_ndk_and_cache(self):
        self.assertEqual(self.check().returncode, 0)
        alias = self.root / 'ndk-alias'
        alias.symlink_to(self.ndk, target_is_directory=True)
        self.assertEqual(self.check(home=alias).returncode, 0)

    def test_wrong_revision_or_conflicting_environment(self):
        (self.ndk / 'source.properties').write_text('Pkg.Revision = 27.3.13750724\n')
        self.assertNotEqual(self.check(False).returncode, 0)
        self.assertNotEqual(self.check(False, self.root / 'other').returncode, 0)

    def test_stale_toolchain_or_compiler(self):
        self.cache.write_text('CMAKE_TOOLCHAIN_FILE:FILEPATH=/old/android.toolchain.cmake\n')
        self.assertNotEqual(self.check().returncode, 0)
        self.cache.write_text(f'CMAKE_TOOLCHAIN_FILE:FILEPATH={self.ndk}/build/cmake/android.toolchain.cmake\n')
        self.compiler.write_text('set(CMAKE_CXX_COMPILER "/old/clang++")\n')
        self.assertNotEqual(self.check().returncode, 0)

    def test_missing_compiler(self):
        self.clang.unlink()
        self.assertNotEqual(self.check(False).returncode, 0)


if __name__ == '__main__':
    unittest.main()
