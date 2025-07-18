承知いたしました。
学習ロードマップNo.1「APIデータビューア」について、ステップバイステップで詳細に解説します。

前回の回答で作成したDevContainer環境と、Node.js/Expressのバックエンドサーバーが動作していることを前提に進めます。

---

### **No.1 APIデータビューア 作成ガイド**

#### **はじめに**

この演習のゴールは、**「バックエンドAPIからデータを取得し、そのデータをAngularコンポーネントの画面に表示する」**という、Webアプリケーションの最も基本的な処理フローを実装することです。

この過程で、Angularの根幹をなす以下の要素を学びます。

*   `HttpClientModule`: HTTP通信を行うための準備
*   `Service`: データ取得ロジックの置き場所
*   `Component`: UIとロジックの入れ物
*   `Data Binding` と `Directive`: データとHTMLを結びつける魔法

それでは、ステップバイステップで進めていきましょう。作業はすべて`frontend`ディレクトリ内で行います。

---

### **ステップ1: HTTP通信の準備 (`HttpClientModule`のインポート)**

**目的:**
Angularアプリケーション全体でHTTP通信機能を使えるようにします。Angularでは、使いたい機能を「モジュール」としてアプリケーションに登録する必要があります。

**手順:**
`src/app/app.module.ts` ファイルを開き、`HttpClientModule` を `imports` 配列に追加します。

**(ファイルパス: `frontend/src/app/app.module.ts`)**
```typescript
// Angularのコア機能やブラウザで動作させるためのモジュールをインポート
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

// ★ここを追加: HTTP通信を行うためのモジュールをインポート
import { HttpClientModule } from '@angular/common/http';

// ルーティング機能とアプリケーションのルートコンポーネントをインポート
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// @NgModuleデコレータは、このクラスがAngularモジュールであることを示す
// モジュールは、関連するコンポーネント、ディレクティブ、パイプ、サービスをまとめたもの
@NgModule({
  declarations: [
    // このモジュールに所属するコンポーネントを宣言
    AppComponent
  ],
  imports: [
    // このモジュールで利用する他のモジュールをインポート
    BrowserModule,
    AppRoutingModule,
    // ★ここを追加: HttpClientModuleをインポートすることで、
    // アプリケーション全体でHttpClientサービスが利用可能になる（DIできるようになる）
    HttpClientModule
  ],
  providers: [
    // このモジュールで利用するサービスを登録する場所（現在は不要）
  ],
  bootstrap: [
    // アプリケーション起動時に最初に表示するコンポーネントを指定
    AppComponent
  ]
})
export class AppModule { }
```

**学習ポイント:**
*   **`@NgModule` とは？**
    Angularアプリケーションの構成要素を整理するための「箱」のようなものです。コンポーネントやサービスなど、関連する部品を一つのグループにまとめます。`AppModule`はアプリケーションの根幹となるルートモジュールです。
*   **`imports` 配列の役割:**
    このモジュールが機能するために必要な「他のモジュール」をリストアップします。ここに `HttpClientModule` を加えることで、AngularのDI（Dependency Injection）システムが `HttpClient` というサービスを認識し、必要な場所で使えるように準備してくれます。

---

### **ステップ2: データモデルの定義 (Interface)**

**目的:**
APIから受け取るデータの「型」を定義します。これにより、TypeScriptの型チェック機能が働き、コードの安全性と可読性が向上します。

**手順:**
1.  `frontend/src/app` の中に `models` という新しいフォルダを作成します。
2.  `models` フォルダの中に `item.model.ts` という新しいファイルを作成します。
3.  作成したファイルに、`Item`インターフェースを定義します。

**(ファイルパス: `frontend/src/app/models/item.model.ts`)**
```typescript
// 'interface' はオブジェクトの構造（プロパティとその型）を定義するためのものです。
// これにより、Item型のオブジェクトは必ず id, name, completed を持つことが保証されます。
export interface Item {
  id: number;
  name: string;
  completed: boolean;
}
```

**学習ポイント:**
*   **`interface` とは？**
    TypeScriptの機能で、オブジェクトの「設計図」や「契約」のようなものです。`Item`型の変数は、必ず`id`（数値）、`name`（文字列）、`completed`（真偽値）のプロパティを持つことを強制できます。これにより、`item.naem` のようなタイポをコンパイル時に発見できたり、エディタがプロパティ名を補完してくれたりするメリットがあります。

---

### **ステップ3: データ取得ロジックの作成 (Service)**

**目的:**
APIとの通信ロジックをコンポーネントから分離し、再利用可能でテストしやすい「サービス」として実装します。

**手順:**
1.  `frontend/src/app` の中に `services` という新しいフォルダを作成します。
2.  `services` フォルダの中に `api.service.ts` という新しいファイルを作成します。
3.  作成したファイルに、API通信を行うサービスを実装します。

**(ファイルパス: `frontend/src/app/services/api.service.ts`)**
```typescript
// Injectableデコレータは、このクラスがDI（依存性の注入）システムによって
// 他のクラスに注入される「サービス」であることを示す。
import { Injectable } from '@angular/core';
// HTTP通信を行うためのHttpClientと、非同期データを扱うためのObservableをインポート
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// ステップ2で作成したItemインターフェースをインポート
import { Item } from '../models/item.model';

// { providedIn: 'root' } は、このサービスがアプリケーションのルートレベルで提供されることを意味する。
// これにより、アプリケーション全体でこのサービスの単一のインスタンス（シングルトン）が共有され、
// どこからでも同じサービスを利用できる。
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // バックエンドAPIのベースURLを定義
  // proxy.conf.jsonで設定したパスに合わせる
  private apiUrl = '/api/items';

  // コンストラクタでHttpClientを「注入」してもらう。
  // これがDependency Injection（依存性の注入）。
  // 自分で new HttpClient() する必要はない。
  constructor(private http: HttpClient) { }

  // Itemの配列をObservableとして返すメソッドを定義。
  // Observableは、非同期に届くデータの「ストリーム（流れ）」を表すオブジェクト。
  getItems(): Observable<Item[]> {
    // http.get<Item[]> は、GETリクエストを送信し、
    // レスポンスのJSONボディをItemの配列として解釈することを期待する。
    // このメソッドはHTTPレスポンスを待たずに、すぐにObservableを返す。
    // 実際のデータは後からストリームに乗って流れてくる。
    return this.http.get<Item[]>(this.apiUrl);
  }
}
```

**学習ポイント:**
*   **`Service` とは？**
    コンポーネントに依存しない共通のロジック（API通信、データ処理、ログ出力など）をまとめるためのクラスです。ロジックをサービスに分離することで、コンポーネントはUIの表示に専念でき、コードの見通しが良くなります。
*   **`@Injectable({ providedIn: 'root' })`:**
    この記述により、`ApiService`はアプリケーション起動時に自動的にインスタンス化され、どのコンポーネントからでも「ください」と言えば（DIすれば）使えるようになります。
*   **`Dependency Injection (DI)`:**
    `constructor(private http: HttpClient)` の部分がDIの核心です。`ApiService`クラスは、「私は`HttpClient`が必要です」と宣言しているだけで、`HttpClient`のインスタンスを自分で作りません。Angularフレームワークがこの宣言を読み取り、事前に用意していた`HttpClient`のインスタンスをコンストラクタの引数として渡してくれます。これにより、クラス間の依存関係が疎になり、テストが容易になります。
*   **`Observable`:**
    RxJSライブラリが提供する、非同期処理の主役です。HTTPリクエストは結果が返ってくるまでに時間がかかります。`Observable`は「未来に届くであろうデータ」の受信予約券のようなものです。後述する`subscribe()`メソッドで、データが届いたときの処理を予約します。

---

### **ステップ4: データを表示するコンポーネントの修正**

**目的:**
アプリケーションのメインコンポーネントである `AppComponent` で、作成した `ApiService` を利用してデータを取得し、プロパティに保持します。

**手順:**
`src/app/app.component.ts` を以下のように修正します。

**(ファイルパス: `frontend/src/app/app.component.ts`)**
```typescript
// Componentデコレータ、OnInitライフサイクルフックをインポート
import { Component, OnInit } from '@angular/core';
// 作成したサービスとモデルをインポート
import { ApiService } from './services/api.service';
import { Item } from './models/item.model';

@Component({
  selector: 'app-root', // このコンポーネントをHTMLで使う際のタグ名 (<app-root></app-root>)
  templateUrl: './app.component.html', // このコンポーネントのHTMLテンプレートのパス
  styleUrls: ['./app.component.scss'] // このコンポーネント専用のスタイルのパス
})
// OnInitインターフェースを実装することで、ngOnInitメソッドを持つことを保証する
export class AppComponent implements OnInit {
  // HTMLテンプレートから参照されるプロパティ
  title = 'Angular 学習用アプリ';

  // APIから取得したItemの配列を格納するプロパティ。初期値は空の配列。
  // `Item[]` と型付けすることで、この配列にはItem型のオブジェクトしか入れられない。
  items: Item[] = [];

  // コンストラクタでApiServiceをDI（依存性の注入）する。
  // これで、このクラス内で `this.apiService` としてApiServiceの機能が使えるようになる。
  constructor(private apiService: ApiService) {}

  // ngOnInitは、コンポーネントのライフサイクルの一環で、
  // プロパティの初期化が終わった直後に一度だけ呼び出される。
  // APIからのデータ取得など、初期化処理に最適な場所。
  ngOnInit(): void {
    // サービスのgetItems()メソッドを呼び出す。これはObservableを返す。
    this.apiService.getItems()
      // .subscribe()メソッドで、Observableを「購読」する。
      // これにより、データが非同期に届いたタイミングで、中の処理が実行される。
      .subscribe((data: Item[]) => {
        // APIから受け取ったデータ（Itemの配列）を、コンポーネントのitemsプロパティに代入する。
        // これにより、HTMLテンプレート側でこのデータを参照できるようになる。
        this.items = data;
        console.log('データ取得成功:', this.items);
      });
  }
}
```

**学習ポイント:**
*   **`Component` ライフサイクルフック:**
    Angularコンポーネントには、作成されてから破棄されるまでの一連のライフサイクル（一生）があります。`ngOnInit`は「誕生直後」に呼ばれるメソッドで、初期化処理に最適です。他にも`ngOnChanges`（`@Input`プロパティが変更されたとき）や`ngOnDestroy`（破棄される直前）などがあります。
*   **`subscribe()`:**
    `Observable`（データの流れ）を購読し、データが流れてきたときに何をするかを定義します。`getItems()`が返した`Observable`を`subscribe()`することで、HTTPレスポンスが返ってきた瞬間に、引数で渡したコールバック関数 `(data) => { ... }` が実行されます。

---

### **ステップ5: HTMLテンプレートでのデータ表示**

**目的:**
コンポーネントが保持している `items` 配列のデータを、HTMLテンプレートを使って画面に表示します。ここではAngularの強力なテンプレート構文を使います。

**手順:**
`src/app/app.component.html` の中身を全て削除し、以下のように書き換えます。

**(ファイルパス: `frontend/src/app/app.component.html`)**
```html
<main class="content">
  <!-- 1. Interpolation (補間): {{ }} -->
  <!-- AppComponentクラスの`title`プロパティの値をここに表示する -->
  <h1>{{ title }}</h1>

  <div class="card">
    <h2>学習項目リスト</h2>
    <ul>
      <!-- 2. 構造ディレクティブ: *ngFor -->
      <!-- AppComponentクラスの`items`配列をループ処理する。 -->
      <!-- 配列の各要素が`item`という名前の変数に代入され、li要素が配列の数だけ繰り返される。 -->
      <!-- `trackBy`はパフォーマンス最適化のテクニック。配列が更新された際に、Angularが各要素を効率的に識別できるようにする。 -->
      <li *ngFor="let item of items; trackBy: trackById">

        <!-- 3. Property Binding (プロパティバインディング): [ ] -->
        <!-- `item.completed`がtrueの場合、このspan要素に`completed`というCSSクラスを追加する。 -->
        <!-- これにより、完了済みの項目にスタイルを適用できる。 -->
        <span [class.completed]="item.completed">
          {{ item.name }}
        </span>

        <!-- 4. 構造ディレクティブ: *ngIf -->
        <!-- `item.completed`がtrueの場合にのみ、このspan要素を表示する。 -->
        <span *ngIf="item.completed" class="status-badge completed-badge">
          完了
        </span>

        <!-- *ngIfのelse構文 -->
        <!-- `item.completed`がfalseの場合にのみ、`pending`テンプレート（下で定義）を表示する。 -->
        <span *ngIf="!item.completed" class="status-badge pending-badge">
          未完了
        </span>
      </li>
    </ul>

    <!-- *ngIfで、items配列が空の場合に表示するメッセージ -->
    <p *ngIf="items.length === 0">
      読み込み中、またはデータがありません...
    </p>
  </div>
</main>
```

**`app.component.ts` に `trackBy` 用のメソッドを追加:**
`*ngFor`のパフォーマンスを最適化するために、`app.component.ts`に以下のメソッドを追加します。

**(ファイルパス: `frontend/src/app/app.component.ts`)**
```typescript
// ... (既存のコードはそのまま)

export class AppComponent implements OnInit {
  // ... (既存のプロパティとコンストラクタはそのまま)

  ngOnInit(): void {
    // ... (既存のngOnInitの中身はそのまま)
  }

  // ★ここを追加: *ngForのtrackByで使用するメソッド
  // これにより、リストが再描画される際に、AngularはIDが変わらない要素はDOMを再利用し、
  // パフォーマンスが向上する。
  trackById(index: number, item: Item): number {
    return item.id;
  }
}
```

**学習ポイント:**
*   **データバインディング:**
    *   **`{{ }}` (Interpolation/補間):** コンポーネントのプロパティ値を文字列としてHTMLに埋め込みます。最もシンプルな一方向バインディングです。
    *   **`[ ]` (Property Binding/プロパティバインディング):** HTML要素のプロパティ（`class`, `id`, `src`など）に、コンポーネントのプロパティ値をバインドします。
*   **ディレクティブ:**
    *   **`*ngFor`:** 配列を繰り返し処理し、HTML要素を生成します。DOM構造を変化させるため「構造ディレクティブ」と呼ばれます。
    *   **`*ngIf`:** 条件に基づいてHTML要素を表示または非表示にします。これも「構造ディレクティブ」です。`*`が付くのは、これが1つの要素を複数の要素に展開するテンプレートの糖衣構文（シンタックスシュガー）であることを示しています。

---

### **ステップ6: スタイルの適用**

**目的:**
表示されたリストに簡単なスタイルを適用して、見栄えを良くします。特に、完了済みの項目が視覚的に分かるようにします。

**手順:**
`src/app/app.component.scss` の中身を全て削除し、以下のように書き換えます。

**(ファイルパス: `frontend/src/app/app.component.scss`)**
```scss
// このファイルに書かれたスタイルは、デフォルトではこのAppComponent内にのみ適用される（コンポーネントスコープ）

.content {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: sans-serif;
}

.card {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  h2 {
    margin-top: 0;
  }
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;

  &:last-child {
    border-bottom: none;
  }
}

// プロパティバインディング [class.completed]="..." で true になった場合に適用されるスタイル
.completed {
  text-decoration: line-through;
  color: #888;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.completed-badge {
  background-color: #4caf50; // 緑
}

.pending-badge {
  background-color: #ff9800; // オレンジ
}
```

**学習ポイント:**
*   **コンポーネントスコープのスタイル:**
    Angular CLIでプロジェクトを作成すると、コンポーネントのスタイルはデフォルトで「カプセル化」されます。つまり、`app.component.scss`に書いたスタイルは`AppComponent`のテンプレートにのみ適用され、他のコンポーネントやアプリケーション全体に影響を与えません。これにより、スタイルの衝突を心配することなく開発を進められます。

---

### **ステップ7: 実行と確認**

全てのファイルの編集が終わりました。 अब、動作を確認しましょう。

1.  **バックエンドサーバーの起動:**
    VSCodeのターミナルで `backend` ディレクトリに移動し、`npm start` が実行されていることを確認します。（まだなら実行してください）
2.  **フロントエンド開発サーバーの起動:**
    別のターミナルで `frontend` ディレクトリに移動し、`ng serve` を実行します。
3.  **ブラウザで確認:**
    コンパイルが完了したら、ブラウザで `http://localhost:4200` を開きます。

**期待される表示:**

以下のように、APIから取得したデータがスタイル付きで表示されていれば成功です！

*   「学習項目1」には取り消し線が引かれ、「完了」バッジが表示されます。
*   「学習項目2」「学習項目3」は通常の文字で、「未完了」バッジが表示されます。
*   ブラウザの開発者ツール（F12）のコンソールに `データ取得成功:` のログが表示されていることも確認しましょう。



### **まとめ**

この演習を通して、あなたはAngularアプリケーション開発の基本的な流れを完全に体験しました。

*   **`AppModule`** で **`HttpClientModule`** をインポートし、HTTP通信の準備をした。
*   再利用可能な **`ApiService`** を作成し、**DI** を使って **`HttpClient`** を注入し、APIからデータを取得するロジックを実装した。
*   **`AppComponent`** で **`ApiService`** をDIし、**`ngOnInit`** ライフサイクルフックでデータを取得し、プロパティに格納した。
*   HTMLテンプレートで **`*ngFor`** や **`*ngIf`** といったディレクティブと、**`{{ }}`** や **`[ ]`** といったデータバインディング構文を駆使して、動的に画面を構築した。

これらの知識は、今後のより複雑なアプリケーションを作成していく上での強固な土台となります。お疲れ様でした！