const CACHE_NAME = "serphawk-crm-v4";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // Basic core assets to cache
      return cache.addAll(["/", "/manifest.json"]);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Network-first strategy ONLY for same-origin static/navigation requests (never intercept API or HMR calls)
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  try {
    const url = new URL(event.request.url);
    if (
      url.origin !== self.location.origin ||
      url.pathname.startsWith("/api/") ||
      url.pathname.startsWith("/_next/")
    ) {
      return;
    }
  } catch (e) {
    return;
  }

  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return new Response("Network error", {
          status: 503,
          headers: { "Content-Type": "text/plain" },
        });
      });
    })
  );
});
