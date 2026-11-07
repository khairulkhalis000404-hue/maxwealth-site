#!/usr/bin/env python3
"""Builds the MaxWealth Consultancy website into ../docs/ (GitHub Pages publishes main /docs).

Every page shares one head, header and footer from this file, so edit copy here and re-run:
    python3 tools/build.py

Bilingual: BM is written into the HTML; English goes in data-en / data-en-<attr> and site.js swaps it.
Photos: drop a JPG into docs/assets/photos/<slot>.jpg (slots: home, about, careers) and rebuild;
until then each slot shows the MaxWealth brand panel.
"""
import hashlib
import html
import os
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', 'docs'))  # GitHub Pages serves main /docs
DOMAIN = 'https://maxwealthconsultancy.com.my'
UPDATED = '2026-11-08'
WA_NUMBER = '60194024401'
REGISTER_URL = ('https://client.asia.manulifeam.com/en_MY/NewUser?invitation_url=8e4d7c50-fed4-11f0-ac63-'
                'b9c251055f4f_rzk7z4m3gtsdl1wj7tla9m59yzqxze2cxwgtpcqwrmxqqkbqyejemhy83v7sriho.1769884932245')
PERSONAL = 'https://khairulkhalis.com'
CHANNEL = 'https://whatsapp.com/channel/0029Vb6tZx5ADTOEl9TRTX2B'
EMAIL = 'khairulkhalis@manulifeinvestment.com.my'


def file_version(name):
    # Asset URLs carry a hash of the file, so browsers fetch the new copy after every change
    with open(os.path.join(SITE, 'assets', name), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


CSS_V = file_version('site.css')
JS_V = file_version('site.js')


def esc(s):
    return html.escape(s, quote=True)


def t(tag, ms, en, a=''):
    """Bilingual element: BM inside, English in data-en."""
    a = (' ' + a) if a else ''
    return f'<{tag}{a} data-en="{esc(en)}">{ms}</{tag}>'


def wa_url(text):
    return f'https://wa.me/{WA_NUMBER}?text={quote(text, safe="")}'


def wa(ms, en):
    """href + English href for a prefilled WhatsApp message to Ika."""
    return f'href="{esc(wa_url(ms))}" data-en-href="{esc(wa_url(en))}" target="_blank" rel="noopener"'


# ---------- Icons (stroke icons share one style) ----------
def svg(body, fill=False):
    if fill:
        return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{body}</svg>'
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


I = {
    'ut': svg('<ellipse cx="12" cy="13.5" rx="6.5" ry="2.3"/><path d="M5.5 13.5v3c0 1.3 2.9 2.3 6.5 2.3s6.5-1 6.5-2.3v-3"/><path d="M5.5 16.5v3c0 1.3 2.9 2.3 6.5 2.3s6.5-1 6.5-2.3v-3"/><path d="M12 13.5V6.5"/><path d="M12 9C12 6.6 10.3 5 7.7 5c0 2.4 1.7 4 4.3 4z"/>'),
    'prs': svg('<rect x="6.5" y="3" width="11" height="3.2" rx="1"/><path d="M8 6.2v1.6C6.2 8.9 5 10.6 5 12.8V18a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3v-5.2c0-2.2-1.2-3.9-3-5V6.2"/><circle cx="12" cy="15" r="2.8"/><path d="M12 13.9v2.2"/>'),
    'corp': svg('<path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16"/><path d="M16 9h2a2 2 0 0 1 2 2v10"/><path d="M3 21h18M8 7h4M8 11h4M8 15h4"/>'),
    'review': svg('<path d="M12 3v9l7.5 4.5"/><circle cx="12" cy="12" r="9"/>'),
    'shield': svg('<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M8.8 12.2l2.2 2.2 4.4-4.6"/>'),
    'people': svg('<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.8"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M15 14.2A5 5 0 0 1 21.5 19"/>'),
    'phone': svg('<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>'),
    'doc': svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
    'calc': svg('<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18.5h8"/>'),
    'book': svg('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7"/>'),
    'megaphone': svg('<path d="M3 11l15-6v14L3 13z"/><path d="M7 13v4a2 2 0 0 0 4 0v-3"/><path d="M21 9v4"/>'),
    'mail': svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
    'user-plus': svg('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>'),
    'globe': svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
    'chat': svg('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.9A8 8 0 1 1 21 12z"/>'),
    'check': svg('<circle cx="12" cy="12" r="9"/><path d="M8.5 12.3l2.3 2.3 4.7-4.9"/>'),
    'arrow': svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    'out': svg('<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    'bars': '<svg class="bars" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    'x': '<svg class="x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    'wa': svg('<path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-.9 1.2-.3.2-.6.1a8 8 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.4 13.4 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.2-.3-.3-.6-.4zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.9L.1 24l6.3-1.6A11.8 11.8 0 0 0 24 12.2a11.7 11.7 0 0 0-3.6-8.6z"/>', fill=True),
    'tiktok': svg('<path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-1.8-2.5V9.7a5.7 5.7 0 1 0 4.9 5.7V9.1a7.3 7.3 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/>', fill=True),
}

NAV = [
    ('/', 'Utama', 'Home'),
    ('/tentang/', 'Tentang', 'About'),
    ('/servis/', 'Servis', 'Services'),
    ('/kerjaya/', 'Kerjaya', 'Careers'),
    ('/sumber/', 'Sumber', 'Resources'),
    ('/faq/', 'FAQ', 'FAQ'),
    ('/hubungi/', 'Hubungi', 'Contact'),
]
LEGAL = [
    ('/privasi/', 'Notis Privasi', 'Privacy Notice'),
    ('/penafian/', 'Penafian', 'Disclaimer'),
    ('/terma/', 'Terma Penggunaan', 'Terms of Use'),
]

WA_GENERAL = ('Hai Ika, saya jumpa MaxWealth Consultancy melalui website. Saya nak tahu lebih lanjut.',
              'Hi Ika, I found MaxWealth Consultancy through the website. I would like to know more.')


def wa_btn(ms_label, en_label, msg=WA_GENERAL, cls='btn'):
    return f'<a class="{cls}" {wa(*msg)}>{I["wa"]}{t("span", ms_label, en_label)}</a>'


def to_ika():
    return t('p', 'Mesej anda akan dihantar kepada Ika (Admin) di WhatsApp.',
             'Your message goes to Ika (Admin) on WhatsApp.', 'class="to-ika"')


def photo(slot, ms_caption, en_caption, ms_sub, en_sub, wide=False, alt='Khairul Khalis', card=True):
    """Photo slot: uses assets/photos/<slot>.jpg when present, else the brand panel."""
    cls = 'panel wide' if wide else 'panel'
    path = os.path.join(SITE, 'assets', 'photos', f'{slot}.jpg')
    if os.path.exists(path):
        cls += ' has-photo'
        inner = f'<img class="photo" src="/assets/photos/{slot}.jpg" alt="{esc(alt)}"{'' if slot == 'home' else ' loading="lazy"'}>'
    else:
        inner = '<img class="mark" src="/assets/maxwealth-mark.png" alt="" width="252" height="241">'
    if not card:
        return f'<div class="{cls}" data-photo-slot="{slot}">{inner}</div>'
    return (f'<div class="{cls}" data-photo-slot="{slot}">{inner}'
            f'<div class="float"><span class="ic-round">{I["shield"]}</span><div>'
            f'{t("b", ms_caption, en_caption)}{t("span", ms_sub, en_sub)}</div></div></div>')


# Rotating "Tahukah anda?" card on the home page (user, 8 Nov 2026). Facts only: no return promises;
# return illustrations use 8–10% a year with a disclaimer (user's rule), KW$P rules apply. Keep each one short enough for ~4 lines on a phone.
FACTS = [
    ('<b>Peraturan 72:</b> bahagikan 72 dengan kadar pulangan setahun untuk anggar berapa tahun wang berganda. Pada 8% setahun, lebih kurang 9 tahun; pada 10%, lebih kurang 7 tahun.<small>Contoh pengiraan sahaja, bukan unjuran pulangan. Pulangan sebenar berubah-ubah dan tidak dijamin.</small>',
     '<b>The Rule of 72:</b> divide 72 by a yearly rate of return to estimate how many years money takes to double. At 8% a year, about 9 years; at 10%, about 7 years.<small>Example calculation only, not a projection of returns. Actual returns vary and are not guaranteed.</small>'),
    ('Dengan inflasi 3% setahun, kuasa beli RM100 hari ini tinggal kira-kira <b>RM55</b> selepas 20 tahun.',
     'With 3% yearly inflation, RM100 today buys only about <b>RM55</b> worth after 20 years.'),
    ('Unit trust pertama di Malaysia dilancarkan pada <b>1959</b> oleh Malayan Unit Trust Ltd.',
     'Malaysia’s first unit trust was launched in <b>1959</b> by Malayan Unit Trust Ltd.'),
    ('Dana pelaburan kolektif pertama dunia dipercayai ditubuhkan di Belanda pada <b>1774</b>.',
     'The world’s first pooled investment fund is believed to have been set up in the Netherlands in <b>1774</b>.'),
    ('Skim Persaraan Swasta (PRS) mula diperkenalkan di Malaysia pada <b>2012</b>.',
     'The Private Retirement Scheme (PRS) was introduced in Malaysia in <b>2012</b>.'),
    ('Caruman PRS layak pelepasan cukai sehingga <b>RM3,000 setahun</b>, tertakluk syarat LHDN.',
     'PRS contributions qualify for tax relief of up to <b>RM3,000 a year</b>, subject to LHDN rules.'),
    ('“Faedah kompaun ialah keajaiban dunia kelapan” sering dikaitkan dengan Einstein, tapi <b>tiada bukti</b> beliau pernah menyebutnya.',
     '“Compound interest is the eighth wonder of the world” is often credited to Einstein, but there is <b>no evidence</b> he ever said it.'),
    ('RM100 sebulan selama 30 tahun boleh jadi lebih kurang <b>RM149,000</b>, berbanding RM59,000 jika 20 tahun. Masa memainkan peranan besar.<small>Ilustrasi andaian 8% setahun dikompaun bulanan, bukan unjuran pulangan. Pulangan sebenar berubah-ubah dan tidak dijamin.</small>',
     'RM100 a month for 30 years could grow to about <b>RM149,000</b>, against RM59,000 over 20 years. Time plays a big part.<small>Illustration at an assumed 8% a year compounded monthly, not a projection of returns. Actual returns vary and are not guaranteed.</small>'),
    ('Wang kertas pertama dunia digunakan di China pada zaman <b>Dinasti Song</b>, kira-kira abad ke-11.',
     'The world’s first paper money was used in China during the <b>Song dynasty</b>, around the 11th century.'),
    ('Perkataan <b>“ringgit”</b> bermaksud “bergerigi”, merujuk tepi bergerigi syiling perak Sepanyol yang pernah digunakan di Tanah Melayu.',
     'The word <b>“ringgit”</b> means “jagged”, after the serrated edges of Spanish silver coins once used in Malaya.'),
    ('Bank Negara Malaysia mula mengeluarkan mata wang Malaysia sendiri pada <b>12 Jun 1967</b>.',
     'Bank Negara Malaysia began issuing Malaysia’s own currency on <b>12 June 1967</b>.'),
    ('Sejak <b>1 April 2008</b>, jumlah bil yang dibayar tunai di Malaysia dibundarkan ke 5 sen terdekat.',
     'Since <b>1 April 2008</b>, bill totals paid in cash in Malaysia are rounded to the nearest 5 sen.'),
    ('Caj kewangan kad kredit di Malaysia boleh mencecah <b>18% setahun</b> ke atas baki yang tidak dijelaskan.',
     'Credit card finance charges in Malaysia can reach <b>18% a year</b> on unpaid balances.'),
    ('Bursa saham moden tertua dunia bermula di <b>Amsterdam pada 1602</b>, dengan saham Syarikat Hindia Timur Belanda.',
     'The world’s oldest modern stock exchange began in <b>Amsterdam in 1602</b>, trading shares of the Dutch East India Company.'),
    ('Malayan Stock Exchange ditubuhkan pada <b>1960</b> dan menjadi asas kepada Bursa Malaysia hari ini.',
     'The Malayan Stock Exchange was set up in <b>1960</b> and is a forerunner of today’s Bursa Malaysia.'),
    ('Harga unit trust dikira <b>setiap hari bekerja</b> berdasarkan Nilai Aset Bersih (NAB) dana.',
     'Unit trust prices are calculated <b>every business day</b> from the fund’s Net Asset Value (NAV).'),
    ('Kad kredit moden pertama, <b>Diners Club</b>, diperkenalkan pada 1950 untuk membayar makan di restoran.',
     'The first modern credit card, <b>Diners Club</b>, was launched in 1950 for paying at restaurants.'),
    ('Mesin ATM pertama dunia dipasang di <b>London pada 1967</b>.',
     'The world’s first ATM was installed in <b>London in 1967</b>.'),
    ('<b>RM10 sehari = RM3,650 setahun.</b> Perbelanjaan kecil yang rutin cepat bertambah.',
     '<b>RM10 a day = RM3,650 a year.</b> Small daily spending adds up fast.'),
    ('Warren Buffett membeli saham pertamanya pada umur <b>11 tahun</b>.',
     'Warren Buffett bought his first shares at age <b>11</b>.'),
]


def fun_card():
    items = ''.join(
        f'<li{" class=\"on\"" if i == 0 else " aria-hidden=\"true\""} data-en="{esc(en)}">{ms}</li>'
        for i, (ms, en) in enumerate(FACTS))
    return f'''<aside class="fun" aria-label="Fakta kewangan" data-en-aria-label="Money facts">
  <div class="fun-head">
    {t("p", "Tahukah anda?", "Did you know?", 'class="eyebrow"')}
    <p class="fun-count"><span class="fun-num">01</span> / {len(FACTS):02d}</p>
  </div>
  <ul class="fun-list">{items}</ul>
  <div class="fun-foot">
    <span class="fun-bar" aria-hidden="true"><i></i></span>
    <button type="button" class="fun-btn" data-step="-1" aria-label="Fakta sebelum" data-en-aria-label="Previous fact"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
    <button type="button" class="fun-btn" data-step="1" aria-label="Fakta seterusnya" data-en-aria-label="Next fact"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
  </div>
</aside>'''


def more(ms, en):
    return f'<span class="more">{t("span", ms, en)}{I["arrow"]}</span>'


# ---------- Layout ----------
def head(path, title_ms, title_en, desc_ms, desc_en):
    url = DOMAIN + path
    # the 404 page must not be indexed or claim a canonical URL
    robots = ('<meta name="robots" content="noindex">' if path == '/404.html'
              else f'<link rel="canonical" href="{url}">')
    full_ms = title_ms if path == '/' else f'{title_ms} · MaxWealth Consultancy'
    full_en = title_en if path == '/' else f'{title_en} · MaxWealth Consultancy'
    return f'''<!doctype html>
<html lang="ms">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try{{if(localStorage.getItem('mwLang')==='en'){{var r=document.documentElement;r.lang='en';r.classList.add('lang-pending');setTimeout(function(){{r.classList.remove('lang-pending')}},1500)}}}}catch(e){{}}</script>
<style>.lang-pending body{{visibility:hidden}}</style>
<title data-en="{esc(full_en)}">{esc(full_ms)}</title>
<meta name="description" content="{esc(desc_ms)}" data-en-content="{esc(desc_en)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#FFFFFF">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="MaxWealth Consultancy">
<meta property="og:locale" content="ms_MY">
<meta property="og:locale:alternate" content="en_MY">
<meta property="og:title" content="{esc(full_ms)}">
<meta property="og:description" content="{esc(desc_ms)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/og-maxwealth.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="MaxWealth Consultancy, Inspiring Financial Excellence">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
<script defer src="/assets/site.js?v={JS_V}"></script>
</head>'''


def header(path):
    def cur(p):
        return ' aria-current="page"' if p == path else ''
    links = ''.join(f'<li><a href="{p}"{cur(p)}>{t("span", ms, en)}</a></li>' for p, ms, en in NAV)
    panel = ''.join(f'<li><a href="{p}"{cur(p)}>{t("span", ms, en)}{I["arrow"]}</a></li>' for p, ms, en in NAV)
    return f'''<body>
<a class="skip" href="#main" data-en="Skip to content">Langkau ke kandungan</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="MaxWealth Consultancy, laman utama" data-en-aria-label="MaxWealth Consultancy, home">
      <img src="/assets/maxwealth-logo.png" alt="MaxWealth Consultancy" width="800" height="241">
    </a>
    <nav class="nav" aria-label="Utama" data-en-aria-label="Main"><ul>{links}</ul></nav>
    <div class="head-tools">
      <div class="lang" role="group" aria-label="Bahasa" data-en-aria-label="Language">
        <button type="button" data-lang="ms" aria-pressed="true">BM</button>
        <button type="button" data-lang="en" aria-pressed="false">EN</button>
      </div>
      <a class="btn sm head-cta" {wa(*WA_GENERAL)}>{I["wa"]}<span>WhatsApp</span></a>
      <button type="button" class="menu-btn" aria-expanded="false" aria-controls="menu" aria-label="Menu">{I["bars"]}{I["x"]}</button>
    </div>
  </div>
  <div class="menu-panel" id="menu">
    <ul>{panel}</ul>
    {wa_btn("WhatsApp Admin kami", "WhatsApp our Admin")}
    {to_ika()}
  </div>
</header>
<main id="main">'''


def footer():
    nav = ''.join(f'<li><a href="{p}">{t("span", ms, en)}</a></li>' for p, ms, en in NAV[1:])
    legal = ''.join(f'<li><a href="{p}">{t("span", ms, en)}</a></li>' for p, ms, en in LEGAL)
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <a class="foot-logo" href="/"><img src="/assets/maxwealth-logo.png" alt="MaxWealth Consultancy, Inspiring Financial Excellence" width="800" height="241" loading="lazy"></a>
        {t("p", "Agensi unit trust dan PRS yang mewakili Manulife Investment Management (M) Berhad. Penerangan yang jelas, langkah yang teratur.", "A unit trust and PRS agency representing Manulife Investment Management (M) Berhad. Clear explanations, well-ordered steps.")}
        <div class="social">
          <a {wa(*WA_GENERAL)} aria-label="WhatsApp Admin">{I["wa"]}</a>
          <a href="mailto:{EMAIL}" aria-label="Emel" data-en-aria-label="Email">{I["mail"]}</a>
          <a href="{CHANNEL}" target="_blank" rel="noopener" aria-label="Saluran WhatsApp" data-en-aria-label="WhatsApp Channel">{I["megaphone"]}</a>
          <a href="https://www.tiktok.com/@kayspresso" target="_blank" rel="noopener" aria-label="TikTok">{I["tiktok"]}</a>
        </div>
      </div>
      <div>
        {t("h2", "Laman", "Pages")}
        <ul>{nav}</ul>
      </div>
      <div>
        {t("h2", "Sumber", "Resources")}
        <ul>
          <li><a href="/sumber/#panduan">{t("span", "Panduan langkah demi langkah", "Step-by-step guides")}</a></li>
          <li><a href="/sumber/#kalkulator">{t("span", "Kalkulator", "Calculators")}</a></li>
          <li><a href="/sumber/#ebook">Ebook</a></li>
          <li><a href="{REGISTER_URL}" target="_blank" rel="noopener">{t("span", "Daftar akaun online", "Open an account online")}</a></li>
        </ul>
      </div>
      <div>
        {t("h2", "Undang-undang", "Legal")}
        <ul>{legal}</ul>
      </div>
    </div>
    <div class="foot-legal">
      <p class="reg">{t("span", "Khairul Khalis, perunding unit trust (UTC) dan PRS berdaftar FIMM (F01065736). Mewakili Manulife Investment Management (M) Berhad melalui agensi MaxWealth Consultancy.", "Khairul Khalis, FIMM-registered unit trust (UTC) and PRS consultant (F01065736). Representing Manulife Investment Management (M) Berhad through MaxWealth Consultancy.")}
        <a href="https://www.fimm.com.my" target="_blank" rel="noopener" data-en="Verify at FIMM">Semak di FIMM</a></p>
      {t("p", "Pelaburan melibatkan risiko. Prestasi lalu bukan petunjuk prestasi masa depan. Harga unit dan agihan (jika ada) boleh naik dan turun. Sila baca dan fahami Prospektus / Disclosure Document dan Product Highlights Sheet (PHS) sebelum melabur. Laman ini untuk maklumat umum sahaja dan bukan tawaran atau ajakan untuk membeli atau menjual mana-mana produk pelaburan.", "Investing involves risk. Past performance is not indicative of future performance. Unit prices and distributions (if any) may go down as well as up. Please read and understand the Prospectus / Disclosure Document and Product Highlights Sheet (PHS) before investing. This site is for general information only and is not an offer or solicitation to buy or sell any investment product.")}
      <div class="foot-bottom">
        <span>© 2026 MaxWealth Consultancy (SSM {SSM})</span>
        <a href="/penafian/" data-en="Read the full disclaimer">Baca penafian penuh</a>
      </div>
    </div>
  </div>
</footer>
</body>
</html>
'''


PAGES = []


def relative(doc, path):
    """Site-internal links become relative, so pages also work under a sub-path such as
    username.github.io/repo/ before the custom domain is live. 404.html stays absolute (served at any depth)."""
    depth = path.strip('/').count('/') + 1 if path.strip('/') else 0
    prefix = '../' * depth or './'
    for attr in ('href', 'src'):
        doc = doc.replace(f'{attr}="/', f'{attr}="{prefix}').replace(f'{attr}=&quot;/', f'{attr}=&quot;{prefix}')
    return doc


def page(path, title_ms, title_en, desc_ms, desc_en, body, priority='0.8', sitemap=True):
    doc = head(path, title_ms, title_en, desc_ms, desc_en) + '\n' + header(path) + '\n' + body + '\n' + footer()
    if path != '/404.html':
        doc = relative(doc, path)
    out = os.path.join(SITE, '404.html') if path == '/404.html' else os.path.join(SITE, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    if sitemap:
        PAGES.append((path, priority))


def page_hero(eyebrow_ms, eyebrow_en, h_ms, h_en, lead_ms, lead_en, extra=''):
    return f'''<section class="page-hero"><div class="wrap">
  {t("p", eyebrow_ms, eyebrow_en, 'class="eyebrow"')}
  {t("h1", h_ms, h_en)}
  {t("p", lead_ms, lead_en, 'class="lead"')}
  {extra}
</div></section>'''


def band(h_ms, h_en, p_ms, p_en, msg=WA_GENERAL, btn=('WhatsApp Admin kami', 'WhatsApp our Admin')):
    return f'''<section class="section"><div class="wrap"><div class="band">
  <div>
    {t("p", "Mula di sini", "Start here", 'class="eyebrow"')}
    {t("h2", h_ms, h_en)}
    {t("p", p_ms, p_en)}
  </div>
  <div>
    {wa_btn(btn[0], btn[1], msg)}
    {to_ika()}
  </div>
</div></div></section>'''


STATS = f'''<div class="stats">
  <div class="stat"><b>6+</b>{t("span", "tahun dalam industri kewangan", "years in the finance industry")}</div>
  <div class="stat"><b>300+</b>{t("span", "pelabur dibantu", "investors served")}</div>
  <div class="stat"><b data-en="RM10m+">RM10 juta+</b>{t("span", "aset di bawah seliaan (AUM)", "assets under management (AUM)")}</div>
</div>
{t("p", "Angka peribadi Khairul Khalis, setakat 2026.", "Khairul Khalis's own figures, as of 2026.", 'class="stats-note"')}'''


SERVICES = [
    ('unit-trust', 'ut', 'Unit trust', 'Unit trusts',
     'Pelaburan sekali atau bulanan, dipilih ikut matlamat dan profil risiko anda.',
     'One-time or monthly investing, chosen to match your goals and risk profile.'),
    ('prs', 'prs', 'PRS (Skim Persaraan Swasta)', 'PRS (Private Retirement Scheme)',
     'Pelaburan persaraan jangka panjang secara sukarela, layak pelepasan cukai tahunan (tertakluk syarat LHDN).',
     'Voluntary long-term retirement investing, eligible for yearly tax relief (subject to LHDN rules).'),
    ('korporat', 'corp', 'Pelaburan korporat', 'Corporate investing',
     'Untuk lebihan tunai syarikat yang tidak diperlukan dalam masa terdekat.',
     'For company surplus cash that is not needed in the near term.'),
    ('semakan-portfolio', 'review', 'Semakan portfolio', 'Portfolio review',
     'Semak pelaburan sedia ada dan susun semula supaya selari dengan matlamat anda.',
     'Review your existing investments and realign them with your goals.'),
]


# ---------- Home ----------
def build_home():
    cards = ''.join(f'''<a class="card" href="/servis/#{sid}">
  <span class="ic-round">{I[ic]}</span>
  {t("h3", tms, ten)}
  {t("p", dms, den)}
  {more("Ketahui lanjut", "Learn more")}
</a>''' for sid, ic, tms, ten, dms, den in SERVICES)

    body = f'''<section class="hero"><div class="wrap hero-grid">
  <div>
    {t("p", "MaxWealth Consultancy", "MaxWealth Consultancy", 'class="eyebrow"')}
    {t("h1", 'Unit trust dan PRS, <em class="hl">diterangkan dengan jelas.</em>', 'Unit trusts and PRS, <em class="hl">explained clearly.</em>')}
    {t("p", "Kami agensi yang mewakili Manulife Investment Management (M) Berhad. Kami bantu individu, keluarga dan syarikat faham pilihan pelaburan mereka, dan mula dengan langkah yang sesuai dengan matlamat serta profil risiko masing-masing.", "We are an agency representing Manulife Investment Management (M) Berhad. We help individuals, families and companies understand their investment options, and start with steps that fit their goals and risk profile.", 'class="lead"')}
    <div class="btns">
      {wa_btn("WhatsApp Admin kami", "WhatsApp our Admin")}
      <a class="btn ghost" href="/servis/">{t("span", "Lihat servis", "See services")}</a>
    </div>
    {to_ika()}
  </div>
  {fun_card()}
</div></section>

<div class="wrap strip"><ul>
  <li><span class="ic-round">{I["shield"]}</span><div>{t("b", "Berdaftar FIMM", "FIMM-registered")}{t("span", "Perunding unit trust dan PRS berdaftar", "Registered unit trust and PRS consultants")}</div></li>
  <li><span class="ic-round">{I["phone"]}</span><div>{t("b", "Akaun dibuka online", "Accounts opened online")}{t("span", "Lebih kurang 10 minit, dengan panduan langkah", "About 10 minutes, with step-by-step guides")}</div></li>
  <li><span class="ic-round">{I["ut"]}</span><div>{t("b", "Mula dari RM100 sebulan", "From RM100 a month")}{t("span", "Pelaburan bulanan yang konsisten", "Consistent monthly investing")}</div></li>
</ul></div>

<section class="section"><div class="wrap">
  <div class="section-head">
    {t("p", "Kenapa melabur", "Why invest", 'class="eyebrow"')}
    {t("h2", "Wang yang dibiarkan pun berubah nilainya.", "Money left alone still changes in value.")}
  </div>
  <div class="facts">
    <div class="fact"><b>−45%</b>{t("p", "Dengan inflasi 3% setahun, RM1,000 hilang hampir separuh nilainya dalam 20 tahun, walaupun dibiarkan dalam akaun bank.", "With 3% inflation a year, RM1,000 loses almost half its value in 20 years, even when left in a bank account.")}{t("small", "Ilustrasi: RM1,000 ÷ 1.03²⁰ ≈ RM554.", "Illustration: RM1,000 ÷ 1.03²⁰ ≈ RM554.")}</div>
    <div class="fact"><b>RM100</b>{t("p", "sebulan sudah cukup untuk mula. Yang penting ialah konsisten dan tempoh yang panjang.", "a month is enough to start. What matters is consistency and time.")}</div>
    <div class="fact"><b>DCA</b>{t("p", "Jumlah tetap setiap bulan membeli lebih banyak unit bila harga rendah dan kurang bila harga tinggi, jadi kos purata lebih seimbang.", "A fixed amount every month buys more units when prices are low and fewer when they are high, which evens out your average cost.")}</div>
  </div>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head">
    {t("p", "Servis", "Services", 'class="eyebrow"')}
    {t("h2", "Apa yang kami bantu.", "How we can help.")}
    {t("p", "Setiap servis bermula dengan perbualan ringkas tentang matlamat anda, dan penerangan yang jelas tentang risiko serta caj sebelum anda membuat keputusan.", "Every service starts with a short conversation about your goals, and a clear explanation of the risks and charges before you decide.", 'class="lead"')}
  </div>
  <div class="grid c4">{cards}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head">
    {t("p", "Cara kami bekerja", "How we work", 'class="eyebrow"')}
    {t("h2", "Empat langkah, tanpa tergesa-gesa.", "Four steps, no rush.")}
  </div>
  <ol class="steps row">
    <li><div>{t("h3", "Berbual", "Talk")}{t("p", "Mesej Admin kami di WhatsApp. Kami aturkan perbualan atau temujanji ikut masa anda.", "Message our Admin on WhatsApp. We arrange a call or meeting at a time that suits you.")}</div></li>
    <li><div>{t("h3", "Faham matlamat", "Understand your goals")}{t("p", "Kita lihat matlamat, tempoh dan profil risiko anda melalui soal selidik profil risiko.", "We look at your goals, time frame and risk profile through a risk profiling questionnaire.")}</div></li>
    <li><div>{t("h3", "Pilih dan buka akaun", "Choose and open an account")}{t("p", "Kami terangkan pilihan dana, caj dan risiko. Akaun dibuka online dalam lebih kurang 10 minit.", "We explain the fund options, charges and risks. Your account is opened online in about 10 minutes.")}</div></li>
    <li><div>{t("h3", "Semakan berkala", "Regular reviews")}{t("p", "Kami semak portfolio anda dari semasa ke semasa dan kemas kini bila matlamat berubah.", "We review your portfolio from time to time and adjust when your goals change.")}</div></li>
  </ol>
</div></section>

<section class="section alt"><div class="wrap">
  <div style="max-width:680px">
    {t("p", "Pengasas MaxWealth", "MaxWealth founder", 'class="eyebrow"')}
    <h2 class="profile-name">Khairul Khalis</h2>
    <p class="titles"><b>Founder &amp; Agency Manager, MaxWealth Consultancy</b><br>{t("span", "Perunding unit trust (UTC) dan PRS berdaftar FIMM", "FIMM-registered unit trust (UTC) and PRS consultant")}</p>
    {STATS}
    <p style="margin-top:32px"><a class="text-link" href="/tentang/">{t("span", "Kenali agensi dan pasukan kami", "Meet the agency and our team")}{I["arrow"]}</a></p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="grid c2">
    <a class="card" href="/sumber/">
      <span class="ic-round">{I["doc"]}</span>
      {t("h3", "Panduan, kalkulator dan ebook", "Guides, calculators and ebooks")}
      {t("p", "Panduan langkah demi langkah untuk buka akaun, labur dan set pelan bulanan, dalam BM dan English.", "Step-by-step guides to open an account, invest and set up a monthly plan, in BM and English.")}
      {more("Buka sumber", "Open resources")}
    </a>
    <a class="card" href="/kerjaya/">
      <span class="ic-round">{I["people"]}</span>
      {t("h3", "Berminat jadi perunding unit trust?", "Interested in becoming a unit trust consultant?")}
      {t("p", "Ketahui proses peperiksaan dan pendaftaran FIMM, latihan, dan cara kerjaya ini berfungsi.", "Learn about the FIMM exam and registration, training, and how this career works.")}
      {more("Lihat kerjaya", "See careers")}
    </a>
  </div>
</div></section>

{band("Ada soalan? Mula dengan satu mesej.", "Have a question? Start with one message.", "Tiada komitmen. Ceritakan matlamat anda, dan kami terangkan pilihan yang ada dengan jelas.", "No commitment. Tell us your goals, and we will explain the options clearly.")}'''
    page('/', 'MaxWealth Consultancy · Unit trust & PRS', 'MaxWealth Consultancy · Unit trusts & PRS',
         'MaxWealth Consultancy, agensi unit trust dan PRS yang mewakili Manulife Investment Management (M) Berhad. Perunding berdaftar FIMM, penerangan yang jelas, mula dari RM100 sebulan.',
         'MaxWealth Consultancy, a unit trust and PRS agency representing Manulife Investment Management (M) Berhad. FIMM-registered consultants, clear explanations, from RM100 a month.',
         body, priority='1.0')


# ---------- About ----------
def build_about():
    values = [
        ('Jelas', 'Clear', 'Kami terangkan produk, caj dan risiko dalam bahasa yang mudah, sebelum anda membuat keputusan.', 'We explain products, charges and risks in plain language, before you decide.'),
        ('Jujur', 'Honest', 'Tiada janji pulangan. Kami bercakap tentang prestasi berbanding penanda aras, dalam tempoh yang dinyatakan.', 'No promised returns. We talk about performance against benchmarks, over stated periods.'),
        ('Konsisten', 'Consistent', 'Kami galakkan pelaburan berkala dan jangka panjang, bukan keputusan tergesa-gesa.', 'We encourage regular, long-term investing, not rushed decisions.'),
        ('Dekat', 'Close by', 'Admin kami membantu urusan akaun dan temujanji, dan perunding kami membuat semakan berkala.', 'Our Admin helps with accounts and appointments, and our consultants carry out regular reviews.'),
    ]
    vcards = ''.join(f'<div class="card">{t("h3", a, b)}{t("p", c, d)}</div>' for a, b, c, d in values)
    awards = [
        ('Champion, Top Regional Producer (Southern)', 'Champion, Top Regional Producer (Southern)', '2026'),
        ('Champion, iFUNDS Personal Sales (Top Regional)', 'Champion, iFUNDS Personal Sales (Top Regional)', '2026'),
        # UTEA explained in plain words: people outside Manulife don't know the title (user, 8 Nov 2026)
        ('1st Runner Up, Top UTEA<small>UTEA (Unit Trust Executive Advisor) ialah gelaran perunding unit trust di Manulife Investments.</small>',
         '1st Runner Up, Top UTEA<small>UTEA (Unit Trust Executive Advisor) is a unit trust consultant title at Manulife Investments.</small>', '2026'),
        ('Million Ringgit Producer', 'Million Ringgit Producer', '2026'),
        ('1st Runner Up, Manulife iFUNDS (Personal Sales) Top Regional Producer (Southern)', '1st Runner Up, Manulife iFUNDS (Personal Sales) Top Regional Producer (Southern)', 'MAC 2025'),
        ('Penceramah jemputan, “Game On! Carnival Boss Preview”', 'Guest speaker, “Game On! Carnival Boss Preview”', 'Sep 2026'),
    ]
    arows = ''.join(f'<li>{t("b", a, b)}<span>{y}</span></li>' for a, b, y in awards)
    body = f'''{page_hero("Tentang kami", "About us", "Agensi kecil, penerangan yang besar maknanya.", "A focused agency that explains things properly.", "MaxWealth Consultancy ialah agensi unit trust dan PRS yang mewakili Manulife Investment Management (M) Berhad. Tagline kami, Inspiring Financial Excellence, bermaksud satu perkara yang mudah: bantu orang faham wang mereka dan mula melabur dengan langkah yang teratur.", "MaxWealth Consultancy is a unit trust and PRS agency representing Manulife Investment Management (M) Berhad. Our tagline, Inspiring Financial Excellence, means something simple: help people understand their money and start investing in well-ordered steps.")}

<section class="section"><div class="wrap">
  <div class="section-head">
    {t("p", "Nilai kami", "What we value", 'class="eyebrow"')}
    {t("h2", "Cara kami berurusan dengan anda.", "How we work with you.")}
  </div>
  <div class="grid c4">{vcards}</div>
</div></section>

<section class="section alt"><div class="wrap split">
  {photo("about", "Khairul Khalis", "Khairul Khalis", "Founder & Agency Manager, MaxWealth Consultancy", "Founder & Agency Manager, MaxWealth Consultancy")}
  <div>
    {t("p", "Pengasas MaxWealth", "MaxWealth founder", 'class="eyebrow"')}
    <h2 class="profile-name">Khairul Khalis</h2>
    <p class="titles"><b>Founder &amp; Agency Manager, MaxWealth Consultancy</b><br>{t("span", "Perunding unit trust (UTC) dan PRS berdaftar FIMM · F01065736", "FIMM-registered unit trust (UTC) and PRS consultant · F01065736")}</p>
    {t("p", "Khairul mula dalam industri kewangan pada 2020 dan dalam unit trust sejak 2021. Beliau mengasaskan MaxWealth Consultancy dan kini, sebagai Agency Manager, membimbing pasukan perunding dan berkongsi pendidikan kewangan melalui ebook, panduan dan media sosial.", "Khairul started in the finance industry in 2020 and in unit trusts in 2021. He founded MaxWealth Consultancy and now, as Agency Manager, coaches a team of consultants and shares financial education through ebooks, guides and social media.", 'class="muted" style="margin-bottom:28px"')}
    {STATS}
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    {t("p", "Pengiktirafan", "Recognition", 'class="eyebrow"')}
    {t("h2", "Anugerah dan pengiktirafan.", "Awards and recognition.")}
    {t("p", "Anugerah Manulife Investments yang diterima oleh Khairul Khalis. Ia mencerminkan pencapaian peribadi beliau, bukan jaminan hasil untuk pelabur atau perunding lain.", "Manulife Investments awards received by Khairul Khalis. They reflect his own results, not an indication of outcomes for any investor or consultant.", 'class="muted" style="margin-top:16px"')}
  </div>
  <ul class="rows">{arows}</ul>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head">
    {t("p", "Pasukan", "Team", 'class="eyebrow"')}
    {t("h2", "Siapa yang anda akan berurusan.", "Who you will work with.")}
  </div>
  <div class="grid c3">
    <div class="card"><span class="ic-round">{I["shield"]}</span><h3>Khairul Khalis</h3>{t("p", "Founder &amp; Agency Manager. Membimbing pasukan dan menguruskan semakan portfolio pelanggan.", "Founder &amp; Agency Manager. Coaches the team and handles client portfolio reviews.")}</div>
    <div class="card"><span class="ic-round">{I["chat"]}</span><h3>Ika</h3>{t("p", "Admin. Titik hubungan pertama anda untuk soalan, temujanji dan urusan akaun di WhatsApp.", "Admin. Your first point of contact for questions, appointments and account matters on WhatsApp.")}</div>
    <div class="card"><span class="ic-round">{I["people"]}</span>{t("h3", "Perunding kami", "Our consultants")}{t("p", "Perunding unit trust dan PRS berdaftar FIMM di bawah agensi MaxWealth Consultancy.", "FIMM-registered unit trust and PRS consultants under the MaxWealth Consultancy agency.")}</div>
  </div>
  <div class="callout" style="margin-top:40px">
    <div>{t("h3", "Semak perunding anda", "Check your consultant")}{t("p", 'Setiap perunding unit trust dan PRS mesti berdaftar dengan FIMM. Anda boleh semak status pendaftaran di <a href="https://www.fimm.com.my" target="_blank" rel="noopener">laman FIMM</a>.', 'Every unit trust and PRS consultant must be registered with FIMM. You can check registration status on the <a href="https://www.fimm.com.my" target="_blank" rel="noopener">FIMM website</a>.')}</div>
  </div>
</div></section>

{band("Nak berbual dengan pasukan kami?", "Want to talk to our team?", "Hantar satu mesej. Ika akan bantu aturkan masa yang sesuai.", "Send one message. Ika will help arrange a suitable time.")}'''
    page('/tentang/', 'Tentang kami', 'About us',
         'Kenali MaxWealth Consultancy dan pengasasnya, Khairul Khalis, perunding unit trust dan PRS berdaftar FIMM.',
         'Meet MaxWealth Consultancy and its founder, Khairul Khalis, a FIMM-registered unit trust and PRS consultant.',
         body)


# ---------- Services ----------
def build_services():
    def ticks(items):
        return '<ul class="ticks">' + ''.join(f'<li>{I["check"]}{t("span", a, b)}</li>' for a, b in items) + '</ul>'

    detail = {
        'unit-trust': (
            'Unit trust mengumpul wang ramai pelabur ke dalam satu dana yang diurus oleh pengurus dana profesional, dan dilaburkan dalam saham, bon atau aset lain ikut objektif dana.',
            'A unit trust pools money from many investors into one fund run by a professional fund manager, invested in shares, bonds or other assets according to the fund’s objective.',
            [('Labur sekali (lump sum) atau bulanan melalui pelan pelaburan bulanan, dari RM100 sebulan', 'Invest a lump sum or monthly through a regular investment plan, from RM100 a month'),
             ('Pilihan dana patuh Shariah dan konvensional', 'Shariah-compliant and conventional fund options'),
             ('Dana dipilih ikut matlamat, tempoh dan profil risiko anda', 'Funds chosen to match your goals, time frame and risk profile'),
             ('Caj dan risiko diterangkan dengan jelas sebelum anda melabur', 'Charges and risks explained clearly before you invest')],
            ('UNIT TRUST - Hai Ika, saya nak tahu lebih tentang pelaburan unit trust.', 'UNIT TRUST - Hi Ika, I would like to know more about unit trust investing.')),
        'prs': (
            'Skim Persaraan Swasta (PRS) ialah skim sukarela untuk melabur bagi persaraan, sebagai tambahan kepada caruman wajib anda. Ia sesuai untuk pekerja makan gaji, pekerja sendiri dan suri rumah.',
            'The Private Retirement Scheme (PRS) is a voluntary scheme for investing towards retirement, on top of your mandatory contributions. It suits employees, the self-employed and homemakers.',
            [('Sumbangan sukarela, ikut kemampuan anda', 'Voluntary contributions, at your own pace'),
             ('Layak pelepasan cukai tahunan, tertakluk syarat LHDN', 'Eligible for yearly tax relief, subject to LHDN rules'),
             ('Pilihan dana ikut umur dan profil risiko', 'Fund options by age and risk profile'),
             ('Pengeluaran sebelum umur persaraan tertakluk syarat dan penalti cukai', 'Withdrawals before retirement age are subject to conditions and a tax penalty')],
            ('PRS - Hai Ika, saya nak tahu lebih tentang PRS dan pelepasan cukai.', 'PRS - Hi Ika, I would like to know more about PRS and the tax relief.')),
        'korporat': (
            'Untuk syarikat yang mempunyai lebihan tunai dalam akaun semasa dan ingin melabur sebahagiannya dengan tempoh dan tahap risiko yang sesuai.',
            'For companies with surplus cash in a current account that want to invest part of it with a suitable time frame and level of risk.',
            [('Akaun atas nama syarikat', 'An account in the company’s name'),
             ('Pilihan dana ikut keperluan tunai dan tempoh syarikat', 'Fund options that fit the company’s cash needs and time frame'),
             ('Dokumen yang diperlukan diterangkan dari awal', 'Required documents explained up front')],
            ('KORPORAT - Hai Ika, saya nak tahu tentang pelaburan untuk syarikat.', 'CORPORATE - Hi Ika, I would like to know about investing for a company.')),
        'semakan-portfolio': (
            'Sudah ada pelaburan? Kami semak apa yang anda pegang sekarang, terangkan prestasinya berbanding penanda aras, dan cadangkan langkah supaya selari dengan matlamat anda.',
            'Already investing? We review what you hold now, explain its performance against its benchmark, and suggest steps to keep it aligned with your goals.',
            [('Semakan pegangan dan agihan aset', 'A review of your holdings and asset allocation'),
             ('Penerangan prestasi berbanding penanda aras, dalam tempoh yang dinyatakan', 'Performance explained against benchmarks, over stated periods'),
             ('Tukar dana (switching) hanya bila ada sebab yang jelas', 'Fund switching only when there is a clear reason')],
            ('SEMAKAN - Hai Ika, saya nak semak portfolio pelaburan saya.', 'REVIEW - Hi Ika, I would like a review of my investment portfolio.')),
    }
    blocks = ''
    for sid, ic, tms, ten, dms, den in SERVICES:
        lead_ms, lead_en, items, msg = detail[sid]
        blocks += f'''<article class="service" id="{sid}">
  <div><span class="ic-round">{I[ic]}</span>{t("h2", tms, ten)}{t("p", dms, den, 'class="muted" style="margin-top:12px"')}</div>
  <div class="body">
    {t("p", lead_ms, lead_en)}
    {t("h3", "Apa yang anda dapat", "What you get")}
    {ticks(items)}
    <div class="btns">{wa_btn("Tanya tentang ini", "Ask about this", msg)}</div>
  </div>
</article>'''
    body = f'''{page_hero("Servis", "Services", "Pelaburan yang dipilih ikut matlamat anda.", "Investments chosen around your goals.", "Empat servis utama, satu pendekatan: faham dulu, kemudian baru melabur.", "Four main services, one approach: understand first, then invest.")}
<section class="section"><div class="wrap">{blocks}</div></section>

<section class="section alt"><div class="wrap split">
  <div>
    {t("p", "Buka akaun", "Open an account", 'class="eyebrow"')}
    {t("h2", "Apa yang anda perlukan.", "What you will need.")}
    {t("p", "Akaun unit trust dan PRS dibuka online melalui Manulife Investments dalam lebih kurang 10 minit. Kami ada panduan bergambar untuk setiap langkah.", "Unit trust and PRS accounts are opened online through Manulife Investments in about 10 minutes. We have illustrated guides for every step.", 'class="muted" style="margin:16px 0 28px"')}
    <div class="btns">
      <a class="btn" href="{REGISTER_URL}" target="_blank" rel="noopener">{I["user-plus"]}{t("span", "Daftar akaun online", "Open an account online")}</a>
      <a class="btn ghost" href="/sumber/#panduan">{t("span", "Lihat panduan", "See the guides")}</a>
    </div>
  </div>
  {ticks([("MyKad (atau pasport untuk bukan warganegara)", "MyKad (or passport for non-citizens)"), ("Akaun bank atas nama sendiri", "A bank account in your own name"), ("Alamat emel dan nombor telefon aktif", "An active email address and phone number"), ("Lebih kurang 10 minit", "About 10 minutes")])}
</div></section>

<section class="section"><div class="wrap">
  <div class="callout">
    <div>{t("h3", "Caj dan yuran", "Charges and fees", )}{t("p", "Caj jualan, yuran pengurusan dan caj lain adalah seperti yang dinyatakan dalam prospektus / Disclosure Document dan PHS setiap dana. Kami tidak mengenakan sebarang caj tambahan, dan tidak menawarkan rebat atau diskaun tunai, selaras dengan Kod Etika FIMM.", "Sales charges, management fees and other charges are as stated in each fund’s prospectus / Disclosure Document and PHS. We do not add any extra charges, and do not offer cash rebates or discounts, in line with the FIMM Code of Ethics.")}</div>
  </div>
</div></section>

{band("Tak pasti servis mana yang sesuai?", "Not sure which service fits?", "Ceritakan situasi anda dalam satu mesej. Kami bantu tunjukkan arah.", "Describe your situation in one message. We will point you in the right direction.")}'''
    page('/servis/', 'Servis', 'Services',
         'Unit trust, PRS, pelaburan korporat dan semakan portfolio bersama MaxWealth Consultancy. Mula dari RM100 sebulan, akaun dibuka online.',
         'Unit trusts, PRS, corporate investing and portfolio reviews with MaxWealth Consultancy. From RM100 a month, accounts opened online.',
         body)


# ---------- Careers ----------
def build_careers():
    msg = ('KERJAYA - Hai Ika, saya berminat nak tahu tentang kerjaya perunding unit trust di MaxWealth Consultancy.',
           'CAREER - Hi Ika, I am interested in a unit trust consultant career at MaxWealth Consultancy.')
    offer = [
        ('Latihan', 'Training', 'Latihan produk, proses dan etika sebelum dan selepas anda berdaftar.', 'Product, process and ethics training before and after you register.'),
        ('Bimbingan', 'Mentoring', 'Bimbingan terus daripada pengasas agensi, termasuk sesi bersama pelanggan.', 'Direct mentoring from the agency’s founder, including client sessions.'),
        ('Bahan sokongan', 'Support materials', 'Panduan pelanggan, ebook pendidikan dan kandungan media sosial yang patuh garis panduan.', 'Client guides, educational ebooks and guideline-compliant social media content.'),
        ('Sokongan admin', 'Admin support', 'Bantuan urusan akaun dan temujanji, supaya anda boleh fokus kepada pelanggan.', 'Help with accounts and appointments, so you can focus on clients.'),
        ('Ilmu kewangan yang lebih luas', 'Wider financial knowledge', 'Belajar tentang produk kewangan lain dan asas pengurusan wang, bukan unit trust sahaja, supaya anda lebih faham keperluan pelanggan.', 'Learn about other financial products and money management basics, not just unit trusts, so you understand clients’ needs better.'),
    ]
    ocards = ''.join(f'<div class="card">{t("h3", a, b)}{t("p", c, d)}</div>' for a, b, c, d in offer)
    body = f'''{page_hero("Kerjaya", "Careers", "Jadi perunding unit trust dan PRS.", "Become a unit trust and PRS consultant.", "Kerjaya untuk mereka yang suka belajar tentang kewangan, suka berjumpa orang, dan mahu membantu orang lain faham pelaburan. Begini prosesnya, secara jujur.", "A career for people who enjoy learning about finance, meeting people, and helping others understand investing. Here is how it works, honestly.")}

<section class="section"><div class="wrap">
  <div class="section-head">
    {t("p", "Proses", "The process", 'class="eyebrow"')}
    {t("h2", "Dari taklimat hingga berdaftar.", "From briefing to registration.")}
  </div>
  <ol class="steps">
    <li><div>{t("h3", "Sesi taklimat", "Briefing session")}{t("p", "Kenali industri, peranan perunding dan cara agensi kami bekerja. Tiada komitmen.", "Learn about the industry, the consultant’s role and how our agency works. No commitment.")}</div></li>
    <li><div>{t("h3", "Peperiksaan FIMM", "FIMM exam")}{t("p", "Daftar dan lulus peperiksaan perunding unit trust (dan PRS jika berminat). Kami bantu dengan bahan dan sesi ulang kaji.", "Register for and pass the unit trust consultant exam (and PRS if you wish). We help with materials and revision sessions.")}</div></li>
    <li><div>{t("h3", "Pendaftaran", "Registration")}{t("p", "Selepas lulus, anda didaftarkan dengan FIMM melalui syarikat pengurusan dana. Hanya perunding berdaftar boleh memasarkan unit trust dan PRS.", "After passing, you are registered with FIMM through the fund management company. Only registered consultants may market unit trusts and PRS.")}</div></li>
    <li><div>{t("h3", "Latihan dan bimbingan", "Training and mentoring")}{t("p", "Latihan produk dan etika, kemudian mula berkhidmat kepada pelanggan bersama bimbingan pasukan.", "Product and ethics training, then you start serving clients with the team’s guidance.")}</div></li>
  </ol>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head">
    {t("p", "Apa yang kami sediakan", "What we provide", 'class="eyebrow"')}
    {t("h2", "Anda tidak bermula seorang diri.", "You do not start alone.")}
  </div>
  <div class="grid c3">{ocards}</div>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    {t("p", "Perlu tahu", "Good to know", 'class="eyebrow"')}
    {t("h2", "Gambaran yang jujur.", "An honest picture.")}
    <div style="margin-top:32px">{photo("careers", "Pasukan MaxWealth Consultancy", "The MaxWealth Consultancy team", "Perunding berdaftar FIMM", "FIMM-registered consultants", wide=True, alt="Pasukan MaxWealth Consultancy", card=False)}</div>
  </div>
  <div style="display:grid;gap:16px">
    <div class="callout"><div>{t("h3", "Pendapatan berasaskan komisen", "Commission-based income")}{t("p", "Tiada gaji tetap. Pendapatan bergantung pada usaha, kemahiran, masa yang diberikan dan keadaan pasaran, dan berbeza bagi setiap orang. Pencapaian mana-mana ahli pasukan bukan petunjuk hasil anda.", "There is no fixed salary. Income depends on effort, skill, time committed and market conditions, and differs for everyone. Any team member’s results are not an indication of yours.")}</div></div>
    <div class="callout"><div>{t("h3", "Perlu lulus dan berdaftar dahulu", "Pass and register first")}{t("p", "Anda hanya boleh memasarkan unit trust atau PRS selepas lulus peperiksaan dan berdaftar dengan FIMM. Syarat kelayakan penuh diterangkan semasa sesi taklimat.", "You may only market unit trusts or PRS after passing the exam and registering with FIMM. Full eligibility requirements are explained at the briefing session.")}</div></div>
    <div class="callout"><div>{t("h3", "Etika dahulu", "Ethics first")}{t("p", "Kami ikut Kod Etika FIMM: tiada janji pulangan, tiada rebat tunai kepada pelanggan, dan cadangan yang sesuai dengan profil risiko pelanggan.", "We follow the FIMM Code of Ethics: no promised returns, no cash rebates to clients, and recommendations that suit each client’s risk profile.")}</div></div>
  </div>
</div></section>

{band("Nak tahu lebih?", "Want to know more?", "Daftar minat untuk sesi taklimat seterusnya. Ika akan hubungi anda dengan tarikh dan butiran.", "Register your interest for the next briefing session. Ika will contact you with the date and details.", msg, ("Daftar minat", "Register interest"))}'''
    page('/kerjaya/', 'Kerjaya', 'Careers',
         'Kerjaya sebagai perunding unit trust dan PRS bersama MaxWealth Consultancy: peperiksaan dan pendaftaran FIMM, latihan dan bimbingan. Pendapatan berasaskan komisen.',
         'A career as a unit trust and PRS consultant with MaxWealth Consultancy: FIMM exam and registration, training and mentoring. Commission-based income.',
         body)


# ---------- Resources ----------
def build_resources():
    guides = [
        ('ut', 'Daftar akaun Unit Trust', 'Register a Unit Trust account', 'panduan-daftar-akaun-unit-trust-bm.pdf', 'guide-register-unit-trust-account-en.pdf'),
        ('prs', 'Daftar akaun PRS', 'Register a PRS account', 'panduan-daftar-akaun-prs-bm.pdf', 'guide-register-prs-account-en.pdf'),
        ('people', 'Buka akaun Unit Trust bersama', 'Open a joint Unit Trust account', 'panduan-buka-akaun-unit-trust-bersama-bm.pdf', 'guide-open-joint-unit-trust-account-en.pdf'),
        ('arrow', 'Cara labur dalam dana', 'How to invest in a fund', 'panduan-cara-labur-dana-bm.pdf', 'guide-how-to-invest-in-a-fund-en.pdf'),
        ('review', 'Set pelan pelaburan bulanan (RSP)', 'Set up a monthly plan (RSP)', 'panduan-set-rsp-bulanan-bm.pdf', 'guide-set-up-monthly-rsp-en.pdf'),
        ('globe', 'Cara tukar dana', 'How to switch funds', 'panduan-cara-tukar-dana-bm.pdf', 'guide-how-to-switch-funds-en.pdf'),
    ]
    grows = ''.join(f'''<div class="guide"><span class="ic-round">{I[ic]}</span>
  <span class="txt">{t("b", ms, en)}{t("span", "PDF, BM dan English", "PDF, BM and English")}</span>
  <span class="pdf"><a href="{PERSONAL}/guides/{bm}" target="_blank" rel="noopener">BM</a><a href="{PERSONAL}/guides/{eng}" target="_blank" rel="noopener">EN</a></span>
</div>''' for ic, ms, en, bm, eng in guides)
    calcs = [
        ('Dana kecemasan', 'Emergency fund', 'Berapa perlu ada, dan berapa lama nak capai.', 'How much you need, and how long to get there.'),
        ('Pertumbuhan kompaun', 'Compound growth', 'Lihat bagaimana pelaburan berkala boleh berkembang dari tahun ke tahun.', 'See how regular investing could grow over the years.'),
        ('TVM (nilai masa wang)', 'TVM (time value of money)', 'Kira sasaran, jumlah bulanan, jumlah sekali atau tempoh.', 'Work out a target, monthly amount, lump sum or time needed.'),
    ]
    ccards = ''.join(f'<div class="card"><span class="ic-round">{I["calc"]}</span>{t("h3", a, b)}{t("p", c, d)}</div>' for a, b, c, d in calcs)
    body = f'''{page_hero("Sumber", "Resources", "Belajar dulu, labur kemudian.", "Learn first, invest later.", "Panduan langkah demi langkah, kalkulator dan ebook pendidikan untuk bantu anda faham sebelum membuat keputusan.", "Step-by-step guides, calculators and educational ebooks to help you understand before you decide.")}

<section class="section" id="panduan"><div class="wrap split" style="align-items:start">
  <div>
    {t("p", "Panduan", "Guides", 'class="eyebrow"')}
    {t("h2", "Panduan langkah demi langkah.", "Step-by-step guides.")}
    {t("p", "Panduan bergambar untuk aplikasi dan laman Manulife iFUNDS. Setiap panduan ada dalam BM dan English, dan dibuka di khairulkhalis.com.", "Illustrated guides for the Manulife iFUNDS app and site. Each guide comes in BM and English, and opens on khairulkhalis.com.", 'class="muted" style="margin-top:16px"')}
  </div>
  <div>{grows}</div>
</div></section>

<section class="section alt" id="kalkulator"><div class="wrap">
  <div class="section-head">
    {t("p", "Kalkulator", "Calculators", 'class="eyebrow"')}
    {t("h2", "Kira dulu, rancang kemudian.", "Do the sums first.")}
    {t("p", "Kalkulator ini berada di laman peribadi Khairul Khalis. Ilustrasi sahaja, berdasarkan andaian pulangan tetap; pulangan sebenar berubah-ubah dan tidak dijamin.", "These calculators live on Khairul Khalis’s personal site. Illustrations only, based on a fixed return assumption; actual returns vary and are not guaranteed.", 'class="lead"')}
  </div>
  <div class="grid c3">{ccards}</div>
  <p style="margin-top:32px"><a class="btn" href="{PERSONAL}/" target="_blank" rel="noopener">{t("span", "Buka kalkulator di khairulkhalis.com", "Open the calculators on khairulkhalis.com")}{I["out"]}</a></p>
</div></section>

<section class="section" id="ebook"><div class="wrap">
  <div class="section-head">
    {t("p", "Ebook", "Ebooks", 'class="eyebrow"')}
    {t("h2", "Ebook pendidikan kewangan.", "Financial education ebooks.")}
    {t("p", "Ditulis oleh Khairul Khalis. Ebook ialah produk pendidikan berasingan; membelinya tidak mewajibkan apa-apa pelaburan.", "Written by Khairul Khalis. The ebooks are a separate educational product; buying one does not require any investment.", 'class="lead"')}
  </div>
  <div class="books">
    <a class="book" href="{PERSONAL}/ebook/sebelum-anda-labur.pdf" target="_blank" rel="noopener">
      <div class="cover"><img src="/assets/cover-free.jpg" alt="Ebook Sebelum Anda Labur" loading="lazy" width="600" height="600"></div>
      {t("span", "Percuma", "Free", 'class="tag y"')}<b>Sebelum Anda Labur</b>{t("span", "Unit trust secara ringkas dan cara mula dengan betul.", "Unit trusts in brief, and how to start the right way.")}
    </a>
    <a class="book" href="{PERSONAL}/" target="_blank" rel="noopener">
      <div class="cover"><img src="/assets/cover-paid.jpg" alt="Ebook Unit Trust Dari Zero" loading="lazy" width="600" height="600"></div>
      {t("span", "Ebook penuh", "Full ebook", 'class="tag"')}<b>Unit Trust Dari Zero</b>{t("span", "Dari “apa benda ni” sampai boleh baca fund fact sheet.", "From “what is this?” to reading a fund fact sheet.")}
    </a>
    <a class="book" href="{PERSONAL}/" target="_blank" rel="noopener">
      <div class="cover"><img src="/assets/cover-urus-duit.jpg" alt="Ebook Urus Duit Dari Zero" loading="lazy" width="600" height="600"></div>
      {t("span", "Ebook penuh", "Full ebook", 'class="tag"')}<b>Urus Duit Dari Zero</b>{t("span", "Kawal duit, keluar dari hutang dan mula bina masa depan.", "Take control of your money, get out of debt and start building your future.")}
    </a>
  </div>
</div></section>

<section class="section tight"><div class="wrap">
  <a class="card" href="{CHANNEL}" target="_blank" rel="noopener" style="flex-direction:row;align-items:center;gap:18px">
    <span class="ic-round">{I["megaphone"]}</span>
    <div style="flex:1">{t("h3", "Saluran WhatsApp Unit Trust", "Unit Trust WhatsApp Channel")}{t("p", "Info pasaran dan tips, percuma untuk diikuti.", "Market updates and tips, free to follow.")}</div>
    {I["out"].replace('<svg', '<svg width="20" height="20"')}
  </a>
</div></section>

{band("Ada soalan selepas membaca?", "Questions after reading?", "Kami boleh terangkan bahagian yang kurang jelas.", "We can explain anything that is not clear.")}'''
    page('/sumber/', 'Sumber', 'Resources',
         'Panduan buka akaun unit trust dan PRS (BM dan English), kalkulator dan ebook pendidikan kewangan daripada MaxWealth Consultancy.',
         'Guides to open unit trust and PRS accounts (BM and English), calculators and financial education ebooks from MaxWealth Consultancy.',
         body)


# ---------- FAQ ----------
def build_faq():
    groups = [
        ('Asas', 'The basics', [
            ('Apa itu unit trust?', 'What is a unit trust?',
             'Unit trust mengumpul wang ramai pelabur ke dalam satu dana yang diurus oleh pengurus dana profesional. Dana itu dilaburkan dalam saham, bon, instrumen pasaran wang atau aset lain ikut objektifnya. Anda memiliki unit dalam dana tersebut, dan nilai unit berubah mengikut nilai aset dana.',
             'A unit trust pools money from many investors into one fund run by a professional fund manager. The fund invests in shares, bonds, money market instruments or other assets according to its objective. You own units in the fund, and their value moves with the value of the fund’s assets.'),
            ('Apa beza unit trust dan PRS?', 'What is the difference between a unit trust and PRS?',
             'Kedua-duanya diurus oleh pengurus dana. PRS khusus untuk persaraan: ia layak pelepasan cukai tahunan (tertakluk syarat LHDN), dan pengeluaran sebelum umur persaraan tertakluk syarat dan penalti cukai. Unit trust biasa lebih fleksibel untuk pelbagai matlamat.',
             'Both are run by fund managers. PRS is specifically for retirement: it is eligible for yearly tax relief (subject to LHDN rules), and withdrawals before retirement age are subject to conditions and a tax penalty. Regular unit trusts are more flexible for different goals.'),
            ('Adakah pulangannya tetap?', 'Are the returns fixed?',
             'Tidak. Harga unit dan agihan (jika ada) boleh naik dan turun, dan anda mungkin mendapat kembali kurang daripada jumlah yang dilaburkan. Prestasi lalu bukan petunjuk prestasi masa depan. Kami terangkan prestasi dana berbanding penanda arasnya, dalam tempoh yang dinyatakan.',
             'No. Unit prices and distributions (if any) may go down as well as up, and you may get back less than you invested. Past performance is not indicative of future performance. We explain a fund’s performance against its benchmark, over stated periods.'),
            ('Ada pilihan patuh Shariah?', 'Are there Shariah-compliant options?',
             'Ya. Terdapat dana unit trust dan PRS yang patuh Shariah. Beritahu kami pilihan anda semasa sesi pertama.',
             'Yes. There are Shariah-compliant unit trust and PRS funds. Let us know your preference at the first session.'),
        ]),
        ('Bermula', 'Getting started', [
            ('Berapa minimum untuk mula?', 'What is the minimum to start?',
             'Melalui pelan pelaburan bulanan, anda boleh mula dari RM100 sebulan. Jumlah minimum untuk pelaburan sekali bergantung pada dana; kami akan maklumkan semasa memilih dana.',
             'Through a monthly investment plan you can start from RM100 a month. The minimum for a lump sum depends on the fund; we will let you know when choosing one.'),
            ('Bagaimana nak buka akaun?', 'How do I open an account?',
             'Akaun dibuka online melalui Manulife Investments dalam lebih kurang 10 minit. Anda perlukan MyKad, akaun bank atas nama sendiri, emel dan nombor telefon. Panduan bergambar ada di halaman <a href="/sumber/#panduan">Sumber</a>.',
             'Accounts are opened online through Manulife Investments in about 10 minutes. You need your MyKad, a bank account in your own name, an email address and a phone number. Illustrated guides are on the <a href="/sumber/#panduan">Resources</a> page.'),
            ('Boleh keluarkan wang bila-bila masa?', 'Can I withdraw at any time?',
             'Untuk unit trust, anda boleh menjual (redeem) unit pada hari bekerja dan wang dibayar dalam tempoh yang dinyatakan dalam prospektus. Untuk PRS, pengeluaran sebelum umur persaraan adalah terhad dan tertakluk syarat serta penalti cukai.',
             'For unit trusts, you can redeem units on business days and the money is paid within the period stated in the prospectus. For PRS, withdrawals before retirement age are limited and subject to conditions and a tax penalty.'),
        ]),
        ('Caj dan perunding', 'Charges and consultants', [
            ('Apa caj yang dikenakan?', 'What are the charges?',
             'Caj jualan, yuran pengurusan dan caj lain adalah seperti yang dinyatakan dalam prospektus / Disclosure Document dan PHS setiap dana. Kami terangkan semuanya sebelum anda melabur, dan tidak mengenakan caj tambahan.',
             'Sales charges, management fees and other charges are as stated in each fund’s prospectus / Disclosure Document and PHS. We explain them all before you invest, and add no extra charges.'),
            ('Ada rebat atau diskaun tunai?', 'Are there cash rebates or discounts?',
             'Tidak. Kod Etika FIMM tidak membenarkan perunding memberi rebat atau diskaun tunai kepada pelabur.',
             'No. The FIMM Code of Ethics does not allow consultants to give investors cash rebates or discounts.'),
            ('Bagaimana nak semak perunding berdaftar?', 'How do I check that a consultant is registered?',
             'Semua perunding unit trust dan PRS mesti berdaftar dengan FIMM. Semak status pendaftaran di <a href="https://www.fimm.com.my" target="_blank" rel="noopener">laman FIMM</a>.',
             'All unit trust and PRS consultants must be registered with FIMM. Check registration status on the <a href="https://www.fimm.com.my" target="_blank" rel="noopener">FIMM website</a>.'),
            ('Siapa yang akan membalas WhatsApp saya?', 'Who will answer my WhatsApp message?',
             'Ika, Admin kami. Ika akan menjawab soalan asas dan mengatur masa untuk anda berbual dengan perunding.',
             'Ika, our Admin. Ika answers basic questions and arranges a time for you to talk to a consultant.'),
        ]),
    ]
    out = ''
    for gms, gen, qs in groups:
        items = ''.join(f'<details><summary data-en="{esc(qen)}">{qms}</summary><div class="a">{t("p", ams, aen)}</div></details>' for qms, qen, ams, aen in qs)
        out += f'<div class="faq-group">{t("h2", gms, gen)}{items}</div>'
    body = f'''{page_hero("FAQ", "FAQ", "Soalan yang selalu ditanya.", "Frequently asked questions.", "Jawapan ringkas kepada soalan biasa tentang unit trust, PRS dan cara kami bekerja.", "Short answers to common questions about unit trusts, PRS and how we work.")}
<section class="section"><div class="wrap faq">{out}</div></section>
{band("Soalan anda tiada di sini?", "Your question is not here?", "Tanya terus. Kami balas di WhatsApp.", "Ask us directly. We reply on WhatsApp.")}'''
    page('/faq/', 'FAQ', 'FAQ',
         'Soalan yang selalu ditanya tentang unit trust dan PRS: minimum untuk mula, caj, pengeluaran, pilihan Shariah dan cara buka akaun bersama MaxWealth Consultancy.',
         'Frequently asked questions about unit trusts and PRS: minimum to start, charges, withdrawals, Shariah options and opening an account with MaxWealth Consultancy.',
         body)


# ---------- Contact ----------
def build_contact():
    topics = [
        ('Unit trust', 'Unit trusts'), ('PRS dan pelepasan cukai', 'PRS and tax relief'),
        ('Pelaburan korporat', 'Corporate investing'), ('Semakan portfolio', 'Portfolio review'),
        ('Bantuan buka akaun', 'Help opening an account'), ('Kerjaya perunding', 'Consultant career'),
        ('Lain-lain', 'Other'),
    ]
    opts = ''.join(f'<option data-en="{esc(en)}">{ms}</option>' for ms, en in topics)
    body = f'''{page_hero("Hubungi", "Contact", "Mula dengan satu mesej.", "Start with one message.", "Cara paling cepat ialah WhatsApp. Ika (Admin) akan membalas dan mengatur masa untuk anda berbual dengan perunding.", "WhatsApp is the fastest way. Ika (Admin) will reply and arrange a time for you to talk to a consultant.")}
<section class="section"><div class="wrap contact-grid">
  <div>
    <ul class="contact-list">
      <li><span class="ic-round">{I["wa"]}</span><div>{t("b", "WhatsApp (Ika, Admin)", "WhatsApp (Ika, Admin)")}<a {wa(*WA_GENERAL)}>+60 19-402 4401</a>{t("span", "Soalan, temujanji dan urusan akaun", "Questions, appointments and account matters")}</div></li>
      <li><span class="ic-round">{I["mail"]}</span><div>{t("b", "Emel", "Email")}<a href="mailto:{EMAIL}">{EMAIL}</a>{t("span", "Khairul Khalis, Founder MaxWealth", "Khairul Khalis, Founder of MaxWealth")}</div></li>
      <li><span class="ic-round">{I["user-plus"]}</span><div>{t("b", "Daftar akaun online", "Open an account online")}<a href="{REGISTER_URL}" target="_blank" rel="noopener" data-en="Manulife Investments registration">Pendaftaran Manulife Investments</a>{t("span", "Lebih kurang 10 minit", "About 10 minutes")}</div></li>
      <li><span class="ic-round">{I["megaphone"]}</span><div>{t("b", "Saluran WhatsApp", "WhatsApp Channel")}<a href="{CHANNEL}" target="_blank" rel="noopener" data-en="Follow the channel">Ikuti saluran</a>{t("span", "Info pasaran dan tips", "Market updates and tips")}</div></li>
    </ul>
  </div>
  <form class="form" id="waForm" novalidate>
    {t("h2", "Tulis mesej anda", "Write your message")}
    {t("p", "Isi ringkas di bawah. Butang ini membuka WhatsApp dengan mesej siap ditulis kepada Ika (Admin); laman ini tidak menyimpan apa-apa.", "Fill in the short form below. The button opens WhatsApp with your message ready for Ika (Admin); this site does not store anything.", 'class="note"')}
    <div class="field">{t("label", "Nama", "Name", 'for="f-name"')}<input id="f-name" name="name" type="text" autocomplete="name" placeholder="Nama anda" data-en-placeholder="Your name"></div>
    <div class="field">{t("label", "Topik", "Topic", 'for="f-topic"')}<select id="f-topic" name="topic">{opts}</select></div>
    <div class="field">{t("label", "Mesej (pilihan)", "Message (optional)", 'for="f-msg"')}<textarea id="f-msg" name="message" placeholder="Contoh: Saya nak mula melabur RM200 sebulan untuk persaraan." data-en-placeholder="Example: I would like to start investing RM200 a month for retirement."></textarea></div>
    <button class="btn" type="submit">{I["wa"]}{t("span", "Buka WhatsApp", "Open WhatsApp")}</button>
  </form>
</div></section>'''
    page('/hubungi/', 'Hubungi', 'Contact',
         'Hubungi MaxWealth Consultancy melalui WhatsApp (Ika, Admin) di +60 19-402 4401 atau emel. Tanya tentang unit trust, PRS, semakan portfolio atau kerjaya.',
         'Contact MaxWealth Consultancy on WhatsApp (Ika, Admin) at +60 19-402 4401 or by email. Ask about unit trusts, PRS, portfolio reviews or careers.',
         body)


# ---------- Legal ----------
SSM = 'CT0171343-H'


def legal_page(path, title_ms, title_en, desc_ms, desc_en, ms_html, en_html):
    body = f'''{page_hero("Undang-undang", "Legal", title_ms, title_en, "Kemas kini terakhir: 8 November 2026", "Last updated: 8 November 2026")}
<section class="section"><div class="wrap">
  <div class="prose lang-block" lang="ms">{ms_html}</div>
  <div class="prose lang-block" lang="en" hidden>{en_html}</div>
</div></section>'''
    page(path, title_ms, title_en, desc_ms, desc_en, body, priority='0.3')


def build_legal():
    privacy_ms = f'''
<p>Notis ini menerangkan bagaimana MaxWealth Consultancy (SSM {SSM}) (“kami”) mengumpul, menggunakan dan melindungi data peribadi anda, selaras dengan Akta Perlindungan Data Peribadi 2010 (PDPA) dan pindaannya. Notis ini disediakan dalam Bahasa Melayu dan English.</p>
<h2>1. Data yang kami kumpul</h2>
<p>Laman web ini tidak mempunyai borang yang menyimpan data. Kami hanya menerima data peribadi apabila anda menghubungi kami sendiri, contohnya melalui WhatsApp atau emel, seperti:</p>
<ul><li>nama, nombor telefon dan alamat emel;</li><li>umur, lokasi, matlamat kewangan dan maklumat pelaburan yang anda kongsi;</li><li>kandungan mesej anda.</li></ul>
<p>Butang “Buka WhatsApp” di halaman Hubungi hanya menyusun mesej dalam pelayar anda dan membuka WhatsApp; laman ini tidak menyimpan atau menghantar data tersebut.</p>
<h2>2. Tujuan</h2>
<ul><li>menjawab pertanyaan anda dan mengatur temujanji;</li><li>menerangkan produk dan membantu proses membuka akaun;</li><li>membuat semakan portfolio dan perkhidmatan selepas jualan;</li><li>mematuhi kehendak undang-undang dan kawal selia.</li></ul>
<h2>3. Pendedahan</h2>
<p>Kami mungkin berkongsi data anda dengan Manulife Investment Management (M) Berhad sebagai pembekal produk (bagi tujuan membuka dan mengurus akaun anda), serta dengan pihak berkuasa atau badan kawal selia apabila dikehendaki oleh undang-undang. Kami tidak menjual data peribadi anda. Pembukaan akaun dibuat di laman Manulife Investments dan tertakluk kepada notis privasi mereka sendiri.</p>
<h2>4. Penyimpanan dan keselamatan</h2>
<p>Kami menyimpan data hanya selama yang perlu untuk tujuan di atas atau seperti yang dikehendaki undang-undang, dan mengambil langkah munasabah untuk melindunginya daripada akses, pendedahan atau kehilangan tanpa kebenaran.</p>
<h2>5. Kuki dan storan pelayar</h2>
<p>Laman ini tidak menggunakan kuki penjejakan atau analitik. Pilihan bahasa anda (BM/EN) disimpan dalam storan tempatan pelayar anda sahaja. Fon laman dimuatkan daripada Google Fonts, yang menerima alamat IP pelayar anda untuk menghantar fail fon.</p>
<h2>6. Hak anda</h2>
<p>Anda berhak meminta akses kepada data peribadi anda, membetulkannya, menarik balik persetujuan, menghadkan pemprosesan, dan meminta pemindahan data seperti yang dibenarkan oleh PDPA. Hantar permintaan melalui saluran di bawah. Jika anda tidak memberikan data yang diperlukan, kami mungkin tidak dapat membantu permintaan anda.</p>
<h2>7. Hubungi kami</h2>
<p>MaxWealth Consultancy (SSM {SSM})<br>WhatsApp: +60 19-402 4401 · Emel: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>8. Perubahan</h2>
<p>Kami mungkin mengemas kini notis ini dari semasa ke semasa. Versi terkini sentiasa ada di halaman ini.</p>
<p>Jika terdapat percanggahan antara versi Bahasa Melayu dan English, versi Bahasa Melayu akan diguna pakai.</p>'''
    privacy_en = f'''
<p>This notice explains how MaxWealth Consultancy (SSM {SSM}) (“we”) collects, uses and protects your personal data, in line with the Personal Data Protection Act 2010 (PDPA) and its amendments. This notice is provided in Bahasa Melayu and English.</p>
<h2>1. Data we collect</h2>
<p>This website has no forms that store data. We only receive personal data when you contact us yourself, for example on WhatsApp or by email, such as:</p>
<ul><li>your name, phone number and email address;</li><li>your age, location, financial goals and any investment details you share;</li><li>the content of your messages.</li></ul>
<p>The “Open WhatsApp” button on the Contact page only composes a message in your browser and opens WhatsApp; this site does not store or send that data.</p>
<h2>2. Purposes</h2>
<ul><li>to answer your questions and arrange appointments;</li><li>to explain products and help with account opening;</li><li>to carry out portfolio reviews and after-sales service;</li><li>to comply with legal and regulatory requirements.</li></ul>
<h2>3. Disclosure</h2>
<p>We may share your data with Manulife Investment Management (M) Berhad as the product provider (to open and manage your account), and with authorities or regulators when required by law. We do not sell your personal data. Accounts are opened on the Manulife Investments site and are subject to their own privacy notice.</p>
<h2>4. Retention and security</h2>
<p>We keep data only as long as needed for the purposes above or as required by law, and take reasonable steps to protect it from unauthorised access, disclosure or loss.</p>
<h2>5. Cookies and browser storage</h2>
<p>This site uses no tracking or analytics cookies. Your language choice (BM/EN) is kept in your browser’s local storage only. The site’s fonts load from Google Fonts, which receives your browser’s IP address to deliver the font files.</p>
<h2>6. Your rights</h2>
<p>You may ask to access your personal data, correct it, withdraw consent, limit processing, and request data portability as permitted by the PDPA. Send requests through the channels below. If you do not provide the data we need, we may not be able to help with your request.</p>
<h2>7. Contact us</h2>
<p>MaxWealth Consultancy (SSM {SSM})<br>WhatsApp: +60 19-402 4401 · Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>8. Changes</h2>
<p>We may update this notice from time to time. The latest version is always on this page.</p>
<p>If there is any inconsistency between the Bahasa Melayu and English versions, the Bahasa Melayu version prevails.</p>'''
    legal_page('/privasi/', 'Notis Privasi', 'Privacy Notice',
               'Notis privasi MaxWealth Consultancy di bawah Akta Perlindungan Data Peribadi 2010 (PDPA): data yang dikumpul, tujuan, pendedahan dan hak anda.',
               'MaxWealth Consultancy privacy notice under the Personal Data Protection Act 2010 (PDPA): data collected, purposes, disclosure and your rights.',
               privacy_ms, privacy_en)

    disc_ms = '''
<h2>Maklumat umum sahaja</h2>
<p>Kandungan laman ini untuk maklumat umum dan pendidikan sahaja. Ia bukan nasihat pelaburan, cukai atau undang-undang, dan bukan tawaran atau ajakan untuk membeli atau menjual mana-mana produk pelaburan. Keputusan pelaburan perlu dibuat berdasarkan objektif, keadaan kewangan dan profil risiko anda sendiri.</p>
<h2>Risiko pelaburan</h2>
<p>Pelaburan melibatkan risiko. Pelaburan unit trust dan PRS tertakluk kepada risiko termasuk risiko kehilangan modal. Harga unit dan agihan pendapatan (jika ada) boleh naik dan turun. Prestasi lalu bukan petunjuk prestasi masa depan.</p>
<h2>Dokumen produk</h2>
<p>Pelabur dinasihatkan membaca dan memahami Prospektus / Memorandum Maklumat (untuk unit trust) atau Disclosure Document (untuk PRS), serta Product Highlights Sheet (PHS), sebelum melabur. Dokumen ini boleh didapati daripada perunding anda atau laman rasmi pengurus dana.</p>
<h2>Ilustrasi dan cukai</h2>
<p>Contoh dan pengiraan di laman ini hanya ilustrasi, bukan unjuran pulangan. Pengiraan cukai adalah anggaran sahaja; sila rujuk LHDN atau perunding cukai.</p>
<h2>Pautan luar</h2>
<p>Laman ini memaut ke laman lain, termasuk khairulkhalis.com, laman Manulife Investments dan WhatsApp. Kami tidak bertanggungjawab ke atas kandungan atau amalan privasi laman tersebut.</p>
<h2>Status perunding</h2>
<p>Khairul Khalis ialah perunding unit trust (UTC) dan PRS berdaftar FIMM (F01065736), mewakili Manulife Investment Management (M) Berhad melalui agensi MaxWealth Consultancy.</p>'''
    disc_en = '''
<h2>General information only</h2>
<p>The content on this site is for general information and education only. It is not investment, tax or legal advice, and is not an offer or solicitation to buy or sell any investment product. Investment decisions should be based on your own objectives, financial situation and risk profile.</p>
<h2>Investment risk</h2>
<p>Investing involves risk. Unit trust and PRS investments are subject to risks, including the risk of capital loss. Unit prices and income distributions (if any) may go down as well as up. Past performance is not indicative of future performance.</p>
<h2>Product documents</h2>
<p>Investors are advised to read and understand the Prospectus / Information Memorandum (for unit trusts) or Disclosure Document (for PRS), and the Product Highlights Sheet (PHS), before investing. These are available from your consultant or the fund manager’s official website.</p>
<h2>Illustrations and tax</h2>
<p>Examples and calculations on this site are illustrations only, not projections of returns. Tax calculations are estimates only; please refer to LHDN or a tax adviser.</p>
<h2>External links</h2>
<p>This site links to other sites, including khairulkhalis.com, the Manulife Investments site and WhatsApp. We are not responsible for their content or privacy practices.</p>
<h2>Consultant status</h2>
<p>Khairul Khalis is a FIMM-registered unit trust (UTC) and PRS consultant (F01065736), representing Manulife Investment Management (M) Berhad through the MaxWealth Consultancy agency.</p>'''
    legal_page('/penafian/', 'Penafian', 'Disclaimer',
               'Penafian MaxWealth Consultancy: maklumat umum sahaja, risiko pelaburan unit trust dan PRS, dokumen produk dan pautan luar.',
               'MaxWealth Consultancy disclaimer: general information only, unit trust and PRS investment risk, product documents and external links.',
               disc_ms, disc_en)

    terms_ms = f'''
<h2>1. Penggunaan laman</h2>
<p>Dengan menggunakan laman ini, anda bersetuju dengan terma ini. Jika anda tidak bersetuju, sila jangan gunakan laman ini.</p>
<h2>2. Kandungan</h2>
<p>Kandungan disediakan untuk maklumat umum sahaja dan tertakluk kepada <a href="/penafian/">Penafian</a> kami. Kami berusaha memastikan maklumat tepat dan terkini, tetapi tidak memberi sebarang waranti tentang ketepatannya atau kesesuaiannya untuk tujuan anda.</p>
<h2>3. Harta intelek</h2>
<p>Logo, nama dan kandungan asal MaxWealth Consultancy adalah milik kami. Nama dan tanda dagangan pihak lain, termasuk Manulife Investments, adalah milik pemilik masing-masing dan digunakan sebagai rujukan sahaja. Anda tidak boleh menyalin atau mengedar kandungan laman ini untuk tujuan komersial tanpa kebenaran bertulis.</p>
<h2>4. Pautan luar</h2>
<p>Pautan ke laman pihak ketiga disediakan untuk kemudahan. Penggunaan laman tersebut tertakluk kepada terma mereka sendiri.</p>
<h2>5. Had liabiliti</h2>
<p>Setakat yang dibenarkan undang-undang, kami tidak bertanggungjawab ke atas sebarang kerugian yang timbul daripada penggunaan laman ini atau pergantungan kepada kandungannya.</p>
<h2>6. Undang-undang</h2>
<p>Terma ini ditadbir oleh undang-undang Malaysia.</p>
<h2>7. Hubungi</h2>
<p>MaxWealth Consultancy (SSM {SSM})<br>WhatsApp: +60 19-402 4401 · Emel: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''
    terms_en = f'''
<h2>1. Using this site</h2>
<p>By using this site you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>2. Content</h2>
<p>Content is provided for general information only and is subject to our <a href="/penafian/">Disclaimer</a>. We aim to keep information accurate and current, but give no warranty about its accuracy or fitness for your purpose.</p>
<h2>3. Intellectual property</h2>
<p>The MaxWealth Consultancy logo, name and original content belong to us. Other names and trademarks, including Manulife Investments, belong to their respective owners and are used for reference only. You may not copy or distribute this site’s content for commercial purposes without written permission.</p>
<h2>4. External links</h2>
<p>Links to third-party sites are provided for convenience. Your use of those sites is subject to their own terms.</p>
<h2>5. Limitation of liability</h2>
<p>To the extent permitted by law, we are not liable for any loss arising from use of this site or reliance on its content.</p>
<h2>6. Governing law</h2>
<p>These terms are governed by the laws of Malaysia.</p>
<h2>7. Contact</h2>
<p>MaxWealth Consultancy (SSM {SSM})<br>WhatsApp: +60 19-402 4401 · Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''
    legal_page('/terma/', 'Terma Penggunaan', 'Terms of Use',
               'Terma penggunaan laman web MaxWealth Consultancy.',
               'Terms of use for the MaxWealth Consultancy website.',
               terms_ms, terms_en)


def build_404():
    body = f'''<section class="nf"><div class="wrap">
  <p class="code">404</p>
  {t("h1", "Halaman tidak dijumpai.", "Page not found.")}
  {t("p", "Pautan ini mungkin sudah berubah. Cuba mula dari halaman utama.", "This link may have changed. Try starting from the home page.", 'class="lead"')}
  <div class="btns"><a class="btn" href="/">{t("span", "Ke halaman utama", "Go to the home page")}</a><a class="btn ghost" href="/hubungi/">{t("span", "Hubungi kami", "Contact us")}</a></div>
</div></section>'''
    page('/404.html', 'Halaman tidak dijumpai', 'Page not found',
         'Halaman yang anda cari tidak dijumpai.', 'The page you are looking for was not found.', body, sitemap=False)


def build_meta_files():
    urls = ''.join(f'  <url><loc>{DOMAIN}{p}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>\n' for p, pr in PAGES)
    files = {
        'sitemap.xml': f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        'robots.txt': f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n',
        'site.webmanifest': '{\n  "name": "MaxWealth Consultancy",\n  "short_name": "MaxWealth",\n  "start_url": "/",\n  "display": "browser",\n  "background_color": "#FFFFFF",\n  "theme_color": "#124674",\n  "icons": [{ "src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png" }]\n}\n',
        # Apache hosting (e.g. cPanel at Exabytes): custom 404 and HTTPS; ignored by GitHub Pages / Netlify
        '.htaccess': 'ErrorDocument 404 /404.html\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n',
    }
    for name, content in files.items():
        with open(os.path.join(SITE, name), 'w', encoding='utf-8') as f:
            f.write(content)


if __name__ == '__main__':
    build_home()
    build_about()
    build_services()
    build_careers()
    build_resources()
    build_faq()
    build_contact()
    build_legal()
    build_404()
    build_meta_files()
    print('Built', len(PAGES) + 1, 'pages into', SITE)
