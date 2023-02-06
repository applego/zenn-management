すみません、少し長くなったので「前処理＆後処理＆引数を渡す」についてだけ、見たい場合「後処理でも引数を使いたい場合」の箇所に飛んでください。

## 各テストケースの前に共通の処理をしたい

そんなときに pytest で役立つのはご存知 fixture

```python
@pytest.fixture
def setup():
    # データの初期化など
    table = Table()
    return table

class TestClass:
    def test_code_1(self, setup):
        test_data = "test_data"
        expected = "test_data"
        assert test_data == expected # なんじゃこのテストはsetupいらんやんけ
```

こんな形で、共通化したい前処理を定義した関数 `setup` に `@pytest.fixture` をデコレートして使う。
テストを実行する関数 `test_code_1` では、以下のように引数に追加するだけでテストの処理に入る前に `setup` の内容を実行してくれる。

ちなみに、`@pytest.fixture(autouse=True)` とすれば、 `test_code_1()` の引数に、 `setup` を渡さなくても実行される。

```python
@pytest.fixture(autouse=True)
def setup():
    ...

class TestClass:
    def test_code_1(self):
    ...

```

## 前処理に加えて、後処理も共通化したい

となったら

```python
@pytest.fixture
def setup():
    # 前処理
    print("テストはじめるよ")

    yield # return -> yield (戻り値があれば yield something）

    # 後処理
    print("テストおわったよ")

class TestClass:
    def test_code_1(self, setup):
        test_data = "test_code_1"
        expected = "test_code_1"

        print("test_code_1")
        assert test_data == expected

    def test_code_2(self, setup):
        test_data = "test_code_2"
        expected = "test_code_2"

        print("test_code_2")
        assert test_data == expected
```

上記のコードを実行すると、

```実行結果
テストはじめるよ
test_code_1
テストおわったよ
テストはじめるよ
test_code_2
テストおわったよ
```

と、各テストの前に　`setup`の`yield` より前の部分、

各テストの後に　`setup`の`yield` より後の部分を実行してくれる。

## setup() の実行タイミングを変えるには（関数毎じゃなくて、テスト全体で一回とか）

1 つ前のコードは、setup 内の処理が、各テストケース毎に呼び出されているが、それは`@pytest.fixture`に渡せる`scope`という引数を指定していないから。

| scope    | 実行タイミング    | default |
| -------- | ----------------- | ------- |
| function | テストケース毎    | ○       |
| class    | クラス毎          |         |
| module   | テストファイル毎  |         |
| session  | テスト全体で 1 回 |         |

上記が`scope`で指定できる値で、デフォルトは function のため、指定しない場合はテストケース毎に実行される。

とここまでタイトルの、「引数を渡す方法」からいくらか脱線してきた気もしますが、ようやく本題に入ります。

## setup() に引数を渡すには

まず、`@pytest.fixture`をデコレートした関数に引数を渡す方法はこんな形です。

```python
@pytest.fixture
def setup():
  def _setup(arg):
    # 前処理
    return arg
  return _setup
```

`setup`の內部に、`_setup`という関数を定義して、その中で前処理を記述します。そして、外側の`setup` では`_setup`を返すようにしています。

## setup() に引数を渡す

今までさんざん、`@pytest.fixture`をデコレートして前処理、前処理言ってきましたが、前処理に限らず共通化したいことに使えるので、例えば引数の数字をソートする関数に`@pytest.fixture`をつけて、引数を渡す例を書いてみます。

```python

@pytest.fixture
def sort_desc():
  def _sort_desc(arg1, arg2, arg3):
    return sorted([arg1, arg2, arg3], reverse=True)
  return _sort_desc

class TestClass:
  def test_code_1(self, sort_desc):
    test_data = sort_desc(1, 2, 3)
    expected = [3, 2, 1]
    assert test_data == expected

  def test_code_2(self, sort_desc):
    test_data = sort_desc(-1, 3, 100)
    expected = [100, 3, -1]
    assert test_data == expected
```

テストケースから呼び出すときには、`_sort_desc` ではなく、`sort_desc`を呼び出せば良いです。

## 前処理＆後処理＆引数を渡す

本当に最後に、共通の前処理、後処理をしたい、そして引数を渡したい場合について、サンプルコードを書いてみます。

先程出てきたクソサンプルコードを再掲

```python
@pytest.fixture
def setup():
    # 前処理
    print("テストはじめるよ")

    yield # return -> yield (戻り値があれば yield something）

    # 後処理
    print("テストおわったよ")

class TestClass:
    def test_code_1(self, setup):
        test_data = "test_code_1"
        expected = "test_code_1"

        print("test_code_1")
        assert test_data == expected

    def test_code_2(self, setup):
        test_data = "test_code_2"
        expected = "test_code_2"

        print("test_code_2")
        assert test_data == expected

```

前処理で”テストはじめるよ”と出力しているので、引数を渡して、テストケース名も出力するようにします。

```python
@pytest.fixture
def setup():
    # 內部に引数を持つ関数を追加

    def _setup(arg):
        # 前処理
        print(f"テストはじめるよ test名: {arg}")
        return

    yield _setup

    # 後処理
    print("テストおわったよ")


class TestClass:
    def test_code_1(self, setup):
        setup("test_code_1")

        test_data = "test_code_1"
        expected = "test_code_1"

        assert test_data == expected

    def test_code_2(self, setup):
        setup("test_code_2")

        test_data = "test_code_2"
        expected = "test_code_2"

        assert test_data == expected
```

これで、今何のテストを実行しているかわかるようになりました。
めでたしめでたし

## 後処理でも引数を使いたい場合

後処理でも引数を使いたい場合は

```python
@pytest.fixture
def setup():

    args = [] # 後処理で使う引数を格納するリスト

    def _setup(arg1):
        # 前処理
        args.append(arg1) # 引数をリストに格納
        print(f"テストはじめるよ test名: {arg1}")
        return

    yield _setup

    # 後処理
    for arg in args:
        print(f"テストおわったよ test名: {arg}")
```

もっと良い方法がありそうですが、とりあえずこれで実現できるはずです。

## まとめ

今更ながら、後処理もするのに関数名が`setup`っていけてないですよね。
そしてサンプルコードが総じてひどくて申し訳ないです。が抽象化して、`scope`もうまく活用してやって頂けたら幸いです。
そして、困ったら（いや最初から）公式ドキュメントを読んでください。
https://docs.pytest.org/en/7.1.x/how-to/fixtures.html
読んでくれてありがとうございました。
