#!/bin/bash
# Fetch Codemagic build log artifact
# Usage: cm-build-log.sh BUILD_ID [ARTIFACT_NAME]
set -e

BUILD_ID="${1:?Usage: cm-build-log.sh BUILD_ID [ARTIFACT_NAME]}"
ARTIFACT_NAME="${2:-build.log}"
EXPIRES_AT=$(( $(date +%s) + 3600 ))

# Get artifact URL from build
ARTIFACT_URL=$(curl -s "https://api.codemagic.io/builds/$BUILD_ID" \
  -H "x-auth-token: $CM_API_TOKEN" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for a in data.get('build', {}).get('artefacts', []):
    url = a.get('url', '')
    name = a.get('name', '')
    if '$ARTIFACT_NAME' in name or '$ARTIFACT_NAME' in url:
        print(url)
        break
")

if [ -z "$ARTIFACT_URL" ]; then
    echo "Artifact '$ARTIFACT_NAME' not found. Available artifacts:"
    curl -s "https://api.codemagic.io/builds/$BUILD_ID" \
      -H "x-auth-token: $CM_API_TOKEN" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for a in data.get('build', {}).get('artefacts', []):
    print(f\"  - {a.get('name', '?')}: {a.get('url', '?')}\")
"
    exit 1
fi

# Get public download URL
DOWNLOAD_URL=$(curl -s -X POST "https://api.codemagic.io/artifacts/$ARTIFACT_URL/public-url" \
  -H "Content-Type: application/json" \
  -H "x-auth-token: $CM_API_TOKEN" \
  -d "{\"expiresAt\": $EXPIRES_AT}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('url', ''))
")

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Failed to get download URL"
    exit 1
fi

# Download and print
curl -sL "$DOWNLOAD_URL"
