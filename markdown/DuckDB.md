# DuckDB

- [https://livebook.manning.com/book/duckdb-in-action/chapter-1/44](https://livebook.manning.com/book/duckdb-in-action/chapter-1/44)
>1.4 DuckDB を使用すべきでないのはどのような場合ですか?
> DuckDB は分析データベースであるため、トランザクションと並列書き込みアクセスのサポートは最小限です。そのため、任意に到着する入力データを処理して保存するアプリケーションや API では使用できません。

- [https://livebook.manning.com/book/duckdb-in-action/chapter-1/66](https://livebook.manning.com/book/duckdb-in-action/chapter-1/66)
>DuckDB はさまざまなデータ形式をサポートしています。
> CSV ファイルは一括して並列に読み込むことができ、列は自動的にマッピングされます。
> DataFrames のメモリは、データをコピーする必要なく、同じ Python プロセス内で DuckDB によって直接処理できます。
> JSON 形式は、構造化解除、フラット化、リレーショナル テーブルに変換できます。DuckDB には、このタイプのデータを保存するための JSON 型もあります。
> Parquet ファイルは、そのスキーマ メタデータとともにクエリできます。クエリで使用される述語はプッシュダウンされ、Parquet ストレージ レイヤーで評価され、ロードされるデータの量が削減されます。これは、データ レイクの読み取りと書き込みに最適な列形式です。
> Apache Arrow の列状のデータは、データのコピーや変換を行わずに、Arrow Database Connectivity (ADBC) を介して読み取ることができます。
> S3 や GCP などのクラウド バケット内のデータにアクセスすると、転送およびコピーのインフラストラクチャが削減され、大量のデータを安価に処理できるようになります。

[https://livebook.manning.com/book/duckdb-in-action/chapter-1/85](https://livebook.manning.com/book/duckdb-in-action/chapter-1/85)
>DuckDB ( https://duckdb.org/docs/sql/aggregates.htmlmin ) では、 、 、などの従来のものから、 、 avg、sumなどのより高度なものhistogramやbitstring_agg、listなどの近似値まで、さまざまな集計関数を使用できますapprox_count_distinct。
[Aggregate Functions](https://duckdb.org/docs/sql/functions/aggregates.html)

[https://livebook.manning.com/book/duckdb-in-action/chapter-1/90](https://livebook.manning.com/book/duckdb-in-action/chapter-1/90)
>DuckDB は、CSV、JSON、Parquet、Excel、Apache Arrow など、さまざまな形式で書き込むことができます。

[https://livebook.manning.com/book/duckdb-in-action/chapter-3/126](https://livebook.manning.com/book/duckdb-in-action/chapter-3/126)
>CSV ファイルに関するデータ パイプラインを構築していて、多くの場合、ファイルは複数のファイルに分割され、ファイルごとに 1 つの共通列があります。これらのファイルを共通列を重複させずに 1 つのファイルに減らしたい場合はどうすればよいでしょうか。これは、内部結合とCOPY TOコマンドを使用すると簡単に実現できます。後者は、任意の関係を取得し、指定された形式を使用してファイルにコピーします。
```csv.sql
duckdb -c "COPY (SELECT * FROM 'production.csv' JOIN 'consumption.csv'
USING (ts) JOIN 'export.csv' USING (ts) JOIN 'import.csv' USING (ts) )
TO '/dev/stdout' (HEADER)"

```
[https://livebook.manning.com/book/duckdb-in-action/chapter-6/39](https://livebook.manning.com/book/duckdb-in-action/chapter-6/39)
>DuckDB で SQL コマンドを実行するのは強力ですが、read_csvPython API を介して関数を直接使用すると、Python ベースのワークフローとシームレスに統合できます。この方法は、データ操作に「Python 的」なアプローチを提供し、SQL データベースと Python データ構造のギャップを埋めるため、Python ベースのプロジェクトに適しています。返されるオブジェクトは、Python コード内からクエリ可能な関係として扱うことができます。次のコードでは、デフォルトのインメモリ データベースを使用しますが、前述のように接続を簡単に変更できます。
```csv.py
import duckdb

con = duckdb.connect(database=':memory:')

con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

population = \
  con.read_csv("https://bit.ly/3KoiZR0")

```
