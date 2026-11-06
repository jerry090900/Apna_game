---
name: regression-review
description: Review Android app changes against known working behavior, run focused build/test/smoke checks, and report regressions and untested risks. Use after fixes, renderer updates, native-code changes, and APK packaging modifications.
---

# Regression review

## Goal
Protect known-good app behavior while verifying that a requested change works. Separate tested outcomes from assumptions.

## Workflow
1. Identify the change scope, baseline commit/tag, requested fix, and any known-working features from tests, issue reports, release notes, and user-provided acceptance criteria. Do not invent a baseline.
2. Review the diff for surprising changes: app ID/signing/versionCode, ABI packaging, native libraries, GPU/renderer fallback, Android permissions, lifecycle, media/audio behavior, storage, onboarding, and UI/navigation. Focus checks on the actual app.
3. Run available low-risk checks in an appropriate environment: Gradle build, lint, unit tests, native tests, static analysis, and relevant instrumentation/emulator tests. Use repo-defined commands; avoid destructive cleanup commands and do not guess task names.
4. Exercise focused smoke checks where supported: install/update (without clearing data), cold launch, resume/background, rotation, core workflows, crash-free shutdown, and the exact previously failing path.
5. Compare actual results to pre-change evidence; distinguish **passed**, **failed**, **blocked**, and **not run**. Do not equate a successful build with runtime correctness.
6. If a regression is confirmed, isolate the change that introduced it; make a narrow correction only if requested and safe, then rerun affected checks.
7. For APK identity/signing concerns, invoke `apk-updates`; for GPU faults, invoke `vulkan-mali`; for native faults, invoke `native-crash` when available.

## Safety
- Do not modify untouched features simply to satisfy a test; report unexpected behavior with evidence.
- Do not uninstall, wipe data, alter signing credentials, or force-update the target device as a review shortcut.
- If test hardware, CI, or prior APKs are unavailable, document the gap explicitly.

## Output contract
Provide **Baseline and scope**, **Regression test matrix (Pass/Fail/Blocked/Not run)**, **Evidence/log paths**, **Changes made**, **Open risks**, and **Go / No-go recommendation** with rationale.
