// /api/gala-images
//   GET                       -> { "<itemId>": [ {url,label,ts}, ... ], ... }
//   POST { id, label, url }   -> records a generated image under that item (so it reloads in the tool)
// Stored in KV FOSTER_FINANCE under key gala_images_v1.

export async function onRequestGet(context) {
  const { env } = context;
  const headers = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' };
  try {
    const raw = env.FOSTER_FINANCE ? await env.FOSTER_FINANCE.get('gala_images_v1') : null;
    return new Response(raw || '{}', { headers });
  } catch (e) {
    return new Response('{}', { headers });
  }
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const headers = { 'Content-Type': 'application/json' };
  let b;
  try { b = await request.json(); } catch { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers }); }
  const id = (b.id || '').toString().slice(0, 40);
  const url = (b.url || '').toString();
  const label = (b.label || 'image').toString().slice(0, 40);
  if (!id || !url) return new Response(JSON.stringify({ error: 'id and url required' }), { status: 400, headers });
  if (!env.FOSTER_FINANCE) return new Response(JSON.stringify({ saved: false }), { headers });
  try {
    const raw = await env.FOSTER_FINANCE.get('gala_images_v1');
    const all = raw ? JSON.parse(raw) : {};
    const arr = all[id] || [];
    if (!arr.some(x => x.url === url)) arr.unshift({ url, label, ts: Date.now() });
    all[id] = arr.slice(0, 8); // keep the last 8 per item
    await env.FOSTER_FINANCE.put('gala_images_v1', JSON.stringify(all));
    return new Response(JSON.stringify({ saved: true }), { headers });
  } catch (e) {
    return new Response(JSON.stringify({ saved: false, error: String(e).slice(0, 120) }), { headers });
  }
}
