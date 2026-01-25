# aquaとlefthookでREADME.mdを簡素に保つ
[aquaとlefthookでREADME.mdを簡素に保つ - TORANA TECH BLOG](https://web.archive.org/web/20241207140900/https://tech.torana.co.jp/entry/2024/11/12/123000)
2024-11-12
SREのクラシマです。
皆さんのREADME.mdには何が書いてありますでしょうか？
トラーナでは、以下を書くようにしています。

- 開発を始めるために必要なツールのinstallについて
- ローカル開発環境について
- (Option)外部のツールのcredentials周り
- (Option)アーキテクチャ図

基本的にはMacで開発しているのですが、ある人はローカル開発環境を起動できるのに別の人はできない、みたいなことが起きると困ります。
(WindowsやLinuxで開発したい、という方ももちろん歓迎しますが、ドキュメントは用意できていないので開拓いただく必要があります...)
開発ドキュメントがたくさん書いてあると書くのも読むのも更新するのも大変です。どうにか減らしたい。
ということで、リポジトリ共通で導入しているツールについて書きます。

リポジトリに入れているツール

- [GitHub - aquaproj/aqua: Declarative CLI Version manager written in Go. Support Lazy Install, Registry, and continuous update with Renovate. CLI version is switched seamlessly](https://github.com/aquaproj/aqua)
  - 開発周りのツールは、基本的にはaquaでinstallします
- [GitHub - evilmartians/lefthook: Fast and powerful Git hooks manager for any type of projects.](https://github.com/evilmartians/lefthook)
  - Git hookの管理ツールです
  - pre-commit hookでローカルでlint / formatを掛けます
  - 初回だけlefthook install が必要です

共通で入れているlinterは↓こんな感じ

- [GitHub - rhysd/actionlint: :octocat: Static checker for GitHub Actions workflow files](https://github.com/rhysd/actionlint)
  - GitHub Actionsのlinter
  - GitHub Actionsのworkflow、早くしようとすると壊れがちなので大事
- [GitHub - gitleaks/gitleaks: Protect and discover secrets using Gitleaks 🔑](https://github.com/gitleaks/gitleaks)
  - credentials情報をリポジトリ内に置かないようにする
- [GitHub - crate-ci/typos: Source code spell checker](https://github.com/crate-ci/typos)
  - typoチェック
- [GitHub - mvdan/sh: A shell parser, formatter, and interpreter with bash support; includes shfmt](https://github.com/mvdan/sh)
  - シェルスクリプトのformater
- [GitHub - koalaman/shellcheck: ShellCheck, a static analysis tool for shell scripts](https://github.com/koalaman/shellcheck)
  - シェルスクリプトのlinter

aqua.ymlのサンプルは↓こんな感じです。
```aqua.yaml
---
# aqua - Declarative CLI Version Manager
# https://aquaproj.github.io/
registries:
 - type: standard
   # for aqua-renovate-config
   # yamllint disable-line rule:comments
   ref: v4.239.0 # renovate: depName=aquaproj/aqua-registry
packages:
 - name: 99designs/aws-vault@v7.2.0
 - name: direnv/direnv@v2.35.0
 - name: zricethezav/gitleaks@v8.21.1
 - name: evilmartians/lefthook@v1.7.22
 - name: mvdan/sh@v3.10.0
 - name: koalaman/shellcheck@v0.10.0
 - name: rhysd/actionlint@v1.7.3
 - name: jqlang/jq@jq-1.7.1
 - name: cli/cli@v2.59.0
 - name: kayac/ecspresso@v2.4.2
 - name: aws/aws-cli@2.18.10
 - name: crate-ci/typos@v1.26.0

```
このくらい準備すると、最初にaquaさえinstallすれば、対象の言語以外のlinter / formatterが準備完了します。

上記のツールをinstallするためのスクリプトを準備していたのですが、aquaが対応してくれるツールが増えるにつれて段々とスクリプトが短くなってきました。
スクリプト内でjqやghなどのコマンドも必要になるので、これもaqua.ymlに書いておくと実行のタイミングでinstallされるので便利です。

あとは対象の言語用のセットアップをします。npm iする、とかcomposer installする、とかですね。
フロントエンドはNext.jsを使っているのでnext dev、バックエンドの開発はdockerを使っているのでdocker compose upすれば概ねローカル開発環境が起動して開発を開始できます。
(dockerコマンドもaquaでinstallできたほうが良いのですが、DockerDesktopに課金したり課金をやめたりなどの歴史的経緯があって、今のところは各自で用意してね、ということにしています...)

Git hookアレコレ
lefthook.ymlの中身は↓こんな感じです。
```lefthook.yml
---
pre-commit:
  parallel: true
  commands:
    yamllint:
      glob: "*.{yml,yaml}"
      run: |
        if type -a yamllint >/dev/null 2>&1; then
          yamllint -- {staged_files}
        else
          echo "yamllint is not found."
        fi
    shellcheck:
      glob: "*.{sh,bash}"
      run: |
        if type -a shellcheck >/dev/null 2>&1; then
          shellcheck -- {staged_files}
        else
          echo "shellcheck is not found."
        fi
    shfmt:
      glob: "*.{sh,bash}"
      run: |
        if type -a shfmt >/dev/null 2>&1; then
          shfmt -d -s -w -- {staged_files}
        else
          echo "shfmt is not found."
        fi
    actionlint:
      root: ".github/workflows/"
      glob: "*.{yml,yaml}"
      run: |
        if type -a actionlint >/dev/null 2>&1; then
          actionlint
        else
          echo 'actionlint is not found.'
        fi
    gitleaks:
      run: |
        if type -a gitleaks >/dev/null 2>&1; then
          gitleaks protect --staged
        else
          echo "gitleaks is not found."
        fi
    typos:
      run: |
        if type -a typos >/dev/null 2>&1; then
          typos
        else
          echo "typos is not found."
        fi
```
基本的にはpre-commitフックでアレコレlinter / formatterを実行しています。
pre-pushフックでブランチ名をチェックしているリポジトリもあります。
同じlinter / fomatterをGitHub Actionsでも動かしています。
二重で実行されるので無駄感があるのですが、ローカルでコケる方が開発サイクルが早いですし、CI上で実行されることで第三者もCIを通っていることがわかるので、二重での実行とする意味はあると考えています。

まとめ
GoやRustで書かれたツールはおおよそaquaでinstallできて、とても便利です。
また、renovateとも相性が良く、最新のバージョンを追いかけるのもそれほど苦労しません。
yamllint、sqlfluff(Python)やmarkdownlint(JavaScript)の管理には悩むところですが、ここはOSSチャンスかも？
[#トラーナテックブログ](トラーナテックブログ)
