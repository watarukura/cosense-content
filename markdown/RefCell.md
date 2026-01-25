# RefCell
[RefCell<T>と内部可変性パターン - The Rust Programming Language 日本語版](https://doc.rust-jp.rs/book-ja/ch15-05-interior-mutability.html)
>RefCell<T>の一般的な使用法は、Rc<T>と組み合わせることにあります。Rc<T>は何らかのデータに複数の所有者を持たせてくれるけれども、 そのデータに不変のアクセスしかさせてくれないことを思い出してください。RefCell<T>を抱えるRc<T>があれば、 複数の所有者を持ちそして、可変化できる値を得ることができるのです。

Rcと組み合わせて使うっぽい

[#Rust](Rust)
