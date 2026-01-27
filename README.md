# cosense-content

cosense(https://scrapbox.io/watarukura) のコンテンツバックアップ用リポジトリ

## 必要なツール

- [aqua](https://aquaproj.github.io/) - CLI Version Manager
- [lefthook](https://github.com/evilmartians/lefthook) - Git hooks manager
  - `aqua i` でinstall後、初回のみ `lefthook install`

## 記事を取得する

```shell
# 全件取得→markdown変換
./scripts/download_cosense.bash
# 期間指定
./scripts/download_cosense.bash --since 2021-01-01
# markdown変換のみ
./scripts/convert_markdown.bash --skip-download
```

## Thanks

- https://github.com/matsushinDB11/Scrapbox_to_md