"""Wait for explicitly supplied local HTTP endpoints, bounded to 60 seconds."""
import sys
import time
import urllib.request
for url in sys.argv[1:]:
    for attempt in range(60):
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status < 400:
                    break
        except (OSError, ValueError):
            pass
        time.sleep(1)
    else:
        raise SystemExit(f'Server not ready: {url}')
