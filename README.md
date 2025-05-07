<img src="images/minsys_chatai.png" width="10%">

# test-chatai-public

## 概要
`minsys-chatai`は、ネットワークエンジニアの業務をサポートするためのAIアシスタントです。  
Discordを通じて、BGP経路情報の取得やAS番号に関する情報を提供します。


## 必要条件
- DockerおよびDocker Composeがインストールされていること
- OpenAI APIキー
- Discord Botのクライアントシークレット
- BGPルーターの接続情報（ホスト、ユーザー名、パスワード）Junosを想定しています。


## セットアップ手順

### 1. リポジトリのクローン
```bash
git clone <リポジトリURL>
cd minsys-chatai
```

### 2. .envファイルの作成
```
cp .env.sample .env
```

.envファイルに以下の情報を記載します：
```bash
DISCORD_BOT_CHATAI_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXX
OPENAI_CHATAI_API_KEYS=XXXXXXXXXXXXXXXXXXXXX
BGP_ROUTER_HOST=xxx.xxx.xxx.xxx
BGP_ROUTER_USER=xxxxx
BGP_ROUTER_PASS=xxxxx
```

## 起動方法
```bash
docker-compose up --build -d
```

## 使用方法
### Discord Botの利用
1. DiscordサーバーにBotを追加します。
2. Discordサーバーに`chatai`というチャンネルを作ります。
3. chataiチャンネルで以下のコマンドを使用できます：
    - !memory：現在の記憶を表示します。
    - !clear：チャットログと記憶をクリアします。
    - その他の質問を自由に入力してください。

### ログの確認
- チャットログ: logs/chat_log.txt
- 記憶データ: logs/memory.txt

## 停止方法
```bash
docker-compose down
```