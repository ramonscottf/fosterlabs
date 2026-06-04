// POST /api/gala-rewrite
// Body: { title, desc, value, tags, model? }
// Returns: { desc_html }
// Calls Claude (Opus) using the existing fosterlabs ANTHROPIC_API_KEY (same one recommendations.js uses).

const DEFAULT_MODEL = 'claude-opus-4-8';

const SYSTEM_PROMPT = `You write punchy silent-auction item descriptions for the Davis Education Foundation Gala 2026 — a charity gala that funds school programs for kids. You are rewriting an existing description into a sharper, more enticing version that makes someone want to bid.

VOICE
- Warm, vivid, a little witty. Clean humor is welcome — never corny, never mean, nothing off-color or edgy (this is a school-kids charity).
- Sell the EXPERIENCE and the feeling, not just the spec sheet. Lead with why someone wants it.
- No marketing clichés ("don't miss out", "act now", "treat yourself today"). No emojis. No exclamation-point spam.

HARD RULE — NO INVENTION
- Use ONLY facts present in the provided item (title, description, value, tags). Do NOT invent brands, sizes, quantities, dates, locations, or features. If the source is thin, keep the output short. Never guess specs.
- Preserve any real caveats or conditions (dates, "carts sold separately", "not included", expirations) as plain factual text, not hype.

FORMAT — return HTML using ONLY these tags: <p>, <strong>, <em>, <ul>, <li>
1. A bold one-line hook: <p><strong>…</strong></p>
2. One short prose paragraph, 1–3 sentences: <p>…</p>
3. If the item is a bundle or has several distinct features, add a bullet list: <ul><li><strong>Label</strong> — detail</li>…</ul>. Lead each bullet with a bold label. Skip the list entirely for simple single items.
4. A short italic closing line: <p><em>…</em></p>
Keep it tight — usually under ~140 words.

OUTPUT
Return VALID JSON ONLY — no markdown fences, no preamble, no commentary:
{"desc_html": "<the rewritten description as HTML>"}`;

export async function onRequestPost(context) {
  const { request, env } = context;
  const headers = { 'Content-Type': 'application/json' };

  let b;
  try { b = await request.json(); }
  catch { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers }); }

  const title = (b.title || '').toString().slice(0, 300);
  const desc = (b.desc || '').toString().slice(0, 6000);
  const value = (b.value || '').toString().slice(0, 40);
  const tags = Array.isArray(b.tags) ? b.tags.join(', ') : (b.tags || '').toString();
  const model = (b.model || DEFAULT_MODEL).toString();

  if (!title && !desc) {
    return new Response(JSON.stringify({ error: 'title or desc required' }), { status: 400, headers });
  }
  if (!env.ANTHROPIC_API_KEY) {
    return new Response(JSON.stringify({ error: 'no ANTHROPIC_API_KEY on this project' }), { status: 500, headers });
  }

  const userMsg = `Item title: ${title}
Value: ${value || '(n/a)'}
Tags: ${tags || '(none)'}

Current description (rewrite this):
"""
${desc || '(none provided — write from the title only, keep it short, invent nothing)'}
"""

Rewrite it per the rules. Return JSON only.`;

  let resp;
  try {
    resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model,
        max_tokens: 1200,
        system: SYSTEM_PROMPT,
        messages: [{ role: 'user', content: userMsg }],
      }),
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'request to Anthropic failed' }), { status: 502, headers });
  }

  if (!resp.ok) {
    const t = await resp.text().catch(() => '');
    return new Response(JSON.stringify({ error: `ai ${resp.status}`, detail: t.slice(0, 300) }), { status: 502, headers });
  }

  const data = await resp.json();
  let txt = (data.content || []).filter(x => x.type === 'text').map(x => x.text).join('').trim();
  txt = txt.replace(/^```(?:json)?/i, '').replace(/```$/, '').trim();

  let out;
  try { out = JSON.parse(txt); }
  catch { out = { desc_html: txt }; } // model returned raw HTML — accept it

  if (!out.desc_html) {
    return new Response(JSON.stringify({ error: 'no content returned' }), { status: 502, headers });
  }
  return new Response(JSON.stringify({ desc_html: out.desc_html, model }), { headers });
}
