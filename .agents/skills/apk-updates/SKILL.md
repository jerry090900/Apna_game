---
name: apk-updates
description: Review Android packaging, signing continuity, and upgrade behavior.
---
Preserve `com.xhyn.ivrecomp`, the existing release certificate, version monotonicity, and user data. Follow `docs/android/BUILDING.md` and `os/android/scripts/package_release.py`. Keep keys and passwords outside Git. Check actual APK identity and signature; only claim upgrade compatibility after an on-device install-over test retaining settings and saves.
