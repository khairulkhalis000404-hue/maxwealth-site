// MaxWealth /daftar/: the same form as khairulkhalis.com/hubungi/. Calculator buttons land here with their numbers
// (?pick=&age=&bal=&lump=&monthly=&rate=&years=); the visitor adds name, age, location and phone, and one WhatsApp
// message goes to Ika (Admin) with everything. Nothing is stored or sent by this site.
(function () {
  var form = document.getElementById('daftar');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var isEn = function () { return document.documentElement.lang === 'en'; };
  var num = function (id) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? v : 0; };
  var rm = function (v) { return 'RM' + Math.round(v).toLocaleString('en-MY'); };
  var row = function (color, label, value) { return '<div><dt><i style="background:' + color + '"></i>' + label + '</dt><dd>' + value + '</dd></div>'; };
  var picks = function () { return [].slice.call(form.querySelectorAll('input[name=pick]:checked')).map(function (c) { return c.value; }); };
  var has = function (p, v) { return p.indexOf(v) !== -1; };

  // Basic Savings in Akaun Persaraan by age, effective 1 Jan 2026 (ages 18 to 55); same table as calc.js
  var BASIC = [900, 1100, 1500, 1900, 4000, 6200, 8500, 11000, 13700, 16600, 19600, 22900, 26300, 30000, 33900,
    38100, 42400, 47000, 51900, 57000, 62400, 68100, 74000, 80200, 86700, 93600, 100000, 108000, 115000, 124000,
    132000, 141000, 150000, 160000, 170000, 181000, 192000, 203000];

  // Calculator-first pages (Servis) have a second age box in the eligibility panel; both stay in step
  var epAge = $('dfEpAge');
  if (epAge) {
    epAge.addEventListener('input', function () { $('dfAge').value = epAge.value; });
    $('dfAge').addEventListener('input', function () { epAge.value = $('dfAge').value; });
  }
  // "I'm not sure how much to invest yet": hides the amount calculators and says so in the message
  var unsure = function () { return !!($('dfUnsure') && $('dfUnsure').checked); };

  function epCalc() {
    var age = Math.floor(num('dfAge')), bal = num('dfBal');
    if (!age || !bal) return { ready: false };
    if (age < 18) return { ready: true, age: age, bal: bal, note: 'young' };
    if (age >= 55) return { ready: true, age: age, bal: bal, note: 'over55' };
    var basic = BASIC[age - 18], excess = Math.max(bal - basic, 0), can = excess * 0.3;
    return { ready: true, age: age, bal: bal, basic: basic, excess: excess, can: can, ok: can >= 1000 };
  }
  // Same method as the compound calculator (calc.js): yearly compounding, a year's top-ups counted at the end of that year
  function growCalc(p) {
    var lump = (has(p, 'lump') || has(p, 'prs') || has(p, 'corp')) ? num('dfLump') : 0;
    var monthly = (has(p, 'monthly') || has(p, 'prs') || has(p, 'corp')) ? num('dfMonthly') : 0;
    var pct = num('dfRate'), years = Math.min(Math.round(num('dfYears')), 60), v = lump;
    for (var y = 0; y < years; y++) v = v * (1 + pct / 100) + monthly * 12;
    return { lump: lump, monthly: monthly, rate: pct, years: years, total: v, paid: lump + monthly * 12 * years };
  }

  function update() {
    var p = picks(), en = isEn();
    $('dfEpBox').hidden = unsure() || !has(p, 'epf');
    $('dfGrowBox').hidden = unsure() || !(has(p, 'lump') || has(p, 'monthly') || has(p, 'prs') || has(p, 'corp'));
    $('dfLumpField').hidden = !(has(p, 'lump') || has(p, 'prs') || has(p, 'corp'));
    $('dfMonthlyField').hidden = !(has(p, 'monthly') || has(p, 'prs') || has(p, 'corp'));
    form.querySelector('[data-field="company"]').hidden = !has(p, 'corp');

    var e = epCalc(), out;
    if (!e.ready) {
      out = '<p class="msg">' + (epAge
        ? (en ? 'Enter your age and your Retirement Account balance.' : 'Isi umur dan baki Akaun Persaraan anda.')
        : (en ? 'Enter your age (section 1) and your Retirement Account balance.' : 'Isi umur (bahagian 1) dan baki Akaun Persaraan anda.')) + '</p>';
    } else if (e.note === 'young') {
      out = '<p class="msg warn">' + (en ? 'Available from age 18.' : 'Untuk umur 18 tahun ke atas.') + '</p>';
    } else if (e.note === 'over55') {
      out = '<p class="msg warn">' + (en
        ? 'At 55 and above, the Members Investment Scheme no longer applies, but you can still invest part of your savings through the Age 55/60 Withdrawal (Investment). Send this form and we will check it with you.'
        : 'Pada umur 55 tahun ke atas, Skim Pelaburan Ahli tidak lagi terpakai, tetapi anda masih boleh melabur sebahagian simpanan melalui Pengeluaran Umur 55/60 (Pelaburan). Hantar borang ini dan kami semak bersama anda.') + '</p>';
    } else {
      out = '<div class="big"><small>' + (en ? 'You can invest up to' : 'Anda boleh labur sehingga') + '</small><b>' + rm(e.ok ? e.can : 0) + '</b></div>' +
        '<dl>' + row('#FFFFFF', en ? 'Basic Savings (age ' + e.age + ')' : 'Simpanan Asas (umur ' + e.age + ')', rm(e.basic)) +
        row('rgba(255,255,255,.35)', en ? 'Amount above Basic Savings' : 'Jumlah melebihi Simpanan Asas', rm(e.excess)) +
        row('var(--accent)', en ? '30% of that amount' : '30% daripada jumlah itu', rm(e.can)) + '</dl>' +
        '<p class="msg' + (e.ok ? '' : ' warn') + '">' + (e.ok
          ? (en ? 'You are eligible. The minimum investment is RM1,000.' : 'Anda layak. Pelaburan minimum ialah RM1,000.')
          : (en ? 'Below the RM1,000 minimum for now. Send the form anyway and we can look at other options with you.'
                : 'Belum capai minimum RM1,000 buat masa ini. Hantar juga borang ini, kami boleh semak pilihan lain bersama anda.')) + '</p>';
    }
    $('dfEpResult').innerHTML = out;

    var g = growCalc(p);
    if (!g.paid) {
      $('dfGrowResult').innerHTML = '<p class="msg">' + (en ? 'Enter an amount to see the illustration.' : 'Isi jumlah untuk lihat ilustrasi.') + '</p>';
    } else {
      var paidPct = g.total > g.paid ? g.paid / g.total * 100 : 100;
      $('dfGrowResult').innerHTML =
        '<div class="big"><small>' + (en ? 'Illustrated value after ' + g.years + ' years' : 'Nilai ilustrasi selepas ' + g.years + ' tahun') + '</small><b>' + rm(g.total) + '</b></div>' +
        '<div class="split"><span class="a" style="width:' + paidPct + '%"></span><span class="b" style="width:' + (100 - paidPct) + '%"></span></div>' +
        '<dl>' + row('#FFFFFF', en ? 'Your capital' : 'Modal anda', rm(g.paid)) +
        row('var(--accent)', en ? 'Growth' : 'Pertumbuhan', rm(Math.max(g.total - g.paid, 0))) + '</dl>';
    }
    $('dfGrowFine').textContent = en
      ? 'Illustration assuming ' + g.rate + '% a year, not a projection of returns. Actual returns vary and are not guaranteed. Investing involves risk.'
      : 'Ilustrasi andaian ' + g.rate + '% setahun, bukan unjuran pulangan. Pulangan sebenar berubah-ubah dan tidak dijamin. Pelaburan melibatkan risiko.';
  }
  form.querySelectorAll('input, textarea').forEach(function (i) {
    i.addEventListener('input', function () { update(); var f = i.closest('[data-field]'); if (f) f.classList.remove('invalid'); });
    i.addEventListener('change', update);
  });

  // Validation: mark fields red and show the reason under them
  function mark(field, bad) {
    var el = form.querySelector('[data-field="' + field + '"]');
    el.classList.toggle('invalid', bad);
    var err = el.querySelector('.df-err');
    if (err) err.hidden = !bad;
    return bad;
  }
  function validate(p) {
    var phone = $('dfPhone').value.replace(/\D/g, '').replace(/^60/, '').replace(/^0/, '');
    var bad = [];
    if (mark('name', $('dfName').value.trim().length < 2)) bad.push('name');
    if (mark('age', !(num('dfAge') >= 18 && num('dfAge') <= 100))) bad.push('age');
    if (mark('city', $('dfCity').value.trim().length < 2)) bad.push('city');
    if (mark('phone', !/^1\d{7,9}$/.test(phone))) bad.push('phone');
    if (mark('choices', p.length === 0)) bad.push('choices');
    $('dfErr').hidden = !bad.length;
    if (bad.length) {
      var first = form.querySelector('[data-field="' + bad[0] + '"]');
      first.scrollIntoView({ behavior: 'smooth', block: 'center' });
      var f = first.querySelector('input');
      if (f && bad[0] !== 'choices') setTimeout(function () { f.focus({ preventScroll: true }); }, 300);
    }
    return { ok: !bad.length, phone: phone };
  }

  // The WhatsApp message, in the visitor's language. The first word is Ika's keyword (SOP): KORPORAT, PRS or UNIT TRUST.
  function buildMessage(p, phone) {
    var en = isEn();
    var names = {
      lump: en ? 'One-time investment (lump sum)' : 'Pelaburan sekali (lump sum)',
      monthly: 'Regular Savings Plan (RSP)',
      epf: en ? 'Retirement Savings (Account 1) investment' : 'Pelaburan Simpanan Persaraan (Akaun 1)',
      corp: en ? 'Corporate investment' : 'Pelaburan korporat',
      prs: en ? 'PRS investment' : 'Pelaburan PRS'
    };
    var key = has(p, 'corp') ? 'KORPORAT' : (p.length === 1 && has(p, 'prs')) ? 'PRS' : 'UNIT TRUST';
    var L = [];
    L.push(key + ' - ' + (en ? '*Registration / investment enquiry (MaxWealth website)*' : '*Pendaftaran / pertanyaan pelaburan (website MaxWealth)*'));
    L.push((en ? 'Name: ' : 'Nama: ') + $('dfName').value.trim());
    L.push((en ? 'Age: ' : 'Umur: ') + Math.floor(num('dfAge')));
    L.push((en ? 'Location: ' : 'Lokasi: ') + $('dfCity').value.trim());
    L.push((en ? 'Phone: ' : 'Telefon: ') + '+60' + phone);
    var co = $('dfCo').value.trim();
    if (has(p, 'corp') && co) L.push((en ? 'Company: ' : 'Syarikat: ') + co);
    L.push((en ? 'Looking for: ' : 'Pilihan: ') + p.map(function (k) { return names[k]; }).join(', '));
    var g = growCalc(p);
    if (unsure()) {
      L.push(en ? 'Amount: not sure yet, please help me work it out' : 'Jumlah: belum pasti, mohon bantu kira');
    } else if (g.paid) {
      if (g.lump) L.push((en ? 'One-time amount: ' : 'Jumlah sekali: ') + rm(g.lump));
      if (g.monthly) L.push((en ? 'Monthly amount: ' : 'Jumlah bulanan: ') + rm(g.monthly));
      L.push((en ? 'Period: ' : 'Tempoh: ') + g.years + (en ? ' years' : ' tahun'));
      L.push((en ? 'Illustration at ' : 'Ilustrasi pada ') + g.rate + '%' + (en ? ' a year: ' : ' setahun: ') + rm(g.total));
    }
    if (has(p, 'epf') && !unsure()) {
      var e = epCalc();
      if (e.ready) {
        L.push((en ? 'Retirement Account balance: ' : 'Baki Akaun Persaraan: ') + rm(e.bal));
        if (e.can !== undefined) L.push((en ? 'Can invest (30% above Basic Savings): ' : 'Boleh labur (30% melebihi Simpanan Asas): ') + rm(e.ok ? e.can : 0));
        if (e.note === 'over55') L.push(en ? 'Age 55+: Age 55/60 Withdrawal (Investment)' : 'Umur 55+: Pengeluaran Umur 55/60 (Pelaburan)');
      }
    }
    var note = $('dfNote').value.trim();
    if (note) L.push((en ? 'Note: ' : 'Nota: ') + note);
    return L.join('\n');
  }

  // Send through a link click so site.js can show its open-in-browser sheet inside TikTok/IG and count the Contact
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var p = picks(), v = validate(p);
    if (!v.ok) return;
    var go = $('dfGo');
    go.href = 'https://wa.me/60194024401?text=' + encodeURIComponent(buildMessage(p, v.phone));
    go.click();
  });

  // Prefill from the calculators, e.g. /daftar/?pick=epf&age=30&bal=50000
  var qs = new URLSearchParams(location.search);
  (qs.get('pick') || '').split(',').forEach(function (val) {
    var c = form.querySelector('input[name=pick][value="' + val + '"]');
    if (c) c.checked = true;
  });
  [['age', 'dfAge'], ['bal', 'dfBal'], ['lump', 'dfLump'], ['monthly', 'dfMonthly'], ['rate', 'dfRate'], ['years', 'dfYears']].forEach(function (m) {
    var val = parseFloat(qs.get(m[0]));
    if (isFinite(val) && val > 0) $(m[1]).value = val;
  });
  if (epAge && $('dfAge').value) epAge.value = $('dfAge').value;
  document.addEventListener('mw:lang', update);
  new MutationObserver(update).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  update();
})();
