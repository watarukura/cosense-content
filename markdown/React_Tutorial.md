# React Tutorial
[https://github.com/watarukura/react-study](https://github.com/watarukura/react-study)
[https://ja.reactjs.org/tutorial/tutorial.html#setup-for-the-tutorial](https://ja.reactjs.org/tutorial/tutorial.html#setup-for-the-tutorial)

- yarn、初めて使った
    - yarn run って書くとrun可能なscriptのリストが出て便利
- react/props-typesがどうしたこうしたみたいなエラーが出た
```bash
Failed to compile.

src/index.js
  Line 18:27:  'squares' is missing in props validation  react/prop-types

Search for the keywords to learn more about each error.

PropTypesで型定義を書いたらエラーが解消した
	https://ja.reactjs.org/docs/typechecking-with-proptypes.html
	yarn add prop-types した
```
```js
import PropTypes from "prop-types";

Board.propTypes = {
  squares: PropTypes.object,
  onClick: PropTypes.func,
};

VS Code
	devContainer便利
		https://takeken1.hatenablog.com/entry/2021/01/02/221510
	シンプルブラウザーも便利
	prettierにformatもおまかせ
```
[https://gyazo.com/57c778fc9fa1f96699b446dc76c04fcf](https://gyazo.com/57c778fc9fa1f96699b446dc76c04fcf)

- わからん
    - JSXがそのままHTMLになるわけではないのね
        - ><div /> という構文は、ビルド時に React.createElement('div') に変換されます。
        - Reactが隠蔽している挙動が全く想像できない
            - Vueでも同じ？
        - 続きは[React](React)に書く

- GitHub Actionsでlint
    - prettier -> eslintでlint
        - https://zenn.dev/teppeis/articles/2021-02-eslint-prettier-vscode を参考に
