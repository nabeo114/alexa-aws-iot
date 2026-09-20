#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$ROOT_DIR/build/lambda"
DIST_DIR="$ROOT_DIR/dist"
ARTIFACT_NAME="alexa-aws-iot-lambda.zip"
ARTIFACT_PATH="$DIST_DIR/$ARTIFACT_NAME"

if ! command -v zip >/dev/null 2>&1; then
  echo "Error: zip command is required but not installed." >&2
  exit 1
fi

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Build dependencies for the Lambda Linux x86_64 runtime, regardless of the local development OS.
python -m pip install --upgrade -r "$ROOT_DIR/requirements.txt" -t "$BUILD_DIR" --no-user \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.12 \
  --only-binary=:all:
cp -R "$ROOT_DIR/src" "$BUILD_DIR/src"

find "$BUILD_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$BUILD_DIR" -type f -name "*.pyc" -delete
rm -rf "$BUILD_DIR"/*.dist-info

rm -f "$ARTIFACT_PATH"
(
  cd "$BUILD_DIR"
  zip -rq "$ARTIFACT_PATH" .
)

echo "Created: $ARTIFACT_PATH"
