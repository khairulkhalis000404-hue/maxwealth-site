// MaxWealth Consultancy ebooks: prices and the Touch 'n Go purchase popup. The PDF is sent manually after the receipt reaches Ika on WhatsApp.
(function () {
  var sheet = document.getElementById('buyEbook');
  var WA = 'https://wa.me/60194024401?text=';
  var TNG_PAY_LINK = 'https://payment.tngdigital.com.my/sc/bDLosGkZ2e';
  var PRODUCTS = {
    ut: { name: 'Unit Trust Dari Zero', promo: 29, normal: 39 },
    urus: { name: 'Urus Duit Dari Zero', promo: 29, normal: 39 },
    combo: { name: 'Kombo Urus Duit Dari Zero + Unit Trust Dari Zero', promo: 49, normal: 69 }
  };
  // Promo until 30 Nov 2026 (Malaysia time), then the normal price; ?promoEnded=1 previews the after state
  var promoOver = Date.now() >= Date.parse('2026-12-01T00:00:00+08:00') || new URLSearchParams(location.search).get('promoEnded') === '1';
  var buyKey = 'ut';
  var isEn = function () { return document.documentElement.lang === 'en'; };
  var priceNow = function (key) { return promoOver ? PRODUCTS[key].normal : PRODUCTS[key].promo; };

  function render() {
    var en = isEn();
    document.querySelectorAll('.book.paid').forEach(function (b) {
      var key = b.dataset.product, p = PRODUCTS[key], now = priceNow(key);
      b.querySelector('.price').innerHTML = '<b>RM' + now + '</b>' + (promoOver ? '' : '<s>RM' + p.normal + '</s>');
      var tag = b.querySelector('.tag.promo');
      if (tag) tag.hidden = promoOver;
      b.href = WA + encodeURIComponent((en ? 'EBOOK - I am interested in the ebook ' : 'EBOOK - Saya berminat dengan ebook ') + p.name + ' (RM' + now + ')');
    });
    document.querySelectorAll('.buy-offer').forEach(function (o) {
      var p = PRODUCTS[o.dataset.product], now = priceNow(o.dataset.product);
      o.querySelector('.price').innerHTML = '<b>RM' + now + '</b>' + (promoOver ? '' : '<s>RM' + p.normal + '</s>');
      o.querySelector('.tag.promo').hidden = promoOver;
    });
    var save = document.querySelector('.book.combo .save');
    if (save) save.textContent = 'RM' + (priceNow('ut') + priceNow('urus') - priceNow('combo'));
    if (!sheet) return;
    var p = PRODUCTS[buyKey], amt = 'RM' + priceNow(buyKey);
    sheet.querySelectorAll('.amt').forEach(function (b) { b.textContent = amt; });
    sheet.querySelector('.buy-name').textContent = p.name;
    sheet.querySelector('.buy-price').textContent = promoOver ? amt
      : amt + (en ? ' (promo until 30 Nov, normally RM' + p.normal + ')' : ' (promo hingga 30 Nov, harga biasa RM' + p.normal + ')');
    var link = document.getElementById('tngLink');
    link.href = TNG_PAY_LINK;
    link.textContent = (en ? 'Pay ' : 'Bayar ') + amt + (en ? ' with Touch ’n Go' : ' dengan Touch ’n Go');
    document.getElementById('paidBtn').href = WA + encodeURIComponent(en
      ? 'EBOOK - I have paid ' + amt + ' via Touch ’n Go for ' + p.name + ', with my phone number in the payment details. Receipt attached.'
      : 'EBOOK - Saya dah bayar ' + amt + ' melalui Touch ’n Go untuk ' + p.name + ', dengan nombor telefon saya dalam butiran bayaran. Resit dilampirkan.');
  }

  if (sheet && sheet.showModal) {
    document.querySelectorAll('.book.paid, [data-buy]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        buyKey = b.dataset.product;
        render();
        sheet.showModal();
      });
    });
    sheet.addEventListener('click', function (e) {
      if (e.target === sheet || e.target.closest('[data-close]')) sheet.close();
    });
  }
  document.addEventListener('mw:lang', render);
  render();
})();
