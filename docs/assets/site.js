// MaxWealth Consultancy site: BM/EN toggle, mobile menu, WhatsApp message composer.
// BM is in the HTML; English lives in data-en (innerHTML) and data-en-<attr> (any attribute, e.g. href, content, aria-label).
(function () {
  var KEY = 'mwLang';
  var root = document.documentElement;

  function getLang() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function saveLang(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  // In-app browsers (TikTok, Instagram...) can't open WhatsApp or Touch 'n Go: name the app in the reminder before the BM/EN texts are read.
  // ?inapp=1 forces the reminder for testing.
  var UA = navigator.userAgent;
  var INAPP = null;
  [['TikTok', /musical_ly|Bytedance|TikTok/i], ['Instagram', /Instagram/i], ['Facebook', /FBAN|FBAV|FB_IAB/i], ['Threads', /Barcelona/i],
   ['LinkedIn', /LinkedInApp/i], ['X', /Twitter/i]].forEach(function (a) { if (!INAPP && a[1].test(UA)) INAPP = a[0]; });
  if (!INAPP && new URLSearchParams(location.search).get('inapp') === '1') INAPP = 'TikTok';
  document.querySelectorAll('#inappSheet [data-en]').forEach(function (el) {
    el.innerHTML = el.innerHTML.replace('{app}', INAPP || 'media sosial');
    el.setAttribute('data-en', el.getAttribute('data-en').replace('{app}', INAPP || 'social media'));
  });

  var textNodes = [];
  document.querySelectorAll('[data-en]').forEach(function (el) {
    textNodes.push({ el: el, ms: el.innerHTML, en: el.getAttribute('data-en') });
  });
  var attrNodes = [];
  document.querySelectorAll('*').forEach(function (el) {
    for (var i = 0; i < el.attributes.length; i++) {
      var a = el.attributes[i];
      if (a.name.indexOf('data-en-') === 0) {
        var name = a.name.slice(8);
        attrNodes.push({ el: el, name: name, ms: el.getAttribute(name), en: a.value });
      }
    }
  });
  // Bilingual legal pages carry a full block per language
  var blocks = document.querySelectorAll('.lang-block');

  function apply(lang) {
    var en = lang === 'en';
    textNodes.forEach(function (n) { n.el.innerHTML = en ? n.en : n.ms; });
    attrNodes.forEach(function (n) {
      var v = en ? n.en : n.ms;
      if (v === null) n.el.removeAttribute(n.name); else n.el.setAttribute(n.name, v);
    });
    blocks.forEach(function (b) { b.hidden = b.getAttribute('lang') !== (en ? 'en' : 'ms'); });
    root.lang = en ? 'en' : 'ms';
    document.querySelectorAll('.lang button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === (en ? 'en' : 'ms')));
    });
    root.classList.remove('lang-pending');
    document.dispatchEvent(new CustomEvent('mw:lang'));
  }

  var current = getLang() === 'en' ? 'en' : 'ms';
  apply(current);
  document.querySelectorAll('.lang button').forEach(function (b) {
    b.addEventListener('click', function () {
      current = b.dataset.lang === 'en' ? 'en' : 'ms';
      apply(current);
      saveLang(current);
    });
  });

  // First visit: ask which language; the choice is remembered, so it only shows once
  function canRemember() {
    try { localStorage.setItem(KEY + 'Test', '1'); localStorage.removeItem(KEY + 'Test'); return true; } catch (e) { return false; }
  }
  if (getLang() === null && canRemember() && !document.querySelector('.lp-hero')) {  // the ad landing page opens straight on the ebook
    var pop = document.createElement('div');
    pop.className = 'lang-pop';
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-modal', 'true');
    pop.setAttribute('aria-labelledby', 'langPopTitle');
    pop.innerHTML = '<div class="lang-pop-box">' +
      '<h2 id="langPopTitle">Choose your language <span>Pilih bahasa</span></h2>' +
      '<div class="lang-pop-btns"><button type="button" class="btn" data-pick="ms">Bahasa Melayu</button><button type="button" class="btn ghost" data-pick="en">English</button></div></div>';
    var done = function (lang) {
      current = lang;
      apply(lang);
      saveLang(lang);
      pop.remove();
      document.body.classList.remove('menu-lock');
    };
    pop.addEventListener('click', function (e) {
      var b = e.target.closest('[data-pick]');
      if (b) done(b.dataset.pick);
    });
    pop.addEventListener('keydown', function (e) {
      var btns = pop.querySelectorAll('button');
      if (e.key === 'Escape') done(current);
      if (e.key === 'Tab') {
        e.preventDefault();
        btns[document.activeElement === btns[0] ? 1 : 0].focus();
      }
    });
    document.body.appendChild(pop);
    document.body.classList.add('menu-lock');
    pop.querySelector('button').focus();
  }

  // Mobile menu
  var header = document.querySelector('.site-header');
  var menuBtn = document.querySelector('.menu-btn');
  function setMenu(open) {
    if (!header || !menuBtn) return;
    header.classList.toggle('menu-open', open);
    document.body.classList.toggle('menu-lock', open);
    menuBtn.setAttribute('aria-expanded', String(open));
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(!header.classList.contains('menu-open')); });
    document.querySelectorAll('.menu-panel a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width: 1000px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  // Servis menu: the header button opens the list of service pages (tap/click; hover also opens it on desktop mice).
  // Closes on a click outside, Escape, or when another one opens.
  var subBtns = document.querySelectorAll('.sub-btn');
  function setSub(btn, open) {
    btn.setAttribute('aria-expanded', String(open));
    document.getElementById(btn.getAttribute('aria-controls')).hidden = !open;
  }
  subBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      subBtns.forEach(function (b) { if (b !== btn) setSub(b, false); });
      setSub(btn, open);
    });
    var li = btn.parentNode, timer;
    if (btn.closest('.nav') && window.matchMedia('(hover: hover)').matches) {
      li.addEventListener('mouseenter', function () { clearTimeout(timer); setSub(btn, true); });
      li.addEventListener('mouseleave', function () { timer = setTimeout(function () { setSub(btn, false); }, 180); });
    }
  });
  document.addEventListener('click', function (e) {
    subBtns.forEach(function (b) { if (b.closest('.nav') && !b.parentNode.contains(e.target)) setSub(b, false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    subBtns.forEach(function (b) { if (b.getAttribute('aria-expanded') === 'true') { setSub(b, false); if (b.closest('.nav')) b.focus(); } });
  });

  // Header hides after scrolling down a fair way (past ~320px) and reappears on scroll up, at the top,
  // or when keyboard focus moves into it. Small jitters (<8px) are ignored; never hides with the menu open.
  if (header) {
    var lastY = window.scrollY;
    window.addEventListener('scroll', function () {
      var y = window.scrollY;
      if (header.classList.contains('menu-open') || y < 320) { header.classList.remove('hide'); lastY = y; return; }
      if (y > lastY + 8) { header.classList.add('hide'); lastY = y; }
      else if (y < lastY - 8) { header.classList.remove('hide'); lastY = y; }
    }, { passive: true });
    header.addEventListener('focusin', function () { header.classList.remove('hide'); });
  }

  // Home: "Tahukah anda?" card. Starts on a random fact and moves on every 8 s (a JS timer drives it and
  // the yellow bar shows the progress); hover/focus/touch pauses it, and pressing an arrow stops the
  // auto-rotation for good so the reader sets the pace.
  var fun = document.querySelector('.fun');
  if (fun) {
    var facts = fun.querySelectorAll('.fun-list li');
    var numEl = fun.querySelector('.fun-num');
    var bar = fun.querySelector('.fun-bar i');
    var STEP = 8000, TICK = 100;
    var at = 0, elapsed = 0, paused = false, stopped = false;
    var show = function (k) {
      facts[at].classList.remove('on'); facts[at].setAttribute('aria-hidden', 'true');
      at = (k + facts.length) % facts.length;
      facts[at].classList.add('on'); facts[at].removeAttribute('aria-hidden');
      numEl.textContent = (at < 9 ? '0' : '') + (at + 1);
      elapsed = 0; bar.style.transform = 'scaleX(0)';
    };
    var timer = setInterval(function () {
      if (paused || stopped) return;
      elapsed += TICK;
      if (elapsed >= STEP) show(at + 1);
      else bar.style.transform = 'scaleX(' + (elapsed / STEP).toFixed(3) + ')';
    }, TICK);
    fun.querySelectorAll('.fun-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        stopped = true; clearInterval(timer); fun.classList.add('stopped');
        show(at + Number(b.dataset.step));
      });
    });
    var pause = function () { paused = true; };
    var resume = function () { paused = false; };
    fun.addEventListener('mouseenter', pause);
    fun.addEventListener('mouseleave', resume);
    fun.addEventListener('focusin', pause);
    fun.addEventListener('focusout', resume);
    fun.addEventListener('touchstart', pause, { passive: true });
    fun.addEventListener('touchend', resume);
    show(Math.floor(Math.random() * facts.length));
  }

  // Contact forms: compose a WhatsApp message to Ika (Admin) or the person picked in the form; nothing is stored or sent by this site
  document.querySelectorAll('#waForm, #waFormAznah').forEach(function (form) {
    // Aznah's form: Ika only covers unit trust and PRS, every other topic goes to Aznah
    if (form.elements.to) {
      var syncTo = function () {
        var topic = form.elements.topic;
        var ika = topic.options[topic.selectedIndex].hasAttribute('data-ika');
        form.elements.to.closest('.field').style.display = ika ? '' : 'none';
        if (!ika) form.elements.to.selectedIndex = 0;
      };
      form.elements.topic.addEventListener('change', syncTo);
      syncTo();
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var en = current === 'en';
      var name = form.elements.name.value.trim();
      var topicEl = form.elements.topic;
      var topic = topicEl.options[topicEl.selectedIndex].text.trim();
      var msg = form.elements.message.value.trim();
      var to = form.elements.to ? form.elements.to.options[form.elements.to.selectedIndex] : null;
      var lines = [];
      if (to) lines.push(en ? to.dataset.helloEn : to.dataset.hello);
      else lines.push(en ? 'Hi Ika, I found MaxWealth Consultancy through the website.' : 'Hai Ika, saya jumpa MaxWealth Consultancy melalui website.');
      if (name) lines.push((en ? 'Name: ' : 'Nama: ') + name);
      lines.push((en ? 'Topic: ' : 'Topik: ') + topic);
      if (msg) lines.push((en ? 'Message: ' : 'Mesej: ') + msg);
      var url = 'https://wa.me/' + (to ? to.value : '60194024401') + '?text=' + encodeURIComponent(lines.join('\n'));
      // 'noopener' would make window.open return null, so detach the opener by hand
      var w = window.open(url, '_blank');
      if (w) w.opener = null; else location.href = url;
    });
  });

  // In-app browsers, same as khairulkhalis.com (user, 14 Nov 2026: the bottom bar was not friendly): the full "open in your browser"
  // sheet once per visit on arrival (after the language popup), and again whenever a WhatsApp or Touch 'n Go link is tapped,
  // since those rarely open inside these apps. One button per phone: Safari on iPhone (iOS 17+), Chrome on Android.
  var inappSheet = document.getElementById('inappSheet');
  if (inappSheet && inappSheet.showModal && INAPP) {
    var IOS = /iPhone|iPad|iPod/i.test(UA), ANDROID = /Android/i.test(UA);
    var browserName = IOS ? 'Safari' : ANDROID ? 'Chrome' : '';
    var openUrl = IOS ? 'x-safari-' + location.href
      : ANDROID ? 'intent://' + location.host + location.pathname + location.search + '#Intent;scheme=https;package=com.android.chrome;end' : '';
    var openBtn = document.getElementById('inappOpen');
    var labelOpen = function () {
      if (browserName) openBtn.textContent = (root.lang === 'en' ? 'Open in ' : 'Buka dalam ') + browserName;
    };
    if (openUrl) {
      openBtn.href = openUrl;
      openBtn.hidden = false;
      document.getElementById('inappCopy').classList.add('ghost');
    }
    labelOpen();
    document.addEventListener('mw:lang', labelOpen);

    var openSheet = function (target) {   // link mode: a WhatsApp / Touch 'n Go button was tapped
      inappSheet.classList.add('link-mode');
      inappSheet.querySelectorAll('.lnk-app').forEach(function (x) { x.textContent = target; });
      if (!inappSheet.open) inappSheet.showModal();
    };
    inappSheet.addEventListener('close', function () { try { sessionStorage.setItem('mwInappSeen', '1'); } catch (e) {} });
    document.getElementById('inappGo').addEventListener('click', function () { inappSheet.close(); });
    document.getElementById('inappStay').addEventListener('click', function () { inappSheet.close(); });
    inappSheet.addEventListener('click', function (e) { if (e.target === inappSheet) inappSheet.close(); });

    // On arrival, once per visit: wait for the first-visit language popup to be answered, then show the general sheet
    var seen = null;
    try { seen = sessionStorage.getItem('mwInappSeen'); } catch (e) {}
    if (!seen) {
      var showGeneral = function () {
        if (document.querySelector('.lang-pop')) { setTimeout(showGeneral, 300); return; }
        inappSheet.classList.remove('link-mode');
        if (!inappSheet.open) inappSheet.showModal();
      };
      setTimeout(showGeneral, 350);
    }
    document.getElementById('inappCopy').addEventListener('click', function () {
      var btn = this, url = location.href;
      var done = function () {
        btn.textContent = root.lang === 'en' ? 'Link copied, paste it in Safari or Chrome' : 'Link disalin, tampal dalam Safari atau Chrome';
      };
      var fallback = function () {
        var t = document.createElement('textarea');
        t.value = url; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
        inappSheet.appendChild(t); t.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        t.remove();
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fallback); else fallback();
    });
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || a.hasAttribute('data-skip-remind') || a.matches('[data-buy], .book.paid')) return;   // ebook buttons open the payment sheet first
      if (!/(^|\.)(wa\.me|whatsapp\.com|tngdigital\.com\.my)$/.test(a.hostname)) return;
      e.preventDefault();
      e.stopPropagation();
      document.getElementById('inappGo').href = a.href;
      openSheet(/tngdigital/.test(a.hostname) ? 'Touch ’n Go' : 'WhatsApp');
    }, true);
  }

  // TikTok Pixel + Umami: WhatsApp buttons count as Contact (the ebook's "I've paid" button is tracked in ebook.js instead)
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.id === 'paidBtn' || a.matches('[data-buy], .book.paid')) return;
    if (!/(^|\.)(wa\.me|whatsapp\.com)$/.test(a.hostname)) return;
    if (window.ttq) window.ttq.track('Contact');
    if (window.umami) window.umami.track('MW: WhatsApp', { page: location.pathname });
  }, true);
})();
