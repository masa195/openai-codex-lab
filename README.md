# openai-codex-lab
OpenAI Codexの実験・練習場

## 目標達成支援アプリ
`goal_tracker.py` はシンプルな目標管理用CLIツールです。以下のようなコマンドが利用できます。

```bash
# 目標の追加
python goal_tracker.py add "読書をする" -d "週に1冊" --due 2024-12-31

# 目標一覧の表示
python goal_tracker.py list

# 目標を完了にする
python goal_tracker.py complete 1

# 目標を削除する
python goal_tracker.py delete 1

# 達成状況を確認する
python goal_tracker.py progress
```

goals.json にデータが保存されます。
