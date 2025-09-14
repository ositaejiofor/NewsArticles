const CACHE_NAME = "newsportal-cache-v1";
const urlsToCache = [
    "/",
    "/static/images/favicon-192x192.png",
    "/static/images/favicon-512x512.png",
    "/static/css/style.css",
    "/static/core/css/navbar.css",
    "/static/js/navbar.js",
];

// Install service worker
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

// Activate service worker
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })
    );
});

// Fetch from cache or network
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
