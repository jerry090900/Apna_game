---
name: vulkan-mali
description: Diagnose Vulkan driver fallback and Mali rendering failures.
---
Record actual driver, capabilities, fallback and failed calls separately. Inspect shader/pipeline code and device logs before changing rendering; distinguish wall timings from GPU timings. Use relevant checks from `.github/workflows/android-checks.yml` and `tools/run_android_host_tests.py`. Verify visual behavior on the target device when possible.
