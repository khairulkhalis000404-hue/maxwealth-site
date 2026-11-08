// MaxWealth Consultancy calculators (Sumber page): emergency fund, compound growth, TVM. Runs in the browser; nothing is stored or sent.
(function () {
  var box = document.getElementById('calc');
  if (!box) return;
  var WA = 'https://wa.me/60194024401?text=';
  var $ = function (id) { return document.getElementById(id); };
  var isEn = function () { return document.documentElement.lang === 'en'; };
  var num = function (id) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? v : 0; };
  var rm = function (v) { return 'RM' + Math.round(v).toLocaleString('en-MY'); };
  var row = function (color, label, value) {
    return '<div><dt><i style="background:' + color + '"></i>' + label + '</dt><dd>' + value + '</dd></div>';
  };
  var unit = function (v, one, many, ms) { return v + (isEn() ? (v === 1 ? one : many) : ms); };
  var bigOut = function (label, value) { return '<div class="big"><small>' + label + '</small><b>' + value + '</b></div>'; };
  var note = function (text, warn) { return '<p class="msg' + (warn ? ' warn' : '') + '">' + text + '</p>'; };
  var setCta = function (id, ms, en) { $(id).href = WA + encodeURIComponent(isEn() ? en : ms); };
  var minNote = function (v) {
    return v > 0 && v < 100 ? note(isEn() ? 'The minimum monthly investment with us is RM100.' : 'Minimum pelaburan bulanan dengan kami ialah RM100.', true) : '';
  };
  var fine = function (pct, extraMs, extraEn) {
    return isEn()
      ? 'Illustration assuming ' + pct + '% a year, not a projection of returns.' + (extraEn || '') + ' Actual returns vary and are not guaranteed. Investing involves risk.'
      : 'Ilustrasi andaian ' + pct + '% setahun, bukan unjuran pulangan.' + (extraMs || '') + ' Pulangan sebenar berubah-ubah dan tidak dijamin. Pelaburan melibatkan risiko.';
  };

  // Year-end values; a year's top-ups (monthly x 12) go in at the end of each year
  function growthPath(start, monthly, pct, years) {
    var r = pct / 100, v = start, out = [start];
    for (var y = 1; y <= years; y++) { v = v * (1 + r) + monthly * 12; out.push(v); }
    return out;
  }
  function rmShort(v) {
    if (v >= 1e6) return 'RM' + (v / 1e6).toFixed(v >= 1e7 ? 0 : 1).replace(/\.0$/, '') + (isEn() ? 'm' : 'j');
    if (v >= 1e3) return 'RM' + Math.round(v / 1e3) + 'k';
    return 'RM' + Math.round(v);
  }
  // Money paid in against 8% and 10% a year (plus 9% when it is the chosen rate)
  function growthChart(start, monthly, pct, years) {
    if (!years || (!start && !monthly)) return '';
    var en = isEn(), paid = [];
    for (var y = 0; y <= years; y++) paid.push(start + monthly * 12 * y);
    var rates = pct === 8 || pct === 10 ? [8, 10] : [8, pct, 10];
    var lines = [{ vals: paid, color: 'rgba(255,255,255,.55)', dash: '4 4', label: en ? 'Your money in' : 'Wang anda masuk' }].concat(rates.map(function (r) {
      return { vals: growthPath(start, monthly, r, years), color: r === pct ? 'var(--accent)' : '#FFFFFF', dash: '', label: r + (en ? '% a year' : '% setahun') };
    }));
    var max = Math.max.apply(null, lines.map(function (l) { return l.vals[years]; })) || 1;
    var mag = Math.pow(10, Math.floor(Math.log10(max / 3)));
    var step = [1, 2, 2.5, 5, 10].map(function (k) { return k * mag; }).filter(function (s) { return max / s <= 4; })[0];
    var top = Math.ceil(max / step) * step;
    var W = 300, H = 160, L = 46, R = 8, T = 8, B = 22, pw = W - L - R, ph = H - T - B;
    var X = function (i) { return L + pw * i / years; }, Y = function (v) { return T + ph * (1 - v / top); };
    var svg = '<svg class="calc-chart" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + (en ? 'Illustrated growth compared with money paid in' : 'Ilustrasi pertumbuhan berbanding wang yang dimasukkan') + '">';
    for (var v = 0; v <= top + 1e-9; v += step) {
      svg += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" stroke="rgba(255,255,255,.14)"/>' +
        '<text x="' + (L - 6) + '" y="' + (Y(v) + 3.5).toFixed(1) + '" text-anchor="end">' + rmShort(v) + '</text>';
    }
    [0, Math.round(years / 2), years].filter(function (a, i, all) { return all.indexOf(a) === i; }).forEach(function (a) {
      svg += '<text x="' + X(a).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="' + (a === 0 ? 'start' : a === years ? 'end' : 'middle') + '">' + (en ? 'Year ' : 'Tahun ') + a + '</text>';
    });
    lines.forEach(function (l) {
      svg += '<polyline fill="none" stroke="' + l.color + '" stroke-width="2.4" stroke-linejoin="round"' + (l.dash ? ' stroke-dasharray="' + l.dash + '"' : '') +
        ' points="' + l.vals.map(function (v, i) { return X(i).toFixed(1) + ',' + Y(v).toFixed(1); }).join(' ') + '"/>';
    });
    return svg + '</svg><dl>' + lines.slice().reverse().map(function (l) { return row(l.color, l.label, rm(l.vals[years])); }).join('') + '</dl>';
  }

  function renderCompound() {
    var en = isEn(), start = num('ccStart'), monthly = num('ccMonthly'), pct = num('ccRate');
    var years = Math.min(Math.round(num('ccYears')), 60);
    var total = growthPath(start, monthly, pct, years)[years];
    var paid = start + monthly * 12 * years, paidPct = total > paid ? paid / total * 100 : 100;
    $('ccResult').innerHTML = bigOut(en ? 'Illustrated value after ' + years + ' years' : 'Nilai ilustrasi selepas ' + years + ' tahun', rm(total)) +
      '<div class="split"><span class="a" style="width:' + paidPct + '%"></span><span class="b" style="width:' + (100 - paidPct) + '%"></span></div>' +
      '<dl>' + row('#FFFFFF', en ? 'Your money in' : 'Wang anda masuk', rm(paid)) + row('var(--accent)', en ? 'Growth' : 'Pertumbuhan', rm(Math.max(total - paid, 0))) + '</dl>' +
      minNote(monthly) + growthChart(start, monthly, pct, years);
    $('ccFine').textContent = fine(pct, ' Dikompaun setiap tahun, dan tambahan setahun dikira pada hujung tahun.', ' Compounded yearly, with each year’s top-ups counted at the end of that year.');
    setCta('ccCta',
      'UNIT TRUST - Hai Ika, saya baru guna kalkulator di website dan nak bincang.\nJumlah permulaan: ' + rm(start) + '\nTambahan bulanan: ' + rm(monthly) + '\nTempoh: ' + years + ' tahun',
      'UNIT TRUST - Hi Ika, I used the calculator on the website and would like to discuss.\nStarting amount: ' + rm(start) + '\nMonthly top-up: ' + rm(monthly) + '\nYears: ' + years);
  }

  // Emergency fund, the user's method: 3 months of salary (minimum) to 6 months (maximum), with an ideal of essential
  // expenses + 20% for 6 months kept within that range. Suggested saving: 20% of salary, at most half of what is left.
  var efEdited = false, efPick = 'ideal';
  function renderEf() {
    var en = isEn(), sal = num('efSalary'), need = num('efNeeds'), have = num('efHave'), left = sal - need;
    var suggest = Math.max(Math.floor(Math.min(sal * 0.2, left * 0.5) / 10) * 10, 0);
    if (!efEdited) $('efMonthly').value = suggest || '';
    var monthly = num('efMonthly');
    $('efMonthlyHint').textContent = suggest ? (en ? 'Suggested: ' + rm(suggest) + ' (you can change it)' : 'Cadangan: ' + rm(suggest) + ' (boleh ubah)') : '';
    var span = function (target) {
      var gap = target - have;
      if (gap <= 0) return en ? 'Already reached' : 'Dah capai';
      if (!monthly) return '–';
      var m = Math.ceil(gap / monthly), y = Math.floor(m / 12), r = m % 12;
      return (en ? 'in ' : 'dalam ') + (y ? unit(y, ' year', ' years', ' tahun') + (r ? ' ' : '') : '') + (r || !y ? unit(r || m, ' month', ' months', ' bulan') : '');
    };
    var html;
    if (!sal) {
      html = note(en ? 'Enter your monthly salary.' : 'Isi gaji bulanan anda.');
    } else {
      var goals = {
        min: { label: en ? 'Minimum · 3 months of salary' : 'Minimum · 3 bulan gaji', amt: sal * 3 },
        ideal: { label: 'Ideal', amt: Math.min(Math.max(need * 1.2 * 6, sal * 3), sal * 6) },
        max: { label: en ? 'Maximum · 6 months of salary' : 'Maksimum · 6 bulan gaji', amt: sal * 6 }
      };
      var goal = function (key) {
        var g = goals[key], on = key === efPick;
        return '<button type="button" class="ef-goal' + (on ? ' on' : '') + '" data-goal="' + key + '" aria-pressed="' + on + '"><small>' + g.label + '</small><b>' + rm(g.amt) + '</b><span>' + span(g.amt) + '</span></button>';
      };
      var aim = goals[efPick].amt, bank = Math.min(Math.max(aim / 3, sal), 6000, aim);
      html = '<div class="ef-goals">' + goal('min') + goal('ideal') + goal('max') + '</div>' +
        (left <= 0 ? note(en ? 'Your essential expenses are equal to or above your salary. Reduce commitments first, then start building this fund.' : 'Perbelanjaan wajib anda sama atau melebihi gaji. Kurangkan komitmen dulu, kemudian mula bina dana ini.', true) : '') +
        note(en ? 'Where to keep ' + rm(aim) + ' (tap an amount above to change):' : 'Cara simpan ' + rm(aim) + ' (tekan jumlah di atas untuk tukar):') + '<dl>' +
        ($('efCard').checked
          ? row('var(--accent)', en ? 'ASB or another fixed-value saving (100%, your credit card covers the first days)' : 'ASB atau simpanan nilai tetap lain (100%, kad kredit tampung hari-hari awal)', rm(aim))
          : row('#FFFFFF', en ? 'Bank account (1/3 or 1 month of salary, up to RM6,000)' : 'Akaun bank (1/3 atau 1 bulan gaji, sehingga RM6,000)', rm(bank)) +
            row('var(--accent)', en ? 'ASB or another fixed-value saving (the rest)' : 'ASB atau simpanan nilai tetap lain (selebihnya)', rm(aim - bank))) + '</dl>';
    }
    $('efResult').innerHTML = html;
    $('efFine').textContent = en
      ? 'General guide only. Keep this fund somewhere with a fixed value that you can withdraw quickly. ASB is open to Bumiputera only.'
      : 'Panduan umum sahaja. Simpan dana ini di tempat yang nilainya tetap dan mudah dikeluarkan. ASB hanya untuk Bumiputera.';
    setCta('efCta',
      'Hai Ika, saya baru kira dana kecemasan di website dan nak tahu lebih lanjut.',
      'Hi Ika, I worked out my emergency fund on the website and would like to know more.');
  }

  // TVM, monthly compounding, investing at the end of each month: FV = PV*g + PMT*(g-1)/r with g = (1+r)^n
  var tvmMode = 'fv';
  function renderTvm() {
    var en = isEn();
    box.querySelectorAll('[data-panel="tv"] [data-need]').forEach(function (l) {
      l.hidden = l.getAttribute('data-need').split(' ').indexOf(tvmMode) === -1;
    });
    var pv = num('tvPv'), pmt = num('tvPmt'), fv = num('tvFv'), pct = num('tvRate'), r = pct / 100 / 12;
    var years = Math.min(Math.round(num('tvYears')), 60), n = years * 12, q = 1 + r;
    var grow = function (m) { return Math.pow(q, m); };
    var annuity = function (m) { return r > 1e-12 ? (Math.pow(q, m) - 1) / r : m; };
    var run = function (a, b, m) { return { value: a * grow(m) + b * annuity(m), paid: a + b * m }; };
    var breakdown = function (x) {
      return row('#FFFFFF', en ? 'Your money in' : 'Wang anda masuk', rm(x.paid)) + row('var(--accent)', en ? 'Growth' : 'Pertumbuhan', rm(Math.max(x.value - x.paid, 0)));
    };
    var yrs = en ? ' years' : ' tahun', perMonth = en ? ' / month' : ' / bulan';
    var big, rows = '', msg = '', low = 0;
    if (tvmMode === 'fv') {
      var a = run(pv, pmt, n);
      big = bigOut(en ? 'Illustrated value after ' + years + yrs : 'Nilai ilustrasi selepas ' + years + yrs, rm(a.value));
      rows = breakdown(a);
      low = pmt;
    } else if (tvmMode === 'pmt') {
      var needed = n ? (fv - pv * grow(n)) / annuity(n) : 0;
      big = bigOut(en ? 'Invest every month for ' + years + yrs : 'Labur setiap bulan selama ' + years + yrs, rm(Math.max(needed, 0)) + perMonth);
      if (needed <= 0) msg = en ? 'In this illustration, your lump sum alone reaches the target.' : 'Dalam ilustrasi ini, jumlah sekali anda sahaja sudah mencapai sasaran.';
      else { rows = breakdown(run(pv, needed, n)); low = needed; }
    } else if (tvmMode === 'pv') {
      var needPv = n ? (fv - pmt * annuity(n)) / grow(n) : 0;
      big = bigOut(en ? 'Invest now, once' : 'Labur sekarang, sekali', rm(Math.max(needPv, 0)));
      if (needPv <= 0) msg = en ? 'In this illustration, your monthly investment alone reaches the target.' : 'Dalam ilustrasi ini, pelaburan bulanan anda sahaja sudah mencapai sasaran.';
      else rows = breakdown(run(needPv, pmt, n));
      low = pmt;
    } else {
      var months = null;
      if (fv <= pv) months = 0;
      else if (r > 1e-12) {
        var ratio = (fv * r + pmt) / (pv * r + pmt), m = ratio > 0 ? Math.log(ratio) / Math.log(q) : NaN;
        if (isFinite(m) && m >= 0) months = Math.ceil(m);
      }
      var span = months === null ? '–' : months > 1200 ? (en ? '100+ years' : '100+ tahun')
        : unit(Math.floor(months / 12), ' year', ' years', ' tahun') + (months % 12 ? ' ' + unit(months % 12, ' month', ' months', ' bulan') : '');
      big = bigOut(en ? 'Time to reach your target' : 'Masa untuk capai sasaran', span);
      if (months === null) msg = en ? 'Enter a lump sum or a monthly investment.' : 'Isi jumlah sekali atau pelaburan bulanan.';
      else if (months <= 1200) rows = breakdown(run(pv, pmt, months));
      low = pmt;
    }
    $('tvResult').innerHTML = big + (rows ? '<dl>' + rows + '</dl>' : '') + (msg ? note(msg) : '') + minNote(low);
    $('tvFine').textContent = fine(pct);
    setCta('tvCta',
      'UNIT TRUST - Hai Ika, saya baru guna kalkulator TVM di website dan nak bincang.\nSasaran: ' + rm(fv) + '\nJumlah sekali: ' + rm(pv) + '\nBulanan: ' + rm(pmt) + '\nTempoh: ' + years + ' tahun',
      'UNIT TRUST - Hi Ika, I used the TVM calculator on the website and would like to discuss.\nTarget: ' + rm(fv) + '\nLump sum: ' + rm(pv) + '\nMonthly: ' + rm(pmt) + '\nYears: ' + years);
  }

  // €PF Basic Savings in Akaun Persaraan by age, effective 1 Jan 2026 (ages 18 to 55)
  var BASIC = [900, 1100, 1500, 1900, 4000, 6200, 8500, 11000, 13700, 16600, 19600, 22900, 26300, 30000, 33900,
    38100, 42400, 47000, 51900, 57000, 62400, 68100, 74000, 80200, 86700, 93600, 100000, 108000, 115000, 124000,
    132000, 141000, 150000, 160000, 170000, 181000, 192000, 203000];

  function renderEp() {
    var en = isEn(), age = Math.floor(num('epAge')), bal = num('epBal'), html;
    if (age < 18) {
      html = note(en ? 'Enter an age of 18 or above.' : 'Masukkan umur 18 tahun ke atas.', true);
    } else if (age >= 55) {
      html = note(en
        ? 'At 55 and above, the Members Investment Scheme no longer applies. WhatsApp us to check your options.'
        : 'Pada umur 55 tahun ke atas, Skim Pelaburan Ahli tidak lagi terpakai. WhatsApp kami untuk semak pilihan anda.', true);
    } else {
      var basic = BASIC[age - 18], excess = Math.max(bal - basic, 0), can = excess * 0.3, ok = can >= 1000;
      var msg = ok
        ? (en ? 'You are eligible. The minimum investment is RM1,000.' : 'Anda layak. Pelaburan minimum ialah RM1,000.')
        : excess <= 0
          ? (en ? 'Your balance has not passed the Basic Savings for age ' + age + ' (' + rm(basic) + ') yet, so you can’t invest from €PF for now.'
                : 'Baki anda belum melebihi Simpanan Asas umur ' + age + ' (' + rm(basic) + '), jadi belum boleh melabur dari KW$P buat masa ini.')
          : (en ? 'Below the RM1,000 minimum. Your balance needs to be at least ' + rm(basic + 1000 / 0.3) + ' to qualify.'
                : 'Kurang daripada minimum RM1,000. Baki anda perlu sekurang-kurangnya ' + rm(basic + 1000 / 0.3) + ' untuk layak.');
      html = bigOut(en ? 'You can invest up to' : 'Anda boleh labur sehingga', rm(ok ? can : 0)) +
        '<dl>' + row('#FFFFFF', en ? 'Basic Savings (age ' + age + ')' : 'Simpanan Asas (umur ' + age + ')', rm(basic)) +
        row('rgba(255,255,255,.35)', en ? 'Amount above Basic Savings' : 'Jumlah melebihi Simpanan Asas', rm(excess)) +
        row('var(--accent)', en ? '30% of that amount' : '30% daripada jumlah itu', rm(can)) + '</dl>' + note(msg, !ok);
    }
    $('epResult').innerHTML = html;
    $('epFine').textContent = en
      ? 'Based on the €PF Basic Savings table effective 1 January 2026. Minimum investment RM1,000; you must be below 55. Check your exact eligible amount in the KW$P app or i-Akaun. Investing involves risk.'
      : 'Berdasarkan jadual Simpanan Asas KW$P berkuat kuasa 1 Januari 2026. Pelaburan minimum RM1,000; anda mesti berumur bawah 55 tahun. Semak jumlah layak sebenar dalam aplikasi KW$P atau i-Akaun. Pelaburan melibatkan risiko.';
    setCta('epCta',
      'Hai Ika, saya baru guna kalkulator Akaun Persaraan di website dan nak bincang.\nUmur: ' + age + '\nBaki Akaun Persaraan: ' + rm(bal),
      'Hi Ika, I used the Akaun Persaraan calculator on the website and would like to discuss.\nAge: ' + age + '\nAkaun Persaraan balance: ' + rm(bal));
  }

  function render() { renderEf(); renderCompound(); renderTvm(); renderEp(); }

  box.addEventListener('input', function (e) {
    if (e.target.id === 'efMonthly') efEdited = true;
    render();
  });
  $('efMonthly').addEventListener('blur', function () { if (this.value === '') { efEdited = false; render(); } });
  box.addEventListener('click', function (e) {
    var goal = e.target.closest('[data-goal]');
    if (goal) { efPick = goal.getAttribute('data-goal'); render(); return; }
    var seg = e.target.closest('[data-tvm]');
    if (seg) {
      tvmMode = seg.dataset.tvm;
      box.querySelectorAll('[data-tvm]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === seg)); });
      render();
      return;
    }
    var tab = e.target.closest('[data-calc]');
    if (tab) {
      box.querySelectorAll('[data-calc]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === tab)); });
      box.querySelectorAll('[data-panel]').forEach(function (p) { p.hidden = p.dataset.panel !== tab.dataset.calc; });
    }
  });
  document.addEventListener('mw:lang', render);
  render();
})();
