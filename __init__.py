"""
Soulful Existence Astro Content Plugin v3 for Hermes Agent
Daily post at 5am Eastern + weekly batch on Sundays
"""

import os
import json
import random
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

COSMIC_API_URL = os.environ.get(
    "KERYKEION_API_URL",
    "https://cosmic-api-production-d4f6.up.railway.app"
)
COSMIC_API_KEY = os.environ.get("COSMIC_API_KEY", "")

# ── Voice prompt ─────────────────────────────────────────────────────────────

SE_VOICE = """You are writing social media content for Gen Rodriguez of Soulful Existence.
Gen is a tarot reader, medium, and past life regression practitioner.

WRITE EXACTLY LIKE THIS:

Gen writes like she is talking to someone she knows. Not a stranger, not a client, not a follower. Someone she would actually text.

HOW SHE WRITES:
- Short sentences that land. She does not over-explain.
- She defines astrology terms once, plainly, then moves on. No repeating, no hand-holding.
- She connects astrology to what is actually happening in the world, in relationships, in the body, in real decisions people are making.
- She makes it personal without oversharing. One real detail that grounds it. Then she moves on.
- Her dry wit shows up occasionally but never tries too hard.
- She ends posts with either a direct question or a short punchy line that lands the whole thing. Never a motivational sign-off.
- She trusts her audience to keep up.

SENTENCE PATTERNS TO USE:
- "Mercury is definitely retrograding." — state the fact, no fanfare
- "There is a reason they are not in my life anymore." — real, dry, moves on
- "I love when astrology makes sense." — short landing line
- "Jupiter brings luck, growth, optimism, and achievement." — clean list, no elaboration needed
- "This is all right on time." — connects sky to world without over-explaining

WHAT SHE DOES NOT DO:
- Does not say "the cosmos are inviting you to..."
- Does not use "energy" as a filler word every other sentence
- Does not write in a whisper or be mysterious about it
- Does not over-qualify — not "this might possibly feel like..." — just say what it is
- Does not hype — no exclamation points unless something is actually surprising
- Does not write fake urgency — no "now is the time to..."
- Does not add a motivational quote at the end
- Does not use dashes as bullet points
- Does not use the word "energy" more than once per post

TONE REFERENCE — actual Gen posts, write like this:

"Mercury is definitely retrograding. I have had a few old so-called friends follow me on here and TikTok in the last week or so. There is a reason they are not in my life anymore, but apparently they are curious. Mercury is in retrograde until August 23rd. It is known for bringing misunderstandings, miscommunication, technology problems, and people from your past. We are meant to reflect, review, choose new paths when it comes to old lessons, and pause before major decisions."

"Both of my bio granddaughters will have significant Leo placements in their birth charts. My North Node is Leo. The North Node is a placement that is known for being what we are working towards in this lifetime. I have a feeling my granddaughters are here to teach me. Probably how to be comfortable in the spotlight or in a leadership position. I love when astrology makes sense."

"In astrology a Conjunction is when there are 0 degrees of separation between two planets. The energy of a conjunction is harmonic, blending the energy of both planets together. Working together and pulling the best of both planets is like rocket fuel for any projects, plans, growth, and achievements you have been working on."

PARAGRAPH STRUCTURE FOR EVERY POST:
Para 1 — What is happening. State it plainly. Define any term that needs defining. One or two sentences max per idea.
Para 2 — Why it matters. What does this actually do or stir up. Connect it to something real — a feeling, a pattern, something people are navigating right now.
Para 3 — Make it personal. One real detail or observation that grounds it. Speak directly to the reader.
Para 4 — Optional. A question or a short landing line. Only if it adds something.

SERVICES (mention sparingly, one CTA max, only when it fits naturally):
Tarot readings, Mediumship sessions, Past Life Regression, Digital products at soulfulexistence.com"""

# ── Daily post prompt ────────────────────────────────────────────────────────

DAILY_POST_PROMPT = """Today is {today}.

Here are the astrological sky events for the next 14 days:
{sky_events}

PRIORITY ORDER for choosing what to write about:
1. If there is a major event TODAY or TOMORROW (ingress of a personal planet, lunation, exact aspect between outer planets, retrograde station, cazimi, eclipse) — write about that.
2. If there is a major event in the next 3-5 days — write about it as upcoming, give people time to prepare.
3. If nothing major — write useful, grounded, educational astrology content. Ideas: how to read your chart, what a specific placement means, how retrogrades actually work, what the nodes represent, how to use astrology practically day to day.

CRITICAL: Use ONLY events that appear in the sky events data above. Do not invent transits.

Generate a daily post in this JSON format. Return ONLY valid JSON, no preamble or markdown:

{{
  "post_type": "major_event or upcoming_event or educational",
  "subject": "One line describing what the post is about",
  "instagram": {{
    "caption": "Full Instagram caption. 3-4 paragraphs in Gen voice. No hashtags in the caption itself.",
    "hashtags": ["8-10 relevant hashtags"]
  }},
  "tiktok": {{
    "hook": "One punchy opening line. Under 10 words. Makes people stop scrolling.",
    "script": "45-60 second spoken script. Written how Gen actually talks. Natural pauses with ellipses. No stage directions."
  }},
  "facebook": {{
    "post": "Slightly longer version of the Instagram caption. More conversational. Ends with a question that invites real responses."
  }},
  "story": {{
    "text": "One line. Max 10 words. For graphic overlay.",
    "visual_note": "Brief note on what kind of visual would work"
  }}
}}"""

# ── Weekly batch prompt ──────────────────────────────────────────────────────

WEEKLY_BATCH_PROMPT = """Today is {today} (Sunday). This is the weekly content batch.

Here are the astrological sky events for the next 14 days:
{sky_events}

SIGN TIP THIS WEEK: {sign_placement} in {sign}

CRITICAL: Use ONLY events that appear in the sky events data above. Do not invent transits.

Generate a full weekly content batch. Return ONLY valid JSON, no preamble or markdown:

{{
  "weekly_overview": {{
    "instagram": {{
      "caption": "Monday overview post. 3-4 paragraphs. What is the collective weather this week. Name the key events, what they mean, what people might feel or notice. Gen voice throughout.",
      "hashtags": ["8-10 hashtags"]
    }},
    "facebook": {{
      "post": "Longer version. More personal. Ends with engagement question."
    }}
  }},
  "transit_spotlight": {{
    "subject": "The single most significant transit this week",
    "date": "When it happens",
    "instagram": {{
      "caption": "Deep dive on this one transit. 3-4 paragraphs. Plain explanation, why it matters, personal connection, landing line or question.",
      "hashtags": ["8-10 hashtags"]
    }},
    "tiktok": {{
      "hook": "One punchy opening line under 10 words",
      "script": "45-60 second spoken script in Gen voice"
    }},
    "facebook": {{
      "post": "Conversational version with engagement question"
    }},
    "story": {{
      "text": "One line max 10 words",
      "visual_note": "Visual direction"
    }}
  }},
  "sign_tip": {{
    "placement": "{sign_placement}",
    "sign": "{sign}",
    "instagram": {{
      "caption": "3 paragraphs about this placement. Practical and specific. Connects to current sky. Speaks directly to people with this placement.",
      "hashtags": ["6-8 hashtags"]
    }},
    "story": {{
      "text": "One punchy line for this placement, max 10 words"
    }}
  }},
  "journal_prompt": {{
    "transit_connection": "Which event this connects to",
    "instagram": {{
      "caption": "3 paragraphs. A real reflective question tied to the sky. Context, the question itself, why it matters right now. Not therapy-speak.",
      "hashtags": ["6-8 hashtags"]
    }},
    "story": {{
      "text": "The question distilled to one line"
    }}
  }},
  "tarot_tie": {{
    "instagram": {{
      "caption": "3 paragraphs connecting current sky to tarot. Which card fits and why. What it is asking right now. Natural connection to a reading without being salesy.",
      "hashtags": ["6-8 hashtags"]
    }}
  }}
}}"""

# ── Sign rotation ────────────────────────────────────────────────────────────

SIGN_PLACEMENTS = ["sun", "moon", "rising", "venus"]
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# ── API ──────────────────────────────────────────────────────────────────────

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
        headers={
            "Content-Type": "application/json",
            "x-railway-secret": COSMIC_API_KEY
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

# ── Formatters ───────────────────────────────────────────────────────────────

def hashtag_str(tags):
    if not tags:
        return ""
    return " ".join([f"#{t.lstrip('#').replace(' ', '')}" for t in tags if t])

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

    return f"""SOULFUL EXISTENCE — DAILY POST
{today_str} | {data.get("subject", "")}

==================================================
INSTAGRAM
==================================================
{ig.get("caption", "")}

{hashtag_str(ig.get("hashtags", []))}

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

def format_weekly(data, today_str, sign_placement, sign):
    wo = data.get("weekly_overview", {})
    ts = data.get("transit_spotlight", {})
    st = data.get("sign_tip", {})
    jp = data.get("journal_prompt", {})
    tt = data.get("tarot_tie", {})

    wo_ig = wo.get("instagram", {})
    wo_fb = wo.get("facebook", {})
    ts_ig = ts.get("instagram", {})
    ts_tk = ts.get("tiktok", {})
    ts_fb = ts.get("facebook", {})
    ts_st = ts.get("story", {})
    st_ig = st.get("instagram", {})
    st_st = st.get("story", {})
    jp_ig = jp.get("instagram", {})
    jp_st = jp.get("story", {})
    tt_ig = tt.get("instagram", {})

    return f"""SOULFUL EXISTENCE — WEEKLY BATCH
Generated: {today_str}

==================================================
WEEKLY OVERVIEW — INSTAGRAM
==================================================
{wo_ig.get("caption", "")}

{hashtag_str(wo_ig.get("hashtags", []))}

WEEKLY OVERVIEW — FACEBOOK
{wo_fb.get("post", "")}

==================================================
TRANSIT SPOTLIGHT: {ts.get("subject", "")} ({ts.get("date", "")})
==================================================
INSTAGRAM:
{ts_ig.get("caption", "")}
{hashtag_str(ts_ig.get("hashtags", []))}

TIKTOK:
Hook: {ts_tk.get("hook", "")}
Script: {ts_tk.get("script", "")}

FACEBOOK:
{ts_fb.get("post", "")}

STORY: "{ts_st.get("text", "")}"
Visual: {ts_st.get("visual_note", "")}

==================================================
SIGN TIP: {sign_placement.upper()} IN {sign.upper()}
==================================================
INSTAGRAM:
{st_ig.get("caption", "")}
{hashtag_str(st_ig.get("hashtags", []))}

STORY: "{st_st.get("text", "")}"

==================================================
JOURNAL PROMPT (re: {jp.get("transit_connection", "")})
==================================================
INSTAGRAM:
{jp_ig.get("caption", "")}
{hashtag_str(jp_ig.get("hashtags", []))}

STORY: "{jp_st.get("text", "")}"

==================================================
TAROT TIE-IN
==================================================
{tt_ig.get("caption", "")}
{hashtag_str(tt_ig.get("hashtags", []))}"""

# ── Handlers ─────────────────────────────────────────────────────────────────

def handle_daily(params, ctx=None, **kwargs):
    try:
        today = datetime.now(timezone.utc)
        start_date = today.strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
        today_str = today.strftime("%B %d, %Y")

        sky_events = fetch_sky_events(start_date, end_date)

        user_prompt = DAILY_POST_PROMPT.format(
            today=today_str,
            sky_events=json.dumps(sky_events.get("events", sky_events), indent=2)
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(
                system=SE_VOICE,
                messages=[{"role": "user", "content": user_prompt}]
            )
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            return "LLM context unavailable."

        data = parse_json(raw)
        return format_daily(data, today_str)

    except urllib.error.URLError as e:
        return f"Could not reach the Cosmic API: {e}"
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

        sky_events = fetch_sky_events(start_date, end_date)

        user_prompt = WEEKLY_BATCH_PROMPT.format(
            today=today_str,
            sky_events=json.dumps(sky_events.get("events", sky_events), indent=2),
            sign_placement=sign_placement,
            sign=sign
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(
                system=SE_VOICE,
                messages=[{"role": "user", "content": user_prompt}]
            )
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            return "LLM context unavailable."

        data = parse_json(raw)
        return format_weekly(data, today_str, sign_placement, sign)

    except urllib.error.URLError as e:
        return f"Could not reach the Cosmic API: {e}"
    except Exception as e:
        return f"Something went wrong: {e}"


# ── Registration ─────────────────────────────────────────────────────────────

def register(ctx):
    # Daily post tool
    ctx.register_tool(
        name="se_daily_post",
        toolset="se_astro_content",
        schema={
            "name": "se_daily_post",
            "description": "Generate today's Soulful Existence daily astrology post. Checks sky events and writes about the most relevant event — major transit, upcoming event, or educational content. Returns Instagram, TikTok, Facebook, and Story formats.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        handler=handle_daily,
        description="Generate SE daily astrology post."
    )

    # Weekly batch tool
    ctx.register_tool(
        name="se_weekly_batch",
        toolset="se_astro_content",
        schema={
            "name": "se_weekly_batch",
            "description": "Generate the full Soulful Existence weekly content batch for Sunday scheduling. Returns weekly overview, transit spotlight, sign tip, journal prompt, and tarot tie-in across all platforms.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        },
        handler=handle_weekly,
        description="Generate SE weekly content batch."
    )

    # Schedule daily post at 5am Eastern (9am UTC, 10am UTC during EDT)
    if hasattr(ctx, "schedule"):
        ctx.schedule(
            name="se_daily_astro",
            cron="0 9 * * *",
            tool="se_daily_post",
            params={},
            message="[SILENT] Run se_daily_post and send the full output to this chat."
        )

        # Weekly batch every Sunday at 6am Eastern (10am UTC)
        ctx.schedule(
            name="se_weekly_astro",
            cron="0 10 * * 0",
            tool="se_weekly_batch",
            params={},
            message="[SILENT] Run se_weekly_batch and send the full output to this chat."
        )
