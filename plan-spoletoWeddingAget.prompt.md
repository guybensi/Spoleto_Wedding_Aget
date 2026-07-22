## Plan: Spoleto WhatsApp Travel Assistant

Build a production-quality private-group travel assistant with OpenClaw as the primary runtime, the native WhatsApp plugin as the transport, and Python limited to OCR and knowledge-ingestion support services. The design is single-tenant, Dockerized for one VPS, prompt-configurable, and reusable for future trips by replacing trip datasets and config rather than changing source logic. I saved the full working plan in session memory for handoff.

**Architecture**
- Runtime: OpenClaw Gateway is the control plane for WhatsApp messaging, sessions, tool orchestration, cron, and policy enforcement.
- Transport: OpenClaw native WhatsApp plugin, not Twilio or Meta Cloud API. This matches OpenClaw’s production path for mention gating, group handling, session routing, and operations.
- Support services: Python handles PNG, PDF, EXCEL ingestion, OCR, vision-assisted extraction, normalization, validation, and publish workflows only.
- Deployment: Single Linux VPS with Docker Compose, persistent volumes, backups, and a locked-down admin path.
- Trust model: one trusted operator boundary. This is a private assistant for one wedding group, not a multi-tenant or adversarial-user system.
- Data authority: private PNG, PDF, EXCEL trip assets are the source of truth. Public web data is fallback only and must never silently override trip knowledge.
- Reusability: permanent travel knowledge and trip-specific knowledge are stored separately so a future trip can be launched by swapping data folders and config.

**Engineering specification**
1. Project overview
- Purpose: answer guest questions about the wedding trip in Spoleto, logistics, local recommendations, and travel help.
- Why: reduce repetitive organizer effort and give guests one reliable place to ask.
- Priority: `P0`.
- Dependencies: WhatsApp runtime, ingestion pipeline, prompt system, core tools.
- Complexity: medium.
- Pitfalls: weak source authority rules, noisy tool access, low-quality extracted data.

2. Functional requirements
- Mention-only replies in the WhatsApp group.
  Why: avoid unsolicited chatter.
  Priority: `P0`.
  Dependencies: WhatsApp group config, mention patterns.
  Complexity: low.
  Pitfalls: missed aliases or accidental always-on behavior.
- Private trip Q&A from PNG-derived knowledge.
  Why: this is the main product value.
  Priority: `P0`.
  Dependencies: ingestion schema, retrieval, provenance.
  Complexity: medium.
  Pitfalls: extraction drift, bad date/time normalization.
- Public web search fallback for restaurants, attractions, pharmacies, weather, local events, and hours.
  Why: guests will ask beyond your documents.
  Priority: `P0`.
  Dependencies: search/fetch wrappers, result normalization.
  Complexity: medium.
  Pitfalls: stale hours, prompt injection, mixed-source answers.
- Clear distinction between trip facts and live search results.
  Why: trust and auditability.
  Priority: `P0`.
  Dependencies: provenance model, response rules.
  Complexity: low.
  Pitfalls: blended answers without attribution.
- Never invent unknown facts.
  Why: travel/logistics errors are costly.
  Priority: `P0`.
  Dependencies: refusal rules, confidence thresholds.
  Complexity: low.
  Pitfalls: overhelpful model behavior.
- Itinerary, transport, hotel, wedding schedule, reservations, logistics, emergency contacts.
  Why: core concierge workload.
  Priority: `P0`.
  Dependencies: normalized trip schemas.
  Complexity: medium.
  Pitfalls: partial documents and conflicting revisions.
- Recommendations for restaurants, cafes, bars, attractions.
  Why: high guest demand.
  Priority: `P1`.
  Dependencies: curated list plus web fallback.
  Complexity: medium.
  Pitfalls: stale or low-quality recommendations.
- Translation English/Italian and local customs guidance.
  Why: frequent travel friction point.
  Priority: `P1`.
  Dependencies: prompt rules, model behavior.
  Complexity: low.
  Pitfalls: nuance and regional phrasing.
- Daily summaries and reminders.
  Why: reduce confusion during the trip.
  Priority: `P1`.
  Dependencies: OpenClaw cron, itinerary rendering.
  Complexity: medium.
  Pitfalls: wrong timing and duplicate sends.
- Long-term memory across the trip.
  Why: preserve useful clarifications and recurring answers.
  Priority: `P1`.
  Dependencies: memory policy, retention rules.
  Complexity: medium.
  Pitfalls: privacy leakage and noisy memory writes.
- Weather, maps links, currency conversion, pharmacy lookup.
  Why: practical support.
  Priority: `P1`.
  Dependencies: deterministic tool wrappers.
  Complexity: medium.
  Pitfalls: provider outages and rate limits.
- Flight status and richer live travel integrations.
  Why: nice-to-have, not central.
  Priority: `P2`.
  Dependencies: additional APIs.
  Complexity: medium.
  Pitfalls: cost and low MVP value.

3. Non-functional requirements
- Accuracy: every answer must trace to a trip source or a named live source.
- Security: least-privilege tool profile, sandboxed non-main sessions, no dangerous default surfaces.
- Privacy: sensitive trip and guest data protected in storage, logs, and retention policy.
- Reliability: gateway restarts safely, WhatsApp relinks recoverably, cron persists.
- Maintainability: prompts, tools, trip data, and config updated independently.
- Reusability: new trip with data replacement only.
- Observability: logs, health checks, alerts, and ingestion QA signals.
- Performance: fast doc-backed answers, acceptable latency for live-search answers.
- Cost control: deterministic preprocessing first, model usage second.

4. User stories
- A guest asks for departure time to an event and gets the exact answer from trip documents.
- A guest asks for coffee near the hotel and gets curated options first, then live options if needed.
- A guest asks for a translation into Italian.
- A guest asks whether a pharmacy is open now and gets a live, labeled result.
- An organizer replaces a PNG and republishes knowledge without touching prompts or runtime code.

5. System architecture
- Inbound mention arrives in WhatsApp group.
- OpenClaw routes the message into the group session.
- Retrieval first loads trip-specific context from rendered knowledge bundles.
- If the answer is incomplete, bounded public tools are called.
- Response labels whether facts came from trip documents or live search.
- Outbound answer is returned to the same group thread.

6. Folder structure
- `/docs/specification` for the engineering spec, ADRs, security/privacy, testing, and operations runbooks.
- `/openclaw` for gateway config and JSON5 include files.
- `/workspace` for OpenClaw bootstrap files such as `AGENTS.md`, `SOUL.md`, `TOOLS.md`, and `MEMORY.md`.
- `/prompts/base` for modular global prompt files.
- `/prompts/trips/spoleto-2026` for trip-specific overlays if needed.
- `/data/permanent` for reusable travel schemas and evergreen knowledge.
- `/data/trips/spoleto-2026/raw/png` for source PNGs.
- `/data/trips/spoleto-2026/extracted` for OCR and vision intermediates.
- `/data/trips/spoleto-2026/normalized` for reviewed structured records.
- `/data/trips/spoleto-2026/rendered` for retrieval-ready bundles.
- `/services/ingestion` for Python OCR and ETL.
- `/services/tool-api` for optional deterministic wrappers.
- `/tests` for unit, integration, and end-to-end coverage.
- `/deploy` for Docker Compose and ops assets.
- `/.github/workflows` for CI.

7. OpenClaw architecture
- One dedicated gateway instance.
- Native WhatsApp plugin with explicit group allowlist and `requireMention`.
- `session.dmScope = per-channel-peer` if multi-user DMs are enabled.
- Sandbox for non-main sessions.
- Minimal guest-facing tool policy.
- Group-triggered turns denied access to exec, browser, filesystem mutation, gateway, and cron unless explicitly justified.
- Gateway bound privately, not directly exposed to the internet.

8. Claude prompt strategy
- All assistant behavior lives in external prompt files, never hardcoded strings.
- Recommended prompt stack: `system.md`, `safety.md`, `personality.md`, `response_style.md`, `itinerary_rules.md`, `trip_context.md`.
- `system.md`: mission, authority order, truthfulness.
- `safety.md`: privacy, hallucination prevention, source conflict handling.
- `personality.md`: warm concierge tone for wedding guests.
- `response_style.md`: concise formatting and explicit source labeling.
- `itinerary_rules.md`: time/date reasoning and schedule conflict handling.
- `trip_context.md`: trip-agnostic template slots for injected knowledge.
- Best practices: small focused files, prompt versioning, regression tests, clear ownership, no logic hidden in prose.

9. Knowledge ingestion pipeline
- Intake PNGs with manifest, naming, and checksums.
- Classify each image by document type.
- Run OCR and/or vision extraction.
- Normalize to canonical schemas.
- Attach provenance and confidence to every field.
- Send low-confidence records to human review.
- Publish reviewed records into rendered knowledge bundles.
- Rebuild only affected slices on source changes.

10. OCR / vision strategy
- OCR-first for clean text-heavy images.
- Vision-assisted extraction for layout-heavy or low-quality assets.
- Keep raw extraction outputs for audits.
- Use confidence thresholds to decide auto-publish versus human review.
- Highest risks: date/time corruption, column merges, phone number errors, rotations, stylized layouts.

11. Memory strategy
- Permanent knowledge: reusable schemas and evergreen destination facts.
- Trip knowledge: trip-specific reviewed records.
- Conversation memory: OpenClaw sessions for continuity.
- Curated long-term memory: recurring clarifications and approved summaries only.
- Do not auto-store arbitrary guest chatter.
- Define post-trip retention and purge rules before launch.

12. Tool integration plan
- Web search with trusted provider and normalization.
- Weather API.
- Maps link generation.
- Currency conversion.
- Translation, mostly model-native.
- Pharmacy and emergency lookup via bounded search workflow.
- Daily reminders and summaries via OpenClaw cron.
- Flight status deferred unless a strong provider is selected later.

13. External services
- Anthropic Claude models.
- Search provider such as Tavily, Brave, or Exa.
- Weather provider such as Open-Meteo or WeatherAPI.
- FX provider.
- Optional OCR engine plus model-based verification.
- GitHub Actions and container registry.

14. Security considerations
- One gateway per trust boundary.
- Prefer a dedicated WhatsApp number.
- Mention-only in groups, DMs disabled or allowlisted by default.
- Loopback-bound gateway with authenticated admin path.
- Sandbox non-main sessions.
- Minimal tool profile for guest-facing flows.
- Secrets outside source control.
- Run OpenClaw security audit before production.

15. Privacy considerations
- Treat phone numbers, hotels, reservations, transport, and emergency contacts as sensitive.
- Keep log redaction on.
- Restrict memory writes.
- Encrypt backups.
- Separate raw source assets from rendered assistant context.
- Archive or purge data after the trip.

16. Deployment strategy
- Single VPS, Docker Compose.
- Services: OpenClaw gateway, optional ingestion worker, optional reverse proxy, optional monitoring.
- Persistent volumes for state, trip data, workspace, and logs.
- Nightly encrypted backups.
- Staging environment with a test WhatsApp number or small test group before production.

17. Testing strategy
- Unit tests for schemas, normalization, prompt assembly.
- Fixture tests for PNG extraction.
- Integration tests for intake-to-publish flow.
- Tool contract tests with mocked providers.
- Prompt regression tests for truthfulness, source labeling, and mention-only behavior.
- End-to-end acceptance tests for top guest scenarios.

18. Logging and monitoring
- Structured logs for ingestion, retrieval, tool calls, cron, and outbound delivery.
- Gateway health, WhatsApp health, cron health, ingestion health.
- Alerts for disconnects, OCR failures, auth failures, and missed reminders.
- Start simple; full observability stack is not required for MVP.

19. Future roadmap
- Embeddings-backed retrieval if needed.
- Guest-uploaded image understanding.
- Personalized DM concierge mode with stronger isolation.
- Flight and rail integrations.
- Admin review UI.
- Multi-language prompt packs.

20. Risks and mitigations
- OCR errors: mitigate with provenance, confidence thresholds, and review.
- Private/public source conflicts: mitigate with strict authority order.
- Prompt injection from web: mitigate with strong model, normalized tool outputs, and minimal tools.
- WhatsApp instability: mitigate with runbooks, health monitoring, and relink procedures.
- Privacy leakage: mitigate with memory discipline, session isolation, and retention controls.
- Cost creep: mitigate with pre-rendered context and narrow MVP scope.

21. MVP definition
- Included: mention-only WhatsApp group assistant, PNG ingestion, trip-first Q&A, labeled live-search fallback, recommendations, translation, weather, maps links, pharmacy and emergency help, daily reminders/summaries, Docker deployment, backups, and monitoring baseline.
- Excluded: flight status by default, autonomous booking, browser automation, guest-profile personalization, voice/calling, full embeddings stack, public access, multi-tenant support.

22. Development milestones
- M1 architecture approval.
- M2 repo scaffold and OpenClaw Docker runtime.
- M3 WhatsApp link and mention-only behavior verified.
- M4 prompt modules assembled externally.
- M5 ingestion pipeline produces reviewed structured knowledge.
- M6 end-to-end trip Q&A works.
- M7 public tools and source labeling shipped.
- M8 reminders, summaries, and memory curation shipped.
- M9 hardening, backups, monitoring, and pilot.
- M10 production launch.

**GitHub roadmap**
1. Repo scaffold and docs baseline.
2. OpenClaw config layout with includes.
3. WhatsApp plugin install and runbook.
4. Group allowlist and mention-only activation.
5. Model and sandbox policy.
6. Prompt file taxonomy and loader contract.
7. Core prompt drafting.
8. Prompt regression suite.
9. Canonical trip schemas.
10. Provenance schema.
11. PNG intake manifest.
12. OCR engine integration.
13. Vision extraction fallback.
14. Normalization pipeline.
15. Confidence scoring and review queue.
16. Publish pipeline to rendered knowledge.
17. Private retrieval context builder.
18. Permanent knowledge overlay.
19. Search provider integration.
20. Weather tool.
21. Maps link tool.
22. Currency conversion tool.
23. Pharmacy lookup workflow.
24. Emergency info workflow.
25. Memory policy and retention.
26. Daily summary cron design.
27. Daily reminder cron design.
28. Secrets and config management.
29. Backup and restore runbook.
30. Monitoring and alerting baseline.
31. Unit and integration tests.
32. End-to-end scenario tests.
33. Pilot group dry run.
34. Production readiness checklist.
35. Launch and trip-time operations review.

If you want, I can refine this into either:
1. A stricter MVP-only spec with less scope.
2. A more detailed issue breakdown with acceptance criteria per GitHub issue.
3. A decision record pack for the key architectural choices before implementation.
