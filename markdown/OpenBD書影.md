# OpenBD書影
OpenBDから書影を取ってきてscrapboxページを作るようにした

  - 残念ながら書影が登録されていないコミック多数
    - 気持ちよく使えるのはありがたいが
  - ISBNから公式サイトを引いてそこから画像を取得できればよいのだが・・・
```amazon_to_scrapbox.js
javascript: (function() {
    const title = document.getElementById("ebooksProductTitle").innerText.trim();

    let pub = [];
    const c = document.getElementsByClassName('author');
    for (g = 0; g < c.length; g++) {
        let at = c[g].innerText.replace(/,/, '');
        let pu = at.match(/\(.+\)/);
        let ct = at.replace(/\(.+\)/, '').replace(/ /g, '');
        pub.push(pu + ' [' + ct + ']');
    }

    const url = window.location.href;
    const asin = /\/dp\/([A-Z0-9]+)\//.exec(url)[1];
    const kindle_comic_url = 'https://read.amazon.co.jp/manga/' + asin;

    const real_book_link = document.querySelector("a.title-text").href;
    const isbn10 = /\/dp\/([A-Z0-9]+)\//.exec(real_book_link)[1];
    const src = `978${isbn10.slice(0, 9)}`;
    const sum = src.split('').map(s => parseInt(s)).reduce((p, c, i) => p + ((i % 2 === 0) ? c : c * 3));
    const rem = 10 - sum % 10;
    const checkdigit = rem === 10 ? 0 : rem;
    const isbn13 = `${src}${checkdigit}`;
    const imageurl = 'https://cover.openbd.jp/' + isbn13 + '.jpg';

    const series = document.querySelector("#reviewFeatureGroup > span > a");

    let lines = `[${imageurl}]\n`;
    lines += 'author: ' + pub.join(' ') + '\n';
    lines += `isbn: ${isbn13}\n`;
    lines += `kindle_comic_link:  [${kindle_comic_url}]\n#コミック`;
    if (series) lines += '\nseries: #' + series.innerText;
    const body = encodeURIComponent(lines);
    window.open('https://scrapbox.io/watarukura-comics/' + encodeURIComponent(title.trim()) + '?body=' + body);
})();

```
2023/12/30 追記

  - [「openBD API（バージョン1）」の終了によるカーリルへの影響について](https://blog.calil.jp/2023/07/openbd-v1-end.html)
    - 書影の公開利用、いい話だと思ってたんだけどなぁ
    - 削除
[https://gyazo.com/09e4e0d23eceaac12af117e8eb7a28d0](https://gyazo.com/09e4e0d23eceaac12af117e8eb7a28d0)
