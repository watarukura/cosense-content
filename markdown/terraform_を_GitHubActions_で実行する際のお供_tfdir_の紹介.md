# terraform を GitHubActions で実行する際のお供 tfdir の紹介
[terraform を GitHubActions で実行する際のお供 tfdir の紹介 - TORANA TECH BLOG](https://web.archive.org/web/20241207133409/https://tech.torana.co.jp/entry/2024/08/08/123000)
2024-08-08
SREのクラシマです。
トラーナで公開しているOSS、tfdirを紹介します。

以下のようなterraformのディレクトリ構成を取っているとします。
```tree.bash
❯ tree
.
├── environment
│   ├── prd
│   │   └── backend
│   │       └── main.tf
│   └── stg
│       └── backend
│           └── main.tf
└── modules
└── backend
└── hoge.tf
```
environment ディレクトリ配下で修正があった場合は、同ディレクトリへ移動して plan / apply を行えばよいです。
modules/backend に修正があった場合は、environment/prd/backend、environment/stg/backend の双方で plan / apply を行う必要があります。
この、依存関係の判定を自動的に行えればいいのにな、ということで、Hashicorp公式が GitHub - hashicorp/terraform-config-inspect: A helper library for shallow inspection of Terraform configurations というツールを出してくれています。
コマンドラインで実行すると、依存しているmoduleが判定できるツールです。
```terraform-config-inspect.bash
❯ cd environment/stg/backend
❯ terraform-config-inspect . --json | jq -r .module_calls
{
  "backend": {
    "name": "backend",
    "source": "../../../modules/backend",
    "pos": {
      "filename": "main.tf",
      "line": 1
    }
  }
}
```
上記 terraform-config-inspect をラップしてCIから使いやすくしたのが tfdir です。
まず、設定ファイルを作ります。

```.tfdir/pull_request/develop.yaml
ExecutedDirs:
  "environments/prd/backend"
  "environments/stg/backend"

```
で、modules 配下で更新差分を作って、tfdir get に渡すと、以下のように modules に依存している environments が抽出できます。
```git-diff.bash
❯ git diff --name-only terraform
modules/backend/hoge.tf
❯ git diff --name-only terraform | tfdir get --config .tfdir/pull_request/develop.yaml
environments/prd/backend
environments/stg/backend
```
トラーナでは、feature ブランチで開発、staging ブランチへのマージ時に staging 環境へデプロイ、動作確認後に master ブランチへマージ時に production 環境へデプロイ、としています。
stagingブランチへプルリクエストでは staging / production の双方で plan が動作してほしい、などを設定ファイルで制御ができます。
GitHub Actions に組み込むときは↓こんな感じ
```tfdir.yaml
on:
  pull_request:
     paths:
       - '**.tf'
jobs:
  get_target_dirs:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - name: install tfdir
        run: |
          curl "https://raw.githubusercontent.com/torana-us/tfdir/master/installer.sh" | bash
      - name: target branch
        id: target_branch
        run: |
          set -xv
          branch=""
          from=""
          to=""
          if [ "$GITHUB_EVENT_NAME" = "push" ]; then
            branch="$GITHUB_REF_NAME"
            from="${{ toJSON(github.event.before) }}"
            to="${{ toJSON(github.event.after) }}"
          else
            branch="$GITHUB_BASE_REF"
            from="origin/$GITHUB_BASE_REF"
            to="${GITHUB_REF/refs\//}"
          fi
          {
            echo "branch=$branch"
            echo "from=$from"
            echo "to=$to"
          } >> "$GITHUB_OUTPUT"
      - name: get diff
        run: |
          set -xv
          diff=$(git diff --diff-filter="AMRCD" \
                  --name-only \
                  "${{ steps.target_branch.outputs.from }}...${{ steps.target_branch.outputs.to }}" \
                  -- "**.tf" \
                  | xargs)
          echo "GIT_DIFF=$diff" >> "$GITHUB_ENV"
      - name: get target dir
        id: target_dirs
        run: |
          set -xv
          targets=$(echo ${{ env.GIT_DIFF }} \
            | tr ' ' '\n' \
            | ./tfdir get --config "./.tfdir/$GITHUB_EVENT_NAME/${{ steps.target_branch.outputs.branch }}.yaml" \
            | jq -cnR '[inputs | select(length > 0)]')
          echo "targets=$targets" >> "$GITHUB_OUTPUT"
```
get_target_dirs の output を使って、matrix strategy で plan / apply を実行しています。

まとめ
GitHub - suzuki-shunsuke/tfaction: Framework for Monorepo to build high level Terraform Workflows by GitHub Actions や GitHub - terramate-io/terramate: Terramate CLI is an open-source Infrastructure as Code (IaC) Orchestration and Code Generation tool for Terraform, OpenTofu and Terragrunt. でも同じことはできますが、tfdir はちっちゃいツールなので小回りが効きます。
よかったら使ってみてください！
[#トラーナテックブログ](トラーナテックブログ)
