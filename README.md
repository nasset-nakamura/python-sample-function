# Python Sample Function

## Version

- Python 3.9.9

## How to Use

### Python をインストール

下記ページから Python 3.9.9 をインストール

[Python Releases for Windows](https://www.python.org/downloads/windows/)

[Python Releases for macOS](https://www.python.org/downloads/macos/)

```bash
# インストールされたことを確認
$ python --version
Python 3.9.9
```

### AWS CLI をインストール

[Windows での AWS CLI バージョン 2 のインストール、更新、アンインストール](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2-windows.html)

[macOS での AWS CLI バージョン 2 のインストール、更新、アンインストール](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2-mac.html)

```bash
# インストールされたことを確認
$ aws --version
aws-cli/2.4.13 Python/3.8.8 Darwin/21.1.0 exe/x86_64 prompt/off
```

### AWS CLI 初期設定

- 事前に AWS マネジメントコンソールで `ACCESS_KEY` と `SECRET_ACCESS_KEY` を作成する。
- AWS CLI を初期設定

```bash
# 対話形式で設定
$ aws configure

AWS Access Key ID [None]: xxxxxxxxxxxxxxxxxxxx
AWS Secret Access Key [None]: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Default region name [ap-northeast-1]:
Default output format [json]:

# ユーザー情報が取得できることを確認
$ aws sts get-caller-identity
```

### 開発環境準備

1. nodejs-sample-function リポジトリをクローン

```bash
$ git clone git@github.com:nasset-nakamura/python-sample-function.git && cd python-sample-function
```

2. 仮想環境作成、パッケージをインストール

```bash
$ poetry config virtualenvs.in-project true
$ poetry install
```

3. 環境変数を準備

- `.env.sample` をコピーして `.env` を作成

4. 実行

```bash
$ python src/xxxxx/main.py
```

### サンプル機能一覧

| ディレクトリ           | 内容                                       |
| ---------------------- | ------------------------------------------ |
| src/chatwork/sample_01 | ChatworkAPI で自分自身の情報を取得         |
| src/chatwork/sample_02 | ChatworkAPI でコンタクのユーザー一覧を取得 |
| src/chatwork/sample_03 | ChatworkAPI でメッセージを追加             |
| src/sendgrid/sample_01 | SendGrid SDK でテキストメール送信          |
| src/sendgrid/sample_02 | SendGrid SDK で HTML メール送信            |
