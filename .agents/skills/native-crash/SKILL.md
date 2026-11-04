---
name: native-crash
description: Investigate and verify native Android crashes with matching binaries.
---
Match tombstone build IDs to exact ELF files; symbolize PCs and inspect registers, fault address, and guest ABI before proposing causes. Preserve logs and settings. Reproduce the defect with an applicable regression; run `python3 tools/run_recomp_core_tests.py` when relevant. A host test does not prove a device crash fixed.
