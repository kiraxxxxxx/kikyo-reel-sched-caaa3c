"""投稿スケジュールのURLを、9/10にリール5本を送った動画スレッドへ返信する。
ボスGO済み（2026-09-16）。出口＝人ゲートを通過した文面のみを送る。
"""
import json, urllib.request
from pathlib import Path

CRED = Path("/Users/yoshihashiryou/meguriwa_test/MEGURIWA_OS/000_Bible/credentials/slack_kikyoya_user.json")
CH = "C0BC2TC67AA"
THREAD = "1789016264.818349"   # 2026-09-10 リール5本の投稿
OUT = Path(__file__).resolve().parent / "slack_post_result.json"

TEXT = """熊澤さん

リールの投稿スケジュールを、動画を見ながら日付を確認できるページにまとめました。

▼投稿スケジュール（確認用）
https://kiraxxxxxx.github.io/kikyo-reel-sched-caaa3c/

・日付ごとに、その日投稿する動画・キャプション・ハッシュタグを並べています
・動画はページ上でそのまま再生できます
・検索には出ない設定にしていますので、このURLをご存知の方だけがご覧になれます

この並びで進めてよいか、入れ替えたい日があればお知らせください。ご確認いただいてから投稿を始めます。

ナレーションが不要でしたら、音声を外した版に差し替えてから投稿しますので、あわせてお知らせください。"""

token = json.loads(CRED.read_text())["user_token"]
body = json.dumps({"channel": CH, "thread_ts": THREAD, "text": TEXT,
                   "unfurl_links": False, "unfurl_media": False}).encode()
req = urllib.request.Request("https://slack.com/api/chat.postMessage", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8",
                                      "Authorization": "Bearer " + token})
with urllib.request.urlopen(req, timeout=30) as f:
    r = json.load(f)
print("ok:", r.get("ok"), "ts:", r.get("ts"), "err:", r.get("error"))
if r.get("ok"):
    OUT.write_text(json.dumps({"channel": CH, "thread_ts": THREAD, "ts": r["ts"],
                               "text": TEXT}, ensure_ascii=False, indent=2))
