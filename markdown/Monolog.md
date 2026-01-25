# Monolog
Slim Frameworkのデフォルトのロガー。PSR-3準拠。

[https://github.com/Seldaek/monolog](https://github.com/Seldaek/monolog)
[http://tech.quartetcom.co.jp/2018/05/31/monolog/](http://tech.quartetcom.co.jp/2018/05/31/monolog/)

```log.php
<?php

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

// create a log channel
$log = new Logger('name');
$log->pushHandler(new StreamHandler('path/to/your.log', Logger::WARNING));

// add records to the log
$log->warning('Foo');
$log->error('Bar');
```
