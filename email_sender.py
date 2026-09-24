#!/usr/bin/env python3
"""Birthday Email Sender — sends the 144 unique company wishes.
Runs on GitHub Actions; each invocation sends due unsent slots (catch-up safe).
Env: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL,
     STATE_FILE (optional), MAX_SEND (safety cap per run), TEST_TO (optional).
"""
import json
import os
import random
import smtplib
import ssl
import sys
import time
from email.message import EmailMessage
from email.utils import formatdate

WISHES = json.load(open(os.environ.get("WISHES_FILE", "wishes.json")))

# 2026-09-25 06:00 IST == 00:30 UTC
import datetime
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
DAY_START = datetime.datetime(2026, 9, 25, 6, 0, tzinfo=IST)
SLOT = datetime.timedelta(minutes=5)
TOTAL = 144

SUBJECTS = [
    "\U0001F382 A birthday wish from {company} {emoji}",
    "\U0001F381 Wish #{n}: {company} says happy birthday! {emoji}",
    "{emoji} Happy Birthday from {company} \U0001F382",
    "\U0001F382 #{n} of 144 \u00b7 a wish from {company} {emoji}",
    "{emoji} {company} sends birthday wishes \U0001F389",
]


def slot_now():
    now = datetime.datetime.now(datetime.timezone.utc)
    return math.floor((now - DAY_START) / SLOT) + 1, now


def load_state(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"sent": []}


def save_state(path, st):
    with open(path, "w") as f:
        json.dump(st, f, indent=1)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_email(w, n):
    subj = SUBJECTS[(n * 7 + w["est"]) % len(SUBJECTS)].format(
        company=w["company"], emoji=w["emoji"], n=n)
    name = f"{w['emoji']} {w['company']}"

    html = f"""<div style="margin:0;padding:24px 12px;background:#0E0920;font-family:Georgia,'Times New Roman',serif;">
<div style="max-width:560px;margin:0 auto;border-radius:16px;overflow:hidden;
 border:2px solid {w['accent']};">
 <div style="background:linear-gradient(160deg,{w['bg1']},{w['bg2']});padding:30px 34px;color:{w['text']};">
  <div style="font-size:12px;letter-spacing:3px;color:{w['sub']};text-transform:uppercase;">
   Birthday Wishes \u00b7 #{n} of 144</div>
  <div style="margin-top:16px;">
   <div style="font-size:30px;">{w['emoji']}</div>
   <div style="font-size:20px;font-weight:bold;margin-top:6px;color:{w['accent']};">{esc(w['company'])}</div>
   <div style="font-size:11.5px;letter-spacing:2px;color:{w['sub']};margin-top:2px;text-transform:uppercase;">
    {esc(w['industry'])} \u00b7 Est. {w['est']}</div>
  </div>
  <div style="border-top:1px solid {w['accent']};opacity:.4;margin:18px 0;"></div>
  <div style="font-size:16px;line-height:1.65;">{esc(w['msg'])}</div>
  <div style="margin-top:22px;font-size:12px;color:{w['sub']};font-style:italic;">
   delivered with care \u00b7 6 AM \u2013 6 PM, every five minutes</div>
 </div>
</div>
</div>"""

    text = (f"BIRTHDAY WISHES - #{n} of 144\n\n{w['emoji']} {w['company']}\n"
            f"{w['industry']} - Est. {w['est']}\n\n{w['msg']}\n\n"
            f"delivered with care - 6 AM to 6 PM, every five minutes")
    return subj, name, html, text


def send_one(w, n, cfg):
    subj, name, html, text = build_email(w, n)
    msg = EmailMessage()
    msg["Subject"] = subj
    msg["From"] = f"{name} <{cfg['user']}>"
    msg["To"] = cfg["to"]
    msg["Date"] = formatdate(localtime=False)
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    ctx = ssl.create_default_context()
    with smtplib.SMTP(cfg["host"], cfg["port"], timeout=60) as s:
        s.starttls(context=ctx)
        s.login(cfg["user"], cfg["password"])
        s.send_message(msg)


def main():
    cfg = {
        "host": os.environ["SMTP_HOST"],
        "port": int(os.environ.get("SMTP_PORT", "587")),
        "user": os.environ["SMTP_USER"],
        "password": os.environ["SMTP_PASSWORD"],
        "to": os.environ.get("TEST_TO") or os.environ["RECIPIENT_EMAIL"],
    }
    state_path = os.environ.get("STATE_FILE", "sent_state.json")
    state = load_state(state_path)
    sent = set(state["sent"])

    if os.environ.get("TEST_TO"):  # test mode: send wish #1 to the tester, once
        if "test-done" in state:
            print("test already sent")
            return
        time.sleep(random.uniform(0, 20))
        send_one(WISHES[0], 1, cfg)
        state.setdefault("test-done", True)
        save_state(state_path, state)
        print("TEST email sent to", cfg["to"])
        return

    slot, now = slot_now()
    if slot < 1:
        print(f"Too early ({now} UTC). First wish at 00:30 UTC Sept 25.")
        return
    due = [i for i in range(1, min(slot, TOTAL) + 1) if i not in sent]
    cap = int(os.environ.get("MAX_SEND", "6"))
    due = due[:cap]
    if not due:
        print("Nothing due — all caught up.")
        return
    print(f"UTC now {now} -> slot {slot}; sending {len(due)} wish(es): {due}")
    for n in due:
        w = WISHES[n - 1]
        try:
            time.sleep(random.uniform(2, 9))  # human-ish pacing
            send_one(w, n, cfg)
            sent.add(n)
            state["sent"] = sorted(sent)
            save_state(state_path, state)
            print(f"  sent #{n} from {w['company']}")
        except Exception as e:
            print(f"  FAILED #{n} ({w['company']}): {e}")
            if n == due[0] and len(sent) == 0 and "test-done" not in state:
                print("First send of run failed hard — exiting 1 for retry.")
                sys.exit(1)
            break
    print(f"Done. Total sent so far: {len(sent)}/144")


if __name__ == "__main__":
    main()
