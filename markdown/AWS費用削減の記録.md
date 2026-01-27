# AWS費用削減の記録
[AWS費用削減の記録 - TORANA TECH BLOG](https://web.archive.org/web/20241204193839/https://tech.torana.co.jp/entry/2023/12/19/123000)
2023-12-19

SREのクラシマです。SREを名乗る前から継続しているAWSの費用削減についてのお話です。

スタートアップは事業拡大が最優先なので、四半期ごとにコスト削減活動にも強弱があります。最近はちょっとがんばってたので、記録として。

### コストの可視化

以前からblogでお伝えしている通り、トラーナはクラスメソッドメンバーズを利用しています。とても良いサービスなのですが、副作用としてCostExplorerが利用できなくなります。(実際には、コンソールは利用できるのですが正確な値ではなくなります)

[「AWSコスト最適化ガイドブック」門畑顕博 [ＰＣ・理工科学書](「AWSコスト最適化ガイドブック」門畑顕博 [ＰＣ・理工科学書) - KADOKAWA https://www.kadokawa.co.jp/product/322104000266/]こちらの本でも「まずは可視化」と書いてありますが、残念ながら一工夫いります。

クラスメソッドメンバーズポータルを開くと、各アカウントの合計金額と日次推移は見られます。が、複数アカウントを一覧で見たい、各AWSサービスの何にいつコストがかかっているか把握したい、となると足りなくなります。

ということで、CostUsageReport(以下、CUR)の出番です。
[コストと使用状況レポート（CUR） — メンバーズポータル ユーザーガイド 2023-09-19 ドキュメント](https://members.classmethod.net/userguide/mcur.html)AWS公式のCURではなく、クラスメソッドさん謹製のCURを使用します。(比較したことがないので項目などに差異があるかは未把握...)
で、S3にCSVが出力されるので、これをAthenaでクエリしてredashから参照します。

[https://gyazo.com/b1aa27b739432eba79e7264cbd495fcd](https://gyazo.com/b1aa27b739432eba79e7264cbd495fcd)

ざっとこんなSQLを書けばアカウント別、サービス別、時刻別に集計できます。日ごとではなく時刻ごとなので、より細かく、AutoScalingしている日中帯に何にコストが掛かっているかなどを把握できます。

```(sql)
select
  lineitem_productcode,
  lineitem_usagestartdate,
  lineitem_usageenddate,
  sum(cost) as cost
from
  (
    select
      "lineitem_productcode",
      "lineitem_usagestartdate",
      "lineitem_usageenddate",
      sum("lineitem_unblendedcost") as cost
    from
      "cur_all_accounts"
    where
      date = DATE_FORMAT(date('{{ start }}'), '%Y%m')
      and lineitem_usageaccountid = {{ aws_account_id }}
      and "lineitem_usagestartdate" between '{{ start }}'
      and '{{ end }}'
    group by
      "lineitem_productcode",
      "lineitem_usagestartdate",
      "lineitem_usageenddate"
  ) tmp
group by
  lineitem_productcode,
  lineitem_usagestartdate,
  lineitem_usageenddate
order by
  lineitem_productcode,
  lineitem_usagestartdate;

```
### 実際のコスト削減施策

前述のAWSコスト最適化ガイドブックや、↓こちらのblogを参照して、大きなところから実施します。[https://aws.amazon.com/jp/blogs/news/9ways-to-optimize-aws-cost/](https://aws.amazon.com/jp/blogs/news/9ways-to-optimize-aws-cost/)


```(txt)
#1　未使用状態のAmazon EC2やAmazon RDS インスタンスへの支払いを止める
#2　未使用状態の Amazon Redshift クラスターへの支払いを止める
#3　Amazon S3 Intelligent-Tieringを有効にする
#4　Amazon DynamoDB にはオンデマンドのキャパシティーモードを利用する
#5　十分に活用されていないEC2 インスタンスへの支払いを止める
#6　十分に活用されていないネットワークリソースを削除する
#7　EC2 スポットインスタンス を利用する
#8　Compute Savings Plans を利用する
#9　リザーブドインスタンスを利用する

```
一番効いたのはRDSを始めとしたデータストア類のRIの購入です。次点でSavingsPlansですが、AutoScaleしていない夜間帯のワークロードの8 - 9割程度を賄う形で購入しているため、それほど大きくはありません。
未使用や、十分に活用されていないインスタンス、というのは、スタートアップのリソースの中にはそれほど無いものです。特に、terraform等でIaCしている場合には。また、ステージング環境や、一部の本番環境ではFARGATE_SPOTも利用しています。

ちなみに、「#3　Amazon S3 Intelligent-Tieringを有効にする」ですが、必ずしもコスト削減につながるとは限りません。ログファイルのような、ファイルサイズの比較的小さいものが多数存在する場合ですと、Tieringの変更にかかるコストの方が保管コストより大きくなってしまいます。...ということが一時間ごとのコスト把握をグラフで可視化して毎日見ているとわかるのです。(実際にやってみて、数日経ってわかりました...)

上記に記載のないものでは、以前にblogにしたデータストアのGraviton2移行やEC2->Fargate移行があります。[https://tech.torana.co.jp/entry/2022/02/07/000000](https://tech.torana.co.jp/entry/2022/02/07/000000)[https://tech.torana.co.jp/entry/2023/02/17/123000](https://tech.torana.co.jp/entry/2023/02/17/123000)

### コスト削減の進め方

四半期ごとに親Issueを立てて、その中で個別のIssueをタスクリストを使って管理しています。以下は前Qのものです。[https://gyazo.com/da0e435560363881ee20e67f778aa533](https://gyazo.com/da0e435560363881ee20e67f778aa533)

一通り大きな物を片付けると、後は小さいコスト削減を積み重ねるしかありません。また、AWS以外のコスト削減にもバランスよく目を向け、効果の望めるものから着手する必要があります。(GitHub ActionsのBuildJet移行とか...。結構いい感じの額が削減できました)

コスト削減のアイデアが欲しくてAWSコスト削減診断を提供している某社に診断いただきましたが、あまり削減余地がない、ということで契約にはいたらず...。
ただ、RDSのバックアップ・リストアはPITRの利用をおすすめいただき、これは大変助かりました！従来はGitHub Actionsから30分おきにスナップショットを作るスクリプトを動かしており、上限まで溜め込んでいました。日次のスナップショットがあればPITRを使って任意の時点に戻せるので、不要とわかりました。

その他の小さなコスト削減で言うと、以下のような施策を実施しました。

- QA環境のAWS WAFの停止
- 本番環境・ステージング環境では稼働させたままにし、開発中のフィーチャーごとに構築するQA環境では停止した
- ステージング環境からDatadogへのMetrics Stream、およびcontainer insightsの停止
- AWS ConfigからEC2:NetworkInterfaceの記録の停止
- [https://aws.amazon.com/jp/blogs/news/announcing-aws-config-now-supports-recording-exclusions-by-resource-type/](https://aws.amazon.com/jp/blogs/news/announcing-aws-config-now-supports-recording-exclusions-by-resource-type/) を参考に、管理アカウントからCloudFormationを実行
- 開発用ALBの集約
- 複数のステージング環境で共用するALBを一つつくり、ホスト名で振り分けをしています
- [https://tech.torana.co.jp/entry/2023/09/28/123000](https://tech.torana.co.jp/entry/2023/09/28/123000) などで使用しています


また、re:invent 2023の発表より、以下を実施中です。

- Cloudwatch Logsのlog classをINFREQUENT_ACCESSに変更
- terraform-provider-awsにもすでに来ているので、Lambda等のログはこちらに変更
- [https://github.com/hashicorp/terraform-provider-aws/issues/34570](https://github.com/hashicorp/terraform-provider-aws/issues/34570)
- AWS Configの定期記録
- こっちはterraform待ちで未着手
- [https://github.com/hashicorp/terraform-provider-aws/issues/34577](https://github.com/hashicorp/terraform-provider-aws/issues/34577)


### まとめ

月次のAWSコスト推移、なかなか順調に下がっています。
[https://gyazo.com/8b06dbc66ef0c8c86d37703e4b2949b7](https://gyazo.com/8b06dbc66ef0c8c86d37703e4b2949b7)

[#トラーナテックブログ](トラーナテックブログ)
