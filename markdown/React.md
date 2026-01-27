# React

- JSX
    - JavaScriptの構文拡張
    - HTMLではない
    - React要素を生成する
    - React要素
    - Reactコンポーネント
        - 要素はコンポーネントを構成するもの
    - ReactDOM.rendor()
        - React要素->DOM
        - 大抵のReactアプリケーションは1回だけ呼び出す
    - 関数コンポーネント
        - React要素を返すReactコンポーネント
    - props
        - 読み取り専用
        - properties->props
    - state
        - propsに似ているが、コンポーネントによって完全に管理されるプライベートなもの
            - stateを所有してセットするコンポーネント自身以外からはそのstateにアクセスすることができない
        - stateを直接変更しない
            - setState()する
        - stateの更新は非同期で、マージされる
    - event
        - camelCaseで書く
        - synthetic event
            - ブラウザのネイティブイベントに対するクロスブラウザ版のラッパー
        - addEventListnerは不要

