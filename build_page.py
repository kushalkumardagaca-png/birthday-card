#!/usr/bin/env python3
"""Builds index.html — the 144 Birthday Wishes Wall (self-contained, no deps)."""
import json

wishes = json.load(open("/home/user/birthday_card/wishes.json"))
WISHES_JSON = json.dumps(wishes, ensure_ascii=False, separators=(",", ":"))

CDN = "https://cdn.jsdelivr.net/gh/kushalkumardagaca-png/blog-assets@main/birthday"

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🎂 Happy Birthday, Kushal!</title>
<meta name="description" content="144 companies wish Kushal a happy birthday — a new one every five minutes.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎂</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,600&family=Great+Vibes&display=swap" rel="stylesheet">
<style>
  :root{ --gold:#F6CD64; --cream:#FFF6E6; --navy:#0E0920; --card:#1A1033; }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    background:var(--navy);
    background-image:radial-gradient(ellipse 80% 50% at 50% -10%, rgba(120,80,160,.28), transparent),
                     radial-gradient(ellipse 60% 40% at 80% 110%, rgba(90,60,130,.22), transparent);
    color:var(--cream); font-family:Georgia,'Times New Roman',serif;
    min-height:100vh; overflow-x:hidden;
  }
  .wrap{max-width:1080px;margin:0 auto;padding:18px 14px 60px}
  /* ---- hero ---- */
  .hero{text-align:center;margin-bottom:14px}
  .hero img{width:100%;max-width:640px;border-radius:18px;display:block;margin:0 auto;
    box-shadow:0 24px 60px -20px rgba(246,205,100,.35), 0 8px 30px rgba(0,0,0,.5)}
  .hero .script{font-family:'Great Vibes',cursive;font-size:clamp(34px,7vw,58px);
    color:var(--gold);text-shadow:0 0 24px rgba(246,205,100,.4);margin-top:-6px}
  .hero .sub{color:#C9B892;font-style:italic;font-size:clamp(14px,3vw,18px);margin-top:2px}
  /* ---- status bar ---- */
  .status{
    position:sticky;top:0;z-index:50;background:rgba(14,9,32,.92);backdrop-filter:blur(8px);
    border:1px solid rgba(246,205,100,.35);border-radius:16px;padding:12px 16px;margin:16px 0 20px;
    box-shadow:0 10px 30px rgba(0,0,0,.45);
  }
  .status .row1{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:baseline}
  .count{font-size:17px;color:var(--cream)} .count b{color:var(--gold)}
  .next{font-size:14.5px;color:#C9B892}
  .next b{color:var(--cream)}
  .bar{height:8px;border-radius:99px;background:rgba(255,255,255,.09);margin-top:10px;overflow:hidden}
  .bar>div{height:100%;width:0%;border-radius:99px;
    background:linear-gradient(90deg,#B98A2E,#F6CD64,#FFE9A8);transition:width .8s ease;
    box-shadow:0 0 12px rgba(246,205,100,.6)}
  /* ---- controls ---- */
  .ctrls{display:flex;justify-content:center;gap:10px;margin:6px 0 18px;flex-wrap:wrap}
  .btn{
    font-family:Georgia,serif;font-size:15px;color:var(--navy);background:linear-gradient(180deg,#FFE9A8,#F6CD64);
    border:0;border-radius:99px;padding:10px 20px;cursor:pointer;font-weight:700;
    box-shadow:0 6px 18px rgba(246,205,100,.35);transition:transform .15s ease;
  }
  .btn:hover{transform:translateY(-2px)} .btn:active{transform:scale(.97)}
  .btn.ghost{background:transparent;color:var(--gold);border:1.5px solid rgba(246,205,100,.55);box-shadow:none}
  /* ---- teaser (before 6 AM) ---- */
  .teaser{ text-align:center;color:#C9B892;font-size:16px;line-height:1.7;padding:26px 10px}
  .teaser .big{font-size:clamp(22px,5vw,34px);color:var(--cream)}
  .sealed{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:18px}
  .sealed span{
    background:rgba(255,255,255,.05);border:1px dashed rgba(246,205,100,.4);border-radius:14px;
    padding:16px 20px;font-size:26px;filter:grayscale(.25);
  }
  .cd{font-variant-numeric:tabular-nums;color:var(--gold);font-size:clamp(26px,6vw,40px);letter-spacing:2px}
  /* ---- wall ---- */
  .wall{display:grid;grid-template-columns:1fr;gap:16px}
  @media(min-width:700px){.wall{grid-template-columns:1fr 1fr}}
  @media(min-width:1050px){.wall{grid-template-columns:1fr 1fr 1fr}}
  .card{
    border-radius:16px;padding:18px 18px 14px;position:relative;overflow:hidden;
    background:linear-gradient(160deg,var(--pbg1),var(--pbg2));
    border:1px solid color-mix(in srgb, var(--pacc) 45%, transparent);
    box-shadow:0 12px 30px -12px rgba(0,0,0,.55);
    color:var(--ptxt);
    animation:pop .7s cubic-bezier(.2,.9,.3,1.2) both;
  }
  @keyframes pop{from{opacity:0;transform:translateY(26px) scale(.94)}to{opacity:1;transform:none}}
  .card .top{display:flex;align-items:center;gap:11px}
  .card .logo{
    width:44px;height:44px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;
    font-size:22px;background:color-mix(in srgb, var(--pacc) 26%, transparent);
    border:1.5px solid color-mix(in srgb, var(--pacc) 65%, transparent);
  }
  .card .co{font-size:15.5px;font-weight:700;letter-spacing:.4px;line-height:1.25}
  .card .ind{font-size:11.5px;color:var(--psub);letter-spacing:1.6px;text-transform:uppercase;margin-top:2px}
  .card hr{border:0;border-top:1px solid color-mix(in srgb, var(--pacc) 40%, transparent);margin:12px 0}
  .card .msg{font-size:15.5px;line-height:1.62}
  .card .foot{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px;
    font-size:12.5px;color:var(--psub)}
  .card .foot .sig{font-style:italic}
  .card .foot .time{font-variant-numeric:tabular-nums;background:color-mix(in srgb, var(--pacc) 18%, transparent);
    border-radius:99px;padding:2px 9px;white-space:nowrap}
  .card .num{
    position:absolute;top:10px;right:12px;font-size:11px;letter-spacing:1.5px;
    color:var(--psub);opacity:.85;
  }
  .card.fresh{border:2px solid var(--pacc);
    box-shadow:0 0 0 0 rgba(246,205,100,.0), 0 14px 40px -10px color-mix(in srgb, var(--pacc) 55%, transparent);
    animation:pop .7s cubic-bezier(.2,.9,.3,1.2) both, halo 2.4s ease-in-out infinite alternate}
  @keyframes halo{from{box-shadow:0 14px 40px -10px color-mix(in srgb, var(--pacc) 35%, transparent)}
                  to{box-shadow:0 14px 46px -6px color-mix(in srgb, var(--pacc) 75%, transparent)}}
  .card.fresh .num::after{content:" · NEW";color:var(--pacc);font-weight:700}
  /* ---- finale ---- */
  .finale{display:none;text-align:center;margin-top:34px}
  .finale.show{display:block;animation:pop .9s ease both}
  .finale img{width:100%;max-width:640px;border-radius:18px;margin:10px auto;display:block;
    box-shadow:0 24px 60px -20px rgba(246,205,100,.35)}
  .finale h2{font-family:'Playfair Display',Georgia,serif;font-size:clamp(24px,5vw,38px);color:var(--gold);
    margin:16px 0 8px}
  .finale p{color:var(--cream);font-size:17px;line-height:1.7;max-width:640px;margin:0 auto}
  .finale .sig{font-family:'Great Vibes',cursive;font-size:30px;color:var(--gold);margin-top:18px}
  .finale-btn{margin-top:16px}
  /* ---- misc ---- */
  .relive{display:none;text-align:center;color:#C9B892;font-style:italic;padding:4px 0 14px;font-size:14.5px}
  .relive.show{display:block}
  .footer{text-align:center;color:#8A7B5E;font-size:13.5px;letter-spacing:2px;margin-top:36px;line-height:2}
  #confetti{position:fixed;inset:0;pointer-events:none;z-index:100}
  .finale-cta{display:none;position:sticky;top:74px;z-index:60;margin:-10px auto 14px;width:fit-content;
    background:linear-gradient(180deg,#FFE9A8,#F6CD64);color:var(--navy);font-weight:700;font-family:Georgia,serif;
    border-radius:99px;padding:9px 18px;font-size:14.5px;cursor:pointer;border:0;
    box-shadow:0 8px 24px rgba(246,205,100,.45);animation:halo 2s ease-in-out infinite alternate}
  .finale-cta.show{display:block}
</style>
</head>
<body>
<canvas id="confetti"></canvas>
<div class="wrap">

  <div class="hero">
    <img src="__HERO__" alt="Happy Birthday Kushal — animated golden card with fireworks and balloons">
    <div class="script">Kushal</div>
    <div class="sub">today, the whole world celebrates you</div>
  </div>

  <div class="status">
    <div class="row1">
      <div class="count" id="count">🎂 Loading your wishes…</div>
      <div class="next" id="next"></div>
    </div>
    <div class="bar"><div id="barfill"></div></div>
  </div>

  <div class="ctrls">
    <button class="btn ghost" id="chimeBtn">🔔 Chime: ON</button>
    <button class="btn" id="tuneBtn">🎵 Play the birthday tune</button>
  </div>

  <div class="relive" id="relive">💛 Reliving the big day — every wish is unlocked again for you 💛</div>
  <div class="teaser" id="teaser">
    <div class="big">The first of <b>144 birthday wishes</b> arrives at <b>6:00 AM</b></div>
    <div style="margin-top:12px">A new company will wish you every 5 minutes, all day until 6 PM.</div>
    <div class="cd" id="precount">—</div>
    <div class="sealed"><span>💌</span><span>💌</span><span>💌</span><span>💌</span><span>💌</span><span>💌</span></div>
  </div>

  <button class="finale-cta" id="finaleCta">🎁 Your grand finale is ready — open it!</button>
  <div class="wall" id="wall"></div>

  <div class="finale" id="finale">
    <h2>144 companies. One wonderful you. 🎉</h2>
    <p>From coffee roasters to stargazers, chocolatiers to kite makers — today they all agreed on one thing:
       the world is brighter with you in it.</p>
    <img src="__CAKE__" alt="Birthday cake with flickering candles — make a wish!">
    <p style="margin-top:14px">Close your eyes. Make the biggest, boldest wish you can imagine…</p>
    <img src="__GIFTS__" alt="Gift boxes popping open with confetti — to the most wonderful year ahead">
    <p class="sig">With all our love, today and always 💛</p>
    <div class="finale-btn"><button class="btn" id="megaburst">🎊 CELEBRATE!</button></div>
  </div>

  <div class="footer">🎂&nbsp;&nbsp;🎈&nbsp;&nbsp;🎁&nbsp;&nbsp;🎉&nbsp;&nbsp;⭐&nbsp;&nbsp;🎉&nbsp;&nbsp;🎁&nbsp;&nbsp;🎈&nbsp;&nbsp;🎂</div>
</div>

<script>
const WISHES = __WISHES__;
const START = Date.UTC(2026, 8, 25, 0, 30);   // 2026-09-25 06:00 IST
const END   = Date.UTC(2026, 8, 25, 12, 30);  // 2026-09-25 18:00 IST
const SLOT  = 5 * 60 * 1000;
const TOTAL = 144;

/* demo override — ?demo=all shows everything, ?demo=N simulates mid-day (for previewing) */
(function(){
  const q = new URLSearchParams(location.search).get("demo");
  if (!q) return;
  let fake;
  if (q === "all") fake = END + 3600 * 1000;
  else { const n = parseInt(q, 10); if (n > 0) fake = START + (n - 1) * SLOT + 1000; }
  if (fake) Date.now = () => fake;
})();

const $ = id => document.getElementById(id);
const wall = $("wall");

function unlocked(n){ return Math.max(0, Math.min(TOTAL, Math.floor((Date.now() - START) / SLOT) + 1)); }
function slotTime(i){ return new Date(START + (i - 1) * SLOT)
  .toLocaleTimeString("en-IN", {timeZone:"Asia/Kolkata", hour:"numeric", minute:"2-digit"}); }

/* ---------- cards ---------- */
function makeCard(w, fresh){
  const d = document.createElement("div");
  d.className = "card" + (fresh ? " fresh" : "");
  d.style.setProperty("--pbg1", w.bg1); d.style.setProperty("--pbg2", w.bg2);
  d.style.setProperty("--pacc", w.accent); d.style.setProperty("--ptxt", w.text);
  d.style.setProperty("--psub", w.sub);
  d.innerHTML =
    '<div class="top"><div class="logo">' + w.emoji + '</div>' +
    '<div><div class="co">' + w.company + '</div>' +
    '<div class="ind">' + w.industry + ' · Est. ' + w.est + '</div></div></div>' +
    '<div class="num">WISH #' + w.n + ' OF 144</div>' +
    '<hr><div class="msg">' + w.msg + '</div>' +
    '<div class="foot"><span class="sig">delivered with care</span>' +
    '<span class="time">📡 ' + slotTime(w.n) + '</span></div>';
  return d;
}

let rendered = 0;
function renderAll(){
  const n = unlocked();
  for (let i = rendered + 1; i <= n; i++){ wall.prepend(makeCard(WISHES[i - 1], false)); }
  rendered = n;
}
function revealNew(){
  const n = unlocked();
  if (n > rendered){
    const news = [];
    for (let i = rendered + 1; i <= n; i++){ news.push(makeCard(WISHES[i - 1], true)); }
    news.forEach(c => wall.prepend(c));
    rendered = n;
    burst(120);
    chime();
  }
}

/* ---------- status ---------- */
function fmt(ms){
  const s = Math.max(0, Math.floor(ms / 1000));
  return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
}
function tick(){
  const now = Date.now();
  if (now < START){
    $("precount").textContent = "⏳ " + fmt(START - now);
    return;
  }
  $("teaser").style.display = "none";
  const n = unlocked();
  const done = now >= END;
  $("count").innerHTML = done
    ? "🎂 All <b>144</b> wishes delivered!"
    : "🎂 Wish <b>" + n + "</b> of <b>144</b> delivered";
  if (done){
    $("next").innerHTML = "🎁 The grand finale is unlocked below 🎉";
  } else if (n >= 144){
    $("next").innerHTML = "All wishes delivered · 🎊 grand finale at <b>6:00 PM</b> in <b>" +
      fmt(END - now) + "</b>";
  } else {
    $("next").innerHTML = "Next: <b>" + WISHES[n].emoji + " " + WISHES[n].company + "</b> in <b>" +
      fmt(START + n * SLOT - now) + "</b>";
  }
  $("barfill").style.width = (n / TOTAL * 100) + "%";
  if (now > END + 24 * 3600 * 1000){ $("relive").classList.add("show"); }
  if (done){ $("finale").classList.add("show"); $("finaleCta").classList.add("show"); }
}

/* ---------- confetti ---------- */
const cv = $("confetti"), cx = cv.getContext("2d");
let parts = [];
function resize(){ cv.width = innerWidth; cv.height = innerHeight; }
addEventListener("resize", resize); resize();
const COLS = ["#F6CD64","#FFE9A8","#E8748A","#5CBABA","#F4976A","#FFF6E6","#966FD6","#F6CD64"];
function spawn(x, y, n, spread){
  for (let i = 0; i < n; i++){
    const a = Math.random() * Math.PI * 2, v = (Math.random() * 6 + 3) * (spread || 1);
    parts.push({x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 3,
      r: Math.random() * 5 + 2, rot: Math.random() * Math.PI, vr: (Math.random() - .5) * .3,
      c: COLS[Math.floor(Math.random() * COLS.length)], life: 1, decay: .006 + Math.random() * .008,
      shape: Math.random() < .3 ? 1 : 0});
  }
}
function burst(n){ spawn(innerWidth / 2, innerHeight * .35, n, 1.4); }
let drizzle = 0;
function loop(){
  cx.clearRect(0, 0, cv.width, cv.height);
  if (Date.now() >= START && Date.now() < END && Math.random() < .25){
    spawn(Math.random() * cv.width, -10, 1, .4);
  }
  parts = parts.filter(p => p.life > 0 && p.y < cv.height + 20);
  for (const p of parts){
    p.x += p.vx; p.y += p.vy; p.vy += .12; p.vx *= .99; p.rot += p.vr; p.life -= p.decay;
    cx.save(); cx.translate(p.x, p.y); cx.rotate(p.rot);
    cx.globalAlpha = Math.max(0, p.life); cx.fillStyle = p.c;
    if (p.shape){ cx.beginPath(); cx.arc(0, 0, p.r * .6, 0, 7); cx.fill(); }
    else cx.fillRect(-p.r, -p.r * .55, p.r * 2, p.r * 1.1);
    cx.restore();
  }
  requestAnimationFrame(loop);
}
loop();
addEventListener("click", e => spawn(e.clientX, e.clientY, 26, 1));

/* ---------- sound ---------- */
let AC = null, chimeOn = true;
try { chimeOn = localStorage.getItem("chime") !== "0"; } catch(e){}
function ac(){ if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)(); return AC; }
function tone(f, t0, dur, type, vol){
  const a = ac(), o = a.createOscillator(), g = a.createGain();
  o.type = type || "sine"; o.frequency.value = f;
  g.gain.setValueAtTime(0, a.currentTime + t0);
  g.gain.linearRampToValueAtTime(vol || .18, a.currentTime + t0 + .02);
  g.gain.exponentialRampToValueAtTime(.0001, a.currentTime + t0 + dur);
  o.connect(g).connect(a.destination);
  o.start(a.currentTime + t0); o.stop(a.currentTime + t0 + dur + .05);
}
function chime(){ if (!chimeOn) return; try{ tone(880, 0, .5); tone(1318.5, .12, .7); }catch(e){} }
$("chimeBtn").onclick = () => {
  chimeOn = !chimeOn;
  try{ localStorage.setItem("chime", chimeOn ? "1" : "0"); }catch(e){}
  $("chimeBtn").textContent = chimeOn ? "🔔 Chime: ON" : "🔕 Chime: OFF";
};
$("chimeBtn").textContent = chimeOn ? "🔔 Chime: ON" : "🔕 Chime: OFF";

/* Happy Birthday — soft music-box */
const N = {G4:392, A4:440, B4:493.88, C5:523.25, D5:587.33, E5:659.25, F5:698.46, G5:783.99};
const TUNE = [[N.G4,.75],[N.G4,.25],[N.A4,1],[N.G4,1],[N.C5,1],[N.B4,2],
              [N.G4,.75],[N.G4,.25],[N.A4,1],[N.G4,1],[N.D5,1],[N.C5,2],
              [N.G4,.75],[N.G4,.25],[N.G5,1],[N.E5,1],[N.C5,1],[N.D5,1],[N.C5,2],
              [N.F5,.75],[N.F5,.25],[N.E5,1],[N.C5,1],[N.D5,1],[N.C5,2]];
let playing = false;
function playTune(){
  if (playing) return; playing = true;
  let t = 0; const beat = .42;
  for (const [f, b] of TUNE){ tone(f, t, b * beat * 1.15, "triangle", .16); t += b * beat; }
  setTimeout(() => { playing = false; burst(160); }, t * 1000);
}
$("tuneBtn").onclick = playTune;
$("megaburst").onclick = () => { burst(200); setTimeout(()=>burst(200), 350); setTimeout(()=>burst(200), 700); playTune(); };
$("finaleCta").onclick = () => $("finale").scrollIntoView({behavior:"smooth"});

/* ---------- main loop ---------- */
renderAll();
tick();
setInterval(() => { tick(); revealNew(); }, 1000);
if (unlocked() > 0) burst(90);
</script>
</body>
</html>
"""

HTML = (HTML
        .replace("__WISHES__", WISHES_JSON)
        .replace("__HERO__", f"{CDN}/hero_happy_birthday.gif")
        .replace("__CAKE__", f"{CDN}/cake_make_a_wish.gif")
        .replace("__GIFTS__", f"{CDN}/gifts_finale.gif"))

out = "/home/user/birthday_card/index.html"
open(out, "w").write(HTML)
import os
print(f"index.html built: {os.path.getsize(out)//1024} KB")
