承知いたしました。
学習ロードマップ No.2「親子コンポーネントカウンター」について、No.1 と同様に、具体的なコードと解説を交えながらステップバイステップで進めていきましょう。

このチュートリアルでは、Angular における最も重要な概念の一つである**コンポーネント間の連携**を学びます。具体的には、親コンポーネントが状態（カウンターの値）を管理し、子コンポーネントが UI（操作ボタン）を担当するという役割分担を実装します。

---

### 学習目標

- **コンポーネントの分割:** なぜコンポーネントを分ける必要があるのかを理解する。
- **`@Input()`:** 親コンポーネントから子コンポーネントへデータを渡す方法を習得する。
- **`@Output()` と `EventEmitter`:** 子コンポーネントから親コンポーネントへイベント（ユーザーの操作など）を通知する方法を習得する。

---

### Step 1: 準備と既存コードの整理

まず、前回作成したプロジェクトを、今回の学習用に整理します。

1.  **VSCode で DevContainer を開く:**
    `angular-learning-space` フォルダを VSCode で開き、DevContainer に接続します。

2.  **ターミナルを開き、開発サーバーを起動:**
    VSCode 内で新しいターミナルを開き、`frontend` ディレクトリに移動して Angular の開発サーバーを起動しておきましょう。コードを変更すると、ブラウザが自動的にリロードされます。

    ```bash
    cd frontend
    ng serve
    ```

3.  **`app.component.ts` のクリーンアップ:**
    API 通信のロジックは今回不要なので、シンプルにします。

    **(ファイルパス: `frontend/src/app/app.component.ts`)**

    ```typescript
    // AppComponentはアプリケーションのルート（最上位）コンポーネントです。
    import { Component } from "@angular/core";

    @Component({
      selector: "app-root",
      templateUrl: "./app.component.html",
      styleUrls: ["./app.component.scss"],
    })
    export class AppComponent {
      // コンポーネントのタイトルをプロパティとして定義します。
      // この値はテンプレート（HTML）側で {{ title }} のようにして表示できます。
      title = "親子コンポーネントカウンター";
    }
    ```

4.  **`app.component.html` のクリーンアップ:**
    こちらも初期状態に近い、シンプルな表示に戻します。

    **(ファイルパス: `frontend/src/app/app.component.html`)**

    ```html
    <!-- 全体を囲むコンテナ -->
    <div class="container">
      <!-- {{ title }} は、app.component.tsで定義したtitleプロパティの値を表示します（データバインディング） -->
      <h1>{{ title }}</h1>
    </div>

    <!-- Angular Routerが、URLに応じて表示するコンポーネントをここに描画します。今回は使いませんが、残しておきます。 -->
    <router-outlet></router-outlet>
    ```

5.  **`app.module.ts` のクリーンアップ:**
    `HttpClientModule`は今回使わないので、`imports`配列から削除します。

    **(ファイルパス: `frontend/src/app/app.module.ts`)**

    ```typescript
    import { NgModule } from "@angular/core";
    import { BrowserModule } from "@angular/platform-browser";

    import { AppRoutingModule } from "./app-routing.module";
    import { AppComponent } from "./app.component";
    // HttpClientModuleは不要なので削除しました

    @NgModule({
      declarations: [AppComponent],
      imports: [
        BrowserModule,
        AppRoutingModule,
        // HttpClientModuleは不要なので削除しました
      ],
      providers: [],
      bootstrap: [AppComponent],
    })
    export class AppModule {}
    ```

    この時点でブラウザ（`http://localhost:4200`）には「親子コンポーネントカウンター」というタイトルだけが表示されているはずです。

---

### Step 2: 子コンポーネントの作成 (CounterButtonComponent)

次に、カウンターの操作ボタンとなる**子コンポーネント**を作成します。このコンポーネントは再利用可能な部品として設計します。

1.  **新しいターミナルを開く:**
    `ng serve`を実行しているターミナルはそのままにして、新しいターミナルを開きます (`Ctrl+Shift+5` or `Cmd+Shift+5`)。

2.  **Angular CLI でコンポーネントを生成:**
    `frontend`ディレクトリにいることを確認し、以下のコマンドを実行します。

    ```bash
    ng generate component components/counter-button
    # 短縮形: ng g c components/counter-button
    ```

    これにより、`src/app/components/counter-button` ディレクトリと、その中に 4 つのファイル (`.ts`, `.html`, `.scss`, `.spec.ts`) が生成されます。また、`app.module.ts` にも自動的にこのコンポーネントが登録されます。

3.  **`counter-button.component.ts` の編集（@Input と @Output の実装）:**
    ここが今回のハイライトです。親からデータを受け取る`@Input`と、親にイベントを通知する`@Output`を定義します。

    **(ファイルパス: `frontend/src/app/components/counter-button/counter-button.component.ts`)**

    ```typescript
    // Component, Input, Output, EventEmitterを@angular/coreからインポートします
    import { Component, Input, Output, EventEmitter } from "@angular/core";

    @Component({
      selector: "app-counter-button",
      templateUrl: "./counter-button.component.html",
      styleUrls: ["./counter-button.component.scss"],
    })
    export class CounterButtonComponent {
      // --- 親から子へのデータ伝達 (Input) ---
      // @Input()デコレータを付けることで、このプロパティが親コンポーネントから値を受け取れるようになります。
      // このコンポーネントを使う側（親）が <app-counter-button [label]="'増やす'"></app-counter-button> のように値を設定します。
      @Input() label: string = ""; // ボタンに表示するテキスト

      // このボタンがカウンターをどれだけ増減させるかを親から受け取ります。
      @Input() amount: number = 1;

      // --- 子から親へのイベント通知 (Output) ---
      // @Output()デコレータとEventEmitterを使って、親にイベントを通知する仕組みを定義します。
      // EventEmitter<number> の <number> は、親に渡すデータの型を指定しています（今回は増減量を渡すのでnumber）。
      // このコンポーネントを使う側（親）が <app-counter-button (changeValue)="親のメソッド($event)"></app-counter-button> のようにイベントを購読します。
      @Output() changeValue = new EventEmitter<number>();

      // ボタンがクリックされたときに呼び出されるメソッド
      onClick(): void {
        // changeValueイベントを発火(emit)させます。
        // emit()の引数に渡した値(this.amount)が、親コンポーネントのイベントハンドラで $event として受け取れます。
        this.changeValue.emit(this.amount);
      }
    }
    ```

4.  **`counter-button.component.html` の編集:**
    コンポーネントの見た目（ボタン）を定義します。

    **(ファイルパス: `frontend/src/app/components/counter-button/counter-button.component.html`)**

    ```html
    <!--
      (click)="onClick()" はイベントバインディングです。
      このボタンがクリックされたときに、counter-button.component.tsで定義したonClick()メソッドが呼び出されます。
    -->
    <button (click)="onClick()">
      <!--
        {{ label }} はプロパティバインディング（補間）です。
        counter-button.component.tsのlabelプロパティの値をここに表示します。
        このlabelの値は、親コンポーネントから@Inputを通じて渡されます。
      -->
      {{ label }}
    </button>
    ```

---

### Step 3: 親コンポーネントの実装 (AppComponent)

次に、作成した子コンポーネントを利用する**親コンポーネント**を実装します。

1.  **`app.component.ts` の編集（状態とロジックの追加）:**
    カウンターの現在の値を保持するプロパティと、その値を更新するメソッドを追加します。

    **(ファイルパス: `frontend/src/app/app.component.ts`)**

    ```typescript
    import { Component } from "@angular/core";

    @Component({
      selector: "app-root",
      templateUrl: "./app.component.html",
      styleUrls: ["./app.component.scss"],
    })
    export class AppComponent {
      title = "親子コンポーネントカウンター";

      // 親コンポーネントがアプリケーションの状態（カウンターの現在値）を管理します。
      // この値が、画面に表示される数値となります。
      currentCount: number = 0;

      // 子コンポーネント（CounterButtonComponent）からイベントが通知されたときに呼び出されるメソッドです。
      // 引数 amount には、子コンポーネントが emit() で渡した値が入ってきます。
      updateCount(amount: number): void {
        this.currentCount += amount;
      }

      // カウンターを0にリセットするメソッド
      resetCount(): void {
        this.currentCount = 0;
      }
    }
    ```

2.  **`app.component.html` の編集（子コンポーネントの利用）:**
    作成した子コンポーネントをテンプレート内で呼び出し、`@Input`と`@Output`を設定します。

    **(ファイルパス: `frontend/src/app/app.component.html`)**

    ```html
    <div class="container">
      <h1>{{ title }}</h1>

      <!-- カウンターの現在値を表示するエリア -->
      <div class="counter-display">{{ currentCount }}</div>

      <!-- 子コンポーネントを配置するエリア -->
      <div class="controls">
        <!--
          これが子コンポーネント <app-counter-button> の利用例です。
          [label]と[amount]はプロパティバインディング（親→子へのデータ渡し, @Input）。
          (changeValue)はイベントバインディング（子→親へのイベント通知, @Output）。
        -->

        <!-- 「+1」ボタン -->
        <app-counter-button
          [label]="'+1'"
          [amount]="1"
          (changeValue)="updateCount($event)"
        >
        </app-counter-button>

        <!-- 「+5」ボタン -->
        <app-counter-button
          [label]="'+5'"
          [amount]="5"
          (changeValue)="updateCount($event)"
        >
        </app-counter-button>

        <!-- 「-1」ボタン -->
        <app-counter-button
          [label]="'-1'"
          [amount]="-1"
          (changeValue)="updateCount($event)"
        >
        </app-counter-button>

        <!-- 「-5」ボタン -->
        <app-counter-button
          [label]="'-5'"
          [amount]="-5"
          (changeValue)="updateCount($event)"
        >
        </app-counter-button>
      </div>

      <!-- リセットボタン -->
      <div class="reset-area">
        <!-- このボタンは親コンポーネントに直接属しており、クリックで親のresetCount()メソッドを呼び出します -->
        <button (click)="resetCount()">リセット</button>
      </div>
    </div>

    <router-outlet></router-outlet>
    ```

    **解説:**

    - `<app-counter-button ...>`: 子コンポーネントのセレクタを使って呼び出しています。
    - `[label]="'+1'"`: `AppComponent`から`CounterButtonComponent`の`label`プロパティ（`@Input`）へ文字列`'+1'`を渡しています。
    - `[amount]="1"`: `AppComponent`から`CounterButtonComponent`の`amount`プロパティ（`@Input`）へ数値`1`を渡しています。
    - `(changeValue)="updateCount($event)"`: `CounterButtonComponent`が`changeValue`イベントを発火（`emit`）させると、`AppComponent`の`updateCount()`メソッドが呼び出されます。`$event`には`emit()`で渡された値（この場合は`amount`の値）が入ります。

---

### Step 4: スタイリング

最後に、見た目を少し整えて完成です。

1.  **`app.component.scss` の編集:**
    親コンポーネントのスタイルを定義します。

    **(ファイルパス: `frontend/src/app/app.component.scss`)**

    ```scss
    // :host は、このコンポーネント自身（<app-root>）を指すセレクタです。
    // コンポーネントのスタイルは、デフォルトではそのコンポーネント内にしか適用されません（View Encapsulation）。
    :host {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      font-family: sans-serif;
      background-color: #f0f2f5;
    }

    .container {
      background: white;
      padding: 2rem 3rem;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      text-align: center;
      width: 400px;
    }

    .counter-display {
      font-size: 5rem;
      font-weight: bold;
      margin: 1rem 0;
      padding: 1rem;
      background-color: #e9ecef;
      border-radius: 4px;
      color: #343a40;
    }

    .controls {
      display: flex;
      justify-content: center;
      gap: 0.5rem; // ボタン間の隙間
      margin-bottom: 1.5rem;
    }

    .reset-area button {
      background-color: #dc3545;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;

      &:hover {
        background-color: #c82333;
      }
    }
    ```

2.  **`counter-button.component.scss` の編集:**
    子コンポーネント（ボタン）のスタイルを定義します。

    **(ファイルパス: `frontend/src/app/components/counter-button/counter-button.component.scss`)**

    ```scss
    button {
      padding: 0.5rem 1rem;
      font-size: 1rem;
      font-weight: bold;
      border-radius: 4px;
      border: 1px solid #007bff;
      background-color: #007bff;
      color: white;
      cursor: pointer;
      min-width: 60px;
      transition: background-color 0.2s, transform 0.1s;

      // ホバーしたときのスタイル
      &:hover {
        background-color: #0056b3;
      }

      // クリックした（アクティブな）ときのスタイル
      &:active {
        transform: scale(0.95);
      }
    }
    ```

---

### Step 5: 動作確認

`ng serve`が実行中であれば、ブラウザ (`http://localhost:4200`) は自動的に更新されているはずです。
表示された画面で、以下の動作を確認してください。

1.  「+1」「+5」ボタンを押すと、中央の数字がそれぞれ 1, 5 ずつ増えること。
2.  「-1」「-5」ボタンを押すと、中央の数字がそれぞれ 1, 5 ずつ減ること。
3.  「リセット」ボタンを押すと、数字が 0 に戻ること。

これらの動作が確認できれば成功です！

### まとめと学習のポイントレビュー

今回の実装を通して、Angular のコンポーネント設計の基本を学びました。

- **コンポーネントの分割と責任の分離**

  - **親 (AppComponent):** アプリケーションの状態（`currentCount`）を保持し、ビジネスロジック（`updateCount`）を持つ **「スマートコンポーネント」** としての役割を果たしました。
  - **子 (CounterButtonComponent):** 自身の状態を持たず、親から渡されたデータを表示し、ユーザー操作を親に通知するだけの **「プレゼンテーション（ダム）コンポーネント」** としての役割を果たしました。
  - **メリット:** このように役割を分けることで、`CounterButtonComponent`は他の場所でも再利用しやすくなり、`AppComponent`は状態管理に集中できます。コードが整理され、テストやメンテナンスが格段にしやすくなります。

- **`@Input()` による親から子へのデータフロー**

  - 親テンプレートの**プロパティバインディング `[ ]`** を通じて、子の `@Input()` プロパティにデータが流れ込みます。これは **一方通行** のデータフローです。
  - `[label]="'+1'"` や `[amount]="1"` のように、再利用可能なコンポーネントの振る舞いを外から制御できました。

- **`@Output()` と `EventEmitter` による子から親へのイベント通知**
  - 親テンプレートの**イベントバインディング `( )`** を通じて、子の `@Output()` から発火されたイベントを受け取ります。
  - `(changeValue)="updateCount($event)"` のように、子の内部で起こった出来事（ボタンクリック）を親が知るための仕組みを構築しました。`$event` を使って子から親へデータを渡せるのがポイントです。

この「`@Input`で下に流し、`@Output`で上に戻す」というパターンは、Angular アプリケーションを構築する上で最も基本的かつ重要なテクニックです。これをマスターすることで、複雑な UI も綺麗に整理されたコンポーネントツリーとして構築できるようになります。
