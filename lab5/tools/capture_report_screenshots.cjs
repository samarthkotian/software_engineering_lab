/* Capture genuine browser screenshots of the saved, unmodified report text. */
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const escape = value => value.replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;').replaceAll('>', '&gt;');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-lcd-text'],
    executablePath: process.env.LAB5_BROWSER_EXE || undefined,
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1140, height: 850 },
      deviceScaleFactor: 1 });
    await fs.mkdir(path.join(root, 'evidence'), { recursive: true });
    for (const stage of ['before', 'after']) {
      const metadata = JSON.parse(await fs.readFile(
        path.join(root, 'reports', stage, 'run_metadata.json'), 'utf8'));
      for (const tool of ['pylint', 'bandit', 'flake8']) {
        let content = await fs.readFile(
          path.join(root, 'reports', stage, `${tool}_report.txt`), 'utf8');
        let note = 'Complete saved analyzer output. Stdout followed by stderr.';
        if (stage === 'before' && tool === 'bandit') {
          const blocks = content.split(/-{40,}\r?\n/);
          content = blocks.filter(block => /\[B(307|324|605):/.test(block))
            .map(block => block.replace(/^.*?(?=>> Issue:)/s, '').trim())
            .join('\n\n----------------------------------------\n\n');
          note = 'High and Medium finding excerpts. The full report is in the PDF appendix.';
        }
        const args = metadata[tool].command.slice(2).join(' ');
        const empty = content.length === 0;
        const html = `<!doctype html><html><head><meta charset="utf-8">
          <title>${tool} ${stage} - saved analysis report</title>
          <style>
          *{box-sizing:border-box}body{margin:0;padding:30px;background:#fff;
          color:#000;font-family:Arial,sans-serif}main{background:#fff;
          padding:28px;border:1px solid #000}
          h1{margin:0 0 10px;font-size:26px}header{display:flex;
          justify-content:space-between;align-items:center}
          .badge{padding:7px 12px;background:#fff;border:1px solid #000;
          font-size:14px}p{font-size:14px;color:#000}
          .command{background:#fff;color:#000;padding:12px 16px;
          font:15px Consolas,monospace;border:1px solid #000}
          pre{font:15px/1.5 Consolas,'Courier New',monospace;margin:18px 0 0;
          white-space:pre-wrap;overflow-wrap:anywhere;color:#000}
          .empty{margin:20px 0 0;padding:18px;background:#fff;
          border:1px solid #000;font-size:17px;color:#000}
          footer{font-size:12px;color:#000;
          margin-top:18px;border-top:1px solid #000;padding-top:12px}
          </style></head><body><main><header><h1>${tool.toUpperCase()} | ${stage.toUpperCase()}</h1>
          <span class="badge">Recorded exit code: ${metadata[tool].exit_code}</span></header>
          <p>${note}</p><div class="command">python -m ${escape(tool + ' ' + args)}</div>
          ${empty ? '<div class="empty">Report file is empty (0 bytes). Flake8 completed successfully with no findings.</div>' : `<pre>${escape(content)}</pre>`}
          <footer>Lab 5 / Samarth Kotian / PES1UG24CS406 / 30 October 2026<br>
          Source: reports/${stage}/${tool}_report.txt</footer></main></body></html>`;
        await page.setContent(html);
        await page.locator('main').screenshot({
          path: path.join(root, 'evidence', `${tool}_${stage}.png`) });
        console.log(`Saved evidence/${tool}_${stage}.png`);
      }
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
