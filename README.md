# fastapi-practice

A small FastAPI practice project for posting media. Files are uploaded to ImageKit, and each upload is saved as a post (caption, URL, file type) in a SQLite database through async SQLAlchemy.

## Tech stack

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) for dependencies (`pyproject.toml`, `uv.lock`)
- FastAPI, served with Uvicorn
- SQLAlchemy (async) with aiosqlite
- ImageKit (`imagekitio`) for file storage
- python-dotenv for loading `.env`
- `fastapi-users[sqlalchemy]` is listed as a dependency but is not used in the code yet

## Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | `/upload` | Upload a file (multipart form: `file`, optional `caption`). Sends it to ImageKit, stores a post, and returns it. `file_type` is `video` for `video/*` content types, otherwise `photo`. |
| GET | `/feed` | List all posts, sorted by `id` descending. |
| DELETE | `/posts/{post_id}` | Delete a post by its UUID. Returns 404 if it does not exist. |

## Getting started

Install dependencies:

```sh
uv sync
```

Create a `.env` file in the project root with your ImageKit key (see Environment variables), then start the server:

```sh
uv run main.py
```

`main.py` runs Uvicorn on `app.app:app` at `http://127.0.0.1:8000` with auto-reload. You can also run it directly with `uv run uvicorn app.app:app --reload`.

Interactive API docs are at `http://127.0.0.1:8000/docs`.

## Database

By default the app uses a SQLite file, `test.db`, in the directory you start the server from (`sqlite+aiosqlite:///./test.db`). The file is in `.gitignore`.

There are no migrations. On startup, the app's lifespan handler calls `create_db_and_table()`, which runs `Base.metadata.create_all` and creates any missing tables. Currently there is one table, `posts` (`id` UUID, `caption`, `url`, `file_type`, `file_name`, `created_at`).

## Environment variables

| Name | Used in | Purpose |
| ---- | ------- | ------- |
| `IMAGEKIT_PRIVATE_KEY` | `app/images.py` | ImageKit private key for uploads. |
| `DATABASE_URL` | `app/db.py` | Optional. Overrides the default SQLite URL. |

`.env` is loaded by `app/images.py` and is in `.gitignore`. `app/db.py` reads `DATABASE_URL` before that happens, so set `DATABASE_URL` in your shell environment rather than in `.env`.

## Project structure

```
main.py           Starts Uvicorn with the app
app/
  app.py          FastAPI app, lifespan, and routes
  db.py           Engine, session dependency, Post model, table creation
  images.py       ImageKit client
  schemas.py      Pydantic PostCreate model (not used by any route yet)
  users.py        Empty placeholder
pyproject.toml    Project metadata and dependencies
uv.lock           Locked dependency versions
```
