# MaxWealth Consultancy website

Static multi-page site for **maxwealthconsultancy.com.my** (main domain; maxwealthconsultancy.com should redirect to it).
Built 8 Nov 2026. Not published yet.

- `docs/` — the deployable folder (upload/push this). Pages: `/`, `/tentang/`, `/servis/`, `/kerjaya/`, `/sumber/`, `/faq/`, `/hubungi/`, `/privasi/`, `/penafian/`, `/terma/`, `404.html`, plus `sitemap.xml`, `robots.txt`, `site.webmanifest`, `.htaccess` (Apache/cPanel only).
- `tools/build.py` — ALL page copy (BM + EN) lives here. Edit, then run `python3 tools/build.py`. Asset URLs get a content hash automatically.
- `tools/preview-sync.sh` — rebuild + copy to the scratchpad the `maxwealth-site` preview server serves (the launcher can't read Desktop).
- `docs/assets/site.css`, `site.js` — design tokens (light/dark), BM/EN toggle, mobile menu, WhatsApp composer.
- `screenshots/` — phone, iPad, desktop, dark mode.

## Done / still open
- Photos (8 Nov 2026, user's pick): `docs/assets/photos/home.jpg` + `about.jpg` = studio grey portrait; `careers.jpg` = team office photo (ask everyone in it for permission before publishing). Replace a file and rebuild to swap.
- SSM CT0171343-H is in the legal pages and footer. No agency address yet (lines removed; add to the privacy/terms contact blocks in build.py when there is one).
- Kerjaya offers confirmed by the user, plus "Ilmu kewangan yang lebih luas" (other financial products).
- Hosting + DNS not decided (Exabytes cPanel, or GitHub Pages like khairulkhalis.com); maxwealthconsultancy.com must 301 to .com.my. No analytics yet (privacy notice says no tracking cookies; update it if Umami is added).

## Compliance choices
- No KW$P investment service, eligibility calculator or "Akaun 1" wording (banned outside ebooks).
- No Manulife or other institution logos; MaxWealth logo only.
- Stats (6+ tahun, 300+ pelabur, RM10 juta+ AUM) labelled as Khairul's own figures.
- Awards listed without the two ambiguous "iFunds (Account)" lines; awards not used on the Kerjaya page.
- Kerjaya: commission-based, no fixed salary, FIMM exam + registration first.
- Every WhatsApp link goes to Ika (Admin) 60194024401 with a prefilled BM or EN message.
