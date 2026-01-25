# Rc
[Rc<T>は、参照カウント方式のスマートポインタ - The Rust Programming Language 日本語版](https://doc.rust-jp.rs/book-ja/ch15-04-rc.html)
>複数の所有権を可能にするため、RustにはRc<T>という型があり、これは、reference counting(参照カウント)の省略形です。 Rc<T>型は、値がまだ使用中かどうか決定する値への参照の数を追跡します。値への参照が0なら、どの参照も無効にすることなく、 値は片付けられます。

複数のリストから共有されるノードに使う例が挙げられている

いい記事見つけた

  - [Rustの Arc を読む(1): Arc/Rcの基本 - Qiita](https://qiita.com/qnighy/items/4bbbb20e71cf4ae527b9)

[#Rust](Rust)
