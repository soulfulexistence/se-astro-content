"""
Soulful Existence Astro Content Plugin v2 for Hermes Agent
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

SE_BRAND_PROMPT = """You are a content writer for Soulful Existence, the personal brand of Gen Rodriguez — a tarot reader, medium, and past life regression practitioner offering virtual sessions worldwide.

BRAND OVERVIEW
Soulful Existence helps people reconnect with their own intuition during moments of change and transition. Services: tarot readings, mediumship sessions, past life regression (guided hypnosis). Ancient, grounded wisdom — like knowledge passed down through generations.

VOICE AND TONE
- Warm, grounded, conversational — like a wise friend who knows your soul
- Spiritually fluent without being preachy or performatively woo
- Honest about difficult transits — no toxic positivity
- Trusts the audience's intelligence
- No dependency language — empowers, does not create reliance
- Never use: the universe whispers, high vibe, manifest your dreams, cosmic downloads
- Understated, confident, real — talks TO people not AT them

THREE AUDIENCE LAYERS (weave all three into every piece of content):
1. NEWCOMERS — explain what the transit/placement is in plain language, no jargon without definition
2. INTERMEDIATE — practical how-to-use-this-energy guidance, what actions or inner work fit this moment
3. PERSONAL — speak directly to the reader using you and your, make them feel seen

ASTROLOGY AS DOORWAY
Use sky events as context and doorway into inner work — not as the main offering.
Connect transits to themes of intuition, transition, and self-knowledge.
Mercury retrograde is not survive this rx — it is here is what this stirs up and here is how going inward helps.

SERVICES (one CTA max per post, used sparingly):
Tarot readings, Mediumship, Past Life Regression, Digital products

NEVER:
- Fear-based transit content
- Overpromising
- Generic astrology with no SE fingerprint
- Excessive emojis or hashtag walls
- Sun-sign-only surface content"""

SIGN_PLACEMENTS = ["sun", "moon", "rising", "venus"]
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

CONTENT_PROMPT = """Based on the following upcoming astrological sky events for the next 14 days, create a full Soulful Existence content batch.

UPCOMING SKY EVENTS:
{sky_events}

TODAY: {today}
DATE RANGE: {start_date} to {end_date}
SIGN TIP FOCUS: {sign_placement} in {sign}

Return ONLY valid JSON with no preamble or markdown fences:

{{
  "weekly_energy": {{
    "instagram_caption": "Monday energy overview. Hook + collective theme for the week + practical meaning + engagement question. All 3 audience layers.",
    "hashtags": ["8-10 relevant hashtags no spaces"]
  }},
  "transit_spotlight": {{
    "planet": "Most significant upcoming transit planet",
    "aspect_or_event": "What it is doing",
    "date": "When it perfects",
    "instagram_caption": "Deep dive on this transit. Plain explanation (newcomers) + how to work with it (intermediate) + speaks directly to reader (personal). SE voice.",
    "tiktok_hook": "3-second punchy opening line",
    "tiktok_script": "45-60 second spoken script, conversational, pauses noted with ellipses",
    "facebook_post": "Longer conversational version with engagement question at end",
    "story_prompt": "One punchy line for graphic overlay max 12 words",
    "story_visual_direction": "Brief note on visual direction for the graphic",
    "hashtags": ["8-10 relevant hashtags"]
  }},
  "sign_tip": {{
    "placement": "{sign_placement}",
    "sign": "{sign}",
    "instagram_caption": "Tip for people with this placement. Practical, warm, specific. Connects to current sky energy. Speaks directly to them.",
    "story_prompt": "One punchy line for this placement max 10 words",
    "hashtags": ["6-8 relevant hashtags"]
  }},
  "journal_prompt": {{
    "transit_tie": "Which transit this connects to",
    "instagram_caption": "Reflective journal prompt tied to current sky energy. One powerful question + brief context + invitation. Real, not therapy-speak.",
    "story_prompt": "Journal question distilled to one line for story graphic",
    "hashtags": ["6-8 relevant hashtags"]
  }},
  "tarot_transit_tie": {{
    "instagram_caption": "Post connecting current sky energy to tarot. Which cards resonate and why. Practical — what the card is asking you to consider right now. Natural bridge to booking.",
    "hashtags": ["6-8 relevant hashtags"]
  }},
  "retrograde_or_ingress_alert": {{
    "applicable": true,
    "planet": "Planet involved or null if none",
    "type": "retrograde or ingress or major_aspect or null",
    "instagram_caption": "Practical navigation guide for this event if applicable, otherwise null",
    "hashtags": ["6-8 relevant hashtags or empty list if not applicable"]
  }}
}}"""


def fetch_sky_events(start_date, end_date):
    payload = json.dumps({
        "start_date": start_date,
        "end_date": end_date,
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone": 0
    }).encode("utf-8")
    api_key = os.environ.get("COSMIC_API_KEY", "")
    req = urllib.request.Request(
    f"{COSMIC_API_URL}/sky-events",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "x-railway-secret": api_key

    },
    method="POST"
)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def hashtag_str(tags):
    if not tags:
        return ""
    return " ".join([f"#{t.lstrip('#').replace(' ','')}" for t in tags if t])


def format_output(raw_json, sign_placement, sign, today_str, start_date, end_date):
    try:
        clean = raw_json.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        d = json.loads(clean)

        we = d.get("weekly_energy", {})
        ts = d.get("transit_spotlight", {})
        st = d.get("sign_tip", {})
        jp = d.get("journal_prompt", {})
        tt = d.get("tarot_transit_tie", {})
        ra = d.get("retrograde_or_ingress_alert", {})

        out = f"""SOULFUL EXISTENCE ASTRO CONTENT BATCH v2
Generated: {today_str} | Covers: {start_date} to {end_date}

==================================================
WEEKLY ENERGY — INSTAGRAM
==================================================
{we.get("instagram_caption", "")}

{hashtag_str(we.get("hashtags", []))}

==================================================
TRANSIT SPOTLIGHT: {ts.get("planet", "")} — {ts.get("aspect_or_event", "")} ({ts.get("date", "")})
==================================================

INSTAGRAM:
{ts.get("instagram_caption", "")}
{hashtag_str(ts.get("hashtags", []))}

TIKTOK HOOK: {ts.get("tiktok_hook", "")}

TIKTOK SCRIPT:
{ts.get("tiktok_script", "")}

FACEBOOK:
{ts.get("facebook_post", "")}

STORY: "{ts.get("story_prompt", "")}"
VISUAL DIRECTION: {ts.get("story_visual_direction", "")}

==================================================
SIGN TIP: {sign_placement.upper()} IN {sign.upper()}
==================================================
INSTAGRAM:
{st.get("instagram_caption", "")}
{hashtag_str(st.get("hashtags", []))}

STORY: "{st.get("story_prompt", "")}"

==================================================
JOURNAL PROMPT (transit: {jp.get("transit_tie", "")})
==================================================
INSTAGRAM:
{jp.get("instagram_caption", "")}
{hashtag_str(jp.get("hashtags", []))}

STORY: "{jp.get("story_prompt", "")}"

==================================================
TAROT + TRANSIT TIE-IN
==================================================
{tt.get("instagram_caption", "")}
{hashtag_str(tt.get("hashtags", []))}"""

        if ra.get("applicable") and ra.get("instagram_caption"):
            out += f"""

==================================================
{ra.get("type", "ALERT").upper().replace("_", " ")}: {ra.get("planet", "")}
==================================================
{ra.get("instagram_caption", "")}
{hashtag_str(ra.get("hashtags", []))}"""

        return out

    except Exception as e:
        return f"Formatting failed: {e}\n\nRaw output:\n{raw_json}"


def handle(params, ctx=None, **kwargs):
    try:
        today = datetime.now(timezone.utc)
        start_date = today.strftime("%Y-%m-%d")
        end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
        today_str = today.strftime("%B %d, %Y")

        sign_placement = random.choice(SIGN_PLACEMENTS)
        sign = random.choice(SIGNS)

        sky_events = fetch_sky_events(start_date, end_date)

        user_prompt = CONTENT_PROMPT.format(
            sky_events=json.dumps(sky_events, indent=2),
            today=today_str,
            start_date=start_date,
            end_date=end_date,
            sign_placement=sign_placement,
            sign=sign
        )

        if ctx and hasattr(ctx, "llm"):
            result = ctx.llm.complete(
                system=SE_BRAND_PROMPT,
                messages=[{"role": "user", "content": user_prompt}]
            )
            raw = result.content if hasattr(result, "content") else str(result)
        else:
            return "Plugin loaded but LLM context not available."

        return format_output(raw, sign_placement, sign, today_str, start_date, end_date)

    except urllib.error.URLError as e:
        return f"Could not reach the Cosmic API: {e}"
    except Exception as e:
        return f"Something went wrong: {e}"


def register(ctx):
    schema = {
        "name": "astro_content_se",
        "description": (
            "Generate a full Soulful Existence social media content batch based on "
            "upcoming astrological sky events over the next 14 days. Produces: "
            "weekly energy overview, transit spotlight with Instagram/TikTok/Facebook/Story formats, "
            "randomly rotated sign placement tip (sun/moon/rising/venus), "
            "journal prompt, tarot-transit tie-in, and retrograde or ingress alert if applicable. "
            "All content is warm, grounded, informative for newcomers, practical for intermediate, "
            "and personal for all readers."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
    ctx.register_tool(
        name="astro_content_se",
        toolset="astro_content_se",
        schema=schema,
        handler=handle,
        description="Generate full SE astro content batch for the next 14 days."
    )
