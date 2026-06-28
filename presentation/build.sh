#!/usr/bin/env bash
# Build the Eclipse Zenoh Marp deck into a publishable site directory.
#
# Usage (run from the repository root):
#   presentation/build.sh [output_dir]
#
# The output directory mirrors the repo layout so the deck's relative
# "../assets/..." image paths (and the SVG animations) resolve no matter which
# sub-path the site is served from:
#
#   <output_dir>/index.html              -> redirect to presentation/
#   <output_dir>/presentation/index.html -> the deck
#   <output_dir>/assets/...              -> diagrams and logos
set -euo pipefail

OUT="${1:-_site}"
MARP_VERSION="4.4.0"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

rm -rf "$OUT"
mkdir -p "$OUT/presentation"
cp -r assets "$OUT/assets"

npx --yes "@marp-team/marp-cli@${MARP_VERSION}" presentation/zenoh.md \
  -o "$OUT/presentation/index.html"

cat > "$OUT/index.html" <<'EOF'
<!doctype html>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=./presentation/">
<link rel="canonical" href="./presentation/">
<title>Eclipse Zenoh presentation</title>
<a href="./presentation/">Eclipse Zenoh presentation</a>
EOF

echo "Built deck into $OUT"
