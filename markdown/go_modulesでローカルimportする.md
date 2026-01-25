# go modulesでローカルimportする
[https://text.baldanders.info/golang/go-module-aware-mode/](https://text.baldanders.info/golang/go-module-aware-mode/)
[https://pod.hatenablog.com/entry/2018/12/26/074944](https://pod.hatenablog.com/entry/2018/12/26/074944)
[https://github.com/golang/go/issues/26645](https://github.com/golang/go/issues/26645)

上記を参考に、下記のようにした

- 共通部品のutilをcalsed.goから呼び出したい
- ローカルimport `../util` するとエラーになる
```terminal
$ tree
.
├── calsed
│   ├── Makefile
│   ├── calsed.go
│   ├── calsed_test.go
│   ├── go.mod
│   ├── go.sum
│   └── testdata
│       ├── TEST1-file.txt
│       ├── TEST7-script.txt
│       ├── TEST8-script.txt
│       └── TEST9-script.txt
└── util
   ├── go.mod
   └── util.go

```
```calsed/go.mod
module github.com/watarukura/OpenUspTukubaiGolang/calsed

require (
	github.com/mattn/go-shellwords v1.0.3
	github.com/watarukura/OpenUspTukubaiGolang/util v0.0.0-20190101144146-47c267814789
)

replace github.com/watarukura/OpenUspTukubaiGolang/util => ../util

```
