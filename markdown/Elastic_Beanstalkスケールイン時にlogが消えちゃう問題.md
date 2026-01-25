# Elastic Beanstalkスケールイン時にlogが消えちゃう問題
[Elastic Beanstalkスケールイン時にlogが消えちゃう問題｜ハンズラボ株式会社](https://www.hands-lab.com/tech/t1180/)  の転記です

2016.02.24
倉嶋です。
最近はすっかりPHPerとしてPHP Stormと戯れる日々です。
頭のいいIDE使うと、知識が足りないところが補完されるので頼りっぱなしです。
AWSはまだまだ補完されない領域が多いので、自分で頭を使う必要がありますね。
ということで、Elastic Beanstalkのログ取得でハマったところをご紹介。

ElasticBeanstalkのログ保存方法
↑こちらの記事にあるとおり、Elastic Beanstalkのログは設定すれば定期的に勝手にS3へ格納されるのですが、サーバが減った時に消えちゃいます。
コレは困る。
ということで、シャットダウン時にログ書き出しのスクリプトを動かすようにしました。

Linuxでシャットダウン時に想定した処理が実行されない
こちらを参考に、ランレベル0と6で動作するスクリプトを書きました。

```logrotate.bash
#!/usr/bin/env bash
lock_file="/var/lock/subsys/forcelogput"
start()
{
    touch ${lock_file}
    #logrotate
    sudo /etc/cron.hourly/cron.logrotate.elasticbeanstalk.webapp.conf
    sudo /etc/cron.hourly/cron.logrotate.elasticbeanstalk.httpd.conf
    #publishLogs
    sudo /usr/bin/publishLogs.py --de-dupe --conf-path '/opt/elasticbeanstalk/tasks/publishlogs.d/*' --location-prefix resources/environments/logs/publish/ --num-concurrent 2
}
stop()
{
    rm -r ${lock_file}
    #logrotate
    sudo /etc/cron.hourly/cron.logrotate.elasticbeanstalk.webapp.conf
    sudo /etc/cron.hourly/cron.logrotate.elasticbeanstalk.httpd.conf
    #publishLogs
    sudo /usr/bin/publishLogs.py --de-dupe --conf-path '/opt/elasticbeanstalk/tasks/publishlogs.d/*' --location-prefix resources/environments/logs/publish/ --num-concurrent 2
}
case "$1" in
    start)
        start
    ;;
    stop)
        stop
    ;;
    *)
        echo "Usage: $0 {start|stop}"
    ;;
esac
exit 0 

```
さらに、.ebextensionsで、このスクリプトを配置するスクリプトを用意しました。
この辺がElastic Beanstalk使う時の難しいところですね。

```ebextensions.bash
files:
    "/opt/elasticbeanstalk/hooks/appdeploy/pre/50_logrotate-before-shutdown.sh" :
        mode: "000777"
        owner: root
        group: root
        content: |
            #!/usr/bin/env bash
            . /opt/elasticbeanstalk/support/envvars
            EB_CONFIG_APP_ONDECK=/var/app/ondeck
            function log {
                local message="$1"
                echo "$(date '+%Y-%m-%d %H:%M:%S') $0 $message" >> /var/app/support/logs/ebextensions.log
            }
            #
            # main
            #
            log "INFO: START"
            # replace default logrotate config file
            log "INFO: replace logrotate config file"
            cp -f /var/app/ondeck/config/replace/logrotate.elasticbeanstalk.webapp.conf /etc/logrotate.elasticbeanstalk.hourly/
            cp -f /var/app/ondeck/config/replace/logrotate.elasticbeanstalk.httpd.conf /etc/logrotate.elasticbeanstalk.hourly/
            touch /var/lock/subsys/forcelogput
            cd /etc/init.d
            # set logrotate to /etc/init.d/
            log "INFO: set logrotate file to /etc/init.d/"
            cp -f /var/app/ondeck/config/replace/forcelogput.sh /etc/init.d/
            # set logrotate-symlink to /etc/rc0.d/ & /etc/rc6.d/
            log "INFO: set logrotate-symlink file to /etc/rc[06].d/"
            cd /etc/rc0.d/ && ln -s /etc/init.d/forcelogput.sh ./K00forcelogput
            cd /etc/rc6.d/ && ln -s /etc/init.d/forcelogput.sh ./K00forcelogput
            # change logrotate daily to hourly
            mv /etc/cron.daily/logrotate /etc/cron.hourly/
            log "INFO: FINISH"
            true
            #----- end of script -----------------------

```
これで、サーバ起動時・終了時に強制的にlogrotate→S3へログを転送することができます。
(logrotateのconfも書き換えていますが、こちらは割愛)

fluentdあたりを使えば悩む必要ないかもですが、この辺りまでElastic Beanstalkのデフォルトで面倒見てほしいなぁ。。。

＜追記＞

```logrotate.conf
/var/app/support/logs/* {
size 1
rotate 10
missingok
compress
notifempty
copytruncate
dateext
dateformat %Y%m%d-%s
olddir /var/app/support/logs/rotated
}
```
喉もとすぎれば熱さを忘れるわけで、割愛と書いた中にもハマリポイントが。
logroateのデフォルトのconfでは、size 10MB指定になっています。
この場合、10MBを超えていないとlogrotateしません。rotateしないとS3へも配信されないので、sizeを1にしています。
[#ハンズラボテックブログ](ハンズラボテックブログ)
