# Perplexity-API (非公式) 開発補助資料

## 1. 概要

*   **プロジェクト名**: Perplexity-API (非公式)
*   **開発者**: Arbaaz Mahmood
*   **リポジトリ**: [https://github.com/Arbaaz-Mahmood/Perplexity-API](https://github.com/Arbaaz-Mahmood/Perplexity-API)
*   **目的**: ブラウザ自動化技術（PuppeteerまたはSelenium）を利用し、Perplexity AIのウェブサイト ([perplexity.ai](https://perplexity.ai/)) にプログラムからクエリを送信し、回答を取得するための非公式インターフェースを提供する。
*   **提供実装**: TypeScriptベースのWebサーバー、Pythonベースのスクリプト

---

## 2. TypeScriptサーバー実装

### 2.1. 技術スタック

*   **言語**: TypeScript
*   **ランタイム**: Node.js (v14.0.0 以上推奨)
*   **Webフレームワーク**: Express
*   **ブラウザ自動化**: Puppeteer
*   **パッケージ管理**: npm (v6.14.0 以上推奨)

### 2.2. セットアップ手順

1.  **リポジトリのクローン**:
    ```bash
    git clone https://github.com/Arbaaz-Mahmood/Perplexity-API.git
    ```
2.  **ディレクトリ移動**:
    ```bash
    cd Perplexity-API/perplexity-query-api
    ```
3.  **依存関係のインストール**:
    ```bash
    npm install
    ```
4.  **サーバーの起動**:
    ```bash
    npx ts-node app.ts
    ```
    *   デフォルトで `http://localhost:3000` でサーバーが起動します。

### 2.3. APIエンドポイント

*   **メソッド**: `POST`
*   **パス**: `/query`
*   **リクエストボディ (JSON)**:
    ```json
    {
      "prompt": "ここにPerplexityへの質問を入力"
    }
    ```
*   **レスポンスボディ (JSON)**:
    *   成功時:
        ```json
        {
          "response": "Perplexity AIからの回答文字列"
        }
        ```
    *   エラー時: (実装によるが、通常はエラーメッセージを含むJSONやステータスコードで示される)

### 2.4. 主要処理フロー

1.  クライアントから `POST /query` リクエストを受信。
2.  リクエストボディから `prompt` (質問文) を取得。
3.  Puppeteerを起動し、ヘッドレスブラウザ（またはデバッグ用にヘッドフル）を初期化。
4.  Perplexity AIのウェブサイト ([perplexity.ai](https://perplexity.ai/)) にアクセス。
5.  (必要に応じて) ログイン処理を実行。
6.  指定されたCSSセレクタを使用して質問入力フィールドを特定し、`prompt` を入力。
7.  送信ボタンをクリック（またはEnterキーイベントをシミュレート）。
8.  回答が表示されるまで待機（特定の要素の出現やテキストの変化を監視）。
9.  指定されたCSSセレクタを使用して回答テキストを含む要素を特定し、内容を取得。
10. ブラウザを閉じる。
11. 取得した回答をJSON形式でクライアントに返却。

---

## 3. Pythonスクリプト実装

### 3.1. 技術スタック

*   **言語**: Python (3.6 以上推奨)
*   **ブラウザ自動化**: Selenium
*   **HTML解析**: BeautifulSoup4 (主に要素特定補助)
*   **WebDriver管理**: webdriver-manager

### 3.2. セットアップ手順

1.  **リポジトリのクローン**: (TypeScriptと同様)
    ```bash
    git clone https://github.com/Arbaaz-Mahmood/Perplexity-API.git
    ```
2.  **ディレクトリ移動**:
    ```bash
    cd Perplexity-API
    ```
3.  **依存関係のインストール**:
    ```bash
    pip install selenium beautifulsoup4 webdriver-manager
    ```
4.  **WebDriverのセットアップ**:
    *   `webdriver-manager` がChromeDriverを自動でダウンロード・管理しますが、手動でのインストールが必要な場合やパス設定が必要な場合があります。
    *   **macOS (Homebrew)**: `brew install chromedriver`
    *   **Windows**: 公式サイトからダウンロードし、PATHを通す。
    *   **Linux (Debian/Ubuntu)**: `sudo apt-get install chromium-chromedriver`
5.  **スクリプトの実行**:
    ```bash
    python perplexity_query.py
    ```
    *   実行後、コンソールで質問の入力を求められます。

### 3.3. 主要関数 (例: `perplexity_query.py` 内)

*   **関数名**: `query_perplexity(prompt: str) -> str` (想定されるインターフェース)
*   **入力**: 質問文字列 (`prompt`)
*   **出力**: Perplexity AIからの回答文字列

### 3.4. 主要処理フロー

1.  スクリプト実行時にコマンドラインから質問 (`prompt`) を受け取る。
2.  `webdriver-manager` を使用して適切なChromeDriverをセットアップ。
3.  Selenium WebDriver (Chrome) を起動。
4.  Perplexity AIのウェブサイト ([perplexity.ai](https://perplexity.ai/)) にアクセス。
5.  (必要に応じて) ログイン処理を実行。
6.  Seleniumの要素特定機能 (例: `find_element`) を使用して質問入力フィールドを特定し、`prompt` を入力。
7.  送信ボタン要素を特定し、クリック。
8.  WebDriverWaitなどの待機メカニズムを使用し、回答が表示されるまで待機。
9.  回答テキストを含む要素を特定し、テキスト内容を取得。
10. WebDriverを終了 (`driver.quit()`)。
11. 取得した回答をコンソールに出力。
