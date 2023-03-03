#!/bin/bash
cd /project/
/opt/venv/bin/hypercorn run:app --config /project/config/hypercorn.toml