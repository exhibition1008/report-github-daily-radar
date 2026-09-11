import urllib.request
import json

url = "https://api.github.com/repos/exhibition1008/report-github-daily-radar/actions/runs"
req = urllib.request.Request(url, headers={"User-Agent": "Radar-Checker"})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        runs = data.get("workflow_runs", [])
        print("Total runs:", len(runs))
        for r in runs[:3]:
            print(f"Run #{r['run_number']} ({r['name']}): Status = {r['status']}, Conclusion = {r['conclusion']}")
            print(f"URL: {r['html_url']}")
except Exception as e:
    print("Error fetching actions runs:", e)
