# MaxWealth Consultancy website

Static multi-page site for **maxwealthconsultancy.com.my** (main domain; maxwealthconsultancy.com should redirect to it).
Built 8 Nov 2026. Repo: https://github.com/khairulkhalis000404-hue/maxwealth-site (public, GitHub Pages from `main` `/docs`).
Temporary live URL until the custom domain is set: https://khairulkhalis.com/maxwealth-site/ (GitHub serves project sites under the user site's domain).

- `docs/` — the published folder (GitHub Pages serves it). Internal links are relative so it works under a sub-path too. Pages: `/`, `/tentang/`, `/servis/`, `/kerjaya/`, `/sumber/`, `/faq/`, `/hubungi/`, `/privasi/`, `/penafian/`, `/terma/`, `404.html`, plus `sitemap.xml`, `robots.txt`, `site.webmanifest`, `.htaccess` (Apache/cPanel only).
- `tools/build.py` — ALL page copy (BM + EN) lives here. Edit, then run `python3 tools/build.py`. Asset URLs get a content hash automatically.
- `tools/preview-sync.sh` — rebuild + copy to the scratchpad the `maxwealth-site` preview server serves (the launcher can't read Desktop).
- `docs/assets/site.css`, `site.js` — design tokens (light/dark), BM/EN toggle, mobile menu, WhatsApp composer.
- `screenshots/` — phone, iPad, desktop, dark mode.

## Done / still open
- Photos (8 Nov 2026, user's pick): `docs/assets/photos/home.jpg` + `about.jpg` = studio grey portrait; `careers.jpg` = team office photo (user confirmed everyone agreed, 8 Nov 2026). Replace a file and rebuild to swap.
- SSM CT0171343-H is in the legal pages and footer. No agency address yet (lines removed; add to the privacy/terms contact blocks in build.py when there is one).
- Kerjaya offers confirmed by the user, plus "Ilmu kewangan yang lebih luas" (other financial products).
- Hosting: GitHub Pages (user's choice, 8 Nov 2026). No analytics yet (privacy notice says no tracking cookies; update it if Umami is added).

## Publishing
Edit `tools/build.py` → `python3 tools/build.py` → preview → ask the user → `git commit` + `git push` (Pages redeploys in ~1 min). Undo = revert commit, never force-push.

## Live domain
Live on **maxwealthconsultancy.com.my** since 10 Nov 2026. DNS is in Exabytes (client area > Manage DNS): `A` `@` -> the four GitHub IPs, `CNAME` `www` -> `khairulkhalis000404-hue.github.io`. **maxwealthconsultancy.com** redirects to it through a Cloudflare Redirect Rule limited to the apex and www, so subdomains such as pay. are not redirected; keep the iCloud MX, TXT and DKIM records there.

## Connecting the domains (when maxwealthconsultancy.com.my is active)
1. **Exabytes, DNS for maxwealthconsultancy.com.my** (the .com.my had no nameservers yet on 8 Nov 2026; activation was pending email/SSM verification):
   - `A` `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` `www` → `khairulkhalis000404-hue.github.io`
2. Then set the custom domain: `gh api -X PUT repos/khairulkhalis000404-hue/maxwealth-site/pages -f cname=maxwealthconsultancy.com.my` (GitHub commits `docs/CNAME`, so `git pull` afterwards), wait for the certificate, then turn on HTTPS: `... -F https_enforced=true`. The khairulkhalis.com/maxwealth-site/ URL then redirects to the new domain.
3. **Cloudflare, maxwealthconsultancy.com** (bought 7 Nov 2026 at Cloudflare Registrar): DNS → add `A` `@` → `192.0.2.1` (Proxied) and `CNAME` `www` → `maxwealthconsultancy.com` (Proxied); Rules → Redirect Rules → "Redirect to a different domain": hostname is maxwealthconsultancy.com or www.maxwealthconsultancy.com → dynamic `concat("https://maxwealthconsultancy.com.my", http.request.uri.path)`, 301, keep query string.

## Compliance choices
- No Akaun 1 investment service in the services list. Never name KW$P/€PF in site copy: write "Simpanan Persaraan (Akaun 1)" / "Retirement Savings (Account 1)" (user, 11 Nov 2026).
- No Manulife or other institution logos; MaxWealth logo only.
- Stats (6+ tahun, 300+ pelabur, RM10 juta+ AUM) labelled as Khairul's own figures.
- Awards listed without the two ambiguous "iFunds (Account)" lines; awards not used on the Kerjaya page.
- Kerjaya: commission-based, no fixed salary, FIMM exam + registration first.
- Every WhatsApp link goes to Ika (Admin) 60194024401 with a prefilled BM or EN message.
