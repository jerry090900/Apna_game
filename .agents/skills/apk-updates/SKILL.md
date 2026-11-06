---
name: apk-updates
description: Protect Android APK upgrade-in-place compatibility: applicationId/package identity, signing certificate/key lineage, monotonically increasing versionCode, ABIs, flavors, and install artifacts. Use before changing release configs or when an APK refuses to update without uninstalling.
---

# APK update compatibility guard

## Goal
Ensure a new APK can install **over the existing app without uninstalling it or losing its data**, when technically possible.

## Workflow
1. Locate Gradle/manifest signing and variant configuration. Record the shipping `applicationId` (including flavors/suffixes), `versionCode`, `versionName`, minSdk, supported ABIs, and APK/AAB output variant.
2. If a previous installable APK is available, inspect its package, versionCode, and signing certificate **fingerprint** using tools such as `aapt`/`apkanalyzer` and `apksigner verify --print-certs`. Prefer evidence from the actual installed release over assumptions from current source.
3. For a normal in-place update require: (a) identical installed package/application ID; (b) compatible signing certificate or a valid, platform-supported signing lineage; and (c) a strictly higher versionCode. Account for device SDK, build type, split APKs, ABI, and installer restrictions. A matching display name or versionName is insufficient.
4. Protect existing keystore files, aliases, passwords, signing environment variables, Play App Signing arrangements, and fingerprints. Never create or replace a signing identity silently, never print private keys or passwords, and never commit signing secrets.
5. Before release/config changes, compare old vs new artifacts and state whether update compatibility is **verified**, **likely**, **broken**, or **unknown**, with the evidence for each claim.
6. When authorized and a safe device/emulator is available, test `adb install -r` of the new APK **over a real prior-version installation**, without uninstalling or clearing data. Verify retained data and launch. Capture the exact install failure code if it fails.
7. If the old signing key is inaccessible or signatures are incompatible, stop and explain that changing `versionCode` cannot repair this. Propose a deliberate new package/channel only with explicit owner approval.
8. Invoke `regression-review` before shipping and record a reproducible build/release checklist.

## Safety
- Never uninstall or clear the existing app to make an update test pass.
- Never generate new release keys, rotate signers, publish APKs, or change package IDs without explicit approval.
- Keep debug and release identities distinct; do not claim debug APKs are update-compatible with release builds.

## Output contract
Provide a **Before / After compatibility table**, **Signing-fingerprint match status**, **versionCode progression**, **Exact install-test result**, **Risks/unknowns**, and **Release decision**.
