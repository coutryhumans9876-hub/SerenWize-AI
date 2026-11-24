"""Chạy 1 lần trong thư mục chứa app.py:  python patch_practice.py
Tạo modules/practice.py (nhiều bài luyện tập) và sửa mục Phòng luyện tập trong app.py.
Bản gốc được lưu thành app_truoc_khi_vá_luyen_tap.py."""
import os, re, shutil

PRACTICE = r'''"""
SerenWize-AI - Phòng luyện tập nhiều bài (hô hấp, neo giác quan, quét cơ thể, thả lỏng cơ)
Đặt file này vào modules/practice.py
"""
import streamlit.components.v1 as components

HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
:root { --ink:#2B2142; --soft:#6B5F82; --mute:#857A9B; --l100:#F3EEFF; --l200:#E8DFFC; --l300:#D6C8F7; --l400:#BDA9F0; --l600:#7F60D8; --l700:#6747BD; --line:rgba(127,96,216,.16); }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Be Vietnam Pro', Arial, sans-serif; color: var(--ink); }
.studio { padding: 22px 18px 26px; background: linear-gradient(135deg, #F6F1FF, #EAF0FF 60%, #F9E8F8); border-radius: 28px; border: 1px solid rgba(255,255,255,.9); }
.chips { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px; }
.chip { text-align: left; padding: 12px 14px; background: rgba(255,255,255,.85); border: 1px solid var(--line); border-radius: 16px; cursor: pointer; font-family: inherit; color: var(--ink); transition: transform .15s ease, border-color .15s ease; }
.chip:hover { transform: translateY(-2px); border-color: var(--l400); }
.chip.on { background: linear-gradient(135deg, #EDE5FF, #F8EBFB); border: 1.5px solid var(--l400); box-shadow: 0 10px 20px -14px rgba(103,71,189,.6); }
.chip .ic { font-size: 20px; }
.chip .nm { font-size: 14px; font-weight: 700; margin-top: 4px; }
.chip .tg { font-size: 12px; color: var(--mute); margin-top: 2px; }
.info { background: rgba(255,255,255,.7); border: 1px solid var(--line); border-radius: 18px; padding: 14px 18px; margin-bottom: 16px; }
.info h3 { margin: 0 0 6px; font-size: 17px; font-weight: 800; }
.info p { margin: 0; color: var(--soft); font-size: 13.5px; line-height: 1.7; }
.bar { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 10px; margin-bottom: 10px; }
select { padding: 9px 14px; border: 1px solid var(--l300); border-radius: 999px; background: #fff; color: var(--l700); font-family: inherit; font-size: 14px; font-weight: 600; }
button.ctl { border: none; border-radius: 999px; padding: 10px 22px; font-family: inherit; font-size: 14px; font-weight: 600; cursor: pointer; color: #fff; background: linear-gradient(135deg, var(--l600), var(--l700)); box-shadow: 0 10px 20px -10px rgba(103,71,189,.7); }
button.ctl:disabled { opacity: .45; cursor: not-allowed; box-shadow: none; }
button.ctl.reset { background: #A8A0B8; box-shadow: none; }
.timer { text-align: center; font-size: 40px; font-weight: 800; color: var(--l700); font-variant-numeric: tabular-nums; margin: 6px 0 12px; }
.stage { display: flex; justify-content: center; align-items: center; height: 230px; }
.orb { width: 170px; height: 170px; border-radius: 50%; background: radial-gradient(circle at 32% 28%, #fff 0%, #E3D8FB 32%, #A78BF0 76%, #8466DB 100%); box-shadow: 0 0 30px #BBA5F5, 0 0 60px #D9CCFA; transform: scale(.72); }
.label { text-align: center; font-size: 23px; font-weight: 800; color: var(--l700); margin-top: 8px; }
.label span { color: var(--mute); font-weight: 600; }
.detail { text-align: center; color: var(--soft); font-size: 14.5px; line-height: 1.7; margin: 8px auto 0; max-width: 560px; min-height: 50px; }
.status { text-align: center; color: #3F7A5C; font-weight: 700; font-size: 14px; min-height: 20px; margin-top: 6px; }
@media (max-width: 640px) { .chips { grid-template-columns: repeat(2, 1fr); } }
</style>
</head>
<body>
<div class="studio">
  <div class="chips" id="chips"></div>
  <div class="info"><h3 id="exName"></h3><p id="exDesc"></p></div>
  <div class="bar">
    <select id="duration">
      <option value="1">1 phút</option><option value="2">2 phút</option>
      <option value="3">3 phút</option><option value="5">5 phút</option>
    </select>
    <button class="ctl" id="start">Bắt đầu</button>
    <button class="ctl" id="pause" disabled>Tạm dừng</button>
    <button class="ctl reset" id="reset">Đặt lại</button>
  </div>
  <div class="timer" id="timer">01:00</div>
  <div class="stage"><div class="orb" id="orb"></div></div>
  <div class="label" id="label">SẴN SÀNG</div>
  <div class="detail" id="detail"></div>
  <div class="status" id="status"></div>
</div>
<script>
const EX = [
  { id: "calm", icon: "🌬️", name: "Thở nhịp nhàng 4-4", tag: "Bài cơ bản",
    desc: "Hít vào 4 giây, thở ra 4 giây. Phù hợp khi bạn muốn bình tĩnh lại nhanh.",
    hint: "Hít vào bằng mũi khi quả cầu lớn lên, thở ra nhẹ nhàng khi quả cầu nhỏ lại.",
    phases: [ { t: "HÍT VÀO", s: 4, k: 1.15 }, { t: "THỞ RA", s: 4, k: 0.72 } ] },
  { id: "long", icon: "🫁", name: "Thở ra dài 4-6", tag: "Thư giãn sâu",
    desc: "Hít vào 4 giây, thở ra chậm 6 giây. Đặt một tay lên bụng và cảm nhận bụng phồng lên, xẹp xuống.",
    hint: "Thở ra chậm như thổi nhẹ một ngọn nến, không cần gắng sức.",
    phases: [ { t: "HÍT VÀO", s: 4, k: 1.15 }, { t: "THỞ RA CHẬM", s: 6, k: 0.72 } ] },
  { id: "box", icon: "⬜", name: "Thở hộp 4-4-4-4", tag: "Tập trung",
    desc: "Hít vào, giữ, thở ra, giữ, mỗi nhịp 4 giây. Giúp tâm trí tập trung và đều nhịp.",
    hint: "Giữ nhẹ nhàng, không nín thở quá sức. Nếu thấy chóng mặt, hãy quay lại bài 4-4.",
    phases: [ { t: "HÍT VÀO", s: 4, k: 1.15 }, { t: "GIỮ NHẸ", s: 4, k: null }, { t: "THỞ RA", s: 4, k: 0.72 }, { t: "GIỮ NHẸ", s: 4, k: null } ] },
  { id: "ground", icon: "🖐️", name: "Neo giác quan 5-4-3-2-1", tag: "Khi dồn dập",
    desc: "Đưa sự chú ý về hiện tại bằng năm giác quan. Làm chậm rãi, gọi thầm tên từng thứ bạn nhận ra.",
    hint: "Không cần làm đúng hay sai, chỉ cần chú ý và gọi tên.",
    phases: [
      { t: "NHÌN", s: 20, k: 1.0, d: "Nhìn quanh và gọi thầm tên 5 thứ bạn đang thấy." },
      { t: "CHẠM", s: 20, k: 0.9, d: "Cảm nhận 4 thứ đang chạm vào bạn: ghế, quần áo, sàn nhà, bàn." },
      { t: "NGHE", s: 15, k: 1.0, d: "Lắng nghe 3 âm thanh xung quanh, gần hoặc xa." },
      { t: "NGỬI", s: 10, k: 0.9, d: "Tìm 2 mùi hương bạn nhận ra được." },
      { t: "NẾM", s: 10, k: 1.0, d: "Chú ý 1 vị trong miệng bạn lúc này." },
      { t: "HÍT THỞ CHẬM", s: 10, k: 0.9, d: "Hít vào chậm, thở ra chậm và nhận thấy bạn đang ở đây, lúc này." } ] },
  { id: "scan", icon: "🧘", name: "Quét cơ thể", tag: "Trước khi ngủ",
    desc: "Đưa sự chú ý đi qua từng vùng cơ thể và thả lỏng dần. Có thể làm khi ngồi hoặc nằm.",
    hint: "Chỉ cần quan sát cảm giác, không cần cố thay đổi điều gì.",
    phases: [
      { t: "BÀN CHÂN", s: 15, k: 1.0, d: "Chú ý đến hai bàn chân. Thả lỏng các ngón chân khi thở ra." },
      { t: "CẲNG VÀ ĐÙI", s: 15, k: 0.9, d: "Để hai chân nặng xuống, buông lỏng từng chút một." },
      { t: "BỤNG", s: 15, k: 1.0, d: "Cảm nhận bụng phồng lên, xẹp xuống theo hơi thở." },
      { t: "NGỰC VÀ LƯNG", s: 15, k: 0.9, d: "Thả lỏng ngực và lưng, để ghế hoặc giường đỡ lấy bạn." },
      { t: "VAI VÀ TAY", s: 15, k: 1.0, d: "Hạ hai vai xuống, thả lỏng cánh tay và các ngón tay." },
      { t: "CỔ VÀ MẶT", s: 15, k: 0.9, d: "Thả lỏng hàm, trán và vùng quanh mắt." } ] },
  { id: "pmr", icon: "✊", name: "Siết và thả lỏng cơ", tag: "Giải tỏa căng thẳng",
    desc: "Siết nhẹ từng nhóm cơ trong 5 giây rồi thả hoàn toàn trong 10 giây để cảm nhận sự khác biệt.",
    hint: "Chỉ siết ở mức vừa phải, không để đau. Bỏ qua vùng nào đang khó chịu.",
    phases: [
      { t: "SIẾT", s: 5, k: 1.1, d: "Nắm chặt hai bàn tay vừa phải." },
      { t: "THẢ LỎNG", s: 10, k: 0.8, d: "Mở bàn tay ra và cảm nhận sự mềm đi." },
      { t: "SIẾT", s: 5, k: 1.1, d: "Nhún hai vai lên gần tai." },
      { t: "THẢ LỎNG", s: 10, k: 0.8, d: "Thả hai vai xuống, thở ra chậm." },
      { t: "SIẾT", s: 5, k: 1.1, d: "Nhăn mặt nhẹ, mắt nhắm lại." },
      { t: "THẢ LỎNG", s: 10, k: 0.8, d: "Thả lỏng trán, mắt và hàm." },
      { t: "SIẾT", s: 5, k: 1.1, d: "Co các ngón chân lại vừa phải." },
      { t: "THẢ LỎNG", s: 10, k: 0.8, d: "Duỗi ngón chân ra, thả lỏng cả hai bàn chân." } ] }
];

const $ = (id) => document.getElementById(id);
const orb = $("orb"), label = $("label"), detail = $("detail"), status = $("status");
const timerEl = $("timer"), durSel = $("duration");
const startB = $("start"), pauseB = $("pause"), resetB = $("reset");
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

let ex = EX[0], running = false, remaining = 60, pi = 0, left = 0, last = 0, timerId = null;

function fmt(sec) {
  const s = Math.max(0, Math.ceil(sec));
  return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
}

function renderChips() {
  $("chips").innerHTML = EX.map((e) =>
    '<button class="chip' + (e.id === ex.id ? " on" : "") + '" data-id="' + e.id + '">' +
    '<div class="ic">' + e.icon + '</div><div class="nm">' + e.name + '</div><div class="tg">' + e.tag + "</div></button>"
  ).join("");
  document.querySelectorAll(".chip").forEach((c) => c.addEventListener("click", () => selectEx(c.dataset.id)));
}

function selectEx(id) {
  ex = EX.find((e) => e.id === id);
  $("exName").textContent = ex.icon + " " + ex.name;
  $("exDesc").textContent = ex.desc;
  renderChips();
  resetAll();
}

function setPhase(i, resumeLeft) {
  pi = i % ex.phases.length;
  const p = ex.phases[pi];
  left = resumeLeft !== undefined ? resumeLeft : p.s;
  label.innerHTML = p.t + ' <span id="cnt"></span>';
  detail.textContent = p.d || ex.hint;
  if (p.k !== null) {
    orb.style.transition = reduce ? "none" : "transform " + left + "s ease-in-out";
    orb.style.transform = "scale(" + p.k + ")";
  }
}

function render() {
  timerEl.textContent = fmt(remaining);
  const c = $("cnt");
  if (c) c.textContent = "· " + Math.ceil(left);
}

function finish() {
  clearInterval(timerId);
  running = false;
  remaining = 0;
  render();
  orb.style.transition = "transform 2s ease-in-out";
  orb.style.transform = "scale(0.72)";
  label.textContent = "HOÀN THÀNH";
  detail.textContent = "Hãy dành một chút thời gian cảm nhận cơ thể và hơi thở của bạn.";
  status.textContent = "Bạn đã hoàn thành buổi luyện tập.";
  startB.disabled = true;
  pauseB.disabled = true;
  durSel.disabled = false;
}

function tick() {
  const now = performance.now();
  const dt = (now - last) / 1000;
  last = now;
  remaining -= dt;
  left -= dt;
  if (remaining <= 0) { finish(); return; }
  if (left <= 0) setPhase(pi + 1);
  render();
}

function startSession() {
  if (running || remaining <= 0) return;
  const resuming = startB.textContent === "Tiếp tục";
  running = true;
  status.textContent = "";
  startB.disabled = true;
  pauseB.disabled = false;
  durSel.disabled = true;
  if (resuming) setPhase(pi, left); else setPhase(0);
  last = performance.now();
  timerId = setInterval(tick, 100);
  render();
}

function pauseSession() {
  if (!running) return;
  clearInterval(timerId);
  running = false;
  const m = getComputedStyle(orb).transform;
  orb.style.transition = "none";
  orb.style.transform = m;
  startB.textContent = "Tiếp tục";
  startB.disabled = false;
  pauseB.disabled = true;
  status.textContent = "Đang tạm dừng.";
}

function resetAll() {
  clearInterval(timerId);
  running = false;
  remaining = Number(durSel.value) * 60;
  pi = 0;
  left = 0;
  orb.style.transition = "transform .6s ease-in-out";
  orb.style.transform = "scale(0.72)";
  label.textContent = "SẴN SÀNG";
  detail.textContent = ex.hint;
  status.textContent = "";
  startB.textContent = "Bắt đầu";
  startB.disabled = false;
  pauseB.disabled = true;
  durSel.disabled = false;
  timerEl.textContent = fmt(remaining);
}

startB.addEventListener("click", startSession);
pauseB.addEventListener("click", pauseSession);
resetB.addEventListener("click", resetAll);
durSel.addEventListener("change", resetAll);
selectEx("calm");
</script>
</body>
</html>
"""


def breathing_studio(height=900):
    components.html(HTML, height=height, scrolling=False)
'''

os.makedirs("modules", exist_ok=True)
open(os.path.join("modules", "practice.py"), "w", encoding="utf-8", newline="\n").write(PRACTICE)

shutil.copy("app.py", "app_truoc_khi_vá_luyen_tap.py")
s = open("app.py", encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
L = s.split(nl)

room = next(i for i, l in enumerate(L) if l.startswith('elif menu == "Phòng luyện tập"'))
start = next(i for i in range(room, len(L)) if "st.components.v1.html(" in L[i])
end = next(i for i in range(start, len(L)) if "height=570" in L[i] and "scrolling=False" in L[i])
L = L[:start] + ["    breathing_studio()"] + L[end + 1:]
s = nl.join(L)

if "from modules.practice import" not in s:
    s = s.replace("from modules.recovery_history import (",
                  "from modules.practice import breathing_studio" + nl + "from modules.recovery_history import (", 1)

s = s.replace('st.subheader("Bài tập hô hấp")', 'st.subheader("Chọn bài luyện tập")')
s = s.replace('"Chọn thời lượng, nhấn Bắt đầu và làm theo "', '"Chọn một bài, chọn thời lượng, nhấn Bắt đầu và làm theo "')
s = s.replace('"nhịp chuyển động của quả cầu."', '"hướng dẫn trên màn hình."')

s = s.replace('"không cố hít quá sâu hoặc nín thở. "', '"không cố hít quá sâu hoặc nín thở quá lâu. "')

open("app.py", "w", encoding="utf-8", newline="").write(s)
print("Xong! Phòng luyện tập giờ có 6 bài. Chạy: streamlit run app.py")
