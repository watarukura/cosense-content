# Vue.js + Slim Framework + ssv
SPAできるフロントエンド層＋薄いPHPのバックエンド層＋取替のきくデータストア層の3層アーキテクチャとかできないかな

フロントエンド層
[https://qiita.com/SoraKumo/items/ded7cec28b3b8792bb88](https://qiita.com/SoraKumo/items/ded7cec28b3b8792bb88)

- [Vue.js](Vue.js)
    - やわらかVue.js [/vue-yawaraka](/vue-yawaraka)
- [axios](axios)

バックエンド層
[https://twitter.com/tanakahisateru/status/1036500463204454401](https://twitter.com/tanakahisateru/status/1036500463204454401)

- [Slim Framework](Slim Framework)
- [https://qiita.com/yookihiroo/items/8222f4c44c7b0e4fe686](https://qiita.com/yookihiroo/items/8222f4c44c7b0e4fe686)
- [DBAL](DBAL)
- [Guzzle](Guzzle)
- [Monolog](Monolog)
[https://gyazo.com/d29764de1c0137962282433db38d1cac](https://gyazo.com/d29764de1c0137962282433db38d1cac)

データストア層

- csv: [ユニケージ開発手法](ユニケージ開発手法) で作成されたssvファイルを操作できるライブラリをPHPで書く？
- [parsecsv](parsecsv) でいけそう
- DynamoDB: [Kettle](Kettle)
- RDB: [idiorm](idiorm) or [DBAL](DBAL)
