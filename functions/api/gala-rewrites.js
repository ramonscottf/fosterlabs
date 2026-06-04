// GET /api/gala-rewrites  -> { "<id>": { desc_html, desc }, ... }
// Returns all AI-generated rewrites that have been saved to KV.

export async function onRequestGet(context) {
  const { env } = context;
  const headers = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' };
  try {
    const raw = env.FOSTER_FINANCE ? await env.FOSTER_FINANCE.get('gala_rewrites_v1') : null;
    return new Response(raw || '{}', { headers });
  } catch (e) {
    return new Response('{}', { headers });
  }
}
