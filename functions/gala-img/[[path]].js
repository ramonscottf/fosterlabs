// GET /gala-img/<key> -> streams the saved image from the gala-assets R2 bucket
export async function onRequestGet(context) {
  const { params, env } = context;
  const key = Array.isArray(params.path) ? params.path.join('/') : (params.path || '');
  if (!key || !env.GALA_ASSETS) return new Response('Not found', { status: 404 });
  const obj = await env.GALA_ASSETS.get(key);
  if (!obj) return new Response('Not found', { status: 404 });
  const headers = new Headers();
  obj.writeHttpMetadata(headers);
  if (!headers.get('Content-Type')) headers.set('Content-Type', 'image/png');
  headers.set('Cache-Control', 'public, max-age=31536000, immutable');
  return new Response(obj.body, { headers });
}
