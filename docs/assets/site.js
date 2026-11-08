// MaxWealth Consultancy site: BM/EN toggle, mobile menu, WhatsApp message composer.
// BM is in the HTML; English lives in data-en (innerHTML) and data-en-<attr> (any attribute, e.g. href, content, aria-label).
(function () {
  var KEY = 'mwLang';
  var root = document.documentElement;

  function getLang() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function saveLang(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

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
  if (getLang() === null && canRemember()) {
    var pop = document.createElement('div');
    pop.className = 'lang-pop';
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-modal', 'true');
    pop.setAttribute('aria-labelledby', 'langPopTitle');
    pop.innerHTML = '<div class="lang-pop-box">' +
      '<h2 id="langPopTitle">Pilih bahasa <span>Choose your language</span></h2>' +
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

  // Contact page: compose a WhatsApp message to Ika (Admin); nothing is stored or sent by this site
  var form = document.getElementById('waForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var en = current === 'en';
      var name = form.elements.name.value.trim();
      var topicEl = form.elements.topic;
      var topic = topicEl.options[topicEl.selectedIndex].text.trim();
      var msg = form.elements.message.value.trim();
      var lines = [];
      lines.push(en ? 'Hi Ika, I found MaxWealth Consultancy through the website.' : 'Hai Ika, saya jumpa MaxWealth Consultancy melalui website.');
      if (name) lines.push((en ? 'Name: ' : 'Nama: ') + name);
      lines.push((en ? 'Topic: ' : 'Topik: ') + topic);
      if (msg) lines.push((en ? 'Message: ' : 'Mesej: ') + msg);
      var url = 'https://wa.me/60194024401?text=' + encodeURIComponent(lines.join('\n'));
      // 'noopener' would make window.open return null, so detach the opener by hand
      var w = window.open(url, '_blank');
      if (w) w.opener = null; else location.href = url;
    });
  }
})();
