# Guzzle
HTTP Client。PSR−7準拠、aws-sdk-phpに同梱される。
[https://github.com/guzzle/guzzle](https://github.com/guzzle/guzzle)
[http://docs.guzzlephp.org/en/stable/](http://docs.guzzlephp.org/en/stable/)
[https://qiita.com/yousan/items/2a4d9eac82c77be8ba8b](https://qiita.com/yousan/items/2a4d9eac82c77be8ba8b)
```guzzle.php
$client = new \GuzzleHttp\Client();
$res = $client->request('GET', 'https://api.github.com/repos/guzzle/guzzle');
echo $res->getStatusCode();
// 200
echo $res->getHeaderLine('content-type');
// 'application/json; charset=utf8'
echo $res->getBody();
// '{"id": 1420053, "name": "guzzle", ...}'

// Send an asynchronous request.
$request = new \GuzzleHttp\Psr7\Request('GET', 'http://httpbin.org');
$promise = $client->sendAsync($request)->then(function ($response) {
    echo 'I completed! ' . $response->getBody();
});
$promise->wait();

```
