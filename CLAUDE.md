# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Django REST backend for [vue-hallow-ethical-hacking](https://github.com/Ky7az/vue-hallow-ethical-hacking). It has four apps, each mounted under `/api/<name>/`:

- **HallowSoup** (`/api/soup/`): knowledge base
- **HallowWatch** (`/api/watch/`): security/technology watch. It scrapes external sources into `Content` items.
- **HallowPentest** (`/api/pentest/`): penetration-testing helper. It builds commands from templates and runs them over SSH on an "attacker" host.
- **HallowWriteup** (`/api/writeup/`): report creator

Other routes: `auth/` (DRF token: POST username/password and get a token back), `admin/`, and `hc/` (django-health-check).

The parent directory (`../`) holds `docker-compose.yml` (prod: gunicorn, celery worker, celery beat, postgres, redis, vue, nginx, traefik) and `docker-compose.debug.yml` (runserver, debugpy on port 5678, vite dev server on 5173).

## Commands

The Python venv lives at `.venv/`. Settings read everything from `.env` through django-environ: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_*`, and `REDIS_URL`. A Postgres database and a Redis server must be reachable even to run tests.

```bash
python manage.py runserver
python manage.py test                                    # all tests
python manage.py test HallowPentest                      # one app
python manage.py test HallowPentest.tests.test_views.TaskAPITestCase.test_list_tasks  # one test
coverage run manage.py test && coverage report            # .coveragerc omits project pkg/tests
celery -A DjangoHallowEthicalHacking worker -l info
celery -A DjangoHallowEthicalHacking beat -l info
ruff check --fix . && ruff format .                       # also run via pre-commit
```

Ruff settings: single quotes, and E501 (line length) is ignored. Bandit and Semgrep configs also exist (`.bandit`, `.semgrepignore`).

When `DEBUG` is set, `manage.py` starts a debugpy listener on `0.0.0.0:5678` in the runserver child process.

## Architecture

- **App layout:** every app has the same shape: `models.py`, `serializers.py`, `views.py` (DRF `ModelViewSet`s registered on a `DefaultRouter` in `urls.py`), `admin.py`, and `tests/` (`test_models`, `test_serializers`, `test_views`).
- **Auth and lookups:** each viewset sets `TokenAuthentication` and `IsAuthenticated` itself, because the global `REST_FRAMEWORK` settings are empty. Most viewsets look objects up by `slug`. Join or anonymous-style models use `id`.
- **Tests:** view tests use `APITestCase` with `force_authenticate`, and also assert that unauthenticated requests get 401.
- **Fixtures:** reference data ships in `<app>/fixtures/*.json` and loads by natural key. Models with fixtures define a `Manager.get_by_natural_key` and a `natural_key()`. These are slugs, except `Action`, which uses a `uuid` field. Keep that pattern when adding fixture-backed models. `entrypoint.sh` runs `migrate` and then `loaddata` for every fixture when `RUN_MIGRATIONS=1`. Only the django container sets this. If you add a new fixture file, add it to `entrypoint.sh` as well.
- **Celery:** configured in `DjangoHallowEthicalHacking/celery.py`, with Redis db 0 as the broker and `django_celery_results` (`CELERY_RESULT_BACKEND='django-db'`) storing results. Models keep a `celery_task_id` so the API can report state through `AsyncResult`.

### HallowPentest command flow
1. An `Action` holds a `command` template written with `str.format` placeholders, such as `{host}` and `{port}`.
2. `TaskSerializer.format_command` fills in `host`, `port` and `path` from the Target/TargetService and `username`/`password` from the Credential. Every other placeholder is resolved from `Parameter` rows. Lookup order, most specific first:
   1. (target, tool)
   2. (target, any tool)
   3. (any target, tool)
   4. global
   If no row matches, it raises "Missing parameter".
3. `POST /api/pentest/tasks/task_command/` previews the formatted command without running it.
4. `TaskSerializer.create` saves the `Task` and queues `HallowPentest.tasks.run_task`. That task connects to the `Attacker` over SSH with paramiko (Ed25519 key stored in `ssh_pkey`), streams stdout into `Task.output`, and saves after each chunk.
5. Deleting a Task queues `clean_task`, which runs `pgrep -f`/`kill` against the remote process.

### HallowWatch scraping
- Celery beat runs `HallowWatch.tasks.scrap_feeds` every hour. It fans out one `run_scrap` per `Feed`.
- `Source.scrap_source` picks the scraper by name: `scrap_source_<slug with - replaced by _>` (requests + BeautifulSoup). To add a source, add that method and a fixture entry in `HallowWatch/fixtures/source.json`.
- Scraped `Content` is de-duplicated by its unique `url`.

<!-- rtk-instructions v2 -->
# Command output

Command output here is condensed to save tokens, keeping every signal and
dropping costly noise. Treat it as the complete result: run commands
normally, and batch related commands into one call to avoid extra turns.
Truncated results state their recovery path in their own output. Re-run a
command as `rtk bypass <cmd>` only when its result is unusable: empty when
output was clearly expected, contradicting its exit code, or garbled.
<!-- /rtk-instructions -->