// MaxWealth home: latest posts. The list is kept once, on khairulkhalis.com (assets/posts/posts.json), so both sites stay in step.
(function () {
  var section = document.getElementById('latestPosts');
  var list = document.getElementById('postList');
  if (!section || !list) return;
  var BASE = 'https://khairulkhalis.com/assets/posts/';
  var CHANNEL = 'https://whatsapp.com/channel/0029Vb6tZx5ADTOEl9TRTX2B';
  var SHOWN = 3;
  var NAMES = { whatsapp: 'WhatsApp', threads: 'Threads', linkedin: 'LinkedIn' };
  var MONTHS = {
    ms: ['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogo', 'Sep', 'Okt', 'Nov', 'Dis'],
    en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  };
  var posts = [];

  function render() {
    if (!posts.length) return;
    var en = document.documentElement.lang === 'en';
    list.innerHTML = '';
    posts.forEach(function (p) {
      var d = p.date.split('-').map(Number), name = NAMES[p.platform] || NAMES.whatsapp;
      var a = document.createElement('a');
      a.className = 'post';
      a.href = p.url || CHANNEL;
      a.target = '_blank';
      a.rel = 'noopener';
      a.innerHTML = '<div class="shot"><img loading="lazy" width="' + (p.w || 720) + '" height="' + (p.h || 900) + '"></div>' +
        '<div class="post-body"><span class="meta">' + name + ' · <time></time></span><span class="t"></span>' +
        '<span class="read">' + (en ? 'Read on ' : 'Baca di ') + name + ' →</span></div>';
      var img = a.querySelector('img');
      img.src = BASE + encodeURIComponent(p.img);
      img.alt = p.alt || '';
      var time = a.querySelector('time');
      time.dateTime = p.date;
      time.textContent = d[2] + ' ' + MONTHS[en ? 'en' : 'ms'][d[1] - 1] + ' ' + d[0];
      a.querySelector('.t').textContent = en ? (p.title_en || p.title_ms) : p.title_ms;
      list.appendChild(a);
    });
    section.hidden = false;
  }

  // Newest first, one post per topic (the same graphic often goes out on several platforms; the newest one wins)
  fetch(BASE + 'posts.json', { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (data) {
      var seen = {};
      posts = (Array.isArray(data) ? data : []).filter(function (p) { return p && p.img && p.date && p.title_ms; })
        .sort(function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; })
        .filter(function (p) { var k = p.topic || p.slug; if (seen[k]) return false; seen[k] = true; return true; })
        .slice(0, SHOWN);
      render();
    })
    .catch(function () {});
  document.addEventListener('mw:lang', render);
})();
