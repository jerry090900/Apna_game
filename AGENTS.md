# XHYN IV engineering

XHYN IV is an Android GTA IV recompilation. Android launcher and build files are in `os/android/app`, native Android integration in `os/android/native`, and the runtime and renderer in `glue/rexglue-sdk-main`. Build instructions are in `docs/android/BUILDING.md`; regression commands are in `.github/workflows/android-checks.yml` and `tools/`.

Inspect the exact source, logs and build before changing behavior; distinguish observations from hypotheses and reproduce failures where practical. Keep fixes focused, run relevant tests and report their actual outcomes and limitations. Preserve existing changes, settings, saves and game data; do not delete data or caches without approval.

Preserve application ID `com.xhyn.ivrecomp` and signing identity. Never expose or commit keystores, passwords, private keys or proprietary game assets. Do not claim a crash or upgrade fixed without reproduction or install-over evidence.

Use `native-crash` for native faults and symbolication, `vulkan-mali` for Mali/Vulkan behavior, `apk-updates` for Android packaging and upgrades, and `regression-review` for verification and review. These skills adapt evidence-first research and targeted testing from [ECC](https://github.com/affaan-m/ECC); no ECC hooks or external servers are required.
