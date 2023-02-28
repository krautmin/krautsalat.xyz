#!/bin/bash
cd /app/
/opt/venv/bin/hypercorn run:application --config hypercorn.dev.toml