# Amazon書影＋Affiリンク

    - [/wkwknote/アソシエイト対応版 AmazonからScrapboxへ書影を取り込むブックマークレット](/wkwknote/アソシエイト対応版 AmazonからScrapboxへ書影を取り込むブックマークレット)←をほぼお借りした
    - Amazonアソシエイトの申請時、URLにハイフンが入っているとNGのようで、仕方なくwatarukuraプロジェクトに作成
        - kindleマンガ本棚用に分離したかったが仕方ない
        - 違った タイトルにkindleが入っているとNGのようだ

```amazon_affi.js
javascript:(function(){
     var p = document.getElementById("productTitle");
     if (!p) var p = document.getElementById("ebooksProductTitle");

     var title = p.innerHTML;
     if (!title) return;

     var imagecontainer = document.getElementById("imageBlockContainer");
     if (!imagecontainer) var imagecontainer = document.getElementById("ebooksImageBlockContainer");
     var image = imagecontainer.getElementsByTagName("img")[0];
     var imageurl = image.getAttribute("src");
     var pub = [];
     var c = document.getElementsByClassName('author');
     for (g=0; g < c.length ;g++){
    			let at = c[g].innerText.replace(/,/,'');
    			let pu = at.match(/\(.+\)/);
    			let ct = at.replace(/\(.+\)/,'').replace(/ /g,'');
    			pub.push(pu + ' [' + ct + ']');
    	}

    	/* アフィリエイト用テキストリンク取得 */
    	const affiliate_text_link = document.getElementById("amzn-ss-text-shortlink-textarea").innerHTML;
    	const text_link = (affiliate_text_link ? affiliate_text_link : window.location.href);

    	/* マンガ本棚用URL作成 */
    	const url = window.location.href;
    	const asin = /\/dp\/([A-Z0-9]+)\//.exec(url)[1];
    	const kindle_comic_url = 'https://read.amazon.co.jp/manga/' + asin;

    	/* 本文 */
     var lines = '[' + imageurl + ' ' + text_link + ']\n'
               + pub.join(' ')
               + '\n[kindleマンガ本棚URL ' + kindle_comic_url + ']'
               + '\n#書評';
     var body = encodeURIComponent(lines);

     /* プロジェクト名を適宜変更する */
     window.open('https://scrapbox.io/watarukura/'+encodeURIComponent(title.trim()) + '?body=' + body)
   })();
```
[#蔵書管理](蔵書管理)
