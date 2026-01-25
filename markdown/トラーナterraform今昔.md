# トラーナterraform今昔
[トラーナterraform今昔 - TORANA TECH BLOG](https://web.archive.org/web/20241102111514/https://tech.torana.co.jp/entry/2024/01/12/123000)
2024-01-12
SREのクラシマです。
トラーナに入社してから、terraformを触るようになりました。
入社後の2年の間に、さまざまな変化があったので、まとめてみようと思います。

最初期
トラーナ開発部最初のプロダクトであるMadrasは、上から下まで元CTOが土台を書いています。
React + Next.jsでfrontendを書き、PHP + Laravel + Swooleでbackendを書き、terraformでIaC。
で、自分の入社とともにterraform部分を引き継ぎ、stg環境だけdeployされて開発が走っていて、本番環境を作るところから参入。
当時のディレクトリ構成はこんな感じでした。

```tree-1st.bash
❯ ls -l
-rw-r--r--  1 watarukura staff   1185  6 14 19:57 main.tf
-rw-r--r--  1 watarukura staff    157  6 14 19:57 meta.tf
drwxr-xr-x 24 watarukura staff    768  6 14 19:57 modules
-rw-r--r--  1 watarukura staff 178905  6 14 19:57 terraform.tfstate
-rw-r--r--  1 watarukura staff 456353 10 21  2021 terraform.tfstate.backup
-rw-r--r--  1 watarukura staff    219  6 14 19:57 terraform.tfvars
-rw-r--r--  1 watarukura staff    411  6 14 19:57 variables.tf
❯ tree -d modules/
modules/
├── acm
├── analyze
├── app
│   ├── files
│   └── modules
│       └── iam_instance_profile
├── cache
├── cdn
├── cognito
├── common
│   ├── base
│   └── domain
│       └── aws
├── database
│   ├── read
│   └── write
├── deploy
├── deployment
├── env
│   ├── prd
│   └── stg
├── frontend
├── iam_service_role
├── network
│   └── modules
│       └── subnet
├── oidc
├── rds
├── search
├── search_engine
├── security
├── security_group
├── servers
│   └── api
└── storage

```
terraform.tfstateがGit管理されていました。
また、EC2用のpackerスクリプトや、Dockerfileなども同じリポジトリで管理していました。

2ndプロダクト期
2つ目のプロダクトであるOrtegaの開発時点では、frontendチーム・backendチームが分かれ、インフラはbackendチームが見ることに。
terraformもbackendアプリケーションと一緒に管理する、というところからスタートしました。

```tree-2nd.bash
❯ tree -d -L 1
.
├── app
├── bin
├── bootstrap
├── config
├── database
├── docs
├── graphql
├── migrations
├── public
├── resources
├── routes
├── storage
├── terraform
└── tests

```
インフラ担当増員期
エンジニア採用が進み、terraformを書くメンバーが1人ではなくなったため、複数人で同時にterraformのコードを書いても大丈夫なようにしなければいけなくなりました。
ローカルからAdminロールを使ってterraform applyしてはいけないし、tfstateのGit管理もやめます。
backendアプリケーションで管理していたterraformのコードは分離、代わりに、Docker周りのコードをbackendアプリケーションに引き渡しました。

Terraform Cloud導入
プルリク作ったらplan
所定のブランチへのマージをトリガにapply
tfstateのGit管理をやめてTF Cloudで管理
OIDCが利用できるようになりセキュアに
Terraform Standard モジュール Structureの採用
main.tfって名前じゃなくても良いルールにはした
めったに更新されないnetworkやdatabaseと、頻繁に更新されるapp、などでtfstateを分離
ディレクトリ構成の移行とtfstateの分割のためにtfstateファイルを切り貼り...
当時はmovedブロックがなかった...
SREチーム立ち上げに合わせて、2ndプロダクトからもterraformディレクトリを分離して別リポジトリに。

Terraform整理＋試行錯誤期
Pull Request上でplan結果が見たい！ 更新差分だけplan/applyしたい！
内部統制とかもいろいろやらなきゃ！ということでアレコレ変更..。

Git diffからterraformコードの更新があったディレクトリを検知する自作CLIツールを作成
Terraform CloudからS3にバックエンドを戻し、GitHub Actions上でplanを実行
tfcmtを導入して見やすく
Terragruntを導入して、terraformの設定周りのコードの重複を排除
Terraform Cloudを共通モジュール置き場として活用
後、GitHubリポジトリをモジュール置き場として使える事がわかり、Terraform Cloudの価格変更もあって利用停止
terraformコードでECSタスク定義を管理するツラミもあり、ecspressoを導入
tflint / terraform fmt / terraform validate / tfsec(後にtrivyに移行)をGitHub Actionsおよびlefthookで実行
lintが実行されて安心
renovate + aquaでterraformバイナリおよびterraform-providerのバージョン管理
原則、最新版に追随
Atlantisの導入検証
実行環境を準備するのが面倒で断念
branch-deployの導入検証
GitHub Enterpriseへ契約をアップグレードする必要があり断念
```tree-latest.bash
❯ tree -d -L 4
.
├── environments
│   ├── prd
│   │   ├── aws
│   │   │   ├── analyze
│   │   │   ├── backend
│   │   │   ├── backend_deploy
│   │   │   ├── cache
│   │   │   ├── frontend
│   │   │   ├── network
│   │   │   └── settings
│   │   └── datadog
│   ├── qa
│   │   ├── aws
│   │   │   ├── app
│   │   │   └── domain
│   │   └── datadog
│   └── stg
│       ├── aws
│       │   ├── analyze
│       │   ├── backend
│       │   ├── backend_deploy
│       │   ├── cache
│       │   ├── domain
│       │   ├── frontend
│       │   ├── network
│       │   ├── oidc
│       │   ├── settings
│       │   └── vrt
│       └── datadog
└── modules
    ├── aws
    │   └── service
    │       ├── analyze
    │       ├── backend
    │       ├── backend_deploy
    │       ├── cache
    │       ├── frontend
    │       └── network
    └── datadog

```
まとめ
ようやくterraform運用が固まってきて、最近は大きな変更はありませんが、OpenTFがやはり気になるところ。
今後も改善を続けていきます。
[#トラーナテックブログ](トラーナテックブログ)
