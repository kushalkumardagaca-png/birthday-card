#!/usr/bin/env python3
"""Birthday card animation generator — three decorative GIF scenes.
Drawn at 2x and downscaled with LANCZOS for smooth anti-aliasing."""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(20260925)

W, H = 600, 350          # hero
CW, CH = 600, 320        # cake
GW, GH = 600, 220        # gifts
SS = 2                   # supersample factor

FONT_DIR = "/home/user/birthday_card/fonts"

def playfair(size, weight=800, italic=False):
    name = "PlayfairDisplay-Italic[wght].ttf" if italic else "PlayfairDisplay[wght].ttf"
    f = ImageFont.truetype(f"{FONT_DIR}/{name}", size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f

def vibes(size):
    return ImageFont.truetype(f"{FONT_DIR}/GreatVibes-Regular.ttf", size)

GOLD = (246, 205, 100)
GOLD_HI = (255, 236, 170)
CREAM = (255, 248, 232)
ROSE = (232, 116, 138)
CORAL = (244, 151, 106)
TEAL = (92, 186, 186)
PURPLE = (150, 111, 214)
NAVY_TOP = (16, 12, 44)
NAVY_BOT = (46, 26, 74)

# ---------------------------------------------------------------- helpers
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vgrad(w, h, top, bot, glow_center=None, glow_color=(120, 90, 160), glow_r=0.55, glow_a=0.35):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = lerp(top, bot, t)
        for x in range(w):
            px[x, y] = c
    if glow_center:
        overlay = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(overlay)
        cx, cy = glow_center
        rr = int(glow_r * min(w, h))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=int(255 * glow_a))
        overlay = overlay.filter(ImageFilter.GaussianBlur(rr * 0.6))
        glow = Image.new("RGB", (w, h), glow_color)
        img = Image.composite(glow, img, overlay.point(lambda v: v))
    return img

def star_poly(cx, cy, r, points=5, rot=0.0, inner=0.45):
    pts = []
    for i in range(points * 2):
        ang = rot + i * math.pi / points
        rad = r if i % 2 == 0 else r * inner
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts

def draw_confetti_particle(d, p):
    x, y, shape, color, size, ang = p
    if shape == 0:   # rectangle
        dx, dy = size * math.cos(ang), size * math.sin(ang)
        d.polygon([(x - dx, y - dy), (x - dx + size * .35, y - dy + size * .1),
                   (x + dx, y + dy), (x + dx - size * .35, y + dy - size * .1)],
                  fill=color)
    elif shape == 1:  # circle
        d.ellipse([x - size * .4, y - size * .4, x + size * .4, y + size * .4], fill=color)
    else:             # star
        d.polygon(star_poly(x, y, size * .55, rot=ang), fill=color)

class Confetti:
    def __init__(self, n, w, h, palette, speed=(28, 70), size=(4, 9)):
        self.n, self.w, self.h, self.palette = n, w, h, palette
        self.speed, self.sizer = speed, size
        self.reset_all()

    def reset(self, top=False):
        return [random.uniform(-40, self.w + 40) if top else random.uniform(0, self.w),
                random.uniform(-self.h * 0.5, 0) if top else random.uniform(-20, self.h),
                random.randint(0, 2),
                random.choice(self.palette),
                random.uniform(*self.sizer),
                random.uniform(0, math.pi * 2),
                random.uniform(*self.speed),
                random.uniform(0.5, 1.6),   # sway amp
                random.uniform(0.02, 0.06)]  # sway freq

    def reset_all(self):
        self.ps = [self.reset() for _ in range(self.n)]

    def step(self, dt):
        out = []
        for p in self.ps:
            x, y = p[0] + math.sin(p[6] * dt * p[8] * 8) * p[7], p[1] + p[6] * dt
            if y > self.h + 14:
                q = self.reset(top=True)
                out.append(q)
            else:
                out.append([x, y] + p[2:])
        self.ps = out

    def draw(self, d):
        for p in self.ps:
            draw_confetti_particle(d, (p[0], p[1], p[2], p[3], p[4], p[5] + p[6] * dt_global * 3))

class Balloons:
    COLORS = [(226, 84, 94), GOLD, ROSE, TEAL, (244, 208, 186), CORAL, PURPLE,
              (200, 220, 250)]
    def __init__(self, n, w, h):
        self.w, self.h = w, h
        self.bs = []
        for i in range(n):
            self.bs.append({
                "x": random.uniform(0.06, 0.94) * w,
                "r": random.uniform(16, 27),
                "col": self.COLORS[i % len(self.COLORS)],
                "speed": random.uniform(18, 34),
                "phase": random.uniform(0, math.pi * 2),
                "alpha": random.uniform(0.55, 0.95),
                "depth": random.uniform(0.5, 1.0),
            })

    def draw(self, d, t, dt):
        for b in self.bs:
            y0 = (b["x"] * 7)  # stagger
            y = ((y0 - b["speed"] * t) % (self.h + 160)) - 80
            sway = math.sin(t * 1.2 + b["phase"]) * 9 * b["depth"]
            x = b["x"] + sway
            r = b["r"] * (0.6 + 0.4 * b["depth"])
            # string
            pts = [(x + math.sin(t * 2 + b["phase"] + k * .8) * 4, y + r * 1.28 + k * 7)
                   for k in range(9)]
            d.line(pts, fill=(210, 200, 230), width=1)
            # balloon body (ellipse with highlight)
            col = b["col"]
            body = tuple(int(c * 0.92) for c in col)
            d.ellipse([x - r, y - r * 1.22, x + r, y + r * 1.22], fill=body,
                      outline=tuple(min(255, c + 30) for c in col))
            d.polygon([(x - r * .22, y + r * 1.2), (x + r * .22, y + r * 1.2),
                       (x, y + r * 1.45)], fill=body)
            hl = lerp(col, (255, 255, 255), 0.55)
            d.ellipse([x - r * .55, y - r * .85, x - r * .12, y - r * .3], fill=hl)

class Fireworks:
    def __init__(self, bursts):
        # bursts: list of (time, x, y, color, n)
        self.bursts = bursts
        self.cache = {}
    def particles(self, t):
        out = []
        for (t0, x, y, col, n) in self.bursts:
            age = t - t0
            if age < 0:
                continue
            key = (t0, x, y, n)
            if key not in self.cache:
                rng = random.Random(int(t0 * 100) + x)
                self.cache[key] = [(rng.uniform(0, math.pi * 2),
                                    rng.uniform(40, 130)) for _ in range(n)]
            life = 1.9
            if age > life:
                continue
            fade = max(0.0, 1 - age / life)
            for (ang, sp) in self.cache[key]:
                drag = 0.55
                px = x + math.cos(ang) * sp * (1 - (1 - drag) ** (age * 3)) / (1 - drag) / 3
                py = y + math.sin(ang) * sp * (1 - (1 - drag) ** (age * 3)) / (1 - drag) / 3 \
                     + 45 * age * age
                r = 2.4 * fade + 0.6
                c = lerp(col, (40, 30, 60), 1 - fade)
                out.append((px, py, r, c))
        return out
    def draw(self, d, t):
        for (px, py, r, c) in self.particles(t):
            d.ellipse([px - r, py - r, px + r, py + r], fill=c)

def draw_stars(d, w, h, t, n=34, seed=7):
    rng = random.Random(seed)
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h * 0.85)
        base = rng.uniform(0.35, 1.0)
        tw = 0.5 + 0.5 * math.sin(t * rng.uniform(1.5, 3.5) + x)
        a = base * tw
        r = rng.uniform(0.8, 1.9)
        c = lerp((70, 60, 110), (255, 244, 214), a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def draw_bunting(d, w, t, colors=(GOLD, ROSE, TEAL, CORAL, CREAM, PURPLE)):
    y0, sag = 26, 26
    n = 11
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        x0 = u0 * (w + 60) - 30
        x1 = u1 * (w + 60) - 30
        yb0 = y0 + math.sin(u0 * math.pi) * sag + math.sin(t * 1.6 + i) * 1.5
        yb1 = y0 + math.sin(u1 * math.pi) * sag + math.sin(t * 1.6 + i + 1) * 1.5
        col = colors[i % len(colors)]
        d.polygon([(x0, yb0), (x1, yb1), ((x0 + x1) / 2, (yb0 + yb1) / 2 + 22)], fill=col)
    # rope
    pts = [(u * (w + 60) - 30, y0 + math.sin(u * math.pi) * sag + math.sin(t * 1.6 + u * n) * 1.5)
           for u in [i / 40 for i in range(41)]]
    d.line(pts, fill=(214, 200, 170), width=2)

def text_layer(size, draw_fn):
    lay = Image.new("L", size, 0)
    ImageDraw.Draw(lay).text  # noqa
    dl = ImageDraw.Draw(lay)
    draw_fn(dl)
    return lay

def glow_text(base, pos, text, font, fill, glow_color, glow_radius=6, glow_alpha=0.85,
              anchor="mm", shimmer=None):
    """Draw glowing text with optional shimmer sweep. shimmer=(t, period)"""
    w, h = base.size
    lay = Image.new("L", (w, h), 0)
    dl = ImageDraw.Draw(lay)
    dl.text(pos, text, font=font, fill=255, anchor=anchor)
    # glow
    glow = lay.filter(ImageFilter.GaussianBlur(glow_radius))
    gimg = Image.new("RGB", (w, h), glow_color)
    base.paste(gimg, (0, 0), glow.point(lambda v: int(v * glow_alpha)))
    # shimmer: moving bright band inside the text
    if shimmer is not None:
        t, period = shimmer
        band = Image.new("L", (w, h), 0)
        db = ImageDraw.Draw(band)
        cx = ((t % period) / period - 0.18) * (w * 1.5)
        for k in range(14):
            a = int(150 * math.exp(-((k - 7) ** 2) / 9))
            db.line([(cx + k * 5 - 35, 0), (cx + k * 5 - 35 + 45, h)], width=6, fill=a)
        band = band.filter(ImageFilter.GaussianBlur(3))
        shim = Image.new("RGB", (w, h), (255, 252, 240))
        base.paste(shim, (0, 0), Image.composite(band, Image.new("L", (w, h), 0), lay))
    # crisp text
    base.paste(Image.new("RGB", (w, h), fill), (0, 0), lay)
    return lay

def save_gif(frames, path, duration=83, colors=112):
    # build a global palette from a sample strip of frames
    picks = frames[::max(1, len(frames) // 6)][:6] + [frames[-1]]
    strip_w = sum(p.width for p in picks)
    strip = Image.new("RGB", (strip_w, picks[0].height))
    x = 0
    for p in picks:
        strip.paste(p, (x, 0))
        x += p.width
    pal = strip.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    q[0].save(path, save_all=True, append_images=q[1:],
              duration=duration, loop=0, optimize=True)
    import os
    print(f"{path}: {os.path.getsize(path)//1024} KB, {len(frames)} frames "
          f"@ {frames[0].size[0]}x{frames[0].size[1]}")

dt_global = 0.0

# ---------------------------------------------------------------- scene 1: hero
def make_hero():
    FPS, DUR = 12, 5.5
    N = int(FPS * DUR)
    palette = [GOLD, GOLD_HI, ROSE, TEAL, CREAM, CORAL, PURPLE, (255, 214, 140)]
    conf = Confetti(46, W, H, palette)
    balloons = Balloons(7, W, H)
    fw = Fireworks([
        (0.30, 130, 88, GOLD_HI, 24), (1.35, 478, 74, (255, 160, 180), 22),
        (2.40, 300, 60, TEAL, 20), (3.45, 90, 110, CORAL, 22),
        (4.35, 520, 120, (180, 160, 255), 24),
    ])
    frames = []
    f_happy = playfair(int(56 * SS), weight=800)
    f_script = vibes(int(120 * SS))
    for i in range(N):
        t = i / FPS
        global dt_global
        dt_global = t
        conf.step(1 / FPS)
        img = vgrad(W * SS, H * SS, NAVY_TOP, NAVY_BOT,
                    glow_center=(W * SS // 2, int(H * SS * 0.52)),
                    glow_color=(96, 64, 130), glow_r=0.75, glow_a=0.30)
        d = ImageDraw.Draw(img, "RGBA")
        draw_stars(d, W * SS, H * SS, t)
        draw_bunting(d, W * SS, t)
        balloons.draw(d, t, 1 / FPS)
        fw.draw(d, t)
        conf.draw(d)
        # ---- text block ----
        cx = W * SS // 2
        glow_text(img, (cx, int(H * SS * 0.44)), "HAPPY", f_happy, CREAM,
                  (250, 190, 90), glow_radius=10 * SS, glow_alpha=0.7,
                  shimmer=(t, DUR / 2))
        glow_text(img, (cx, int(H * SS * 0.60)), "BIRTHDAY", f_happy, GOLD,
                  (255, 180, 80), glow_radius=10 * SS, glow_alpha=0.8,
                  shimmer=(t + 0.4, DUR / 2))
        glow_text(img, (cx, int(H * SS * 0.80)), "Kushal", f_script, GOLD_HI,
                  (255, 170, 60), glow_radius=12 * SS, glow_alpha=0.9,
                  shimmer=(t + 0.8, DUR / 2))
        # sparkles around the name
        for k in range(5):
            ang = t * 1.4 + k * math.pi * 2 / 5
            sx = cx + math.cos(ang) * 150 * SS
            sy = int(H * SS * 0.80) + math.sin(ang) * 26 * SS
            tw = 0.5 + 0.5 * math.sin(t * 6 + k)
            d.polygon(star_poly(sx, sy, (3 + 3 * tw) * SS, rot=ang), fill=GOLD_HI)
        frames.append(img.resize((W, H), Image.LANCZOS))
    return frames

# ---------------------------------------------------------------- scene 2: cake
def make_cake():
    FPS, DUR = 12, 3.6
    N = int(FPS * DUR)
    palette = [GOLD, ROSE, CREAM, TEAL, CORAL]
    conf = Confetti(22, CW, CH, palette, speed=(12, 30), size=(3, 6))
    frames = []
    f_script = vibes(int(56 * SS))
    f_small = playfair(int(17 * SS), weight=600, italic=True)
    for i in range(N):
        t = i / FPS
        global dt_global
        dt_global = t
        conf.step(1 / FPS)
        img = vgrad(CW * SS, CH * SS, (24, 14, 48), (56, 30, 66),
                    glow_center=(CW * SS // 2, int(CH * SS * 0.66)),
                    glow_color=(150, 90, 90), glow_r=0.8, glow_a=0.32)
        d = ImageDraw.Draw(img, "RGBA")
        # bokeh
        rng = random.Random(11)
        for _ in range(12):
            bx, by = rng.uniform(0, CW * SS), rng.uniform(0, CH * SS * 0.8)
            br = rng.uniform(4, 13) * SS
            ba = int(28 + 18 * math.sin(t * 1.4 + bx))
            d.ellipse([bx - br, by - br, bx + br, by + br],
                      fill=(255, 200, 150, max(10, ba)))
        draw_stars(d, CW * SS, CH * SS, t, n=18, seed=3)
        conf.draw(d)
        # ---- cake ----
        cxx, base_y = CW * SS // 2, int(CH * SS * 0.94)
        tiers = [(204 * SS, 54 * SS, (246, 226, 200)), (146 * SS, 48 * SS, (242, 205, 205)),
                 (94 * SS, 44 * SS, (250, 232, 210))]
        # plate
        d.ellipse([cxx - 150 * SS, base_y - 12 * SS, cxx + 150 * SS, base_y + 14 * SS],
                  fill=(212, 175, 110), outline=GOLD)
        y = base_y - 6 * SS
        for (tw, th, tc) in tiers:
            top = y - th
            d.rounded_rectangle([cxx - tw // 2, top, cxx + tw // 2, y], radius=10 * SS,
                                fill=tc, outline=tuple(int(c * .8) for c in tc))
            # icing drips
            drr = ImageDraw.Draw(img, "RGBA")
            for k in range(int(tw // (22 * SS))):
                dx = cxx - tw // 2 + (k + 0.5) * 22 * SS
                dh = (10 + 8 * math.sin(k * 2.7)) * SS
                col = CREAM if tc[1] > 215 else (250, 214, 214)
                drr.rounded_rectangle([dx - 8 * SS, top - 2 * SS, dx + 8 * SS, top + dh],
                                      radius=8 * SS, fill=col)
            # scallop border at bottom
            for k in range(int(tw // (16 * SS)) + 1):
                dx = cxx - tw // 2 + k * 16 * SS
                d.ellipse([dx - 8 * SS, y - 8 * SS, dx + 8 * SS, y + 8 * SS],
                          fill=lerp(tc, GOLD, 0.55))
            # sprinkles
            rng2 = random.Random(int(tw))
            for _ in range(9):
                sx = rng2.uniform(-tw / 2 + 14 * SS, tw / 2 - 14 * SS)
                sy = rng2.uniform(top + 12 * SS, y - 14 * SS)
                scol = rng2.choice([ROSE, TEAL, GOLD, CORAL])
                d.line([(cxx + sx - 4 * SS, cxx * 0 + sy + 2 * SS),
                        (cxx + sx + 4 * SS, sy - 2 * SS)], fill=scol, width=3 * SS)
            y = top - 2 * SS
        # candles on top tier
        n_c = 5
        top_cx = cxx
        for k in range(n_c):
            cxk = top_cx + (k - (n_c - 1) / 2) * 20 * SS
            ch_ = 30 * SS
            cy0 = y + 4 * SS
            stripe = (232, 116, 138) if k % 2 == 0 else (92, 186, 186)
            d.rounded_rectangle([cxk - 4 * SS, cy0 - ch_, cxk + 4 * SS, cy0],
                                radius=3 * SS, fill=CREAM, outline=stripe)
            for s in range(3):
                yy = cy0 - ch_ + (s + 0.5) * ch_ / 3
                d.line([(cxk - 4 * SS, yy), (cxk + 4 * SS, yy - 4 * SS)],
                       fill=stripe, width=3 * SS)
            # flame
            fl = 0.5 + 0.5 * math.sin(t * 9 + k * 2.2) * math.sin(t * 5.3 + k)
            fh = (10 + 4 * fl) * SS
            fx, fy = cxk, cy0 - ch_ - 2 * SS
            halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
            dh = ImageDraw.Draw(halo)
            hr = (14 + 5 * fl) * SS
            dh.ellipse([fx - hr, fy - fh - hr, fx + hr, fy + hr],
                       fill=(255, 190, 90, 90))
            img.paste(halo.filter(ImageFilter.GaussianBlur(6 * SS)).convert('RGB'), (0, 0), halo.filter(ImageFilter.GaussianBlur(6 * SS)))
            d = ImageDraw.Draw(img, "RGBA")
            d.polygon([(fx, fy - fh * 1.5), (fx + 5 * SS, fy), (fx, fy + 4 * SS),
                       (fx - 5 * SS, fy)],
                      fill=(255, 236, 150))
            d.ellipse([fx - 2.4 * SS, fy - 5 * SS, fx + 2.4 * SS, fy + 1 * SS],
                      fill=(255, 255, 225))
        # ---- text ----
        d = ImageDraw.Draw(img, "RGBA")
        glow_text(img, (CW * SS // 2, int(CH * SS * 0.13)), "Make a Wish!", f_script,
                  GOLD_HI, (255, 180, 90), glow_radius=8 * SS, glow_alpha=0.75,
                  shimmer=(t, 2.0))
        for k in range(7):
            ang = t * 1.8 + k * math.pi * 2 / 7
            sx = CW * SS / 2 + math.cos(ang) * (190 + 22 * math.sin(t + k)) * SS / 1.6
            sy = int(CH * SS * 0.13) + math.sin(ang * 0.9) * 18 * SS
            tw = 0.5 + 0.5 * math.sin(t * 5 + k * 2)
            d.polygon(star_poly(sx, sy, (2.2 + 2.6 * tw) * SS, rot=ang), fill=GOLD)
        frames.append(img.resize((CW, CH), Image.LANCZOS))
    return frames

# ---------------------------------------------------------------- scene 3: gifts
def make_gifts():
    FPS, DUR = 12, 3.6
    N = int(FPS * DUR)
    palette = [GOLD, ROSE, TEAL, CREAM, CORAL, PURPLE]
    conf = Confetti(18, GW, GH, palette, speed=(15, 40), size=(3, 7))
    frames = []
    f_line = playfair(int(26 * SS), weight=700, italic=True)
    boxes = [((150, GOLD, ROSE), 165), ((240, ROSE, GOLD), 300), ((330, TEAL, GOLD), 435)]
    for i in range(N):
        t = i / FPS
        global dt_global
        dt_global = t
        conf.step(1 / FPS)
        img = vgrad(GW * SS, GH * SS, (24, 14, 48), (60, 30, 68),
                    glow_center=(GW * SS // 2, int(GH * SS * 0.7)),
                    glow_color=(140, 95, 130), glow_r=0.85, glow_a=0.3)
        d = ImageDraw.Draw(img, "RGBA")
        draw_stars(d, GW * SS, GH * SS, t, n=16, seed=5)
        conf.draw(d)
        # ---- gift boxes ----
        for bi, ((bx, box_col, ribbon_col), cx) in enumerate(boxes):
            cx *= SS
            pop_t = 0.9 + bi * 0.9           # when this box pops
            bw, bh = 92 * SS, 74 * SS
            by = int(GH * SS * 0.78)
            d.rounded_rectangle([cx - bw // 2, by - bh, cx + bw // 2, by],
                                radius=8 * SS, fill=box_col)
            d.rectangle([cx - 9 * SS, by - bh, cx + 9 * SS, by], fill=ribbon_col)
            d.rectangle([cx - bw // 2, by - bh, cx + bw // 2, by - bh + 12 * SS],
                        fill=ribbon_col)
            # lid (pops!)
            age = t - pop_t
            if age < 0:
                lid_y = by - bh
                rot = 0
            else:
                u = min(1.0, age / 0.5)
                lid_y = by - bh - (u ** 2) * 30 * SS
                rot = math.sin(u * math.pi) * 0.5
            lid_img = Image.new("RGBA", (bw + 16 * SS, 20 * SS), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lid_img)
            dl.rounded_rectangle([0, 0, bw + 16 * SS, 18 * SS], radius=6 * SS,
                                 fill=box_col, outline=ribbon_col, width=3 * SS)
            dl.rectangle([bw // 2 + 8 * SS - 9 * SS, 0, bw // 2 + 8 * SS + 9 * SS, 18 * SS],
                         fill=ribbon_col)
            if rot:
                lid_img = lid_img.rotate(math.degrees(rot), expand=True,
                                         resample=Image.BICUBIC)
            img.paste(lid_img.convert('RGB'), (int(cx - bw // 2 - 8 * SS), int(lid_y - 10 * SS)), lid_img)
            d = ImageDraw.Draw(img, "RGBA")
            # bow
            for sgn in (-1, 1):
                d.polygon([(cx, by - bh - 8 * SS),
                           (cx + sgn * 26 * SS, by - bh - 22 * SS),
                           (cx + sgn * 20 * SS, by - bh - 2 * SS)], fill=ribbon_col)
            d.ellipse([cx - 6 * SS, by - bh - 14 * SS, cx + 6 * SS, by - bh - 2 * SS],
                      fill=lerp(ribbon_col, (255, 255, 255), 0.35))
            # burst on pop
            if 0 <= age <= 1.2:
                rng = random.Random(bi * 31 + 5)
                for k in range(14):
                    ang = rng.uniform(0, math.pi * 2)
                    sp = rng.uniform(60, 150)
                    u = min(1.0, age / 1.2)
                    px = cx + math.cos(ang) * sp * u
                    py = (by - bh - 30 * SS) + math.sin(ang) * sp * u + 40 * u * u * SS
                    fade = 1 - u
                    r = (2.5 * fade + 0.5) * SS
                    col = lerp(rng.choice(palette), (50, 40, 70), 1 - fade)
                    d.ellipse([px - r, py - r, px + r, py + r], fill=col)
        # ---- text ----
        glow_text(img, (GW * SS // 2, int(GH * SS * 0.22)),
                  "To the most wonderful year ahead!", f_line, CREAM,
                  (255, 190, 100), glow_radius=6 * SS, glow_alpha=0.7,
                  shimmer=(t, 2.0))
        frames.append(img.resize((GW, GH), Image.LANCZOS))
    return frames

if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = "/home/user/birthday_card"
    if which in ("hero", "all"):
        save_gif(make_hero(), f"{out}/hero_happy_birthday.gif", duration=66)
    if which in ("cake", "all"):
        save_gif(make_cake(), f"{out}/cake_make_a_wish.gif", duration=66)
    if which in ("gifts", "all"):
        save_gif(make_gifts(), f"{out}/gifts_finale.gif", duration=66)
