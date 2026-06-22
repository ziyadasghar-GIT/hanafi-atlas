// Ḥanafī Atlas — Service Worker
// Caches app shell + CDN assets for offline use.
// Map tiles: network-first with cache fallback.

const CACHE_NAME = 'hanafi-atlas-v1';

// Assets to pre-cache on install (app shell)
const PRECACHE_URLS = [
  './',
  './index.html',
  './map.html',
  './network.html',
  './manifest.json',
  './responsive.css',
  './icon-48x48.png',
  './icon-72x72.png',
  './icon-96x96.png',
  './icon-144x144.png',
  './icon-192x192.png',
  './icon-512x512.png',
  // CDN assets (versioned — safe to cache-first)
  'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css',
  'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js',
  'https://unpkg.com/@turf/turf@7.1.0/turf.min.js',
  'https://d3js.org/d3.v7.min.js',
];

// ── Install: pre-cache app shell ──
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch((err) => {
        // Don't fail install if some CDN assets are unreachable
        console.warn('SW: precache partial failure', err);
      });
    })
  );
  // Activate immediately — don't wait for old tabs
  self.skipWaiting();
});

// ── Activate: clean old caches ──
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  // Take control of all clients immediately
  self.clients.claim();
});

// ── Fetch: smart caching strategy ──
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // ── Strategy 1: Cache-first for versioned CDN assets ──
  if (
    url.hostname === 'unpkg.com' ||
    url.hostname === 'd3js.org'
  ) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // ── Strategy 2: Network-first for map tiles ──
  if (url.hostname === 'tiles.openfreemap.org') {
    event.respondWith(networkFirst(request));
    return;
  }

  // ── Strategy 3: Network-first for Google Fonts ──
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(networkFirst(request));
    return;
  }

  // ── Strategy 4: Stale-while-revalidate for app pages ──
  if (
    request.destination === 'document' ||
    url.pathname.endsWith('.html') ||
    url.pathname === '/' ||
    url.pathname.endsWith('/')
  ) {
    event.respondWith(staleWhileRevalidate(request));
    return;
  }

  // ── Default: network-first with cache fallback ──
  event.respondWith(networkFirst(request));
});

// ── Caching strategies ──

function cacheFirst(request) {
  return caches.match(request).then((cached) => {
    if (cached) return cached;
    return fetch(request).then((response) => {
      if (!response || response.status !== 200) return response;
      const clone = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
      return response;
    });
  });
}

function networkFirst(request) {
  return fetch(request)
    .then((response) => {
      if (!response || response.status !== 200) return response;
      const clone = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
      return response;
    })
    .catch(() => {
      return caches.match(request);
    });
}

function staleWhileRevalidate(request) {
  return caches.open(CACHE_NAME).then((cache) => {
    return cache.match(request).then((cached) => {
      const fetchPromise = fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            cache.put(request, response.clone());
          }
          return response;
        })
        .catch(() => cached);
      return cached || fetchPromise;
    });
  });
}
