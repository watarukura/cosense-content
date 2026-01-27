# nix

    - やりたいこと(vim-jp-slackで相談した)
        - 複数のPHPバージョンを同居させたい
- 開発するリポジトリごとに、PHPのバージョンはパッチバージョンまで固定したい
- EoL済みのPHP5系、7系が必要になることがある
    - [https://lazamar.co.uk/nix-versions/?channel=nixpkgs-unstable&package=php](https://lazamar.co.uk/nix-versions/?channel=nixpkgs-unstable&package=php)
    - ↑全パッチバージョン、ある
- [https://nix.dev/manual/nix/2.28/installation/uninstall.html](https://nix.dev/manual/nix/2.28/installation/uninstall.html)
    - 念の為uninstall方法を確認しておく
- nixはストレージをいっぱい使うので、整理用スクリプトにGCを組み込み
```config.fish
function clear_storage
    aqua vacuum -d 1
    uv cache clean
    docker system prune
    brew cleanup
    go clean -modcache
    nix-collect-garbage # ←新規追加
end

```

    - [fish - NixOS Wiki](https://nixos.wiki/wiki/Fish)
        - fish使いたい
        - global <-> project みたいな使い分け、どうやってやるんだろう？
        - [home-manager入門](https://zenn.dev/kuu/articles/20250204_introduce-home-manager)
            - home-managerがglobal？ホーム環境構築ツール？dotfilesの管理用か？
    - [nixpkgs/doc/languages-frameworks/php.section.md at boot-spec-unstable · DeterminateSystems/nixpkgs](https://github.com/DeterminateSystems/nixpkgs/blob/boot-spec-unstable/doc/languages-frameworks/php.section.md?plain=1)
        - これは読むと良さそう
    - [Automated Dependency Updates for Nix - Renovate Docs](https://docs.renovatebot.com/modules/manager/nix/)
        - renovate公式でもnix対応ある様子
    - [numtide/treefmt-nix: treefmt nix configuration](https://github.com/numtide/treefmt-nix)
        - formatterはコレっぽい
            - 違う？flake.nixのformatに使うものではなさそう？

資料

- [Nix入門](https://zenn.dev/asa1984/books/nix-introduction)
- [org-nix-shell入門 | takeokunn's blog](https://www.takeokunn.org/posts/fleeting/20250126140928-introduction_org_nix_shell/)
- [Nix Package Versions](https://lazamar.co.uk/nix-versions/?channel=nixpkgs-unstable&package=php)
