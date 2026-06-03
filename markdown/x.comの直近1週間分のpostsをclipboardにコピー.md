# x.comの直近1週間分のpostsをclipboardにコピー
```xposts.js
javascript: (
  async () => {
    const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const posts = [...document.querySelectorAll('article')]
      .map(a => {
        const time = a.querySelector('time');
        if (!time) return null;
        const ts = new Date(time.dateTime)
          .getTime();
        if (ts < weekAgo) return null;
        const link = time.closest('a');
        const url = link ? new URL(link.getAttribute('href'), location.origin).href : '';
        const date = new Date(time.dateTime).toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
        const text = [...a.querySelectorAll('[data-testid="tweetText"]')]
          .map(e => e.textContent)
          .join('\n')
          .trim();
        if (!text) return null;
        return { ts, body: ` ${date} [${url}]\n  >${text.replace(/\n/g, "\n  >")}` };
      }
      )
      .filter(Boolean).sort((a, b) => b.ts - a.ts);
    const out = `${posts
      .map(p => p.body)
      .join('\n\n')}`;
    await navigator.clipboard.writeText(out);
    alert(`${posts.length} posts copied`);
  }
)();


```
[#bookmarklet](bookmarklet)
