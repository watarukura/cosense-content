# compilerbook
[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook/)

知らなかったことメモ

    - [objdump](objdump)
        - コンパイル結果をobjdumpしてもアセンブリと同じにならないのはなんでだろう
            - [godbolt.org](https://godbolt.org) を使うとリアルタイム・オンライン・コンパイルできる
        - なんかいっぱい出る
    - gccはアセンブリをアセンブルできる
        - アセンブリの拡張子は.s
    - >大雑把にいうと、Cコンパイラは、test1.cのようなCコードを読み込んで、test2.sのようなアセンブリを出力するプログラムということになります。
        - そうだったのか！
    - 思った以上にCが読めない
        - Goっぽい(逆だけど)
        - ポインタ辛い(滅びろ)
    - unary operator : 単項演算子

あまりにもCがわからないので[C言語プログラミングレッスン](https://github.com/watarukura/study-lc)を開始

    - プロトタイプ宣言・・・全然覚えてない
        - [https://www.grapecity.com/developer/support/powernews/column/clang/015/page02.htm](https://www.grapecity.com/developer/support/powernews/column/clang/015/page02.htm)
    - かろうじてfor文は覚えてた
