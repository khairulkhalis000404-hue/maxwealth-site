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
