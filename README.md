# 🔍 KWIC Search Tool（KWIC検索ツール）

このツールは、**Flask** と **spaCy** を使って構築されたWebベースの KWIC（Key Word in Context）検索アプリケーションです。  
キーワードの前後の文脈を表示し、以下のタイプに対応した検索が可能です：

- ✅ 単語（token）
- ✅ 品詞（POS）
- ✅ 固有表現（Entity）
- ✅ フレーズ（N-gram）

---

## ✨ 主な機能

- 📂 `.txt`ファイルをドラッグ＆ドロップでアップロード可能
- 📝 フォームから直接テキスト入力もOK
- 🎯 対象語の強調表示（太字、下線）
- 📱 モバイル対応のレスポンシブデザイン
- 🔁 検索結果は「次に続く単語」や「品詞」で並べ替え可能

---

## 🧩 必要な環境

- Python 3.8 以上
- Flask
- spaCy + 英語モデル `en_core_web_sm`

### インストール方法

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
