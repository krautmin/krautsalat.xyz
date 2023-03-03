# krautsalat.xyz
Personal (portfolio) page built with [Quart](https://github.com/pallets/quart), [MongoDB](https://github.com/mongodb/mongo), [TailwindCSS](https://github.com/tailwindlabs/tailwindcss) & [HTMX](https://github.com/bigskysoftware/htmx). In a nutshell this project exists because i wanted to explore asyncio, ASGI and NoSQL databases and deviate from what i already know quite well (WSGI, Django + PostgreSQL).

## Implemented Features
 - based on [Python](https://github.com/python) 3.10 and the [Quart](https://github.com/pallets/quart) async micro-framework
 - runs with [hypercorn](https://github.com/pgjones/hypercorn) and [uvloop](https://github.com/MagicStack/uvloop)
 - [MongoDB](https://github.com/mongodb/mongo) as database with [Motor](https://github.com/mongodb/motor) as async driver and [Beanie](https://github.com/roman-right/beanie) as ODM
 - persistent session management with [Quart-Session](https://github.com/kroketio/quart-session) and [Redis](https://github.com/redis/redis)
 - data classes and validation with [Pydantic](https://github.com/pydantic/pydantic)
 - JSON-API with request and response validation as well as auto-generated [OpenAPI](https://github.com/OAI/OpenAPI-Specification) docs using [Quart-Schema](https://github.com/pgjones/quart-schema)
 - frontend build with [TailwindCSS](https://github.com/tailwindlabs/tailwindcss) and [daisyui](https://daisyui.com/)
 - server-side rendering with [Jinja](https://github.com/pallets/jinja) made SPA-like with [HTMX](https://github.com/bigskysoftware/htmx)
 - simple caching implementation using [aiocache](https://github.com/aio-libs/aiocache) and Redis
 - simple authentication and user management to allow live editing
 - distributed task queue with [arq](https://github.com/samuelcolvin/arq) and Redis
 - simple mail integration with [aiosmtplib](https://github.com/cole/aiosmtplib)

## In Progress
 - [Editor.js](https://github.com/codex-team/editor.js) for creating posts/editing content

## Planned
 - Page analytics with [plausible.io](https://github.com/plausible/analytics)
 - admin dashboard
 - comment function

## Missing
 - content... 😢