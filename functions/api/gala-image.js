// /api/gala-image
//   POST { id, imageUrl, prompt?, model?, aspect_ratio?, resolution? } -> { taskId }
//   GET  ?taskId=...                                                   -> { state, imageUrl, failMsg }
// Image gen via Kie.ai. Default model google/nano-banana-edit (single photo cleanup, uses image_urls).
// model "nano-banana-pro" -> Nano Banana Pro (uses image_input + aspect_ratio + resolution).
// Needs KIE_API_KEY as a Pages env var.

const SUBMIT = 'https://api.kie.ai/api/v1/jobs/createTask';
const POLL   = 'https://api.kie.ai/api/v1/jobs/recordInfo';

const DEFAULT_PROMPT = `Professional product photograph for an online charity-auction listing. Keep the product itself EXACTLY the same — identical shape, colors, materials, branding, labels, and details. Do NOT redesign, restyle, recolor, or invent any part of the product. Change ONLY the presentation: replace a cluttered background with a clean, softly lit neutral studio backdrop, improve lighting, sharpness, white balance and exposure, remove clutter. Photorealistic, crisp, e-commerce quality. No added text, logos, watermarks, or new objects.`;

function buildInput(model, prompt, imageUrl, aspect_ratio, resolution) {
  const isPro = /pro/i.test(model);
  const input = { prompt, output_format: 'png' };
  if (imageUrl) {
    if (isPro) input.image_input = [imageUrl];   // Nano Banana Pro
    else input.image_urls = [imageUrl];          // Nano Banana Edit
  }
  if (aspect_ratio) input.aspect_ratio = aspect_ratio;
  if (isPro) input.resolution = resolution || '2K';
  return input;
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const headers = { 'Content-Type': 'application/json' };
  if (!env.KIE_API_KEY) return new Response(JSON.stringify({ error: 'KIE_API_KEY not set on this project — add it in Pages → fosterlabs → Settings → Variables' }), { status: 500, headers });

  let b;
  try { b = await request.json(); } catch { return new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers }); }
  const imageUrl = (b.imageUrl || '').toString();
  const model = (b.model || 'google/nano-banana-edit').toString();
  const aspect_ratio = b.aspect_ratio ? b.aspect_ratio.toString() : '';
  const resolution = b.resolution ? b.resolution.toString() : '';
  const prompt = (b.prompt || DEFAULT_PROMPT).toString().slice(0, 2500);
  if (!imageUrl && !/text/i.test(model)) { /* image-to-image needs a source, but allow text models without */ }

  let resp;
  try {
    resp = await fetch(SUBMIT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + env.KIE_API_KEY },
      body: JSON.stringify({ model, input: buildInput(model, prompt, imageUrl, aspect_ratio, resolution) }),
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
  let url = null, tempUrl = null;
  if (d.state === 'success' && d.resultJson) {
    try { tempUrl = (JSON.parse(d.resultJson).resultUrls || [])[0] || null; } catch (_) {}
    url = tempUrl;
    if (tempUrl && env.GALA_ASSETS) {
      const key = 'gen/' + taskId + '.png';
      try {
        let exists = null;
        try { exists = await env.GALA_ASSETS.head(key); } catch (_) {}
        if (!exists) {
          const ir = await fetch(tempUrl);
          if (ir.ok) {
            const buf = await ir.arrayBuffer();
            await env.GALA_ASSETS.put(key, buf, { httpMetadata: { contentType: 'image/png' } });
          }
        }
        url = new URL(request.url).origin + '/gala-img/' + key; // permanent
      } catch (e) { /* keep temp url as fallback */ }
    }
  }
  return new Response(JSON.stringify({ state: d.state || 'unknown', imageUrl: url, tempUrl, failMsg: d.failMsg || '' }), { headers });
}
