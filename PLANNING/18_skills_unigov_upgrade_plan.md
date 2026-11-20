# UniGov Master Implementation Plan: 18 Android Skills 2026 SOTA Upgrade

**Document ID**: `UNIGOV-PLAN-2026-SKILLS-18`  
**Governing Standard**: UniGov Project Governance & Constitutional Law-000 (Zero Shortcuts)  
**Target Environment**: `~/.gemini/config/skills/`, `~/.gemini/antigravity/skills/`, `~/.gemini/antigravity-ide/skills/`  
**Status**: `PENDING_FOUNDER_CONFIRMATION`  

---

## 1. Executive Governance Overview

### 1.1 Objective
Transform 18 malfunctioning and technically outdated Android developer skills into high-performance, 2026 SOTA (State-of-the-Art) engineering assets. This eliminates all startup YAML frontmatter errors, incorporates Android 15/16 APIs, Kotlin 2.1+ K2 compiler workflows, Jetpack Compose 1.7+ modern patterns, and enforces rigorous UniGov verification gates.

### 1.2 Constitutional Invariants (Law-000)
1. **YAML Frontmatter Integrity**: Every `SKILL.md` MUST strictly validate against YAML 1.2 specs using block scalar `description: >-` without dangling unquoted keys, stray colons, or syntax anomalies.
2. **Zero Devanagari Invariant**: Absolutely zero Devanagari glyphs in any markdown, doc, or code.
3. **Zero Vehicle/Transport Metaphors**: Strictly technical terminology only (`cluster`, `module`, `console`, `orchestrator`).
4. **Authentic 2026 SOTA Knowledge**: No superficial copy-paste or stub heuristics. Real production-grade blueprints, API tables, and verification commands.
5. **Exact Cross-Environment Bit-Parity**: All copies across `~/.gemini/config/skills`, `~/.gemini/antigravity/skills`, and `~/.gemini/antigravity-ide/skills` must match SHA-256 hashes.

---

## 2. Hierarchical Dependency DAG (Tiers & Modules)

```
[Phase 1: Invariant & Validation Engine]
       │
       ▼
[Phase 2: Domain 1 - Performance & Profiling (Skills 1-3)]
       │
       ▼
[Phase 3: Domain 2 - Modern UI & Insets (Skills 4-7)]
       │
       ▼
[Phase 4: Domain 3 - Next-Gen Interaction & Nav (Skills 8-11)]
       │
       ▼
[Phase 5: Domain 4 - Security & Identity (Skills 12-14)]
       │
       ▼
[Phase 6: Domain 5 - Toolchain & Testing (Skills 15-18)]
       │
       ▼
[Phase 7: Parity Sync, Brain Memory & Dev Log Commit]
```

---

## 3. Detailed Per-Skill UniGov Engineering Specifications

---

### Domain 1: Performance, Profiling & APK Optimization

#### [TASK-SKILL-01] `perfetto-trace-analysis`
* **Target File**: `perfetto-trace-analysis/SKILL.md` (+ `references/`)
* **Current Baseline**: 79 lines, high-level trace tips, broken YAML frontmatter.
* **Blast Radius**: `SKILL.md`, `references/perfetto-stdlib.md`, `references/hints_*.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. Implement **5-Stage Systematic Triage Protocol**:
     - Stage 1: Choreographer Frame Jank & Missed VSync (120Hz/144Hz deadline calculations).
     - Stage 2: Main Thread Uninterruptible Sleep (D-state) & Disk I/O blocking.
     - Stage 3: Binder IPC contention and cross-process transaction stalls.
     - Stage 4: ART Runtime Concurrent Mark Sweep / Generational Garbage Collection pauses.
     - Stage 5: GPU SurfaceFlinger queue stalls.
  3. Add automated Python CLI trace parser recipe to extract culprit thread names and callstacks.
  4. Macrobenchmark startup profiling (Cold, Warm, Hot) with baseline profiles comparison.
* **Verification Gate**:
  ```bash
  python3 -c "import yaml; yaml.safe_load(open('.../perfetto-trace-analysis/SKILL.md').read().split('---')[1])"
  ```

#### [TASK-SKILL-02] `perfetto-sql`
* **Target File**: `perfetto-sql/SKILL.md` (+ `references/`)
* **Current Baseline**: 142 lines, basic queries, broken YAML frontmatter.
* **Blast Radius**: `SKILL.md`, `references/perfetto-stdlib.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. Add **2026 Perfetto Stdlib Query Blueprints**:
     - `android_frames`: Jank cause quantification per frame.
     - `android_jank_cuj`: Critical User Journey (CUJ) frame metrics for scrolling lists.
     - `thread_slice` & `sched`: Core allocation, CPU frequency pinning, and thread wakeup latency.
  3. Tailored queries for POS / Retail continuous billing stress-tests and thermal printer socket I/O delays.
  4. Ready-to-execute `trace_processor_shell` batch query invocation templates.
* **Verification Gate**: YAML parse check + SQL syntax validation test.

#### [TASK-SKILL-03] `r8-analyzer`
* **Target File**: `r8-analyzer/SKILL.md` (+ `references/`)
* **Current Baseline**: 62 lines, generic R8 analyzer setup, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/KEEP-RULES-IMPACT-HIERARCHY.md`, `references/REDUNDANT-RULES.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Full-Mode R8 Optimization Blueprint** (`android.enableR8.fullMode=true`):
     - Safe reflection-free shrinking rules.
     - `kotlinx.serialization` zero-reflection keep-rule templates.
  3. **Wildcard Keep Audit Algorithm**:
     - Detecting and replacing greedy `-keep class com.** { *; }` patterns.
     - Surgical method-level rules (`-keepclassmembers`, `-keepattributes Signature, InnerClasses`).
  4. Reproducible release mapping files and AppArmor / DexGuard compatibility notes.
* **Verification Gate**: YAML parse check + Proguard syntax validation.

---

### Domain 2: Modern Android 15/16 UI & Insets Architecture

#### [TASK-SKILL-04] `adaptive`
* **Target File**: `adaptive/SKILL.md` (+ `references/`)
* **Current Baseline**: 301 lines, basic WindowSizeClass, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Material 3 Adaptive Canonical Layouts**:
     - `ListDetailPaneScaffold` and `SupportingPaneScaffold` complete architecture.
     - ThreePaneScaffoldNavigator state restoration and deep link parsing.
  3. **Foldable Posture Physics**:
     - Jetpack WindowManager posture calculation (`FoldingFeature.OcclusionType`, `Orientation`).
     - Dynamic tabletop mode and book mode dual-pane splits.
  4. **Two-Tier Harmonic Proportional Weighting & Anti-Starvation Invariant**:
     - Row budgeting rules to prevent horizontal clipping on narrow displays.
     - Enforce WCAG 2.2 AA 48x48dp minimum touch bounds across phone, foldable, tablet, and POS screens.
* **Verification Gate**: YAML parse check + Compose layout contract checks.

#### [TASK-SKILL-05] `edge-to-edge`
* **Target File**: `edge-to-edge/SKILL.md` (+ `references/`)
* **Current Baseline**: 426 lines, Android 15 basic insets, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android15_mandatory_edge_to_edge_dialogs.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Android 15 & 16 Mandatory Edge-to-Edge Compliance**:
     - Elimination of deprecated `fitsSystemWindows`, `setStatusBarColor`, `WindowInsetsControllerCompat`.
     - Standard `enableEdgeToEdge()` configuration with transparent system bars.
  3. **Complete Insets Physics & Form UX**:
     - `WindowInsets.safeDrawing`, `imeNestedScroll()`, and dynamic bottom padding for billing submit buttons.
     - Keyboard open/close spring physics and zero-jitter layout animation.
  4. Split-screen, multi-window, and foldable edge-to-edge budgeting.
* **Verification Gate**: YAML parse check + Inset modifier contract validation.

#### [TASK-SKILL-06] `styles`
* **Target File**: `styles/SKILL.md` (+ `references/`)
* **Current Baseline**: 220 lines, experimental Compose Styles, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Design Token Architecture (DTCG Standard)**:
     - Multi-tier tokens (Global -> Semantic -> Component) compiled to Compose `@Immutable` state objects.
  3. **Visual Archetype Theming Engine**:
     - Modern Minimalist, NeuGlass frosted blur, Brutalist, and Editorial archetypes.
  4. **OLED True Black & Accessibility High-Contrast Modes**:
     - Zero-recomposition runtime dynamic switching.
     - WCAG 2.2 AAA contrast token validation.
* **Verification Gate**: YAML parse check + Token schema validation.

#### [TASK-SKILL-07] `migrate-xml-views-to-jetpack-compose`
* **Target File**: `migrate-xml-views-to-jetpack-compose/SKILL.md` (+ `references/`)
* **Current Baseline**: 124 lines, 10-step summary, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/identify-optimal-xml-candidate.md`, `references/xml-layout-migration.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Strangler Fig Architecture**:
     - Incremental bottom-up component migration without breaking host XML activities/fragments.
  3. **ComposeView Lifecycle Governance**:
     - `ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed` mandatory standard.
     - Strong Skipping Mode (Compose 1.7+) and compiler stability metrics.
  4. **State Modernization**:
     - Migrating legacy LiveData / RxJava to Kotlin Coroutines `StateFlow` and `@Immutable` data states.
  5. **Visual Parity Verification**:
     - Screenshot diff testing before removing legacy XML files.
* **Verification Gate**: YAML parse check + Migration checklist completeness.

---

### Domain 3: Next-Gen App Interaction & Navigation

#### [TASK-SKILL-08] `navigation-3`
* **Target File**: `navigation-3/SKILL.md` (+ `references/`)
* **Current Baseline**: 112 lines, early draft, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Type-Safe Navigation DSL**:
     - Kotlin 2.1 `@Serializable` destination objects and data classes (eliminating string URI routes).
     - Safe argument passing with custom Parcelable / NavType serializers.
  3. **Multi-Stack State Retention**:
     - Tab-based navigation preserving backstacks across nested flows.
  4. **Scene Transitions & Shared Element Transitions**:
     - Integration with `SharedTransitionLayout` for seamless list-to-detail hero animations.
  5. **Hilt Navigation Scoping**:
     - Binding `@HiltViewModel` to specific Navigation 3 backstack entries.
* **Verification Gate**: YAML parse check + Type-safe route pattern validation.

#### [TASK-SKILL-09] `appfunctions`
* **Target File**: `appfunctions/SKILL.md` (+ `references/`)
* **Current Baseline**: 65 lines, Android 16 preview stubs, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/feature-discovery-analysis.md`, `references/implementation-configuration.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Android 16 AppFunctions SDK Production Architecture**:
     - Exposing app capabilities (e.g., "Create Quick Invoice", "Query Product Stock", "View Daily Balance") directly to on-device AI models (Gemini Nano / UniBrain) and system voice assistants.
  3. **Structured Parameter Schemas & KDoc Contracts**:
     - Compile-time structured parameter validation ensuring on-device LLMs pass typed, verified arguments.
  4. **Security & Authorization Gates**:
     - Caller signature verification and mandatory user biometric/PIN prompt for financial mutations.
* **Verification Gate**: YAML parse check + AppFunction schema validator.

#### [TASK-SKILL-10] `display-glasses-with-jetpack-compose-glimmer`
* **Target File**: `display-glasses-with-jetpack-compose-glimmer/SKILL.md` (+ `references/`)
* **Current Baseline**: 337 lines, smart glasses HUD stubs, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/*.md` (21 reference files).
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Android XR & Spatial HUD Architecture**:
     - Alignment with Google Android XR SDK standards.
  3. **Zero-Distraction Ultra-Low Luminance UI**:
     - High-contrast pure black OLED backgrounds to minimize display power draw and eliminate eye fatigue.
  4. **Hands-Free POS & Inventory Glanceables**:
     - Hands-free barcode scan verification HUD, inventory count alerts, and voice-confirmed item lookup.
* **Verification Gate**: YAML parse check + Glimmer layout constraints check.

#### [TASK-SKILL-11] `wear-compose-m3`
* **Target File**: `wear-compose-m3/SKILL.md` (+ `references/`)
* **Current Baseline**: 280 lines, basic Wear OS Compose, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Wear OS 5 / 6 Material 3 Standards**:
     - `AppScaffold`, `ScreenScaffold`, and `TransformingLazyColumn` with curved text and round screen clipping.
  3. **Rotary Input & Tactile Physics**:
     - Crown scroll integration (`rotaryScrollable`) with haptic detents.
  4. **Glanceable Wear Tiles & Standalone Sync**:
     - Quick tiles for retail metrics (Today's Sales, Pending Orders) with offline Room DB caching.
* **Verification Gate**: YAML parse check + Wear Compose component audit.

---

### Domain 4: Security, Hardware & Identity

#### [TASK-SKILL-12] `android-intent-security`
* **Target File**: `android-intent-security/SKILL.md`
* **Current Baseline**: 554 lines, Android 6-8 era, broken YAML.
* **Blast Radius**: `SKILL.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Android 14/15/16 Explicit Receiver Laws**:
     - Mandatory `RECEIVER_EXPORTED` vs `RECEIVER_NOT_EXPORTED` enforcement in code and Manifest.
  3. **PendingIntent Immutability Contract**:
     - Mandatory `FLAG_IMMUTABLE` by default; strict cryptographic scoping for mutable exceptions.
  4. **Deep Link Hijacking Defense**:
     - Digital Asset Links (`assetlinks.json`) automated verification, route hijacking defense, and sanitized Uri parsing.
  5. **Caller Identity Verification**:
     - `Binder.getCallingUid()` and package signature hashing before IPC data execution.
* **Verification Gate**: YAML parse check + Security invariant rules check.

#### [TASK-SKILL-13] `verified-email`
* **Target File**: `verified-email/SKILL.md` (+ `references/`)
* **Current Baseline**: 420 lines, legacy email retrieval, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Unified Android Credential Manager API (2026 SOTA)**:
     - Single seamless bottom sheet supporting Passkeys, FIDO2 WebAuthn, Google ID, and Verified Email.
  3. **Cryptographic Token Verification**:
     - Client-side token packaging and server-side public key signature validation.
  4. **Offline POS Kiosk Fallbacks**:
     - Graceful degradation to local cryptographic PIN / StrongBox auth during network outages.
* **Verification Gate**: YAML parse check + Credential Manager flow check.

#### [TASK-SKILL-14] `camera1-to-camerax`
* **Target File**: `camera1-to-camerax/SKILL.md`
* **Current Baseline**: 270 lines, CameraX 1.3, broken YAML.
* **Blast Radius**: `SKILL.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **CameraX 1.4 / 1.5 Architecture**:
     - Zero-copy buffer recycling with `ImageAnalysis.Builder.setOutputImageFormat()`.
  3. **High-Speed ML Kit Barcode Decoding Pipeline**:
     - GS1 DataMatrix, EAN-13, and QR code parsing for pharma and retail checkout at 60 FPS.
  4. **Modern Permissions & Lifecycle**:
     - Jetpack Activity Result Contracts (`rememberLauncherForActivityResult`) without legacy callbacks.
* **Verification Gate**: YAML parse check + CameraX pipeline contract check.

---

### Domain 5: Toolchains, Testing & Store Compliance

#### [TASK-SKILL-15] `agp-9-upgrade`
* **Target File**: `agp-9-upgrade/SKILL.md` (+ `references/`)
* **Current Baseline**: 103 lines, AGP 9 early notes, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/recipes.md`, `references/ksp-kapt.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Gradle 9 & AGP 9.0+ Production Configuration**:
     - Configuration Cache and Project Isolation full compatibility checklist.
  3. **KSP2 & K2 Compiler Migration**:
     - Complete elimination of KAPT; migrating Room, Hilt, and Moshi/Moshi-IR to KSP2.
  4. **Java 21 LTS Toolchain Invariant**:
     - Modern JVM bytecode targets and build performance flags.
* **Verification Gate**: YAML parse check + Gradle recipe check.

#### [TASK-SKILL-16] `testing-setup`
* **Target File**: `testing-setup/SKILL.md` (+ `references/`)
* **Current Baseline**: 198 lines, generic testing notes, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/android/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Modern 3-Tier Testing Pyramid Architecture**:
     - Tier 1: Unit Tests (JUnit 5 + MockK + Turbine for asynchronous StateFlow/Coroutines).
     - Tier 2: Headless Integration Tests (Robolectric 4.14+ with simulated Android 15 environment).
     - Tier 3: UI Screenshot Regression Tests (Roborazzi / Paparazzi).
  3. **Law-000 Zero Mock-Hacks**:
     - Authentic in-memory fake repositories and test doubles instead of brittle mock heuristics.
  4. **UniGov Automated Test Execution Gate**:
     - Deterministic CI commands to verify full test suite before release.
* **Verification Gate**: YAML parse check + Testing pyramid structure check.

#### [TASK-SKILL-17] `play-billing-library-version-upgrade`
* **Target File**: `play-billing-library-version-upgrade/SKILL.md` (+ `references/`)
* **Current Baseline**: 93 lines, PBL 7/8 notes, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/version-checklist.md`, `references/migration-logic.md`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Play Billing Library 7.x & 8.x SOTA Compliance**:
     - Base plans, multi-offer subscription models, installment plans, and prepaid balances.
  3. **Alternative Billing (User Choice Billing - UCB in India & EU)**:
     - Statutory alternative payment rails integration alongside Google Play Billing.
  4. **Idempotent Webhook Verification**:
     - Real-Time Developer Notifications (RTDN) backend verification patterns.
* **Verification Gate**: YAML parse check + Billing flow checklist check.

#### [TASK-SKILL-18] `engage-sdk-integration`
* **Target File**: `engage-sdk-integration/SKILL.md` (+ `references/`)
* **Current Baseline**: 129 lines, generic engage clusters, broken YAML.
* **Blast Radius**: `SKILL.md`, `references/clusters.md`, `references/schemas/`.
* **2026 Upgrades**:
  1. Fix YAML frontmatter (`description: >-`).
  2. **Google Play Engage Retail / Shop Cluster Blueprint**:
     - Personalized recommendations, price drop alerts, and cart continuation clusters.
  3. **Non-Blocking Background Publishing Pipeline**:
     - Scheduled `CoroutineWorker` execution with battery-efficient sync constraints.
  4. **JSON Schema Validator**:
     - Compile-time payload validation against Google Play cluster schema definitions.
* **Verification Gate**: YAML parse check + Schema contract check.

---

## 4. Phase-Wise Execution Protocol

1. **Phase 1: Verification Engine Scaffold**
   - Create a deterministic automated test script: `test_all_18_skills.py` that parses YAML frontmatter, validates all required sections, checks for forbidden Devanagari/transport terms, and asserts 2026 standards.
2. **Phase 2: Domain 1 (Skills 1–3) Upgrades & Verification**
   - Upgrade `perfetto-trace-analysis`, `perfetto-sql`, `r8-analyzer`.
   - Run verification gate on Domain 1.
3. **Phase 3: Domain 2 (Skills 4–7) Upgrades & Verification**
   - Upgrade `adaptive`, `edge-to-edge`, `styles`, `migrate-xml-views-to-jetpack-compose`.
   - Run verification gate on Domain 2.
4. **Phase 4: Domain 3 (Skills 8–11) Upgrades & Verification**
   - Upgrade `navigation-3`, `appfunctions`, `display-glasses-with-jetpack-compose-glimmer`, `wear-compose-m3`.
   - Run verification gate on Domain 3.
5. **Phase 5: Domain 4 (Skills 12–14) Upgrades & Verification**
   - Upgrade `android-intent-security`, `verified-email`, `camera1-to-camerax`.
   - Run verification gate on Domain 4.
6. **Phase 6: Domain 5 (Skills 15–18) Upgrades & Verification**
   - Upgrade `agp-9-upgrade`, `testing-setup`, `play-billing-library-version-upgrade`, `engage-sdk-integration`.
   - Run verification gate on Domain 5.
7. **Phase 7: Full Sync, Memory Update & Dev Log Commit**
   - Mirror updated skills across `~/.gemini/config/skills/`, `~/.gemini/antigravity/skills/`, and `~/.gemini/antigravity-ide/skills/`.
   - Re-run `auto_brain_sync.py`.
   - Append detailed milestone entry into project `dev_logs.txt`.

---
*Authored by: UniAi Co-Architect for Founder Shoeb Ahmad*
