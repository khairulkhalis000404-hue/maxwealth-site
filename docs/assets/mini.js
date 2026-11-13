// MaxWealth home: quick growth illustration in the hero. Same method and wording as the compound
// calculator in calc.js (yearly compounding, a year's top-ups counted at the end of that year).
(function () {
  var st = document.getElementById('miStart'), m = document.getElementById('miMonthly'), y = document.getElementById('miYears'), r = document.getElementById('miRate');
  var out = document.getElementById('miOut'), fine = document.getElementById('miFine');
  if (!m || !out) return;
  var num = function (el) { var v = parseFloat(el.value); return isFinite(v) && v > 0 ? v : 0; };
  var rm = function (v) { return 'RM' + Math.round(v).toLocaleString('en-MY'); };
  function render() {
    var en = document.documentElement.lang === 'en';
    var start = st ? num(st) : 0, monthly = num(m), years = Math.min(Math.round(num(y)), 60), pct = num(r), total = start;
    for (var i = 0; i < years; i++) total = total * (1 + pct / 100) + monthly * 12;
    var paid = start + monthly * 12 * years, paidPct = total > paid ? paid / total * 100 : 100;
    out.innerHTML =
      '<small>' + (en ? 'Illustrated value after ' + years + ' years' : 'Nilai ilustrasi selepas ' + years + ' tahun') + '</small>' +
      '<b>' + rm(total) + '</b>' +
      '<div class="mini-bar" aria-hidden="true"><i style="width:' + paidPct + '%"></i></div>' +
      '<span>' + (en ? 'Your capital: ' : 'Modal anda: ') + rm(paid) + '</span>' +
      (start > 0 && start < 200
        ? '<p class="mini-warn">' + (en ? 'The minimum initial investment is RM200 for individuals.' : 'Minimum pelaburan permulaan ialah RM200 bagi individu.') + '</p>'
        : '') +
      (monthly > 0 && monthly < 100
        ? '<p class="mini-warn">' + (en ? 'The minimum monthly investment with us is RM100.' : 'Minimum pelaburan bulanan dengan kami ialah RM100.') + '</p>'
        : '');
    fine.textContent = en
      ? 'Illustration assuming ' + pct + '% a year, not a projection of returns. Actual returns vary and are not guaranteed. Investing involves risk.'
      : 'Ilustrasi andaian ' + pct + '% setahun, bukan unjuran pulangan. Pulangan sebenar berubah-ubah dan tidak dijamin. Pelaburan melibatkan risiko.';
  }
  [st, m, y, r].forEach(function (el) { if (el) el.addEventListener('input', render); });
  new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  render();
  var go = document.getElementById('miGo');
  if (go) go.addEventListener('click', function () { setTimeout(function () { m.focus({ preventScroll: true }); m.select(); }, 400); });
})();
