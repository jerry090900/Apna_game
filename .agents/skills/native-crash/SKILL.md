---
name: native-crash
description: Investigate Android app crashes and native NDK/JNI faults using logcat, tombstones, stack traces, symbols, and reproducible evidence. Use for SIGSEGV, SIGABRT, linker errors, ANRs, and native crashes; not for ordinary feature requests.
---

# Native crash investigation

## Goal
Identify a reproducible, evidence-backed cause of a crash and propose the smallest safe fix. Do not guess a cause from a screenshot, isolated error string, or incomplete stack trace.

## Workflow
1. Establish the affected package, app version/versionCode, build variant, ABI, Android API level, device/GPU, failure time, and exact steps to reproduce. Inspect repo configuration first; ask only for facts not available.
2. Review existing bug reports, logs, CI artifacts, crash traces, or user-supplied files before requesting new diagnostics. If permitted and ADB is available, gather bounded evidence (for example `adb logcat -b crash -d -v threadtime` and relevant application log lines). Avoid full log dumps when a targeted excerpt is sufficient. Redact tokens, account data, and other private content.
3. Classify the failure: Java/Kotlin exception, native signal (SIGSEGV/SIGABRT/SIGBUS), JNI contract, dynamic linker/ABI mismatch, ANR, memory pressure, or graphics-driver crash. Preserve the exact timestamp, signal, exception, fault address, process/thread, library, and stack frames.
4. For native crashes, check build IDs and use **matching** unstripped native symbols with `ndk-stack`, `llvm-symbolizer`, or `llvm-addr2line` when available. If matching symbols are unavailable, report the limitation rather than invent a function name.
5. Trace the implicated call path into source and native dependencies. Write a hypothesis with confirming and contradicting evidence. Distinguish the proximate crash site from the underlying root cause.
6. Make only the smallest justified code change when the task requests a fix. Preserve working behavior; avoid unrelated dependency upgrades or broad rewrites.
7. Reproduce before and after where a compatible test environment exists; otherwise perform targeted static checks/tests and clearly state which runtime checks were not possible. Invoke `regression-review` after a fix when available.

## Safety
- Never silently reset app data, uninstall an app, flash firmware, root a device, change signing keys, or overwrite release artifacts.
- Never treat an unobserved outcome as a successful reproduction or a verified fix.
- Ask for explicit approval before disruptive device actions.

## Output contract
Provide: **Observed evidence**, **Crash classification**, **Cause / confidence / unknowns**, **Files changed**, **Tests and exact outcomes**, and **Next diagnostic step**. Label unverified conclusions as hypotheses.
