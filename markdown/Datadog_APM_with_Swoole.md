# Datadog APM with Swoole
[Datadog APM with Swoole - TORANA TECH BLOG](https://web.archive.org/web/20250120125705/https://tech.torana.co.jp/entry/2024/05/20/123000)
2024-05-20
SREのクラシマです。

さて、久々にSwooleの話を。
X(旧Twitter)でDatadog APMがSwooleと一緒だと動かなくて悲しいとつぶやいたところ、親切な方が「動くようになったらしいよ」と教えて下さいました。
これは検証するしかない！

Tracing with async/CLI setups · Issue #704 · DataDog/dd-trace-php · GitHub こちらがSwooleとFrankenPHPでDatadog APMが動くようになったIssueです。2020年初出。
弊社からもDatadog社の営業の方へ要望をあげたりしましたが、ようやく実現して感無量です。
注意事項として、現時点(2024-05-17現在)ではOpenSwooleには未対応です。
トラーナ社ではOpenSwooleに移行してしまったので出戻りしないといけません。
まぁ、Swoole 4.6.xでは動いてましたし、なんとかなるでしょう。

なお、弊社のプロダクトはLaravel Octaneではなくlaravel-swooleを使用しています。
Bug: Laravel Octane traces not showing in dashboard · Issue #2636 · DataDog/dd-trace-php · GitHub Octaneでの動作に苦戦している方もいらっしゃるようで、不幸中の幸いかもしれません。
(いずれはOctane移行したい)

Swooleをインストール
Release v5.1.2 · swoole/swoole-src · GitHub 最新のSwooleはv5.1.2です。
なぜかpecl install swoole-5.1.2するとエラーに。

PECL release of swoole 5.1.2 · Issue #5242 · swoole/swoole-src · GitHub 2024-05-10まで存在しませんでした...。
6.0.0の開発に忙しいとのコメントがあり、活発に開発が継続している模様です。

Swoole -> OpenSwooleへの書き換え時に修正した箇所で、「OpenSwooleが読み込まれていたら」を「SwooleかOpenSwooleが読み込まれていたら」に書き換えます。
ide-helperもSwoole用に切り替えて、CIを回すとphpstanが大量に警告を出しました。
phpstan-baseline.neonを再生成して、修正は後回し...。

ローカル環境でdocker buildに成功、stg環境にdeployして動作確認。
どうやら動きそうです。

Datadog APMを有効化する
dd-trace-php 0.99.1 をinstallして、ECSタスクの環境変数を設定します。
https://github.com/DataDog/dd-trace-php/issues/704#issuecomment-2050158934 先ほども記載したIssueに環境変数の例が乗っているので、ありがたく拝借。
ECSタスク定義を編集し、改めてstg環境にdeployします。
↓最終的に動いたタスク定義はこんな感じです。GitHub - kayac/ecspresso: ecspresso is a deployment tool for Amazon ECSを使っているので、タスク定義はJSONファイルとして管理しています。

```taskdef.json
{
  "containerDefinitions": [
    {
      "cpu": 0,
      "dependsOn": [
        {
          "containerName": "datadog-stg",
          "condition": "HEALTHY"
        }
      ],
      "essential": true,
      "image": "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/api-stg:{{ env `IMAGE_TAG` `latest` }}",
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "stg",
          "awslogs-region": "ap-northeast-1",
          "awslogs-stream-prefix": "api-stg",
          "awslogs-datetime-format": "\\[%Y-%m-%d %H:%M:%S\\]"
        },
        "secretOptions": [
          {
            "name": "apikey",
            "valueFrom": "/api-stg/datadog/key"
          }
        ]
      },
      "name": "api-stg",
      "portMappings": [
        {
          "appProtocol": "",
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DD_TRACE_PHP_BIN",
          "value": "/usr/local/bin/php"
        },
        {
          "name": "DD_TRACE_CLI_ENABLED",
          "value": "true"
        },
        {
          "name": "DD_TRACE_SWOOLE_ENABLED",
          "value": "true"
        },
        {
          "name": "DD_TRACE_LARAVEL_ENABLED",
          "value": "true"
        },
        {
          "name": "DD_SERVICE",
          "value": "madras"
        },
        {
          "name": "DD_VERSION",
          "value": "{{ env `IMAGE_TAG` `latest` }}"
        },
        {
          "name": "DD_TRACE_SIDECAR_TRACE_SENDER",
          "value": "1"
        },
        {
          "name": "DD_ENV",
          "value": "staging"
        },
        {
          "name": "DD_AGENT_HOST",
          "value": "localhost"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "/rds/stg/password"
        },
        {
          "name": "DB_USERNAME",
          "valueFrom": "/rds/stg/username"
        },
        {
          "name": "DD_API_KEY",
          "valueFrom": "/api-stg/datadog/key"
        }
      ],
      "ulimits": [
        {
          "hardLimit": 1006500,
          "name": "nofile",
          "softLimit": 1006500
        },
        {
          "hardLimit": 1006500,
          "name": "nproc",
          "softLimit": 1006500
        }
      ],
      "workingDirectory": "/var/www/html",
      "systemControls": [
        {
          "namespace": "net.ipv4.tcp_syncookies",
          "value": "1"
        },
        {
          "namespace": "net.ipv4.tcp_max_syn_backlog",
          "value": "81920"
        },
        {
          "namespace": "net.ipv4.tcp_synack_retries",
          "value": "3"
        },
        {
          "namespace": "net.ipv4.tcp_fin_timeout",
          "value": "30"
        },
        {
          "namespace": "net.ipv4.tcp_keepalive_time",
          "value": "300"
        },
        {
          "namespace": "net.ipv4.tcp_tw_reuse",
          "value": "1"
        },
        {
          "namespace": "net.ipv4.ip_local_port_range",
          "value": "20000 65000"
        },
        {
          "namespace": "net.ipv4.tcp_max_tw_buckets",
          "value": "200000"
        },
        {
          "namespace": "net.ipv4.tcp_syn_retries",
          "value": "3"
        },
        {
          "namespace": "net.ipv4.tcp_wmem",
          "value": "4096 16384 4194304"
        },
        {
          "namespace": "net.ipv4.tcp_rmem",
          "value": "4096 16384 4194304"
        }
      ]
    },
    {
      "cpu": 0,
      "essential": true,
      "image": "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/nginx-stg:{{ env `IMAGE_TAG` `latest` }}",
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "stg",
          "awslogs-region": "ap-northeast-1",
          "awslogs-stream-prefix": "nginx-stg"
        }
      },
      "name": "nginx-stg",
      "portMappings": [
        {
          "appProtocol": "",
          "containerPort": 8080,
          "hostPort": 8080,
          "protocol": "tcp"
        }
      ]
    },
    {
      "cpu": 0,
      "environment": [
        {
          "name": "ECS_FARGATE",
          "value": "true"
        },
        {
          "name": "DD_APM_ENABLED",
          "value": "true"
        },
        {
          "name": "DD_APM_NON_LOCAL_TRAFFIC",
          "value": "true"
        }
      ],
      "essential": false,
      "image": "public.ecr.aws/datadog/agent:latest",
      "name": "datadog-stg",
      "portMappings": [
        {
          "appProtocol": "",
          "containerPort": 8126,
          "hostPort": 8126,
          "protocol": "tcp"
        }
      ],
      "healthCheck": {
        "retries": 3,
        "command": [
          "CMD-SHELL",
          "agent health"
        ],
        "timeout": 5,
        "interval": 30,
        "startPeriod": 15
      },
      "secrets": [
        {
          "name": "DD_API_KEY",
          "valueFrom": "/api-stg/datadog/key"
        }
      ]
    }
  ],
  "cpu": "***",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecs-task-execution-role-stg",
  "family": "madras-api-stg",
  "ipcMode": "",
  "memory": "***",
  "networkMode": "awsvpc",
  "pidMode": "",
  "requiresCompatibilities": [
    "FARGATE"
  ],
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecs-task-role-stg"
}

```
試行錯誤
ちなみに、↑にたどり着くまで3営業日くらいかかりました。
(もちろん、他の開発タスクの合間を縫って検証しているわけですが...)
Datadog APMコンソールにTraceがでてこない、がスタートです。

ECS Execでコンテナに入ってartisanコマンドを実行するとTraceが表示されました。
どうやら、アプリケーションとdd-agent、Datadogの設定には問題なさそうです。
リクエストをhookしてTraceを始めるところがうまくいってないのかと推測。

Bug: Laravel Octane traces not showing in dashboard · Issue #2636 · DataDog/dd-trace-php · GitHub
先ほどの「Octaneで動かない」のIssueを見ると、laravel.request の文字があります。
雰囲気でこれをhookしているのかとアタリをつけてdd-trace-phpのコード中を検索すると、どうやらそれっぽい。
dd-trace-php/src/DDTrace/Integrations/Laravel/LaravelIntegration.php at 48190be6f5d8f4b500345923d193a333675fc6ff · DataDog/dd-trace-php · GitHub

普通のLaravelならLaravel Integrationを有効にするだけで動くはずなのですが、
弊社の魔改造Laravelでは動かない様子。
調べてみると、リクエストの開始時にswoole.request というイベントを発行していました。
これをlaravel.request に書き換えてみると、動きました！

やったぜ、と思ったのもつかの間、なぜかAPMが表示されるRouteとされないRouteがあります。
GETはおおよそ表示されるのですが、PATCH・POSTは表示されないのです。
さっぱり原因がわかりませんが、PATCH・POST時のログにtrace_id、span_idを出力するよう仕込んでみると、発行されています。
Traceが開始しているものの、終了していないのでは？と、app->terminate()後に\DDTrace\flush()を指定してみると、今度こそ良さそうです！
[https://gyazo.com/ba58d8f6f3e0f4ac499f61f7fa9b9f7a](https://gyazo.com/ba58d8f6f3e0f4ac499f61f7fa9b9f7a)

まとめ
開発開始から4年ちょっと、悲願だったAPMが動作するようになりました！
これを機に性能改善につなげ、より使いやすく安定したプロダクトに成長させていきたいところです。
[#トラーナテックブログ](トラーナテックブログ)
