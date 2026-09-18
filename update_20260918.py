"""2026-09-17 定例の決定をスケジュールページに反映する。
- ③秋の食卓（蒸しずし）は11月へ後ろ倒し（9/28から外す）
- ④あなたならどれから食べる を 10/4 → 9/28 へ前倒し
- 10/4 の枠は未確定（熊澤さんの自作を置くのか等）→ 確認中の枠として表示
- 全動画をナレーションなし（BGMのみ）版に差し替えた旨を明記
"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent
p = D / "index.html"
s = p.read_text(encoding="utf-8")

cards = re.findall(r'<article class="card">.*?</article>', s, re.S)
assert len(cards) == 6, len(cards)
by = {}
for c in cards:
    d = re.search(r'class="dd">([^<]+)<', c).group(1)
    by[d] = c

# --- 9/28 を ④ に差し替え（10/4のカードを日付だけ変えて使う）
new928 = by["10/4"].replace('<span class="dd">10/4</span><span class="ww">日</span>',
                            '<span class="dd">9/28</span><span class="ww">月</span>')
new928 = new928.replace(
    "<p class=\"note\">店名の読み、具材名（麩→紅梅麩）、イラストの3点を修正した版で投稿します。字幕・ナレーションともに「紅梅麩」です。</p>",
    "<p class=\"note\">9/17のお打ち合わせで、蒸しずしの回を11月に移すことになったため、この回を9/28に前倒ししています。店名の読み・具材名（麩→紅梅麩）・イラストを修正した版です。</p>")

# --- 10/4 は確認中の枠に
new104 = """<article class="card">
  <div class="left">
    <div class="date"><span class="dd">10/4</span><span class="ww">日</span></div>
    <span class="badge b-cl">相談中</span>
    <p class="who">制作：未定</p>
  </div>
  <div class="mid"><div class="novid">この回の内容を<br>ご相談させてください</div></div>
  <div class="right">
    <h2>この回をどうするか</h2>
    <p class="cap">（内容が決まっていません）</p>
    <p class="note">9/28に「あなたなら、どれから食べますか」を前倒ししたため、この枠が空いています。熊澤さんが1本作られるか、こちらで用意するか、お知らせください。</p>
  </div>
</article>"""

order = ["9/19", "9/22", "9/25", "9/28", "10/1", "10/4"]
built = {"9/19": by["9/19"], "9/22": by["9/22"], "9/25": by["9/25"],
         "9/28": new928, "10/1": by["10/1"], "10/4": new104}

start = s.index(cards[0])
end = s.index(cards[-1]) + len(cards[-1])
s = s[:start] + "\n".join(built[d] for d in order) + s[end:]

# --- 動画をナレなし版に差し替え（ファイル名は同じ、中身を入れ替える運用）
old_lead = "<b>日付・キャプション・並び順について、気になるところがあればお知らせください。</b></p>"
new_lead = ("<b>日付・キャプション・並び順について、気になるところがあればお知らせください。</b><br>"
            "動画は、9/17のお打ち合わせのとおり<b>ナレーションを外してBGMのみ</b>にしています。</p>")
assert s.count(old_lead) == 1
s = s.replace(old_lead, new_lead)

# --- 補足
old_foot = "・9月22日は、カレンダーどおり熊澤さんが作られる回です。<br>"
new_foot = ("・9月22日は、カレンダーどおり熊澤さんが作られる回です。<br>\n"
            "・蒸しずしの回（秋の食卓）は、11月に回します。素材はそのまま保管しています。<br>")
assert s.count(old_foot) == 1
s = s.replace(old_foot, new_foot)

p.write_text(s, encoding="utf-8")
print("updated:", [re.search(r'class="dd">([^<]+)<', c).group(1)
                   for c in re.findall(r'<article class="card">.*?</article>', s, re.S)])
