// Open the ISO C11 page in a headless browser and record status, title and a screenshot.
// Usage: NODE_PATH=<dir containing puppeteer> node open-iso-page.cjs OUTPNG
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36');
  await page.evaluateOnNewDocument(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  await page.setViewport({ width: 1280, height: 900 });
  const statuses = [];
  page.on('response', r => { if (r.url().startsWith('https://www.iso.org/standard/57853')) statuses.push(r.status()); });
  await page.goto('https://www.iso.org/standard/57853.html', { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.log('goto:', e.message));
  for (let i = 0; i < 20; i++) {
    const t = await page.title().catch(() => '');
    if (t && !/just a moment/i.test(t)) break;
    await new Promise(r => setTimeout(r, 1500));
  }
  const title = await page.title().catch(() => '');
  const h1 = await page.$eval('h1', e => e.innerText).catch(() => '');
  console.log(JSON.stringify({ url: page.url(), statuses, title, h1 }));
  await page.screenshot({ path: process.argv[2] });
  await browser.close();
})();
