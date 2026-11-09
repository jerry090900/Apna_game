#!/usr/bin/env python3
"""Verify signed release identity and report public APK metadata after apksigner verification."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

unsigned, signed, cert_file, badging_file, expected, previous = sys.argv[1:]
def fail(message):
    raise SystemExit(message)
def normalize(value):
    value = value.replace(':', '').lower()
    if not re.fullmatch(r'[0-9a-f]{64}', value):
        fail('Invalid expected certificate SHA-256')
    return value
certs = re.findall(r'^Signer #\d+ certificate SHA-256 digest:\s*([0-9a-fA-F:]+)\s*$', Path(cert_file).read_text(), re.MULTILINE)
if len(certs) != 1 or normalize(certs[0]) != normalize(expected):
    fail('Signed APK certificate does not match the trusted release certificate')
badging = Path(badging_file).read_text()
package = re.search(r"^package: name='([^']+)' versionCode='(\d+)' versionName='([^']*)'", badging, re.MULTILINE)
if not package or package.group(1) != 'com.xhyn.ivrecomp':
    fail('Unexpected APK package metadata')
if not previous.isdecimal() or int(package.group(2)) <= int(previous):
    fail('versionCode must exceed the verified highest prior release code')
with zipfile.ZipFile(unsigned) as original, zipfile.ZipFile(signed) as output:
    if output.testzip(): fail('Signed APK contains damaged archive entries')
    entries = [n for n in original.namelist() if n.startswith('lib/')]
    if not entries or any(not n.startswith('lib/arm64-v8a/') for n in entries): fail('Invalid native ABI')
    if set(entries) != {n for n in output.namelist() if n.startswith('lib/')}:
        fail('Signed APK native library set differs from verified unsigned APK')
    for name in entries:
        if hashlib.sha256(original.read(name)).digest() != hashlib.sha256(output.read(name)).digest():
            fail('Signed APK native library contents differ')
apk = Path(signed)
print(json.dumps({'package': package.group(1), 'version_code': int(package.group(2)), 'version_name': package.group(3), 'signer_sha256': normalize(certs[0]), 'apk_sha256': hashlib.sha256(apk.read_bytes()).hexdigest(), 'size_bytes': apk.stat().st_size}, indent=2))
