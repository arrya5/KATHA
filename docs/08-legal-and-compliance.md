# Katha — Legal & Compliance

> **Not legal advice.** This is an engineering/founder working document to be reviewed by a
> qualified Indian lawyer before any public launch (and again before Phase 2). It captures the
> current (2026) regulatory landscape and how Katha is designed to stay on the right side of it.
>
> Companion to [04-cultural-fidelity.md](04-cultural-fidelity.md) (reverence policy) and [07-moderation-and-safety.md](07-moderation-and-safety.md) (enforcement).

---

## 1. Regulatory landscape (India, as of 2026)

The HANDOFF's "IT Rules 2021" framing is **outdated for games.** Current state:

### 1.1 Promotion and Regulation of Online Gaming Act, 2025 + Rules, 2026
- Act enacted **Aug 2025**; **Online Gaming Rules, 2026** in force **1 May 2026**; enforced by
  the new **Online Gaming Authority of India (OGAI)**.
- Three buckets: **online money games — banned** (criminal penalties for offering/advertising);
  **e-sports — permitted, registration required**; **online social games — permitted.**
- **Katha = an "online social game" / interactive story.** No wagering, no real-money stake, no
  payout. We sit in the **permitted** lane. **Design constraint:** monetization stays
  subscription / story-pack only; **no loot boxes framed as gambling, no real-money mechanics,
  no wagering** — anything that could reclassify us as a "money game" is forbidden by design
  ([10-business-and-pitch.md](10-business-and-pitch.md)).
- **Action:** confirm whether any registration/notification to OGAI applies to social games at
  our scale; monitor as Rules are clarified.

### 1.2 Digital Personal Data Protection (DPDP) Act, 2023
- Governs personal data, with specific protections for **minors** (parental consent for users
  under 18; restrictions on tracking/targeted ads to children).
- Drives Katha's **data-minimization** design (§3) and the **age-gate** (§4).

### 1.3 Intermediary / content obligations
- IT Rules 2021 still relevant for intermediary duties, grievance redressal, and unlawful-content
  takedown — Katha publishes a **grievance contact** and removes unlawful content promptly.
- General laws still apply: provisions on outraging religious feelings, obscenity, hate speech.
  The fidelity + moderation stack ([04-cultural-fidelity.md](04-cultural-fidelity.md), [07-moderation-and-safety.md](07-moderation-and-safety.md)) is how we stay clear.

---

## 2. Content & IP

- **Phase 1 (Vikram aur Betaal):** grounded in **public-domain** sources (Burton 1870, Forbes,
  Tawney's Kathāsaritsāgara) — see [06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md) §2. Clean.
- **Phase 2 (Mahabharata):** corpus = **public-domain Ganguli**; BORI critical-edition structure
  and Debroy used as **non-redistributed reference only** — see [02-data-pipeline.md](02-data-pipeline.md) §1. Clean,
  *provided* the wall between redistributed (Ganguli) and reference (Debroy) holds.
- **Provenance log** (`data/raw/SOURCES.md`) documents every source's license and date.
- **Generated art/voice:** confirm the licensing/usage terms of image-gen tools (Midjourney/Flux)
  and Sarvam for **commercial** use and Play Store distribution; keep records. Avoid training/
  output that mimics a living artist's protected style.
- **Original work** (authored tales, character bibles, art) — Katha owns; keep contributor
  agreements for any freelancers/advisors (IP assignment + credit).

---

## 3. Data & privacy (design, not just policy)
- **No verbatim conversation storage.** Store **vectorized summaries** + hashes, not raw player
  transcripts ([01-architecture.md](01-architecture.md) §5). Minimizes DPDP exposure and is itself a fidelity/privacy
  selling point.
- **Minimal PII:** device_id + language + game state; no real name/email required to play.
- **Voice data:** audio sent to Sarvam for STT is transient; don't retain raw audio beyond the
  turn; document Sarvam's data-handling terms.
- **Retention & deletion:** define retention windows; provide a data-deletion path (DPDP right).
- **Regional hosting:** prefer India-region data residency where feasible (Sarvam is
  India-sovereign — a plus).

---

## 4. Age & safety
- **Age gate 13+** (neutral age-screen; consider higher/parental-consent handling per DPDP for
  under-18). Phase 1 is broadly family-friendly; Phase 2's war themes still target 13+.
- **Content rating:** target an appropriate Play Store / IARC rating; the cremation-ground
  setting (Phase 1) and war (Phase 2) are *atmospheric, not graphic* ([06-phase1-vikram-betaal.md](06-phase1-vikram-betaal.md) §8).
- **Self-harm handling:** the one moderation case that may break immersion to surface help
  ([07-moderation-and-safety.md](07-moderation-and-safety.md) §1).

---

## 5. Documents to ship before launch
- [ ] **Terms of Service** — incl. acceptable-use (no abuse, no attempts to elicit disrespectful
      content), the social-game (no-real-money) nature, and limitation of liability.
- [ ] **Privacy Policy** — DPDP-aligned; what's collected, why, retention, deletion, Sarvam/LLM
      sub-processors named.
- [ ] **Community / Respect Guidelines** — plain-language, tied to the strike system.
- [ ] **Public Fidelity Statement** — reverence + sourcing ([04-cultural-fidelity.md](04-cultural-fidelity.md) §8).
- [ ] **Grievance redressal** — named contact + response SLA (intermediary obligation).
- [ ] **Contributor/advisor agreements** — IP assignment, credit, confidentiality.

---

## 6. Compliance checklist by phase

**Phase 1 (Vikram aur Betaal) — before soft launch**
- [ ] Lawyer review: social-game classification; OGAI notification (if any); ToS/Privacy.
- [ ] DPDP data-minimization implemented; deletion path live.
- [ ] Age gate + content rating.
- [ ] Grievance contact published; takedown path tested.
- [ ] Public-domain provenance documented.

**Phase 2 (Mahabharata) — additional, gated by graduation ([05-phasing-roadmap.md](05-phasing-roadmap.md) §4)**
- [ ] Re-review under religious-feelings / content law with the actual scripts.
- [ ] Cultural Advisory sign-off on record.
- [ ] Ganguli/Debroy redistribution wall verified.
- [ ] Incident-response + comms plan rehearsed.

---

## 7. Open decisions
1. **Entity & registration** — when to incorporate (Pvt Ltd vs LLP); affects fundraising,
   Startup India / SISFS eligibility ([10-business-and-pitch.md](10-business-and-pitch.md)).
2. **OGAI registration applicability** — confirm with counsel whether social games must notify.
3. **Commercial-use terms** for each AI/art/voice vendor — get in writing before monetizing.
