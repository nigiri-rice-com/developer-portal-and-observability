# Developer Portal & Observability Stack (Qiita 7大ドキュメント準拠)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![Uptime Kuma](https://img.shields.io/badge/Monitoring-Uptime%20Kuma-5cd875.svg)](https://github.com/louislam/uptime-kuma)
[![Prometheus](https://img.shields.io/badge/Prometheus-v2.51-e6522c.svg)](https://prometheus.io/)

Qiita の策定基準（7つの必須ドキュメント）に準拠した統合開発者ポータル（FastAPI）と、
Uptime Kuma / Prometheus / Grafana による全方位クラウドネイティブ監視スタックのリファレンス実装です。

---

## 🌟 主な特徴

1. **Qiita 7大必須ドキュメント完全準拠ポータル**
   - 要件定義・技術選定・DB設計・画面/API仕様・処理フロー・運用Runbook・復旧手順を完備。
   - GitHub Docs 風のモダンな UI（Tailwind CSS, Lucide Icons, Mermaid.js ダイアグラム動的描画）。
2. **リアルタイム死活監視 & SLA ステータスページ**
   - Uptime Kuma による外形監視（HTTPS 200 OK、レスポンスタイム、証明書有効期限）。
   - パブリックステータスページをリアルタイム提供。
3. **Prometheus & Grafana メトリクス可観測性**
   - コンテナ、CPU、メモリ、ディスクI/O、ネットワーク帯域の包括的テレメトリ収集。

---

## 🚀 クイックスタート

```bash
# 1. Developer Portal (FastAPI) 起動
cd portal
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8080

# 2. 可観測性スタック (Uptime Kuma / Prometheus) 起動
cd ../monitoring
docker compose -f docker-compose.monitoring.yml up -d
```

---

## 📄 ライセンス

本リポジトリは [MIT License](LICENSE) の下で公開されています。
