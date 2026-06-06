"""
Soulful Existence Astro Content Plugin v5
- Branded Pillow graphics (no AI image gen)
- 115 social-optimized hooks across 8 categories
- Platform-specific formatting
- Tiered hashtag strategy
- Daily 5am Eastern + Sunday weekly batch
"""

import os
import json
import random
import urllib.request
import urllib.error
import base64
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from io import BytesIO

COSMIC_API_URL = os.environ.get("KERYKION_API_URL", "https://cosmic-api-production-d4f6.up.railway.app")
COSMIC_API_KEY = os.environ.get("KERYKION_API_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_pillow():
    try:
        from PIL import Image
        return True
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "--break-system-packages", "-q"])
        try:
            from PIL import Image
            return True
        except ImportError:
            return False

def ensure_fonts():
    font_dir = "/data/.hermes/fonts"
    os.makedirs(font_dir, exist_ok=True)
    fonts = {
        "CormorantGaramond-LightItalic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond-LightItalic.ttf",
        "CormorantGaramond-Light.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond-Light.ttf",
    }
    for name, url in fonts.items():
        path = os.path.join(font_dir, name)
        if not os.path.exists(path) or os.path.getsize(path) < 1000:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(path, "wb") as f:
                        f.write(resp.read())
            except Exception:
                pass

def generate_graphic(event_name, pull_quote, post_date, handle="@soulfulxistence"):
    if not ensure_pillow():
        return None
    ensure_fonts()
    try:
        graphic_path = os.path.join(PLUGIN_DIR, "se_graphic.py")
        if not os.path.exists(graphic_path):
            return None
        import importlib.util
        spec = importlib.util.spec_from_file_location("se_graphic", graphic_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        b64 = mod.draw_se_graphic(event_name, pull_quote, post_date, handle)
        return b64
    except Exception as e:
        return None

# ── Voice ─────────────────────────────────────────────────────────────────────

SE_VOICE = """You are writing social media content for Gen Rodriguez of Soulful Existence.
Gen is a tarot reader, medium, and past life regression practitioner based in the US.

WRITE EXACTLY LIKE THIS:
Gen writes like she is talking to someone she knows. Not a stranger, not a client. Someone she would actually text.

HOW SHE WRITES:
- Short sentences that land. She does not over-explain.
- She defines astrology terms once, plainly, then moves on.
- She connects astrology to what is actually happening in real life.
- She makes it personal without oversharing. One real detail. Then moves on.
- Dry wit shows up occasionally but never tries too hard.
- She ends posts with a direct question or a short punchy line. Never a motivational sign-off.
- She trusts her audience to keep up.

NEVER:
- "The cosmos are inviting you to..."
- "Energy" as a filler word more than once per post
- Fake urgency: "now is the time to..."
- Motivational sign-offs
- Exclamation points unless something is genuinely surprising
- Dashes as bullet points

PARAGRAPH STRUCTURE:
Para 1 — What is happening. Plain. Define terms once.
Para 2 — Why it matters. Real life connection.
Para 3 — Speak directly to the reader. Personal and grounding.
Para 4 — Optional. Question or landing line only if it adds something.

TONE REFERENCE:
"Mercury is definitely retrograding. I have had a few old so-called friends follow me on here in the last week or so. There is a reason they are not in my life anymore, but apparently they are curious."
"I love when astrology makes sense."
"The sky gives you the weather. Your birth chart tells you what to wear."

SERVICES (one CTA max, used sparingly):
Tarot readings, Mediumship, Past Life Regression, Digital products at soulfulexistence.com"""

# ── Hooks ─────────────────────────────────────────────────────────────────────

HOOKS = {
    "transit_and_sky": [
        "Nobody talks about what {transit} actually does to your {life_area}.",
        "I have been watching {transit} all year. Here is what I am seeing.",
        "This is the part of {transit} that nobody warns you about.",
        "{Transit} is not what most people think it is.",
        "Something shifted in the sky this week. Here is what that means for you.",
        "The sky is doing something interesting right now and it explains a lot.",
        "If you have been feeling {feeling} lately, there is a reason for that.",
        "{Transit} does not announce itself. It just starts working.",
        "We are in {transit} territory right now.",
        "This is what {transit} is asking you to look at.",
        "Not every astrologer will tell you this about {transit}.",
        "{Planet} just moved into {sign}. Here is what changes.",
        "The {moon_phase} is coming. Here is what to do with that.",
        "This week the sky is asking one specific question.",
        "Everyone is talking about {transit}. Here is what it actually means in real life.",
        "{Transit} hits different when you understand what it is actually doing.",
        "I keep saying this in readings and I will say it here too.",
        "What nobody tells you about {moon_phase} energy.",
        "The {planet} energy this week is about one thing.",
        "If {transit} has been making your life feel {adjective}, that tracks."
    ],
    "tarot": [
        "The {card} keeps coming up in readings right now and it makes complete sense.",
        "If the {card} has been showing up for you, here is what it is trying to say.",
        "I pulled the {card} this morning. Here is what I think it means for the collective.",
        "The tarot card that describes this week is {card} and here is why.",
        "This is what the {card} actually means — not the watered down version.",
        "Three cards that keep coming up in readings this month.",
        "The {card} is one of the most misunderstood cards in the deck.",
        "Your card for this week is {card}. Here is what it is asking.",
        "I have been reading tarot for years and the {card} still stops me every time.",
        "The difference between the {card} and what people think it means."
    ],
    "personal": [
        "Something I notice in almost every reading I do right now.",
        "I said this to a client yesterday and I think more people need to hear it.",
        "This comes up in readings more than anything else right now.",
        "A pattern I keep seeing that I think is worth talking about.",
        "I do not say this lightly but something is shifting for a lot of people right now.",
        "The question I get asked most often in readings, and my honest answer.",
        "Something changed in my own chart this year and I finally understand what it was.",
        "I used to think this about astrology. I do not anymore.",
        "Three things I wish I had known about astrology when I was starting out.",
        "The thing about intuition that nobody talks about.",
        "I have been doing this work long enough to notice patterns. Here is one.",
        "What I actually look at first when I sit down with someone's chart.",
        "Something my own chart has been teaching me lately.",
        "The most common thing people misunderstand about tarot readings.",
        "A reading I did recently reminded me why I do this work."
    ],
    "educational": [
        "Let me explain {concept} in plain language because the astrology world overcomplicates it.",
        "If you have never understood {concept}, here is what it actually means.",
        "{Concept} explained without the jargon.",
        "The simplest way I know how to explain {concept}.",
        "What {placement} actually means in your chart — not the textbook version.",
        "If your {placement} has ever confused you, read this.",
        "This is what it means when {planet} is in {sign} in your birth chart.",
        "The difference between your sun sign, moon sign, and rising sign — finally explained simply.",
        "What the houses in your birth chart actually represent.",
        "Why your rising sign matters more than most people realize.",
        "The one thing your birth chart can tell you that nothing else can.",
        "What it means when a planet is retrograde — the actual meaning, not the meme version.",
        "If you only ever learn one thing about astrology, learn this.",
        "Why two people with the same sun sign can be completely different.",
        "What a stellium in your chart actually means for your life.",
        "The chart placement that shows what you are working toward in this lifetime.",
        "What the North Node in your chart is actually asking you to do.",
        "The part of astrology that most beginners skip over entirely.",
        "What aspects in a birth chart actually tell you.",
        "The placement most people ignore that tells you the most about relationships."
    ],
    "sign_placement": [
        "If you have {sign} anywhere in your chart, this one is for you.",
        "People with {sign} rising navigate the world in a very specific way.",
        "Moon in {sign} people feel things differently than most. Here is how.",
        "Venus in {sign} is one of the most {adjective} placements in the chart.",
        "What it means to have {planet} in {sign} — from someone who actually works with charts.",
        "The {sign} in your chart you have probably been ignoring.",
        "This is for everyone with heavy {sign} energy in their chart.",
        "Having {sign} as your rising sign means the world sees you differently than you see yourself.",
        "The shadow side of {sign} that does not get talked about enough.",
        "If your {sign} is showing right now, there is a reason for that."
    ],
    "spiritual": [
        "Your intuition is not broken. Here is what is actually happening.",
        "The difference between intuition and anxiety — how I explain it to clients.",
        "Something I believe about psychic ability that might surprise you.",
        "Past life energy is real and here is how it shows up in your current life.",
        "What happens in a mediumship session that I think more people should understand.",
        "The thing about spirit communication that nobody talks about.",
        "Your spirit guides are not silent. Here is why you might not be hearing them.",
        "Mediumship is not what most people think it is.",
        "What past life regression actually feels like — from someone who does it.",
        "The difference between a tarot reading and a psychic reading.",
        "Why I believe everyone has intuition and not everyone believes it yet.",
        "What I have learned about grief from years of mediumship work.",
        "The most common thing that comes up in past life regression sessions.",
        "What it means when the same message keeps showing up in different ways.",
        "Something a client said in a session recently that has stayed with me."
    ],
    "direct": [
        "Astrology is not about prediction. It never was.",
        "The reason your Mercury retrograde is not ruining your life.",
        "Hot take: knowing your sun sign is the least interesting thing about your chart.",
        "If astrology feels like it does not apply to you, you are probably looking at the wrong thing.",
        "The astrology content you are seeing online is missing something important.",
        "I will say what most astrologers will not say about this transit.",
        "Astrology is not a personality test. Here is what it actually is.",
        "If someone told you that placement is bad, they were wrong.",
        "The problem with how most people use tarot.",
        "Most astrology content treats you like you cannot handle complexity. I do not.",
        "The thing about this transit that fear-based astrology content always gets wrong.",
        "I do not do doom and gloom astrology and here is why.",
        "Not all astrology advice ages well. Here is what I actually stand behind.",
        "The version of astrology you have been taught is incomplete.",
        "Why I stopped reading astrology the way I was taught."
    ],
    "engagement": [
        "Do you relate more to your sun sign or your moon sign?",
        "What placement in your chart have you struggled to understand?",
        "Has a tarot reading ever told you something you already knew but needed to hear?",
        "Which sign energy do you have the hardest time with?",
        "What is the one thing about your birth chart that makes complete sense to you?",
        "Has astrology ever explained something about yourself that nothing else could?",
        "What would you want to know if you could ask your chart one question?",
        "What does home mean to you right now?",
        "If your chart could tell you one thing you needed to hear today, what would it say?",
        "When did astrology start making sense for you?"
    ]
}

HASHTAG_TIERS = {
    "broad": ["#astrology", "#tarot", "#spirituality", "#zodiac", "#intuition", "#selfgrowth", "#mindfulness", "#spiritual"],
    "mid_astro": ["#astrologytok", "#astrologer", "#birthchart", "#moonphase", "#mercuryretrograde", "#fullmoon", "#newmoon", "#astrologycommunity"],
    "mid_tarot": ["#tarotreader", "#tarotcommunity", "#tarotreading", "#dailytarot", "#tarotcards", "#oraclecards"],
    "mid_spiritual": ["#psychic", "#medium", "#pastliferegression", "#spiritualawakening", "#higherself", "#energyhealing"],
    "niche": ["#soulfulexistence", "#genrodriguez", "#tarotreaderforwomen", "#astrologyforyou", "#spiritualbutnotweird", "#midlifespiritual"]
}

def get_hashtags(content_type="astro"):
    broad = random.sample(HASHTAG_TIERS["broad"], 3)
    niche = HASHTAG_TIERS["niche"][:3]
    if content_type == "tarot":
        mid = random.sample(HASHTAG_TIERS["mid_tarot"], 3)
    elif content_type == "spiritual":
        mid = random.sample(HASHTAG_TIERS["mid_spiritual"], 3)
    else:
        mid = random.sample(HASHTAG_TIERS["mid_astro"], 3)
    return " ".join([f"#{t.lstrip('#')}" for t in broad + mid + niche])

def get_hook(category=None):
    if not category:
        category = random.choice(list(HOOKS.keys()))
    return random.choice(HOOKS.get(category, HOOKS["transit_and_sky"]))

SIGN_PLACEMENTS = ["sun", "moon", "rising", "venus"]
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def fetch_sky_events(start_date, end_date):
    payload = json.dumps({
        "start_date": start_date, "end_date": end_date,
        "latitude": 0.0, "longitude": 0.0, "timezone": 0
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{COSMIC_API_URL}/sky-events",
        data=payload,
        headers={"Content-Type": "application/json", "x-railway-secret": COSMIC_API_KEY},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def call_llm(system, user_prompt, max_tokens=3000):
    payload = json.dumps({
        "model": "anthropic/claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": user_prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {OPENROUTER_KEY}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

def parse_json(raw):
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(clean)

DAILY_PROMPT = """Today is {today}.

SKY EVENTS (next 14 days — use ONLY these, do not invent transits):
{sky_events}

HOOK TO USE as the exact first line of every platform caption:
{hook}

PRIORITY: Write about the most significant event today or in the next 3 days.
If nothing major, write educational or evergreen astrology content.

Return ONLY valid JSON, no preamble or markdown fences:

{{
  "post_type": "major_event or upcoming_event or educational",
  "subject": "One line — what this post is about",
  "event_name": "Short astrological event name for the graphic header (max 4 words, e.g. Venus in Leo)",
  "pull_quote": "The single most shareable line from the post — max 12 words, no punctuation at end",
  "instagram": {{
    "caption": "Hook line + 3-4 paragraphs in Gen voice. Hook is the exact first line. Blank line between paragraphs. No hashtags.",
    "hashtags": "9 hashtags — 3 broad, 3 mid-range, 3 niche SE"
  }},
  "tiktok": {{
    "hook": "Spoken hook — under 8 words, punchy",
    "script": "45-60 second spoken script in Gen voice. Ends with bold statement or question, not a CTA."
  }},
  "facebook": {{
    "post": "Hook line + longer conversational version. Ends with question inviting real responses."
  }},
  "story": {{
    "text": "Pull quote or bold statement — max 10 words for graphic overlay",
    "visual_note": "One line on image mood"
  }}
}}"""

WEEKLY_PROMPT = """Today is {today} (Sunday). Weekly content batch.

SKY EVENTS (next 14 days — use ONLY these):
{sky_events}

SIGN TIP: {sign_placement} in {sign}
HOOKS: {hooks}

Return ONLY valid JSON, no preamble or markdown fences:

{{
  "weekly_overview": {{
    "event_name": "Main event name for graphic",
    "pull_quote": "Most shareable line — max 12 words",
    "instagram": {{"caption": "Hook + 3-4 paragraphs. Collective weather this week.", "hashtags": "9 hashtags"}},
    "facebook": {{"post": "Longer personal version. Ends with engagement question."}}
  }},
  "transit_spotlight": {{
    "subject": "Most significant transit this week",
    "date": "When it happens",
    "event_name": "Transit name for graphic",
    "pull_quote": "Most shareable line — max 12 words",
    "instagram": {{"caption": "Hook + 3-4 paragraphs deep dive.", "hashtags": "9 hashtags"}},
    "tiktok": {{"hook": "Spoken hook under 8 words", "script": "45-60 second script"}},
    "facebook": {{"post": "Conversational version with engagement question"}},
    "story": {{"text": "One line max 10 words", "visual_note": "Image mood"}}
  }},
  "sign_tip": {{
    "placement": "{sign_placement}", "sign": "{sign}",
    "instagram": {{"caption": "Hook + 3 paragraphs about this placement.", "hashtags": "9 hashtags"}},
    "story": {{"text": "One punchy line max 10 words"}}
  }},
  "journal_prompt": {{
    "transit_connection": "Which event this connects to",
    "instagram": {{"caption": "Hook + 3 paragraphs. Real reflective question.", "hashtags": "9 hashtags"}},
    "story": {{"text": "The question in one line"}}
  }},
  "tarot_tie": {{
    "instagram": {{"caption": "Hook + 3 paragraphs connecting sky to tarot.", "hashtags": "9 hashtags"}}
  }}
}}"""

def format_daily(data, today_str, graphic_b64):
    ig = data.get("instagram", {})
    tk = data.get("tiktok", {})
    fb = data.get("facebook", {})
    st = data.get("story", {})

    graphic_note = ""
    if graphic_b64:
        graphic_note = f"\n[GRAPHIC ATTACHED — {data.get('event_name', '')} — {data.get('pull_quote', '')}]"

    return f"""SOULFUL EXISTENCE — DAILY POST
{today_str} | {data.get("subject", "")}{graphic_note}

==================================================
INSTAGRAM
==================================================
{ig.get("caption", "")}

{ig.get("hashtags", "")}

==================================================
TIKTOK
==================================================
Hook: {tk.get("hook", "")}

{tk.get("script", "")}

==================================================
FACEBOOK
==================================================
{fb.get("post", "")}

==================================================
STORY
==================================================
"{st.get("text", "")}"
Visual: {st.get("visual_note", "")}"""

def handle_daily(params, ctx=None, **kwargs):
    try:
        today = datetime.now(timezone.utc)
        start_date = today.strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
        today_str = today.strftime("%B %d, %Y")

        sky_data = fetch_sky_events(start_date, end_date)
        sky_events = sky_data.get("events", sky_data)[:20]

        hook = get_hook(random.choice(["transit_and_sky", "personal", "direct", "educational"]))

        user_prompt = DAILY_PROMPT.format(
            today=today_str,
            sky_events=json.dumps(sky_events, indent=2),
            hook=hook
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(system=SE_VOICE, messages=[{"role": "user", "content": user_prompt}])
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            raw = call_llm(SE_VOICE, user_prompt)

        data = parse_json(raw)

        # Generate branded graphic
        graphic_b64 = generate_graphic(
            event_name=data.get("event_name", "Astrology"),
            pull_quote=data.get("pull_quote", ""),
            post_date=today_str
        )

        # Send graphic as image if context supports it
        if graphic_b64 and ctx and hasattr(ctx, "send_image"):
            try:
                img_bytes = base64.b64decode(graphic_b64)
                ctx.send_image(img_bytes, filename=f"SE_{today.strftime('%Y%m%d')}.png")
            except Exception:
                pass

        return format_daily(data, today_str, graphic_b64)

    except Exception as e:
        return f"Something went wrong: {e}"

def handle_weekly(params, ctx=None, **kwargs):
    try:
        today = datetime.now(timezone.utc)
        start_date = today.strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
        today_str = today.strftime("%B %d, %Y")

        sign_placement = random.choice(SIGN_PLACEMENTS)
        sign = random.choice(SIGNS)

        sky_data = fetch_sky_events(start_date, end_date)
        sky_events = sky_data.get("events", sky_data)[:20]

        hooks = {k: get_hook(k) for k in ["transit_and_sky", "direct", "sign_placement", "engagement", "tarot"]}

        user_prompt = WEEKLY_PROMPT.format(
            today=today_str,
            sky_events=json.dumps(sky_events, indent=2),
            sign_placement=sign_placement,
            sign=sign,
            hooks=json.dumps(hooks, indent=2)
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(system=SE_VOICE, messages=[{"role": "user", "content": user_prompt}])
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            raw = call_llm(SE_VOICE, user_prompt)

        data = parse_json(raw)

        # Generate graphic for transit spotlight
        ts = data.get("transit_spotlight", {})
        graphic_b64 = generate_graphic(
            event_name=ts.get("event_name", "Weekly Astrology"),
            pull_quote=ts.get("pull_quote", ""),
            post_date=today_str
        )

        if graphic_b64 and ctx and hasattr(ctx, "send_image"):
            try:
                img_bytes = base64.b64decode(graphic_b64)
                ctx.send_image(img_bytes, filename=f"SE_Weekly_{today.strftime('%Y%m%d')}.png")
            except Exception:
                pass

        # Format output
        wo = data.get("weekly_overview", {})
        ts_data = data.get("transit_spotlight", {})
        st = data.get("sign_tip", {})
        jp = data.get("journal_prompt", {})
        tt = data.get("tarot_tie", {})

        out = f"""SOULFUL EXISTENCE — WEEKLY BATCH
{today_str}
{"[GRAPHIC: " + ts_data.get("event_name", "") + " — " + ts_data.get("pull_quote", "") + "]" if graphic_b64 else ""}

==================================================
WEEKLY OVERVIEW — INSTAGRAM
==================================================
{wo.get("instagram", {}).get("caption", "")}

{wo.get("instagram", {}).get("hashtags", "")}

FACEBOOK:
{wo.get("facebook", {}).get("post", "")}

==================================================
TRANSIT SPOTLIGHT: {ts_data.get("subject", "")} ({ts_data.get("date", "")})
==================================================
INSTAGRAM:
{ts_data.get("instagram", {}).get("caption", "")}
{ts_data.get("instagram", {}).get("hashtags", "")}

TIKTOK:
Hook: {ts_data.get("tiktok", {}).get("hook", "")}
{ts_data.get("tiktok", {}).get("script", "")}

FACEBOOK:
{ts_data.get("facebook", {}).get("post", "")}

STORY: "{ts_data.get("story", {}).get("text", "")}"
Visual: {ts_data.get("story", {}).get("visual_note", "")}

==================================================
SIGN TIP: {sign_placement.upper()} IN {sign.upper()}
==================================================
{st.get("instagram", {}).get("caption", "")}
{st.get("instagram", {}).get("hashtags", "")}

STORY: "{st.get("story", {}).get("text", "")}"

==================================================
JOURNAL PROMPT (re: {jp.get("transit_connection", "")})
==================================================
{jp.get("instagram", {}).get("caption", "")}
{jp.get("instagram", {}).get("hashtags", "")}

STORY: "{jp.get("story", {}).get("text", "")}"

==================================================
TAROT TIE-IN
==================================================
{tt.get("instagram", {}).get("caption", "")}
{tt.get("instagram", {}).get("hashtags", "")}"""

        return out

    except Exception as e:
        return f"Something went wrong: {e}"

def register(ctx):
    ctx.register_tool(
        name="se_daily_post",
        toolset="se_astro_content",
        schema={
            "name": "se_daily_post",
            "description": "Generate today's Soulful Existence daily astrology social media post with branded graphic, social-optimized hook, IG/TikTok/FB/Story content, and tiered hashtags.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        handler=handle_daily,
        description="Generate SE daily post with graphic."
    )

    ctx.register_tool(
        name="se_weekly_batch",
        toolset="se_astro_content",
        schema={
            "name": "se_weekly_batch",
            "description": "Generate the full Soulful Existence weekly content batch with branded graphic. Weekly overview, transit spotlight, sign tip, journal prompt, tarot tie-in.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        handler=handle_weekly,
        description="Generate SE weekly batch with graphic."
    )

    if hasattr(ctx, "schedule"):
        ctx.schedule(
            name="se_daily_astro",
            cron="0 9 * * *",
            tool="se_daily_post",
            params={},
            message="[SILENT] Run se_daily_post and send the full output including any images to this chat."
        )
        ctx.schedule(
            name="se_weekly_astro",
            cron="0 10 * * 0",
            tool="se_weekly_batch",
            params={},
            message="[SILENT] Run se_weekly_batch and send the full output including any images to this chat."
        )
