# -*- coding: utf-8 -*-
"""
Statuspage Data Provider for Nigiri Developer Portal
Modeled after Atlassian Statuspage (discordstatus.com)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

def generate_90_days_history(base_uptime=99.99, recent_maintenance_date="2026-09-11") -> List[Dict[str, Any]]:
    history = []
    today = datetime(2026, 9, 12)
    for i in range(89, -1, -1):
        d = today - timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        
        status = "operational"
        uptime = 100.0
        note = "正常稼働 (0 incidents)"

        if date_str == recent_maintenance_date:
            status = "maintenance"
            uptime = 99.8
            note = "定期メンテナンス (正常完了)"
        elif date_str == "2026-09-08":
            status = "maintenance"
            uptime = 99.7
            note = "全域システム更新 (正常完了)"

        history.append({
            "date": date_str,
            "status": status,
            "uptime": uptime,
            "note": note
        })
    return history

def get_status_page_data() -> Dict[str, Any]:
    return {
        "overall_status": "All Systems Operational",
        "overall_color": "emerald",
        "last_updated": "2026-09-12 03:26 JST",
        "component_groups": [
            {
                "name": "認証 & ID 基盤 (Identity & Security)",
                "icon": "shield-check",
                "components": [
                    {
                        "name": "Keycloak SSO (OmusuBI Core)",
                        "description": "HA 2 Pods / Quarkus / master realm",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-09")
                    },
                    {
                        "name": "OmusuBI Console",
                        "description": "アカウント統合管理 / Excel・CSV 出力",
                        "status": "Operational",
                        "uptime": "99.98",
                        "history": generate_90_days_history(99.98, "2026-09-10")
                    },
                    {
                        "name": "HashiCorp Vault",
                        "description": "シークレット共有・動的トークン / SSO標準化",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-11")
                    }
                ]
            },
            {
                "name": "エッジ & ネットワーク (Edge & Routing)",
                "icon": "globe",
                "components": [
                    {
                        "name": "Cloudflare Edge & WAF",
                        "description": "DNS / DDoS 防護 / SSL Full Strict",
                        "status": "Operational",
                        "uptime": "100.0",
                        "history": generate_90_days_history(100.0)
                    },
                    {
                        "name": "Caddy Reverse Proxy",
                        "description": "Let's Encrypt 自動更新 / エッジルーティング",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-11")
                    },
                    {
                        "name": "Ingress-NGINX Controller",
                        "description": "K8s NodePort 30180 / 2 Pods HA",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99)
                    },
                    {
                        "name": "Cloudflare Argo CD Tunnel",
                        "description": "cloudflared 2 Pods 冗長暗号化トンネル",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-09")
                    }
                ]
            },
            {
                "name": "ストレージ & レジストリ (Storage & Registries)",
                "icon": "database",
                "components": [
                    {
                        "name": "Harbor Container Registry",
                        "description": "プライベートレジストリ / Trivy セキュリティスキャン",
                        "status": "Operational",
                        "uptime": "99.98",
                        "history": generate_90_days_history(99.98)
                    },
                    {
                        "name": "SMB CSI Storage Driver",
                        "description": "CIFS ボリュームマウント (ホスト固定)",
                        "status": "Operational",
                        "uptime": "99.97",
                        "history": generate_90_days_history(99.97, "2026-09-09")
                    }
                ]
            },
            {
                "name": "業務アプリケーション (Business Applications)",
                "icon": "layers",
                "components": [
                    {
                        "name": "CNT Connect (本番環境)",
                        "description": "備品・貸出管理 / Next.js + NestJS + PostgreSQL",
                        "status": "Operational",
                        "uptime": "99.98",
                        "history": generate_90_days_history(99.98)
                    },
                    {
                        "name": "CNT Connect (開発環境)",
                        "description": "ステージング・新機能結合テスト環境",
                        "status": "Operational",
                        "uptime": "99.95",
                        "history": generate_90_days_history(99.95)
                    },
                    {
                        "name": "WordPress (nigiri-rice.com)",
                        "description": "公式コーポレートサイト & MariaDB",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99)
                    },
                    {
                        "name": "Nigiri Developer Portal",
                        "description": "開発ハブ / 2 Pods HA / JIT ロール同期",
                        "status": "Operational",
                        "uptime": "100.0",
                        "history": generate_90_days_history(100.0)
                    }
                ]
            },
            {
                "name": "メール & 独立サービス (Mail & Standalone)",
                "icon": "mail",
                "components": [
                    {
                        "name": "Mailcow メールサーバー",
                        "description": "SMTP / IMAP / SOGo Webmail / Rspamd",
                        "status": "Operational",
                        "uptime": "99.97",
                        "history": generate_90_days_history(99.97, "2026-09-07")
                    },
                    {
                        "name": "AFFiNE ナレッジベース",
                        "description": "ドキュメント・ホワイトボード共有 (Port 8083)",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-08")
                    },
                    {
                        "name": "Portainer 管理基盤",
                        "description": "K8s 管理コンソール (v2.45.0)",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-07")
                    }
                ]
            },
            {
                "name": "インフラホスト基盤 (Infrastructure Hosts)",
                "icon": "server",
                "components": [
                    {
                        "name": "Xserver VPS (nigiri-vps)",
                        "description": "Ubuntu 24.04 / k3s Control Plane",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99, "2026-09-08")
                    },
                    {
                        "name": "k3s Worker Nodes (01〜04)",
                        "description": "4台の Docker DinD Worker ノード",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99)
                    },
                    {
                        "name": "Proxmox VE (PVE ホスト)",
                        "description": "オンプレミス仮想化基盤 (Kernel 7.0.14-15)",
                        "status": "Operational",
                        "uptime": "99.98",
                        "history": generate_90_days_history(99.98, "2026-09-08")
                    },
                    {
                        "name": "Active Directory (VM 140)",
                        "description": "Windows Server ドメインコントローラ",
                        "status": "Operational",
                        "uptime": "99.99",
                        "history": generate_90_days_history(99.99)
                    }
                ]
            }
        ],
        "incidents": [
            {
                "title": "HashiCorp Vault SSO 標準化 & OIDC デフォルトログイン設定",
                "date": "2026-09-11 01:40 JST",
                "duration": "15 分",
                "status": "完了",
                "description": "Vault 認証方式を SSO (Keycloak OIDC) と Admin (Token) に限定し、Web UI アクセス時に ?with=oidc へ自動リダイレクトするルールを Caddyfile に配備。未認証表示チューニングを実施。",
                "impact": "影響なし (無停止リロードにて反映)"
            },
            {
                "title": "OmusuBI Console UI 刷新 & ユーザーエクスポート (Excel/CSV) 機能修復",
                "date": "2026-09-10 01:25 JST",
                "duration": "30 分",
                "status": "完了",
                "description": "有効ユーザー（9名）、無効ユーザー（1名）、全ユーザー（10名）のエクスポート条件分岐を実装。Orion 表記を完全排除し、EnableAt / DisableAt 列を維持した Excel 出力機能を復旧。",
                "impact": "影響なし (ローリングアップデート)"
            },
            {
                "title": "Argo CD k8s-cluster-yaml 管理移行 & SMB CSI ホスト固定配備",
                "date": "2026-09-09 18:45 JST",
                "duration": "45 分",
                "status": "完了",
                "description": "全12アプリケーションの GitOps 管理元を nigiri-rice-com/k8s-cluster-yaml に統合。Linux カーネルの rshared 制約に対応し、SMB CSI Node をホスト nigiri-vps に固定運用化。",
                "impact": "影響なし (GitOps 手動/自動同期移行)"
            },
            {
                "title": "VPS / PVE 全域定期システム更新 & カーネル適用",
                "date": "2026-09-08 08:15 JST",
                "duration": "1 時間",
                "status": "完了",
                "description": "PVE 9.2.11 / Kernel 7.0.14-15 へのアップグレード、VPS APT セキュリティパッチ適用、MariaDB および PostgreSQL のマイナー更新を実施。",
                "impact": "計画メンテナンス (早朝帯にて実施完了)"
            }
        ]
    }
