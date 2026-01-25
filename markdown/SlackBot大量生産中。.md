# SlackBot大量生産中。
[SlackBot大量生産中。｜ハンズラボ株式会社](https://www.hands-lab.com/tech/t925/)  の転記です
2015.12.03
BooklogBot作った倉嶋です。
↑は昨日・今日で作った社長の予定を通知するHHBotです。(Hideki Hasegawa Botの略)
今日はLambda＋PythonじゃなくてGoogle Apps ScriptでSlack Bot作った話をば。
おかげ様で前回の投稿は好評いただいたのですが、Lambdaで作ると大量生産には向きません。
もっと遊びたい 基、Slack生活向上のため、もっと簡単に作りたい。
ちょっと調べてみたところ、Google Apps Scriptで作るのが良さそうだ、ということでいくつか作ってみました。
ざっくりお昼休み2,3回に1つくらいのペースでBotが作れます。
以下、作ったBotを順不同に。

  - 今日の予定通知Bot
  - 社内ポータル更新通知Bot
  - 今日のオススメランチBot
  - Slackに新しいチャンネルできたよBot
  - Slackのスターをつけたよ消したよBot
  - 社長の予定通知Bot new!
Google Apps Scriptのいいところ

  - Googleのサービスとの連携が簡単
  - Slack連携のライブラリを公開してくれている方がいる
  - Javascriptで書ける
  - 勝手に版管理してくれる
東急ハンズはGoogle Apps for Businessを全社的に導入していますので、メールはgmail、カレンダーはgoogle calendar、忘年会の出欠簿はgoogle spreadsheetです。
(MS Officeも使っていますが、ハンズラボメンバーはMacユーザも多く、それほど使用頻度は多くないです)
おかげで、gmailやgcalと連携してほしい情報をjsonなどで取ってきて、ちょっと体裁を整えてSlackに投げればBotがすぐに作れます。
Google Apps Scriptの拡張子は.gsですがほぼJavascriptなので、Javascriptの勉強にもなります。

Google Apps Scriptのもう少し・・・なところ

  - Editorが組み込みオブジェクトのメソッド・プロパティは補完してくれない
  - プロジェクトが個人のmailアドレスに紐づくので、作った人が退職したら「権限の譲渡」とかしないと読めなくなる
  - npmなどでライブラリの追加ができない
  - 時間帯指定では起動できるが、時刻指定はできない
    - var dt = new Date(); とかしたらDateオブジェクトのメソッドとか補完してほしいじゃないですか！
  - あとはECMAScript2015対応とかどうなるんですかね？
Google Apps Script、お気軽に作れておすすめです。社内のJavascript勉強会で作り方を共有したので、倉嶋以外が作ったBotもドンドン作られるはず。どんなBotが出てくるか、楽しみです！
— 追記 —
参考にさせていただいたサイトは以下のとおりです。ありがとうございます！
Slack BotをGASでいい感じで書くためのライブラリを作った

  - 今日の予定をまとめて教えてくれるslackの秘書BOT

[#ハンズラボテックブログ](ハンズラボテックブログ)
