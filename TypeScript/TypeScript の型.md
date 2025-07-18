### はじめに：なぜTypeScriptの「型」が重要なのか？

TypeScriptは、JavaScriptに「静的な型」という概念を導入した、JavaScriptのスーパーセット（上位互換）です。なぜわざわざ型を付けるのでしょうか？

*   **バグの早期発見**: 「数値を入れるはずの場所に文字列が入っていた」といった単純なミスを、コードを実行する前（コンパイル時）に発見できます。これは開発の生産性を劇的に向上させます。
*   **コードの可読性と保守性**: 型定義は、その変数や関数が「何を期待しているか」という仕様をコード自体で表現します。これにより、他の人（あるいは未来の自分）がコードを読んだときに、意図を理解しやすくなります。
*   **エディタの強力なサポート**: VSCodeなどのエディタはTypeScriptの型情報を解析し、非常に賢い自動補完（インテリセンス）、エラーチェック、リファクタリング機能を提供してくれます。これはもはや「魔法」のレベルです。

このチートシートでは、基本的な型からTypeScript独自の高度な型までを、段階的に解説していきます。

---

### Part 1: 基本の型 (Primitive Types)

これらは、JavaScriptにも存在する最も基本的なデータ型です。すべての型の基礎となります。

| 型           | 説明                     | サンプルコード                                          |
| :---------- | :--------------------- | :----------------------------------------------- |
| `string`    | 文字列                    | `let name: string = "Alice";`                    |
| `number`    | 数値（整数・浮動小数点数）          | `let age: number = 30;`                          |
| `boolean`   | 真偽値（true/false）        | `let isLoggedIn: boolean = true;`                |
| `null`      | null値（「何もない」ことを意図的に示す） | `let data: null = null;`                         |
| `undefined` | 未定義（値がまだ代入されていない）      | `let notAssigned: undefined = undefined;`        |
| `symbol`    | 一意で不変な値                | `const key: symbol = Symbol("id");`              |
| `bigint`    | 巨大な整数                  | `const largeNumber: bigint = 9007199254740991n;` |

**【背景と知識】**

*   **静的型付け vs 動的型付け**: JavaScriptは動的型付け言語で、変数の型は実行時に決まります。TypeScriptは静的型付け言語で、変数の型はコードを書いた時点で決まります。これが最大の違いです。
    ```typescript
    // TypeScript (Error!)
    let myNumber: number = 10;
    myNumber = "hello"; // Error: Type 'string' is not assignable to type 'number'.

    // JavaScript (OK)
    let myNumberJS = 10;
    myNumberJS = "hello"; // 実行時に型が number から string に変わる
    ```
*   **`null` と `undefined` の違い**:
    *   `undefined`: 変数を宣言したが、まだ値が代入されていない状態。システムのデフォルト。
    *   `null`: 開発者が意図的に「値が存在しない」ことを示すために代入する値。
*   **`strictNullChecks`**: TypeScriptの設定 (`tsconfig.json`) で `strictNullChecks` を `true` にすることを強く推奨します。これにより、`null` や `undefined` を意図せず使ってしまうバグ（"Cannot read property '...' of null" のようなエラー）を防ぐことができます。

---

### Part 2: よく使う複合的な型 (Common Complex Types)

基本の型を組み合わせて、より複雑なデータ構造を表現します。

| 型 | 説明 | サンプルコード |
| :--- | :--- | :--- |
| **配列 (Array)** | 同じ型の要素のリスト | `let list: number[] = [1, 2, 3];` <br> `let genericList: Array<string> = ["a", "b"];` |
| **タプル (Tuple)** | 型と要素数が固定された配列 | `let user: [string, number] = ["Bob", 42];` |
| **オブジェクト (Object)** | プリミティブ型以外の値 | `let obj: object = { name: "Taro" };` |
| **関数 (Function)** | 引数と戻り値の型 | `function greet(name: string): void { console.log("Hello, " + name); }` <br> `const add: (a: number, b: number) => number = (a, b) => a + b;` |
| **列挙型 (Enum)** | 特定の定数セットに名前を付ける | `enum Color { Red, Green, Blue }` <br> `let c: Color = Color.Green;` |

**【背景と知識】**

*   **配列 vs タプル**:
    *   **配列 (`string[]`)**: 長さが可変で、すべての要素が同じ型。
    *   **タプル (`[string, number]`)**: 長さが固定で、各要素が異なる型を持つことができる。APIの戻り値など、位置に意味がある場合に便利です。（例: Reactの `useState` フック）
*   **`object` 型の注意点**: `object` 型は「プリミティブ型ではない」という程度の弱い型です。通常は、より具体的にオブジェクトの構造を示す **`interface`** や **`type`** (後述) を使います。
*   **関数の戻り値 `void`**: この関数が「何も返さない」ことを明示します。戻り値を利用しようとするとエラーになります。
*   **Enum の種類**:
    *   **数値Enum**: デフォルトでは `0, 1, 2...` と数値が割り当てられます。
    *   **文字列Enum**: `enum Direction { Up = "UP", Down = "DOWN" }` のように、値に文字列を明示的に指定します。コードの可読性が高まるため、文字列Enumが推奨されることが多いです。

---

### Part 3: TypeScript独自のパワフルな型 (TypeScript's Powerful Types)

ここからがTypeScriptの真骨頂です。コードの柔軟性と安全性を両立させるための強力な機能群です。

| 型                       | 説明                       | サンプルコード                                                                                                                                |                                                         
| :---------------------- | :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| `any`                   | **最終手段**。型チェックを無効化する。    | `let anything: any = 4;` <br> `anything = "hello"; // OK` <br> `anything.doSomething(); // OK (実行時にエラーになる可能性)`                                     |
| `unknown`               | `any` の安全版。利用前に型チェックが必須。 | `let value: unknown = "hello";` <br> `if (typeof value === 'string') { console.log(value.toUpperCase()); }`                                               |
| **Union (`             ｜ `)**                     | OR。複数の型のいずれか。          | `let id: string                                             ｜ number = "123-abc";` <br> `id = 456;` |
| **Intersection (`&`)**  | AND。複数の型をすべて併せ持つ。        | `type Draggable = { drag: () => void; };` <br> `type Resizable = { resize: () => void; };` <br> `type Widget = Draggable & Resizable;` |                                  |
| **Type Alias (`type`)** | 型に別名を付ける。                | `type UserID = string     ｜ number;` <br> `type User = { name: string; age: number; };` |                                       |
| **Interface**           | オブジェクトの「形状」を定義する契約。      | `interface Person { name: string; age: number; }`                                                                                      |                                              |

**【背景と知識】**

*   **`any` vs `unknown`**:
    *   `any`: 「どんな型でもOK」とTypeScriptに嘘をつくようなもの。型安全性が失われるため、既存のJavaScriptコードを移行する際など、限定的な場面でのみ使用します。**できる限り避けるべきです。**
    *   `unknown`: 「型が不明」であることを正直に伝える型。値を使う前に `typeof` や `instanceof` で型を絞り込む（＝型ガード）ことを強制されるため、安全です。**`any` を使いたくなったら、まず `unknown` を検討してください。**
*   **`type` vs `interface`**: これは非常に頻出する質問です。
    *   **共通点**: どちらもオブジェクトの形状を定義できます。
    *   **違い**:
        *   **拡張方法**: `interface` は `extends` で、`type` は `&` で拡張します。
        *   **宣言のマージ**: 同じ名前の `interface` は自動でマージされますが、`type` はできません（エラーになる）。
    *   **使い分けの指針（コミュニティの慣習）**:
        *   **`interface` を使う**: オブジェクトやクラスの「形状（Shape）」を定義する場合。
        *   **`type` を使う**: Union型、Tuple型、プリミティブ型に別名を付けるなど、`interface` で表現できない複雑な型を定義する場合。
    *   迷ったら、まずは **「オブジェクトの定義には `interface`」** と覚えておくと良いでしょう。

---

### Part 4: 型を操作する高度なテクニック (Advanced Type Manipulation)

より柔軟で再利用性の高い型を作るための、応用的なテクニックです。

| 機能 | 説明 | サンプルコード |
| :--- | :--- | :--- |
| **ジェネリクス (`<T>`)** | 型を引数として受け取る。再利用性の高いコンポーネントを作る。 | `function identity<T>(arg: T): T { return arg; }` <br> `let output = identity<string>("myString");` |
| **型アサーション (`as`)**| 開発者が型を断定する。推論を上書き。 | `const myCanvas = document.getElementById("main_canvas") as HTMLCanvasElement;` |
| **リテラル型** | 特定の文字列や数値そのものを型にする。 | `let status: "success" ｜ "error" ｜ "loading";` <br> `status = "success"; // OK` <br> `status = "pending"; // Error!` |
| **型ガード** | `if` 文などで型を絞り込むテクニック。 | `function printId(id: string ｜ number) {` <br> `  if (typeof id === "string") {` <br> `    console.log(id.toUpperCase()); // ここでは id は string 型` <br> `  }` <br> `}` |
| **ユーティリティ型** | 型操作に便利な組み込みの型。 | `interface Todo { title: string; desc: string; }` <br> `type PartialTodo = Partial<Todo>; // すべてのプロパティがオプショナルになる` <br> `type ReadonlyTodo = Readonly<Todo>; // すべてのプロパティが読み取り専用になる` <br> `type PickedTodo = Pick<Todo, 'title'>; // 'title'プロパティだけを抜き出す`|

**【背景と知識】**

*   **ジェネリクスの重要性**: ジェネリクスは、型安全性を保ちつつ、様々な型に対応できる関数やクラスを作るための鍵です。`any` を使ってしまうと型情報が失われますが、ジェネリクスを使えば、入力された型に応じて出力の型も決まります。
*   **型アサーションの注意点**: `as` は「型キャスト」ではありません。実行時のチェックは行われず、コンパイラに「この型であることは私が保証します」と伝えるだけです。間違った型をアサーションすると、実行時エラーの原因になります。本当に必要な場面以外での多用は避けましょう。
*   **リテラル型 + Union型**: この組み合わせは非常に強力です。`"click" | "mouseover" | "keydown"` のように、イベント名や状態など、取りうる値が限られているケースで絶大な効果を発揮し、タイプミスを防ぎます。これは `Enum` の代替としてもよく使われます。
*   **ユーティリティ型**: これらはTypeScriptが提供する「便利な道具箱」です。よくある型変換（「既存の型のプロパティを一部だけ使いたい」「すべてオプショナルにしたい」など）を簡単に行えます。他にも `Omit`, `Record`, `ReturnType` などたくさんあるので、公式ドキュメントで一度眺めてみることをお勧めします。

---

### 今後の学習への道しるべ

このチートシートをマスターしたら、あなたはTypeScriptエンジニアとして大きく成長しているはずです。次のステップとしては、以下のトピックに挑戦してみましょう。

1.  **`tsconfig.json` の探求**: 特に `"strict": true` オプションを有効にすることで、TypeScriptの恩恵を最大限に受けることができます。どのようなチェックが有効になるのかを理解しましょう。
2.  **非同期処理と型**: `Promise<T>` や `async/await` での型付けは、現代的なWeb開発に必須です。
3.  **より高度な型操作**:
    *   **Conditional Types (`T extends U ? X : Y`)**: 条件によって型を切り替える。
    *   **Mapped Types (`[K in keyof T]: ...`)**: 既存の型のキーを元に新しい型を生成する。
4.  **DefinitelyTyped (`@types/...`)**: 型定義ファイルを持たない純粋なJavaScriptライブラリに型を付けるための、巨大なコミュニティプロジェクトです。`npm install @types/lodash` のようにして使います。

