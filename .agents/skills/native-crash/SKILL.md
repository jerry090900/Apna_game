---
name: native-crash
description: Investigate Android native crashes using matching binaries, tombstones, and regression tests.
---

Preserve the original logs and settings. Match tombstone build IDs to the exact ELF files; symbolize PCs and inspect fault address, registers, guest ABI and source before attributing a cause. Separate proven facts from hypotheses. Reproduce the defect when practical and run `python3 tools/run_recomp_core_tests.py` for relevant PPC/runtime changes. Report whether device reproduction was performed; a host test alone cannot establish the crash is fixed.
