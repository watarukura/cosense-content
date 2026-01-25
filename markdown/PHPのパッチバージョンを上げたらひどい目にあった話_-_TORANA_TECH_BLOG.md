# PHPのパッチバージョンを上げたらひどい目にあった話 - TORANA TECH BLOG
[PHPのパッチバージョンを上げたらひどい目にあった話 - TORANA TECH BLOG](https://web.archive.org/web/20241109050108/https://tech.torana.co.jp/entry/2021/09/29/141642)
バックエンドエンジニアのクラシマです。

2021/08/25(水)に、本番サーバのPHPを7.4.21 -> 7.4.22にバージョンアップしました。
renovateでプルリクエストが作られるので、追っかけるだけです。
[https://tech.torana.co.jp/entry/2021/07/16/110139](https://tech.torana.co.jp/entry/2021/07/16/110139)



AMIは前日に作ってあり、当日はLaunchTemplateの向き先を変更するためにterraform applyして、AutoScalingGroupからインスタンスの更新をするだけ。

や～便利になったなぁ、なんて作業してたらSlackが大騒ぎに・・・
[https://gyazo.com/6dfe06656619be06bb15e2b6e295ccf5](https://gyazo.com/6dfe06656619be06bb15e2b6e295ccf5)



### 切り戻し！

急いで切り戻し！と判断したのは良いものの、まさかPHPのバージョンアップ起因だとはその時は思いもよらず。

当日deployしたアプリケーションや、Aurora MySQLの設定変更などを順次戻していきますが、一向に回復せず。

stg環境でも動作が同じだったのですが、もう一台のpre-stg環境(featureブランチを適用しての動作確認用環境)では保存できることが判明。
AMIを変更したら戻った、というところから根本原因の調査を開始しました。

(この間、約1.5h...)

### 原因調査

本番・stg環境とpre-stg環境の差異を上げて、1つずつ検証していき、ようやくPHPのパッチバージョン起因と判明。

PHP 7.4.22 + Swoole 4.6.7 からamazon-sdk-phpを呼び出すと遅い。
SQSへジョブキューを溜めているのですが、メッセージが保存されてから、なぜかレスポンスが返ってくるのに60秒かかる。
ALBのタイムアウトをデフォルトの60秒で使っていたので、504 Gateway Timeout、というわけです。

PHPのバージョンとSwooleのバージョンの組み合わせを変えたりと試してみたのですが、PHP 7.4.21 + Swoole 4.6.7以外は遅くて実用に耐えないことがわかりました。

### 是正対応

さて、困りました。EC2で動作しているアプリケーションのPHPのパッチバージョンを固定したい。

現在は、PackerでAMIを作っており、remiを使用してPHP7.4をyum installしています。
マイナーバージョンまでは指定できるものの、パッチバージョンは指定できません。

以下、3つの方法を試しました。

1. PHPをソースコードからビルドする
2. Dockerを使用する
3. 動いていたAMIを活かす


1.はだいぶ苦労する道でした・・・。

とりあえずPHP公式イメージを使っていた開発用のDockerイメージをAmazonLinux2に変更してビルド、動作するまで試してみます。
ローカルでテストを一回し、全部通ったらPackerでAMI作って動作確認。
めもりーさんが「ソースからビルドするのは簡単ですよ」って言うのでホイホイやってみたのですが、まぁ、うん、できますけど、うん...。
で。EC2起動して動かしてみたらどうも動作が遅い、どこに原因があるかわからない。期限として決めていた1週間が過ぎたので、とりあえずこの線はパスだな、と。
[https://zenn.dev/memory/articles/43e0e2fb0c525a4aa025](https://zenn.dev/memory/articles/43e0e2fb0c525a4aa025)

2.では、まずFargate on ECSへの移行を考えました。

影響範囲をコントロールしやすいバッチサーバから移行してみようとcronジョブとジョブキューを1つずつTaskに切り出して検証してみます。
動作に支障がなさそうでよしよし、と思っていたところ、EC2からの実行だと3時間で終わるcronジョブの1つが一向に終わらないことに気づきました。
AuroraMySQLからデータを取り出し、PHPで加工してElasticsearch Service(以下、ES)へ登録する、というものです。どうやら、ESへの書き込みが遅い。5倍くらい時間がかかる。

Swooleはカーネルパラメータやulimitを変更しないとリソース不足で動かないので、その辺かと当たりをつけたのですが、Fargateからはカーネルパラメータがいじれない。
諦めてEC2 on ECSで実行し、ネットワークモードをawsvpcからbridgeやhostに変更してみたもののコレでもダメ。
ECSの問題か、と既存のバッチサーバ用EC2にdockerをインストールしてdocker runしてもダメ。
AWSサポートに相談してみたものの、「ECSの問題ではなさそうなので回答できませんね」と切り分けていただきました。無念。と、この対応には結局2週間かかりました。

↓みなさまも+1していただけるとAWSさんがFargateでsysctlsをサポートしてくれるかも！
[https://github.com/aws/containers-roadmap/issues/460#issuecomment-918791111](https://github.com/aws/containers-roadmap/issues/460#issuecomment-918791111)



で、3.です。

PHP 7.4.21 + Swoole 4.6.7が動作しているAMIを使って、Packerでアレコレ追加実装した部分をCodeDeployのinstallAfterスクリプトに移植します。

具体的には、Cloudwatch-Agentのインストールなどです。
動作検証こそ面倒なものの、手堅く動きます。
問題は、PHPもSwooleもバージョンがどんどん進んでいくことです。セキュリティ面からも、追随しないことには不安があります。

### 恒久対応

しかし、もう大丈夫。めもりーさんがSwoole本体に上げたIssueがクローズされ、次のバージョンのSwooleへは反映されそうです。
当該コミットハッシュをcheckoutして検証してみましたが、PHP 7.4.21でも7.4.24(2021/09/29時点の最新)でも支障なく動作します。
[https://github.com/swoole/swoole-src/issues/4393](https://github.com/swoole/swoole-src/issues/4393)

ということで、1ヶ月かかった障害の恒久対応がようやく終わりそうでほっとしております。
PHPのパッチバージョンを上げるのにもヒヤヒヤする仕事、一緒にやっていきたい方を募集中です。

[https://www.wantedly.com/projects/533124](https://www.wantedly.com/projects/533124)

[https://www.wantedly.com/projects/533131](https://www.wantedly.com/projects/533131)

[#トラーナテックブログ](トラーナテックブログ)
