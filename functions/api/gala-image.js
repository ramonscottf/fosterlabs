// /api/gala-image
//   POST { id, imageUrl, prompt? }            -> { taskId }
//   GET  ?taskId=...                          -> { state, imageUrl, failMsg }
// Enhances the REAL product photo via Kie.ai Nano Banana Edit (keeps the item accurate).
// Needs KIE_API_KEY as a Pages env var.

const SUBMIT = 'https://api.kie.ai/api/v1/jobs/createTask';
const POLL   = 'https://api.kie.ai/api/v1/jobs/recordInfo';
const MODEL  = 'google/nano-banana-edit';

const DEFAULT_PROMPT = `Professional product photograph for an online charity-auction listing. Keep the product itself EXACTLY the same — identical shape, colors, materials, branding, labels, and details. Do NOT redesign, restyle, recolor, or invent any part of the product. Change ONLY the presentation: replace a cluttered or distracting background with a clean, softly lit neutral studio backdrop, improve lighting, sharpness, white balance, and exposure, and remove clutter. Photorealistic, crisp, e-commerce quality. Do not add any text, logos, watermarks, or new objects.`;

export async function onRequestPost(context) {
  const { request, env } = context;
  const headers = { 'Content-Type': 'application/json' };
  if (!env.KIE_API_KEY) return new Response(JSON.stringify({ error: 'KIE_API_KEY not set on this project — add it in Pages → fosterlabs → Settings → Variables' }), { status: 500, headers });

  let b;
  try { b = await request.json(); } catch { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers }); }
  const imageUrl = (b.imageUrl || '').toString();
  if (!imageUrl) return new Response(JSON.stringify({ error: 'imageUrl required' }), { status: 400, headers });
  const prompt = (b.prompt || DEFAULT_PROMPT).toString().slice(0, 2000);

  let resp;
  try {
    resp = await fetch(SUBMIT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + env.KIE_API_KEY },
      body: JSON.stringify({ model: MODEL, input: { prompt, image_urls: [imageUrl], output_format: 'png' } }),
    });
  } catch (e) { return new Response(JSON.stringify({ error: 'submit request failed' }), { status: 502, headers }); }

  const data = await resp.json().catch(() => ({}));
  if (!resp.ok || !(data.data && data.data.taskId)) {
    return new Response(JSON.stringify({ error: 'kie submit failed', detail: JSON.stringify(data).slice(0, 300) }), { status: 502, headers });
  }
  return new Response(JSON.stringify({ taskId: data.data.taskId }), { headers });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const headers = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' };
  if (!env.KIE_API_KEY) return new Response(JSON.stringify({ error: 'KIE_API_KEY not set' }), { status: 500, headers });

  const taskId = new URL(request.url).searchParams.get('taskId');
  if (!taskId) return new Response(JSON.stringify({ error: 'taskId required' }), { status: 400, headers });

  let resp;
  try { resp = await fetch(POLL + '?taskId=' + encodeURIComponent(taskId), { headers: { 'Authorization': 'Bearer ' + env.KIE_API_KEY } }); }
  catch (e) { return new Response(JSON.stringify({ error: 'poll request failed' }), { status: 502, headers }); }

  const data = await resp.json().catch(() => ({}));
  const d = data.data || {};
  let url = null;
  if (d.state === 'success' && d.resultJson) {
    try { url = (JSON.parse(d.resultJson).resultUrls || [])[0] || null; } catch (_) {}
  }
  return new Response(JSON.stringify({ state: d.state || 'unknown', imageUrl: url, failMsg: d.failMsg || '' }), { headers });
}
