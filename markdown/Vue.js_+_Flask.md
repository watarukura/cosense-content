# Vue.js + Flask
Python手習いのため、FlaskでWebAPIサーバを書く

教本
[https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs](https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs)

フロントエンド

- [Vue.js](Vue.js)
    - [Nuxt.js](Nuxt.js) ・・・使用するか悩む

バックエンド

    - [Flask](Flask)

データストア

- RDB: [SQLAlchemy](SQLAlchemy)
- DynamoDB: [PynamoDB](PynamoDB)

開発環境

- VS Codeで環境作る https://qiita.com/shibukawa/items/1650724daf117fad6ccd
- Docker使う、PythonのWeb APIサーバでステップ実行する http://www.atmarkit.co.jp/ait/articles/1809/06/news030.html

ハマりメモ

- python用にgenerateされた.gitignoreで`build/`が無視されるため、webpack用のbuildコマンドが通らなかった
    - .gitignoreから`build/`を削除して解決
