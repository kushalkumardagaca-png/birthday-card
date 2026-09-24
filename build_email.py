#!/usr/bin/env python3
"""Builds the birthday email (CDN images) + an in-chat preview (data-URI images)."""
import base64

CDN = "https://cdn.jsdelivr.net/gh/kushalkumardagaca-png/blog-assets@main/birthday"

SUBJECT = "🎂✨ Happy Birthday, Kushal! ✨🎈"
SIGNATURE = "With all our love, today and always 💛"

BODY = """
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#0E0920" style="background-color:#0E0920;">
<tr><td align="center" style="padding:28px 12px;">

  <!-- gold frame -->
  <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="#C9973F" style="background-color:#C9973F;border-radius:18px;max-width:600px;width:100%;">
  <tr><td style="padding:3px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#1A1033" style="background-color:#1A1033;border-radius:16px;">
  <tr><td align="center" style="padding:0;">

    <img src="{HERO}" width="600" alt="Happy Birthday Kushal — golden animated card with fireworks, balloons and confetti" style="display:block;width:100%;max-width:600px;height:auto;border:0;border-radius:16px 16px 0 0;">

    <div style="font-family:Georgia,'Times New Roman',serif;font-size:20px;line-height:34px;color:#FFF6E6;padding:30px 48px 8px 48px;">
      Today the world got a little brighter, a little warmer, and a whole lot luckier &mdash; because it&rsquo;s the day <strong style="color:#F6CD64;">you</strong> were born. 🌟
    </div>

    <div style="font-family:Georgia,serif;font-size:24px;letter-spacing:6px;color:#F6CD64;padding:18px 0 10px 0;">
      ✨&nbsp;&nbsp;🎈&nbsp;&nbsp;✨&nbsp;&nbsp;🎁&nbsp;&nbsp;✨&nbsp;&nbsp;🎈&nbsp;&nbsp;✨
    </div>

    <img src="{CAKE}" width="600" alt="Birthday cake with flickering candles — Make a Wish!" style="display:block;width:100%;max-width:600px;height:auto;border:0;">

    <div style="font-family:Georgia,serif;font-size:20px;line-height:34px;color:#FFF6E6;padding:26px 48px 4px 48px;">
      Close your eyes. Make the biggest, boldest, most wonderful wish you can imagine&hellip; <br>then blow out the candles! 🎂✨
    </div>

    <img src="{GIFTS}" width="600" alt="Gift boxes popping open with confetti — to the most wonderful year ahead" style="display:block;width:100%;max-width:600px;height:auto;border:0;">

    <div style="font-family:Georgia,serif;font-size:20px;line-height:34px;color:#FFF6E6;padding:26px 48px 6px 48px;">
      May this new year of yours overflow with laughter, cake for breakfast, your favourite music, and a hundred little beautiful surprises. 🎁💫
    </div>

    <div style="font-family:Georgia,serif;font-size:28px;line-height:40px;color:#F6CD64;font-style:italic;padding:22px 40px 6px 40px;">
      Happiest of birthdays, Kushal! 🎉
    </div>

    <div style="font-family:Georgia,serif;font-size:17px;line-height:28px;color:#D9C9A8;padding:6px 40px 8px 40px;">
      {SIGNATURE}
    </div>

    <div style="font-family:Georgia,serif;font-size:14px;letter-spacing:4px;color:#8A7B5E;padding:20px 20px 30px 20px;">
      🎂&nbsp;&nbsp;🎈&nbsp;&nbsp;🎁&nbsp;&nbsp;🎉&nbsp;&nbsp;⭐&nbsp;&nbsp;🎉&nbsp;&nbsp;🎁&nbsp;&nbsp;🎈&nbsp;&nbsp;🎂
    </div>

  </td></tr>
  </table>
  </td></tr>
  </table>

</td></tr>
</table>
"""


def build():
    email_html = BODY.replace("{HERO}", f"{CDN}/hero_happy_birthday.gif") \
                     .replace("{CAKE}", f"{CDN}/cake_make_a_wish.gif") \
                     .replace("{GIFTS}", f"{CDN}/gifts_finale.gif") \
                     .replace("{SIGNATURE}", SIGNATURE)
    full_email = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{SUBJECT}</title>
</head><body style="margin:0;padding:0;background-color:#0E0920;">
<div style="display:none;max-height:0;overflow:hidden;">The confetti is ready... 🎊</div>
{email_html}
</body></html>"""
    open("/home/user/birthday_card/birthday_email.html", "w").write(full_email)

    def datauri(fn):
        return "data:image/gif;base64," + base64.b64encode(open(fn, "rb").read()).decode()

    preview = BODY.replace("{HERO}", datauri("hero_happy_birthday.gif")) \
                  .replace("{CAKE}", datauri("cake_make_a_wish.gif")) \
                  .replace("{GIFTS}", datauri("gifts_finale.gif")) \
                  .replace("{SIGNATURE}", SIGNATURE)
    preview_full = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Birthday Card Preview</title>
<style>body{{margin:0;padding:16px 0;background:#0E0920;}}</style>
</head><body>
<div style="text-align:center;color:#8A7B5E;font-family:Georgia,serif;font-size:13px;letter-spacing:2px;padding:6px 0 14px 0;">
PREVIEW &mdash; HOW THE EMAIL WILL LOOK</div>
{preview}
</body></html>"""
    open("/home/user/Birthday_Card_Preview.html", "w").write(preview_full)
    import os
    print("email:", os.path.getsize("/home/user/birthday_card/birthday_email.html") // 1024, "KB")
    print("preview:", os.path.getsize("/home/user/Birthday_Card_Preview.html") // 1024 // 1024, "MB")


if __name__ == "__main__":
    build()
