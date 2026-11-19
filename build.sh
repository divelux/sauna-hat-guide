#!/bin/sh
# Rebuild everything: HTML from build.py, PDFs via Playwright (one Chromium, closed right away), metadata via pypdf.
# Playwright is looked up through NODE_PATH; set PLAYWRIGHT_NODE_PATH if it lives elsewhere.
set -e
cd "$(dirname "$0")"
python3 build.py
NODE_PATH="${PLAYWRIGHT_NODE_PATH:-/opt/carmax/node_modules}" node render.js
python3 finalize.py
