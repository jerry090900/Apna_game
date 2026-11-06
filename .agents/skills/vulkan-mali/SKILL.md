---
name: vulkan-mali
description: Diagnose Android Vulkan rendering failures and mobile GPU compatibility, especially Arm Mali but also Adreno/PowerVR. Use for Vulkan crashes, black screens, device-lost errors, shader/swapchain issues, and unsupported GPU features; first identify the actual GPU.
---

# Vulkan and mobile GPU compatibility

## Goal
Investigate graphics failures without assuming the phone uses a Mali GPU or that Vulkan is supported. Preserve existing working rendering and audio behavior unless the task specifically requires changing them.

## Workflow
1. Identify the app/build, Android version, actual GPU vendor/model, graphics API path (Vulkan/OpenGL ES), driver version, and failure scenario from available code/logs/device data. A Snapdragon-based phone may use Adreno, **not Mali**; branch diagnosis by verified hardware.
2. Inspect the renderer's initialization, feature and extension checks, surface/swapchain setup, shader pipeline, synchronization, resource lifetimes, and error reporting. Check relevant `VkResult` values including `VK_ERROR_DEVICE_LOST`, `VK_ERROR_OUT_OF_DATE_KHR`, and `VK_ERROR_SURFACE_LOST_KHR`.
3. Where execution is authorized and tools exist, inspect Vulkan physical-device properties, supported queue families, required extensions/features, surface formats/present modes, and app logs. A shell feature flag alone does not prove that the app's Vulkan path works.
4. Compare the renderer's requested capabilities to **observed** device support. Distinguish app defects, unsupported capabilities, shader/compiler issues, Android lifecycle/surface issues, and possible vendor driver defects. Never claim a driver bug without corroborating evidence.
5. Prefer capability-based checks, correct synchronization, resource cleanup, and graceful fallback to an **existing** supported renderer. Do not force Vulkan on unsupported devices or introduce invasive driver hacks.
6. Validate launch, rotate/background/foreground, resize/surface recreation, repeated rendering, and any graphics baseline tests available. Invoke `native-crash` for signal/tombstone diagnosis and `regression-review` to protect working features.

## Safety
- Do not flash/update GPU drivers, replace system libraries, change boot images, or modify the device without explicit approval.
- Keep graphics changes separate from music/audio synchronization unless the user specifically asks for both.
- If hardware, driver, or logs are unknown, report a data gap rather than guessing the fix.

## Output contract
Provide: **Verified GPU/driver/API**, **Required versus supported capabilities**, **Evidence and root-cause hypothesis**, **Minimal fix**, **Validation matrix**, and **Remaining device-specific risks**.
