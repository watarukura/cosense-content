# Windows11再セットアップ
Windows10 → Ubuntu22.04 → Ubuntu24.04 → Windows11をクリーンインストールしたメモ

- ChatGPTに相談: WindowsプレインストールのASUSのノートPCに ubuntuをクリーンインストールしました。工場出荷時に戻したい場合、どのような方法がありますか？
    - 一度Ubuntuをクリーンインストールしているので、リカバリーディスクがない
    - Windowsインストールメディアから再インストールすればライセンスはファームウェアに残ってるから問題なく使えるはず
        - ドライバは再インストールしないと駄目
        - MyASUSも入れれば工場出荷状態とニアリーイコールになる
- Windowsインストールメディアを作る
    - UbuntuからもMacからも作るのが割とむずい
        - FATが4GBまでしか読めないのでファイル分割する必要がある
        - ISOファイルをマウントしてddでコピーするが書き込みがめっちゃ遅い...
    - Windowsから作るのが簡単
        - 息子のWinマシンを借りてUSBメモリで作る
- 再インストール
    - Wifiに繋がらない
        - 無線LANドライバがなくてインストールが途中で止まる
        - 再度WInマシンでドライバをダウンロードしてきてUSBメモリに突っ込む
        - 再インストール途中で無線LANドライバをインストールして進める
    - RPGツクールMZ製のアプリケーションが起動しない
        - GPUドライバがなくてChromeからOpenGLが動かない
        - NVIDIAのドライバをインストール → まだ動かない
        - AMD APUのドライバをインストール → 動いた
        - 基本的に内蔵のAMDのGPUを使って、デカい計算が必要な場合にNVIDIAのGPUを使う構成になっているとのこと
- セットアップ
    - Google Chromeをインストール
    - CapslockキーにCtrlを割り当てる
        - [Ctrl2Cap - Sysinternals | Microsoft Learn](https://learn.microsoft.com/ja-jp/sysinternals/downloads/ctrl2cap)
    - Google日本語入力をインストール
        - 変換キー → IMEオン、無変換キー → IMEオフに割り当てる
    - Wingetで以下をインストール
        - vim
        - neovim
    - coreutils
        - ないよなーと思いつつdiffコマンドとかなくて不便
```coreutils.bash
C:\Program Files\coreutils\bin>ls
_why_is_this_700MB_.txt  csplit.exe   fmt.exe       mv.exe        readlink.exe   sort.exe      tsort.exe
arch.exe                 cut.exe      fold.exe      nl.exe        realpath.exe   split.exe     unexpand.exe
b2sum.exe                date.exe     grep.exe      nproc.exe     rm.exe         stat.exe      uniq.exe
base32.exe               df.exe       head.exe      numfmt.exe    rmdir.exe      sum.exe       unlink.exe
base64.exe               dirname.exe  hostname.exe  od.exe        seq.exe        tac.exe       uptime.exe
basename.exe             du.exe       join.exe      paste.exe     sha1sum.exe    tail.exe      wc.exe
basenc.exe               echo.exe     link.exe      pathchk.exe   sha224sum.exe  tee.exe       xargs.exe
cat.exe                  env.exe      ln.exe        pr.exe        sha256sum.exe  test.exe      yes.exe
cksum.exe                expr.exe     ls.exe        printenv.exe  sha384sum.exe  touch.exe
comm.exe                 factor.exe   md5sum.exe    printf.exe    sha512sum.exe  tr.exe
 coreutils-manager.exe    false.exe    mkdir.exe     ptx.exe       shuf.exe       true.exe
  cp.exe                   find.exe     mktemp.exe    pwd.exe       sleep.exe      truncate.exe 

  git
  	こっちには色々ある
  	とはいえ、こっちをdefault shellにするのもなぁ...
```
```git_bash.bash
C:\Program Files\Git\bin>bash.exe

whatr@watarukura-asus MINGW64 /bin
$ ls
'[.exe'                      gpgconf.exe              msys-p11-kit-0.dll           sha1sum.exe
 addgnupghome                gpg-connect-agent.exe    msys-pcre-1.dll              sha224sum.exe
 applygnupgdefaults          gpg-error.exe            msys-pcre2-8-0.dll           sha256sum.exe
 arch.exe                    gpg-mail-tube.exe        msys-perl5_42.dll            sha384sum.exe
 astextplain                 gpgparsemail.exe         msys-psl-5.dll               sha512sum.exe
 awk.exe                     gpgscm.exe               msys-readline8.dll           shred.exe
 b2sum.exe                   gpgsm.exe                msys-roken-18.dll            shuf.exe
 backup                      gpgsplit.exe             msys-sasl2-3.dll             sleep.exe
 base32.exe                  gpgtar.exe               msys-serf-1-0.dll            sort.exe
 base64.exe                  gpgv.exe                 msys-smartcols-1.dll         split.exe
 basename.exe                gpg-wks-client.exe       msys-sqlite3-0.dll           ssh.exe
 basenc.exe                  gpg-wks-server.exe       msys-ssl-3.dll               ssh-add.exe
 bash.exe                    grep.exe                 msys-svn_client-1-0.dll      ssh-agent.exe
 bashbug                     groups.exe               msys-svn_delta-1-0.dll       ssh-copy-id
 bunzip2.exe                 gunzip                   msys-svn_diff-1-0.dll        ssh-keygen.exe
 bzcat.exe                   gzexe                    msys-svn_fs_fs-1-0.dll       ssh-keyscan.exe
 bzcmp                       gzip.exe                 msys-svn_fs_util-1-0.dll     ssh-pageant.exe
 bzdiff                      head.exe                 msys-svn_fs_x-1-0.dll        ssp.exe
 bzegrep                     hmac256.exe              msys-svn_fs-1-0.dll          start
 bzfgrep                     hostid.exe               msys-svn_ra_local-1-0.dll    stat.exe
 bzgrep                      hostname.exe             msys-svn_ra_serf-1-0.dll     stdbuf.exe
 bzip2.exe                   iconv.exe                msys-svn_ra_svn-1-0.dll      strace.exe
 bzip2recover.exe            id.exe                   msys-svn_ra-1-0.dll          stty.exe
 bzless                      infocmp.exe              msys-svn_repos-1-0.dll       sum.exe
 c_rehash                    infotocap.exe            msys-svn_subr-1-0.dll        sync.exe
 captoinfo.exe               install.exe              msys-svn_swig_perl-1-0.dll   tabs.exe
 cat.exe                     join.exe                 msys-svn_wc-1-0.dll          tac.exe
 chattr.exe                  kbxutil.exe              msys-tasn1-6.dll             tail.exe
 chcon.exe                   kill.exe                 msys-ticw6.dll               tar.exe
 chgrp.exe                   ldd.exe                  msys-unistring-5.dll         tee.exe
 chmod.exe                   ldh.exe                  msys-uuid-1.dll              test.exe
 chown.exe                   less.exe                 msys-wind-0.dll              tic.exe
 chroot.exe                  lesskey.exe              msys-z.dll                   tig.exe
 cksum.exe                   link.exe                 msys-zstd-1.dll              timeout.exe
 clear.exe                   ln.exe                   mv.exe                       toe.exe
 cmp.exe                     locale.exe               nano.exe                     touch.exe
 column.exe                  locate.exe               nettle-hash.exe              tput.exe
 comm.exe                    logname.exe              nettle-lfib-stream.exe       tr.exe
 core_perl                   ls.exe                   nettle-pbkdf2.exe            true.exe
 cp.exe                      lsattr.exe               newgrp.exe                   truncate.exe
 csplit.exe                  mac2unix.exe             nice.exe                     trust.exe
 cut.exe                     md5sum.exe               nl.exe                       tset.exe
 cygcheck.exe                minidumper.exe           nohup.exe                    tsort.exe
 cygpath.exe                 mintheme                 notepad                      tty.exe
 cygwin-console-helper.exe   mintty.exe               nproc.exe                    tzset.exe
 d2u.exe                     mkdir.exe                numfmt.exe                   u2d.exe
 dash.exe                    mkfifo.exe               od.exe                       umount.exe
 date.exe                    mkgroup.exe              openssl.exe                  uname.exe
 dd.exe                      mknod.exe                p11-kit.exe                  uncompress
 df.exe                      mkpasswd.exe             passwd.exe                   unexpand.exe
 diff.exe                    mktemp.exe               paste.exe                    uniq.exe
 diff3.exe                   mount.exe                patch.exe                    unix2dos.exe
 dir.exe                     mpicalc.exe              pathchk.exe                  unix2mac.exe
 dircolors.exe               msys-2.0.dll             perl.exe                     unlink.exe
 dirmngr.exe                 msys-apr-1-0.dll         perl5.42.2.exe               unzip.exe
 dirmngr-client.exe          msys-aprutil-1-0.dll     pinentry.exe                 unzipsfx.exe
 dirname.exe                 msys-asn1-8.dll          pinentry-w32.exe             update-ca-trust
 docx2txt                    msys-assuan-9.dll        pinky.exe                    updatedb
 docx2txt.pl                 msys-bz2-1.dll           pkcs1-conv.exe               users.exe
 dos2unix.exe                msys-cbor-0.11.dll       pldd.exe                     vdir.exe
 du.exe                      msys-com_err-1.dll       pluginviewer.exe             vendor_perl
 dumpsexp.exe                msys-crypt-2.dll         pr.exe                       vi
 echo.exe                    msys-crypto-3.dll        printenv.exe                 view.exe
 egrep                       msys-edit-0.dll          printf.exe                   vim.exe
 env.exe                     msys-expat-1.dll         profiler.exe                 vimdiff.exe
 ex.exe                      msys-ffi-8.dll           ps.exe                       vimtutor
 expand.exe                  msys-fido2-1.dll         psl.exe                      watchgnupg.exe
 expr.exe                    msys-gcc_s-seh-1.dll     psl-make-dafsa               wc.exe
 factor.exe                  msys-gcrypt-20.dll       ptx.exe                      which.exe
 false.exe                   msys-gdbm_compat-4.dll   pwd.exe                      who.exe
 fgrep                       msys-gdbm-6.dll          readlink.exe                 whoami.exe
 file.exe                    msys-gmp-10.dll          realpath.exe                 winpty.dll
 find.exe                    msys-gnutls-30.dll       rebase.exe                   winpty.exe
 findssl.sh                  msys-gpg-error-0.dll     rebaseall                    winpty-agent.exe
 fmt.exe                     msys-gssapi-3.dll        regtool.exe                  winpty-debugserver.exe
 fold.exe                    msys-hcrypto-4.dll       reset.exe                    wordpad
 funzip.exe                  msys-heimbase-1.dll      restore                      xargs.exe
 gawk.exe                    msys-heimntlm-0.dll      rm.exe                       xxd.exe
 gawk-5.4.0.exe              msys-hogweed-7.dll       rmdir.exe                    yat2m.exe
 gawkbug                     msys-hx509-5.dll         rnano.exe                    yes.exe
 gdbm_dump.exe               msys-iconv-2.dll         runcon.exe                   zcat
 gdbm_load.exe               msys-idn2-0.dll          rview.exe                    zcmp
 gdbmtool.exe                msys-intl-8.dll          rvim.exe                     zdiff
 gencat.exe                  msys-krb5-26.dll         scp.exe                      zegrep
 getconf.exe                 msys-ksba-8.dll          sdiff.exe                    zfgrep
 getfacl.exe                 msys-lz4-1.dll           sed.exe                      zforce
 getopt.exe                  msys-lzma-5.dll          seq.exe                      zgrep
 gkill.exe                   msys-magic-1.dll         setfacl.exe                  zipgrep
 gmondump.exe                msys-mpfr-6.dll          setmetamode.exe              zipinfo.exe
 gpg.exe                     msys-ncursesw6.dll       sexp-conv.exe                zless
 gpg-agent.exe               msys-nettle-9.dll        sftp.exe                     znew
 gpg-card.exe                msys-npth-0.dll          sh.exe


wsl containersを動かしてみる
	[WSL Containersに触れてみた https://zenn.dev/user_thebigslee/articles/wsl-container-trial]

軽量化
	使わないプレインストールアプリケーションを削除
		MyASUSも勝手にインストールされてたので削除
		ニュース、天気、Teams、OneDrive、...
		なんでクリーンインストールなのにこんなに使わないアプリケーションが入ってるんだ...???
	レジストリ
　	[Windowsの高速化をがんばってみた https://zenn.dev/maedan/articles/91caa405e30165]
  [Windowsの高速化をがんばってみた（２） https://zenn.dev/maedan/articles/f9a13ac72d5f3a]
  できるだけスッキリさせたい
  一方でregeditあんまり手で触りたくない
  regeditでexportして、テキストファイル書き換えてimportすればいいのかな...
  	linterとかあるのかしらん
OneDriveの洗礼
	OneDriveくん、マジで:shit:だな！噂通りだ
		何を勝手にコピってんのよ...
		Explorerのドキュメントの向き先も`C:\Users\<user>\Onedrive\ドキュメント`になってるし
```
```onedrive.bash
C:\Users\whatr>ls OneDrive
Desktop  デスクトップ  ドキュメント  添付ファイル  画像
C:\Users\whatr>ls
 .bash_history   Contacts    Downloads   Links   OneDrive       Searches   _viminfo   vimfiles
 .bashrc         Documents   Favorites   Music  'Saved Games'   Videos     ansel

```
現状の不満点

    - Ctrll + f / Ctrl + a / Ctrl + e が効かない
        - 入力候補があるときにCtrl + fをよく打ってるので大変困る...
        - [Ctrl + F が機能しない · Issue #4532 · microsoft/WSL](https://github.com/microsoft/WSL/issues/4532)
    - MacからRemote Desktopできない
        - Home Editionなのでしゃーなし...
        - Proにアップグレードするか？
    - ChromeのショートカットキーがWinとMacで異なる
        - オレは隣のタブに移動したいだけなんだ...
            - Win: Ctrl + Tab
            - Mac: Alt + Cmd + →

参考

    - [Emacs使いがWindows11で行う初期設定メモ #キーバインド - Qiita](https://qiita.com/yasushi00/items/8d7fc8c6837a3eed3e2f)

