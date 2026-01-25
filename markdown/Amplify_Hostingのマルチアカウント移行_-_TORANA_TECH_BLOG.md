# Amplify Hostingのマルチアカウント移行 - TORANA TECH BLOG
[Amplify Hostingのマルチアカウント移行 - TORANA TECH BLOG](https://web.archive.org/web/20241109031930/https://tech.torana.co.jp/entry/2023/04/03/123000)
SREチームのクラシマです。
クラスメソッドメンバーズ組織管理プランへ移行して、IAM Identity Center + GoogleアカウントでAWSアカウントにSSOできてサイコーな日々です。
さて。これまで、1アカウントに本番環境・ステージング環境・QA環境が詰め込んでいたのですが、権限の分離やコストの把握の観点からマルチアカウント移行を実施しました。
terraform管理外のリソースなどもありそれなりの苦労もありつつ、ECSなどの移行が完了。最後に残ったのがAmplify Hostingでした。
さて、1アカウントで環境分離して使うのはAmplifyが得意とするところで、GitHubのリポジトリと連携、特定のブランチやブランチ名のパターンによって環境を分離するのも簡単にできます。
しかし、マルチアカウントになるとなかなか厄介でした...。
### ステージング環境を分離する
弊社では、現時点ではGit Flowを使用しています。feature / develop / masterブランチからそれぞれQA環境 / ステージング環境 / 本番環境が紐付いています。ブランチと環境が1:1になっているステージング環境からまずは分離してみます。
amplify cliでどうにかしたらいけるか？とあれこれ試したもののどうやらbackend以外はamplify push / pullの対象外のようです。諦めてAWSコンソールでポチポチします。弊社ではAmplify HostingでNext.jsを動かしていて、frontendだけがAmplifyの適用範囲です。また、一度はterraform化したものの、applyしたらAmplifyアプリケーションが吹っ飛ぶ障害があり、現時点ではAmplify部分はIaC対象とはしていません。既存リポジトリにamplify.yamlは存在するので、ビルドはうまくいくはず。
と、ビルド時に環境変数から読み込むsecretが読み込めず。パラメータストアでの登録が足りないようです。`/amplify/{your_app_id}/{your_backend_environment_name}/{your_parameter_name}` の形式でパラメータストアに登録すると、SecureStringで登録できて便利です。(知らなかった...。構築した担当はSecretManagerも来てくれと言ってました)
[https://docs.aws.amazon.com/ja_jp/amplify/latest/userguide/environment-variables.html#environment-secrets](https://docs.aws.amazon.com/ja_jp/amplify/latest/userguide/environment-variables.html#environment-secrets)
と、ビルドはうまくいったのですが、今度はAPIが呼べません。CORSエラーがでます。
ということで、カスタムドメインを登録します。
さて、Route53は本番アカウントにありますが、Amplifyが別アカウントのRoute53にレコードを書きに行ってはくれないので、サブドメインの委譲を行います。
いつもお世話になっているDevelopers.ioを参照します。[Route 53でサブドメインを別のHosted Zoneに権限委譲する](https://dev.classmethod.jp/articles/route53-transfer-hostedzones/)

1. ステージングアカウントにサブドメインでホストゾーンを作成する (e.g. stg.example.com)
2. 本番アカウントのホストゾーンに1.で作成したホストゾーン名をNSレコードとして登録する
3. Amplifyコンソールで、ドメインの管理からカスタムドメインに1.で登録したホストゾーンを指定、developブランチとstg.example.comを紐付ける
これで、無事にステージング環境が起動できました。
### QA環境を分離する
既存の本番環境にAmplify環境のqaが存在するため、そのままビルドしたらエラーになりました。はて、と公式ドキュメントを見ると、team-provider-info.json を.gitignore に追加せよと書いてあります。team-provider-info.json には、当該Amplify環境名で使用するIAMロール名などが埋め込んであり、新QA環境には当然そんなものはないので落ちる、というわけですね。
所定のブランチ名パターンでgit pushするとAmplifyがビルドしてURLも発行してくれる便利機能を使って、QA環境を構築します。`feature/epic/**, feature/feat/**, feature/fix/**, ...` のようなブランチ名をpushすると、feature-epic-hoge.example.com が利用できるようになり、カスタムドメインも指定できます。さて、ステージング環境では一つのサブドメインを委譲するだけだったのですが、今回は自動生成されるのですべて登録するというわけにはいきません。
とりあえず、qa.example.comを委譲してカスタムドメインを有効にしてみます。と、feature-epic-hoge.qa.example.com が利用できるようになりました。なるほど、サブドメインのサブドメインまで委譲されるんですね。動かしてみるまでわからなかった...。思ったより簡単に分離できてホッとしました。
### 仕上げ
Amplifyでのビルド結果と接続先URLを通知するLambdaを移植したり、deploy用のGitHub Actionsの向き先を切り替えて、本番環境でのステージング環境・QA環境の自動ビルドを止めて出来上がり。無事に分離できました。

[#トラーナテックブログ](トラーナテックブログ)
