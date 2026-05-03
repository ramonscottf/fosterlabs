const CACHE = 'foster-health-v1';
const SHELL_ASSETS = [
  '/health/',
  '/health/index.html',
  '/health/manifest.json',
  '/health/icon-192.png',
  '/health/icon-512.png',
  '/health/icon-512.svg',
  '/health/apple-touch-icon.png',
  'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL_ASSETS).catch(err => {
      console.warn('Cache addAll partial fail:', err);
    }))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Network-first for API, cache-first for shell
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Don't intercept API calls — always go to network so D1 stays consistent
  if (url.pathname.startsWith('/api/')) {
    return; // browser default
  }

  // Only handle requests inside /health/ scope (or shared font CDN)
  if (!url.pathname.startsWith('/health/') && url.host !== 'fonts.googleapis.com' && url.host !== 'fonts.gstatic.com') {
    return;
  }

  // Cache-first for shell
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(resp => {
        // Cache successful responses
        if (resp.ok && resp.type !== 'opaque') {
          const clone = resp.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return resp;
      }).catch(() => caches.match('/health/'));
    })
  );
});
