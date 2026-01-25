# ZeroToProductionInRust
おもしろ

- apiはhealth_checkから作る
  - GETに200を返すだけ
  - クエリストリングもレスポンスボディもなし
- sqlx
  - sqlxcliでmigrationができる
    - こっちはCargo.tomlに書かずに、globalにinstallする
  - sqlxはライブラリとしてDBへの接続・クエリの実行ができる
    - 概ねSQLを書く感じなので気楽
- Postgres
  - MySQLでもよかったけど、まぁせっかくなので
  - PostgresもMySQLも同程度によい
    - メンバーが慣れている・詳しいメンバーがいる方でよいってsongmuさんも書いてた
  - CREATE TYPEで独自の型を作れる
    - 独自の型をRustのstructに変換
- PgPool
  - sqlxは非同期Interfaceを持っているが、複数クエリを平行(Concurrently)に同じconnectionから実行できない
    - PgConnection > PgPool
    - PgConnectionでLockをかけながら1connectionずつ実行することもできなくはないが遅い
- Test Isolation
  - setup で Begin Transaction して teardown で Rollback するのかと思ったが
  - 1テストごとに Database 作って、migration する方式
    - Databaseが削除されないのでどんどん溜まっていく...
    - volumeマウントやめて毎回作り直すか？
- Telemetry
  - Loggingよりも細かい単位でログ出力していく(=Tracing)
    - request  response
    - sql execution
    - OpenTelemetryに形式を揃えておくと良さそう
- Secret
  - Logに秘密情報を出力しない
  - どれが秘密情報か宣言できる仕組み、便利
  - 秘密情報を使うときはひと手間かかる
      - `Secret<String>` になってて、Secretを剥がすためにexpose_secret()する
- Config
  - 環境ごとに分離、baseに共通部分を書く
- TypeDriven Development
  - ValidationのためのTypeを作る
  - validator traitも普通に存在する
  - TryFrom traitを使って、try_into()を実装するときれいに書ける
- Email
  - SaaS使え、SMTP or REST APIだ
    - REST API使えばREST Clientだけでいいぞ
  - REST API Clientもconnection poolを使う
    - Appインスタンス起動のたびにconnection poolを作るか、同じpoolをAppで使い回すか
- Test
  - 1ファイルでテストを書いていくとコンパイル時間は線形に増える
    - コンパイルが並列で実行されるように分割する
  - testsディレクトリに結合テスト、各アプリケーションコードに単体テストを書く
- Transaction
  - 普通にPgPool使っていてもTransaction貼れる
  - beginしたTransactionでpoolを固定しているのか？この辺はsqlxのソースを読まないとわからないかも
- Error Handling
  - エラーメッセージは人間が読んで誤りについて理解するためのもの
    - Control Flow: what todo next must be accessible to a machine
    - Error Reports: primarly consumed by human
    - **errors should be logged when they are handled.**
  - thiserrorとanyhowがでてきた 同じ作者らしい
    - 両方使う
    - thiserror: enumでエラー種別を一箇所に固める
    - anyhou: contextを使ってエラー時のメッセージや型を指定できる
table: error

  - INTERNAL	AT THE EDGE
- Control Flow	Types, method, fields	Status codes
- Reporting	Logs/traces	Response body

- Auth
  - Basic Auth
  - Hash Algorithm
    - SHA3256 なのでモダン...
  - Algon2id
    - PHCフォーマット
      - PHPからArgon2使うときのやつ
  - timing attack
    - validなusernameを一つ知っていれば、response timeを比べてinvalidなチャレンジを潰していける
- Machine to Machine / to Human
  - mutual TLS(mTLS)
  - OAuth2
- Login
  - Cookie
    - Session Cookie と Persistent Cookie
    - Cookieを利用してユーザから見えないところ・さわれないところでサーバとクライアントがやり取りする
    - XSSに注意
- Session
  - Session Store
    - Postgresを使う > expirationを自動化する仕組みを作る必要がある
    - Redisを使う > TTLを設定できる、inmemory DBなので早い、bulkでsessionを扱う必要はないのでKVSで十分
  - session fixation attack
  - extension trait pattern
    - [https://rustlang.github.io/rfcs/0445extensiontraitconventions.html](https://rustlang.github.io/rfcs/0445extensiontraitconventions.html)
- Middleware
  - actixweblab: experiment with future additions to actix_web
- Fault tolerant
  - あらゆる箇所が壊れうる
    - 外部API、DB、アプリケーション...
  - Idempotency(冪等性)
    - API endopoint is retrysafe
- Module
  - 最初は1ファイルに書く
    - 大きくなってきたらディレクトリにして、mod.rsを置いて分割する


やりたい
✅cargo tomlfmt
⬜ADR

  - ⬜actixweb
  - ✅DBMS
  - ✅DB_CRATE
✅typos
✅cargowatch
✅configuration.ymlを環境ごとに分離

  - CIとlocalは分けたい
✅lefthook
⬜teardown時にDatabase削除する

  - RAMディスク化した
  - database削除スクリプトを実装した
  - teardownも書きたい
    - [https://medium.com/@ericdreichert/testsetupandteardowninrustwithoutaframeworkba32d97aa5ab](https://medium.com/@ericdreichert/testsetupandteardowninrustwithoutaframeworkba32d97aa5ab)
✅superlinter

    - ✅yamllint
  - ✅markdownlint
  - ✅actionslint
✅docker postgres image use dev/shm for disk
✅aqua for no rust tools

  - aqua対応のツールが少ない...
    - typos
    - actionlint
  - gh cliも入れられるが、gh configを設定したかったので止めた
    - configファイルをコピーすればいいか
    - gh cliもaquaにした
✅distroless + musl

    - [https://www.getto.systems/entry/2021/04/23/114316](https://www.getto.systems/entry/2021/04/23/114316)
✅Makefile or Makefile.toml > lefthook.yml

  - sqlx create database && sqlx migrate run
  - fish config
    - set gx PATH "$HOME/.local/share/aquaprojaqua/bin" $PATH
  - aqua install
-  sccache
  - [# コンパイルキャッシュでRustのビルド時間を短縮しよう](https://qiita.com/tatsuya6502/items/76b28a6786a1ddc9d479)
  - [https://github.com/dimensionhq/fleet](https://github.com/dimensionhq/fleet)
-  OpenAPI
  - [https://dylananthony.com/blog/fastapirust2research/](https://dylananthony.com/blog/fastapirust2research/)
✅Rust 1.59.0 > 1.60.0

-  code coverage

後で調べる

-  mod
-  OpenTelemetry
  -  Jaeger
  -  Honeycomb.io
-  PgPool with Transaction
-  lifetime
  - [https://github.com/pretzelhammer/rustblog/blob/master/posts/commonrustlifetimemisconceptions.md#commonrustlifetimemisconceptions](https://github.com/pretzelhammer/rustblog/blob/master/posts/commonrustlifetimemisconceptions.md#commonrustlifetimemisconceptions)
-  async
  - [https://ryhl.io/blog/asyncwhatisblocking/](https://ryhl.io/blog/asyncwhatisblocking/)
-  mTLS
-  PostgresのCREATE TYPE、配列型

感想

- Rustはコストにうるさい
  - 富豪的プログラミングで育ってきたので「こまけーこたぁいいんだよ」という気持ちになる
  - が、こうすると速くなる・軽くなる・堅牢になるってことをコンパイラが教えてくれる
  - 環境に優しいコードが書ける
- 改めてRESTは好き
  - エラーハンドリングして定義したエラーをHTTPステータスコードと紐付けていくのは悪くない体験
    - GraphQLではこの辺についての知識がない
      - RESTと違って類推しづらい、ということはあるかもしれない
      - ステータスコードのような指針がほしいところ
    - RESTのURI設計とDBモデリングとは別個にやるべきで、密結合にして開発速度を上げるアプローチはシステムの寿命を縮めるのでは...???
      - 特にDBモデリング...
      - 勝手にcreated_atとupdated_atとdeleted_atを生やすんじゃない！という気持ち
- コメントに大事なことが書いてあるのでコメント含めて写経すると理解が進む
- 字が小さい
  - 老眼かもしれません

参考

- [https://github.com/LukeMathWalker/zero-to-production](https://github.com/LukeMathWalker/zero-to-production)
- [https://www.zero2prod.com/index.html?country=Japan&discount_code=VAT20](https://www.zero2prod.com/index.html?country=Japan&discount_code=VAT20)
- [https://github.com/watarukura/zero_to_production_study](https://github.com/watarukura/zero_to_production_study)
