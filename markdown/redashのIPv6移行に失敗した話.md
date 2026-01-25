# redashのIPv6移行に失敗した話
[redashのIPv6移行に失敗した話 - TORANA TECH BLOG](https://web.archive.org/web/20250120130148/https://tech.torana.co.jp/entry/2023/08/24/123000)
2023-08-24
SREのクラシマです。今回も失敗した話をば。



[https://aws.amazon.com/jp/blogs/news/new-aws-public-ipv4-address-charge-public-ip-insights/](https://aws.amazon.com/jp/blogs/news/new-aws-public-ipv4-address-charge-public-ip-insights/)
2024年2月よりPublic IPv4への課金が開始されるという話が出たので、社内でのPublic IPv4アドレスをカウントしたところ、金額がそれなりになりそうなので対策することにしました。とはいえ、これまですべてのサービスでIPv4のみを利用、NAT GW費用もかけたくないのでPublic Subnetにサービスを構築しています。また、[https://developers.cyberagent.co.jp/blog/archives/43423/](https://developers.cyberagent.co.jp/blog/archives/43423/) を拝読すると、CloudFrontのオリジンにはまだIPv6が未対応とのこと。弊社のプロダクトではAPIサーバの前にCloudFrontを置いているケースや、WordPressの前にCloudFrontを置いているケースがあり、移行対象外にせざるを得ないものも散見されます。そんな中、先日引っ越しブログを書いた[[https://tech.torana.co.jp/entry/2023/07/03/120000](https://tech.torana.co.jp/entry/2023/07/03/120000)は独立したVPCで動作しており、CloudFrontなども配置しておらず、最初にIPv6移行を試して見るにはちょうど良さそう、ということで移行してみたのですが...。 https://tech.torana.co.jp/entry/2023/07/03/120000:title]は独立したVPCで動作しており、CloudFrontなども配置しておらず、最初にIPv6移行を試して見るにはちょうど良さそう、ということで移行してみたのですが...。]

### ネットワークのIPv6移行

terraform管理しているVPC/Subnet/IGW/RouteTableをdualstackに切り替えます。
ざっくり、以下の対応を実施。

1. VPCにIPv6 CIDRを付与。特にこだわりがないのでAWSから自動でアサインされるものをそのまま使います
2. 3AZ構成のサブネットそれぞれにIPv6 CIDRを付与、その際にDNS64/リソース作成時IPv6自動付与/起動時DNS AAAAレコード有効化をそれぞれONに
3. route tableにIPv6でのIGWへのルート(`::/0`)を付与


```(hcl)
module "subnet" {
  source = "../../"

  for_each = local.subnets

  vpc_id          = aws_vpc.vpc.id
  az              = each.value.az
  cidr_block      = each.value.cidr_block
  ipv6_cidr_block = each.value.ipv6_cidr_block
  gateway_route = {
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.gateway.id
  }
  gateway_route_ipv6 = {
    destination_cidr_block = "::/0"
    gateway_id             = aws_internet_gateway.gateway.id
  }
  name = each.key
}

locals {
  cidr_block = "192.168.0.0/16"
  subnets = {
    subnet-1a_1 = {
      az              = "ap-northeast-1a"
      cidr_block      = cidrsubnet(local.cidr_block, 8, 1)
      ipv6_cidr_block = cidrsubnet(aws_vpc.vpc.ipv6_cidr_block, 8, 1)
    }
    subnet-1c_1 = {
      az              = "ap-northeast-1c"
      cidr_block      = cidrsubnet(local.cidr_block, 8, 2)
      ipv6_cidr_block = cidrsubnet(aws_vpc.vpc.ipv6_cidr_block, 8, 2)
    }
    subnet-1d_1 = {
      az              = "ap-northeast-1d"
      cidr_block      = cidrsubnet(local.cidr_block, 8, 3)
      ipv6_cidr_block = cidrsubnet(aws_vpc.vpc.ipv6_cidr_block, 8, 3)
    }
  }
}

resource "aws_vpc" "vpc" {
  cidr_block                       = local.cidr_block
  assign_generated_ipv6_cidr_block = true
}

```
```(hcl)
locals {
  ipv6_only   = var.cidr_block == null
  ipv6_enable = var.ipv6_cidr_block != null
}

resource "aws_subnet" "this" {
  cidr_block        = var.cidr_block
  vpc_id            = var.vpc_id
  availability_zone = var.az

  ipv6_cidr_block                                = var.ipv6_cidr_block
  ipv6_native                                    = local.ipv6_only
  enable_dns64                                   = local.ipv6_enable
  assign_ipv6_address_on_creation                = local.ipv6_enable
  enable_resource_name_dns_aaaa_record_on_launch = local.ipv6_enable

  tags = {
    Name = var.name
  }
}

resource "aws_route_table" "this" {
  vpc_id = var.vpc_id

  tags = {
    Name = var.name
  }
}

resource "aws_route_table_association" "this" {
  route_table_id = aws_route_table.this.id
  subnet_id      = aws_subnet.this.id
}

resource "aws_route" "gateway" {
  count = var.gateway_route == null ? 0 : 1

  route_table_id         = aws_route_table.this.id
  destination_cidr_block = var.gateway_route.destination_cidr_block
  gateway_id             = var.gateway_route.gateway_id
}

resource "aws_route" "gateway_ipv6" {
  count = var.gateway_route_ipv6 == null ? 0 : 1

  route_table_id              = aws_route_table.this.id
  destination_ipv6_cidr_block = var.gateway_route_ipv6.destination_cidr_block
  gateway_id                  = var.gateway_route_ipv6.gateway_id
}

```
切り替え自体はサービスダウンなしにうまくいきましたが、terraform-provider-aws v5.13.0以前だとIPv6 CIDRのアサインとIPv6関連フラグの有効化の順序が逆でapplyで落ちました。[https://github.com/hashicorp/terraform-provider-aws/pull/32896](https://github.com/hashicorp/terraform-provider-aws/pull/32896) ちんまりとしたコントリビューションですが、自分が使っているツールに貢献できて嬉しいところ。

### ALB/ECS FargateのIPv6移行

ALBをにIPアドレスタイプをdualstackに切り替え、セキュリティグループもIPv6からの接続に対応します。ターゲットグループもIPアドレスタイプをIPv6に切り替えるのですが、こちらは再作成になってしまうので、BLUE/GREEN DEPLOYMENT構成の場合は片側ずつ切り替えてやるのが良さそうです。

...と、ここまでは想定して手順書を組み立てていたのですが、「ターゲットグループの再作成めんどいなぁ」と日程調整しているある日...。

### redashが沈黙

...稀によくあるやつで、重いクエリを投げつけたところredashが沈黙、CPUが100%に張り付いてうんともすんとも言わなくなりました。EC2の頃はサーバ再起動用のGHAを用意していたのですが、Fargate移行後は手作業で再デプロイが必要です。(自動化しないとなぁ)また、現行のredashが使用しているRQ Schedulerのバージョンが古く、scheduler更新に失敗する場合があります。[https://dev.classmethod.jp/articles/fix-redash-scheduler-error-by-rq-scheduler/](https://dev.classmethod.jp/articles/fix-redash-scheduler-error-by-rq-scheduler/)(最近、redashリポジトリの更新が盛んになっていて、RQ Schedulerのバージョンも上がっているので、次期バージョンでは直るはず！)

ということで、デプロイして次のschedulerが起動する前にredashが利用しているredisに接続してFLUSHDBを実行します。さて、と待っているとworker、schedulerは正常起動したものの、serverが起動しません。WORKER_TIMEOUTが発生します。Gunicornのタイムアウトは120秒に設定しており、前回のデプロイ時から特に変更してないのにおかしい、と数回デプロイを繰り返しますが起動せず。redash停止から1時間ほどして、IPv6を無効化してみたところserverが起動してことなきを得ました。

### ポストモーテム

根本原因として、[https://github.com/benoitc/gunicorn/issues/1628](https://github.com/benoitc/gunicorn/issues/1628) どうやらGunicornがIPv6未対応のようです。Subnetの設定で、リソース作成時にIPv6を付与するようにしたため、既存のインスタンスにはIPv4のみがアタッチされていましたが、新規のインスタンスにはIPv6がアタッチされたために発生したものと推定しています。教訓: WebサーバがIPv6対応しているかを事前調査しましょう

ということで、改めて他のプロダクトも調査しましたがIPv6移行できそうな対象がほぼないことがわかりました...。ステージング環境は3AZ -> 2AZにしてALBのIPアドレスを削減したり、Internal ALBへの切り替えなどで対応することを検討しようと思います。
[#トラーナテックブログ](トラーナテックブログ)
