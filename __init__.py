"""
Soulful Existence Astro Content Plugin v4
- Social media optimized hooks (115 hooks, 8 categories)
- Platform-specific formatting for IG, TikTok, FB, Story
- Tiered hashtag strategy (broad/mid/niche)
- AI image generation via OpenRouter (dark academia aesthetic)
- Daily 5am Eastern + Sunday weekly batch
"""

import os
import json
import random
import urllib.request
import urllib.error
import base64
from datetime import datetime, timedelta, timezone

COSMIC_API_URL = os.environ.get("KERYKEION_API_URL", "https://cosmic-api-production-d4f6.up.railway.app")
COSMIC_API_KEY = os.environ.get("COSMIC_API_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# ── Voice ─────────────────────────────────────────────────────────────────────

SE_VOICE = """You are writing social media content for Gen Rodriguez of Soulful Existence.
Gen is a tarot reader, medium, and past life regression practitioner based in the US.

WRITE EXACTLY LIKE THIS:
Gen writes like she is talking to someone she knows. Not a stranger, not a client. Someone she would actually text.

HOW SHE WRITES:
- Short sentences that land. She does not over-explain.
- She defines astrology terms once, plainly, then moves on.
- She connects astrology to what is actually happening in real life — relationships, decisions, patterns people are navigating.
- She makes it personal without oversharing. One real detail. Then moves on.
- Dry wit shows up occasionally but never tries too hard.
- She ends posts with a direct question or a short punchy line. Never a motivational sign-off.
- She trusts her audience to keep up.

SENTENCE PATTERNS:
- "Mercury is definitely retrograding." — state the fact, no fanfare
- "I love when astrology makes sense." — short landing line
- "Jupiter brings luck, growth, optimism, and achievement." — clean list, done
- "This is all right on time." — connects sky to real world simply

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

SERVICES (one CTA max, used sparingly, only when it fits):
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
        "We are in {transit} territory right now. Let me explain what that actually means.",
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
        "Three cards that keep coming up in readings this month and what they have in common.",
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
        "I will say what most astrologers will not say about {transit}.",
        "Astrology is not a personality test. Here is what it actually is.",
        "If someone told you {placement} is bad, they were wrong.",
        "The problem with how most people use tarot.",
        "Most astrology content treats you like you cannot handle complexity. I do not.",
        "The thing about {transit} that fear-based astrology content always gets wrong.",
        "I do not do doom and gloom astrology and here is why.",
        "Not all astrology advice ages well. Here is what I actually stand behind.",
        "The version of {concept} you have been taught is incomplete.",
        "Why I stopped reading astrology the way I was taught."
    ],
    "engagement": [
        "Do you relate more to your sun sign or your moon sign?",
        "What placement in your chart have you struggled to understand?",
        "Has a tarot reading ever told you something you already knew but needed to hear?",
        "What does {transit} have you thinking about right now?",
        "Which {sign} energy do you have the hardest time with?",
        "What is the one thing about your birth chart that makes complete sense to you?",
        "Has astrology ever explained something about yourself that nothing else could?",
        "What would you want to know if you could ask your chart one question?",
        "What does home mean to you right now?",
        "If your chart could tell you one thing you needed to hear today, what would it say?"
    ]
}

# ── Hashtag tiers ─────────────────────────────────────────────────────────────

HASHTAG_TIERS = {
    "broad": ["#astrology", "#tarot", "#spirituality", "#zodiac", "#intuition", "#manifestation", "#selfgrowth", "#mindfulness"],
    "mid_astro": ["#astrologytok", "#astrologer", "#birthchart", "#moonphase", "#mercuryretrograde", "#fullmoon", "#newmoon", "#venusintransit"],
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
    return broad + mid + niche

def get_hook(category=None):
    if not category:
        category = random.choice(list(HOOKS.keys()))
    hooks = HOOKS.get(category, HOOKS["transit_and_sky"])
    return random.choice(hooks)

# ── Image generation ──────────────────────────────────────────────────────────

def generate_image(subject, event_name, quote):
    """Generate a dark academia / cottage witch social media image via OpenRouter."""
    if not OPENROUTER_KEY:
        return None

    prompt = f"""Dark academia cottage witch aesthetic. Secret library in a secret garden at night.
Deep navy and forest green tones, candlelight, aged books, botanical elements, moonlight through windows.
Mysterious and atmospheric. No people. No faces.
Central theme: {subject}
Mood: {event_name}
Style: editorial, ethereal, slightly gothic, rich textures, cinematic lighting.
Text overlay space at bottom for handle @soulfulxistence.
Square format 1:1. High quality, detailed."""

    payload = json.dumps({
        "model": "openai/gpt-5.4-image-2",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image"]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_KEY}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            images = data.get("choices", [{}])[0].get("message", {}).get("images", [])
            if images:
                return images[0].get("url") or images[0].get("data")
    except Exception as e:
        return f"[Image generation failed: {e}]"
    return None

# ── API ───────────────────────────────────────────────────────────────────────

def fetch_sky_events(start_date, end_date):
    payload = json.dumps({
        "start_date": start_date,
        "end_date": end_date,
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone": 0
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{COSMIC_API_URL}/sky-events",
        data=payload,
        headers={"Content-Type": "application/json", "x-railway-secret": COSMIC_API_KEY},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

# ── Prompts ───────────────────────────────────────────────────────────────────

DAILY_PROMPT = """Today is {today}.

SKY EVENTS (next 14 days — use ONLY these, do not invent transits):
{sky_events}

HOOK TO USE (first line of every platform):
{hook}

PRIORITY: Write about the most significant event today or in the next 3 days.
If nothing major, write educational/evergreen content about astrology, tarot, or intuition.

Generate a daily post. Return ONLY valid JSON, no preamble or markdown fences:

{{
  "post_type": "major_event or upcoming_event or educational",
  "subject": "One line — what this post is about",
  "event_name": "The astrological event name for the image (e.g. Venus in Leo, New Moon in Gemini)",
  "pull_quote": "The single most shareable line from the post — max 12 words",
  "instagram": {{
    "caption": "Hook line from above + 3-4 paragraphs in Gen voice. Hook must be the exact first line. Paragraphs separated by blank lines. No hashtags in caption.",
    "hashtags": "String of 9 hashtags — 3 broad reach, 3 mid-range, 3 niche SE tags. Format: #tag1 #tag2 etc"
  }},
  "tiktok": {{
    "hook": "The exact hook line adapted for spoken word — under 8 words, punchy",
    "script": "45-60 second spoken script. Written how Gen actually talks. Natural pauses with ellipses. Ends with a bold statement or question, never a CTA."
  }},
  "facebook": {{
    "post": "Hook line + longer conversational version. More personal. Ends with a question that invites real responses, not just likes."
  }},
  "story": {{
    "text": "Pull quote or bold statement — max 10 words for graphic overlay",
    "visual_note": "One line describing the image mood for this specific post"
  }},
  "image_prompt_addition": "2-3 specific visual elements to add to the standard dark academia prompt for this post's theme"
}}"""

WEEKLY_PROMPT = """Today is {today} (Sunday). Weekly content batch.

SKY EVENTS (next 14 days — use ONLY these, do not invent transits):
{sky_events}

SIGN TIP THIS WEEK: {sign_placement} in {sign}
HOOKS THIS WEEK: {hooks}

Generate the full weekly batch. Return ONLY valid JSON, no preamble or markdown fences:

{{
  "weekly_overview": {{
    "subject": "What this week is about in one line",
    "event_name": "Main event for image",
    "instagram": {{
      "caption": "Hook + 3-4 paragraphs. What is the collective weather this week. Names key events, what they mean, what people might feel. Gen voice.",
      "hashtags": "9 hashtags — 3 broad, 3 mid, 3 niche"
    }},
    "facebook": {{
      "post": "Longer personal version. Ends with engagement question."
    }}
  }},
  "transit_spotlight": {{
    "subject": "Most significant transit this week",
    "date": "When it happens",
    "event_name": "Transit name for image",
    "pull_quote": "Most shareable line — max 12 words",
    "instagram": {{
      "caption": "Hook + 3-4 paragraphs. Deep dive. Plain explanation, real life meaning, speaks directly to reader.",
      "hashtags": "9 hashtags — 3 broad, 3 mid, 3 niche"
    }},
    "tiktok": {{
      "hook": "Spoken hook under 8 words",
      "script": "45-60 second spoken script in Gen voice"
    }},
    "facebook": {{
      "post": "Conversational version with engagement question"
    }},
    "story": {{
      "text": "One line max 10 words",
      "visual_note": "Image mood for this post"
    }}
  }},
  "sign_tip": {{
    "placement": "{sign_placement}",
    "sign": "{sign}",
    "instagram": {{
      "caption": "Hook + 3 paragraphs about this placement. Practical and specific. Connects to current sky.",
      "hashtags": "9 hashtags"
    }},
    "story": {{
      "text": "One punchy line for this placement, max 10 words"
    }}
  }},
  "journal_prompt": {{
    "transit_connection": "Which event this connects to",
    "instagram": {{
      "caption": "Hook + 3 paragraphs. Real reflective question tied to the sky. Not therapy-speak.",
      "hashtags": "9 hashtags"
    }},
    "story": {{
      "text": "The question distilled to one line"
    }}
  }},
  "tarot_tie": {{
    "instagram": {{
      "caption": "Hook + 3 paragraphs connecting sky to tarot. Which card fits. What it is asking right now.",
      "hashtags": "9 hashtags"
    }}
  }}
}}"""

SIGN_PLACEMENTS = ["sun", "moon", "rising", "venus"]
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def call_llm(system, user_prompt):
    if not OPENROUTER_KEY:
        return None
    payload = json.dumps({
        "model": "anthropic/claude-sonnet-4-6",
        "max_tokens": 4000,
        "messages": [{"role": "user", "content": user_prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_KEY}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

def parse_json(raw):
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(clean)

def format_daily(data, today_str):
    ig = data.get("instagram", {})
    tk = data.get("tiktok", {})
    fb = data.get("facebook", {})
    st = data.get("story", {})
    image_url = data.get("image_url", "")

    out = f"""SOULFUL EXISTENCE — DAILY POST
{today_str}
Subject: {data.get("subject", "")}

{"IMAGE: " + image_url if image_url else ""}

==================================================
INSTAGRAM
==================================================
{ig.get("caption", "")}

{ig.get("hashtags", "")}

==================================================
TIKTOK
==================================================
Hook: {tk.get("hook", "")}

Script:
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
    return out

def format_weekly(data, today_str, sign_placement, sign):
    sections = []
    sections.append(f"SOULFUL EXISTENCE — WEEKLY BATCH\n{today_str}\n")

    wo = data.get("weekly_overview", {})
    wo_ig = wo.get("instagram", {})
    sections.append(f"==================================================\nWEEKLY OVERVIEW\n==================================================\n{wo_ig.get('caption', '')}\n\n{wo_ig.get('hashtags', '')}\n\nFACEBOOK:\n{wo.get('facebook', {}).get('post', '')}")

    ts = data.get("transit_spotlight", {})
    ts_ig = ts.get("instagram", {})
    ts_tk = ts.get("tiktok", {})
    ts_fb = ts.get("facebook", {})
    ts_st = ts.get("story", {})
    image_url = ts.get("image_url", "")
    sections.append(f"==================================================\nTRANSIT SPOTLIGHT: {ts.get('subject', '')} ({ts.get('date', '')})\n==================================================\n{'IMAGE: ' + image_url if image_url else ''}\n\nINSTAGRAM:\n{ts_ig.get('caption', '')}\n{ts_ig.get('hashtags', '')}\n\nTIKTOK:\nHook: {ts_tk.get('hook', '')}\nScript: {ts_tk.get('script', '')}\n\nFACEBOOK:\n{ts_fb.get('post', '')}\n\nSTORY: \"{ts_st.get('text', '')}\"\nVisual: {ts_st.get('visual_note', '')}")

    st = data.get("sign_tip", {})
    st_ig = st.get("instagram", {})
    sections.append(f"==================================================\nSIGN TIP: {sign_placement.upper()} IN {sign.upper()}\n==================================================\n{st_ig.get('caption', '')}\n{st_ig.get('hashtags', '')}\n\nSTORY: \"{st.get('story', {}).get('text', '')}\"")

    jp = data.get("journal_prompt", {})
    jp_ig = jp.get("instagram", {})
    sections.append(f"==================================================\nJOURNAL PROMPT (re: {jp.get('transit_connection', '')})\n==================================================\n{jp_ig.get('caption', '')}\n{jp_ig.get('hashtags', '')}\n\nSTORY: \"{jp.get('story', {}).get('text', '')}\"")

    tt = data.get("tarot_tie", {})
    tt_ig = tt.get("instagram", {})
    sections.append(f"==================================================\nTAROT TIE-IN\n==================================================\n{tt_ig.get('caption', '')}\n{tt_ig.get('hashtags', '')}")

    return "\n\n".join(sections)

def handle_daily(params, ctx=None, **kwargs):
    try:
        today = datetime.now(timezone.utc)
        start_date = today.strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
        today_str = today.strftime("%B %d, %Y")

        sky_data = fetch_sky_events(start_date, end_date)
        sky_events = sky_data.get("events", sky_data)

        hook_category = random.choice(["transit_and_sky", "personal", "direct", "educational"])
        hook = get_hook(hook_category)

        user_prompt = DAILY_PROMPT.format(
            today=today_str,
            sky_events=json.dumps(sky_events[:20], indent=2),
            hook=hook
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(system=SE_VOICE, messages=[{"role": "user", "content": user_prompt}])
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            raw = call_llm(SE_VOICE, user_prompt)
            if not raw:
                return "LLM unavailable."

        data = parse_json(raw)

        image_url = generate_image(
            data.get("subject", "astrological energy"),
            data.get("event_name", "astrology"),
            data.get("pull_quote", "")
        )
        if image_url:
            data["image_url"] = image_url

        return format_daily(data, today_str)

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
        sky_events = sky_data.get("events", sky_data)

        hooks = {
            "weekly_overview": get_hook("transit_and_sky"),
            "transit_spotlight": get_hook("direct"),
            "sign_tip": get_hook("sign_placement"),
            "journal_prompt": get_hook("engagement"),
            "tarot_tie": get_hook("tarot")
        }

        user_prompt = WEEKLY_PROMPT.format(
            today=today_str,
            sky_events=json.dumps(sky_events[:20], indent=2),
            sign_placement=sign_placement,
            sign=sign,
            hooks=json.dumps(hooks, indent=2)
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(system=SE_VOICE, messages=[{"role": "user", "content": user_prompt}])
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            raw = call_llm(SE_VOICE, user_prompt)
            if not raw:
                return "LLM unavailable."

        data = parse_json(raw)

        ts = data.get("transit_spotlight", {})
        image_url = generate_image(
            ts.get("subject", "weekly astrology"),
            ts.get("event_name", "astrology"),
            ts.get("pull_quote", "")
        )
        if image_url:
            data["transit_spotlight"]["image_url"] = image_url

        return format_weekly(data, today_str, sign_placement, sign)

    except Exception as e:
        return f"Something went wrong: {e}"

def register(ctx):
    ctx.register_tool(
        name="se_daily_post",
        toolset="se_astro_content",
        schema={
            "name": "se_daily_post",
            "description": "Generate today's Soulful Existence daily astrology social media post with social-optimized hook, platform-specific content for IG/TikTok/FB/Story, tiered hashtags, and a dark academia AI image.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        handler=handle_daily,
        description="Generate SE daily post."
    )

    ctx.register_tool(
        name="se_weekly_batch",
        toolset="se_astro_content",
        schema={
            "name": "se_weekly_batch",
            "description": "Generate the full Soulful Existence weekly content batch for Sunday scheduling. Weekly overview, transit spotlight, sign tip, journal prompt, tarot tie-in — all platforms, all optimized.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        handler=handle_weekly,
        description="Generate SE weekly batch."
    )

    if hasattr(ctx, "schedule"):
        ctx.schedule(
            name="se_daily_astro",
            cron="0 9 * * *",
            tool="se_daily_post",
            params={},
            message="[SILENT] Run se_daily_post and send the full output to this chat."
        )
        ctx.schedule(
            name="se_weekly_astro",
            cron="0 10 * * 0",
            tool="se_weekly_batch",
            params={},
            message="[SILENT] Run se_weekly_batch and send the full output to this chat."
        )
