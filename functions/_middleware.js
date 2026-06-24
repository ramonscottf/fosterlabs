// Foster Labs — edge inject the floating pill menu into every HTML page.
// Defensive: any failure falls through to the original response untouched.
export async function onRequest(context) {
  const res = await context.next();
  try {
    const ct = res.headers.get('content-type') || '';
    if (!ct.includes('text/html')) return res;
    return new HTMLRewriter()
      .on('body', {
        element(el) {
          el.append('\n<script defer src="/menu.js"></script>\n', { html: true });
        },
      })
      .transform(res);
  } catch (e) {
    return res;
  }
}
