# XHYN IV engineering

Use evidence before changing code: identify the exact build, reproduce where possible, and distinguish observations from hypotheses. Preserve existing work and user data. Keep changes minimal and run relevant checks from `.github/workflows/android-checks.yml` and `repository-checks.yml`.

Keep application ID `com.xhyn.ivrecomp` and signing-key continuity. Never commit credentials, private keys, keystores, or proprietary game assets. Never claim a crash or upgrade fixed without a matching reproduction or upgrade test. Do not delete saves, caches, or game data without approval.

Repository skills in `.agents/skills` cover crash, Mali, APK, and regression workflows. Inspect MCP tools before enabling them; see `docs/development/CODEX-TOOLKIT.md`.
