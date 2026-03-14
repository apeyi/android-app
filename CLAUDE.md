# FBAudio Project

## iOS Builds (Codemagic)

You can trigger and monitor iOS builds using the Codemagic API. The `CM_API_TOKEN` env variable is available.

### Trigger a build

```bash
curl -s -X POST https://api.codemagic.io/builds \
  -H "Content-Type: application/json" \
  -H "x-auth-token: $CM_API_TOKEN" \
  -d '{"appId": "69b57cbdee625882cf704b1b", "workflowId": "ios-build", "branch": "main"}'
```

The response contains a `buildId` — save it to check status.

### Check build status

```bash
curl -s "https://api.codemagic.io/builds/BUILD_ID" \
  -H "x-auth-token: $CM_API_TOKEN" | python3 -c "
import json, sys
b = json.load(sys.stdin).get('build', {})
print('Status:', b.get('status'))
print('Message:', b.get('message', ''))
"
```

Statuses: `queued`, `building`, `finished`, `failed`, `canceled`.

### Get build log URL

```bash
curl -s "https://api.codemagic.io/builds/BUILD_ID" \
  -H "x-auth-token: $CM_API_TOKEN" | python3 -c "
import json, sys
b = json.load(sys.stdin).get('build', {})
for step in b.get('steps', []):
    status = '✓' if step.get('status') == 'success' else '✗'
    print(f\"{status} {step.get('name')}\")
    if step.get('logUrl'):
        print(f\"  Log: {step['logUrl']}\")
"
```

### Workflow

1. Make iOS code changes in `FBAudio-iOS/`
2. Commit and push to trigger a build, or trigger manually via API
3. Check build status until finished
4. If failed, read the logs, fix, and retry
