# responder
[Flask](Flask)心配なのでこっちで作るか[watarukura.icon](watarukura.icon)

[公式ドキュメント](https://python-responder.org/en/latest/index.html)
[Github](https://github.com/kennethreitz/responder)
[人間のためのイケてるPython WebFramework「responder」、そして作者のKenneth Reitzについて](https://blog.ikedaosushi.com/entry/2018/12/01/195512)

いきなりハマる

- `pipenv install responder --pre` で `ModuleNotFoundError: No module named 'pkg_resources'` が出力される
  - [https://rutei.hatenablog.com/entry/2018/12/02/020358](https://rutei.hatenablog.com/entry/2018/12/02/020358)
```Pipfile
[packages]
responder = "*"
starlette = "==0.8"

```
入門した

  - [https://github.com/watarukura/responder_study](https://github.com/watarukura/responder_study)

[SQLAlchemy](SQLAlchemy)使うか[PyMySQL](PyMySQL)使うか悩む

- [Pythonで話題のWEBフレームワークresponderでサンプルのtodoリストを作成](https://note.mu/shimakaze_soft/n/ne47bc123dc83)
- [PyMySQL](PyMySQL)は社内で導入事例あるから[SQLAlchemy](SQLAlchemy)の知見を貯めるか・・・という気持ち

[Vue.js + Flask](Vue.js + Flask) で検討した構成も取れる

  - SPA対応もできる

OpenAPI v3にも対応

[https://gyazo.com/1bf123e329828c312c3b8561e227a126](https://gyazo.com/1bf123e329828c312c3b8561e227a126)
[#python](python)
