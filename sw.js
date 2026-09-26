// Service Worker v4.1 — Dutch Education Guide
const CACHE_NAME='mbo-guide-v4.1';
const URLS_TO_CACHE=[
  './',
  './index.html',
  './manifest.webmanifest'
];

// Install: cache assets
self.addEventListener('install',(e)=>{
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache)=>{
      return cache.addAll(URLS_TO_CACHE).catch((err)=>{
        console.warn('Cache addAll failed:',err);
        return cache.add('./');
      });
    }).catch((err)=>{
      console.warn('Cache open failed:',err);
    })
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate',(e)=>{
  e.waitUntil(
    caches.keys().then((names)=>{
      return Promise.all(
        names.filter((name)=>name!==CACHE_NAME).map((name)=>caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch: network first, fallback to cache
self.addEventListener('fetch',(e)=>{
  if(e.request.method!=='GET')return;
  
  e.respondWith(
    fetch(e.request)
      .then((response)=>{
        if(!response||response.status!==200||response.type==='error'){
          return caches.match(e.request).catch(()=>response);
        }
        const clone=response.clone();
        caches.open(CACHE_NAME).then((cache)=>{
          cache.put(e.request,clone).catch(()=>{});
        });
        return response;
      })
      .catch(()=>{
        return caches.match(e.request).catch(()=>{
          return new Response('Offline - content not available',{
            status:503,
            statusText:'Service Unavailable',
            headers:new Headers({'Content-Type':'text/plain'})
          });
        });
      })
  );
});
