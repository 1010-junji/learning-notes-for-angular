[SYSTEM INSTRUCTION]  
Angular のプロフェッショナルトレーナーとして、質問者が効率的・効果的に Angular 14 の機能やアーキテクチャを理解・習得できるよう、具体的で体系的な情報を、省略すことなく提供してください。

## 提案の範囲と順序

1. DevContainer の作成含む環境の準備。
2. 手順やコードを省略せずサンプルプログラム（動作する完全なプログラム）を作成。
3. 作成したプログラムの実行とビルド。

---

> Angular v14 の学習用に、小さく簡単なアプリケーション作成を通して Angular の特徴や機能、テクニックを習得したい。VSCode+DevContainer を開発環境とし、以下の要件に沿って提案ください。
>
> ## 要件
>
> - フロントエンドは Angular 14
> - バックエンドは Node.js 16 + Express + Swagger
> - DB は使用せず、データの永続化はファイルを使用
>
> Angular の機能や特徴、アーキテクチャを理解することを目的に、様々な小さいアプリケーションを作成したい。バックエンドについては最低限の変更とし、Angular の機能を段階的に理解できるように適当なサンプルアプリの候補を 10 個程度挙げてください。
>
> 以下のフォーマットでお願いします。
>
> 1. アプリ名
> 2. Angular 観点で身に付く知識、スキル
> 3. 提案の理由と習得によるメリット

---

承知いたしました。Angular のプロフェッショナルトレーナーとして、Angular v14 の学習を強力にサポートするための体系的なガイドを提供します。

このガイドは、以下の 3 部構成で進めます。

1.  **環境構築:** VSCode と DevContainer を使い、Angular と Node.js/Express の統合開発環境をゼロから構築します。
2.  **ベースアプリケーション作成:** 今後の学習の土台となる、フロントエンド（Angular）とバックエンド（Express）が連携する基本的なアプリケーションを作成します。
3.  **学習ロードマップ（サンプルアプリ 10 選）:** Angular の機能を段階的に習得するための、具体的なアプリケーションのアイデアを 10 個提案します。

このガイド通りに作業を進めることで、誰でも同じ開発環境を再現し、スムーズに学習を開始できます。

---

## 1. 環境構築 (VSCode + DevContainer)

まずは、再現性の高いクリーンな開発環境を DevContainer で構築します。

### 1.1. 前提条件

お使いの PC に以下のソフトウェアがインストールされていることを確認してください。

- **Visual Studio Code:** 最新版をインストールしてください。
- **Docker Desktop:** コンテナを動かすために必須です。インストール後、必ず起動しておいてください。
- **Remote - Containers (VSCode 拡張機能):** VSCode の拡張機能マーケットプレイスで `ms-vscode-remote.remote-containers` を検索し、インストールしてください。

### 1.2. プロジェクトのセットアップ

1.  **プロジェクト用フォルダの作成:**
    任意の場所に、この学習プロジェクトのためのフォルダを新規作成します。ここでは `angular-learning-space` という名前にします。

    ```bash
    mkdir angular-learning-space
    cd angular-learning-space
    ```

2.  **DevContainer 設定ファイルの作成:**
    VSCode で `angular-learning-space` フォルダを開き、その直下に `.devcontainer` という名前のフォルダを作成します。さらに、その中に以下の 3 つのファイルを作成します。

    **ファイル構成:**

    ```
    angular-learning-space/
    └── .devcontainer/
        ├── devcontainer.json
        ├── docker-compose.yml
        └── Dockerfile
    ```

3.  **`docker-compose.yml` の記述:**
    フロントエンドとバックエンドのサービスを定義します。

    **(ファイルパス: `.devcontainer/docker-compose.yml`)**

    ```yaml
    version: "3.8"
    services:
      # メインの開発コンテナ (Angular Frontend)
      app:
        build:
          context: .
          dockerfile: Dockerfile
        volumes:
          # 1. ソースコード全体をホストと同期
          - ..:/workspace:cached
          # 2. 特定のフォルダを名前付きボリュームにマウントし、ホストとの同期から除外（パフォーマンス向上）
          - frontend_node_modules:/workspace/frontend/node_modules
          - ng_cache:/workspace/frontend/.angular/cache
        command: sleep infinity
        networks:
          - dev-network

      # バックエンド用のコンテナ (Node.js/Express)
      backend:
        image: node:16-bullseye
        working_dir: /workspace/backend
        volumes:
          # 1. ソースコード全体をホストと同期
          - ..:/workspace:cached
          # 2. node_modulesを名前付きボリュームにマウントし、ホストとの同期から除外
          - backend_node_modules:/workspace/backend/node_modules
        # コンテナ起動時に自動で依存関係をインストールし、サーバーを起動
        command: sh -c "npm install && npm start"
        ports:
          - "3000:3000"
        networks:
          - dev-network

    networks:
      dev-network:
        driver: bridge

    # パフォーマンス向上のための名前付きボリューム定義
    # ここで定義した名前のボリュームがDockerによって管理される
    volumes:
      frontend_node_modules:
      backend_node_modules:
      ng_cache:
    ```

4.  **`Dockerfile` の記述:**
    Angular 開発用のコンテナイメージを定義します。Node.js をベースに Angular CLI をインストールします。

    **(ファイルパス: `.devcontainer/Dockerfile`)**

    ```Dockerfile
    # Node.js 16をベースイメージとして使用
    FROM node:16-bullseye

    # sudoをインストールし、nodeユーザーにパスワードなしsudo権限を付与
    # これにより、コンテナ作成後のコマンドで権限を変更できる
    RUN apt-get update && apt-get install -y sudo \
        && echo "node ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/nopasswd \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

    # Angular CLI v14をグローバルにインストール
    # イメージビルド時にインストールしておくことで、コンテナ再作成時の時間を短縮
    RUN npm install -g @angular/cli@14 --force

    # タイムゾーンを日本時間に設定 (任意)
    ENV TZ=Asia/Tokyo
    RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
    ```

5.  **`devcontainer.json` の記述:**
    DevContainer の挙動を定義する中心的なファイルです。

    **(ファイルパス: `.devcontainer/devcontainer.json`)**

    ```json
    {
      "name": "Angular 14 Learning Space",
      "dockerComposeFile": "docker-compose.yml",
      "service": "app",
      "workspaceFolder": "/workspace",

      "forwardPorts": [4200, 3000],

      // コンテナ作成後、ワークスペースの所有権をnodeユーザーに変更し、念のためAngular CLIも再インストール
      "postCreateCommand": "sudo chown -R node:node /workspace && sudo npm install -g @angular/cli@14",

      "customizations": {
        "vscode": {
          "extensions": [
            "Angular.ng-template",
            "esbenp.prettier-vscode",
            "dbaeumer.vscode-eslint",
            "firsttris.vscode-jest-runner",
            "humao.rest-client"
          ]
        }
      },

      "remoteUser": "node"
    }
    ```

### 1.3. DevContainer の起動

1.  VSCode で `angular-learning-space` フォルダを開いていることを確認します。
2.  左下の緑色の `><` アイコンをクリックするか、`F1`キーを押してコマンドパレットを開き、`Remote-Containers: Reopen in Container` を選択します。
3.  初回はコンテナイメージのビルドに数分かかります。ビルドが完了すると、VSCode がリロードされ、コンテナ内の環境に接続された状態になります。左下の表示が `Dev Container: Angular 14 Learning Space` となっていれば成功です。

---

## 2. ベースアプリケーション作成

次に、今後の開発の土台となるバックエンド API と Angular アプリケーションの雛形を作成します。作業はすべて DevContainer に接続された VSCode 内で行います。

### 2.1. バックエンド (Node.js + Express) の作成

1.  **ターミナルを開く:** VSCode のメニューから `Terminal > New Terminal` を選択します。プロンプトが `/workspace $` となっていることを確認してください。
2.  **フォルダ作成と初期化:**
    ```bash
    cd backend
    npm init -y
    ```
3.  **必要なパッケージをインストール:**
    ```bash
    npm install express cors swagger-ui-express yamljs
    ```
4.  **データファイルの作成:**
    `backend`フォルダ内に`data`フォルダを作成し、その中にダミーデータ用の JSON ファイルを作成します。

    **(ファイルパス: `backend/data/items.json`)**

    ```json
    [
      { "id": 1, "name": "学習項目1: コンポーネントの作成", "completed": true },
      { "id": 2, "name": "学習項目2: サービスの利用", "completed": false },
      { "id": 3, "name": "学習項目3: HTTP通信の実装", "completed": false }
    ]
    ```

5.  **Swagger(API 仕様書)ファイルの作成:**

    **(ファイルパス: `backend/swagger.yaml`)**

    ```yaml
    openapi: 3.0.0
    info:
      title: Simple API for Angular Learning
      version: 1.0.0
      description: A simple API to be consumed by our Angular app.
    paths:
      /api/items:
        get:
          summary: Get all items
          responses:
            "200":
              description: A list of items.
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                        completed:
                          type: boolean
    ```

6.  **サーバー本体 (`server.js`) の作成:**

    **(ファイルパス: `backend/server.js`)**

    ```javascript
    const express = require("express");
    const cors = require("cors");
    const fs = require("fs/promises");
    const path = require("path");
    const swaggerUi = require("swagger-ui-express");
    const YAML = require("yamljs");

    const app = express();
    const PORT = 3000;
    const DATA_FILE = path.join(__dirname, "data", "items.json");

    // Middleware
    app.use(cors()); // CORSを許可
    app.use(express.json()); // JSONボディをパース

    // Swagger UI
    const swaggerDocument = YAML.load("./swagger.yaml");
    app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

    // API Routes
    app.get("/api/items", async (req, res) => {
      try {
        const data = await fs.readFile(DATA_FILE, "utf-8");
        res.json(JSON.parse(data));
      } catch (error) {
        res.status(500).json({ message: "Error reading data file." });
      }
    });

    app.listen(PORT, () => {
      console.log(`Backend server is running at http://localhost:${PORT}`);
      console.log(`API docs available at http://localhost:${PORT}/api-docs`);
    });
    ```

7.  **`package.json` の編集:**
    `server.js`を簡単に起動できるよう、`scripts`に`start`コマンドを追加します。

    **(ファイルパス: `backend/package.json`)**

    ```json
    {
      // ... 他の設定 ...
      "scripts": {
        "start": "node server.js", // この行を追加
        "test": "echo \"Error: no test specified\" && exit 1"
      }
      // ... 他の設定 ...
    }
    ```

### 2.2. フロントエンド (Angular 14) の作成

1.  **新しいターミナルを開く:** VSCode で新しいターミナルを開きます (`Ctrl+Shift+5` or `Cmd+Shift+5`)。
2.  **Angular プロジェクトの作成:**
    `/workspace` ディレクトリにいることを確認し、以下のコマンドで `frontend` フォルダに Angular プロジェクトを生成します。

    ```bash
    # `frontend`という名前のディレクトリにプロジェクトを作成
    # --routing: ルーティングモジュールを追加
    # --style=scss: スタイルをSCSSに設定
    # --strict: 厳格モードを有効化
    ng new frontend --routing=true --style=scss --strict=true
    ```

    いくつかの質問が表示されますが、すべて Enter キーでデフォルトを選択して問題ありません。

3.  **プロキシ設定の作成:**
    開発中に Angular アプリ(`localhost:4200`)から Express API(`localhost:3000`)を呼び出すと CORS エラーが発生します。これを回避するためにプロキシを設定します。
    `frontend`フォルダの直下に`proxy.conf.json`を作成します。

    **(ファイルパス: `frontend/proxy.conf.json`)**

    ```json
    {
      "/api": {
        "target": "http://backend:3000",
        "secure": false,
        "logLevel": "debug"
      }
    }
    ```

    **補足:** `target`を`http://localhost:3000`ではなく`http://backend:3000`としています。これは、`docker-compose.yml`で定義したサービス名でコンテナ間通信を行うためです。

4.  **`angular.json`の編集:**
    作成したプロキシ設定を Angular の開発サーバーが利用するように設定します。

    **(ファイルパス: `frontend/angular.json`)**
    `projects > frontend > architect > serve > options` のオブジェクトに `"proxyConfig": "proxy.conf.json"` を追加します。

    ```json
    // ...
    "architect": {
      "serve": {
        "builder": "@angular-devkit/build-angular:dev-server",
        "configurations": {
          "production": {
            "browserTarget": "frontend:build:production"
          },
          "development": {
            "browserTarget": "frontend:build:development"
          }
        },
        "defaultConfiguration": "development",
        "options": { // このoptionsオブジェクトを探す
          "proxyConfig": "proxy.conf.json" // この行を追加
        }
      },
    // ...
    ```

> [!TIP]  
> **`tsconfig.json`の編集:**  
> 型定義ファイル（.d.ts）の型チェックをスキップするオプションです。これにより、型定義ファイル内の型エラーを無視します。
>
> **(ファイルパス: `frontend/tsconfig.json`)** > `compilerOptions` セクションに `"skipLibCheck": true` を追加します。
>
> ```json
> // ...
> {
>   "compileOnSave": false,
>   "compilerOptions": {
>     ...
>     "lib": [
>       "es2020",
>       "dom"
>     ],
>     "skipLibCheck": true
>   },
> // ...
> ```

### 2.3. プログラムの実行とビルド

これで開発の準備が整いました。実際にサーバーを起動してみましょう。

1.  **バックエンドサーバーの起動:**

    - VSCode のターミナル（1 つ目）で、`backend`ディレクトリに移動します。
    - `npm start` を実行します。
    - `Backend server is running at http://localhost:3000` と表示されれば成功です。
    - ブラウザで `http://localhost:3000/api/items` や `http://localhost:3000/api-docs` にアクセスして動作を確認できます。

2.  **フロントエンド開発サーバーの起動:**

    - VSCode のターミナル（2 つ目）で、`frontend`ディレクトリに移動します。
    - `ng serve` を実行します。
    - コンパイルが完了すると、`http://localhost:4200/` でアプリケーションにアクセスできます。
    - VSCode がポートのフォワーディングを提案してきた場合は、「Open in Browser」をクリックしてください。

3.  **動作確認:**
    Angular のデフォルトページが表示されていれば成功です。これで、バックエンドと通信可能な Angular の開発環境が完成しました。

4.  **ビルド（参考）:**
    アプリケーションを本番環境向けにビルドするには、`frontend`ディレクトリで以下のコマンドを実行します。

    ```bash
    ng build
    ```

    これにより、`frontend/dist/frontend/` ディレクトリに静的な HTML/CSS/JS ファイルが生成されます。これらを Web サーバーに配置することで、アプリケーションを公開できます。

---

## 3. 学習ロードマップ（サンプルアプリ 10 選）

上記のベースアプリケーションを元に、段階的に Angular の機能を学んでいくためのサンプルアプリのアイデアを 10 個提案します。簡単なものから順に挑戦してみてください。

---

#### No. 1：データバインディング表示アプリ

1.  **アプリ名:**
    API データビューア
2.  **Angular 観点で身に付く知識、スキル:**
    - `Component` の基本構造（`ts`, `html`, `scss`ファイルの関係）
    - データバインディング: `Interpolation` (補間 `{{ }}`), `Property Binding` (`[ ]`), `Event Binding` (`( )`)
    - ディレクティブ: `*ngFor`, `*ngIf`
    - `HttpClientModule` と `HttpClient` を使った基本的な API 通信
3.  **提案の理由と習得によるメリット:**
    Angular の最も基本的な機能である「コンポーネント」と「データバインディング」を最初に固めるためのステップです。バックエンド API から取得したデータを画面に表示する一連の流れを体験することで、Angular アプリケーションの骨格を理解できます。これができれば、あらゆる動的な Web ページ作成の基礎が身に付きます。

---

#### No. 2：親子コンポーネントカウンター

1.  **アプリ名:**
    インタラクティブ・カウンター
2.  **Angular 観点で身に付く知識、スキル:**
    - コンポーネントの分割と再利用
    - 親から子へのデータ伝達: `@Input()` デコレータ
    - 子から親へのイベント通知: `@Output()` デコレータと `EventEmitter`
3.  **提案の理由と習得によるメリット:**
    単一コンポーネントから脱却し、複数のコンポーネントを連携させる方法を学びます。`@Input`と`@Output`はコンポーネント設計の中核となる概念です。これをマスターすることで、UI を再利用可能な部品に分割して、複雑な画面を整理・構築する能力が飛躍的に向上します。

---

#### No. 3：ToDo リストアプリ

1.  **アプリ名:**
    サービスクラス分離型 ToDo リスト
2.  **Angular 観点で身に付く知識、スキル:**
    - `Service` の作成と役割
    - `Dependency Injection (DI)` (依存性の注入) の概念と実践
    - コンポーネントからビジネスロジック（データ操作など）を分離する設計
    - 双方向データバインディング: `[(ngModel)]` と `FormsModule`
3.  **提案の理由と習得によるメリット:**
    コンポーネントにすべてのロジックを書くのではなく、データ操作や API 通信などを「サービス」として切り出す設計パターンを学びます。DI の仕組みを理解することで、テストしやすく、再利用性の高いコードを書けるようになります。これは中規模以上のアプリケーション開発に必須のスキルです。

---

#### No. 4：シンプルブログ（ルーティング）

1.  **アプリ名:**
    記事一覧＆詳細ページ
2.  **Angular 観点で身に付く知識、スキル:**
    - `Angular Router` の設定 (`RouterModule.forRoot`)
    - `<router-outlet>` の役割
    - `routerLink` ディレクティブによる画面遷移
    - `ActivatedRoute` を使った URL パラメータ（例: `/posts/:id`）の取得
3.  **提案の理由と習得によるメリット:**
    シングルページアプリケーション（SPA）の核となる画面遷移（ルーティング）を学びます。複数のページを持つアプリケーションの作り方を理解し、URL とコンポーネントを対応付けることができます。これにより、ユーザー体験の良い本格的な Web アプリケーションの構築が可能になります。

---

#### No. 5：リアルタイム検索ボックス (RxJS)

1.  **アプリ名:**
    インクリメンタルサーチ機能
2.  **Angular 観点で身に付く知識、スキル:**
    - リアクティブプログラミングの考え方
    - `RxJS` の基本的な使い方 (`Observable`, `Subject`)
    - RxJS オペレータ: `pipe`, `debounceTime`, `distinctUntilChanged`, `switchMap`
    - `async` パイプによる `Observable` の自動購読管理
3.  **提案の理由と習得によるメリット:**
    Angular で多用される RxJS の強力さを体験します。ユーザーの入力イベントのような非同期ストリームを効率的に処理する方法を学びます。これにより、サーバーへの不要なリクエストを削減したり、複雑な非同期処理を宣言的でクリーンなコードで記述できるようになります。

---

#### No. 6：ユーザー登録フォーム (Reactive Forms)

1.  **アプリ名:**
    リアクティブフォームによる入力画面
2.  **Angular 観点で身に付く知識、スキル:**
    - `ReactiveFormsModule`
    - `FormGroup`, `FormControl`, `FormBuilder`
    - フォームのバリデーション（`Validators`）とエラーメッセージ表示
    - フォームの値の取得と送信
3.  **提案の理由と習得によるメリット:**
    Angular が推奨する強力なフォーム制御手法である Reactive Forms を学びます。複雑なバリデーションルールや動的なフォームの生成など、テンプレート駆動フォーム (`ngModel`) では難しい要件にも対応できます。エンタープライズレベルの堅牢な入力フォームを実装するスキルが身に付きます。

---

#### No. 7：スタンドアロンコンポーネント (v14 新機能)

1.  **アプリ名:**
    NgModule 不要の UI ウィジェット
2.  **Angular 観点で身に付く知識、スキル:**
    - `Standalone Components` の作成 (`standalone: true`)
    - コンポーネント自身の `imports` 配列に必要な依存関係を定義する方法
    - `bootstrapApplication` を使ったアプリケーションの起動
    - Standalone API を使ったルーティング設定
3.  **提案の理由と習得によるメリット:**
    Angular v14 の目玉機能であり、今後の主流となるであろう`Standalone` API を学びます。`NgModule`の記述を減らし、コンポーネントの自己完結性を高めることで、コードの見通しが良くなり、より直感的な開発が可能になります。この新しいパラダイムを習得することで、モダンな Angular 開発の最前線に立つことができます。

---

#### No. 8：シンプルな状態管理（Service with BehaviorSubject）

1.  **アプリ名:**
    ショッピングカート機能
2.  **Angular 観点で身に付く知識、スキル:**
    - `BehaviorSubject` を使った状態管理サービスの設計
    - アプリケーション全体で共有される状態（カートの中身など）の管理方法
    - 複数のコンポーネントが単一のデータソースを購読・更新するパターン
3.  **提案の理由と習得によるメリット:**
    `NgRx`のような大規模な状態管理ライブラリを導入する前に、RxJS とサービスだけで状態管理を実現する方法を学びます。これにより、状態管理の基本的な考え方を理解でき、小〜中規模アプリケーションにおいて最適な設計を選択する能力が身に付きます。

---

#### No. 9：高度なルーティング（遅延読み込みとガード）

1.  **アプリ名:**
    管理者専用ダッシュボード
2.  **Angular 観点で身に付く知識、スキル:**
    - 機能モジュール (`Feature Module`) の作成
    - 遅延読み込み (`Lazy Loading`) の設定 (`loadChildren`)
    - ルートガード (`CanActivate`) を使ったアクセス制御
3.  **提案の理由と習得によるメリット:**
    大規模アプリケーションに必須のパフォーマンス最適化技術である「遅延読み込み」を学びます。初回ロード時のバンドルサイズを削減し、アプリケーションの起動速度を劇的に改善できます。また、ルートガードにより特定のユーザーしかアクセスできないページを実装でき、セキュリティを向上させることができます。

---

#### No. 10：パフォーマンス最適化 (`OnPush`)

1.  **アプリ名:**
    高頻度更新データ表示パネル
2.  **Angular 観点で身に付く知識、スキル:**
    - Angular の変更検知 (`Change Detection`) の仕組み
    - `ChangeDetectionStrategy.OnPush` の設定と効果
    - `@Input`参照の不変性 (`Immutability`) の重要性
    - `ChangeDetectorRef` を使った手動での変更検知のトリガー
3.  **提案の理由と習得によるメリット:**
    Angular のパフォーマンスチューニングの核心に触れます。`OnPush`を使いこなすことで、不要な再描画を劇的に減らし、アプリケーションの応答性を高めることができます。データが大量に表示されたり、高頻度で更新されたりする画面でも、スムーズなユーザー体験を提供するための高度なテクニックが身に付きます。

---

以上のステップで、Angular の基礎から応用、そして最新機能までを体系的に学習できます。まずは環境構築から始めて、一つずつ着実に進めていきましょう。応援しています！
