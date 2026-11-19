// Renders guide.html -> guide-raw.pdf (Letter) and slides.html -> slides-raw.pdf (16:9).
// One Chromium at a time, closed right away. Then run: python3 finalize.py
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    const jobs = [
      ['guide.html', 'guide-raw.pdf', '8.5in', '11in'],
      ['slides.html', 'slides-raw.pdf', '13.333in', '7.5in'],
    ];
    for (const [src, out, width, height] of jobs) {
      await page.goto('file://' + path.join(__dirname, src), { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      // Report any page whose content is taller than the page box.
      const over = await page.evaluate(() => [...document.querySelectorAll('.page,.slide')].map((p, i) => {
        const foot = p.querySelector('.foot');
        const limit = foot ? foot.getBoundingClientRect().top : p.getBoundingClientRect().bottom;
        let max = 0;
        for (const el of p.children) if (el !== foot) max = Math.max(max, el.getBoundingClientRect().bottom);
        return { n: i + 1, spare: Math.round(limit - max), scroll: p.scrollHeight > p.clientHeight + 1 };
      }));
      console.log(src, over.map(o => `${o.n}:${o.spare}${o.scroll ? '!' : ''}`).join(' '));
      await page.pdf({ path: path.join(__dirname, out), width, height, printBackground: true,
        margin: { top: '0', right: '0', bottom: '0', left: '0' }, preferCSSPageSize: true });
    }
  } finally {
    await browser.close();
  }
})();
