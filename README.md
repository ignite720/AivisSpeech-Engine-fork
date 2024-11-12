
# AivisSpeech Engine

[![Releases](https://img.shields.io/github/v/release/Aivis-Project/AivisSpeech-Engine?label=Release)](https://github.com/Aivis-Project/AivisSpeech-Engine/releases)
[![License: LGPL-3.0](https://img.shields.io/badge/License-LGPL3-blue.svg)](LICENSE)
[![CI: Build](https://github.com/Aivis-Project/AivisSpeech-Engine/actions/workflows/build-engine-package.yml/badge.svg)](https://github.com/Aivis-Project/AivisSpeech-Engine/actions/workflows/build-engine-package.yml)
[![CI: Test](https://github.com/Aivis-Project/AivisSpeech-Engine/actions/workflows/test.yml/badge.svg)](https://github.com/Aivis-Project/AivisSpeech-Engine/actions/workflows/test.yml)

💠 **AivisSpeech Engine:** **AI** **V**oice **I**mitation **S**ystem - Text to **Speech** **Engine**

-----

**AivisSpeech Engine は、[VOICEVOX ENGINE](https://github.com/Aivis-Project/AivisSpeech-Engine) をベースにした、日本語音声合成エンジンです。**  
日本語音声合成ソフトウェアの [AivisSpeech](https://github.com/Aivis-Project/AivisSpeech) に組み込まれており、かんたんに感情豊かな音声を生成できます。

#### [💠 AivisSpeech をダウンロード](https://aivis-project.com/speech/) ／ [💠 AivisSpeech Engine をダウンロード](https://github.com/Aivis-Project/AivisSpeech-Engine/releases)

-----

- [ユーザーの方へ](#ユーザーの方へ)
- [動作環境](#動作環境)
- [サポートされている音声合成モデル](#サポートされている音声合成モデル)
  - [対応モデルアーキテクチャ](#対応モデルアーキテクチャ)
  - [モデルファイルの配置場所](#モデルファイルの配置場所)
- [音声合成 API を使う](#音声合成-api-を使う)
- [VOICEVOX API との互換性について](#voicevox-api-との互換性について)
  - [AivisSpeech Engine におけるスタイル ID](#aivisspeech-engine-におけるスタイル-id)
  - [`AudioQuery` 型の仕様変更](#audioquery-型の仕様変更)
  - [`Mora` 型の仕様変更](#mora-型の仕様変更)
  - [`Preset` 型の仕様変更](#preset-型の仕様変更)
  - [AivisSpeech Engine ではサポートされていない API エンドポイント](#aivisspeech-engine-ではサポートされていない-api-エンドポイント)
  - [AivisSpeech Engine ではサポートされていない API パラメータ](#aivisspeech-engine-ではサポートされていない-api-パラメータ)
- [開発方針](#開発方針)
- [開発環境の構築](#開発環境の構築)
- [開発](#開発)
- [ライセンス](#ライセンス)

## ユーザーの方へ

**AivisSpeech の使い方をお探しの方は、[AivisSpeech 公式サイト](https://aivis-project.com/speech/) をご覧ください。**

このページでは、主に開発者向けの情報を掲載しています。  
以下はユーザーの方向けのドキュメントです。

- **[使い方](public/howtouse.md)**
- **[よくある質問](public/qAndA.md)**
- **[お問い合わせ](public/contact.md)**

## 動作環境

Windows・macOS・Linux 搭載の PC に対応しています。

- **Windows:** Windows 10・Windows 11
- **macOS:** macOS 13 Ventura 以降
- **Linux:** Ubuntu 20.04 以降

> [!TIP]
> デスクトップアプリである AivisSpeech は、Windows と macOS でのみ利用できます。  
> 一方、音声合成 API サーバーである AivisSpeech Engine は、Ubuntu / Debian 系の Linux でも利用できます。

> [!NOTE]
> Intel CPU 搭載 Mac での動作は積極的に検証していません。  
> Intel CPU 搭載 Mac はすでに製造が終了しており、検証環境やビルド環境の用意自体が難しくなってきています。Apple Silicon 搭載 Mac での利用をおすすめいたします。

## サポートされている音声合成モデル

**AivisSpeech Engine は、[AIVMX (**Ai**vis **V**oice **M**odel for ONN**X**)](https://github.com/Aivis-Project/aivmlib#aivmx-file-format-specification) (拡張子 `.aivmx`) フォーマットの音声合成モデルファイルをサポートしています。**

**AIVM** (**Ai**vis **V**oice **M**odel) / **AIVMX** (**Ai**vis **V**oice **M**odel for ONN**X**) は、**学習済みモデル・ハイパーパラメータ・スタイルベクトル・話者メタデータ（名前・概要・ライセンス・アイコン・ボイスサンプル など）を 1 つのファイルにギュッとまとめた、AI 音声合成モデル用オープンファイルフォーマット**です。  

AIVM 仕様や AIVM / AIVMX ファイルについての詳細は、Aivis Project にて策定した **[AIVM 仕様](https://github.com/Aivis-Project/aivmlib#aivm-specification)** をご参照ください。

> [!NOTE]  
> **「AIVM」は、AIVM / AIVMX 両方のフォーマット仕様・メタデータ仕様の総称でもあります。**  
> 具体的には、AIVM ファイルは「AIVM メタデータを追加した Safetensors 形式」、AIVMX ファイルは「AIVM メタデータを追加した ONNX 形式」のモデルファイルです。  
> 「AIVM メタデータ」とは、AIVM 仕様に定義されている、学習済みモデルに紐づく各種メタデータのことをいいます。

> [!IMPORTANT]  
> **AivisSpeech Engine は AIVM 仕様のリファレンス実装でもありますが、敢えて AIVMX ファイルのみをサポートする設計としています。**  
> これにより、PyTorch への依存を排除してインストールサイズを削減し、ONNX Runtime による高速な CPU 推論を実現しています。

> [!TIP]  
> **[AIVM Generator](https://aivm-generator.aivis-project.com/) を使うと、既存の音声合成モデルから AIVM / AIVMX ファイルを生成したり、既存の AIVM / AIVMX ファイルのメタデータを編集したりできます！**

### 対応モデルアーキテクチャ

以下のモデルアーキテクチャの AIVMX ファイルを利用できます。

- `Style-Bert-VITS2`
- `Style-Bert-VITS2 (JP-Extra)`

> [!NOTE]
> AIVM の仕様上は多言語対応の話者を定義できますが、AivisSpeech Engine は VOICEVOX ENGINE と同様に、日本語音声合成のみに対応しています。  
> そのため、英語や中国語に対応した音声合成モデルであっても、日本語以外の音声合成はできません。

### モデルファイルの配置場所

AIVMX ファイルは、OS ごとに以下のフォルダに配置してください。  

- **Windows:** `C:\Users\(ユーザー名)\AppData\Roaming\AivisSpeech-Engine\Models`
- **macOS:** `~/Library/Application Support/AivisSpeech-Engine/Models`
- **Linux:** `~/.local/share/AivisSpeech-Engine/Models`

実際のフォルダパスは、AivisSpeech Engine の起動直後のログに `Models directory:` として表示されます。

> [!TIP]  
> **AivisSpeech 利用時は、AivisSpeech の UI 画面から簡単に音声合成モデルを追加できます！**  
> エンドユーザーの方は、基本的にこちらの方法で音声合成モデルを追加することをおすすめします。

> [!IMPORTANT]
> 開発版 (PyInstaller でビルドされていない状態で実行している場合) の配置フォルダは、`AivisSpeech-Engine` 以下ではなく `AivisSpeech-Engine-Dev` 以下となります。

## 音声合成 API を使う

Bash で以下のワンライナーを実行すると、`audio.wav` に音声合成した WAV ファイルが出力されます。  
詳細な API リクエスト・レスポンスの仕様は、API ドキュメントや [VOICEVOX API との互換性について](#voicevox-api-との互換性について) をご参照ください。

> [!TIP]
> **AivisSpeech Engine の API ドキュメントは、AivisSpeech Engine もしくは AivisSpeech エディタを起動した状態で、http://127.0.0.1:10101/docs にアクセスすると確認できます。**

> [!IMPORTANT]  
> 事前に AivisSpeech Engine が起動していて、かつログに表示される `Models directory:` 以下のディレクトリに、スタイル ID に対応する音声合成モデル (.aivmx) が格納されていることが前提です。

```bash
STYLE_ID=(音声合成対象のスタイル ID 、別途 /speakers API から取得が必要) && \
echo -n "こんにちは、音声合成の世界へようこそ！" > text.txt && \
curl -s -X POST "127.0.0.1:10101/audio_query?speaker=$STYLE_ID" --get --data-urlencode text@text.txt > query.json && \
curl -s -H "Content-Type: application/json" -X POST -d @query.json "127.0.0.1:10101/synthesis?speaker=$STYLE_ID" > audio.wav && \
rm text.txt query.json
```

## VOICEVOX API との互換性について

AivisSpeech Engine は、概ね VOICEVOX ENGINE の HTTP API と互換性があります。

**VOICEVOX ENGINE の HTTP API に対応したソフトウェアであれば、API URL を `http://127.0.0.1:10101` に差し替えるだけで、AivisSpeech Engine に対応できるはずです。**

> [!IMPORTANT]  
> **ただし、API クライアント側で `/audio_query` API から取得した `AudioQuery` の内容を編集してから `/synthesis` API に渡している場合は、仕様差異により正常に音声合成できない場合があります (後述) 。**
> 
> この関係で、**AivisSpeech エディタは AivisSpeech Engine と VOICEVOX ENGINE の両方を利用できますが（マルチエンジン機能利用時）、VOICEVOX エディタから AivisSpeech Engine を利用することはできません。**  
> VOICEVOX エディタで AivisSpeech Engine を利用すると、エディタの実装上の制限により音声合成の品質が著しく低下します。AivisSpeech Engine 独自のパラメータも活用できなくなるほか、非対応機能の呼び出しでエラーが発生する可能性もあります。  
> より良い音声合成結果を得るため、AivisSpeech エディタでの利用を強くおすすめします。

> [!NOTE]  
> 一般的な API ユースケースにおいては概ね互換性があるはずですが、**根本的に異なるモデルアーキテクチャの音声合成システムを強引に同一の API 仕様に収めている関係で、下記以外にも互換性のない API があるかもしれません。**  
> Issue にて報告頂ければ、互換性改善が可能なものに関しては修正いたします。

VOICEVOX ENGINE からの API 仕様の変更点は次のとおりです。

### AivisSpeech Engine におけるスタイル ID

AIVMX ファイルに含まれる AIVM マニフェスト内の話者スタイルのローカル ID は、話者ごとに 0 から始まる連番で管理されています。  
Style-Bert-VITS2 アーキテクチャの音声合成モデルでは、この値はモデルのハイパーパラメータ `data.style2id` の値と一致します。

一方、VOICEVOX ENGINE の API では、歴史的経緯からか「話者 UUID」(`speaker_uuid`) を指定せず、「スタイル ID」(`style_id`) のみを音声合成 API に渡す仕様となっています。  
VOICEVOX ENGINE では搭載されている話者やスタイルは固定のため、開発側で「スタイル ID」を一意に管理できていました。

一方、AivisSpeech Engine では、ユーザーが自由に音声合成モデルを追加できる仕様となっています。  
そのため、VOICEVOX API 互換の「スタイル ID」は、どのような音声合成モデルが追加されても一意な値である必要があります。  
これは、一意な値でない場合、新しい音声合成モデルを追加した際に既存のモデルに含まれる話者スタイルとスタイル ID が重複してしまう可能性があるためです。

そこで AivisSpeech Engine では、**AIVM マニフェスト上の話者 UUID とスタイル ID を組み合わせて、VOICEVOX API 互換のグローバルに一意な「スタイル ID」を生成しています。**  
具体的な生成方法は以下のとおりです。

1. 話者 UUID を MD5 ハッシュ値に変換する
2. このハッシュ値の下位 27bit とローカルスタイル ID の 5bit (0 ~ 31) を組み合わせる
3. 32bit 符号付き整数に変換する

> [!WARNING]  
> この関係で、**「スタイル ID」に 32bit 符号付き整数が入ることを想定していない VOICEVOX API 対応ソフトウェアでは、予期せぬ不具合が発生する可能性があります。**  

> [!WARNING]  
> 32bit 符号付き整数の範囲に収めるために話者 UUID のグローバルな一意性を犠牲にしているため、**極めて低い確率ですが、異なる話者のスタイル ID が重複（衝突）する可能性があります。**  
> 現時点でスタイル ID が重複した際の回避策はありませんが、現実的にはほとんどのケースで問題にならないと考えられます。

### `AudioQuery` 型の仕様変更

`AudioQuery` 型は、テキストや音素列を指定して音声合成を行うためのクエリです。

変更点の詳細は、[model.py](./voicevox_engine/model.py) を参照してください。

### `Mora` 型の仕様変更

`Mora` 型は、読み上げテキストのモーラを表すデータ構造です。

> [!TIP]  
> モーラとは、実際に発音される際の音のまとまりの最小単位（「あ」「か」「を」など）のことです。  
> `Mora` 型単独で API リクエスト・レスポンスに使われることはなく、常に `AudioQuery.accent_phrases[n].moras` または `AudioQuery.accent_phrases[n].pause_mora` を通して間接的に利用されます。

変更点の詳細は、[tts_pipeline/model.py](./voicevox_engine/tts_pipeline/model.py) を参照してください。

### `Preset` 型の仕様変更

`Preset` 型は、エディタ側で音声合成クエリの初期値を決定するためのプリセット情報です。

変更点の詳細は、[preset/model.py](./voicevox_engine/preset/model.py) を参照してください。

### AivisSpeech Engine ではサポートされていない API エンドポイント

> [!WARNING]  
> **歌声合成系 API と、キャンセル可能な音声合成 API はサポートされていません。**  
> 互換性のためエンドポイントとして存在はしますが、常に `501 Not Implemented` を返します。  
> 詳細は [app/routers/character.py](./voicevox_engine/app/routers/character.py) / [app/routers/tts_pipeline.py](./voicevox_engine/app/routers/tts_pipeline.py) を確認してください。

- **GET `/singers`**
- **GET `/singer_info`**
- **POST `/cancellable_synthesis`**
- **POST `/sing_frame_audio_query`**
- **POST `/sing_frame_volume`**
- **POST `/frame_synthesis`**

> [!WARNING]  
> **モーフィング機能を提供する `/synthesis_morphing` API はサポートされていません。**  
> 話者ごとに発声タイミングが異なる関係で実装不可能なため（動作こそするが聴くに耐えない）、常に `400 Bad Request` を返します。  
> 各話者ごとにモーフィングの利用可否を返す `/morphable_targets` API では、すべての話者でモーフィング禁止扱いとしています。  
> 詳細は [app/routers/morphing.py](./voicevox_engine/app/routers/morphing.py) を確認してください。

- **POST `/synthesis_morphing`**
- **POST `/morphable_targets`**

### AivisSpeech Engine ではサポートされていない API パラメータ

> [!WARNING]  
> **互換性のためパラメータとして存在はしますが、常に無視されます。**  
> 詳細は [app/routers/character.py](./voicevox_engine/app/routers/character.py) / [app/routers/tts_pipeline.py](./voicevox_engine/app/routers/tts_pipeline.py) を確認してください。

- **`core_version` パラメータ**
  - VOICEVOX CORE のバージョンを指定するパラメータです。
  - AivisSpeech Engine では VOICEVOX CORE に対応するコンポーネントがないため、常に無視されます。
- **`enable_interrogative_upspeak` パラメータ**
  - 疑問系のテキストが与えられたら語尾を自動調整するかのパラメータです。
  - AivisSpeech Engine では、常に「！」「？」「…」「〜」などのテキストに含まれる記号に対応した、自然な抑揚で読み上げられます。
  - したがって、`どうですか…？` のように読み上げテキストの末尾に「？」を付与するだけで、疑問系の抑揚で読み上げることができます。

## 開発方針

[VOICEVOX](https://github.com/VOICEVOX) は非常に巨大なソフトウェアであり、現在も活発に開発が続けられています。  
そのため、AivisSpeech Engine では VOICEVOX ENGINE の最新版をベースに、以下の方針で開発を行っています。

- VOICEVOX 最新版への追従を容易にするため、できるだけ改変を必要最小限に留める
  - VOICEVOX ENGINE から AivisSpeech Engine へのリブランディングは必要な箇所のみ行う
  - `voicevox_engine` ディレクトリをリネームすると import 文の変更差分が膨大になるため、あえてリブランディングを行わない
- リファクタリングを行わない
  - VOICEVOX ENGINE とのコンフリクトが発生することが容易に予想される上、コード全体に精通しているわけではないため
- AivisSpeech で利用しない機能 (歌声合成機能など) であっても、コードの削除は行わない
  - これもコンフリクトを回避するため
  - 利用しないコードの無効化は削除ではなく、コメントアウトで行う
    - VOICEVOX ENGINE との差分を最小限に抑えるため、大量にコメントアウトが必要な場合は、# ではなく """ """ を使う
  - ただし、Dockerfile や GitHub Actions などの構成ファイルやビルドツール類はこの限りではない
    - 元々 AivisSpeech Engine での改変量が大きい部分につき、コメントアウトでは非常に雑多なコードになるため
- 保守や追従が困難なため、ドキュメントの更新は行わない
  - このため各ドキュメントは一切更新されておらず、AivisSpeech Engine での変更を反映していない
- AivisSpeech Engine 向けの改変にともないテストコードの維持が困難なため、テストコードの追加は行わない
  - 既存のテストコードのみ、テストが通るように一部箇所の修正やコメントアウトを行い、消極的に維持する
    - AivisSpeech Engine での改変により、テスト結果のスナップショットは VOICEVOX ENGINE と異なる
    - AivisSpeech Engine での改変により動かなくなったテストの修正は行わず、コメントアウトで対応する
  - AivisSpeech Engine 向けに新規開発した箇所は、保守コストを鑑みテストコードを追加しない

## 開発環境の構築

手順はオリジナルの VOICEVOX ENGINE と大幅に異なります。  
事前に Python 3.11 がインストールされている必要があります。

```bash
# Poetry と pre-commit をインストール
pip install poetry poetry-plugin-export pre-commit

# pre-commit を有効化
pre-commit install

# 依存関係をすべてインストール
poetry install
```

## 開発

手順はオリジナルの VOICEVOX ENGINE と大幅に異なります。

```bash
# 開発環境で AivisSpeech Engine を起動
poetry run task serve

# AivisSpeech Engine のヘルプを表示
poetry run task serve --help

# コードフォーマットを自動修正
poetry run task format

# コードフォーマットをチェック
poetry run task lint

# typos によるタイポチェック
poetry run task typos

# テストを実行
poetry run task test

# テストのスナップショットを更新
poetry run task update-snapshots

# ライセンス情報を更新
poetry run task update-licenses

# AivisSpeech Engine をビルド
poetry run task build
```

## ライセンス

ベースである VOICEVOX ENGINE のデュアルライセンスのうち、[LGPL-3.0](LICENSE) のみを単独で継承します。

下記ならびに [docs/](docs/) 以下のドキュメントは、[VOICEVOX ENGINE](https://github.com/VOICEVOX/voicevox_engine) 本家のドキュメントを改変なしでそのまま引き継いでいます。これらのドキュメントの内容が AivisSpeech Engine にも通用するかは保証されません。

-----

# VOICEVOX ENGINE

[![build](https://github.com/VOICEVOX/voicevox_engine/actions/workflows/build-engine-package.yml/badge.svg)](https://github.com/VOICEVOX/voicevox_engine/actions/workflows/build-engine-package.yml)
[![releases](https://img.shields.io/github/v/release/VOICEVOX/voicevox_engine)](https://github.com/VOICEVOX/voicevox_engine/releases)
[![discord](https://img.shields.io/discord/879570910208733277?color=5865f2&label=&logo=discord&logoColor=ffffff)](https://discord.gg/WMwWetrzuh)

[![test](https://github.com/VOICEVOX/voicevox_engine/actions/workflows/test.yml/badge.svg)](https://github.com/VOICEVOX/voicevox_engine/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/VOICEVOX/voicevox_engine/badge.svg)](https://coveralls.io/github/VOICEVOX/voicevox_engine)

[![build-docker](https://github.com/VOICEVOX/voicevox_engine/actions/workflows/build-engine-container.yml/badge.svg)](https://github.com/VOICEVOX/voicevox_engine/actions/workflows/build-engine-container.yml)
[![docker](https://img.shields.io/docker/pulls/voicevox/voicevox_engine)](https://hub.docker.com/r/voicevox/voicevox_engine)

[VOICEVOX](https://voicevox.hiroshiba.jp/) のエンジンです。  
実態は HTTP サーバーなので、リクエストを送信すればテキスト音声合成できます。

（エディターは [VOICEVOX](https://github.com/VOICEVOX/voicevox/) 、
コアは [VOICEVOX CORE](https://github.com/VOICEVOX/voicevox_core/) 、
全体構成は [こちら](https://github.com/VOICEVOX/voicevox/blob/main/docs/%E5%85%A8%E4%BD%93%E6%A7%8B%E6%88%90.md) に詳細があります。）

## 目次

目的に合わせたガイドはこちらです。

- [ユーザーガイド](#ユーザーガイド): 音声合成をしたい方向け
- [貢献者ガイド](#貢献者ガイド): コントリビュートしたい方向け
- [開発者ガイド](#開発者ガイド): コードを利用したい方向け

## ユーザーガイド

### ダウンロード

[こちら](https://github.com/VOICEVOX/voicevox_engine/releases/latest)から対応するエンジンをダウンロードしてください。

### API ドキュメント

[API ドキュメント](https://voicevox.github.io/voicevox_engine/api/)をご参照ください。

VOICEVOX エンジンもしくはエディタを起動した状態で http://127.0.0.1:50021/docs にアクセスすると、起動中のエンジンのドキュメントも確認できます。  
今後の方針などについては [VOICEVOX 音声合成エンジンとの連携](./docs/VOICEVOX音声合成エンジンとの連携.md) も参考になるかもしれません。

### Docker イメージ

#### CPU

```bash
docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
docker run --rm -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```

#### GPU

```bash
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

##### トラブルシューティング

GPU 版を利用する場合、環境によってエラーが発生することがあります。その場合、`--runtime=nvidia`を`docker run`につけて実行すると解決できることがあります。

### HTTP リクエストで音声合成するサンプルコード

```bash
echo -n "こんにちは、音声合成の世界へようこそ" >text.txt

curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query?speaker=1"\
    --get --data-urlencode text@text.txt \
    > query.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=1" \
    > audio.wav
```

生成される音声はサンプリングレートが 24000Hz と少し特殊なため、音声プレーヤーによっては再生できない場合があります。

`speaker` に指定する値は `/speakers` エンドポイントで得られる `style_id` です。互換性のために `speaker` という名前になっています。

### 音声を調整するサンプルコード

`/audio_query` で得られる音声合成用のクエリのパラメータを編集することで、音声を調整できます。

例えば、話速を 1.5 倍速にしてみます。

```bash
echo -n "こんにちは、音声合成の世界へようこそ" >text.txt

curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query?speaker=1" \
    --get --data-urlencode text@text.txt \
    > query.json

# sed を使用して speedScale の値を 1.5 に変更
sed -i -r 's/"speedScale":[0-9.]+/"speedScale":1.5/' query.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=1" \
    > audio_fast.wav
```

### 読み方を AquesTalk 風記法で取得・修正

#### AquesTalk 風記法

<!-- NOTE: この節は静的リンクとして運用中なので変更しない方が良い(voicevox_engine#816) -->

「**AquesTalk 風記法**」はカタカナと記号だけで読み方を指定する記法です。[AquesTalk 本家の記法](https://www.a-quest.com/archive/manual/siyo_onseikigou.pdf)とは一部が異なります。  
AquesTalk 風記法は次のルールに従います：

- 全てのカナはカタカナで記述される
- アクセント句は `/` または `、` で区切る。 `、` で区切った場合に限り無音区間が挿入される。
- カナの手前に `_` を入れるとそのカナは無声化される
- アクセント位置を `'` で指定する。全てのアクセント句にはアクセント位置を 1 つ指定する必要がある。
- アクセント句末に `？` (全角)を入れることにより疑問文の発音ができる

#### AquesTalk 風記法のサンプルコード

`/audio_query`のレスポンスにはエンジンが判断した読み方が[AquesTalk 風記法](#aquestalk-風記法)で記述されます。  
これを修正することで音声の読み仮名やアクセントを制御できます。

```bash
# 読ませたい文章をutf-8でtext.txtに書き出す
echo -n "ディープラーニングは万能薬ではありません" >text.txt

curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query?speaker=1" \
    --get --data-urlencode text@text.txt \
    > query.json

cat query.json | grep -o -E "\"kana\":\".*\""
# 結果... "kana":"ディ'イプ/ラ'アニングワ/バンノオヤクデワアリマセ'ン"

# "ディイプラ'アニングワ/バンノ'オヤクデワ/アリマセ'ン"と読ませたいので、
# is_kana=trueをつけてイントネーションを取得しnewphrases.jsonに保存
echo -n "ディイプラ'アニングワ/バンノ'オヤクデワ/アリマセ'ン" > kana.txt
curl -s \
    -X POST \
    "127.0.0.1:50021/accent_phrases?speaker=1&is_kana=true" \
    --get --data-urlencode text@kana.txt \
    > newphrases.json

# query.jsonの"accent_phrases"の内容をnewphrases.jsonの内容に置き換える
cat query.json | sed -e "s/\[{.*}\]/$(cat newphrases.json)/g" > newquery.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @newquery.json \
    "127.0.0.1:50021/synthesis?speaker=1" \
    > audio.wav
```

### ユーザー辞書機能について

API からユーザー辞書の参照、単語の追加、編集、削除を行うことができます。

#### 参照

`/user_dict`に GET リクエストを投げることでユーザー辞書の一覧を取得することができます。

```bash
curl -s -X GET "127.0.0.1:50021/user_dict"
```

#### 単語追加

`/user_dict_word`に POST リクエストを投げる事でユーザー辞書に単語を追加することができます。  
URL パラメータとして、以下が必要です。

- surface （辞書に登録する単語）
- pronunciation （カタカナでの読み方）
- accent_type （アクセント核位置、整数）

アクセント核位置については、こちらの文章が参考になるかと思います。  
〇型となっている数字の部分がアクセント核位置になります。  
https://tdmelodic.readthedocs.io/ja/latest/pages/introduction.html

成功した場合の返り値は単語に割り当てられる UUID の文字列になります。

```bash
surface="test"
pronunciation="テスト"
accent_type="1"

curl -s -X POST "127.0.0.1:50021/user_dict_word" \
    --get \
    --data-urlencode "surface=$surface" \
    --data-urlencode "pronunciation=$pronunciation" \
    --data-urlencode "accent_type=$accent_type"
```

#### 単語修正

`/user_dict_word/{word_uuid}`に PUT リクエストを投げる事でユーザー辞書の単語を修正することができます。  
URL パラメータとして、以下が必要です。

- surface （辞書に登録するワード）
- pronunciation （カタカナでの読み方）
- accent_type （アクセント核位置、整数）

word_uuid は単語追加時に確認できるほか、ユーザー辞書を参照することでも確認できます。  
成功した場合の返り値は`204 No Content`になります。

```bash
surface="test2"
pronunciation="テストツー"
accent_type="2"
# 環境によってword_uuidは適宜書き換えてください
word_uuid="cce59b5f-86ab-42b9-bb75-9fd3407f1e2d"

curl -s -X PUT "127.0.0.1:50021/user_dict_word/$word_uuid" \
    --get \
    --data-urlencode "surface=$surface" \
    --data-urlencode "pronunciation=$pronunciation" \
    --data-urlencode "accent_type=$accent_type"
```

#### 単語削除

`/user_dict_word/{word_uuid}`に DELETE リクエストを投げる事でユーザー辞書の単語を削除することができます。

word_uuid は単語追加時に確認できるほか、ユーザー辞書を参照することでも確認できます。  
成功した場合の返り値は`204 No Content`になります。

```bash
# 環境によってword_uuidは適宜書き換えてください
word_uuid="cce59b5f-86ab-42b9-bb75-9fd3407f1e2d"

curl -s -X DELETE "127.0.0.1:50021/user_dict_word/$word_uuid"
```

#### 辞書のインポート&エクスポート

エンジンの[設定ページ](http://127.0.0.1:50021/setting)内の「ユーザー辞書のエクスポート&インポート」節で、ユーザー辞書のインポート&エクスポートが可能です。

他にも API でユーザー辞書のインポート&エクスポートが可能です。  
インポートには `POST /import_user_dict`、エクスポートには `GET /user_dict` を利用します。  
引数等の詳細は API ドキュメントをご覧ください。

### プリセット機能について

`presets.yaml`を編集することでキャラクターや話速などのプリセットを使うことができます。

```bash
echo -n "プリセットをうまく活用すれば、サードパーティ間で同じ設定を使うことができます" >text.txt

# プリセット情報を取得
curl -s -X GET "127.0.0.1:50021/presets" > presets.json

preset_id=$(cat presets.json | sed -r 's/^.+"id"\:\s?([0-9]+?).+$/\1/g')
style_id=$(cat presets.json | sed -r 's/^.+"style_id"\:\s?([0-9]+?).+$/\1/g')

# 音声合成用のクエリを取得
curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query_from_preset?preset_id=$preset_id"\
    --get --data-urlencode text@text.txt \
    > query.json

# 音声合成
curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=$style_id" \
    > audio.wav
```

- `speaker_uuid`は、`/speakers`で確認できます
- `id`は重複してはいけません
- エンジン起動後にファイルを書き換えるとエンジンに反映されます

### 2 種類のスタイルでモーフィングするサンプルコード

`/synthesis_morphing`では、2 種類のスタイルでそれぞれ合成された音声を元に、モーフィングした音声を生成します。

```bash
echo -n "モーフィングを利用することで、２種類の声を混ぜることができます。" > text.txt

curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query?speaker=8"\
    --get --data-urlencode text@text.txt \
    > query.json

# 元のスタイルでの合成結果
curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=8" \
    > audio.wav

export MORPH_RATE=0.5

# スタイル2種類分の音声合成+WORLDによる音声分析が入るため時間が掛かるので注意
curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis_morphing?base_speaker=8&target_speaker=10&morph_rate=$MORPH_RATE" \
    > audio.wav

export MORPH_RATE=0.9

# query、base_speaker、target_speakerが同じ場合はキャッシュが使用されるため比較的高速に生成される
curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis_morphing?base_speaker=8&target_speaker=10&morph_rate=$MORPH_RATE" \
    > audio.wav
```

### キャラクターの追加情報を取得するサンプルコード

追加情報の中の portrait.png を取得するコードです。  
（[jq](https://stedolan.github.io/jq/)を使用して json をパースしています。）

```bash
curl -s -X GET "127.0.0.1:50021/speaker_info?speaker_uuid=7ffcb7ce-00ec-4bdc-82cd-45a8889e43ff" \
    | jq  -r ".portrait" \
    | base64 -d \
    > portrait.png
```

### キャンセル可能な音声合成

`/cancellable_synthesis`では通信を切断した場合に即座に計算リソースが開放されます。  
(`/synthesis`では通信を切断しても最後まで音声合成の計算が行われます)  
この API は実験的機能であり、エンジン起動時に引数で`--enable_cancellable_synthesis`を指定しないと有効化されません。  
音声合成に必要なパラメータは`/synthesis`と同様です。

### HTTP リクエストで歌声合成するサンプルコード

```bash
echo -n '{
  "notes": [
    { "key": null, "frame_length": 15, "lyric": "" },
    { "key": 60, "frame_length": 45, "lyric": "ド" },
    { "key": 62, "frame_length": 45, "lyric": "レ" },
    { "key": 64, "frame_length": 45, "lyric": "ミ" },
    { "key": null, "frame_length": 15, "lyric": "" }
  ]
}' > score.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @score.json \
    "127.0.0.1:50021/sing_frame_audio_query?speaker=6000" \
    > query.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/frame_synthesis?speaker=3001" \
    > audio.wav
```

楽譜の`key`は MIDI 番号です。  
`lyric`は歌詞で、任意の文字列を指定できますが、エンジンによってはひらがな・カタカナ１モーラ以外の文字列はエラーになることがあります。  
フレームレートはデフォルトが 93.75Hz で、エンジンマニフェストの`frame_rate`で取得できます。  
１つ目のノートは無音である必要があります。

`/sing_frame_audio_query`で指定できる`speaker`は、`/singers`で取得できるスタイルの内、種類が`sing`か`singing_teacher`なスタイルの`style_id`です。  
`/frame_synthesis`で指定できる`speaker`は、`/singers`で取得できるスタイルの内、種類が`frame_decode`の`style_id`です。  
引数が `speaker` という名前になっているのは、他の API と一貫性をもたせるためです。

`/sing_frame_audio_query`と`/frame_synthesis`に異なるスタイルを指定することも可能です。

### CORS 設定

VOICEVOX ではセキュリティ保護のため`localhost`・`127.0.0.1`・`app://`・Origin なし以外の Origin からリクエストを受け入れないようになっています。
そのため、一部のサードパーティアプリからのレスポンスを受け取れない可能性があります。  
これを回避する方法として、エンジンから設定できる UI を用意しています。

#### 設定方法

1. <http://127.0.0.1:50021/setting> にアクセスします。
2. 利用するアプリに合わせて設定を変更、追加してください。
3. 保存ボタンを押して、変更を確定してください。
4. 設定の適用にはエンジンの再起動が必要です。必要に応じて再起動をしてください。

### データを変更する API を無効化する

実行時引数`--disable_mutable_api`か環境変数`VV_DISABLE_MUTABLE_API=1`を指定することで、エンジンの設定や辞書などを変更する API を無効にできます。

### 文字コード

リクエスト・レスポンスの文字コードはすべて UTF-8 です。

### その他の引数

エンジン起動時に引数を指定できます。詳しいことは`-h`引数でヘルプを確認してください。

```bash
$ python run.py -h

usage: run.py [-h] [--host HOST] [--port PORT] [--use_gpu] [--voicevox_dir VOICEVOX_DIR] [--voicelib_dir VOICELIB_DIR] [--runtime_dir RUNTIME_DIR] [--enable_mock] [--enable_cancellable_synthesis]
              [--init_processes INIT_PROCESSES] [--load_all_models] [--cpu_num_threads CPU_NUM_THREADS] [--output_log_utf8] [--cors_policy_mode {CorsPolicyMode.all,CorsPolicyMode.localapps}]
              [--allow_origin [ALLOW_ORIGIN ...]] [--setting_file SETTING_FILE] [--preset_file PRESET_FILE] [--disable_mutable_api]

VOICEVOX のエンジンです。

options:
  -h, --help            show this help message and exit
  --host HOST           接続を受け付けるホストアドレスです。
  --port PORT           接続を受け付けるポート番号です。
  --use_gpu             GPUを使って音声合成するようになります。
  --voicevox_dir VOICEVOX_DIR
                        VOICEVOXのディレクトリパスです。
  --voicelib_dir VOICELIB_DIR
                        VOICEVOX COREのディレクトリパスです。
  --runtime_dir RUNTIME_DIR
                        VOICEVOX COREで使用するライブラリのディレクトリパスです。
  --enable_mock         VOICEVOX COREを使わずモックで音声合成を行います。
  --enable_cancellable_synthesis
                        音声合成を途中でキャンセルできるようになります。
  --init_processes INIT_PROCESSES
                        cancellable_synthesis機能の初期化時に生成するプロセス数です。
  --load_all_models     起動時に全ての音声合成モデルを読み込みます。
  --cpu_num_threads CPU_NUM_THREADS
                        音声合成を行うスレッド数です。指定しない場合、代わりに環境変数 VV_CPU_NUM_THREADS の値が使われます。VV_CPU_NUM_THREADS が空文字列でなく数値でもない場合はエラー終了します。
  --output_log_utf8     ログ出力をUTF-8でおこないます。指定しない場合、代わりに環境変数 VV_OUTPUT_LOG_UTF8 の値が使われます。VV_OUTPUT_LOG_UTF8 の値が1の場合はUTF-8で、0または空文字、値がない場合は環境によって自動的に決定されます。
  --cors_policy_mode {CorsPolicyMode.all,CorsPolicyMode.localapps}
                        CORSの許可モード。allまたはlocalappsが指定できます。allはすべてを許可します。localappsはオリジン間リソース共有ポリシーを、app://.とlocalhost関連に限定します。その他のオリジンはallow_originオプションで追加できます。デフォルトはlocalapps。このオプションは--
                        setting_fileで指定される設定ファイルよりも優先されます。
  --allow_origin [ALLOW_ORIGIN ...]
                        許可するオリジンを指定します。スペースで区切ることで複数指定できます。このオプションは--setting_fileで指定される設定ファイルよりも優先されます。
  --setting_file SETTING_FILE
                        設定ファイルを指定できます。
  --preset_file PRESET_FILE
                        プリセットファイルを指定できます。指定がない場合、環境変数 VV_PRESET_FILE、実行ファイルのディレクトリのpresets.yamlを順に探します。
  --disable_mutable_api
                        辞書登録や設定変更など、エンジンの静的なデータを変更するAPIを無効化します。指定しない場合、代わりに環境変数 VV_DISABLE_MUTABLE_API の値が使われます。VV_DISABLE_MUTABLE_API の値が1の場合は無効化で、0または空文字、値がない場合は無視されます。
```

### アップデート

エンジンディレクトリ内にあるファイルを全て消去し、新しいものに置き換えてください。

## 貢献者ガイド

VOICEVOX ENGINE は皆さんのコントリビューションをお待ちしています！  
詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) をご覧ください。  
また [VOICEVOX 非公式 Discord サーバー](https://discord.gg/WMwWetrzuh)にて、開発の議論や雑談を行っています。気軽にご参加ください。

なお、Issue を解決するプルリクエストを作成される際は、別の方と同じ Issue に取り組むことを避けるため、Issue 側で取り組み始めたことを伝えるか、最初に Draft プルリクエストを作成することを推奨しています。

## 開発者ガイド

### 環境構築

`Python 3.11.9` を用いて開発されています。
インストールするには、各 OS ごとの C/C++ コンパイラ、CMake が必要になります。

```bash
# 実行環境のインストール
python -m pip install -r requirements.txt

# 開発環境・テスト環境・ビルド環境のインストール
python -m pip install -r requirements-dev.txt -r requirements-build.txt
```

### 実行

コマンドライン引数の詳細は以下のコマンドで確認してください。

```bash
python run.py --help
```

```bash
# 製品版 VOICEVOX でサーバーを起動
VOICEVOX_DIR="C:/path/to/voicevox" # 製品版 VOICEVOX ディレクトリのパス
python run.py --voicevox_dir=$VOICEVOX_DIR
```

<!-- 差し替え可能な音声ライブラリまたはその仕様が公開されたらコメントを外す
```bash
# 音声ライブラリを差し替える
VOICELIB_DIR="C:/path/to/your/tts-model"
python run.py --voicevox_dir=$VOICEVOX_DIR --voicelib_dir=$VOICELIB_DIR
```
-->

```bash
# モックでサーバー起動
python run.py --enable_mock
```

```bash
# ログをUTF8に変更
python run.py --output_log_utf8
# もしくは VV_OUTPUT_LOG_UTF8=1 python run.py
```

#### CPU スレッド数を指定する

CPU スレッド数が未指定の場合は、論理コア数の半分が使われます。（殆どの CPU で、これは全体の処理能力の半分です）  
もし IaaS 上で実行していたり、専用サーバーで実行している場合など、  
エンジンが使う処理能力を調節したい場合は、CPU スレッド数を指定することで実現できます。

- 実行時引数で指定する
  ```bash
  python run.py --voicevox_dir=$VOICEVOX_DIR --cpu_num_threads=4
  ```
- 環境変数で指定する
  ```bash
  export VV_CPU_NUM_THREADS=4
  python run.py --voicevox_dir=$VOICEVOX_DIR
  ```

#### 過去のバージョンのコアを使う

VOICEVOX Core 0.5.4 以降のコアを使用する事が可能です。  
Mac での libtorch 版コアのサポートはしていません。

##### 過去のバイナリを指定する

製品版 VOICEVOX もしくはコンパイル済みエンジンのディレクトリを`--voicevox_dir`引数で指定すると、そのバージョンのコアが使用されます。

```bash
python run.py --voicevox_dir="/path/to/voicevox"
```

Mac では、`DYLD_LIBRARY_PATH`の指定が必要です。

```bash
DYLD_LIBRARY_PATH="/path/to/voicevox" python run.py --voicevox_dir="/path/to/voicevox"
```

##### 音声ライブラリを直接指定する

[VOICEVOX Core の zip ファイル](https://github.com/VOICEVOX/voicevox_core/releases)を解凍したディレクトリを`--voicelib_dir`引数で指定します。  
また、コアのバージョンに合わせて、[libtorch](https://pytorch.org/)や[onnxruntime](https://github.com/microsoft/onnxruntime) (共有ライブラリ) のディレクトリを`--runtime_dir`引数で指定します。  
ただし、システムの探索パス上に libtorch、onnxruntime がある場合、`--runtime_dir`引数の指定は不要です。  
`--voicelib_dir`引数、`--runtime_dir`引数は複数回使用可能です。  
API エンドポイントでコアのバージョンを指定する場合は`core_version`引数を指定してください。（未指定の場合は最新のコアが使用されます）

```bash
python run.py --voicelib_dir="/path/to/voicevox_core" --runtime_dir="/path/to/libtorch_or_onnx"
```

Mac では、`--runtime_dir`引数の代わりに`DYLD_LIBRARY_PATH`の指定が必要です。

```bash
DYLD_LIBRARY_PATH="/path/to/onnx" python run.py --voicelib_dir="/path/to/voicevox_core"
```

##### ユーザーディレクトリに配置する

以下のディレクトリにある音声ライブラリは自動で読み込まれます。

- ビルド版: `<user_data_dir>/voicevox-engine/core_libraries/`
- Python 版: `<user_data_dir>/voicevox-engine-dev/core_libraries/`

`<user_data_dir>`は OS によって異なります。

- Windows: `C:\Users\<username>\AppData\Local\`
- macOS: `/Users/<username>/Library/Application\ Support/`
- Linux: `/home/<username>/.local/share/`

### ビルド

`pyinstaller` を用いたパッケージ化と Dockerfile を用いたコンテナ化によりローカルでビルドが可能です。  
手順の詳細は [貢献者ガイド#ビルド](./CONTRIBUTING.md#ビルド) を御覧ください。

GitHub を用いる場合、fork したリポジトリで GitHub Actions によるビルドが可能です。  
Actions を ON にし、workflow_dispatch で`build-engine-package.yml`を起動すればビルドできます。
成果物は Release にアップロードされます。
ビルドに必要な GitHub Actions の設定は [貢献者ガイド#GitHub Actions](./CONTRIBUTING.md#github-actions) を御覧ください。

### テスト・静的解析

`pytest` を用いたテストと各種リンターを用いた静的解析が可能です。  
手順の詳細は [貢献者ガイド#テスト](./CONTRIBUTING.md#テスト), [貢献者ガイド#静的解析](./CONTRIBUTING.md#静的解析) を御覧ください。

### 依存関係

依存関係は `poetry` で管理されています。また、導入可能な依存ライブラリにはライセンス上の制約があります。  
詳細は [貢献者ガイド#パッケージ](./CONTRIBUTING.md#パッケージ) を御覧ください。

### マルチエンジン機能に関して

VOICEVOX エディターでは、複数のエンジンを同時に起動することができます。
この機能を利用することで、自作の音声合成エンジンや既存の音声合成エンジンを VOICEVOX エディター上で動かすことが可能です。

<img src="./docs/res/マルチエンジン概念図.svg" width="320">

<details>

#### マルチエンジン機能の仕組み

VOICEVOX API に準拠した複数のエンジンの Web API をポートを分けて起動し、統一的に扱うことでマルチエンジン機能を実現しています。
エディターがそれぞれのエンジンを実行バイナリ経由で起動し、EngineID と結びつけて設定や状態を個別管理します。

#### マルチエンジン機能への対応方法

VOICEVOX API 準拠エンジンを起動する実行バイナリを作ることで対応が可能です。
VOICEVOX ENGINE リポジトリを fork し、一部の機能を改造するのが簡単です。

改造すべき点はエンジン情報・キャラクター情報・音声合成の３点です。

エンジンの情報はルート直下のマニフェストファイル（`engine_manifest.json`）で管理されています。
この形式のマニフェストファイルは VOICEVOX API 準拠エンジンに必須です。
マニフェストファイル内の情報を見て適宜変更してください。
音声合成手法によっては、例えばモーフィング機能など、VOICEVOX と同じ機能を持つことができない場合があります。
その場合はマニフェストファイル内の`supported_features`内の情報を適宜変更してください。

キャラクター情報は`resources/character_info`ディレクトリ内のファイルで管理されています。
ダミーのアイコンなどが用意されているので適宜変更してください。

音声合成は`voicevox_engine/tts_pipeline/tts_engine.py`で行われています。
VOICEVOX API での音声合成は、エンジン側で音声合成用のクエリ `AudioQuery` の初期値を作成してユーザーに返し、ユーザーが必要に応じてクエリを編集したあと、エンジンがクエリに従って音声合成することで実現しています。
クエリ作成は`/audio_query`エンドポイントで、音声合成は`/synthesis`エンドポイントで行っており、最低この２つに対応すれば VOICEVOX API に準拠したことになります。

#### マルチエンジン機能対応エンジンの配布方法

VVPP ファイルとして配布するのがおすすめです。
VVPP は「VOICEVOX プラグインパッケージ」の略で、中身はビルドしたエンジンなどを含んだディレクトリの Zip ファイルです。
拡張子を`.vvpp`にすると、ダブルクリックで VOICEVOX エディターにインストールできます。

エディター側は受け取った VVPP ファイルをローカルディスク上に Zip 展開したあと、ルートの直下にある`engine_manifest.json`に従ってファイルを探査します。
VOICEVOX エディターにうまく読み込ませられないときは、エディターのエラーログを参照してください。

また、`xxx.vvpp`は分割して連番を付けた`xxx.0.vvppp`ファイルとして配布することも可能です。
これはファイル容量が大きくて配布が困難な場合に有用です。

</details>

## 事例紹介

**[voicevox-client](https://github.com/voicevox-client) [@voicevox-client](https://github.com/voicevox-client)** ･･･ VOICEVOX ENGINE の各言語向け API ラッパー

## ライセンス

LGPL v3 と、ソースコードの公開が不要な別ライセンスのデュアルライセンスです。
別ライセンスを取得したい場合は、ヒホに求めてください。  
X アカウント: [@hiho_karuta](https://x.com/hiho_karuta)
