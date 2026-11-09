#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'verify_signed_artifact.py'
class VerifyArtifact(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        d = Path(self.temp.name)
        self.unsigned, self.signed, self.cert, self.badging = [d / n for n in ('unsigned.apk', 'signed.apk', 'cert', 'badging')]
        for apk in (self.unsigned, self.signed):
            with zipfile.ZipFile(apk, 'w') as z: z.writestr('lib/arm64-v8a/libmain.so', b'fixture')
        self.fingerprint = 'ab' * 32
        self.cert.write_text('Signer #1 certificate SHA-256 digest: ' + self.fingerprint + '\n')
        self.badging.write_text("package: name='com.xhyn.ivrecomp' versionCode='41' versionName='test'\n")
    def run_check(self, fingerprint=None, previous='40'):
        return subprocess.run(['python3', str(SCRIPT), str(self.unsigned), str(self.signed), str(self.cert), str(self.badging), fingerprint or self.fingerprint, previous], capture_output=True, text=True)
    def test_verified_metadata(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['version_code'], 41)
    def test_wrong_certificate_and_non_increasing_version(self):
        self.assertNotEqual(self.run_check('cd' * 32).returncode, 0)
        self.assertNotEqual(self.run_check(previous='41').returncode, 0)
    def test_missing_or_multiple_signers(self):
        self.cert.write_text('')
        self.assertNotEqual(self.run_check().returncode, 0)
        self.cert.write_text('Signer #1 certificate SHA-256 digest: ' + self.fingerprint + '\nSigner #2 certificate SHA-256 digest: ' + self.fingerprint + '\n')
        self.assertNotEqual(self.run_check().returncode, 0)
    def test_wrong_package_and_changed_library(self):
        self.badging.write_text("package: name='other' versionCode='41' versionName='test'\n")
        self.assertNotEqual(self.run_check().returncode, 0)
        self.badging.write_text("package: name='com.xhyn.ivrecomp' versionCode='41' versionName='test'\n")
        with zipfile.ZipFile(self.signed, 'w') as z: z.writestr('lib/arm64-v8a/libmain.so', b'changed')
        self.assertNotEqual(self.run_check().returncode, 0)
if __name__ == '__main__': unittest.main()
