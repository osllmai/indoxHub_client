# Changelog

All notable changes to IndoxHub Python Client will be documented in this file.



## [0.2.3] - 2026-08-27

### Fixed

- **Every write call was failing against the live API.** Request URLs were
  built without a trailing slash (`/api/v1/chat/completions`), and the
  server's slashless catch-all is CSRF-protected, so each POST got a
  `403` HTML page instead of a redirect. All paths now end in `/`, with the
  query string kept after the slash (`videos/jobs/?limit=20`). Covers every
  method, including `resemble.*`, plus the hardcoded `/auth/api-key/` and
  `/auth/token/` URLs.

### Changed

- `pytest.ini` `testpaths` pointed at `indoxhub/tests` and
  `indoxhub_server/tests`, neither of which exists — a bare `pytest` run
  collected nothing. Now `tests`.
- Removed `requirements.txt`: a UTF-16 `pip freeze` of an mkdocs docs
  environment, referenced by nothing and unrelated to the package. Runtime
  deps live in `pyproject.toml`; `pytest` is now declared under the `dev`
  extra.

## [0.2.2] - 2026-05-02

### Notes

- **Republish of the v0.2.1 cleanup work.** v0.2.1 was already on PyPI
  (uploaded manually via `twine upload` on 2026-04-27) before this
  cleanup landed in git, so the cleaned-up artifacts had to ship as a
  fresh patch rather than overwriting v0.2.1. No public API differences
  vs v0.2.1; only metadata + type hints + tests are touched.

### Changed

- Synced `__version__` in `indoxhub/__init__.py` with `pyproject.toml`
  (was drifted at `0.2.0`).
- `pyproject.toml` URLs corrected to point at `osllmai/indoxHub_client`
  (Homepage / Repository / Issues).

### Fixed

- Type hints: annotated every `data` / `request_params` / `filtered_kwargs`
  dict in `client.py` as `Dict[str, Any]` so dynamic kwarg splat into
  `requests.Session.request(**...)` no longer triggers 28 mypy `[arg-type]`
  errors. Replaced the `Optional[callable]` typo with
  `Optional[Callable[[Dict[str, Any]], None]]` on `wait_for_video_job`.
- Replaced 3 bare `except:` clauses in `client.py` with
  `except (ValueError, json.JSONDecodeError):` for safer error handling.
- Removed unused imports (`datetime`, `timedelta`, `ProviderError`).
- Test suite: `tests/unit/test_client.py::TestClient` is now green.
  Added an autouse `_stub_authenticate` fixture so `Client.__init__` no
  longer attempts a live auth network call during unit tests, and fixed
  the call-arg position assertion in `test_speech_to_text_with_optional_params`.
  Suite is now 98 passed, 4 skipped (was 4 failed + 9 errored).

## [0.2.1] - 2026-04-27

### Added

- **R2 mirror surface** — Resemble responses now expose `audio_url` (presigned
  Cloudflare R2 URL) and `expires_at` (ISO 8601 timestamp). Affected methods:
  `tts.synthesize`, `audio_jobs.get_enhance` / `get_edit`, `watermark.get_apply`.
  Mirroring is server-side, lazy + idempotent — first GET after job completion
  writes to R2, subsequent GETs return the same R2 URL.
- **`uploads.create(file_path, purpose=None)`** — new `purpose` parameter
  controls retention. Pass `purpose="voice_clone"` to land voice-clone source
  recordings under `voice-recordings/` with **PERMANENT** retention. Other
  values: `stt_input` (30d), `watermark_input` (7d), `audio_job_input` (7d).
  Default (no purpose): `uploads/` prefix, 30-day retention.
- Docstring updates noting the new fields and per-asset retention model.

### Changed

- Maintainer email: `support@indoxhub.com`.

## [0.2.0] - 2026-04-22

### Added

- **Resemble AI namespace** at `client.resemble.*` covering 13 endpoint groups (~67 endpoints):
  text-to-speech (sync synth, voice listing), speech-to-text (async jobs),
  audio enhance + edit, deepfake detection / content intelligence / audio
  source tracing, watermark apply + detect, identity (beta) search/enroll/CRUD,
  voice cloning + voice design (Business-plan gated), recordings (training audio),
  projects + nested clips, agents + tools + webhooks + knowledge base, file uploads.
- `ResembleBusinessPlanError` exception raised when the deployment's
  `RESEMBLE_BUSINESS_PLAN_ACTIVE` flag is off and a gated capability is called.
- 77 unit tests covering every Resemble method (mocked).

### Notes

- BYOK is not supported on Resemble routes (server uses a single account key).
- WebSocket TTS streaming and live agent dispatch are intentionally not exposed.

## [0.1.40]

### Changed

- Package name changed from `indoxrouter` to `indoxhub`

## [0.1.39] - 2025-11-09

### Added

- Video generation via API support
- New image models integration

### Added

- Video generation support with multiple providers (OpenAI, Google, Amazon)
- Asynchronous video processing with job status tracking
- Enhanced image generation with provider failover
- Better error handling and retry logic
- Improved logging and debugging capabilities
