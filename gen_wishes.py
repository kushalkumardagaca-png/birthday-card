#!/usr/bin/env python3
"""Generates 144 unique birthday-wish company cards (names, messages, palettes)
and builds the final index.html for the Birthday Wishes Wall."""

import json
import random

random.seed(252026)

# ---------------------------------------------------------------- companies
# 48 industries x 3 companies = 144. Each company gets a unique message
# assembled from a unique (opening, industry flavor line, closing) triple.
IND = [
    # (emoji, [3 company names], industry label, [3 flavor lines])
    ("☕", ["Blue Harbor Roasters", "Copperkettle Coffee Co.", "Morning Tide Roasting"],
     "Specialty Coffee",
     ["may every single morning of your new year begin with warmth in the cup and calm in the heart.",
      "here's to a year that brews slowly, tastes rich, and never runs bitter.",
      "we measured it carefully: your year ahead contains exactly 365 perfect mornings. Enjoy every one."]),
    ("🥐", ["The Gilded Crumb", "Amber Oven Bakehouse", "Larkspur Patisserie"],
     "Artisan Bakery",
     ["may your year ahead rise beautifully, turn golden at the edges, and be layered with the sweetest surprises.",
      "we believe the best things in life are freshly made — may this year hand you something wonderful straight from the oven.",
      "a birthday, like good pastry, should be flaky, buttery, and gone before you know it. Savour every bite of this one."]),
    ("📚", ["Fable & Fern Books", "Dog-Eared Page Press", "Inkwell & Quill Library"],
     "Booksellers",
     ["may the next chapter of your life be the one you will re-read forever.",
      "here's to plot twists that turn out to be blessings in disguise.",
      "we stock thousands of stories, and yours remains our favourite series. Happy birthday to a bestseller of a human."]),
    ("⏰", ["Meridian Timepieces", "Aurelia Clockworks", "Tick-Tock & Whitaker"],
     "Watchmakers",
     ["may every hour of your new year be one worth remembering, and may time be gentle with you.",
      "we make watches, so trust us on this: the good hours always feel too short. May you get countless of them.",
      "a very fine year takes very fine timing — and yours starts today, right on schedule."]),
    ("🏨", ["Harborlight Hotels", "The Velvet Key Inn", "Solstice Grand Suites"],
     "Hospitality",
     ["consider this your lifelong upgrade: may every room you enter feel like a suite, and every day feel like check-in at your favourite place.",
      "may the year ahead feel like the best kind of stay — effortless, comfortable, and impossible to want to leave.",
      "our motto is 'welcome home' — may the whole world treat you that way this year."]),
    ("🍯", ["Golden Meadow Apiaries", "Clover & Comb Honey", "Sundrop Apiary"],
     "Beekeepers",
     ["from three hundred thousand bees: may your year be buzzing, golden, and unreasonably sweet.",
      "we know busy — you know busy. May this year finally flow as smoothly as honey off the spoon.",
      "the hive voted unanimously: you deserve twelve months of golden days. The motion passes."]),
    ("🌿", ["Juniper & Sage Botanicals", "Fernbrook Gardens", "Verdant House Herbarium"],
     "Botanical Gardens",
     ["may you grow slowly, root deeply, and bloom exactly when you're ready — the best things in nature are never rushed.",
      "here's to a year of good seasons: rain when you need rest, sun when you need energy.",
      "every garden celebrates the day its finest plant arrived. Today, that's you."]),
    ("🗺️", ["Indigo Atlas Cartography", "True North Map House", "Meridian Lines Ltd."],
     "Cartographers",
     ["may the year ahead be the kind of journey where every wrong turn leads somewhere wonderful.",
      "we've charted the whole world, and we can say with confidence: the best destination this year is wherever you're happiest.",
      "here's to new places, good company, and a compass that always points toward joy."]),
    ("🎵", ["Cadence House Records", "Blueleaf Music Hall", "Allegro & Sons"],
     "Music",
     ["may your new year have a soundtrack worth dancing to — and may the good songs play on repeat.",
      "we live by one rule: life sounds better in a major key. May yours stay bright all year.",
      "a very wise orchestra once said: celebrate every note. Today's note is yours."]),
    ("🏺", ["Clay & Ember Studio", "Wheelhouse Pottery", "Terra & Glaze Works"],
     "Ceramic Artists",
     ["may this year shape you gently, fire you strong, and glaze you in all things golden.",
      "the finest pieces take time and heat — may every challenge this year leave you more beautiful than before.",
      "we craft things made to last. Here's to a year of moments just as durable."]),
    ("🔭", ["Starfield Observatory", "Celestia Sky Institute", "Nova Point Telescope Co."],
     "Astronomers",
     ["our telescopes confirm it: a star was born on this day. May it shine at record brightness this year.",
      "the universe is 13.8 billion years old and still celebrating your arrival. So are we.",
      "wishing you a year of clear skies, quiet wonder, and at least one perfect meteor."]),
    ("✂️", ["Winslow & Thread", "Bespoke Avenue Tailors", "Needle & Noble"],
     "Tailors",
     ["may the year ahead fit you perfectly — no loose threads, no tight spots, and impeccable lining.",
      "we tailor suits, but you were cut from finer cloth. Happy birthday to a one-of-a-kind original.",
      "here's to a year that suits you down to the ground."]),
    ("🍫", ["Cocoa Atelier No. 7", "Marble & Melt Chocolates", "The Ganache Room"],
     "Chocolatiers",
     ["may your year be like the finest truffle: rich, surprising, and gone far too soon.",
      "we temper chocolate for a living, so believe us: sweetness holds its shape best under pressure. You've got this year.",
      "seventy percent cacao, thirty percent joy — that's our recipe for your best year yet."]),
    ("🚲", ["Pedalworks Bicycle Co.", "Freewheel & Fender", "Summit Cycle Works"],
     "Bicycle Makers",
     ["may the year ahead have tailwinds, smooth roads, and just enough hills to keep it interesting.",
      "life is better in motion — may this year pick up speed in all the right directions.",
      "training wheels off, confidence up. This year is yours to ride."]),
    ("⛵", ["Fairwind Charters", "Spindrift Sailing Co.", "Regatta Blue Marine"],
     "Sailmakers",
     ["may your sails stay full, your anchor drop only in beautiful harbours, and your horizons keep widening.",
      "we read the winds for a living: fair breezes and following seas are headed your way all year.",
      "smooth seas never made a skilled sailor — but this year, we're requesting calm weather just for you."]),
    ("🏔️", ["Alpenrose Expeditions", "Timberline Guides", "Northface Basecamp Co."],
     "Mountain Guides",
     ["may every summit you reach this year reveal an even better view than you imagined.",
      "the mountain doesn't care about the weather, and neither should you — but may your year be all bluebird days.",
      "step by step, season by season — here's to climbing gently toward everything you want."]),
    ("🕯️", ["Lumière & Wick", "Emberglow Candle Co.", "Honeywax Studio"],
     "Candle Makers",
     ["may your year burn steady, glow warm, and scent every room you walk into with something good.",
      "we know light: even the smallest flame pushes back a lot of dark. Keep shining this year.",
      "one wish per candle — but for you, we lit the whole box."]),
    ("🎷", ["The Velvet Brass Lounge", "Midnight Ramble Club", "Satin & Sax Revue"],
     "Jazz Club",
     ["may your year swing, improvise beautifully, and always find its way back to the melody.",
      "jazz rule number one: when you don't know what's coming, make it sound intentional. Best of luck with the solo this year!",
      "the house band has been rehearsing 'Happy Birthday' in seven keys. They're ready. Are you?"],
     ),
    ("🎭", ["Marquee & Velvet Theatre", "Curtain Call Productions", "The Gilded Stage Co."],
     "Theatre",
     ["may your year get standing ovations, and may all your entrances be grand ones.",
      "we've seen a thousand opening nights — yours is the one worth publishing. Enjoy your spotlight.",
      "break a leg this year — but only metaphorically. The show must go on beautifully."]),
    ("📝", ["Papyrus Post Stationers", "Deckle & Fold Paper Co.", "Vellum Lane Press"],
     "Stationers",
     ["may your year be written in beautiful ink, on paper that never tears, in a story you love reading back.",
      "we believe the small things matter: good pens, thick paper, and birthdays properly celebrated.",
      "consider this card our finest stock — reserved for very fine people."]),
    ("🖊️", ["Ironwood Pen Works", "Fountain & Nib Ltd.", "Scriptorium Fine Pens"],
     "Pen Makers",
     ["may the year ahead write itself smoothly — bold strokes, no smudges, and a signature people remember.",
      "we craft instruments for important words. These are some: Happy Birthday, Kushal.",
      "here's to signing great deals, great memories, and great years. Start with the last one."]),
    ("📷", ["Silverleaf Studios", "Aperture & Ivy Photo", "Golden Hour Gallery"],
     "Photographers",
     ["may your year be full of golden hours, candid laughter, and frames worth keeping forever.",
      "we chase light for a living — and people like you are why. Happy birthday to a natural highlight.",
      "the best photos are never posed. May your year unfold just as beautifully unscripted."]),
    ("🧀", ["Cloverhill Creamery", "Rind & Rennet Dairy", "Meadowbrook Cheese Cave"],
     "Cheesemakers",
     ["may your year age gracefully, pair well with everything, and improve with every month.",
      "we're in the business of patience and good things — may both find you this year.",
      "life is richer with a little culture. Happy birthday from our whole (curd-loving) team."]),
    ("🌸", ["Petal & Stem Florals", "Bloomerie Flower House", "Rosalind's Garden Co."],
     "Florists",
     ["may your year be in constant, beautiful bloom — and may someone hand you flowers for no reason at all.",
      "every bouquet we've ever made says something. This one says: the world is lovelier with you in it.",
      "here's to a year that blossoms in all the right directions."]),
    ("🍵", ["Mistral Tea House", "Steep & Saucer Co.", "Jade Kettle Teahouse"],
     "Tea House",
     ["may your year steep slowly, warm both hands, and never go bitter on you.",
      "we believe problems look smaller over a second pot. May this year need neither.",
      "the kettle is on, the cups are out, and today we're toasting one thing only: you."]),
    ("🛏️", ["Everline Linens", "Cloudrest Bedding Co.", "Loomcraft Home"],
     "Fine Linens",
     ["may your nights be cloud-soft and your mornings feel like freshly pressed possibilities.",
      "we make comfort for a living — may this year wrap you in the same quality.",
      "here's to a year of good rest, slow Sundays, and dreams that actually come true."]),
    ("🧭", ["Wayfarer & Compass", "Longitude Travel House", "Voyager's Outfitters"],
     "Travel Outfitters",
     ["may your year include one great journey, a window seat, and a bag packed light with worries.",
      "we equip wanderers — and we've never met one who deserved a grand tour more.",
      "the world is big and your year is fresh. May they meet each other halfway."]),
    ("🍦", ["Cypress Gelateria", "Sugarcone & Sea", "Alba Gelato Kitchen"],
     "Gelateria",
     ["may your year have sprinkles on ordinary days and a cherry on the really good ones.",
      "we scoop happiness by the cone — may life do the same for you, twice, with extra toppings.",
      "best served immediately, best shared widely: that's gelato, and that's this wish."]),
    ("🎨", ["Prisma Fine Arts", "Chroma Collective Gallery", "Ochre & Umber Studio"],
     "Art Gallery",
     ["may your year be painted in bold strokes, warm tones, and at least one colour nobody expected.",
      "every masterpiece begins with a single brave mark. Yours starts again today.",
      "we hang art that makes people stop and stare. Thank you for doing that in life."]),
    ("🌊", ["Tidewater Aquarium", "Coral & Current Institute", "Deep Blue Discovery"],
     "Aquarium",
     ["may your year move with the calm confidence of a very content sea turtle.",
      "we've studied the ocean for years: even the biggest waves pass. May yours carry you somewhere lovely.",
      "from the octopus, the seahorses, and one extremely enthusiastic dolphin: happy birthday."]),
    ("🚂", ["Grand Meridian Railway", "Steam & Cedar Rail Co.", "Blue Comet Trains"],
     "Railway",
     ["may your year run on time, take the scenic route, and make every stop worth remembering.",
      "all aboard the best year yet — first-class ticket, window seat, no changes required.",
      "we've been running trains for a century: the journey matters more than the destination. Enjoy yours."]),
    ("🪐", ["Aurora Planetarium", "Stellar Dome Institute", "Comet & Crown Space Co."],
     "Planetarium",
     ["we project the cosmos nightly, and we can confirm: your constellation is having its best alignment in years.",
      "somewhere out there, a star the same age as you is still burning bright. Keep each other company this year.",
      "may your gravity be strong, your orbits stable, and your year full of wonder."]),
    ("🎺", ["The Orpheum Opera", "Bel Canto House", "Aria & Antiphon Co."],
     "Opera House",
     ["may your year hit every high note and recover gracefully from the occasional low one.",
      "the maestro insists: passion first, precision second, celebration always. Happy birthday!",
      "tonight's programme: one overture, one aria, and one standing ovation — all for you."]),
    ("🍏", ["Amberfield Orchards", "Suncrest Farms", "Orchard Lane Growers"],
     "Orchards",
     ["may your year be heavy with good fruit, light with worry, and sweet to the core.",
      "the best crops take all season — may everything you've planted finally come in this year.",
      "we picked our finest basket for today. Consider it delivered."]),
    ("🧵", ["Loom & Lark Textiles", "Shuttle & Skein Works", "Heirloom Weaving Co."],
     "Weavers",
     ["may the threads of your year weave into something you'll be proud to hand down.",
      "we believe in taking raw material and making it beautiful. You're already most of the way there.",
      "tight weave, soft touch, strong finish — that's our recipe for textiles and for years."]),
    ("🏰", ["Thornbury Keep Estates", "Ivywall Heritage House", "Kingsmere Manor"],
     "Heritage Estates",
     ["may your year be rich in tradition, generous in comfort, and grand in every small detail.",
      "some things only improve with age: estates, wine, and people born on days like today.",
      "the manor has prepared the long table, the good candles, and the finest wishes — all for you."]),
    ("🐦", ["Dawn Chorus Aviary", "Featherpost Bird Sanctuary", "Skylark & Finch Co."],
     "Aviary",
     ["may your year begin each morning with birdsong and end each night with quiet skies.",
      "our flock learned a new phrase just for today. It sounds suspiciously like 'happy birthday'.",
      "a bird doesn't sing because it has answers — it sings because it has a song. May yours never stop."]),
    ("🪞", ["Silverglass Mirror Co.", "Bevel & Shine Studio", "Looking Glass Works"],
     "Mirror Makers",
     ["we polish glass all day, so trust our expert opinion: what we'd really like to see this year is more of you smiling.",
      "may the year ahead reflect back everything good you put out into the world.",
      "our mirrors never lie — and today, they show someone worth celebrating."]),
    ("🍀", ["Four-Leaf Farm", "Cloverline Fields", "Shamrock Grove Acres"],
     "Lucky Farms",
     ["we searched every field we own and found exactly one four-leaf clover. It has your name on it.",
      "may luck find you early, stay late, and bring friends.",
      "some people make their own luck — may this year hand you a little of both."]),
    ("🛍️", ["Emporium & Thread", "Bramble & Beau Goods", "The Curated Cart"],
     "Curated Goods",
     ["we've spent years collecting beautiful things, and today we're reminded the best ones aren't things at all.",
      "may your year include small luxuries, perfect finds, and one purchase you never regret.",
      "consider this wish hand-picked, gift-wrapped, and delivered with care."]),
    ("☕", ["Verona Espresso Bars", "Crema & Co. Coffee", "Lantern Roast House"],
     "Espresso Bars",
     ["may your year be perfectly extracted: strong where it counts, sweet in the finish.",
      "double shot of joy, splash of luck, no bitterness — that's your order for the year, on us.",
      "we pull 400 shots a day, and today every single one is a toast to you."]),
    ("🍯", ["Hillcrest Preserves", "Orchard Gold Jams", "Bramble & Rose Conserves"],
     "Preservers",
     ["we seal the best of every season into jars — may your year preserve only its sweetest moments.",
      "some things are worth keeping: summer fruit, good friends, and people like you.",
      "a jar a day keeps the gloom away. We've stocked your year accordingly."]),
    ("🚿", ["Rainspa Bath House", "Cascade & Cedar Springs", "Steam & Stone Baths"],
     "Bath House",
     ["may your year wash away what doesn't matter and leave you feeling brand new.",
      "heat, steam, stillness — our three secrets, and our three wishes for your year.",
      "you've carried a lot. Today, and this whole year, let the world carry you."]),
    ("🎡", ["Aurora Fairgrounds", "Lantern Wheel Carnival", "Starlight Amusements"],
     "Amusements",
     ["may your year feel like the front row of the Ferris wheel: elevated, bright, and worth the queue.",
      "we run the fun for a living — and we've never seen a queue this worth it. Happy birthday!",
      "cotton candy rules apply: messy, sweet, gone too fast. Enjoy every second of this year."]),
    ("🎻", ["Stradivaria Strings", "Bows & Bridges Music", "Cantabile Instrument Co."],
     "Instrument Makers",
     ["may your year stay in tune, project beautifully, and inspire spontaneous applause.",
      "we build instruments that outlive their makers. May your influence do exactly the same.",
      "four strings, endless possibilities. Same goes for your year."]),
    ("🌱", ["First Sprout Nursery", "Greenhouse No. 9", "Sapling & Soil Co."],
     "Nursery",
     ["may everything you quietly plant this year burst into growth when you least expect it.",
      "big trees start as stubborn little seeds. Keep pushing toward the light.",
      "we grow things for a living — and people like you are proof the soil is good."]),
    ("🧊", ["Frost & Crystal Ice Co.", "Polar Springs Water", "Glacier & Co. Refreshments"],
     "Spring Water",
     ["may your year stay crisp, your worries stay diluted, and your glass stay full.",
      "purest ingredients, zero impurities — that's our wish for your year ahead.",
      "stay cool, stay clear, stay refreshing. You've always managed it."]),
    ("🪁", ["Skynote Kite Works", "Tailwind Toys", "Zephyr & String Co."],
     "Kite Makers",
     ["may your spirits stay high, your strings stay untangled, and your feet touch the ground only when you want them to.",
      "we send things aloft for a living — but you've always known how to rise on your own.",
      "the wind is friendly today. It knows whose birthday it is."]),
]

OPENINGS = [
    "Dear Kushal,",
    "Happy birthday, Kushal!",
    "To Kushal, on his special day —",
    "Good morning, birthday champion —",
    "Dear Mr. Birthday himself,",
    "Kushal —",
    "Dearest Kushal,",
    "To a truly remarkable birthday person:",
    "Attention, birthday star:",
    "Dear Kushal, on behalf of our entire team:",
    "For Kushal, with pleasure:",
    "A very important announcement for Kushal:",
    "Dear Kushal, first things first:",
    "To the one and only Kushal —",
    "From all of us, to Kushal:",
    "Dear Kushal, before anything else today:",
    "Greetings and cake, Kushal!",
    "To Kushal of the September birthday —",
    "Dear birthday VIP,",
    "Kushal, happiest of birthdays from our whole floor:",
    "A public service announcement: Kushal is having a birthday.",
    "Dear Kushal, please stop everything —",
    "With great enthusiasm, to Kushal:",
    "Dear Kushal, the management requests —",
    "To Kushal, certainly and immediately:",
    "Happy birthday to Kushal, formally and joyfully:",
    "Kushal — a word, if we may:",
    "Dear Kushal, from the entire workshop:",
    "Dear Kushal, from behind our counters and desks:",
    "To Kushal, whose birthday it gloriously is:",
    "Notice to all calendars: it's Kushal's birthday.",
    "Dear Kushal, all of us agreed on this:",
    "Kushal, permit us a moment —",
    "To Kushal, warmly and without delay:",
    "Dear Kushal, consider this official:",
    "A cheerfully formal note to Kushal:",
    "Kushal, today's agenda has one item:",
    "To Kushal, on behalf of everyone who knows him:",
    "Dear Kushal — yes, you:",
    "Happy birthday, Kushal. Truly.",
    "To Kushal, from the bottom of our org chart:",
    "Dear Kushal, the sign on our door today reads:",
    "Kushal, this one's for you:",
    "To a September classic — Kushal:",
    "Dear Kushal, allow us to be direct:",
    "Kushal, the whole team signs below —",
    "To Kushal, no occasion greater:",
    "Dear Kushal, our finest customer of birthdays:",
]

CLOSINGS = [
    "Warmest regards,", "With birthday cheers,", "Yours in celebration,",
    "Respectfully and joyfully,", "With kindest wishes,", "Warmly,",
    "In festive spirit,", "Sincerely, and with cake,", "With admiration,",
    "Cheerfully yours,", "Most warmly,", "With every good wish,",
    "Respectfully yours,", "Brightly and warmly,", "In true celebration,",
    "With gratitude and joy,",
]

FOOTERS = [
    "The {name} Team", "Everyone at {name}", "Your friends at {name}",
    "The whole crew at {name}", "All of us at {name}", "The {name} family",
    "Warmly, from {name}", "The management & staff of {name}",
]

PALETTES_DARK = [
    ("#1B1436", "#34205C", "#F6CD64", "#FFF6E6", "#BBA9D6"),
    ("#0F2438", "#1E4A5F", "#5FD3C4", "#EAFBF8", "#9CC8C0"),
    ("#2B0F22", "#57204A", "#FF9EC3", "#FFEDF5", "#D6A8C0"),
    ("#101F1A", "#1F4A38", "#7FE0A0", "#EAFFF2", "#A3CDB4"),
    ("#28140E", "#5A2E18", "#FFAE5D", "#FFF0E0", "#D6B49A"),
    ("#131A38", "#28376B", "#8FA8FF", "#EDF0FF", "#A8B0D6"),
    ("#251422", "#4A1E3E", "#E37FB4", "#FFEAF4", "#C7A0BA"),
    ("#161616", "#3A3A3A", "#E8E0C8", "#FFFDF4", "#C2BBA8"),
    ("#12262B", "#1F4A50", "#6FD6D6", "#E8FAFA", "#9CC4C7"),
    ("#2A1A0E", "#553A16", "#F0C05A", "#FFF7E0", "#D6BE96"),
    ("#1E1030", "#42246A", "#B48CFF", "#F4EDFF", "#BCA9D6"),
    ("#0E2430", "#1C4A4E", "#63D6B8", "#E9FBF5", "#9BC8BF"),
    ("#301414", "#5E2424", "#FF8A7A", "#FFEDE8", "#D6A5A0"),
    ("#141E2E", "#2A4059", "#7EA6E0", "#EBF2FC", "#A3B5CC"),
    ("#241A0E", "#4A3A14", "#E0C05A", "#FBF7E2", "#C2B696"),
]
PALETTES_LIGHT = [
    ("#FDF3E3", "#F7E3C0", "#B07818", "#3A2A10", "#8A7355"),
    ("#EDF7F3", "#D2ECDF", "#1F7A55", "#0F3A28", "#4A7A64"),
    ("#FFF0F4", "#FBDCE6", "#C2447C", "#4A1230", "#A06E84"),
    ("#F0F5FF", "#DCE8FB", "#3A62C2", "#16255A", "#6E7FA0"),
    ("#FFF7EC", "#FBEAD0", "#B06A20", "#3F2708", "#9A7A54"),
    ("#F4FBF9", "#DDF2EC", "#2A8A76", "#0E3A30", "#5F8A7E"),
    ("#FAF0FF", "#F0DCF9", "#8A44C2", "#31105A", "#8A6EA0"),
    ("#FFFBEF", "#F8F0D8", "#8A7A1F", "#3A3208", "#8A7E55"),
    ("#F0FAF8", "#D8F2EE", "#1F8A9A", "#0A3A42", "#5F8A90"),
    ("#FFF3F0", "#FBE2DB", "#C25537", "#4A1B0F", "#A07566"),
    ("#F5F5FA", "#E4E4F2", "#4A4AA0", "#1A1A45", "#74749A"),
    ("#EFF9F0", "#DAF0DD", "#3A8A45", "#14381A", "#648A6A"),
    ("#FDF6EF", "#F5E8D5", "#9A6A3A", "#3A2810", "#9A8465"),
    ("#EEF6FF", "#D9EBFB", "#2A6AC2", "#0E2A5A", "#6A82A4"),
    ("#FBF4FF", "#F2E4FB", "#7A3AB2", "#2E1050", "#8A6C9E"),
]



import colorsys

def _shift(hex_color, deg):
    """Shift hue of a hex color by deg degrees."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    hh = (hh + deg / 360.0) % 1.0
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))

def _variant(base, k):
    """k = 0..4 unique variant of a base palette."""
    bg1, bg2, accent, text_c, sub = base
    d = (k - 2) * 7  # -14..+14 degrees
    return (_shift(bg1, d), _shift(bg2, d), _shift(accent, d), text_c, sub)

DARK_VARIANTS = [_variant(p, k) for p in PALETTES_DARK for k in range(5)]
LIGHT_VARIANTS = [_variant(p, k) for p in PALETTES_LIGHT for k in range(5)]

def build_wishes():
    companies = []
    for emoji, names, industry, flavors in IND:
        assert len(names) == len(flavors) == 3, f"bad industry: {names}"
        for n, f in zip(names, flavors):
            companies.append({"emoji": emoji, "name": n, "industry": industry, "flavor": f})

    assert len(companies) == 144, f"expected 144, got {len(companies)}"

    names = [c["name"] for c in companies]
    assert len(set(names)) == 144, "duplicate company names!"

    # unique message assembly: rotate openings/closings so every full text differs
    wishes = []
    used_texts = set()
    oi, ci, fi = 0, 0, 0
    for idx, c in enumerate(companies):
        for attempt in range(200):
            if idx % 4 == 3:
                opening = ""
            else:
                opening = OPENINGS[(oi + attempt * 13) % len(OPENINGS)] + " "
            closing = CLOSINGS[(ci + attempt * 7) % len(CLOSINGS)]
            footer = FOOTERS[(fi + attempt * 5) % len(FOOTERS)].format(name=c["name"])
            flavor = c["flavor"]
            if opening == "":
                flavor = flavor[0].upper() + flavor[1:]
                text = f"{flavor} {closing} {footer}."
            else:
                text = f"{opening}{flavor} {closing} {footer}."
            if text not in used_texts:
                break
        used_texts.add(text)
        oi += 1; ci += 5; fi += 2

        # unique palette per card (rotate dark/light, unique hue variants)
        if idx % 2 == 0:
            bg1, bg2, accent, text_c, sub = DARK_VARIANTS[(idx // 2) % len(DARK_VARIANTS)]
            theme = "dark"
        else:
            bg1, bg2, accent, text_c, sub = LIGHT_VARIANTS[(idx // 2) % len(LIGHT_VARIANTS)]
            theme = "light"

        wishes.append({
            "n": idx + 1,
            "company": c["name"],
            "emoji": c["emoji"],
            "industry": c["industry"],
            "msg": text,
            "est": 1900 + ((idx * 37) % 120),
            "theme": theme,
            "bg1": bg1, "bg2": bg2, "accent": accent, "text": text_c, "sub": sub,
        })

    # uniqueness of palettes: (bg1,accent) pairs must all differ
    pal = [(w["bg1"], w["accent"]) for w in wishes]
    assert len(set(pal)) == 144, f"palettes not unique: {len(set(pal))}"
    msgs = [w["msg"] for w in wishes]
    assert len(set(msgs)) == 144, "messages not unique!"

    with open("/home/user/birthday_card/wishes.json", "w") as f:
        json.dump(wishes, f, ensure_ascii=False, indent=1)
    print(f"144 wishes generated · all names, messages and palettes unique ✓")
    return wishes


if __name__ == "__main__":
    build_wishes()
