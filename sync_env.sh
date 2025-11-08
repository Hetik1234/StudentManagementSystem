#!/bin/bash
# -----------------------------------------------------------------------------
# sync_env.sh — Robust sync of local .env to Elastic Beanstalk
# -----------------------------------------------------------------------------

set -e

echo "Syncing environment variables from .env → Elastic Beanstalk"

if [ ! -f .env ]; then
  echo "No .env file found in current directory!"
  exit 1
fi

EB_ENV_ARGS=""

# Read file line-by-line
while IFS= read -r line || [ -n "$line" ]; do
  # Skip empty lines and comments
  if [[ -z "$line" || "$line" =~ ^# ]]; then
    continue
  fi

  # Ensure line contains '='
  if [[ "$line" != *"="* ]]; then
    echo "Skipping invalid line: $line"
    continue
  fi

  key="${line%%=*}"
  value="${line#*=}"

  # Trim whitespace
  key="$(echo -e "${key}" | tr -d '[:space:]')"
  value="$(echo -e "${value}" | tr -d '\r')"

  # Sanity check: key must start with a letter or underscore
  if [[ ! "$key" =~ ^[A-Za-z_] ]]; then
    echo "⚠️ Skipping invalid key: $key"
    continue
  fi

  # Escape double quotes in value
  value=$(echo "$value" | sed 's/"/\\"/g')

  EB_ENV_ARGS+="$key=\"$value\" "
done < .env

echo "Syncing these variables:"
echo "$EB_ENV_ARGS"

eb setenv $EB_ENV_ARGS

echo "Environment variables synced successfully!"
