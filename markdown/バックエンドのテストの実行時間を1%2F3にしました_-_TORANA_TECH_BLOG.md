# バックエンドのテストの実行時間を1/3にしました - TORANA TECH BLOG
[バックエンドのテストの実行時間を1/3にしました - TORANA TECH BLOG](https://web.archive.org/web/20241003095657/https://tech.torana.co.jp/entry/2021/05/26/120000)
はじめまして。4月より株式会社トラーナに入社した、 バックエンドチームのクラシマです。（[@watarukura](https://github.com/watarukura)）

deploy周りの改善が好きなので、バックエンドのテスト実行時間を短縮した話をします。
テストケースを分割して、parallelで実行するようにしました。

### バックエンドのテストの状況



↑こちらのスライドから更に半年、テストは1300件に近づき、アサーションも5900件近くになりました。
[https://gyazo.com/71713074b56e6587211682e7c651fe73](https://gyazo.com/71713074b56e6587211682e7c651fe73)


バックエンドは機能追加したらテストを書くルールになっていて大変治安が良いのですが、副作用としてテストの実行に30分くらいかかっていました。
テストが終わらないとプルリクエストをマージできないので、レビュー依頼する前に30分待って、指摘を受けて修正して30分待って・・・、と開発サイクルが滞ってしまいます。
コレはいかん、ということで高速化することにしました。

### GitHub Actionsのmatrixを使う

[paratest](https://github.com/paratestphp/paratest)も試してみたのですが、うまく動作せず断念しました。
docker-composeでテスト用DBも起動してテストしているのですが、一部のテストに順序依存が発生しているようです。
スパッと諦めて、GitHub Actionsのmatrix実行を試してみます。

```(yaml)
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        parallelism: [5]
        id: [0,1,2,3,4]
...
      - name: Run tests
        run: |
          set -xv
          test_target=$(find tests/Unit/ -name '*Test.php' \
                          | LANG=C sort \
                          | awk "NR % ${{ matrix.parallelism }} == ${{ matrix.id }}" \
                          | sed -e 's/^/<file>/' -e 's;$;</file>;' \
                          | tr -d '\n')
          sed -i '/\/tests\/Unit/c\'$test_target'' phpunit.xml
          ./bin/phpunit -d memory_limit=-1 --stop-on-failure --debug

```
テスト対象ファイルのリストを5分割して、`<file>`と`</file>`で囲み、普段使っているphpunit.xmlを直接書き換えています。
↓こちらの記事を参考にさせていただきました。ありがとうございます！
[https://qiita.com/ProjectEuropa/items/afd871c4a58ad5b22f44](https://qiita.com/ProjectEuropa/items/afd871c4a58ad5b22f44)

jobs.<job_id>.strategy.matrix の公式ドキュメントはこちら。
[https://docs.github.com/ja/actions/reference/workflow-syntax-for-github-actions](https://docs.github.com/ja/actions/reference/workflow-syntax-for-github-actions)

matrix実行については、公式ドキュメントのサンプルにある通りNode.jsやOSなどで複数バージョンの並行テストに使うのは知っていたのですが、`awk "NR % ${{ matrix.parallelism }} == ${{ matrix.id }}"` で実行対象の振り分けに使う、というのは盲点でした。

parallelismの値をもっと大きくすればよいのでは？と疑問の方もいらっしゃると思いますが、何度か試したところ5並列でも1〜2ジョブが起動待ちになってしまうことがあり、並列実行数には上限があるようです。
jobs.<job_id>.strategy.max-parallel には↓の記載があります。
> デフォルトでは、GitHubはGitHubがホストしている仮想マシン上で利用できるrunnerに応じてできるかぎりの数のジョブを並列に実行します。

before: 1300件のテストを直列で実行する
[https://gyazo.com/f8b23cdd43a77fb6b8ca38939e7222d5](https://gyazo.com/f8b23cdd43a77fb6b8ca38939e7222d5)

after: 1300件のテストを260件ずつ並行で実行する
[https://gyazo.com/65dfcfe828b88e9c826e5f55eed0b3eb](https://gyazo.com/65dfcfe828b88e9c826e5f55eed0b3eb)

Yeah!

1ファイルごとのテスト数に偏りがありますが、最長でも実行時間がおおよそ1/3になりました！

### 苦労話

- `phpunit 'filename1' 'filename2'`で動くのでは？ -> 最初の1ファイルしか実行されない
- `phpunit --filter 'filename1|filename2|...'`で動くのでは？ -> 何度か動かしたものの、`no test found`で落ちる
- --filterにはnamespace + class名を書きましょう
- ファイル名から↑に変換できなくもない？と粘ったものの、phpunit.xmlを書き換えるほうが簡単でした・・・
- ローカル環境ではdocker内でphpunitを実行するためにラッパースクリプトを使用しており、phpunitへ引き渡す引数について中身が問題なのか形式が問題なのかの切り分けが大変でした・・・
- `set -xv` はBashのデバッグ用途でつけています
- `$test_target`が展開して表示されるので、実行予定のテストの一覧ができて便利です


### 最後に

今後もdeploy頻度を増やす活動を続けていきます。
開発体験の改善が大好きなエンジニアの皆さん、ぜひ一緒に働きましょう！

[#トラーナテックブログ](トラーナテックブログ)
