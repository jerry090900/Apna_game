---
name: regression-review
description: Review a change and choose evidence-producing project regression checks.
---

Inspect the diff, relevant implementation and existing tests first. When practical, demonstrate a regression failing before the minimal fix and passing afterward. Choose affected checks from `.github/workflows/android-checks.yml`, `tools/run_android_host_tests.py`, `tools/run_recomp_core_tests.py` and `tools/run_android_java_tests.py`; retain command exit statuses. Report passed, failed, skipped and unrun checks separately, and do not equate compilation with runtime verification.
