承知いたしました。
それでは、学習ロードマップの No. 7「スタンドアロンコンポーネント (v14 新機能)」について、ステップバイステップで解説します。

このチュートリアルでは、前回作成したベースアプリケーションを、Angular v14 の目玉機能である**Standalone Components**を使ったアーキテクチャに移行します。これにより、`NgModule`の記述から解放され、よりシンプルで直感的なコンポーネント開発を体験できます。

---

### はじめに：学習目標と Standalone Components の概要

#### 🎯 このステップでの学習目標

1.  **Standalone Components の概念**を理解する。
2.  `ng generate`コマンドで Standalone Component を**作成**できる。
3.  既存の`NgModule`ベースのアプリケーションを、Standalone ベースに**移行**できる。
4.  `bootstrapApplication`関数を使った新しいアプリケーションの**起動方法**を理解する。
5.  Standalone Component を**ルーティングで利用する**（遅延読み込みを含む）方法を習得する。

#### 💡 Standalone Components とは？

従来の Angular では、すべてのコンポーネント、ディレクティブ、パイプは、必ず`NgModule`に`declarations`（宣言）する必要がありました。`NgModule`は、関連する部品をグループ化し、依存関係（他のモジュールやサービスなど）を管理する役割を担っていました。

しかし、アプリケーションが大きくなるにつれて`NgModule`の管理は複雑になりがちでした。

**Standalone Components**は、この`NgModule`への依存をなくし、コンポーネント自身が必要な依存関係を直接`imports`できる仕組みです。

**主なメリット:**

- **コードの削減:** `NgModule`ファイルが不要になり、記述量が減ります。
- **自己完結性:** コンポーネントファイルを見れば、そのコンポーネントが何に依存しているかが一目瞭然になります。
- **直感的な学習曲線:** `NgModule`という概念を一旦脇に置いてコンポーネント開発に集中できるため、初学者が学びやすくなります。
- **Tree-shaking の向上:** ビルド時に不要なコードを削除する最適化（Tree-shaking）がより効率的に行われやすくなります。

それでは、実際に手を動かして学んでいきましょう。

---

### ステップバイステップ・チュートリアル

作業はすべて、前回構築した DevContainer 環境に接続された VSCode 内で行います。
`frontend`ディレクトリで作業を進めます。

```bash
# VSCodeのターミナルを開き、frontendディレクトリに移動します
cd frontend
```

#### Step 1: 既存アプリケーションの整理と AppComponent の Standalone 化

まず、アプリケーションのルートとなる`AppComponent`を Standalone 化します。これにより、アプリケーション全体が`NgModule`から独立する第一歩を踏み出します。

1.  **`app.component.ts` を編集:**
    `@Component`デコレータに `standalone: true` を追加し、`NgModule`が担っていた依存関係を`imports`配列に移動させます。

    **(ファイルパス: `frontend/src/app/app.component.ts`)**

    ```typescript
    import { Component } from "@angular/core";
    // RouterModuleをインポートします。これにより<router-outlet>が使えるようになります。
    import { RouterModule } from "@angular/router";
    // HttpClientをインポートします（このコンポーネントでは直接使いませんが、後でサービスが使うため）。
    import { HttpClientModule } from "@angular/common/http";

    @Component({
      selector: "app-root",
      // standalone: true を追加することが、Standalone Componentにするための宣言です。
      standalone: true,
      // このコンポーネントのテンプレート内で使用する他のコンポーネント、ディレクティブ、パイプ、モジュールをここに記述します。
      // 以前はAppModuleに記述していましたが、それをこのコンポーネント自身が持つ形になります。
      imports: [
        RouterModule, // <router-outlet>やrouterLinkディレクティブのために必要
        HttpClientModule, // HttpClientサービスをアプリケーション全体で利用可能にするために必要
        // 本来はmain.tsでprovideHttpClient()を使うのがv15以降の推奨ですが、
        // v14の学習としてNgModuleの役割を移行するイメージを掴むため、ここではHttpClientModuleをインポートします。
      ],
      templateUrl: "./app.component.html",
      styleUrls: ["./app.component.scss"],
    })
    export class AppComponent {
      title = "frontend";
    }
    ```

    **学習ポイント:**
    `standalone: true` を指定すると、このコンポーネントは`NgModule`に属さなくなります。その代わり、テンプレートで使う`<router-outlet>`などの機能は、`imports`配列に`RouterModule`を直接追加して解決します。

2.  **`app.component.html`をシンプルにする:**
    後のステップでルーティングを使ってコンテンツを表示するため、デフォルトの HTML をシンプルなものに置き換えます。

    **(ファイルパス: `frontend/src/app/app.component.html`)**

    ```html
    <!-- <h1>ようこそ、{{ title }}!</h1> -->

    <header>
      <h1>Angular v14 Standalone Demo</h1>
      <nav>
        <!-- routerLinkディレクティブで、クリックすると指定したパスに遷移します -->
        <a routerLink="/">Home</a> |
        <a routerLink="/widget">Standalone Widget (Lazy Loaded)</a>
      </nav>
    </header>

    <main>
      <!-- <router-outlet>は、現在のルートに対応するコンポーネントを描画する場所です -->
      <router-outlet></router-outlet>
    </main>

    <footer>
      <p>Learning Standalone Components in Angular 14</p>
    </footer>
    ```

#### Step 2: アプリケーションの起動方法を変更 (`main.ts`)

`AppModule`を使わなくなったため、アプリケーションを起動する方法も新しい方法`bootstrapApplication`に変更する必要があります。

1.  **`main.ts` を編集:**
    `platformBrowserDynamic().bootstrapModule(AppModule)` を `bootstrapApplication(AppComponent, ...)` に置き換えます。

    **(ファイルパス: `frontend/src/main.ts`)**

    ```typescript
    import { enableProdMode, importProvidersFrom } from "@angular/core";
    import { bootstrapApplication } from "@angular/platform-browser";
    import { RouterModule } from "@angular/router";

    import { AppComponent } from "./app/app.component";
    import { AppRoutingModule } from "./app/app-routing.module"; // 後でルーティング設定を直接記述するため、まだ残しておきます
    import { environment } from "./environments/environment";

    if (environment.production) {
      enableProdMode();
    }

    // これが新しいアプリケーション起動方法です
    bootstrapApplication(AppComponent, {
      // アプリケーション全体で利用可能にするサービスや設定（プロバイダー）をここに記述します。
      // 以前はAppModuleのproviders配列やimports配列で設定していました。
      providers: [
        // importProvidersFromは、既存のNgModuleベースの設定をプロバイダー形式に変換してくれる便利なユーティリティです。
        // ここでAppRoutingModuleをインポートして、ルーティング設定を有効にします。
        importProvidersFrom(AppRoutingModule),
      ],
    }).catch((err) => console.error(err));
    ```

    **学習ポイント:**
    `bootstrapApplication`は 2 つの引数を取ります。

    1.  **ルートコンポーネント:** 起動する Standalone Component (`AppComponent`)。
    2.  **アプリケーション設定:** `providers`配列を含むオブジェクト。ここに DI（依存性注入）システムに登録したいサービスや設定を記述します。`RouterModule`の設定もここで行います。

#### Step 3: 不要になった`AppModule`を削除

`AppComponent`が Standalone 化し、`main.ts`も新しい起動方法になったので、`app.module.ts`は完全に不要になりました。

1.  **`app.module.ts` を削除:**
    VSCode のエクスプローラーから `frontend/src/app/app.module.ts` ファイルを右クリックし、削除します。

    **学習ポイント:**
    `NgModule`が 1 つ減りました！これが Standalone アーキテクチャの直接的なメリットの一つです。コンポーネントとアプリケーション起動ファイルだけで構成が完結し、見通しが良くなりました。

#### Step 4: 新しい Standalone Component の作成とルーティング設定

次に、新しい Standalone Component を`ng generate`コマンドで作成し、それを遅延読み込み（Lazy Loading）するルーティングを設定します。

1.  **新しい Standalone Component を生成:**
    ターミナルで以下のコマンドを実行します。`--standalone`フラグがポイントです。

    ```bash
    # `components`フォルダに`standalone-widget`という名前のコンポーネントを
    # --standaloneフラグ付きで作成します。
    ng generate component components/standalone-widget --standalone
    ```

    これにより、`NgModule`に宣言されることなく、`standalone-widget.component.ts` ファイルが単体で生成されます。

2.  **生成された Widget コンポーネントを編集:**
    中身がわかるように簡単なメッセージと、API からデータを取得するロジックを追加します。

    **(ファイルパス: `frontend/src/app/components/standalone-widget/standalone-widget.component.ts`)**

    ```typescript
    import { Component, OnInit } from "@angular/core";
    // CommonModuleをインポートすることで、*ngFor, *ngIf, asyncパイプなどが使えるようになります。
    import { CommonModule } from "@angular/common";
    import { HttpClient } from "@angular/common/http";
    import { Observable } from "rxjs";

    // APIから返ってくるデータの型を定義しておくと、コードの安全性が高まります。
    interface ApiItem {
      id: number;
      name: string;
      completed: boolean;
    }

    @Component({
      selector: "app-standalone-widget",
      // このコンポーネントもstandaloneです。
      standalone: true,
      // このコンポーネント内で使う機能だけをimportsします。
      // CommonModuleがないと、テンプレートで*ngForなどが使えません。
      imports: [CommonModule],
      templateUrl: "./standalone-widget.component.html",
      styleUrls: ["./standalone-widget.component.scss"],
    })
    export class StandaloneWidgetComponent implements OnInit {
      // APIから取得したデータを格納するObservable
      public items$!: Observable<ApiItem[]>;

      // DIを使ってHttpClientのインスタンスを注入します。
      constructor(private http: HttpClient) {}

      ngOnInit(): void {
        // コンポーネントが初期化されたときにAPIを呼び出します。
        // プロキシ設定が効いているので、`/api/items` だけでバックエンド(localhost:3000)にリクエストが飛びます。
        this.items$ = this.http.get<ApiItem[]>("/api/items");
      }
    }
    ```

3.  **Widget コンポーネントのテンプレートを編集:**

    **(ファイルパス: `frontend/src/app/components/standalone-widget/standalone-widget.component.html`)**

    ```html
    <h2>Hello from a Standalone Widget!</h2>
    <p>This component was lazy-loaded without any NgModule.</p>
    <p>It fetches data from the backend API:</p>

    <!--
      items$ は Observable なので、そのままでは表示できません。
      async パイプを使うと、Observableを自動で購読(subscribe)し、
      データが流れてきたら表示してくれます。コンポーネントが破棄されると自動で購読解除(unsubscribe)もしてくれる優れものです。
    -->
    <ul *ngIf="items$ | async as items; else loading">
      <!-- itemsが空の場合の表示 -->
      <li *ngIf="items.length === 0">No items found.</li>
      <!-- items配列をループして表示 -->
      <li *ngFor="let item of items">
        {{ item.name }} - {{ item.completed ? 'Completed' : 'Pending' }}
      </li>
    </ul>

    <!-- items$がまだデータを受信していない間（ローディング中）に表示するテンプレート -->
    <ng-template #loading>
      <p>Loading data...</p>
    </ng-template>
    ```

4.  **ルーティング設定の変更 (`app-routing.module.ts`)**
    最後に、この新しいコンポーネントへのルートを追加します。Standalone API では、`loadComponent`を使ってコンポーネントを直接遅延読み込みできます。

    **(ファイルパス: `frontend/src/app/app-routing.module.ts`)**

    ```typescript
    import { NgModule } from "@angular/core";
    import { RouterModule, Routes } from "@angular/router";

    const routes: Routes = [
      {
        path: "widget",
        // これがStandalone Componentの遅延読み込みの書き方です。
        // 以前の `loadChildren` はモジュールを読み込んでいましたが、
        // `loadComponent` はコンポーネントを直接読み込みます。
        loadComponent: () =>
          import(
            "./components/standalone-widget/standalone-widget.component"
          ).then((m) => m.StandaloneWidgetComponent), // importしたファイルからコンポーネントクラスを返す
      },
      // ホーム画面用のコンポーネントを一時的に作成しても良いですが、
      // ここでは空のパスでリダイレクトする例を示します。
      {
        path: "",
        pathMatch: "full",
        redirectTo: "widget", // デフォルトで/widgetに飛ばす
      },
    ];

    @NgModule({
      imports: [RouterModule.forRoot(routes)],
      exports: [RouterModule],
    })
    export class AppRoutingModule {}
    ```

    **学習ポイント:**
    `loadComponent`は`NgModule`を介さずにコンポーネントを遅延読み込みするための新しい方法です。これにより、ユーザーが特定のページにアクセスするまで、そのコンポーネントのコードはダウンロードされません。これはアプリケーションの初期表示速度を向上させる非常に重要なテクニックです。

---

### 最終確認と実行

すべての変更が完了しました。最終的な`frontend/src/app`ディレクトリの主要なファイル構成は以下のようになっているはずです。

```
frontend/src/app/
├── app.component.html
├── app.component.scss
├── app.component.ts     # Standalone化済み
├── app-routing.module.ts # loadComponentを使用
└── components/
    └── standalone-widget/
        ├── standalone-widget.component.html
        ├── standalone-widget.component.scss
        └── standalone-widget.component.ts # Standaloneとして生成
```

`app.module.ts`がなくなっていることに注目してください。

#### アプリケーションの実行

1.  VSCode のターミナルで、バックエンドとフロントエンドが起動していることを確認します。もし停止していたら、それぞれのディレクトリで起動し直してください。

    - **バックエンド:** `backend`ディレクトリで `npm start`
    - **フロントエンド:** `frontend`ディレクトリで `ng serve`

2.  ブラウザで `http://localhost:4200` を開きます。
    - デフォルトルートが`/widget`にリダイレクトされるため、「Hello from a Standalone Widget!」という見出しが表示されます。
    - 少し待つと、「Loading data...」という表示が消え、バックエンド API から取得した ToDo リストが表示されるはずです。
    - ブラウザの開発者ツール（F12 キー）のネットワークタブを開いてページをリロードすると、`widget`コンポーネントの JavaScript ファイル（例: `src_app_components_standalone-widget_standalone-widget_component_ts.js`）が、最初に読み込まれず、後から動的に読み込まれていることが確認できます。これが遅延読み込みの証拠です。

### まとめ：Standalone Components で得られたもの

今回のチュートリアルを通して、以下のことを実践的に学びました。

- **コンポーネントの独立:** `standalone: true`と`imports`配列により、コンポーネントは`NgModule`から解放され、自己完結しました。
- **シンプルな起動プロセス:** `bootstrapApplication`により、アプリケーションの起動がより直接的で分かりやすくなりました。
- **コードの簡潔化:** ボイラープレートであった`AppModule`を削除し、プロジェクト全体の見通しが良くなりました。
- **モダンな遅延読み込み:** `loadComponent`を使うことで、`NgModule`なしにコンポーネント単位での遅延読み込みを簡単に実装できました。

Standalone Components は、Angular 開発をよりモダンで生産的なものにするための大きな一歩です。この新しいパラダイムをマスターすることで、今後の Angular プロジェクトをより効率的に、そしてクリーンに構築していくことができるでしょう。

---

## 既存コードからの Standalone Component への移行

承知いたしました。
既存の Angular NgModule アプリケーションを、Standalone Components ベースのアーキテクチャへ段階的に移行する方法について、具体的な戦略、過渡期のコードサンプル、そして注意点を詳細に解説します。

このガイドは、大規模なリファクタリングを一度に行うのではなく、**開発を続けながら安全に、少しずつ移行していく**ことを目的としています。

---

### 1. 段階的移行の戦略：葉から根へ (Leaf-to-Root)

一気にすべての`NgModule`をなくそうとすると、アプリケーションの規模によっては非常に大きな作業となり、リスクも高まります。そこで推奨されるのが、**「葉から根へ」**というアプローチです。

- **葉 (Leaf):** アプリケーションの末端にある、依存関係の少ないコンポーネント（例: 共通のボタン、カード、モーダルなどの UI コンポーネント）。
- **枝 (Branch):** 特定の機能を持つ Feature Module（例: ユーザー管理機能、商品一覧ページなど）。
- **幹 (Trunk):** アプリケーション全体で共有される`SharedModule`や`CoreModule`。
- **根 (Root):** アプリケーションの起点である`AppModule`と`AppComponent`。

この「葉 → 枝 → 幹 → 根」の順で移行を進めることで、影響範囲を限定し、一つ一つの変更を確実にテストしながら進めることができます。

#### 移行ステッププラン

1.  **【準備】新機能は Standalone で:**
    これから開発する新しい機能やコンポーネントは、原則として`--standalone`フラグを付けて生成します。これにより、既存コードに影響を与えることなく、新しいアーキテクチャに慣れることができます。

2.  **【葉】末端の共通 UI コンポーネントを Standalone 化:**
    `SharedModule`で宣言・エクスポートされているような、再利用可能な UI コンポーネント（例: `ButtonComponent`, `CardComponent`）から始めます。これらは依存関係が少ないため、最初のステップとして最適です。

3.  **【枝】Feature Module を Standalone ベースに置き換える:**
    遅延読み込みされている Feature Module（例: `UserModule`）をリファクタリングします。

    - `UserModule`内の各コンポーネントを Standalone 化します。
    - `UserModule`自体を削除します。
    - ルーティング設定を`loadChildren`から`loadComponent`（または、ルートコンポーネントだけを読み込み、子ルートは`children`プロパティで定義する）に変更します。

4.  **【幹】SharedModule / CoreModule の解体:**
    `SharedModule`は、多くのコンポーネントやモジュールからインポートされているため、影響範囲が広いです。

    - `SharedModule`がエクスポートしていた Standalone 化済みのコンポーネントやパイプを、それらを使用する各コンポーネントや`NgModule`の`imports`配列に直接追加するように変更します。
    - `CoreModule`が提供していたシングルトンサービスは、`provideIn: 'root'`に移行するか、`main.ts`の`providers`に移動します。

5.  **【根】AppComponent の Standalone 化と AppModule の削除:**
    最後に、アプリケーションのルートである`AppComponent`を Standalone 化し、`main.ts`を`bootstrapApplication`に書き換え、`AppModule`を完全に削除します。これが移行の最終ゴールです。

---

### 2. 過渡期のサンプルアプリケーションとコード解説

ここでは、「NgModule ベースの既存機能」と「新しい Standalone コンポーネント」が共存する過渡期の状態を具体的に見ていきましょう。

#### シナリオ設定

以下のような構成の既存アプリケーションがあるとします。

```
app/
├── app.module.ts         # Root Module
├── app-routing.module.ts # Root Routing
├── app.component.ts      # Root Component
|
├── features/
│   └── items/
│       ├── items.module.ts         # Feature Module (Lazy Loaded)
│       ├── items-routing.module.ts
│       └── items-list/
│           └── items-list.component.ts
|
└── shared/
    ├── shared.module.ts      # 共通部品を提供するModule
    └── components/
        └── card/
            └── card.component.ts # 共通UIコンポーネント
```

- `SharedModule`は`CardComponent`を宣言・エクスポートしています。
- `ItemsModule`は`SharedModule`をインポートし、`CardComponent`を使っています。
- `app-routing.module.ts`は`ItemsModule`を遅延読み込みしています。

#### Step 1: 「葉」の移行 (`CardComponent`を Standalone 化)

まず、末端の`CardComponent`を Standalone 化し、`SharedModule`と`ItemsModule`を修正します。

1.  **`card.component.ts` を編集:**
    `standalone: true`を追加し、`*ngIf`などのために`CommonModule`をインポートします。

    **(ファイルパス: `shared/components/card/card.component.ts`)**

    ```typescript
    import { Component, Input } from "@angular/core";
    import { CommonModule } from "@angular/common"; // *ngIfなどを使うために必要

    @Component({
      selector: "app-card",
      // Standalone Componentであることを宣言
      standalone: true,
      // このコンポーネントが必要とする依存関係を直接インポート
      imports: [CommonModule],
      template: `
        <div class="card">
          <div class="card-header" *ngIf="title">
            {{ title }}
          </div>
          <div class="card-body">
            <ng-content></ng-content>
          </div>
        </div>
      `,
      styles: [
        /* ... */
      ],
    })
    export class CardComponent {
      @Input() title?: string;
    }
    ```

2.  **`shared.module.ts` から `CardComponent` を削除:**
    `CardComponent`はもう`NgModule`に属さないため、`SharedModule`での宣言・エクスポートは不要になります。

    **(ファイルパス: `shared/shared.module.ts`)**

    ```typescript
    import { NgModule } from "@angular/core";
    import { CommonModule } from "@angular/common";
    // import { CardComponent } from './components/card/card.component'; // 削除

    @NgModule({
      // declarations から CardComponent を削除
      declarations: [],
      imports: [CommonModule],
      // exports から CardComponent を削除
      exports: [
        CommonModule, // CommonModuleはまだ他のNgModuleのためにエクスポートしておく
      ],
    })
    export class SharedModule {}
    ```

3.  **`items.module.ts` を修正:**
    `SharedModule`経由ではなく、`CardComponent`を直接インポートするように変更します。

    **(ファイルパス: `features/items/items.module.ts`)**

    ```typescript
    import { NgModule } from "@angular/core";
    import { CommonModule } from "@angular/common";
    import { ItemsRoutingModule } from "./items-routing.module";
    import { ItemsListComponent } from "./items-list/items-list.component";

    // 変更前: import { SharedModule } from '../../shared/shared.module';
    // Standalone化されたコンポーネントを直接インポートする
    import { CardComponent } from "../../shared/components/card/card.component";

    @NgModule({
      declarations: [ItemsListComponent],
      imports: [
        CommonModule,
        ItemsRoutingModule,
        // 変更前: SharedModule
        // Standalone ComponentはNgModuleのimports配列に直接追加して使用する
        CardComponent,
      ],
    })
    export class ItemsModule {}
    ```

**この時点での状態:**
`CardComponent`は Standalone になりましたが、それを使っている`ItemsModule`はまだ`NgModule`のままです。このように、**Standalone Component は NgModule 内でも問題なく利用できます。** これが段階的移行の鍵です。

#### Step 2: 新機能を Standalone として追加

次に、既存の構造はそのままに、全く新しい機能を Standalone Component として遅延読み込みで追加します。

1.  **新しい Standalone Component を生成:**

    ```bash
    # `features`フォルダに`report`という新しいコンポーネントをstandaloneで作成
    ng g c features/report --standalone
    ```

    これにより`report.component.ts`が生成されます。

2.  **`app-routing.module.ts` に新しいルートを追加:**
    `NgModule`ベースの`loadChildren`と、`Standalone`ベースの`loadComponent`が共存するルーティングファイルを作成します。

    **(ファイルパス: `app-routing.module.ts`)**

    ```typescript
    import { NgModule } from "@angular/core";
    import { RouterModule, Routes } from "@angular/router";

    const routes: Routes = [
      {
        path: "items",
        // 【既存】NgModuleベースの遅延読み込み
        loadChildren: () =>
          import("./features/items/items.module").then((m) => m.ItemsModule),
      },
      {
        path: "report",
        // 【新規】Standalone Componentベースの遅延読み込み
        loadComponent: () =>
          import("./features/report/report.component").then(
            (m) => m.ReportComponent
          ),
      },
      {
        path: "",
        redirectTo: "items",
        pathMatch: "full",
      },
    ];

    @NgModule({
      imports: [RouterModule.forRoot(routes)],
      exports: [RouterModule],
    })
    export class AppRoutingModule {}
    ```

**この時点での状態:**
アプリケーションは、NgModule ベースの遅延読み込みと Standalone Component ベースの遅延読み込みの両方をサポートしています。新しい機能開発を Standalone で進めつつ、既存機能はそのまま動作させることが可能です。

---

### 3. 移行時の注意点とベストプラクティス

1.  **依存関係の明示化:**

    - **メリット:** Standalone Component は、そのファイルを見るだけで依存関係（`imports`配列）が明確になります。
    - **デメリット:** これまで`SharedModule`を 1 つインポートすれば済んでいたものが、`CommonModule`, `FormsModule`, `CardComponent`, `ButtonComponent`... のように、個別にインポートする必要が出てきます。コードが冗長に感じることもありますが、これは意図された「明示性」のトレードオフです。

2.  **DI (Dependency Injection) の考慮:**

    - **シングルトンサービス:** `CoreModule`で`providedIn: 'root'`なしに提供されていたサービスは、`main.ts`の`bootstrapApplication`の`providers`配列に移動するか、サービス自体に`@Injectable({ providedIn: 'root' })`を追加するのが最もクリーンな解決策です。
    - **フィーチャースコープのサービス:** Feature Module の`providers`配列で提供されていたサービス（そのフィーチャー内だけで使われるインスタンス）は、**ルートの`providers`プロパティ**に定義することで同じ挙動を再現できます。
      ```typescript
      // ルーティング設定で、特定のルートツリーでのみ有効なサービスを定義する
      {
        path: 'admin',
        loadComponent: () => import('./admin/admin.component'),
        providers: [AdminOnlyService] // このサービスは/admin配下でのみ利用可能
      }
      ```

3.  **サードパーティ製ライブラリの扱い:**
    多くの UI ライブラリ（例: Angular Material）は、v14 時点ではまだ`NgModule`ベースです。これらのライブラリを使う Standalone Component では、`imports`配列に必要な`NgModule`（例: `MatButtonModule`, `MatCardModule`）を追加します。

    ```typescript
    import { MatButtonModule } from "@angular/material/button";
    import { MatCardModule } from "@angular/material/card";

    @Component({
      standalone: true,
      imports: [CommonModule, MatCardModule, MatButtonModule],
      // ...
    })
    export class MyStandaloneCardComponent {}
    ```

4.  **テストコードの修正:**
    コンポーネントのユニットテスト（`.spec.ts`）も修正が必要です。`TestBed.configureTestingModule`の`imports`配列に、テスト対象の Standalone Component そのものを追加します。

    ```typescript
    // 変更前（NgModuleベース）
    TestBed.configureTestingModule({
      declarations: [ItemsListComponent],
      imports: [SharedModule], // SharedModuleがCardComponentを提供していた
    });

    // 変更後（Standaloneベース）
    TestBed.configureTestingModule({
      // declarationsは不要
      imports: [
        ItemsListComponent, // テスト対象のコンポーネントを直接インポート
        // CardComponent // ItemsListComponentがCardComponentを使っている場合、それもインポート
      ],
    });

    // ItemsListComponentがStandalone化された場合
    TestBed.configureTestingModule({
      imports: [ItemsListComponent], // ItemsListComponentが内部でCardComponentをimportしていればこれだけで良い
    });
    ```

5.  **`ng g`コマンドの活用:**
    Angular CLI には、`NgModule`ベースのアプリを Standalone に移行するためのスキーマティックが用意されています（v15.2 以降でより強化）。
    ```bash
    ng generate @angular/core:standalone
    ```
    このコマンドを実行すると、移行のモード（例: 全コンポーネントを Standalone 化、`bootstrapApplication`に切り替えなど）を選択でき、自動でコードを変換してくれます。大規模な移行を行う際には、このツールの利用を検討すると良いでしょう。

以上の戦略と具体的な手順、注意点を踏まえることで、既存のアプリケーションを安全かつ着実に、新しい Standalone アーキテクチャへと進化させることができます。焦らず、一つ一つの部品を確実に移行していくことが成功の鍵です。
