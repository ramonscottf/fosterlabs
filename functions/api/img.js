// Image proxy so the private /gala-items copy tool can copy auction photos to
// the clipboard. The rackcdn CDN sends no CORS header, which blocks fetch()/
// canvas in the browser. This re-serves the image same-origin with CORS.
// Locked to rackcdn hosts so it can't be used as an open proxy.
export async function onRequestGet(context) {
  const { request } = context;
  const url = new URL(request.url);
  const target = url.searchParams.get("u");
  if (!target) return new Response("missing u", { status: 400 });

  let t;
  try { t = new URL(target); } catch (_) { return new Response("bad url", { status: 400 }); }
  if (t.protocol !== "https:" || !/(^|\.)rackcdn\.com$/.test(t.hostname)) {
    return new Response("host not allowed", { status: 403 });
  }

  let upstream;
  try {
    upstream = await fetch(t.toString(), {
      headers: { "User-Agent": "Mozilla/5.0 (compatible; FosterLabsImgProxy/1.0)" },
      cf: { cacheTtl: 86400, cacheEverything: true },
    });
  } catch (_) { return new Response("fetch failed", { status: 502 }); }
  if (!upstream.ok) return new Response("upstream " + upstream.status, { status: 502 });

  const headers = new Headers();
  headers.set("Content-Type", upstream.headers.get("Content-Type") || "image/png");
  headers.set("Access-Control-Allow-Origin", "*");
  headers.set("Cache-Control", "public, max-age=86400");
  return new Response(upstream.body, { status: 200, headers });
}
