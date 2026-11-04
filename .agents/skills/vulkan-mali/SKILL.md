---
name: vulkan-mali
description: Diagnose Mali and Vulkan driver fallback, shader, rendering, or performance issues.
---

Record the selected and actual driver, device capabilities, failing calls and fallback separately. Inspect `os/android/native` and `glue/rexglue-sdk-main` renderer code and correlate logs before changing behavior. Wall-time and published FPS are not GPU timings. Use relevant checks in `.github/workflows/android-checks.yml` and `python3 tools/run_android_host_tests.py`; report whether target-device rendering was tested.
