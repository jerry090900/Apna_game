# Codex instructions — XHYN IV / Apna Game

These instructions apply to work in this repository. Read the relevant files before editing. Prefer small, reviewable changes backed by evidence, and follow the applicable repository-local skill in `.agents/skills/`.

## Project and source of truth

- This repository is XHYN IV, an Android ARM64 port based on LibertyRecomp/LibertyRecompAndroid. Game files are **not** included; do not add proprietary game images, title updates, or user game data.
- Android application module: `os/android/app/`; build configuration: `os/android/app/build.gradle.kts`. The shipping application ID is `com.xhyn.ivrecomp`, with `arm64-v8a` as the packaged ABI.
- Android native build/runtime: `LibertyRecomp/`, `LibertyRecompLib/`, `glue/`, `os/android/native/`, and `os/android/scripts/`.
- Start with `README.md`, `docs/android/BUILDING.md`, `docs/android/INSTALL.md`, and `docs/android/TROUBLESHOOTING.md` as appropriate. Use `.github/workflows/android-checks.yml` to find established regression commands.
- **Gradle packages the app; it does not build all native game libraries.** A complete release needs the documented CMake/NDK native build and `os/android/scripts/package_release.py`. Never claim a Gradle-only APK is a complete game build.

## Choose the appropriate skill

- `.agents/skills/native-crash/SKILL.md`: SIGSEGV/SIGABRT, JNI/linker faults, ANRs, tombstones, and native backtraces.
- `.agents/skills/vulkan-mali/SKILL.md`: Vulkan, GPU drivers, shader/swapchain errors, rendering and device-specific compatibility. Verify the GPU first; do not assume Mali.
- `.agents/skills/apk-updates/SKILL.md`: package identity, APK signatures, release signing, versionCode, ABI, and in-place update compatibility.
- `.agents/skills/regression-review/SKILL.md`: after code/build changes, review regressions and report actual validation outcomes.

Read the skill file when its topic applies; use multiple skills for cross-cutting changes (for example, `apk-updates` plus `regression-review` for releases).

## Evidence-first workflow

1. State the task, current branch/baseline, affected components, and known evidence. Inspect source, errors, available logs, and prior tests **before** diagnosing a failure.
2. Separate observed facts from hypotheses. For native crashes, match the exact library build IDs to symbols before naming faulting functions. If evidence is missing, say what is unknown.
3. Propose and implement the smallest safe change authorized by the task. Avoid unrelated refactors, dependency upgrades, and broad rewrites.
4. Run relevant existing checks and capture commands, output, and failures. Useful checks are documented in `.github/workflows/android-checks.yml`, including `python3 tools/run_android_java_tests.py`, `python3 tools/run_android_host_tests.py`, `python3 tools/run_recomp_core_tests.py`, and `python3 tools/check_android_native.py --ndk <installed-ndk-path>` when prerequisites exist. Do not assume these tests ran successfully unless they did.
5. Report changed files, tests **passed / failed / blocked / not run**, remaining risks, and what would prove the fix on a real Android device. A successful compile is not proof that gameplay or update-in-place works.

## Android release and data safety

- Preserve `com.xhyn.ivrecomp` and existing data/settings/saves unless the owner explicitly authorizes a migration.
- The checked-in Test12 baseline uses `versionCode = 40`; inspect current source and shipped APKs before choosing any subsequent release number. New upgrade-compatible releases need a higher versionCode and matching package and signing identity (or a valid supported signing lineage).
- Treat the **next signed release** as the intended permanent update baseline only after the owner has securely established and backed up its stable release key. Do not invent, generate, rotate, overwrite, commit, or print keys/passwords without explicit owner approval. Keep secrets out of code, logs, commits, CI artifacts, and pull requests.
- Never uninstall the app, clear app data, overwrite saves, flash drivers, change device settings, or publish a release as a shortcut. Ask before destructive or irreversible actions.
- Use `apksigner`/manifest inspection and, when explicitly authorized, a safe install-over-old-version test with retained data to confirm upgrade compatibility. Mark missing device/artifact verification as **unverified**.
- Repository MCP tools and third-party ECC tooling are **not automatically trusted or installed**. Review their code, capabilities, and security implications before enabling them. Do not enable a general-purpose terminal MCP server just because it exists.

## Completion expectations

For every task, give a concise outcome with links or paths, changes made, exact tests and results, and any unresolved blockers. Never guess the cause of an observed failure or claim an unperformed action is complete.
