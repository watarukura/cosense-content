# SATySFi
神殺しアプリケーションwatarukura.icon

[Github](https://github.com/gfngfn/SATySFi)
[The SATySFiBook](https://gfngfn.booth.pm/items/1127224)

ハマりメモ

- `brew install --HEAD nyuichi/satysfi/satysfi` でなにかエラーが出たのでOpam経由で
- `satysfi demo.saty -o demo.pdf` したらエラーでた
```bash
 $ make
 satysfi demo.saty
  ---- ---- ---- ----
   target file: 'demo.pdf'
 ! [Error] package file not found:
       dist/hash/default-font.satysfi-hash
     candidate paths:
       /Users/kurashimawataru/.satysfi/dist/hash/default-font.satysfi-hash
       /usr/local/share/satysfi/dist/hash/default-font.satysfi-hash
       /usr/share/satysfi/dist/hash/default-font.satysfi-hash
 make: *** [all] Error 1
code:bash
 $ cd
 $ mkdir .satysfi
 $ ln -s ~/.opam/4.06.0/share/satysfi/dist dist
```
[https://gyazo.com/55ebbf5bc6503f560b2a8a4514ed6393](https://gyazo.com/55ebbf5bc6503f560b2a8a4514ed6393)
