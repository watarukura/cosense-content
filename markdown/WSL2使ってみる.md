# WSL2使ってみる
10年ぶりくらい?にWindows PCを買った
WSL2で遊んでみたいという理由なのだが、なんだか使い勝手が良くないのでメモ

- CapsLock無効化したい
    - PowerToysというMS謹製のツールがあるのでこれを使ってCapsLockをCtrlと交換しようとした
    - なぜかCtrl押しっぱなしになる
    - わからぬ
    - [https://learn.microsoft.com/en-us/sysinternals/downloads/ctrl2cap](https://learn.microsoft.com/en-us/sysinternals/downloads/ctrl2cap)
        - こっちを使うことにした
        - まぁ、左Ctrlキーとか使わんだろう多分
- 変換、無変換キーの動作をMacのかな、英数キーと同じ挙動にしたい
    - Google日本語入力でキー設定を変更した
    - [https://gyazo.com/0453d81053f93aa75d37158067014c11](https://gyazo.com/0453d81053f93aa75d37158067014c11)

- WSL2入れる
    - Ubuntuにした
- aptであれこれ入れる
    - linuxbrewでも良かったが、Macは会社からの貸与で使ってるので
    - golang-go
    - neovim
    - fzf
    - ghq
- Docker Destop入れる

