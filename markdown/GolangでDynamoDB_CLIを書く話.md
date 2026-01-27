# GolangでDynamoDB CLIを書く話
[GolangでDynamoDB CLIを書く話｜ハンズラボ株式会社](https://www.hands-lab.com/tech/t3180/)  の転記です
2017.12.04
[https://gyazo.com/2211cf96cdfb412de10d5cda3c289a80](https://gyazo.com/2211cf96cdfb412de10d5cda3c289a80)
こんにちは。クラシマです。
ハンズラボ Advent Calendar 2017 4日目の記事です。
もう随分前になりますが、井上がGolang製のDynamoDB用のCLIを探していたことがありました。
ネットストアのセールに向けて行った負荷対策について/ハンズアラボエンジニアブログ
結局見つからなかったのでNode.jsで井上本人が書き、現在もECサイトの本番環境で使っています。
↓それがこちらのbikkeです。
[https://github.com/inouet/bikke](https://github.com/inouet/bikke)
10月末くらいから趣味プロジェクトでGolangを書いていたのですが、
井上の記事を思い出したのでDynamoDB用のCLIを書くことにしました。
できあがったものが↓これです。
[https://github.com/watarukura/gody](https://github.com/watarukura/gody)

AWSプロファイルはstg

itemテーブルからGSI:jan-indexのパーティションキー:janに4937751121103を指定でqueryする

出力はヘッダ付きで空白区切りテキスト(ssv)とし、出力するフィールドはjanとnameに絞る
```gody.bash
gody query 
--profile stg 
--table item 
--pkey 4937751121103 
--index jan-index 
--format ssv 
--header 
--field jan,name
=>
name jan
つぼキーク 4937751121103

```
自分でCLIのツールを書くのは初めてなので三歩進んで二歩下がりながら進めています。
個人的にJSONを手で書くのが苦痛なので、JSONをオプションに使わない、というのがコンセプトです。
まだlist/get/query/scanしかできないので、put/update/deleteができるようになったら本番環境で使えないか検証したいところです。
put/updateのオプションをどうするか、今も悩んでいます。
テストもあまり書けてないですし・・・。
趣味プロジェクトから業務プロジェクトに反映するにはもう少し時間がかかりそうです。
Golang、いいですね！
低レイヤーの知識がないと速いプログラムが書けない、というところも魅力です。
日頃はPHPを書いていて、ポインタやバッファを気にすることはなくて、この辺りの扱いはさっぱりです。
今のところも並行処理的な機能をほぼ使ってないので、速くなる余地が随分残っている気がします。
あとは、JSONの扱いが楽なのがモダンな言語という感じがします。
弊社、ユニケージ開発により大量のBashスクリプトが稼働していますが、JSONの扱いは特に困るところです。
DynamoDBをデータストアの1st Choiceにするプロジェクトはそれなりにあるので、
そこでJSONを経由せずにDynamoDBを扱えるようになると、楽ができる部分は結構増えます。
ECサイト以外でも、ハンズラボ全体で使えるツールになるといいなぁと夢想しています。
AWS LambdaのGolangサポートも発表されましたし、今後ますますGolangを使うシーンが増えそうです。
折よく、開発に使っていたGoLandも販売開始になりました。
PHPStormユーザがGolangを書くならGoLandで決まりですね！
ハンズラボ Advent Calendar 2017 の5日目は、青木さんです。
Golangの学習には以下の書籍とサイトに大変お世話になりました。
この場を借りてお礼申し上げます。

    - スターティングGo言語
        - 通勤路で読むのにちょうどよい内容でした。コラムでGolangのポインタについて「C言語との互換性のためにある」という見解で、使わなくても書けそうだなーと気が楽になりました。
    - Treasure 2017 の研修資料は Go を学ぶのに最高だった
        - GASでSlackBotを書く趣味プロジェクトが一段落して次を探していたときに、こちらの記事を読んでGolangの学習を始めました。
    - Go入門　Treasure2017版
        - A Tour of Goに挫折していたのでこのスライドを見て再挑戦でした。ajito.fmに出てるsuzukenさんだ！と気づいたのはちょっと後になってからです。
    - Go言語でAWSのサービスを使ってみる ~SQS・DynamoDBを試す~
        - aws-sdk-go、扱いが辛そうで躊躇していたところ、こちらの記事記載のaws-sdk-go-wrapperをみてwrapper-wrapperなら書けそう！と思えました。
    - GoでAWS SDKを叩くCLIツールを作ってリリースするまでの流れ(aws-sdk-go+cobra+viper+gox+ghr)
        - flagパッケージだけではサブコマンドのあるCLIを作るのは辛そうだったので、こちらの記事を読んでCLIフレームワークにcobraを使いました。
    - Golangのコマンドライブラリcobraを使って少しうまく実装する
        - テスト書いてないまま「テスト駆動開発」を読んでいて不安が増してきたため、テストの書き方を参考にさせていただきました。
※ アイキャッチのGopherくんの原著作者はRenée Frenchさんです。

[#ハンズラボテックブログ](ハンズラボテックブログ)
