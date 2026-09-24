# -*- coding: utf-8 -*-
"""
Services Metadata & Architecture Definitions for Nigiri Developer Portal
OmusuBI Dev Platform - 2026
"""

from typing import Dict, Any, List, Optional

SERVICES_DATA: Dict[str, Dict[str, Any]] = {
    "argocd": {
        "id": "argocd",
        "name": "Argo CD",
        "category": "GitOps / デプロイ",
        "tag": "GitOps",
        "icon": "git-pull-request",
        "description": "Kubernetes マニフェスト自動同期・GitOps コントロールパネル。リポジトリの変更をクラスタへ自動反映します。",
        "status": "正常稼働中 (HA 2 Pods 冗長構成)",
        "status_color": "emerald",
        "public_url": "https://argocd.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "argocd",
        "network": {
            "public_dns": "argocd.nigiri-rice.com",
            "internal_dns": "argocd-server.argocd.svc.cluster.local",
            "internal_port": "80 (HTTP) / 443 (HTTPS)",
            "protocol": "HTTPS (TLS Termination via Cloudflare / Caddy)",
            "ingress_route": "Cloudflare Tunnel -> Ingress-NGINX (NodePort 30180) -> argocd-server:80"
        },
        "k8s": {
            "namespace": "argocd",
            "workload_type": "Deployment / StatefulSet",
            "replicas": "argocd-server: 2 Pods / argocd-repo-server: 2 Pods",
            "nodes": "nigiri-vps, vps-worker-04 (分散配置)",
            "database": "Redis HA (Sentinel 3ノード構成)",
            "storage": "Ephemeral / ConfigMap & Secrets",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/cloudflare-argocd-tunnel/"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC)",
            "realm": "master",
            "client_id": "argocd",
            "auth_flow": "Authorization Code Flow (PKCE)",
            "allowed_roles": ["admin", "Developer"]
        },
        "topology": [
            {"step": "1. ユーザーアクセス", "from": "Client Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "WAF & DNS (argocd.nigiri-rice.com)"},
            {"step": "2. エッジトンネル", "from": "Cloudflare Edge", "to": "cloudflared Tunnel Pods", "protocol": "HTTP/2 QUIC", "note": "内部クラスタへ暗号化トンネル"},
            {"step": "3. サービス解決", "from": "cloudflared", "to": "argocd-server (Service)", "protocol": "ClusterIP :80", "note": "K8s 内部 CoreDNS 経由"},
            {"step": "4. コントローラ連携", "from": "argocd-server", "to": "argocd-repo-server", "protocol": "gRPC :8081", "note": "マニフェスト生成 & Gitリポジトリ取得"},
            {"step": "5. クラスタ同期", "from": "argocd-controller", "to": "K8s API Server", "protocol": "HTTPS :6443", "note": "5ノードへのマニフェスト自動反映"},
            {"step": "6. キャッシュ & 状態", "from": "argocd-server", "to": "argocd-redis-ha", "protocol": "TCP :6379", "note": "セッション & クラスタ状態キャッシュ"}
        ],
        "mermaid": """graph TD
    Client["User Browser"] -->|HTTPS:443| CF["Cloudflare Edge (WAF/DNS)"]
    CF -->|Tunnel / QUIC| CFT["cloudflared Daemon (2 Pods)"]
    CFT -->|HTTP:80| Svc["Service: argocd-server"]
    Svc --> Pod1["argocd-server-pod-1 (nigiri-vps)"]
    Svc --> Pod2["argocd-server-pod-2 (vps-worker-04)"]
    Pod1 & Pod2 -->|gRPC:8081| Repo["argocd-repo-server (HA)"]
    Pod1 & Pod2 -->|TCP:6379| Redis["argocd-redis-ha (3 Nodes)"]
    Pod1 & Pod2 -->|OIDC Auth| Keycloak["Keycloak SSO (sso.nigiri-rice.com)"]
    Repo -->|Sync| Git["GitHub (k8s-cluster-yaml)"]
    Pod1 & Pod2 -->|Apply| K8sAPI["k3s Control Plane API :6443"]""",
        "commands": [
            {"desc": "ArgoCD 関連 Pod の稼働状況確認", "cmd": "kubectl get pods -n argocd -o wide"},
            {"desc": "ArgoCD Server のログ確認 (直近50行)", "cmd": "kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server --tail=50"},
            {"desc": "GitOps 同期ステータス確認", "cmd": "kubectl get applications -n argocd"},
            {"desc": "ArgoCD Server 再起動 (ローリングアップデート)", "cmd": "kubectl rollout restart deploy -n argocd argocd-server"}
        ]
    },
    "harbor": {
        "id": "harbor",
        "name": "Harbor Registry",
        "category": "コンテナレジストリ",
        "tag": "OCI",
        "icon": "box",
        "description": "プライベート OCI / Docker コンテナイメージ保管庫 & 脆弱性スキャナー。CI/CDパイプラインの中心ハブです。",
        "status": "正常稼働中 (HA 2 Pods 冗長構成)",
        "status_color": "emerald",
        "public_url": "https://registry.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "harbor",
        "network": {
            "public_dns": "registry.nigiri-rice.com",
            "internal_dns": "harbor-portal.harbor.svc.cluster.local",
            "internal_port": "80 (HTTP) / 443 (HTTPS)",
            "protocol": "HTTPS (TLS Termination via Caddy)",
            "ingress_route": "Cloudflare -> Caddy (Host) -> Ingress-NGINX (NodePort 30180) -> harbor-portal:80"
        },
        "k8s": {
            "namespace": "harbor",
            "workload_type": "Deployment / StatefulSet",
            "replicas": "harbor-core: 2 Pods / harbor-portal: 2 Pods",
            "nodes": "nigiri-vps, vps-worker-04",
            "database": "PostgreSQL (harbor-database)",
            "storage": "PVC (Local PersistentVolume / Registry Data)",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/harbor/"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC)",
            "realm": "master",
            "client_id": "harbor",
            "auth_flow": "OIDC Integration with Keycloak",
            "allowed_roles": ["admin", "Developer"]
        },
        "topology": [
            {"step": "1. ユーザー / Docker Client", "from": "Docker CLI / Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "docker login registry.nigiri-rice.com"},
            {"step": "2. エッジプロキシ", "from": "Cloudflare Edge", "to": "Caddy Reverse Proxy", "protocol": "HTTPS :443", "note": "Let's Encrypt TLS 終端 & Hostルーティング"},
            {"step": "3. クラスタ Ingress", "from": "Caddy", "to": "Ingress-NGINX Controller", "protocol": "HTTP :30180", "note": "NodePort 経由でクラスタ内転送"},
            {"step": "4. Harbor Core", "from": "Ingress-NGINX", "to": "harbor-core (2 Pods)", "protocol": "HTTP :8080", "note": "API処理 & 認証トークン発行"},
            {"step": "5. イメージ保存", "from": "harbor-core", "to": "harbor-registry (Storage)", "protocol": "HTTP :5000", "note": "OCI レジストリ Blob 保存 (PVC)"},
            {"step": "6. 脆弱性スキャン", "from": "harbor-jobservice", "to": "trivy-scanner", "protocol": "Internal API", "note": "イメージ Push 時の自動スキャン"}
        ],
        "mermaid": """graph TD
    Client["Docker Client / Developer"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|Proxy| Caddy["Caddy Proxy (nigiri-vps)"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX (HA)"]
    Ing -->|HTTP| Core["harbor-core (2 Pods)"]
    Core -->|Auth| Keycloak["Keycloak SSO (sso.nigiri-rice.com)"]
    Core -->|Registry| Reg["harbor-registry (Blob Store)"]
    Core -->|Metadata| DB["harbor-database (PostgreSQL)"]
    Core -->|Jobs| Job["harbor-jobservice"]
    Job -->|Scan| Trivy["Trivy Vulnerability Scanner"]""",
        "commands": [
            {"desc": "Harbor 関連 Pod 一覧", "cmd": "kubectl get pods -n harbor -o wide"},
            {"desc": "Harbor Core ログ監視", "cmd": "kubectl logs -n harbor -l app.kubernetes.io/component=core --tail=50 -f"},
            {"desc": "Harbor 関連 PVC / ストレージ使用量確認", "cmd": "kubectl get pvc -n harbor"}
        ]
    },
    "vault": {
        "id": "vault",
        "name": "HashiCorp Vault",
        "category": "シークレット管理",
        "tag": "Secrets",
        "icon": "shield-check",
        "description": "APIキー、暗号化キー、各種トークンのセキュアストレージ & 動的シークレット基盤。",
        "status": "正常稼働中 (Standalone / PVC File Storage)",
        "status_color": "emerald",
        "public_url": "https://vault.nigiri-rice.com/ui/vault/dashboard",
        "sso_enabled": True,
        "cred_keyword": "vault",
        "network": {
            "public_dns": "vault.nigiri-rice.com",
            "internal_dns": "vault.vault.svc.cluster.local",
            "internal_port": "8200 (API / HTTP)",
            "protocol": "HTTPS (TLS)",
            "ingress_route": "Cloudflare -> Caddy -> Ingress-NGINX (NodePort 30180) -> vault:8200"
        },
        "k8s": {
            "namespace": "vault",
            "workload_type": "StatefulSet (vault-0) + Agent Injector (2 Pods)",
            "replicas": "1 Server + 2 Injectors",
            "nodes": "nigiri-vps (Server), vps-worker-01, vps-worker-03 (Injectors)",
            "database": "Standalone Encrypted File Storage (Local PV)",
            "storage": "PersistentVolumeClaim (vault-data)",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "vault-secretstore/"
        },
        "auth": {
            "provider": "OIDC (SSO: Keycloak) / Token (Admin) / Kubernetes",
            "realm": "master (Keycloak OIDC連携)",
            "client_id": "vault",
            "auth_flow": "OIDC Authorization Code Flow (PKCE) / Token Auth",
            "allowed_roles": ["admin"]
        },
        "topology": [
            {"step": "1. 開発者 / 外部接続", "from": "Developer / External Client", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "vault.nigiri-rice.com (SSO自動誘導)"},
            {"step": "2. リバースプロキシ", "from": "Cloudflare Edge", "to": "Caddy (nigiri-vps)", "protocol": "HTTPS :443", "note": "TLS 終端 & ?with=oidc 自動リダイレクト"},
            {"step": "3. サービス解決", "from": "Ingress-NGINX", "to": "vault (ClusterIP 10.43.191.0)", "protocol": "TCP :8200", "note": "vault-0 へのルーティング"},
            {"step": "4. SSO 認証連携", "from": "vault-0", "to": "Keycloak (sso.nigiri-rice.com)", "protocol": "HTTPS :443", "note": "OIDC PKCE コード検証・adminポリシー付与"},
            {"step": "5. シークレット注入", "from": "vault-agent-injector", "to": "K8s App Pods", "protocol": "Internal IPC", "note": "Mutating Webhook 経由サイドカー注入"}
        ],
        "mermaid": """graph TD
    Client["Developer / Browser"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (SSO Redir)"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX"]
    Ing -->|HTTP:8200| Svc["vault Service :8200"]
    Svc --> Server["vault-0 (Active Server)"]
    Server <-->|OIDC Auth| KC["Keycloak SSO"]
    Inj["vault-agent-injector (2 Pods)"] -->|Webhook| K8sApp["K8s App Pods"]
    K8sApp -->|K8s Auth| Server""",
        "commands": [
            {"desc": "Vault サーバー状態確認", "cmd": "kubectl exec -n vault vault-0 -- vault status"},
            {"desc": "Vault 稼働 Pod 一覧", "cmd": "kubectl get pods -n vault -o wide"},
            {"desc": "Vault 認証メソッド一覧", "cmd": "kubectl exec -n vault vault-0 -- vault auth list"}
        ]
    },
    "keycloak_admin": {
        "id": "keycloak_admin",
        "name": "Keycloak SSO Admin",
        "category": "ID & 認証基盤",
        "tag": "Admin",
        "icon": "key",
        "description": "レルム設定、クライアント管理、ユーザー・ロールマッピング、Discordソーシャル連携の認証コア基盤。",
        "status": "正常稼働中 (HA 2 Pods 冗長構成)",
        "status_color": "emerald",
        "public_url": "https://sso.nigiri-rice.com/admin/master/console/",
        "sso_enabled": True,
        "cred_keyword": "keycloak",
        "network": {
            "public_dns": "sso.nigiri-rice.com",
            "internal_dns": "omusubi-core.omusubi.svc.cluster.local",
            "internal_port": "8080 (HTTP)",
            "protocol": "HTTPS (TLS Termination via Caddy)",
            "ingress_route": "Cloudflare -> Caddy -> Ingress-NGINX (NodePort 30180) -> omusubi-core:8080"
        },
        "k8s": {
            "namespace": "omusubi",
            "workload_type": "Deployment (omusubi-core)",
            "replicas": "2 Pods (HA 冗長構成)",
            "nodes": "nigiri-vps, vps-worker-04",
            "database": "PostgreSQL 16 (omusubi-core-postgres.omusubi.svc:5432)",
            "storage": "Postgres PV / PVC",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/omusubi-keycloak/"
        },
        "auth": {
            "provider": "Self (Keycloak Master Realm)",
            "realm": "master",
            "client_id": "security-admin-console",
            "auth_flow": "OAuth2 / OIDC",
            "allowed_roles": ["admin"]
        },
        "topology": [
            {"step": "1. 認証リクエスト", "from": "All Apps & Users", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "sso.nigiri-rice.com"},
            {"step": "2. プロキシルーティング", "from": "Cloudflare Edge", "to": "Caddy (nigiri-vps)", "protocol": "HTTPS :443", "note": "TLS終端 & Ingress 30180"},
            {"step": "3. サービス分散", "from": "Ingress-NGINX", "to": "omusubi-core (Service)", "protocol": "ClusterIP :8080", "note": "ラウンドロビン負荷分散"},
            {"step": "4. 冗長 Pod 処理", "from": "omusubi-core (Svc)", "to": "omusubi-core-pod-1 & 2", "protocol": "HTTP :8080", "note": "nigiri-vps & vps-worker-04"},
            {"step": "5. 分散セッション同期", "from": "pod-1", "to": "pod-2", "protocol": "JGroups / Infinispan :7800", "note": "Pod間クラスタリング通信"},
            {"step": "6. 永続データ取得", "from": "omusubi-core", "to": "omusubi-core-postgres", "protocol": "TCP :5432", "note": "PostgreSQL 接続プール"}
        ],
        "mermaid": """graph TD
    User["User / Apps (All Services)"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy Reverse Proxy"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX (HA)"]
    Ing -->|HTTP:8080| Svc["Service: omusubi-core"]
    Svc --> Pod1["omusubi-core-pod-1 (nigiri-vps)"]
    Svc --> Pod2["omusubi-core-pod-2 (vps-worker-04)"]
    Pod1 <-->|"Infinispan :7800 (HA Sync)"| Pod2
    Pod1 & Pod2 -->|JDBC:5432| DB["omusubi-core-postgres (PostgreSQL 16)"]
    Pod1 & Pod2 -->|REST API| Discord["Discord API (OAuth2 / Roles)"]""",
        "commands": [
            {"desc": "Keycloak (omusubi-core) Pod 稼働状況確認", "cmd": "kubectl get pods -n omusubi -o wide"},
            {"desc": "Infinispan クラスタ同期ログの確認", "cmd": "kubectl logs -n omusubi -l app.kubernetes.io/name=omusubi-core --tail=100 | grep -i ispn"},
            {"desc": "PostgreSQL DB 接続テスト", "cmd": "kubectl exec -n omusubi deploy/omusubi-core -- curl -s http://localhost:8080/health/ready"}
        ]
    },
    "omusubi_console": {
        "id": "omusubi_console",
        "name": "OmusuBI Console",
        "category": "ID & 認証基盤",
        "tag": "IdP",
        "icon": "user-check",
        "description": "統合ID管理、ソーシャルアカウント連携、アカウント設定コンソール。ユーザー自身による登録・設定画面です。",
        "status": "正常稼働中 (HA 2 Pods 冗長構成)",
        "status_color": "emerald",
        "public_url": "https://id.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "omusubi",
        "network": {
            "public_dns": "id.nigiri-rice.com",
            "internal_dns": "omusubi-console.omusubi.svc.cluster.local",
            "internal_port": "8080 (HTTP)",
            "protocol": "HTTPS (TLS Termination via Caddy)",
            "ingress_route": "Cloudflare -> Caddy -> Ingress-NGINX (NodePort 30180) -> omusubi-console:8080"
        },
        "k8s": {
            "namespace": "omusubi",
            "workload_type": "Deployment (omusubi-console)",
            "replicas": "2 Pods (HA 冗長構成)",
            "nodes": "nigiri-vps, vps-worker-04",
            "database": "Keycloak Admin REST API 連携",
            "storage": "Stateless",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/omusubi-console/"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC)",
            "realm": "master",
            "client_id": "omusubi-console",
            "auth_flow": "NextAuth / OIDC Code Flow",
            "allowed_roles": ["Developer", "admin", "User"]
        },
        "topology": [
            {"step": "1. ユーザーアクセス", "from": "User Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "id.nigiri-rice.com"},
            {"step": "2. Caddy ルーティング", "from": "Cloudflare Edge", "to": "Caddy Reverse Proxy", "protocol": "HTTPS :443", "note": "nigiri-vps ホスト"},
            {"step": "3. クラスタ Ingress", "from": "Caddy", "to": "Ingress-NGINX", "protocol": "HTTP :30180", "note": "NodePort 転送"},
            {"step": "4. フロントエンド配信", "from": "Ingress-NGINX", "to": "omusubi-console (2 Pods)", "protocol": "HTTP :8080", "note": "Next.js SSR / Static Assets"},
            {"step": "5. API 通信", "from": "omusubi-console", "to": "omusubi-core (Keycloak)", "protocol": "HTTP :8080", "note": "クラスタ内部 CoreDNS 経由"}
        ],
        "mermaid": """graph TD
    User["User Browser"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (nigiri-vps)"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX"]
    Ing -->|HTTP:8080| Svc["Service: omusubi-console"]
    Svc --> Pod1["omusubi-console-pod-1 (nigiri-vps)"]
    Svc --> Pod2["omusubi-console-pod-2 (vps-worker-04)"]
    Pod1 & Pod2 -->|Internal API:8080| Keycloak["omusubi-core (Keycloak)"]""",
        "commands": [
            {"desc": "Console Pod 一覧確認", "cmd": "kubectl get pods -n omusubi -l app.kubernetes.io/name=omusubi-console -o wide"},
            {"desc": "Console Pod ログ確認", "cmd": "kubectl logs -n omusubi -l app.kubernetes.io/name=omusubi-console --tail=50"},
            {"desc": "Console 再起動 (ローリング)", "cmd": "kubectl rollout restart deploy -n omusubi omusubi-console"}
        ]
    },
    "portainer": {
        "id": "portainer",
        "name": "Portainer Management",
        "category": "インフラ運用",
        "tag": "Infra",
        "icon": "layers",
        "description": "Docker コンテナ & Kubernetes クラスター可視化・リソース監視。クラスター全体のワークロード状況を一元管理します。",
        "status": "正常稼働中 (Kubernetes Deployment)",
        "status_color": "emerald",
        "public_url": "https://manage.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "portainer",
        "network": {
            "public_dns": "manage.nigiri-rice.com",
            "internal_dns": "portainer.portainer.svc.cluster.local",
            "internal_port": "9000 (HTTP) / 9443 (HTTPS)",
            "protocol": "HTTPS (TLS Termination via Ingress)",
            "ingress_route": "Cloudflare -> Ingress NGINX -> portainer:9000"
        },
        "k8s": {
            "namespace": "portainer",
            "workload_type": "Kubernetes Deployment",
            "replicas": "1/1 Ready",
            "nodes": "nigiri-vps",
            "database": "Portainer BoltDB (PersistentVolumeClaim)",
            "storage": "PVC (portainer-data)",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/portainer/"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OAuth2 / OIDC)",
            "realm": "master",
            "client_id": "portainer",
            "auth_flow": "OAuth2 SSO",
            "allowed_roles": ["admin"]
        },
        "topology": [
            {"step": "1. 管理者アクセス", "from": "Admin Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "manage.nigiri-rice.com"},
            {"step": "2. Ingress ルーティング", "from": "Cloudflare Edge", "to": "Ingress NGINX", "protocol": "HTTPS :443", "note": "TLS 終端 & プロキシ"},
            {"step": "3. Pod 転送", "from": "Ingress NGINX", "to": "portainer Pod", "protocol": "HTTP :9000", "note": "クラスター内部通信"},
            {"step": "4. K8s API 監視", "from": "portainer", "to": "Kubernetes API", "protocol": "HTTPS :6443", "note": "クラスター制御 & リソース監視"},
            {"step": "5. 認証連携", "from": "portainer", "to": "Keycloak SSO", "protocol": "OAuth2 / OIDC", "note": "SSO ログイン"}
        ],
        "mermaid": """graph TD
    Admin["Admin Browser"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Ingress["Ingress NGINX"]
    Ingress -->|HTTP:9000| Portainer["Portainer Pod (portainer ns)"]
    Portainer -->|HTTPS:6443| K8s["Kubernetes API Server"]
    Portainer -->|OAuth2| Keycloak["Keycloak SSO"]""",
        "commands": [
            {"desc": "Portainer Pod ステータス確認", "cmd": "kubectl get pods -n portainer"},
            {"desc": "Portainer ログ確認", "cmd": "kubectl logs -n portainer -l app.kubernetes.io/name=portainer --tail 50"},
            {"desc": "Portainer 再起動", "cmd": "kubectl rollout restart deployment portainer -n portainer"}
        ]
    },
    "webmail": {
        "id": "webmail",
        "name": "Mailcow Webmail",
        "category": "コミュニケーション",
        "tag": "Email",
        "icon": "mail",
        "description": "独自ドメインメール送受信基盤・SOGo Webmail インターフェース。DKIM/SPF/DMARC 完備のメールサーバーです。",
        "status": "正常稼働中 (Docker Compose マルチコンテナ)",
        "status_color": "emerald",
        "public_url": "https://webmail.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "mailcow",
        "network": {
            "public_dns": "webmail.nigiri-rice.com / mail.nigiri-rice.com",
            "internal_dns": "127.0.0.1 (nigiri-vps)",
            "internal_port": "8443 (SOGo Web) / 25 (SMTP) / 993 (IMAPS)",
            "protocol": "HTTPS (TLS via Caddy) / SMTP / IMAP",
            "ingress_route": "Cloudflare -> Caddy (Host) -> 127.0.0.1:8443 (Webmail)"
        },
        "k8s": {
            "namespace": "Host Docker Compose (nigiri-vps)",
            "workload_type": "Docker Compose Stack (Mailcow)",
            "replicas": "Multi-container (Postfix, Dovecot, SOGo, Rspamd, ClamAV)",
            "nodes": "nigiri-vps (Host 210.131.211.17)",
            "database": "MariaDB (mailcow-dockerized)",
            "storage": "Local Volumes (vmail, crypt)",
            "gitops_repo": "N/A (Host /opt/mailcow-dockerized)",
            "manifest_path": "/opt/mailcow-dockerized/docker-compose.yml"
        },
        "auth": {
            "provider": "Mailcow Internal + OIDC Auth",
            "realm": "master",
            "client_id": "mailcow",
            "auth_flow": "IMAP / OIDC / Web SSO",
            "allowed_roles": ["Developer", "admin"]
        },
        "topology": [
            {"step": "1. Webmail アクセス", "from": "User Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "webmail.nigiri-rice.com"},
            {"step": "2. Caddy ルーティング", "from": "Cloudflare Edge", "to": "Caddy (Host)", "protocol": "HTTPS :443", "note": "nigiri-vps"},
            {"step": "3. SOGo UI 転送", "from": "Caddy", "to": "sogo-mailcow", "protocol": "HTTP :8443", "note": "SOGo Webmail コンテナ"},
            {"step": "4. メールプロトコル", "from": "Mail Clients", "to": "Postfix / Dovecot", "protocol": "SMTP:25 / IMAPS:993", "note": "メール送受信"},
            {"step": "5. スパム & セキュリティ", "from": "Postfix", "to": "Rspamd / ClamAV", "protocol": "Internal TCP", "note": "DKIM / SPF 署名 & ウイルス検査"},
            {"step": "6. メールボックス保存", "from": "Dovecot", "to": "vmail-volume", "protocol": "Storage IO", "note": "Maildir 暗号化ストレージ"}
        ],
        "mermaid": """graph TD
    Client["Browser / Mail Client"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (nigiri-vps)"]
    Caddy -->|HTTP:8443| SOGo["SOGo Webmail Container"]
    Client -->|SMTP:25 / 587| Postfix["Postfix SMTP"]
    Client -->|IMAPS:993| Dovecot["Dovecot IMAP"]
    Postfix -->|Scan| Rspamd["Rspamd & ClamAV"]
    Dovecot & Postfix -->|Storage| Vmail["vmail Storage Volume"]
    SOGo & Postfix -->|Auth| DB["MariaDB (Mailcow DB)"]""",
        "commands": [
            {"desc": "Mailcow 全コンテナステータス確認", "cmd": "cd /opt/mailcow-dockerized && docker compose ps"},
            {"desc": "Postfix 送信ログリアルタイム監視", "cmd": "cd /opt/mailcow-dockerized && docker compose logs -f --tail=50 postfix-mailcow"},
            {"desc": "Mailcow 再起動", "cmd": "cd /opt/mailcow-dockerized && docker compose restart"}
        ],
        "email_client_settings": {
            "incoming": {
                "protocol": "IMAP (推奨) / POP3",
                "server": "webmail.nigiri-rice.com",
                "alt_server": "mail.nigiri-rice.com",
                "imap_port": 993,
                "imap_security": "SSL / TLS",
                "pop_port": 995,
                "pop_security": "SSL / TLS",
                "auth_method": "通常のパスワード認証 (プレーン / 暗号化なしパスワード)",
                "username_hint": "完全なメールアドレス (例: user@nigiri-rice.com)"
            },
            "outgoing": {
                "protocol": "SMTP (Submission)",
                "server": "webmail.nigiri-rice.com",
                "alt_server": "mail.nigiri-rice.com",
                "port_starttls": 587,
                "security_starttls": "STARTTLS (推奨)",
                "port_ssl": 465,
                "security_ssl": "SSL / TLS",
                "auth_required": True,
                "auth_method": "通常のパスワード認証 (受信サーバーと同じアカウント情報を利用)",
                "username_hint": "完全なメールアドレス (例: user@nigiri-rice.com)"
            },
            "guides": [
                {
                    "client": "iPhone / iPad (iOS 標準メール)",
                    "icon": "smartphone",
                    "steps": [
                        "「設定」>「メール」>「アカウント」>「アカウントを追加」を開きます。",
                        "「その他」>「メールアカウントを追加」をタップします。",
                        "名前、メールアドレス（例: user@nigiri-rice.com）、パスワードを入力して「次へ」。",
                        "「IMAP」が選択されていることを確認します。",
                        "【受信メールサーバー】ホスト名: webmail.nigiri-rice.com、ユーザー名: 完全なメールアドレス、パスワードを入力。",
                        "【送信メールサーバー】ホスト名: webmail.nigiri-rice.com、ユーザー名・パスワード（必須）を入力して「保存」。"
                    ]
                },
                {
                    "client": "Thunderbird (Windows / Mac / Linux)",
                    "icon": "mail",
                    "steps": [
                        "「アカウント設定」>「アカウント操作」>「メールアカウントを追加」を開きます。",
                        "お名前、メールアドレス、パスワードを入力し「手動設定」をクリックします。",
                        "【受信】プロトコル: IMAP、ホスト名: webmail.nigiri-rice.com、ポート: 993、接続の保護: SSL/TLS、認証方式: 通常のパスワード認証。",
                        "【送信】ホスト名: webmail.nigiri-rice.com、ポート: 587 (または 465)、接続の保護: STARTTLS (または SSL/TLS)、認証方式: 通常のパスワード認証。",
                        "ユーザー名: 送受信ともに「完全なメールアドレス」を指定し、「再テスト」>「完了」をクリックします。"
                    ]
                },
                {
                    "client": "Microsoft Outlook",
                    "icon": "layout",
                    "steps": [
                        "「ファイル」>「アカウントの追加」を開きます。",
                        "メールアドレスを入力し、「詳細オプション」の「自分で自分のアカウントを手動で設定」にチェックを入れ「接続」。",
                        "アカウントの種類で「IMAP」を選択します。",
                        "【受信メール】サーバー: webmail.nigiri-rice.com、ポート: 993、暗号化方法: SSL/TLS。",
                        "【送信メール】サーバー: webmail.nigiri-rice.com、ポート: 587、暗号化方法: STARTTLS（または 465 / SSL/TLS）。",
                        "パスワードを入力して完了します。「送信サーバーに認証が必要」が有効になっていることを確認してください。"
                    ]
                },
                {
                    "client": "Android (Gmail アプリ等)",
                    "icon": "tablet",
                    "steps": [
                        "Gmail アプリのアイコン >「別のアカウントを追加」>「その他」を選択。",
                        "メールアドレスを入力し、「手動設定」>「個人用 (IMAP)」を選択。",
                        "アカウントのパスワードを入力します。",
                        "【受信サーバー設定】サーバー: webmail.nigiri-rice.com、ポート: 993、セキュリティの種類: SSL/TLS。",
                        "【送信サーバー設定】サーバー: webmail.nigiri-rice.com、ポート: 587、セキュリティの種類: STARTTLS (または 465 / SSL/TLS)。「ログインが必要」をオン。",
                        "同期頻度等を選択して完了します。"
                    ]
                },
                {
                    "client": "📎 メール添付ファイルシステム: 送信の脱PPAP・自動リンク化 (Thunderbird Filelink)",
                    "icon": "paperclip",
                    "steps": [
                        "【概要】メール本文に重いZipやファイルを直接添付せず、Nextcloud上のダウンロードURL（パスワード・期限付）へ自動変換します。",
                        "Thunderbird の「設定」>「編集」>「添付ファイル」タブを開きます。",
                        "「Filelink」セクションの「アドオンを探す」から『Filelink for Nextcloud』を追加します。",
                        "「アカウントの追加」をクリックし、サーバーURLに『https://fs.nigiri-rice.com』を設定、OmusuBIアカウントで認証します。",
                        "保存先フォルダに『/Public/MailAttachments』を指定し、「1MB以上の添付時に自動でリンク化を提案」を有効化します。",
                        "【効果】メール送信時にファイルを添付すると自動的に Nextcloud へアップロードされ、本文中にセキュアなダウンロードURLが挿入されます。"
                    ]
                },
                {
                    "client": "📥 メール添付ファイルシステム: 受信メールの添付リンク化 (脱PPAP受信)",
                    "icon": "inbox",
                    "steps": [
                        "【方式1: Nextcloud Mail アプリ（標準推奨）】Nextcloud (https://fs.nigiri-rice.com) の「Mail」アプリを開くと、受信メールの添付ファイル横に「Nextcloudに保存」ボタンが表示されます。ワンクリックで『/Public/MailInbound』に保存され、即座に共有リンクを発行可能です。",
                        "【方式2: サーバー側自動分離 (Mailcow/Postfix + Python)】Mailcow の受信パイプライン（Postfix Content Filter / Dovecot Sieve）で添付ファイルを自動抽出し、Nextcloud の『/srv/shares/public/MailInbound』へ格納の上、本文にダウンロードURLを追記して添付実体を削除する運用に対応しています。",
                        "【メリット】受信トレイの容量圧迫を95%削減し、マルウェア直接開封のリスクを完全に排除します。"
                    ]
                },
                {
                    "client": "📤 社外からの大容量受け取り: ファイルドロップ (File Drop)",
                    "icon": "upload-cloud",
                    "steps": [
                        "Nextcloud (https://fs.nigiri-rice.com) にログインし、『Public > MailDrop』フォルダを開きます。",
                        "右側の共有アイコンをクリックし、「リンクを共有」を作成します。",
                        "共有の権限設定で『アップロードのみ (ファイルドロップ)』を選択し、必要に応じてパスワードと有効期限（例: 14日）を設定します。",
                        "発行された共有リンクを相手にメール等で連絡します。",
                        "【相手の操作】相手はアカウント登録不要で、ブラウザからドラッグ＆ドロップするだけで数十GBのファイルを安全にアップロードできます（他人の提出ファイルは一切見えません）。"
                    ]
                }
            ],
            "notes": [
                "【重要】ユーザー名欄には、アカウントID単体（例: user）ではなく、ドメイン部を含む『完全なメールアドレス（例: user@nigiri-rice.com）』を必ず入力してください。",
                "ブラウザから直接送受信・管理を行いたい場合は、SOGo Webmail（https://webmail.nigiri-rice.com）または Nextcloud Mail（https://fs.nigiri-rice.com）から即座にご利用いただけます。",
                "【メール添付システム】脱PPAP（パスワード付きZip添付廃止）ガイドに完全対応。大容量添付の送信・受信用フォルダ（/Public/MailAttachments, /Public/MailInbound, /Public/MailDrop）が完備されています。",
                "パスワード変更や新規メールアカウントの発行は、Mailcow 管理コンソール（管理者権限）または管理者にお問い合わせください。"
            ]
        }
    },
    "outline": {
        "id": "outline",
        "name": "Outline Docs",
        "category": "ドキュメント",
        "tag": "Wiki (撤去済み)",
        "icon": "book-open",
        "description": "技術仕様書・ナレッジベース共有プラットフォーム（現在撤去済み。ドキュメントおよびナレッジはAffiNEおよびGitへ集約・移行）。",
        "status": "撤去済み (Decommissioned)",
        "status_color": "slate",
        "public_url": "https://docs.nigiri-rice.com (停止中)",
        "sso_enabled": False,
        "cred_keyword": "outline",
        "network": {
            "public_dns": "docs.nigiri-rice.com (DNS停止/アーカイブ)",
            "internal_dns": "N/A (撤去済み)",
            "internal_port": "N/A",
            "protocol": "N/A",
            "ingress_route": "N/A (撤去済み)"
        },
        "k8s": {
            "namespace": "N/A (撤去済み)",
            "workload_type": "None (Decommissioned)",
            "replicas": "0 Instance",
            "nodes": "N/A",
            "database": "アーカイブ退避済み",
            "storage": "S3 / MinIO (アーカイブ保管)",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "撤去済み"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (過去連携)",
            "realm": "master",
            "client_id": "outline",
            "auth_flow": "OIDC Authentication Flow (停止)",
            "allowed_roles": ["admin"]
        },
        "topology": [
            {"step": "状態", "from": "運用状態", "to": "撤去完了", "protocol": "N/A", "note": "AffiNE および Git 管理へナレッジ移行完了"}
        ],
        "mermaid": """graph TD
    Status["Outline Docs: 撤去済み (Decommissioned)"]
    Migrate["移行先: AffiNE / Git ナレッジベース"]
    Status -.->|移行| Migrate""",
        "commands": [
            {"desc": "namespace 確認 (撤去済み確認)", "cmd": "kubectl get ns | grep outline || echo 'Outline namespace not present'"}
        ]
    },
    "affine": {
        "id": "affine",
        "name": "AFFiNE Workspace",
        "category": "ナレッジベース",
        "tag": "Collab",
        "icon": "edit-3",
        "description": "ホワイトボード、ノート、プロジェクトタスク管理が一体となったオールインワン・ワークスペース。",
        "status": "正常稼働中 (Docker Container Port 8083)",
        "status_color": "emerald",
        "public_url": "https://affine.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "affine",
        "network": {
            "public_dns": "affine.nigiri-rice.com",
            "internal_dns": "127.0.0.1 (Host)",
            "internal_port": "8083 (HTTP)",
            "protocol": "HTTPS (TLS Termination via Caddy)",
            "ingress_route": "Cloudflare -> Caddy -> 127.0.0.1:8083"
        },
        "k8s": {
            "namespace": "Host Docker (nigiri-vps)",
            "workload_type": "Docker Compose Stack",
            "replicas": "1 Instance",
            "nodes": "nigiri-vps",
            "database": "PostgreSQL 16 + Redis",
            "storage": "Local Docker Volume",
            "gitops_repo": "N/A (Host Docker 管理)",
            "manifest_path": "/opt/affine/docker-compose.yml"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC / OAuth2)",
            "realm": "master",
            "client_id": "affine",
            "auth_flow": "OIDC Code Flow",
            "allowed_roles": ["Developer", "admin"]
        },
        "topology": [
            {"step": "1. ワークスペース接続", "from": "User Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "affine.nigiri-rice.com"},
            {"step": "2. プロキシ転送", "from": "Cloudflare Edge", "to": "Caddy (Host)", "protocol": "HTTPS :443", "note": "TLS 終端"},
            {"step": "3. AFFiNE サーバー", "from": "Caddy", "to": "AFFiNE Server", "protocol": "HTTP :8083", "note": "CRDT リアルタイム同期エンジン"},
            {"step": "4. データベース", "from": "AFFiNE", "to": "PostgreSQL & Redis", "protocol": "TCP :5432 / :6379", "note": "ブロックデータ & キャッシュ"}
        ],
        "mermaid": """graph TD
    User["User Browser"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (nigiri-vps)"]
    Caddy -->|HTTP:8083| Affine["AFFiNE Server (Docker)"]
    Affine -->|OIDC Auth| Keycloak["Keycloak SSO"]
    Affine -->|TCP:5432| DB["PostgreSQL 16"]
    Affine -->|TCP:6379| Redis["Redis Cache"]""",
        "commands": [
            {"desc": "AFFiNE コンテナステータス確認", "cmd": "docker ps --filter name=affine"},
            {"desc": "AFFiNE ログ監視", "cmd": "docker logs -f --tail=50 affine"}
        ]
    },
    "cnt_prod": {
        "id": "cnt_prod",
        "name": "CNT Connect (本番)",
        "category": "プロダクト",
        "tag": "Production",
        "icon": "globe",
        "description": "CNT Connect プラットフォーム 本番サービス環境。高信頼な本番トラフィックを処理します。",
        "status": "正常稼働中 (K8s Namespace: cnt-connect-prod)",
        "status_color": "emerald",
        "public_url": "https://cnt-connect.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "cnt",
        "network": {
            "public_dns": "cnt-connect.nigiri-rice.com",
            "internal_dns": "cnt-connect-prod.cnt-connect-prod.svc.cluster.local",
            "internal_port": "80 / 8080",
            "protocol": "HTTPS (TLS via Caddy)",
            "ingress_route": "Cloudflare -> Caddy -> Ingress-NGINX (NodePort 30180) -> cnt-connect-prod:80"
        },
        "k8s": {
            "namespace": "cnt-connect-prod",
            "workload_type": "Deployment / Service",
            "replicas": "2 Pods (冗長化)",
            "nodes": "vps-worker-01, vps-worker-02, vps-worker-04",
            "database": "MySQL / PostgreSQL",
            "storage": "PVC Persistent Storage",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/cnt-connect-prod/"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC)",
            "realm": "master",
            "client_id": "cnt-connect",
            "auth_flow": "OAuth2 / OIDC",
            "allowed_roles": ["Developer", "admin", "User"]
        },
        "topology": [
            {"step": "1. ユーザーアクセス", "from": "End Users", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "cnt-connect.nigiri-rice.com"},
            {"step": "2. Caddy ルーティング", "from": "Cloudflare Edge", "to": "Caddy (Host)", "protocol": "HTTPS :443", "note": "TLS 終端"},
            {"step": "3. クラスタ Ingress", "from": "Caddy", "to": "Ingress-NGINX", "protocol": "HTTP :30180", "note": "NodePort 転送"},
            {"step": "4. 本番 App Pods", "from": "Ingress-NGINX", "to": "cnt-connect-prod Pods", "protocol": "HTTP :8080", "note": "HA 2 Pods 負荷分散"},
            {"step": "5. DB クエリ", "from": "cnt-connect-prod", "to": "Database Pods", "protocol": "TCP :3306 / :5432", "note": "本番データ永続化"}
        ],
        "mermaid": """graph TD
    Users["Public End Users"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (nigiri-vps)"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX (HA)"]
    Ing -->|HTTP| Svc["Service: cnt-connect-prod"]
    Svc --> Pod1["cnt-prod-pod-1 (Worker-01)"]
    Svc --> Pod2["cnt-prod-pod-2 (Worker-04)"]
    Pod1 & Pod2 -->|OIDC| Keycloak["Keycloak SSO"]
    Pod1 & Pod2 -->|DB| DB["Database Cluster"]""",
        "commands": [
            {"desc": "CNT Connect 本番 Pods 確認", "cmd": "kubectl get pods -n cnt-connect-prod -o wide"},
            {"desc": "CNT Connect 本番ログリアルタイム監視", "cmd": "kubectl logs -n cnt-connect-prod -l app=cnt-connect --tail=50 -f"},
            {"desc": "本番デプロイのロールアウト状況", "cmd": "kubectl rollout status deploy -n cnt-connect-prod"}
        ]
    },
    "cnt_dev": {
        "id": "cnt_dev",
        "name": "CNT Connect (開発)",
        "category": "プロダクト",
        "tag": "Development",
        "icon": "terminal",
        "description": "CNT Connect プラットフォーム 開発・ステージング環境。新機能やアップデートの事前検証環境です。",
        "status": "正常稼働中 (K8s Namespace: cnt-connect-dev)",
        "status_color": "emerald",
        "public_url": "https://dev.cnt-connect.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "cnt",
        "network": {
            "public_dns": "dev.cnt-connect.nigiri-rice.com",
            "internal_dns": "cnt-connect-dev.cnt-connect-dev.svc.cluster.local",
            "internal_port": "80 / 8080",
            "protocol": "HTTPS (TLS via Caddy)",
            "ingress_route": "Cloudflare -> Caddy -> Ingress-NGINX (NodePort 30180) -> cnt-connect-dev:80"
        },
        "k8s": {
            "namespace": "cnt-connect-dev",
            "workload_type": "Deployment / Service",
            "replicas": "1 Pod (開発用)",
            "nodes": "vps-worker-02",
            "database": "MySQL / PostgreSQL (Dev DB)",
            "storage": "PVC Persistent Storage",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/cnt-connect-dev/"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC)",
            "realm": "master",
            "client_id": "cnt-connect-dev",
            "auth_flow": "OAuth2 / OIDC",
            "allowed_roles": ["Developer", "admin"]
        },
        "topology": [
            {"step": "1. 開発者アクセス", "from": "Developer Browser", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "dev.cnt-connect.nigiri-rice.com"},
            {"step": "2. Caddy ルーティング", "from": "Cloudflare Edge", "to": "Caddy (Host)", "protocol": "HTTPS :443", "note": "TLS 終端"},
            {"step": "3. クラスタ Ingress", "from": "Caddy", "to": "Ingress-NGINX", "protocol": "HTTP :30180", "note": "NodePort 転送"},
            {"step": "4. 開発 Pod", "from": "Ingress-NGINX", "to": "cnt-connect-dev Pod", "protocol": "HTTP :8080", "note": "vps-worker-02"},
            {"step": "5. 開発 DB", "from": "cnt-connect-dev", "to": "Dev Database Pod", "protocol": "TCP :3306", "note": "検証用データベース"}
        ],
        "mermaid": """graph TD
    Dev["Developer Browser"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (nigiri-vps)"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX"]
    Ing -->|HTTP| Svc["Service: cnt-connect-dev"]
    Svc --> Pod["cnt-dev-pod (Worker-02)"]
    Pod -->|OIDC Auth| Keycloak["Keycloak SSO"]
    Pod -->|DB:3306| DB["cnt-connect-dev-db"]""",
        "commands": [
            {"desc": "開発環境 Pods 確認", "cmd": "kubectl get pods -n cnt-connect-dev -o wide"},
            {"desc": "開発環境ログリアルタイム監視", "cmd": "kubectl logs -n cnt-connect-dev -l app=cnt-connect-dev --tail=50 -f"}
        ]
    },
    "wordpress": {
        "id": "wordpress",
        "name": "WordPress (公式サイト)",
        "category": "Webサイト",
        "tag": "CMS",
        "icon": "layout",
        "description": "nigiri-rice.com 公式ホームページ。会社概要、ニュース、サービス紹介を掲載しています。",
        "status": "正常稼働中 (K8s Namespace: nigiri-homepage)",
        "status_color": "emerald",
        "public_url": "https://www.nigiri-rice.com",
        "sso_enabled": False,
        "cred_keyword": "wordpress",
        "network": {
            "public_dns": "www.nigiri-rice.com / nigiri-rice.com",
            "internal_dns": "wordpress.nigiri-homepage.svc.cluster.local",
            "internal_port": "80 (HTTP)",
            "protocol": "HTTPS (TLS via Caddy)",
            "ingress_route": "Cloudflare -> Caddy -> Ingress-NGINX (NodePort 30180) -> wordpress:80"
        },
        "k8s": {
            "namespace": "nigiri-homepage",
            "workload_type": "Deployment (wordpress)",
            "replicas": "1 Pod",
            "nodes": "nigiri-vps (Host Control Plane)",
            "database": "MariaDB (mariadb.nigiri-homepage.svc:3306)",
            "storage": "Local PV (wp-content / uploads)",
            "gitops_repo": "https://github.com/nigiri-rice-com/k8s-cluster-yaml.git",
            "manifest_path": "clusters/vps/workloads/nigiri-homepage/"
        },
        "auth": {
            "provider": "WordPress Native Auth",
            "realm": "N/A",
            "client_id": "wp-admin",
            "auth_flow": "Cookie Auth",
            "allowed_roles": ["Administrator", "Editor"]
        },
        "topology": [
            {"step": "1. 一般アクセス", "from": "Public Visitors", "to": "Cloudflare Edge", "protocol": "HTTPS :443", "note": "www.nigiri-rice.com (WAF & CDN)"},
            {"step": "2. Caddy ルーティング", "from": "Cloudflare Edge", "to": "Caddy (Host)", "protocol": "HTTPS :443", "note": "TLS 終端 & /portal 等のルーティング分岐"},
            {"step": "3. クラスタ Ingress", "from": "Caddy", "to": "Ingress-NGINX", "protocol": "HTTP :30180", "note": "NodePort 転送"},
            {"step": "4. WordPress Pod", "from": "Ingress-NGINX", "to": "wordpress Pod", "protocol": "HTTP :80", "note": "Apache + PHP 8.x"},
            {"step": "5. DB クエリ", "from": "wordpress", "to": "mariadb Pod", "protocol": "TCP :3306", "note": "MariaDB 10.x (Local PV)"}
        ],
        "mermaid": """graph TD
    Public["Public Visitors"] -->|HTTPS:443| CF["Cloudflare Edge"]
    CF -->|TLS:443| Caddy["Caddy (nigiri-vps)"]
    Caddy -->|NodePort:30180| Ing["Ingress-NGINX"]
    Ing -->|HTTP:80| WP["WordPress Pod (nigiri-homepage)"]
    WP -->|TCP:3306| DB["MariaDB Pod (nigiri-homepage)"]
    WP -->|Storage| PV["Local PV (wp-content)"]""",
        "commands": [
            {"desc": "WordPress & DB Pod 確認", "cmd": "kubectl get pods -n nigiri-homepage -o wide"},
            {"desc": "WordPress Apache ログ確認", "cmd": "kubectl logs -n nigiri-homepage -l app=wordpress --tail=50"},
            {"desc": "WordPress 再起動", "cmd": "kubectl rollout restart deploy -n nigiri-homepage wordpress"}
        ]
    },
    "fs": {
        "id": "fs",
        "name": "Nextcloud Hub & Samba 4 AD",
        "category": "ストレージ / ID管理",
        "tag": "Nextcloud & AD",
        "icon": "cloud",
        "description": "Nextcloud Hub (v35) ＆ Samba 4 AD DC 統合クラウドストレージ基盤（軽量 Cloudreve への段階移行対応）。iOS / Android 公式アプリ、iOS「ファイル」アプリ統合、Windows / Mac (SMB / \\\\10.155.0.144\\public)、WebUI (https://fs.nigiri-rice.com) から全方位シームレスに操作可能。ユーザー個別領域は作成せず、単一共通共有ストレージ（Public）を一元運用。Samba 4 AD DC (nigiri-rice ドメイン) & OmusuBI SSO 認証対応。",
        "status": "正常稼働中 (CT 144: fs-ad-server / Nextcloud Hub + Samba 4 AD DC + MariaDB + Redis)",
        "status_color": "emerald",
        "public_url": "https://fs.nigiri-rice.com",
        "sso_enabled": True,
        "cred_keyword": "fs",
        "network": {
            "public_dns": "fs.nigiri-rice.com (Cloudflare Direct A Record / Caddy TLS 終端 / 100MB制限なし)",
            "internal_dns": "ad.nigiri-rice.com (10.155.0.144)",
            "internal_port": "8080 (Nextcloud Nginx) / 5212 (Cloudreve) / 445 (SMB) / 139 (NetBIOS) / 21 (FTP) / 389 (LDAP) / 636 (LDAPS)",
            "protocol": "HTTPS (WebUI & WebDAV) / SMB 3.1.1 (PC共有) / vsftpd (FTP) / Kerberos & LDAP",
            "ingress_route": "Web & スマホ: リモート/社内 -> Cloudflare DNS -> VPS Caddy (fs.nigiri-rice.com) -> Tailscale -> CT 144:8080 (Cloudreve移行時は5212)\nPCマウント: リモート/社内 -> Tailscale VPN (10.155.0.0/24) -> SMB (\\\\10.155.0.144\\public) -> CT 144:445"
        },
        "k8s": {
            "namespace": "On-Premises Proxmox VE (CT 144)",
            "workload_type": "Proxmox Privileged LXC (Debian 12 Bookworm)",
            "replicas": "1 Node (2 vCPU / 2GB RAM / 40GB Storage / ZFS local-lvm)",
            "nodes": "PVE Host (10.155.0.10) -> CT 144: fs-ad-server (10.155.0.144)",
            "database": "MariaDB 10.11 (nextcloud) / Redis 7.0 (Cache & Locking) / Samba 4 LDB",
            "storage": "ZFS Pool: /srv/shares/public (共通共有マウント /Public), /var/nextcloud_data",
            "gitops_repo": "N/A (Systemd Daemon Managed + Automated Provisioning Script)",
            "manifest_path": "/etc/nginx/sites-available/nextcloud.conf, /var/www/nextcloud/config/config.php, /etc/samba/smb.conf"
        },
        "auth": {
            "provider": "OmusuBI Keycloak (OIDC SSO) ＆ Samba 4 AD DC (user_ldap)",
            "realm": "master (OmusuBI SSO) / AD.NIGIRI-RICE.COM (Kerberos REALM / Workgroup: NIGIRI-RICE)",
            "client_id": "nextcloud (OIDC Client) / Samba 4 AD user_ldap",
            "auth_flow": "OmusuBI SSO (user_oidc 1クリックログイン) + 5分毎Samba ADプロビジョニング",
            "allowed_roles": ["admin", "Developer", "Users"],
            "admin_role_mapping": "Keycloak 'admin' ロール保持者を Nextcloud 'admin' グループ（管理者権限）および Samba 'Domain Admins' へ自動マッピング"
        },
        "topology": [
            {"step": "1. Web / モバイルアクセス", "from": "iOS / Android / Web", "to": "VPS Caddy", "protocol": "HTTPS :443", "note": "fs.nigiri-rice.com (公式Nextcloudアプリ & WebUI / リモート直通)"},
            {"step": "2. リバースプロキシ転送", "from": "VPS Caddy", "to": "Nextcloud (CT 144)", "protocol": "HTTP :8080", "note": "Tailscale メッシュ経由で 10.155.0.144:8080 へ安全に転送"},
            {"step": "3. OIDC SSO 認証", "from": "Nextcloud (user_oidc)", "to": "Keycloak SSO", "protocol": "OIDC Authorization Code", "note": "sso.nigiri-rice.com (Adminロール保持者に管理者権限自動付与)"},
            {"step": "4. PCマウント", "from": "Windows / Mac PC (Tailscale)", "to": "Samba AD DC (CT 144)", "protocol": "SMB :445", "note": "\\\\10.155.0.144\\public (ADドメイン認証: nigiri-rice\\<user>)"},
            {"step": "5. 双方向リアルタイム同期", "from": "SMB & Nextcloud", "to": "/srv/shares/public", "protocol": "POSIX ACL / inotifywait", "note": "Windows側変更を inotify が検知し Nextcloud へ即時インデックス"},
            {"step": "6. メール添付ファイル連携", "from": "Thunderbird / Outlook / Mail", "to": "Nextcloud Hub", "protocol": "WebDAV / Filelink", "note": "大容量添付の自動リンク化（脱PPAP）・受信用ファイルドロップ"}
        ],
        "mermaid": """graph TD
    UserApp["Nextcloud 公式アプリ (iOS / Android)"] -->|"HTTPS:443"| Caddy["VPS Caddy (fs.nigiri-rice.com)"]
    UserWeb["Web ブラウザ (PC / スマホ / リモート)"] -->|"HTTPS:443"| Caddy
    MailClient["メールソフト (Thunderbird / Outlook)"] -->|"添付ファイルリンク化 (Filelink)"| Caddy
    Caddy -->|"Tailscale HTTP:8080"| NC["Nextcloud Hub v35 (Nginx + PHP 8.3-FPM)"]
    UserPC["Windows / Mac (Tailscale経由)"] -->|"SMB:445"| Samba["Samba 4 AD DC (Domain: nigiri-rice)"]
    
    subgraph CT144 ["CT 144: fs-ad-server (10.155.0.144)"]
        NC -->|"Local Mount /Public"| Storage["単一共通共有ストレージ: /srv/shares/public"]
        Samba -->|"SMB 共有"| Storage
        
        Watch["inotifywait Watcher (nextcloud-smb-watch)"] -.->|"リアルタイム変更検知"| Storage
        Watch -->|"occ files:scan 即時インデックス"| NC
        
        SambaAD["Samba 4 AD DC (127.0.0.1:389)"] -->|"user_ldap"| NC
        MariaDB["MariaDB 10.11"] --- NC
        Redis["Redis 7.0 (Cache & Locking)"] --- NC
    end
    
    Keycloak["OmusuBI Keycloak (sso.nigiri-rice.com)"] -->|"OIDC SSO (Adminロール自動昇格)"| NC
    Keycloak -->|"LDAP / REST API (5分毎同期)"| SambaAD
    Mailcow["Mailcow Webmail (webmail.nigiri-rice.com)"] -->|"Nextcloud Mail App (IMAP/SMTP)"| NC""",
        "commands": [
            {"desc": "OmusuBI OIDC SSO 直接ログイン URL", "cmd": "https://fs.nigiri-rice.com/apps/user_oidc/login/1"},
            {"desc": "Windows PC からの SMB 接続 (コマンドプロンプト/PowerShell)", "cmd": "net use \\\\10.155.0.144\\public /user:nigiri-rice\\i.shimamoto <SSOパスワード>"},
            {"desc": "iOS / Android 公式アプリ接続先 URL", "cmd": "https://fs.nigiri-rice.com"},
            {"desc": "CT 144 へ SSH ログイン", "cmd": "ssh root@10.155.0.144"},
            {"desc": "Nextcloud OIDC Admin ロール権限マッピング設定", "cmd": "sudo -u www-data php /var/www/nextcloud/occ user_oidc:provider:update 1 --mapping-groups=groups --group-mapping='{\"admin\": \"admin\", \"Admin\": \"admin\"}'"},
            {"desc": "ユーザー手動管理者権限付与 (即時反映)", "cmd": "sudo -u www-data php /var/www/nextcloud/occ group:adduser admin <ユーザー名>"},
            {"desc": "Nextcloud システムステータス確認", "cmd": "sudo -u www-data php /var/www/nextcloud/occ status"},
            {"desc": "Nextcloud 全ファイルスキャン手動実行", "cmd": "sudo -u www-data php /var/www/nextcloud/occ files:scan --all"},
            {"desc": "SMB ファイル監視リアルタイム同期デーモン確認", "cmd": "systemctl status nextcloud-smb-watch.service"},
            {"desc": "Samba 4 AD DC サービス稼働状態確認", "cmd": "systemctl status samba-ad-dc"}
        ]
    }
}

def get_service_detail(service_id: str) -> Optional[Dict[str, Any]]:
    aliases = {
        "mailcow": "webmail",
        "mail": "webmail",
    }
    target_id = aliases.get(service_id, service_id)
    return SERVICES_DATA.get(target_id)

for s in SERVICES_DATA.values():
    if "url" not in s:
        s["url"] = s["public_url"]

def get_all_services_list() -> List[Dict[str, Any]]:
    return list(SERVICES_DATA.values())

OVERALL_MERMAID = """graph TB
    subgraph Clients ["クライアント & 外部アクセス"]
        User["一般ユーザー / 業務端末"]
        Dev["開発者 / システム管理者"]
    end

    subgraph Cloudflare ["Cloudflare Edge Network"]
        CF_DNS["Cloudflare DNS<br/>(Proxy: Proxied)"]
        CF_WAF["Cloudflare WAF / DDoS 防護<br/>(SSL/TLS Strict 暗号化)"]
        CF_Tunnel["Cloudflare Tunnel<br/>(argocd.nigiri-rice.com)"]
        CF_DNS --> CF_WAF
    end

    subgraph VPS ["Xserver VPS (210.131.211.17) - Ubuntu 24.04.4 LTS"]
        Caddy["Caddy v2<br/>Edge Reverse Proxy (Port 80, 443)"]
        
        subgraph K3s_Cluster ["k3s Kubernetes クラスタ (v1.36.4+k3s1)"]
            Node_Master["Control Plane: nigiri-vps (Host)"]
            Node_W1["Worker 01<br/>vps-worker-01 (172.30.0.2)"]
            Node_W2["Worker 02<br/>vps-worker-02 (172.30.0.3)"]
            Node_W3["Worker 03<br/>vps-worker-03 (172.30.0.4)"]
            Node_W4["Worker 04<br/>vps-worker-04 (172.30.0.5)"]
            Ingress_Nginx["Ingress-NGINX (NodePort 30180)"]
            
            subgraph K8s_Workloads ["主要 K8s ワークロード (12 アプリケーション)"]
                SSO["Keycloak SSO<br/>(sso.nigiri-rice.com)"]
                Vault["HashiCorp Vault<br/>(vault.nigiri-rice.com)"]
                Console["OmusuBI Console<br/>(console.nigiri-rice.com)"]
                Harbor["Harbor Registry<br/>(registry.nigiri-rice.com)"]
                CNT_Prod["CNT Connect Prod<br/>(cnt-connect.nigiri-rice.com)"]
                CNT_Dev["CNT Connect Dev<br/>(dev.cnt-connect.nigiri-rice.com)"]
                WP["WordPress<br/>(www.nigiri-rice.com)"]
                Portal["Developer Portal<br/>(www.nigiri-rice.com/portal/)"]
            end
        end

        subgraph Docker_Standalone ["VPS 独立 Docker サービス"]
            Mailcow["Mailcow-dockerized<br/>mail.nigiri-rice.com<br/>(SMTP:25,587, IMAP:993, Web:8448)"]
            AFFiNE["AFFiNE Knowledge Base<br/>affine.nigiri-rice.com (Port 8083)"]
            Portainer_Host["Portainer Server<br/>manage.nigiri-rice.com:8082"]
            Monitoring["Prometheus / cAdvisor<br/>Node Exporter"]
            Shumoku["Shumoku Discord Bot<br/>(Node.js)"]
        end
    end

    subgraph Home_Environment ["オンプレミス 宅内インフラ基盤 (ドコモ光 10ギガ / GMOとくとくBB)"]
        subgraph Home_Network_10G ["物理光回線 & 宅内ネットワーク (10Gbps WAN / 10G LAN)"]
            Docomo10G["ドコモ光 10ギガ<br/>GMOとくとくBB v6プラス<br/>(IPoE / IPv4 over IPv6)"]
            ONU_10G["NTT 10G 光回線終端装置<br/>(10G-EPON ONU)"]
            Router_TP["TP-Link 10G ルーター<br/>(10.155.0.1 / WAN 10G SFP+, LAN 10G/2.5G)"]
            Switch_LAN["宅内 スイッチングハブ<br/>(10.155.0.0/16)"]

            Docomo10G -->|10Gbps 光ファイバー| ONU_10G
            ONU_10G -->|10GBASE-T WAN| Router_TP
            Router_TP -->|10G/2.5G LAN| Switch_LAN
        end

        subgraph PVE_Cluster ["Proxmox VE 8.x 物理ホスト (10.155.0.10 - Ryzen 8C/16T, 32GB RAM, ZFS)"]
            GPU_Hardware["NVIDIA GeForce RTX 2060 Mobile<br/>(TU106M / 6GB VRAM, IOMMU Group 8)"]

            subgraph PVE_Infra_Guests ["基幹 VM / 管理 LXC コンテナ群 (10.155.0.0/16)"]
                CT_Proxy["CT 121: reverse-proxy (Caddy v2)<br/>(*.home.nigiri-rice.com / SSL自動証明書)"]
                CT_Portal131["CT 131: aaa-portal (React Dashboard)<br/>(portal.home.nigiri-rice.com)"]
                CT_HomePortal["CT 132: home-portal (Django 機器/発電監視)<br/>(homeportal.home.nigiri-rice.com)"]
                CT_VPN["CT 150: tailscale-vpn (Subnet Router)<br/>(宅内メッシュ直結 10.155.0.0/16)"]
                CT_FS_AD["CT 144: fs-ad-server (10.155.0.144)<br/>(Nextcloud Hub v35 / Samba 4 AD DC: fs.nigiri-rice.com)"]
            end

            subgraph PVE_K8s_Cluster ["PVE 宅内 Kubernetes クラスタ (k3s v1.36.4 - 8ノード構成)"]
                subgraph K8s_CP_Group ["Control Plane (3ノード etcd HA クラスタ)"]
                    CP01["CT 200: k8s-cp-01<br/>(10.155.200.201 / Leader)"]
                    CP02["CT 211: k8s-cp-02<br/>(10.155.200.202 / etcd)"]
                    CP03["CT 212: k8s-cp-03<br/>(10.155.200.203 / etcd)"]
                end

                subgraph K8s_Worker_Group ["Worker ノード (5ノード)"]
                    W_GPU["VM 201: k8s-worker-gpu-01<br/>(10.155.200.204 / GPU Worker)"]
                    W02["CT 202: k8s-worker-02 (10.155.200.205)"]
                    W03["CT 203: k8s-worker-03 (10.155.200.206)"]
                    W04["CT 204: k8s-worker-04 (10.155.200.207)"]
                    W05["CT 205: k8s-worker-05 (10.155.200.208)"]
                end

                subgraph K8s_Home_Workloads ["主要 K8s アプリケーション & ストレージ"]
                    PVE_Ingress["Ingress-NGINX<br/>(NodePort 30180 / 30444)"]
                    PVE_ArgoCD["Argo CD (GitOps 運用自動化)<br/>(argocd.home.nigiri-rice.com)"]
                    PVE_Jupyter["JupyterHub (GPU AI開発環境)<br/>(jupyterhub.home.nigiri-rice.com)"]
                    PVE_Harbor["Harbor (コンテナレジストリ)<br/>(registry.home.nigiri-rice.com)"]
                    PVE_SMB["SMB CSI Storage<br/>(TrueNAS / SMB 永続PVマウント)"]
                end
            end

            GPU_Hardware -.->|PCI Passthrough| W_GPU
            CT_Proxy -->|NodePort 30180| PVE_Ingress
            PVE_Ingress --> PVE_ArgoCD & PVE_Jupyter & PVE_Harbor
        end

        Switch_LAN -->|10G/2.5G 物理リンク| PVE_Cluster
    end

    User --> CF_DNS
    CF_WAF --> Caddy
    Dev --> CF_Tunnel --> Node_Master
    Caddy --> Ingress_Nginx
    Caddy --> Mailcow
    Caddy --> AFFiNE
    Caddy --> Portainer_Host
    Caddy -->|"Tailscale HTTP:8080 (fs.nigiri-rice.com)"| CT_FS_AD
    Ingress_Nginx --> Node_W1 & Node_W2 & Node_W3 & Node_W4
    
    CT_VPN <-->|"Tailscale Mesh VPN 暗号化トンネル (宅内ポート開放不要・メッシュ直結)"| Caddy
    Dev -.->|"Tailscale VPN 経由 / RDP・SSH・SMB:445"| CT_FS_AD
    Dev -.->|"Tailscale VPN 経由 / RDP・SSH"| Router_TP"""
