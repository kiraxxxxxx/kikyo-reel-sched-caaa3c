import json, urllib.request, urllib.parse
from pathlib import Path

token = json.loads(Path("/Users/yoshihashiryou/meguriwa_test/MEGURIWA_OS/000_Bible/credentials/slack_kikyoya_user.json").read_text())["user_token"]
q = urllib.parse.urlencode({"channel": "C0BC2TC67AA", "ts": "1789016264.818349", "limit": 50})
req = urllib.request.Request("https://slack.com/api/conversations.replies?" + q,
                             headers={"Authorization": "Bearer " + token})
with urllib.request.urlopen(req, timeout=30) as f:
    d = json.load(f)
msgs = d.get("messages", [])
print("ok:", d.get("ok"), "replies:", len(msgs))
for m in msgs[-3:]:
    print("---", m.get("ts"), (m.get("user") or m.get("bot_id")))
    print((m.get("text") or "")[:300])
