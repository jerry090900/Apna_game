---
name: apk-updates
description: Review Android APK identity, signing, packaging, and upgrade compatibility.
---

Preserve `com.xhyn.ivrecomp`, signing certificate continuity, monotonic version codes, settings and saves. Follow `docs/android/BUILDING.md` and `os/android/scripts/package_release.py`; keep secrets outside Git and logs. Verify the actual APK package, version and certificate. Only claim an upgrade works after installing the next APK over the baseline on Android and checking retained settings and saves; never silently replace a missing signing key.
