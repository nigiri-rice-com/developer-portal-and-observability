# -*- coding: utf-8 -*-
"""
Documentation Database & Architecture Manuals for Nigiri Developer Portal
Modeled after GitHub Docs (https://docs.github.com/ja)
Compliant with the Qiita 7-Document Standards (https://qiita.com/komeri/items/0bff68f873ea614b716f)
Updated: 2026-09-18 (v1.7.0)
"""

from typing import Dict, List, Any, Optional

CATEGORIES = [ { 'description': 'Qiita準拠の7つの必須ドキュメント基準、システム全体インベントリ、日常巡回、定期保守、障害対応の包括的ガイドラインです。',
    'icon': 'book-open',
    'id': 'guidelines',
    'title': '設計標準 & 運用ガイドライン'},
  { 'description': 'Keycloak SSO、OmusuBI Console、HashiCorp Vault によるセキュアなID管理・資格情報共有・認可基盤です。',
    'icon': 'shield-check',
    'id': 'identity',
    'title': '認証 & ID 基盤'},
  { 'description': 'Cloudflare エッジ、Caddy リバースプロキシ、Ingress-NGINX、Argo CD トンネルによるセキュアルーティング基盤です。',
    'icon': 'globe',
    'id': 'network',
    'title': 'エッジ & ネットワーク'},
  { 'description': 'Harbor コンテナレジストリおよび CIFS/SMB CSI ストレージドライバの運用手順と構成仕様です。',
    'icon': 'database',
    'id': 'storage',
    'title': 'ストレージ & レジストリ'},
  { 'description': 'CNT Connect（本番・開発）、WordPress コーポレートサイト、Developer Portal の設計と運用保守仕様です。',
    'icon': 'layers',
    'id': 'apps',
    'title': '業務アプリケーション'},
  { 'description': 'Mailcow メールサーバー、AFFiNE ナレッジベース、Portainer、監視基盤、Discord Bot の独立サービス群です。',
    'icon': 'mail',
    'id': 'standalone',
    'title': 'メール & 独立サービス'},
  { 'description': 'Xserver VPS（k3s Control Plane & Workers）およびオンプレミス Proxmox VE（PVE / AD）の基盤マニュアルです。',
    'icon': 'server',
    'id': 'infrastructure',
    'title': 'インフラホスト基盤'}]

DOCS = {
  'fs-storage': {
    'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-24', 'SSO Admin権限自動付与', 'OSS公開リポジトリあり', 'Samba 4 AD (NIGIRI)'],
    'category_id': 'storage',
    'category_name': 'ストレージ & レジストリ',
    'content_html': '\n<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n  Nextcloud Hub (v35) と Samba 4 Active Directory DC を統合した、次世代エンタープライズ・クラウドストレージ基盤。<br>\n  さらに今後の運用負荷軽減のため、超軽量 Go 製ストレージ「Cloudreve」への段階移行に対応しています。<br>\n  iOS / Android の公式アプリに標準対応し、Windows / Mac からの SMB ダイレクトマウント（<code>\\\\10.155.0.144\\public</code>）および WebUI（<code>https://fs.nigiri-rice.com</code>）から全方位でシームレスに操作可能です。<br>\n  個人個別フォルダは作成せず、全員が1つの共通共有ストレージ（<code>/Public</code>）を一元利用するシンプルかつ実用的な設計を採用しています。\n</p>\n\n<div class="gh-alert gh-alert-tip mb-6">\n  <div class="gh-alert-title"><i data-lucide="github" class="w-4 h-4 shrink-0"></i><span>オープンソース公開情報 & 開発記録</span></div>\n  <div class="gh-alert-body">\n    本アーキテクチャの完全な設定テンプレートと同期スクリプトは GitHub にて OSS (MIT License) として公開されています。<br>\n    ・<strong>GitHub リポジトリ:</strong> <a href="https://github.com/nigiri-rice-com/hybrid-cloud-storage" target="_blank" class="underline text-emerald-600 dark:text-emerald-400 font-semibold">nigiri-rice-com/hybrid-cloud-storage</a><br>\n    ・<strong>公式開発記録記事:</strong> <a href="https://www.nigiri-rice.com/2026/09/24/hybrid-cloud-storage-architecture/" target="_blank" class="underline text-emerald-600 dark:text-emerald-400 font-semibold">設計と構築の技術詳細（WordPress）</a>\n  </div>\n</div>\n\n<div class="gh-alert gh-alert-note">\n  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n  <div class="gh-alert-body">本ページは Qiita 策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n</div>\n\n<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n<div class="space-y-4 mb-6">\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n  <p>Windows Server に依存しないオープンソースの Active Directory ドメインコントローラと、スマホ（iOS/Android）・PC（SMB）・ブラウザ（WebUI）の全デバイスから即時アクセス可能なクラウドストレージ基盤を構築すること。</p>\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>\n  <ul class="list-disc pl-6 space-y-1">\n    <li><strong>マルチクライアント対応:</strong> iOS「ファイル」アプリ、Android Nextcloud 公式アプリ、Windows PC SMB マウント、WebUI のすべてから同一共有フォルダを操作可能。</li>\n    <li><strong>単一共有ストレージ運用:</strong> ユーザー個別領域を作成せず、全ユーザーが共通共有ストレージ（<code>/srv/shares/public</code>）を閲覧・編集可能。</li>\n    <li><strong>SSO Admin 権限自動昇格:</strong> OmusuBI (Keycloak) で <code>admin</code> ロールを持つユーザーに対し、Nextcloud の <code>admin</code> グループ（全管理者権限）および Samba <code>Domain Admins</code> を自動付与。</li>\n    <li><strong>ドメイン名統一:</strong> Samba ドメイン名（Workgroup）を <code>nigiri-rice</code>（NetBIOS: <code>NIGIRI-RICE</code>）に設定し、SSO アカウントと完全同期。</li>\n    <li><strong>双方向リアルタイム同期:</strong> Windows SMB 側で変更されたファイルが <code>inotifywait</code> により 1 秒以内に Nextcloud にインデックス反映されること。</li>\n    <li><strong>ID プロビジョニング連携:</strong> OmusuBI (Keycloak) を Source of Truth とし、5分間隔で Samba 4 AD DC および Nextcloud にユーザー・グループが自動同期されること。</li>\n  </ul>\n</div>\n\n<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / レイヤー</th><th>採用技術 / バージョン</th><th>選定理由・メリット</th></tr></thead><tbody>\n<tr><td>クラウドストレージ (現行)</td><td>Nextcloud Hub v35 (Hub 10)</td><td>iOS / Android 公式アプリ対応、WebDAV、iOS「ファイル」アプリ統合、写真自動バックアップ</td></tr>\n<tr><td>クラウドストレージ (移行先)</td><td>Cloudreve v3.8+ (Go Binary)</td><td>超軽量（メモリ数十MB）、高速起動、React モダンWebUI、ローカルストレージ透過連携</td></tr>\n<tr><td>ディレクトリ & SMB</td><td>Samba 4.17+ AD DC (nigiri-rice)</td><td>Windows AD DS 互換ドメインコントローラ、Kerberos 認証、高速 SMB 3.1.1 共有</td></tr>\n<tr><td>Web サーバー</td><td>Nginx 1.22 + PHP 8.3-FPM</td><td>Nextcloud 最適化構成、大容量ファイル（16GB+）アップロード、HTTP/2 対応</td></tr>\n<tr><td>データベース</td><td>MariaDB 10.11 (InnoDB utf8mb4)</td><td>Nextcloud / Cloudreve ファイルメタデータ、権限、タグの高速トランザクション処理</td></tr>\n<tr><td>キャッシュ & ロック</td><td>Redis 7.0</td><td>セッションキャッシュおよび分散ファイルロック（Memcache & Locking）</td></tr>\n<tr><td>リアルタイム検知</td><td>inotify-tools (inotifywait)</td><td>SMB 経由のファイル追加・更新をカーネルレベルで即座に検知しストレージへ自動同期</td></tr>\n<tr><td>リバースプロキシ</td><td>Caddy v2 (VPS)</td><td>Let\'s Encrypt 自動 TLS 終端、Cloudflare プロキシバイパス（100MB制限回避）、WebDAV リダイレクト</td></tr>\n</tbody></table></div>\n\n<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n<div class="space-y-4 mb-6">\n  <p>Proxmox VE ホスト上の特権 LXC コンテナ <code>CT 144 (fs-ad-server)</code> 内の ZFS プール上にストレージが配置されています：</p>\n  <ul class="list-disc pl-6 space-y-1">\n    <li><strong>共通共有ストレージ:</strong> <code>/srv/shares/public</code> (POSIX ACL: <code>u:www-data:rwx,g:www-data:rwx,o:rwx</code>, default ACL 継承)</li>\n    <li><strong>Nextcloud マウント:</strong> <code>files_external</code> (Local) によりルート直下に <code>/Public</code> として自動マウント</li>\n    <li><strong>Cloudreve 連携パス:</strong> ストレージ保存ルールを <code>{path}/{filename}</code> とし、<code>/srv/shares/public</code> と直接同期</li>\n    <li><strong>個人クォータ制限:</strong> <code>default_quota => 0 B</code> に設定し、個人専用領域を使わせず共通ストレージへ誘導</li>\n    <li><strong>Samba 共有設定:</strong> <code>oplocks = no</code>, <code>level2 oplocks = no</code> により Windows キャッシュによる同期遅延を防止</li>\n  </ul>\n</div>\n\n<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様 (モバイル / PC / リモート接続 / SSO Admin)</h2>\n<div class="space-y-4 mb-6">\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">🌐 リモート環境からの 3 つの接続方法</h3>\n  <p>外出先・自宅・スマホなどリモート環境からファイルサーバーを利用する方法です：</p>\n  <ul class="list-disc pl-6 space-y-2 text-sm mb-4">\n    <li><strong>方式1: Web ブラウザ（VPN 不要・世界中から直接アクセス）</strong><br>\n      URL: <code>https://fs.nigiri-rice.com/</code><br>\n      OmusuBI SSO（Keycloak）でログイン。ファイルのドラッグ＆ドロップ、大容量アップロード、PDF・文書プレビュー、外部共有リンク発行が可能。</li>\n    <li><strong>方式2: スマホアプリ（iOS / Android）</strong><br>\n      「Nextcloud」公式アプリでサーバーアドレスに <code>https://fs.nigiri-rice.com</code> を設定。iOS 標準「ファイル」アプリ統合およびカメラロール自動写真バックアップが社外からそのまま動作します。</li>\n    <li><strong>方式3: リモート PC からのエクスプローラー SMB マウント（Tailscale VPN 経由）</strong><br>\n      SMB（Port 445）は安全のため Tailscale 暗号化トンネルを経由します。リモート端末で Tailscale にログインしていれば、社外でも社内 LAN と全く同様に以下の構文でマウント可能です。</li>\n  </ul>\n\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">🔑 OmusuBI SSO Admin ロール管理者権限マッピング</h3>\n  <p class="text-sm">Keycloak (OmusuBI SSO) において <code>admin</code> ロールを付与されているアカウントは、Nextcloud へ OIDC SSO ログインした際に自動的に Nextcloud の <code>admin</code> グループへマッピングされます。<br>\n  これにより、特別な管理者ログインURLや個別パスワードを使用せず、OmusuBI の SSO 認証のみで全管理機能（システム設定、ユーザー管理、アプリ管理）へアクセス可能になります。</p>\n\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">💻 Windows / Mac PC からの SMB マウント手順 (ドメイン: nigiri-rice)</h3>\n  <div class="code-block-wrapper">\n    <div class="code-header"><span class="code-lang">powershell</span></div>\n    <pre><code class="language-powershell"># Windows PowerShell / コマンドプロンプト\nnet use \\\\\\\\10.155.0.144\\\\public /user:nigiri-rice\\\\i.shimamoto <SSOパスワード></code></pre>\n  </div>\n  <p class="text-xs text-slate-500 mt-1">※ユーザー名は <code>nigiri-rice\\&lt;ユーザー名&gt;</code> または <code>&lt;ユーザー名&gt;@nigiri-rice.com</code> を指定してください。</p>\n</div>\n\n<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n<p class="mb-4">マルチデバイスからのアクセスと双方向同期のアーキテクチャフローです：</p>\n<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10">\n<pre class="mermaid text-sm">sequenceDiagram\n    autonumber\n    actor Mobile as スマホ (iOS/Android)\n    actor PC as Windows / Mac (Tailscale)\n    participant Caddy as VPS Caddy (fs.nigiri-rice.com)\n    participant NC as Nextcloud Hub / Cloudreve (CT 144)\n    participant KC as OmusuBI Keycloak (sso.nigiri-rice.com)\n    participant Watch as inotifywait Watcher\n    participant Storage as 共通共有 /srv/shares/public\n    participant Samba as Samba 4 AD (nigiri-rice)\n\n    rect rgb(240, 253, 250)\n    Note over Mobile,KC: 経路 A: SSO ログイン & Admin権限自動付与\n    Mobile->>Caddy: HTTPS :443 (fs.nigiri-rice.com)\n    Caddy->>NC: Tailscale Proxy (Port 8080)\n    NC->>KC: OIDC 認証リクエスト\n    KC-->>NC: ID Token (roles: [admin])\n    NC->>NC: admin グループ自動割当 (全権昇格)\n    NC->>Storage: POSIX ACL 経由で直接読み書き\n    end\n\n    rect rgb(254, 243, 199)\n    Note over PC,NC: 経路 B: リモート / 社内 PC (SMB) からの直接書き込み\n    PC->>Samba: SMB Port 445 (Tailscale VPN経由)\n    Samba->>Storage: ディスク書き込み\n    Storage->>Watch: Linux カーネル inotify イベント発火\n    Watch->>NC: occ / sync スキャン即時実行\n    NC-->>Mobile: モバイルアプリ / WebUI に即座にプッシュ反映\n    end\n</pre>\n</div>\n\n<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n<p class="mb-4">障害調査やメンテナンス時に実行する主要コマンド集です：</p>\n<div class="space-y-4 mb-6">\n  <div class="code-block-wrapper">\n    <div class="code-header"><span class="code-lang">bash</span></div>\n    <pre><code class="language-bash"># CT 144 へログイン\nssh root@10.155.0.144\n\n# Nextcloud 診断ステータス確認\nsudo -u www-data php /var/www/nextcloud/occ status\n\n# Nextcloud OIDC Admin ロール権限マッピング設定 (groupsクレームとadminグループの紐付け)\nsudo -u www-data php /var/www/nextcloud/occ user_oidc:provider:update 1 \\\n  --mapping-groups=groups \\\n  --group-mapping=\'{\"admin\": \"admin\", \"Admin\": \"admin\"}\'\n\n# admin グループ所属ユーザー確認\nsudo -u www-data php /var/www/nextcloud/occ group:list-members admin\n\n# 手動での管理者権限付与 (即時有効化)\nsudo -u www-data php /var/www/nextcloud/occ group:adduser admin i.shimamoto\n\n# 全ファイル手動スキャン\nsudo -u www-data php /var/www/nextcloud/occ files:scan --all\n\n# SMB ファイル監視デーモンの稼働状態\nsystemctl status nextcloud-smb-watch.service\n\n# Samba 4 AD DC ドメインコントローラの状態 (nigiri-rice)\nsystemctl status samba-ad-dc\n\n# OmusuBI からのユーザー/グループ同期手動実行\npython3 /usr/local/bin/sync_omusubi_to_samba.py\n</code></pre>\n  </div>\n</div>\n\n<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">7. 障害復旧 & Cloudreve 移行計画</h2>\n<div class="space-y-4 mb-6">\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">Cloudreve 段階的移行ステップ</h3>\n  <ol class="list-decimal pl-6 space-y-1 text-sm">\n    <li><strong>バイナリ配置:</strong> CT 144 上に Cloudreve 公式 amd64 バイナリを設置し、Port 5212 で起動。</li>\n    <li><strong>ストレージマウント:</strong> 保存先ディレクトリを <code>/srv/shares/public</code>、命名規則を <code>{path}/{filename}</code> に指定。</li>\n    <li><strong>Keycloak OAuth 2.0 連携:</strong> OmusuBI SSO クライアント <code>cloudreve</code> を作成し、SSO ログインを検証。</li>\n    <li><strong>並行検証:</strong> VPS Caddy に <code>drive.nigiri-rice.com</code> を追加し、Nextcloud を止めずに並行テスト。</li>\n    <li><strong>本番昇格:</strong> 検証完了後、<code>fs.nigiri-rice.com</code> の転送先を Port 5212 へ切り替え。</li>\n  </ol>\n\n  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">MariaDB バックアップ & リストア</h3>\n  <div class="code-block-wrapper">\n    <div class="code-header"><span class="code-lang">bash</span></div>\n    <pre><code class="language-bash"># バックアップ取得\nmariadb-dump -u nextcloud -p\'${DB_PASSWORD}\' nextcloud > /var/backups/nextcloud-$(date +%Y%m%d).sql\n\n# リストア手順\nmariadb -u nextcloud -p\'${DB_PASSWORD}\' nextcloud < /var/backups/nextcloud-20260918.sql\nsudo -u www-data php /var/www/nextcloud/occ maintenance:mode --off</code></pre>\n  </div>\n</div>\n',
    'id': 'fs-storage',
    'title': 'Nextcloud Hub ＆ Samba 4 AD 統合クラウドストレージ',
    'toc': [
      {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
      {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
      {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
      {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様 (モバイル/PC/Web)'},
      {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
      {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
      {'id': 'sec-7-setup', 'level': 2, 'title': '7. 障害復旧 & 整合性復元手順'}
    ]
  },
 'affine': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-18', 'Auto-join Enabled', 'Production'],
              'category_id': 'standalone',
              'category_name': 'メール & 独立サービス',
              'content_html': '\n'
                              '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">Notion / Miro '
                              '代替の次世代オープンソース・コラボレーティブナレッジベース基盤。</p>\n'
                              '\n'
                              '<div class="gh-alert gh-alert-note">\n'
                              '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                              'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                              '  <div class="gh-alert-body">本ページは Qiita '
                              '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                              '背景</h3>\n'
                              '  <p>チーム内の技術ドキュメント、設計ノート、ホワイトボードアイデアをリアルタイム共同編集・蓄積すること。</p>\n'
                              '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI / '
                              '動作基準)</h3>\n'
                              '  <ul class="list-disc pl-6 space-y-1">\n'
                              '    <li>ドキュメントとホワイトボードのシームレスな統合</li><li>ローカルファースト + クラウド同期による高速描画</li>\n'
                              '  </ul>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                              '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                              '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                              'レイヤー</th><th>採用技術 / '
                              'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>コア</td><td>AFFiNE Server '
                              'v0.27.4</td><td>GraphQL API + Node.js サーバー (Port '
                              '8083)</td></tr><tr><td>データベース</td><td>PostgreSQL 16 '
                              '(affine-postgres)</td><td>ワークスペースおよびドキュメントストア</td></tr><tr><td>キャッシュ</td><td>Redis 7 '
                              '(affine-redis)</td><td>リアルタイムコラボレーション同期</td></tr></tbody></table></div>\n'
                              '\n'
                              '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <p>Docker Volume <code>affine-postgres-data</code> および <code>affine-storage</code> '
                              'に格納。</p>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <p>アクセス URL: <code>https://affine.nigiri-rice.com/</code> (Caddy -> '
                              'localhost:8083)</p>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 '
                              'dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                              '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                              '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                              'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                              'text-sm">graph TD\n'
                              '    User["Team Member"] -->|HTTPS:443| Caddy["Caddy (VPS)"]\n'
                              '    Caddy -->|Proxy:8083| AFFiNE["AFFiNE Server"]\n'
                              '    AFFiNE --> PG["PostgreSQL (affine-postgres)"]\n'
                              '    AFFiNE --> Redis["Redis (affine-redis)"]</pre></div>\n'
                              '\n'
                              '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                              '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <div class="code-block-wrapper">\n'
                              '  <div class="code-header">\n'
                              '    <span class="code-lang">bash</span>\n'
                              '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                              '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                              '      <span>コピー</span>\n'
                              '    </button>\n'
                              '  </div>\n'
                              '  <pre><code class="language-bash">docker ps | grep affine\n'
                              'docker exec affine-postgres pg_dump -U affine affine &gt; /opt/backups/db-$(date '
                              '+%Y%m%d)/affine.sql</code></pre>\n'
                              '</div>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <div class="code-block-wrapper">\n'
                              '  <div class="code-header">\n'
                              '    <span class="code-lang">bash</span>\n'
                              '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                              '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                              '      <span>コピー</span>\n'
                              '    </button>\n'
                              '  </div>\n'
                              '  <pre><code class="language-bash">cd /opt/affine &amp;&amp; docker compose '
                              'restart</code></pre>\n'
                              '</div>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-autojoin" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">8. 全員参加型ワークスペース (Auto-join) 設計</h2>\n'
                              '<div class="gh-alert gh-alert-note">\n'
                              '  <div class="gh-alert-title"><i data-lucide="check-circle" class="w-4 h-4 '
                              'shrink-0"></i><span>新規ユーザーの初期自動参加仕様</span></div>\n'
                              '  <div class="gh-alert-body">\n'
                              '    新規登録・初回ログインを行ったすべてのユーザーは、PostgreSQL トリガーにより自動的にメイン共有ワークスペース '
                              '<strong>nigiri-rice.com</strong> (<code>926f4c2c-a0be-4f3a-a1cf-8247bf62621a</code>) '
                              'のアクティブメンバーとして即座に追加されます。\n'
                              '  </div>\n'
                              '</div>\n'
                              '<p class="mb-4">\n'
                              'AFFiNE バックエンド PostgreSQL (<code>affine-postgres</code>) に配備されたトリガー定義：\n'
                              '</p>\n'
                              '<div class="code-block-wrapper">\n'
                              '  <div class="code-header">\n'
                              '    <span class="code-lang">sql</span>\n'
                              '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                              '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                              '      <span>コピー</span>\n'
                              '    </button>\n'
                              '  </div>\n'
                              '  <pre><code class="language-sql">CREATE OR REPLACE FUNCTION '
                              'auto_join_default_workspace()\n'
                              'RETURNS TRIGGER AS $$\n'
                              'BEGIN\n'
                              '    INSERT INTO workspace_members (id, workspace_id, user_id, role, state, source, '
                              'created_at, updated_at)\n'
                              '    VALUES (\n'
                              "        'perm_' || md5(random()::text || clock_timestamp()::text),\n"
                              "        '926f4c2c-a0be-4f3a-a1cf-8247bf62621a',\n"
                              '        NEW.id,\n'
                              "        'member',\n"
                              "        'active',\n"
                              "        'system',\n"
                              '        NOW(),\n'
                              '        NOW()\n'
                              '    )\n'
                              '    ON CONFLICT (workspace_id, user_id, state) DO NOTHING;\n'
                              '    RETURN NEW;\n'
                              'END;\n'
                              '$$ LANGUAGE plpgsql;\n'
                              '\n'
                              'DROP TRIGGER IF EXISTS trg_auto_join_default_workspace ON users;\n'
                              'CREATE TRIGGER trg_auto_join_default_workspace\n'
                              'AFTER INSERT ON users\n'
                              'FOR EACH ROW\n'
                              'EXECUTE FUNCTION auto_join_default_workspace();\n'
                              '</code></pre>\n'
                              '</div>\n',
              'description': 'Notion / Miro 代替の次世代オープンソース・コラボレーティブナレッジベース基盤。',
              'icon': 'book',
              'id': 'affine',
              'last_updated': '2026-09-18',
              'service_id': 'affine',
              'title': 'AFFiNE ナレッジベース 運用マニュアル',
              'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                       {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                       {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                       {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                       {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                       {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                       {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'backup-recovery': { 'badges': ['バックアップ', 'DR手順', 'Runbook'],
                       'category_id': 'guidelines',
                       'category_name': '設計標準 & 運用ガイドライン',
                       'content_html': '\n'
                                       '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n'
                                       '全データベースの定時バックアップおよび緊急時リストア（復元）の実行手順書です。\n'
                                       '</p>\n'
                                       '\n'
                                       '<h2 id="sec-policy" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">1. バックアップ保管方針</h2>\n'
                                       '<ul class="list-disc pl-6 space-y-2 mb-6">\n'
                                       '  <li><strong>保管先ルート</strong>: <code>/opt/backups/db-YYYYMMDD/</code></li>\n'
                                       '  <li><strong>保管世代</strong>: 直近 7 世代（7日分）</li>\n'
                                       '  <li><strong>タイミング</strong>: 毎日深夜 03:00 JST 自動実行、および大規模リリース・設定変更前の手動実行</li>\n'
                                       '</ul>\n'
                                       '\n'
                                       '<h2 id="sec-k8s-db" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">2. K8s 内 PostgreSQL / MariaDB '
                                       'バックアップ</h2>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash"># 1. Keycloak PostgreSQL\n'
                                       'mkdir -p /opt/backups/db-$(date +%Y%m%d)\n'
                                       'kubectl -n omusubi exec omusubi-core-postgres-0 -- pg_dump -U keycloak '
                                       'keycloak &gt; /opt/backups/db-$(date +%Y%m%d)/keycloak.sql\n'
                                       '\n'
                                       '# 2. CNT Connect (本番 &amp; 開発)\n'
                                       'kubectl -n cnt-connect-prod exec postgres-0 -- pg_dump -U cnt cnt_connect &gt; '
                                       '/opt/backups/db-$(date +%Y%m%d)/cnt_prod.sql\n'
                                       'kubectl -n cnt-connect-dev exec postgres-0 -- pg_dump -U cnt cnt_connect &gt; '
                                       '/opt/backups/db-$(date +%Y%m%d)/cnt_dev.sql\n'
                                       '\n'
                                       '# 3. WordPress MariaDB\n'
                                       'WP_POD=$(kubectl -n nigiri-homepage get pods -l app=mariadb -o '
                                       "jsonpath='{.items[0].metadata.name}')\n"
                                       'kubectl -n nigiri-homepage exec $WP_POD -- mariadb-dump -u root -p$(kubectl -n '
                                       "nigiri-homepage get secret mariadb -o jsonpath='{.data.mariadb-root-password}' "
                                       '| base64 -d) wordpress &gt; /opt/backups/db-$(date '
                                       '+%Y%m%d)/wordpress.sql</code></pre>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-docker-db" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">3. 独立 Docker DB バックアップ</h2>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash"># Mailcow MySQL\n'
                                       'docker exec mailcowdockerized-mysql-mailcow-1 mysqldump -u root -p$(grep -E '
                                       "'^DBROOT=' /opt/mailcow-dockerized/mailcow.conf | cut -d= -f2) --all-databases "
                                       '&gt; /opt/backups/db-$(date +%Y%m%d)/mailcow-all.sql\n'
                                       '\n'
                                       '# AFFiNE PostgreSQL\n'
                                       'docker exec affine-postgres pg_dump -U affine affine &gt; '
                                       '/opt/backups/db-$(date +%Y%m%d)/affine.sql</code></pre>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-vault-backup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">4. Vault 暗号化ストレージ退避</h2>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash">mkdir -p /opt/backups/vault-$(date '
                                       '+%Y%m%d)\n'
                                       'kubectl -n vault exec vault-0 -- tar czf - -C /vault data &gt; '
                                       '/opt/backups/vault-$(date +%Y%m%d)/vault-data.tar.gz</code></pre>\n'
                                       '</div>\n',
                       'description': 'Keycloak, CNT Connect, WordPress, Mailcow, AFFiNE, Vault '
                                      'のデータベース退避および障害リストア手順です。',
                       'icon': 'archive',
                       'id': 'backup-recovery',
                       'last_updated': '2026-09-12',
                       'service_id': None,
                       'title': 'データベースバックアップ & リストア手順',
                       'toc': [ {'id': 'sec-policy', 'level': 2, 'title': '1. バックアップ保管方針'},
                                {'id': 'sec-k8s-db', 'level': 2, 'title': '2. K8s 内 PostgreSQL / MariaDB バックアップ'},
                                {'id': 'sec-docker-db', 'level': 2, 'title': '3. 独立 Docker DB バックアップ'},
                                {'id': 'sec-vault-backup', 'level': 2, 'title': '4. Vault 暗号化ストレージ退避'}]},
  'cloudflare-tunnel': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                         'category_id': 'network',
                         'category_name': 'エッジ & ネットワーク',
                         'content_html': '\n'
                                         '<p class="lead text-lg text-slate-600 dark:text-slate-300 '
                                         'mb-6">インバウンドポートを開放することなく、Argo CD 管理画面への安全なリモートアクセスを実現する暗号化トンネル。</p>\n'
                                         '\n'
                                         '<div class="gh-alert gh-alert-note">\n'
                                         '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                         'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                         '  <div class="gh-alert-body">本ページは Qiita '
                                         '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                         '</div>\n'
                                         '\n'
                                         '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 '
                                         'border-b border-slate-200 dark:border-emerald-950/70">1. 要件定義書 '
                                         '(Requirements)</h2>\n'
                                         '<div class="space-y-4 mb-6">\n'
                                         '  <h3 class="text-lg font-semibold text-emerald-600 '
                                         'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                         '  <p>Argo CD (argocd.nigiri-rice.com) に対し、ポート 443 を外部公開することなく Cloudflare '
                                         'Zero Trust 経由の安全な暗号化トンネルを提供すること。</p>\n'
                                         '  <h3 class="text-lg font-semibold text-emerald-600 '
                                         'dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>\n'
                                         '  <ul class="list-disc pl-6 space-y-1">\n'
                                         '    <li>cloudflared デーモン 2 Pods 冗長構成による無停止トンネリング</li><li>外部からのポートスキャン遮断および '
                                         'Cloudflare WAF による防御</li>\n'
                                         '  </ul>\n'
                                         '</div>\n'
                                         '\n'
                                         '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                         'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                         '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                         '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                         'レイヤー</th><th>採用技術 / '
                                         'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>トンネルエージェント</td><td>cloudflared '
                                         '(2 Pods HA)</td><td>Cloudflare Edge との間に常時暗号化 HTTP/2 QUIC '
                                         'コネクションを確立</td></tr><tr><td>マニフェスト管理</td><td>Argo CD / '
                                         'k8s-cluster-yaml</td><td>GitOps 自動同期による構成維持</td></tr></tbody></table></div>\n'
                                         '\n'
                                         '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                         'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                         '<div class="space-y-4 mb-6">\n'
                                         '  <p>ステートレスワークロード。Cloudflare トンネル認証トークンは Secret '
                                         '<code>cloudflare-argocd-tunnel</code> として暗号化保持。</p>\n'
                                         '</div>\n'
                                         '\n'
                                         '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                         'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                         '<div class="space-y-4 mb-6">\n'
                                         '  <p>アクセス URL: <code>https://argocd.nigiri-rice.com/</code> (Cloudflare '
                                         'Tunnel 経由)</p>\n'
                                         '</div>\n'
                                         '\n'
                                         '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                         'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                         '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                         '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                         'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                         'class="mermaid text-sm">sequenceDiagram\n'
                                         '    actor Admin as 管理者\n'
                                         '    participant CF as Cloudflare Edge\n'
                                         '    participant Daemon as cloudflared (2 Pods)\n'
                                         '    participant Argo as argocd-server (Service)\n'
                                         '\n'
                                         '    Admin->>CF: https://argocd.nigiri-rice.com\n'
                                         '    CF->>Daemon: 暗号化トンネル経由でリクエスト転送\n'
                                         '    Daemon->>Argo: 内部 ClusterIP :80 へ転送\n'
                                         '    Argo-->>Daemon: レスポンス返却\n'
                                         '    Daemon-->>CF: トンネル経由返却\n'
                                         '    CF-->>Admin: Argo CD 画面描画</pre></div>\n'
                                         '\n'
                                         '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                         'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 '
                                         '(Runbook)</h2>\n'
                                         '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                         '<div class="space-y-4 mb-6">\n'
                                         '  <div class="code-block-wrapper">\n'
                                         '  <div class="code-header">\n'
                                         '    <span class="code-lang">bash</span>\n'
                                         '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                         '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                         '      <span>コピー</span>\n'
                                         '    </button>\n'
                                         '  </div>\n'
                                         '  <pre><code class="language-bash">kubectl get pods -n cloudflare -o wide\n'
                                         'kubectl logs -n cloudflare -l app=cloudflare-argocd-tunnel '
                                         '--tail=50</code></pre>\n'
                                         '</div>\n'
                                         '</div>\n'
                                         '\n'
                                         '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                         'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                         '<div class="space-y-4 mb-6">\n'
                                         '  <div class="code-block-wrapper">\n'
                                         '  <div class="code-header">\n'
                                         '    <span class="code-lang">bash</span>\n'
                                         '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                         '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                         '      <span>コピー</span>\n'
                                         '    </button>\n'
                                         '  </div>\n'
                                         '  <pre><code class="language-bash">kubectl rollout restart deployment '
                                         'cloudflare-argocd-tunnel -n cloudflare</code></pre>\n'
                                         '</div>\n'
                                         '</div>\n',
                         'description': 'インバウンドポートを開放することなく、Argo CD 管理画面への安全なリモートアクセスを実現する暗号化トンネル。',
                         'icon': 'shield',
                         'id': 'cloudflare-tunnel',
                         'last_updated': '2026-09-12',
                         'service_id': 'cloudflare_tunnel',
                         'title': 'Cloudflare Argo CD Tunnel 運用マニュアル',
                         'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                                  {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                                  {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                                  {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                                  {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                                  {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                                  {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'cnt-connect-dev': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                       'category_id': 'apps',
                       'category_name': '業務アプリケーション',
                       'content_html': '\n'
                                       '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">CNT Connect '
                                       'の新機能検証・UI改善・ステージングテストを行うための開発環境。</p>\n'
                                       '\n'
                                       '<div class="gh-alert gh-alert-note">\n'
                                       '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                       'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                       '  <div class="gh-alert-body">本ページは Qiita '
                                       '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <h3 class="text-lg font-semibold text-emerald-600 '
                                       'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                       '  <p>本番環境に影響を与えることなく、新規機能やバージョンアップの結合テストを実施できる独立検証基盤を提供すること。</p>\n'
                                       '  <h3 class="text-lg font-semibold text-emerald-600 '
                                       'dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>\n'
                                       '  <ul class="list-disc pl-6 space-y-1">\n'
                                       '    <li>開発用シードデータの自動投入およびリセット機能</li><li>本番同等のアーキテクチャによる忠実な事前検証</li>\n'
                                       '  </ul>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                       '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                       '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                       'レイヤー</th><th>採用技術 / '
                                       'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>構成</td><td>Next.js + '
                                       'NestJS + PostgreSQL '
                                       '16</td><td>本番環境と同一のコンテナスタック</td></tr><tr><td>Namespace</td><td>cnt-connect-dev</td><td>本番と完全分離されたネットワークとストレージ</td></tr></tbody></table></div>\n'
                                       '\n'
                                       '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <p>StatefulSet <code>postgres-0</code> (Namespace: '
                                       '<code>cnt-connect-dev</code>) で独立稼働。</p>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <ul class="list-disc pl-6 space-y-1">\n'
                                       '  <li>管理画面: <code>https://dev.cnt-connect.nigiri-rice.com/</code></li>\n'
                                       '  <li>生徒ポータル: <code>https://dev.cnt-st.nigiri-rice.com/</code></li>\n'
                                       '</ul>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                       '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                       '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                       'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                       'class="mermaid text-sm">graph LR\n'
                                       '    Dev["Developer"] -->|Push Git| GH["GitHub Actions"]\n'
                                       '    GH -->|Deploy| K8sDev["cnt-connect-dev (K8s)"]\n'
                                       '    K8sDev --> DBDev["postgres-0 (Dev DB)"]</pre></div>\n'
                                       '\n'
                                       '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 '
                                       '(Runbook)</h2>\n'
                                       '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash">kubectl get pods -n cnt-connect-dev -o '
                                       'wide\n'
                                       'kubectl rollout restart deployment api admin-web student-web -n '
                                       'cnt-connect-dev</code></pre>\n'
                                       '</div>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash">cat /opt/backups/db-YYYYMMDD/cnt_dev.sql | '
                                       'kubectl -n cnt-connect-dev exec -i postgres-0 -- psql -U cnt '
                                       'cnt_connect</code></pre>\n'
                                       '</div>\n'
                                       '</div>\n',
                       'description': 'CNT Connect の新機能検証・UI改善・ステージングテストを行うための開発環境。',
                       'icon': 'code',
                       'id': 'cnt-connect-dev',
                       'last_updated': '2026-09-12',
                       'service_id': 'cnt_dev',
                       'title': 'CNT Connect 開発環境 運用保守マニュアル',
                       'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                                {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                                {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                                {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                                {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                                {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                                {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'cnt-connect-prod': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                        'category_id': 'apps',
                        'category_name': '業務アプリケーション',
                        'content_html': '\n'
                                        '<p class="lead text-lg text-slate-600 dark:text-slate-300 '
                                        'mb-6">生徒・スタッフ向け備品管理・貸出予約・QRスキャン・在庫管理システムの本番稼働環境。</p>\n'
                                        '\n'
                                        '<div class="gh-alert gh-alert-note">\n'
                                        '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                        'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                        '  <div class="gh-alert-body">本ページは Qiita '
                                        '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 '
                                        'border-b border-slate-200 dark:border-emerald-950/70">1. 要件定義書 '
                                        '(Requirements)</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <h3 class="text-lg font-semibold text-emerald-600 '
                                        'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                        '  <p>備品や教材の貸出・返却・在庫移動・点検をリアルタイムに自動化し、紛失防止と業務効率化を達成すること。</p>\n'
                                        '  <h3 class="text-lg font-semibold text-emerald-600 '
                                        'dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>\n'
                                        '  <ul class="list-disc pl-6 space-y-1">\n'
                                        '    <li>稼働可用性 99.9% の維持</li><li>生徒用パス (QRスキャン) の 1 '
                                        '秒以内即時照合</li><li>夜間自動バッチによる日次台帳集計とバックアップ</li>\n'
                                        '  </ul>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                        '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                        '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                        'レイヤー</th><th>採用技術 / '
                                        'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>フロントエンド</td><td>Next.js '
                                        '/ React (Admin & Student)</td><td>モダンなコンポーネント設計と PWA '
                                        '対応</td></tr><tr><td>バックエンド API</td><td>NestJS '
                                        '(TypeScript)</td><td>堅牢なモジュール設計、TypeORM による DB '
                                        '制御</td></tr><tr><td>データベース</td><td>PostgreSQL 16 (StatefulSet '
                                        'postgres-0)</td><td>永続ボリューム PVC マウント</td></tr><tr><td>イメージ配信</td><td>GitHub '
                                        'Container Registry (ghcr.io)</td><td>プライベートリポジトリから PAT '
                                        '経由で取得</td></tr></tbody></table></div>\n'
                                        '\n'
                                        '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">データベース設計</h4>\n'
                                        '<p>StatefulSet <code>postgres-0</code> (Namespace: '
                                        '<code>cnt-connect-prod</code>) 上で稼働。主要テーブル: <code>users</code>, '
                                        '<code>items</code>, <code>ledgers</code>, <code>loan_groups</code>, '
                                        '<code>reservations</code>。</p>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <ul class="list-disc pl-6 space-y-1">\n'
                                        '  <li>管理者画面: <code>https://cnt-connect.nigiri-rice.com/</code></li>\n'
                                        '  <li>生徒用ポータル: <code>https://cnt-st.nigiri-rice.com/</code></li>\n'
                                        '  <li>API エンドポイント: '
                                        '<code>https://cnt-connect.nigiri-rice.com/api/v1/...</code></li>\n'
                                        '</ul>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                        '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                        '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                        'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                        'class="mermaid text-sm">sequenceDiagram\n'
                                        '    actor Student as 生徒端末\n'
                                        '    participant STWeb as student-web\n'
                                        '    participant API as api (NestJS)\n'
                                        '    participant DB as postgres-0\n'
                                        '\n'
                                        '    Student->>STWeb: QRパス提示 / 貸出申請\n'
                                        '    STWeb->>API: POST /api/v1/loans/checkout\n'
                                        '    API->>DB: トランザクション開始 & 在庫状態更新\n'
                                        '    DB-->>API: 確定\n'
                                        '    API-->>STWeb: 貸出完了 (Ledger ID 発行)\n'
                                        '    STWeb-->>Student: 完了画面表示</pre></div>\n'
                                        '\n'
                                        '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 '
                                        '(Runbook)</h2>\n'
                                        '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <div class="code-block-wrapper">\n'
                                        '  <div class="code-header">\n'
                                        '    <span class="code-lang">bash</span>\n'
                                        '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                        '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                        '      <span>コピー</span>\n'
                                        '    </button>\n'
                                        '  </div>\n'
                                        '  <pre><code class="language-bash"># 1. Pod 状態確認\n'
                                        'kubectl get pods -n cnt-connect-prod -o wide\n'
                                        '\n'
                                        '# 2. API ログ確認\n'
                                        'kubectl logs -n cnt-connect-prod -l app=api -f --tail=50\n'
                                        '\n'
                                        '# 3. DB バックアップ\n'
                                        'kubectl -n cnt-connect-prod exec postgres-0 -- pg_dump -U cnt cnt_connect '
                                        '&gt; /opt/backups/db-$(date +%Y%m%d)/cnt_prod.sql</code></pre>\n'
                                        '</div>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <div class="code-block-wrapper">\n'
                                        '  <div class="code-header">\n'
                                        '    <span class="code-lang">bash</span>\n'
                                        '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                        '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                        '      <span>コピー</span>\n'
                                        '    </button>\n'
                                        '  </div>\n'
                                        '  <pre><code class="language-bash"># GHCR 認証更新手順\n'
                                        'kubectl -n cnt-connect-prod create secret docker-registry ghcr-secret \\\n'
                                        '  --docker-server=ghcr.io --docker-username=YOUR_USER '
                                        '--docker-password=YOUR_PAT \\\n'
                                        '  --dry-run=client -o yaml | kubectl apply -f -\n'
                                        'kubectl rollout restart deployment api admin-web student-web -n '
                                        'cnt-connect-prod</code></pre>\n'
                                        '</div>\n'
                                        '</div>\n',
                        'description': '生徒・スタッフ向け備品管理・貸出予約・QRスキャン・在庫管理システムの本番稼働環境。',
                        'icon': 'package',
                        'id': 'cnt-connect-prod',
                        'last_updated': '2026-09-12',
                        'service_id': 'cnt_prod',
                        'title': 'CNT Connect 本番環境 運用保守マニュアル',
                        'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                                 {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                                 {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                                 {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                                 {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                                 {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                                 {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'daily-operations': { 'badges': ['日常運用', 'Verified: 2026-09-12', 'Runbook'],
                        'category_id': 'guidelines',
                        'category_name': '設計標準 & 運用ガイドライン',
                        'content_html': '\n'
                                        '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n'
                                        '日々のインフラ安定稼働を担保するため、毎朝（09:00 JST）および毎夕（18:00 JST）に実行する巡回点検手順です。\n'
                                        '</p>\n'
                                        '\n'
                                        '<h2 id="sec-oneliner" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">1. 朝夕巡回ワンライナーチェックスクリプト</h2>\n'
                                        '<p class="mb-4">VPS（<code>210.131.211.17</code>）に SSH '
                                        '接続後、以下のコマンドブロックをそのままターミナルに貼り付けて実行します：</p>\n'
                                        '\n'
                                        '<div class="code-block-wrapper">\n'
                                        '  <div class="code-header">\n'
                                        '    <span class="code-lang">bash</span>\n'
                                        '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                        '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                        '      <span>コピー</span>\n'
                                        '    </button>\n'
                                        '  </div>\n'
                                        '  <pre><code class="language-bash">echo "=== 1. Argo CD 全アプリ同期ステータス ==="\n'
                                        'kubectl get applications -n argocd -o '
                                        'custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status\n'
                                        '\n'
                                        'echo "=== 2. 異常 Pod 検知 (Running/Completed 以外) ==="\n'
                                        'kubectl get pods -A '
                                        '--field-selector=status.phase!=Running,status.phase!=Succeeded\n'
                                        '\n'
                                        'echo "=== 3. ノード健全性 &amp; リソース使用率 ==="\n'
                                        'kubectl get nodes -o wide\n'
                                        'kubectl top nodes || true\n'
                                        '\n'
                                        'echo "=== 4. VPS 独立 Docker コンテナ稼働状態 ==="\n'
                                        'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E '
                                        '"(mailcow|affine|portainer|cadvisor)"\n'
                                        '\n'
                                        'echo "=== 5. ストレージ残量 &amp; システム時刻 ==="\n'
                                        'df -h /\n'
                                        'timedatectl | grep -E "(Local time|synchronized)"</code></pre>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-judgment" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">2. 正常・異常の判定基準</h2>\n'
                                        '<div class="table-responsive"><table '
                                        'class="gh-table"><thead><tr><th>チェック項目</th><th>正常判定基準</th><th>異常時の一次対応</th></tr></thead><tbody><tr><td>Argo '
                                        'CD 12 アプリ</td><td>全アプリが <code>Synced</code> かつ '
                                        '<code>Healthy</code></td><td>OutOfSync の場合はマニフェスト差分確認後、手動 sync '
                                        '実行。</td></tr><tr><td>Pod 異常検知</td><td><code>No resources found</code> '
                                        'と出力されること</td><td>CrashLoopBackOff や ImagePullBackOff の Pod を describe / logs '
                                        '確認。</td></tr><tr><td>ノード健全性</td><td>5ノードすべてが '
                                        '<code>Ready</code></td><td>NotReady ノードの kubelet ログまたは Docker '
                                        'コンテナ再起動。</td></tr><tr><td>独立コンテナ</td><td>Mailcow, AFFiNE, Portainer が Up '
                                        '(healthy)</td><td>docker compose restart または docker restart '
                                        '実行。</td></tr><tr><td>ストレージ残量</td><td>使用率が 80% 以下（目安: 49% 前後）</td><td>docker '
                                        'system prune や不要バックアップのアーカイブ削除。</td></tr><tr><td>日本標準時 '
                                        '(NTP)</td><td><code>synchronized: yes</code> かつ <code>JST '
                                        '(+0900)</code></td><td>systemctl restart systemd-timesyncd '
                                        '実行。</td></tr></tbody></table></div>\n',
                        'description': '運用管理者が毎朝・毎夕に実行する、全クラスタ・コンテナ・リソースのワンライナー健全性点検手順です。',
                        'icon': 'clipboard-check',
                        'id': 'daily-operations',
                        'last_updated': '2026-09-12',
                        'service_id': None,
                        'title': '日常巡回 & 朝夕ワンライナー点検手順',
                        'toc': [ {'id': 'sec-oneliner', 'level': 2, 'title': '1. 朝夕巡回ワンライナーチェックスクリプト'},
                                 {'id': 'sec-judgment', 'level': 2, 'title': '2. 正常・異常の判定基準'},
                                 {'id': 'sec-subsystems', 'level': 2, 'title': '3. サブシステム別詳細点検'}]},
  'developer-portal': { 'badges': ['7つの必須ドキュメント準拠', 'v1.7.0', 'Verified: 2026-09-18', 'Production'],
                        'category_id': 'apps',
                        'category_name': '業務アプリケーション',
                        'content_html': '\n'
                                        '<p class="lead text-lg text-slate-600 dark:text-slate-300 '
                                        'mb-6">全サービス一覧、アーキテクチャ構成図、資格情報共有、ドキュメントビューア、公開ステータスページを提供する開発統合ハブ。</p>\n'
                                        '\n'
                                        '<div class="gh-alert gh-alert-note">\n'
                                        '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                        'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                        '  <div class="gh-alert-body">本ページは Qiita '
                                        '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 '
                                        'border-b border-slate-200 dark:border-emerald-950/70">1. 要件定義書 '
                                        '(Requirements)</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <h3 class="text-lg font-semibold text-emerald-600 '
                                        'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                        '  '
                                        '<p>開発者および運用者が全サービスの稼働状況・構成図・ドキュメント・認証情報をワンストップで把握・利用できるプラットフォームを提供すること。</p>\n'
                                        '  <h3 class="text-lg font-semibold text-emerald-600 '
                                        'dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>\n'
                                        '  <ul class="list-disc pl-6 space-y-1">\n'
                                        '    <li>Keycloak OIDC による JIT (Just-in-Time) ロール自動付与</li><li>GitHub Docs '
                                        '風ドキュメントビューアおよび公開ステータスページの常時提供</li><li>2 Pods HA 冗長稼働による無停止運用</li>\n'
                                        '  </ul>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                        '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                        '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                        'レイヤー</th><th>採用技術 / '
                                        'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>フレームワーク</td><td>FastAPI '
                                        '(Python 3.11)</td><td>高速な非同期 Web アプリケーション</td></tr><tr><td>UI '
                                        'デザイン</td><td>Tailwind CSS + Lucide '
                                        'Icons</td><td>洗練されたダーク/ライトテーマ対応</td></tr><tr><td>配備形態</td><td>Deployment '
                                        'nigiri-portal (2 Pods HA)</td><td>nigiri-homepage namespace '
                                        '内で稼働</td></tr></tbody></table></div>\n'
                                        '\n'
                                        '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <p>ステートレス設計。資格情報は <code>data/credentials.json</code>、サービス定義は '
                                        '<code>services_data.py</code>、ドキュメントは <code>docs_data.py</code> で管理。</p>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <ul class="list-disc pl-6 space-y-1">\n'
                                        '  <li>ポータルトップ: <code>https://www.nigiri-rice.com/portal/</code></li>\n'
                                        '  <li>ドキュメント: <code>https://www.nigiri-rice.com/portal/docs</code></li>\n'
                                        '  <li>公開ステータス: <code>https://www.nigiri-rice.com/portal/status</code> '
                                        '(認証不要)</li>\n'
                                        '  <li>ヘルスチェック: <code>/healthz</code></li>\n'
                                        '</ul>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                        '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                        '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                        'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                        'class="mermaid text-sm">graph TD\n'
                                        '    Dev["Developer"] -->|HTTPS:443| Caddy["Caddy (VPS)"]\n'
                                        '    Caddy -->|ClusterIP:8080| Portal["nigiri-portal (2 Pods)"]\n'
                                        '    Portal <-->|OIDC Auth| KC["Keycloak SSO"]\n'
                                        '    Portal --> Docs["docs_data.py (GitHub Docs)"]\n'
                                        '    Portal --> Status["/status (Statuspage)"]</pre></div>\n'
                                        '\n'
                                        '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 '
                                        '(Runbook)</h2>\n'
                                        '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <div class="code-block-wrapper">\n'
                                        '  <div class="code-header">\n'
                                        '    <span class="code-lang">bash</span>\n'
                                        '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                        '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                        '      <span>コピー</span>\n'
                                        '    </button>\n'
                                        '  </div>\n'
                                        '  <pre><code class="language-bash">kubectl get pods -n nigiri-homepage -l '
                                        'app.kubernetes.io/name=nigiri-portal -o wide\n'
                                        'kubectl logs -n nigiri-homepage -l app.kubernetes.io/name=nigiri-portal -f '
                                        '--tail=50</code></pre>\n'
                                        '</div>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                        '<div class="space-y-4 mb-6">\n'
                                        '  <div class="code-block-wrapper">\n'
                                        '  <div class="code-header">\n'
                                        '    <span class="code-lang">bash</span>\n'
                                        '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                        '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                        '      <span>コピー</span>\n'
                                        '    </button>\n'
                                        '  </div>\n'
                                        '  <pre><code class="language-bash">kubectl -n nigiri-homepage rollout restart '
                                        'deployment nigiri-portal</code></pre>\n'
                                        '</div>\n'
                                        '</div>\n'
                                        '\n'
                                        '<h2 id="sec-v170-updates" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                        'border-slate-200 dark:border-emerald-950/70">8. v1.7.0 最新改修内容 '
                                        '(2026-09-18)</h2>\n'
                                        '<ul class="list-disc pl-6 space-y-2 mb-6">\n'
                                        '  <li><strong>Keycloak OIDC ログアウトの完全修復</strong>: RP-Initiated Logout '
                                        '仕様に準拠し、<code>client_id=nigiri-developer-portal</code> を付与するとともに Keycloak 側に '
                                        '<code>post.logout.redirect.uris</code> を登録。従来の 400 Bad '
                                        'Request（おむすび型崩れエラー）を完全解消。</li>\n'
                                        '  <li><strong>共有認証情報の HashiCorp Vault 完全移行</strong>: '
                                        '自作平文保管（<code>credentials.json</code>）を廃止し、ポータルの認証情報リンクおよびタブを '
                                        '<code>https://vault.nigiri-rice.com/ui/vault/auth?with=oidc</code>（Keycloak '
                                        'OIDC SSO 認証）へ直接リダイレクトする構成へ昇格。</li>\n'
                                        '  <li><strong>ステータス監視の status.nigiri-rice.com 統合</strong>: '
                                        '旧静的ステータスページを廃止し、<code>/status</code> アクセス時およびヘッダーボタンを新規外部監視基盤 '
                                        '<code>https://status.nigiri-rice.com</code> へリダイレクト／直接リンク。</li>\n'
                                        '  <li><strong>モバイル目次ドロワーのスクロール不具合修正</strong>: 画面幅 1024px '
                                        '未満でハンバーガーメニューから開く目次スライドインドロワーにおいて、CSS の <code>min-height: 0</code> および '
                                        '<code>overscroll-behavior: contain</code> を適用し、上下スクロールが確実に機能するよう改修。</li>\n'
                                        '</ul>\n',
                        'description': '全サービス一覧、アーキテクチャ構成図、資格情報共有、ドキュメントビューア、公開ステータスページを提供する開発統合ハブ。',
                        'icon': 'compass',
                        'id': 'developer-portal',
                        'last_updated': '2026-09-18',
                        'service_id': 'portal',
                        'title': 'Nigiri Developer Portal 運用マニュアル (v1.7.0)',
                        'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                                 {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                                 {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                                 {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                                 {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                                 {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                                 {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'harbor': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
              'category_id': 'storage',
              'category_name': 'ストレージ & レジストリ',
              'content_html': '\n'
                              '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">社内プライベートコンテナイメージおよび '
                              'Helm チャートのセキュア保管、脆弱性スキャン (Trivy) 基盤。</p>\n'
                              '\n'
                              '<div class="gh-alert gh-alert-note">\n'
                              '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                              'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                              '  <div class="gh-alert-body">本ページは Qiita '
                              '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                              '背景</h3>\n'
                              '  <p>nigiri-rice.com 内部の全独自コンテナイメージ（Console, Portal, Shumoku等）を自社管理下で安全に格納・配布すること。</p>\n'
                              '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI / '
                              '動作基準)</h3>\n'
                              '  <ul class="list-disc pl-6 space-y-1">\n'
                              '    <li>docker pull / push の高速性（クラスタ内部帯域活用）</li><li>Trivy によるイメージ push 時の自動脆弱性スキャンと CVE '
                              '早期検知</li><li>CI/CD ロボットアカウントによる安全なプッシュ権限分離</li>\n'
                              '  </ul>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                              '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                              '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                              'レイヤー</th><th>採用技術 / '
                              'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>レジストリコア</td><td>Harbor '
                              'v2.10.x</td><td>ロールベースアクセス制御、Webフック、マルチプロジェクト管理</td></tr><tr><td>脆弱性スキャナ</td><td>Trivy '
                              '(StatefulSet)</td><td>Aqua Security '
                              '製の高速コンテナ脆弱性スキャナ</td></tr><tr><td>バックエンドDB</td><td>PostgreSQL '
                              '(harbor-database)</td><td>Harbor メタデータおよびユーザー権限ストア</td></tr><tr><td>キャッシュ</td><td>Redis '
                              '(harbor-redis)</td><td>セッションおよびジョブキューキャッシュ</td></tr></tbody></table></div>\n'
                              '\n'
                              '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">イメージ永続化ストレージ</h4>\n'
                              '<p>コンテナイメージ層（Blob）は PVC <code>harbor-registry</code> 上に格納されます。メタデータは '
                              '<code>harbor-database</code> (PostgreSQL PVC) に永続化。</p>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <ul class="list-disc pl-6 space-y-1">\n'
                              '  <li>Web UI: <code>https://registry.nigiri-rice.com/</code> (または '
                              '<code>https://harbor.nigiri-rice.com/</code>)</li>\n'
                              '  <li>Docker Login: <code>docker login registry.nigiri-rice.com</code></li>\n'
                              '  <li>SSO 連携: Keycloak OIDC (master realm) 構成済み</li>\n'
                              '</ul>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 '
                              'dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                              '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                              '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                              'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                              'text-sm">graph TD\n'
                              '    Dev["Developer / CI/CD"] -->|docker push| Reg["registry.nigiri-rice.com"]\n'
                              '    Reg --> Ingress["Ingress-NGINX"]\n'
                              '    Ingress --> Core["harbor-core (2 Pods)"]\n'
                              '    Core --> Storage["PVC: harbor-registry"]\n'
                              '    Core --> Trivy["Trivy Vulnerability Scanner"]\n'
                              '    Core --> DB["PostgreSQL: harbor-database"]</pre></div>\n'
                              '\n'
                              '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                              '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <div class="code-block-wrapper">\n'
                              '  <div class="code-header">\n'
                              '    <span class="code-lang">bash</span>\n'
                              '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                              '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                              '      <span>コピー</span>\n'
                              '    </button>\n'
                              '  </div>\n'
                              '  <pre><code class="language-bash"># Harbor 全コンポーネント確認\n'
                              'kubectl get pods -n harbor -o wide\n'
                              '\n'
                              '# Core ログ追跡\n'
                              'kubectl logs -n harbor -l app.kubernetes.io/name=harbor-core --tail=50</code></pre>\n'
                              '</div>\n'
                              '</div>\n'
                              '\n'
                              '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                              'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                              '<div class="space-y-4 mb-6">\n'
                              '  <div class="code-block-wrapper">\n'
                              '  <div class="code-header">\n'
                              '    <span class="code-lang">bash</span>\n'
                              '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                              '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                              '      <span>コピー</span>\n'
                              '    </button>\n'
                              '  </div>\n'
                              '  <pre><code class="language-bash">kubectl rollout restart deployment harbor-core '
                              'harbor-portal -n harbor</code></pre>\n'
                              '</div>\n'
                              '</div>\n',
              'description': '社内プライベートコンテナイメージおよび Helm チャートのセキュア保管、脆弱性スキャン (Trivy) 基盤。',
              'icon': 'box',
              'id': 'harbor',
              'last_updated': '2026-09-12',
              'service_id': 'harbor',
              'title': 'Harbor Container Registry 運用保守マニュアル',
              'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                       {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                       {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                       {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                       {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                       {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                       {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'ingress-caddy': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                     'category_id': 'network',
                     'category_name': 'エッジ & ネットワーク',
                     'content_html': '\n'
                                     '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">Cloudflare Edge '
                                     'と K8s クラスタを繋ぐエッジリバースプロキシ (Caddy) およびクラスタ内 Ingress-NGINX コントローラ。</p>\n'
                                     '\n'
                                     '<div class="gh-alert gh-alert-note">\n'
                                     '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                     'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                     '  <div class="gh-alert-body">本ページは Qiita '
                                     '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                     '</div>\n'
                                     '\n'
                                     '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                     '<div class="space-y-4 mb-6">\n'
                                     '  <h3 class="text-lg font-semibold text-emerald-600 '
                                     'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                     "  <p>HTTPS TLS 終端、Let's Encrypt 自動証明書管理、パスベースルーティング、および Ingress-NGINX "
                                     'へのトラフィック中継を一元化すること。</p>\n'
                                     '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 '
                                     '(KPI / 動作基準)</h3>\n'
                                     '  <ul class="list-disc pl-6 space-y-1">\n'
                                     "    <li>全ドメインにおける SSL/TLS 自動更新（Let's Encrypt ACME）の 100% 成功</li><li>NodePort "
                                     '30180 経由の低レイテンシ（< 5ms）内部ルーティング</li><li>Vault SSO '
                                     '自動リダイレクト等、エッジレベルでの高度なヘッダー・クエリ制御</li>\n'
                                     '  </ul>\n'
                                     '</div>\n'
                                     '\n'
                                     '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                     '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                     '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                     'レイヤー</th><th>採用技術 / '
                                     'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>エッジプロキシ</td><td>Caddy v2 '
                                     '(systemd on nigiri-vps)</td><td>HTTP/2, HTTP/3 (QUIC) '
                                     '対応、自動証明書管理、高速リバースプロキシ</td></tr><tr><td>クラスター Ingress</td><td>Ingress-NGINX '
                                     'Controller (2 Pods HA)</td><td>K8s 標準 Ingress コントローラ。NodePort 30180 (HTTP) / '
                                     '30444 (HTTPS)</td></tr><tr><td>エッジ DNS / WAF</td><td>Cloudflare Edge</td><td>DNS '
                                     'キャッシュ、DDoS 防護、SSL Full Strict モード</td></tr></tbody></table></div>\n'
                                     '\n'
                                     '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                     '<div class="space-y-4 mb-6">\n'
                                     '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">設定ファイル & '
                                     '証明書ストレージ</h4>\n'
                                     '<ul class="list-disc pl-6 space-y-1">\n'
                                     '  <li>設定ファイル: <code>/etc/caddy/Caddyfile</code> (バックアップ: '
                                     '<code>/etc/caddy/Caddyfile.bak</code>)</li>\n'
                                     '  <li>ACME 証明書ストレージ: '
                                     '<code>/var/lib/caddy/.local/share/caddy/certificates/</code></li>\n'
                                     '</ul>\n'
                                     '</div>\n'
                                     '\n'
                                     '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                     '<div class="space-y-4 mb-6">\n'
                                     '  <h4 class="font-semibold text-slate-800 '
                                     'dark:text-slate-200">主要ルーティングエンドポイント</h4>\n'
                                     '<ul class="list-disc pl-6 space-y-1">\n'
                                     '  <li><code>vault.nigiri-rice.com</code> -> <code>127.0.0.1:30180</code> (SSO '
                                     'リダイレクト付与)</li>\n'
                                     '  <li><code>registry.nigiri-rice.com</code> -> <code>127.0.0.1:30180</code> '
                                     '(Harbor Ingress)</li>\n'
                                     '  <li><code>www.nigiri-rice.com</code> -> <code>10.43.53.28:80</code> '
                                     '(WordPress), <code>/portal*</code> -> <code>10.43.216.166:8080</code> '
                                     '(Portal)</li>\n'
                                     '  <li><code>sso.nigiri-rice.com</code> -> <code>10.43.148.25:8080</code> '
                                     '(Keycloak)</li>\n'
                                     '  <li><code>console.nigiri-rice.com</code> -> <code>10.43.155.158:80</code> '
                                     '(Console)</li>\n'
                                     '</ul>\n'
                                     '</div>\n'
                                     '\n'
                                     '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                     '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                     '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                     'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                     'class="mermaid text-sm">graph LR\n'
                                     '    Client["Client Browser"] -->|HTTPS:443| CF["Cloudflare Edge"]\n'
                                     '    CF -->|TLS Full Strict| Caddy["Caddy (nigiri-vps)"]\n'
                                     '    Caddy -->|NodePort:30180| Ingress["Ingress-NGINX (2 Pods)"]\n'
                                     '    Caddy -->|ClusterIP:8080| Portal["Portal Pods"]\n'
                                     '    Caddy -->|ClusterIP:80| WP["WordPress Pods"]\n'
                                     '    Ingress -->|ClusterIP:8200| Vault["Vault Pod"]\n'
                                     '    Ingress -->|ClusterIP:80| Harbor["Harbor Pods"]</pre></div>\n'
                                     '\n'
                                     '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                     '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                     '<div class="space-y-4 mb-6">\n'
                                     '  <div class="code-block-wrapper">\n'
                                     '  <div class="code-header">\n'
                                     '    <span class="code-lang">bash</span>\n'
                                     '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                     '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                     '      <span>コピー</span>\n'
                                     '    </button>\n'
                                     '  </div>\n'
                                     '  <pre><code class="language-bash"># 1. Caddy 構文チェック &amp; リロード\n'
                                     'caddy validate --config /etc/caddy/Caddyfile\n'
                                     'systemctl reload caddy\n'
                                     '\n'
                                     '# 2. Ingress-NGINX Pod 稼働確認\n'
                                     'kubectl get pods -n nginx-ingress -o wide\n'
                                     '\n'
                                     '# 3. エラーログ確認\n'
                                     'journalctl -u caddy -n 50 --no-pager</code></pre>\n'
                                     '</div>\n'
                                     '</div>\n'
                                     '\n'
                                     '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                     'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                     '<div class="space-y-4 mb-6">\n'
                                     '  <div class="code-block-wrapper">\n'
                                     '  <div class="code-header">\n'
                                     '    <span class="code-lang">bash</span>\n'
                                     '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                     '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                     '      <span>コピー</span>\n'
                                     '    </button>\n'
                                     '  </div>\n'
                                     '  <pre><code class="language-bash"># 設定ロールバック\n'
                                     'cp /etc/caddy/Caddyfile.bak /etc/caddy/Caddyfile\n'
                                     'caddy validate --config /etc/caddy/Caddyfile &amp;&amp; systemctl restart '
                                     'caddy</code></pre>\n'
                                     '</div>\n'
                                     '</div>\n',
                     'description': 'Cloudflare Edge と K8s クラスタを繋ぐエッジリバースプロキシ (Caddy) およびクラスタ内 Ingress-NGINX コントローラ。',
                     'icon': 'globe',
                     'id': 'ingress-caddy',
                     'last_updated': '2026-09-12',
                     'service_id': 'ingress_nginx',
                     'title': 'Caddy & Ingress-NGINX ルーティングマニュアル',
                     'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                              {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                              {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                              {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                              {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                              {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                              {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'keycloak': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                'category_id': 'identity',
                'category_name': '認証 & ID 基盤',
                'content_html': '\n'
                                '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">社内全システム（Vault, '
                                'Console, Harbor, CNT Connect, Portal）のシングルサインオン (SSO) および ID Federation '
                                'を統括する認証中核基盤。</p>\n'
                                '\n'
                                '<div class="gh-alert gh-alert-note">\n'
                                '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                '  <div class="gh-alert-body">本ページは Qiita '
                                '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                                '背景</h3>\n'
                                '  <p>nigiri-rice.com における全サービスのユーザー認証を一本化し、SSO、MFA、ロールベース認可 '
                                '(RBAC)、およびアカウントライフサイクルを一元管理すること。</p>\n'
                                '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI '
                                '/ 動作基準)</h3>\n'
                                '  <ul class="list-disc pl-6 space-y-1">\n'
                                '    <li>全サービスにおける SSO 認証の可用性 99.9% 以上の維持</li><li>Infinispan / JGroups による 2 Pods HA '
                                '冗長稼働とセッションフェイルオーバー</li><li>パスワードポリシー、セッション有効期限、アクセス監査ログの完全性</li>\n'
                                '  </ul>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                'レイヤー</th><th>採用技術 / '
                                'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>認証コア</td><td>Keycloak v26.7.0 '
                                '(Quarkus runtime)</td><td>高速起動・省メモリな次世代 Quarkus ベース OIDC/SAML '
                                'IdP</td></tr><tr><td>データベース</td><td>PostgreSQL 16 '
                                '(omusubi-core-postgres)</td><td>コネクション上限 '
                                '250、自動日次バックアップ対応の専用ストア</td></tr><tr><td>クラスタリング</td><td>JGroups '
                                '(KUBE_PING)</td><td>Kubernetes Service 経由で Pod '
                                '間キャッシュを同期する分散クラスタ</td></tr><tr><td>管理UI</td><td>Keycloak Admin Console</td><td>master '
                                'レルムおよび各サービスクライアントのGUI管理画面</td></tr></tbody></table></div>\n'
                                '\n'
                                '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">PostgreSQL '
                                'データベース構造</h4>\n'
                                '<p>Keycloak のデータは <code>omusubi-core-postgres</code> (StatefulSet) 上の '
                                '<code>keycloak</code> データベースに格納されます。PVC <code>data-omusubi-core-postgres-0</code> '
                                'により永続化されています。</p>\n'
                                '<ul class="list-disc pl-6 space-y-1">\n'
                                '  <li>内部ホスト: <code>omusubi-core-postgres.omusubi.svc.cluster.local:5432</code></li>\n'
                                '  <li>DB名: <code>keycloak</code>, ユーザー: <code>keycloak</code></li>\n'
                                '  <li>パラメータ: <code>max_connections=250</code>, '
                                '<code>shared_buffers=256MB</code></li>\n'
                                '</ul>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">管理画面 & エンドポイント仕様</h4>\n'
                                '<ul class="list-disc pl-6 space-y-1">\n'
                                '  <li>管理コンソール: <code>https://sso.nigiri-rice.com/admin/master/console/</code></li>\n'
                                '  <li>レルム定義: <code>master</code> (主要全クライアント収容)</li>\n'
                                '  <li>OIDC Discovery: '
                                '<code>https://sso.nigiri-rice.com/realms/master/.well-known/openid-configuration</code></li>\n'
                                '  <li>トークン有効期間: Access Token 1時間, Refresh Token 8時間</li>\n'
                                '</ul>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                                'text-sm">sequenceDiagram\n'
                                '    autonumber\n'
                                '    actor User as ユーザー\n'
                                '    participant App as 連携アプリ (Portal / Vault)\n'
                                '    participant KC as Keycloak Core (HA 2 Pods)\n'
                                '    participant DB as PostgreSQL (omusubi)\n'
                                '\n'
                                '    User->>App: ログイン要求\n'
                                '    App->>KC: OIDC Auth Redirect (/realms/master/protocol/openid-connect/auth)\n'
                                '    KC-->>User: 認証フォーム表示 (Login / MFA)\n'
                                '    User->>KC: 資格情報送信\n'
                                '    KC->>DB: ユーザー照合 & パスワード検証\n'
                                '    DB-->>KC: 属性 & ロール返却\n'
                                '    KC-->>App: 認可コード返却 (Redirect with code)\n'
                                '    App->>KC: /token エンドポイントへコード交換要求\n'
                                '    KC-->>App: ID Token & Access Token (JWT)\n'
                                '    App-->>User: ログイン完了</pre></div>\n'
                                '\n'
                                '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <div class="code-block-wrapper">\n'
                                '  <div class="code-header">\n'
                                '    <span class="code-lang">bash</span>\n'
                                '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                '      <span>コピー</span>\n'
                                '    </button>\n'
                                '  </div>\n'
                                '  <pre><code class="language-bash"># 1. Keycloak Pod 稼働確認 (2 Pods Running)\n'
                                'kubectl get pods -n omusubi -l app.kubernetes.io/name=keycloak -o wide\n'
                                '\n'
                                '# 2. ログ追跡 (リアルタイム)\n'
                                'kubectl logs -n omusubi -l app.kubernetes.io/name=keycloak -c keycloak -f --tail=50\n'
                                '\n'
                                '# 3. Pod ローリング再起動\n'
                                'kubectl -n omusubi rollout restart deployment omusubi-core</code></pre>\n'
                                '</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <div class="code-block-wrapper">\n'
                                '  <div class="code-header">\n'
                                '    <span class="code-lang">bash</span>\n'
                                '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                '      <span>コピー</span>\n'
                                '    </button>\n'
                                '  </div>\n'
                                '  <pre><code class="language-bash"># DB リストア手順\n'
                                'cat /opt/backups/db-YYYYMMDD/keycloak.sql | kubectl -n omusubi exec -i '
                                'omusubi-core-postgres-0 -- psql -U keycloak keycloak\n'
                                'kubectl -n omusubi rollout restart deployment omusubi-core</code></pre>\n'
                                '</div>\n'
                                '</div>\n',
                'description': '社内全システム（Vault, Console, Harbor, CNT Connect, Portal）のシングルサインオン (SSO) および ID Federation '
                               'を統括する認証中核基盤。',
                'icon': 'key',
                'id': 'keycloak',
                'last_updated': '2026-09-12',
                'service_id': 'keycloak_admin',
                'title': 'Keycloak SSO (OmusuBI Core) 運用保守マニュアル',
                'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                         {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                         {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                         {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                         {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                         {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                         {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'mailcow': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-19', '脱PPAP添付システム対応', 'Production'],
                'category_id': 'standalone',
                'category_name': 'メール & 独立サービス',
                'content_html': '''
<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">
  Docker コンテナ群（Postfix, Dovecot, SOGo, Rspamd, ClamAV, MySQL）で構成される企業メール送受信基盤。<br>
  脱PPAP（パスワード付きZIP廃止）に対応した<strong>大容量添付ファイル自動リンク化システム</strong>を完備し、受信メールの添付自動抽出・Nextcloud クラウドストレージ（Office / PDF プレビュー対応）へのセキュア連携を実現しています。
</p>

<div class="gh-alert gh-alert-note">
  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>
  <div class="gh-alert-body">本ページは Qiita 策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>
</div>

<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>
<div class="space-y-4 mb-6">
  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & 背景</h3>
  <p>nigiri-rice.com ドメインにおける信頼性の高いメール送受信、Webmail (SOGo)、高度なスパムフィルタリング、およびウイルススキャンを提供すること。さらに、従来の暗号化ZIP別送（PPAP）を廃止し、セキュアかつ容量効率の高い添付ファイル送受信環境を構築すること。</p>
  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>
  <ul class="list-disc pl-6 space-y-1">
    <li><strong>DKIM / SPF / DMARC 100% 準拠:</strong> 主要キャリア・企業宛てメールの到達性を確保。</li>
    <li><strong>脱PPAP 送信リンク化:</strong> Thunderbird Filelink または Nextcloud 共有リンクにより、メール本文への安全なダウンロードURL挿入。</li>
    <li><strong>受信メール添付自動リンク化:</strong> 外部から届いた添付ファイルを自動的に Nextcloud (<code>/Public/MailInbound</code>) へ保存し、メール本文に Collabora プレビュー付きの安全リンクを付与。</li>
    <li><strong>メールボックス容量最適化:</strong> 大容量添付ファイルを Nextcloud ZFS ストレージへ分離し、メールボックス肥大化を防止。</li>
  </ul>
</div>

<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>
<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>
<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / レイヤー</th><th>採用技術 / バージョン</th><th>選定理由・メリット</th></tr></thead><tbody>
<tr><td>MTA / 送信</td><td>Postfix 3.10</td><td>SMTP (25), Submission (587), SMTPS (465) / TLS 厳格適用</td></tr>
<tr><td>MDA / 受信</td><td>Dovecot 2.3</td><td>IMAP (143), IMAPS (993), Sieve フィルタ, Maildir 格納</td></tr>
<tr><td>Webmail</td><td>SOGo Groupware 5.12</td><td>Web メール, カレンダー, アドレス帳 (Port 8448, SSO 対応)</td></tr>
<tr><td>スパム・ウイルス防護</td><td>Rspamd 4.1 + ClamAV + Redis</td><td>機械学習型スパム判定 & リアルタイムシグネチャ更新</td></tr>
<tr><td>脱PPAP 添付リンク化</td><td>OmusuBI Attachment Linker (Python)</td><td>新着メール添付自動抽出 → Nextcloud CT 144 へ転送・プレビューリンク付与</td></tr>
<tr><td>ファイルプレビュー</td><td>Collabora Online 26.04 (CODE)</td><td>Word / Excel / PPT / PDF のブラウザ直接閲覧・共同編集</td></tr>
</tbody></table></div>

<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>
<div class="space-y-4 mb-6">
  <h4 class="font-semibold text-slate-800 dark:text-slate-200">メールデータ永続化 & 添付ファイル分離</h4>
  <p>メール本体は VPS 上の Docker Volume <code>mailcowdockerized_vmail-vol-1</code> (Maildir 形式) に格納されます。</p>
  <ul class="list-disc pl-6 space-y-1">
    <li><strong>受信添付ファイル格納先:</strong> <code>/srv/shares/public/MailInbound/{YYYY-MM}/{受信者}/</code> (CT 144 ZFS プール)</li>
  <li><strong>Windows SMB 共有:</strong> <code>\\\\10.155.0.144\\public\\MailInbound</code> より直接アクセス可能。</li>\n
    <li><strong>リアルタイムインデックス:</strong> <code>nextcloud-smb-watch.service</code> (inotifywait) により 0.1 秒で Nextcloud に同期。</li>
  </ul>
</div>

<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様 (脱PPAP運用マニュアル)</h2>
<div class="space-y-4 mb-6">
  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">📤 送信時の脱PPAP手順 (Thunderbird Filelink)</h3>
  <ol class="list-decimal pl-6 space-y-1 text-sm">
    <li>Thunderbird の「設定」→「編集とアドレス入力」→「添付ファイル」を開く。</li>
    <li>「Filelink」設定で <strong>Nextcloud</strong> を追加（サーバー: <code>https://fs.nigiri-rice.com</code>）。</li>
    <li>OmusuBI アカウントで認証を完了。</li>
    <li>メール作成時に大容量ファイルをドラッグ＆ドロップすると、「Filelink で送信」が自動提示され、本文にセキュアリンクが挿入されます。</li>
  </ol>

  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">📥 受信メールの自動リンク化機能</h3>
  <p class="text-sm">外部から添付ファイル付きメールを受信すると、システムが自動的に添付を抽出し、メール本文末尾に以下の安全プレビューブロックを付与します：</p>
  <div class="p-3 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-500/30 rounded-lg text-xs space-y-1">
    <div class="font-semibold text-emerald-800 dark:text-emerald-300">📎 【脱PPAP 添付ファイル安全プレビューリンク】</div>
    <div>・ファイル名: 企画提案書_2026.docx (1.2 MB)</div>
    <div class="text-emerald-600 dark:text-emerald-400 font-mono">👉 プレビュー & ダウンロード: https://fs.nigiri-rice.com/apps/files/files?dir=/Public/MailInbound/2026-09/i.shimamoto</div>
  </div>
</div>

<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>
<p class="mb-4">メール送受信および添付ファイル自動リンク化のアーキテクチャフローです：</p>
<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid text-sm">sequenceDiagram
    autonumber
    actor ExtSender as 外部送信者
    participant Postfix as Postfix (MTA:25)
    participant Dovecot as Dovecot (Maildir)
    participant Linker as Attachment Linker Daemon
    participant Nextcloud as Nextcloud FS (CT 144)
    actor Recipient as 社内ユーザー (Webmail / TB)

    ExtSender->>Postfix: 添付ファイル付きメール送信
    Postfix->>Dovecot: スパム・ウイルス検査後、Maildir へ配送
    Linker->>Dovecot: Maildir を検知 & 添付ファイル抽出
    Linker->>Nextcloud: SSH/SCP で /Public/MailInbound へ保存
    Nextcloud->>Nextcloud: inotify 検知 & Collabora プレビュー有効化
    Linker->>Dovecot: メール本文へ「脱PPAP 安全リンク」を追記
    Recipient->>Dovecot: Webmail (SOGo) または IMAP でメール閲覧
    Recipient->>Nextcloud: リンクをクリックしてブラウザで即座にプレビュー
</pre></div>

<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>
<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>
<div class="space-y-4 mb-6">
  <div class="code-block-wrapper">
  <div class="code-header"><span class="code-lang">bash</span></div>
  <pre><code class="language-bash"># 脱PPAP 添付ファイル自動リンク化タイマーの状態
systemctl status mailcow-attachment-linker.timer

# 手動スキャン実行
python3 /opt/mailcow-attachment-linker/attachment_linker.py

# 処理ログ確認
tail -f /var/log/mailcow-attachment-linker.log

# Postfix 送信キュー状態確認 (破壊的操作は行わない)
docker exec mailcowdockerized-postfix-mailcow-1 postqueue -p

# Mailcow コンテナ状態確認
cd /opt/mailcow-dockerized && docker compose ps
</code></pre>
</div>
</div>

<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>
<div class="space-y-4 mb-6">
  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">添付ファイル自動同期の不整合復旧</h3>
  <p>添付ファイルが Nextcloud 側で認識されない場合は、CT 144 上で以下の再スキャンを実行します：</p>
  <div class="code-block-wrapper">
    <div class="code-header"><span class="code-lang">bash</span></div>
    <pre><code class="language-bash"># CT 144 内で MailInbound フォルダを再インデックス
sudo -u www-data php /var/www/nextcloud/occ files:scan --path="/admin/files/Public/MailInbound"
</code></pre>
  </div>
</div>
''',
                'description': 'Docker コンテナ群（Postfix, Dovecot, SOGo）で構成される企業メール基盤。脱PPAP添付自動リンク化・Nextcloud Officeプレビュー対応。',
                'icon': 'mail',
                'id': 'mailcow',
                'last_updated': '2026-09-19',
                'service_id': 'webmail',
                'title': 'Mailcow メールサーバー & 脱PPAP添付ファイルシステム',
                'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                         {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                         {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                         {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様 (脱PPAP運用マニュアル)'},
                         {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                         {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                         {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'monitoring': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-19', '全37項目監視', 'Production', 'Public'],
                  'category_id': 'standalone',
                  'category_name': 'メール & 独立サービス',
                  'content_html': '''
<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">
  本ドキュメントは、<strong>nigiri-rice.com</strong> プラットフォームの全システム（Cloud Web Services 16項目、Servers & Nodes 端末監視 13項目、Bot & 基盤デーモン 3項目、宅内オンプレミス PVE 5項目）を 24時間 365日体制で死活監視し、障害検知および一般公開ステータスページを提供する <strong>status.nigiri-rice.com (Uptime Kuma)</strong> の公式運用マニュアルです。
</p>

<div class="gh-alert gh-alert-note">
  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 shrink-0"></i><span>一般公開・認証不要ステータスページ</span></div>
  <div class="gh-alert-body">
    <code>https://status.nigiri-rice.com/</code> にアクセスすると、未ログイン・認証不要で全システムのリアルタイム稼働状況・稼働率バーが閲覧可能です。管理・モニター編集は <code>/dashboard</code> より管理者アカウントでログインして実施します。
  </div>
</div>

<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>
<div class="space-y-4 mb-6">
  <p>クラウド・オンプレミスを跨ぐインフラ全体の一元可視化、Bot稼働状況、物理端末および仮想ノード死活のリアルタイム監視を実現すること。</p>
  <ul class="list-disc pl-6 space-y-1">
    <li><strong>パブリック公開性:</strong> ユーザーおよび利用者がいつでもサービスの稼働状態を確認可能であること。</li>
    <li><strong>端末レベルの死活監視:</strong> クラウドノード・宅内物理ホスト・全LXCコンテナの疎通断を1分以内に検知すること。</li>
    <li><strong>Bot/デーモン監視:</strong> Discord Bot (OmusuBI Connecter) およびメール基盤のAPI/ポートを直接監視すること。</li>
  </ul>
</div>

<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">2. 技術スタック & アーキテクチャ</h2>
<p class="mb-4">
  監視基盤は <strong>Xserver VPS (<code>210.131.211.17</code>)</strong> 上でホストネットワークモード (<code>network_mode: host</code>) の Docker コンテナとして稼働しています。
</p>
<ul class="list-disc pl-6 space-y-2 mb-6">
  <li><strong>共倒れ防止 (Fail-Safe):</strong> 外部 VPS に配置することで、宅内光回線断や停電時でも 100% 確実に稼働状況を外部へ可視化。</li>
  <li><strong>Tailscale 内部メッシュ監視:</strong> VPS から <code>10.155.0.0/16</code> を経由し、PVE物理ホストや各CTへ直接Pingヘルスチェック。</li>
  <li><strong>Cloudflare & Caddy:</strong> <code>status.nigiri-rice.com</code> は Cloudflare (Proxied) → VPS Caddy → <code>localhost:3001</code> でセキュアに配信。</li>
</ul>

<h2 id="sec-3-monitors" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">3. 全37監視モニター & 4グループ一覧</h2>
<div class="table-responsive"><table class="gh-table"><thead><tr><th>グループ</th><th>監視項目数</th><th>主な監視対象</th><th>監視プロトコル</th></tr></thead><tbody>
<tr><td><strong>Cloud Web Services (VPS 公開サービス)</strong></td><td>16</td><td>Web Portal, Developer Portal, OmusuBI Console (id), Keycloak SSO, Nextcloud Hub (fs), AFFiNE, Mailcow, Vault, Harbor, Portainer (vps), Docs, CNT Connect/Pass</td><td>HTTP(s) GET / 60秒</td></tr>
<tr><td><strong>Servers & Cluster Nodes (端末死活監視)</strong></td><td>13</td><td>Cloud VPS Host, K8s Worker 01〜04, PVE 物理ホスト (10.155.0.10), CT 121 (Caddy Gateway), CT 144 (FS & AD), CT 150 (Tailscale VPN), CT 131, CT 132, CT 138, CT 120</td><td>ICMP Ping / 60秒</td></tr>
<tr><td><strong>Bot & Background Daemons (連携Bot・基盤)</strong></td><td>3</td><td>Discord Bot (OmusuBI Connecter), Mail SMTP (587), Mail IMAP (993)</td><td>HTTP(s) / TCP Port / 60秒</td></tr>
<tr><td><strong>On-Premise Infrastructure (宅内 PVE サービス)</strong></td><td>5</td><td>PVE Web UI, ArgoCD GitOps, Portal Home (CT 131), HomePortal (CT 132), JupyterHub</td><td>HTTP(s) / 60秒</td></tr>
</tbody></table></div>

<h2 id="sec-4-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 dark:border-emerald-950/70">4. 運用保守 & 再起動 Runbook</h2>
<div class="code-block-wrapper">
  <div class="code-header"><span class="code-lang">bash</span></div>
  <pre><code class="language-bash"># Uptime Kuma コンテナ状態確認
docker ps --filter name=uptime-kuma

# コンテナ再起動
docker restart uptime-kuma

# ログ追跡
docker logs -f uptime-kuma --tail=100

# データベースバックアップ
sqlite3 /opt/uptime-kuma/data/kuma.db ".backup /opt/uptime-kuma/data/kuma.db.bak"
</code></pre>
</div>
''',
                  'description': '全システム（クラウド・端末・Bot・宅内 PVE）を常時死活監視し、一般公開・認証不要で閲覧可能な status.nigiri-rice.com (Uptime Kuma) の運用マニュアルです。',
                  'icon': 'activity',
                  'id': 'monitoring',
                  'last_updated': '2026-09-19',
                  'service_id': None,
                  'title': '死活監視 & 公開ステータス基盤 (Uptime Kuma & status.nigiri-rice.com)',
                  'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                           {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & アーキテクチャ'},
                           {'id': 'sec-3-monitors', 'level': 2, 'title': '3. 全37監視モニター & 4グループ一覧'},
                           {'id': 'sec-4-runbook', 'level': 2, 'title': '4. 運用保守 & 再起動 Runbook'}]},
  'omusubi-console': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                       'category_id': 'identity',
                       'category_name': '認証 & ID 基盤',
                       'content_html': '\n'
                                       '<p class="lead text-lg text-slate-600 dark:text-slate-300 '
                                       'mb-6">統合アカウント管理、ユーザー一覧/無効ユーザー分離エクスポート、Excel一括属性更新、アカウント有効化/無効化予約を制御するWebコンソール。</p>\n'
                                       '\n'
                                       '<div class="gh-alert gh-alert-note">\n'
                                       '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                       'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                       '  <div class="gh-alert-body">本ページは Qiita '
                                       '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <h3 class="text-lg font-semibold text-emerald-600 '
                                       'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                       '  <p>エンジニアおよび人事・管理部門向けに、Keycloak 上のユーザー・グループ・ロール・予約属性（EnableAt, '
                                       'DisableAt）を直感的に操作・一括管理するインターフェースを提供すること。</p>\n'
                                       '  <h3 class="text-lg font-semibold text-emerald-600 '
                                       'dark:text-emerald-400">成功の基準 (KPI / 動作基準)</h3>\n'
                                       '  <ul class="list-disc pl-6 space-y-1">\n'
                                       '    <li>ユーザー一覧（有効9名）、無効ユーザー（1名）、全件の完全分離エクスポート</li><li>Excel (.xlsx) および CSV '
                                       '出力時の Orion 表記完全排除と EnableAt/DisableAt 列保持</li><li>アカウント即時作成および予約属性の安全な '
                                       'Keycloak 反映</li>\n'
                                       '  </ul>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                       '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                       '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                       'レイヤー</th><th>採用技術 / '
                                       'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>バックエンド</td><td>Python '
                                       'FastAPI</td><td>非同期処理による Keycloak Admin REST API '
                                       'の高速ラッパー</td></tr><tr><td>フロントエンド</td><td>Tailwind CSS + Vanilla JS / Vue '
                                       'SPA</td><td>軽量かつレスポンシブな管理ダッシュボード</td></tr><tr><td>配備イメージ</td><td>localhost/omusubi-console:20260910-v2</td><td>HA '
                                       '2 Pods (vps-worker-01, vps-worker-02 '
                                       '分散)</td></tr><tr><td>連携プロトコル</td><td>Keycloak Admin REST API (Bearer '
                                       'Token)</td><td>master レルムの管理アカウントによる安全な API '
                                       '制御</td></tr></tbody></table></div>\n'
                                       '\n'
                                       '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <h4 class="font-semibold text-slate-800 '
                                       'dark:text-slate-200">ユーザー属性データ仕様</h4>\n'
                                       '<p>Console は独自の DB を持たず、Keycloak の User Attributes をマスターデータとして直接参照・更新します。</p>\n'
                                       '<ul class="list-disc pl-6 space-y-1">\n'
                                       '  <li><code>EnableAt</code>: アカウント有効化予定日時 (ISO 8601 または YYYY-MM-DD)</li>\n'
                                       '  <li><code>DisableAt</code>: アカウント失効・無効化予定日時</li>\n'
                                       '  <li><code>discord_id</code>: Discord コミュニティ連携用アカウントID</li>\n'
                                       '</ul>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">画面一覧 & '
                                       'ダウンロードエンドポイント</h4>\n'
                                       '<ul class="list-disc pl-6 space-y-1">\n'
                                       '  <li>公開 URL: <code>https://console.nigiri-rice.com/</code> (または '
                                       '<code>https://id.nigiri-rice.com/</code>)</li>\n'
                                       '  <li>有効ユーザー一覧: <code>/users</code> (ダウンロード: '
                                       '<code>/api/export/users.xlsx?enabled=true</code>)</li>\n'
                                       '  <li>無効ユーザー一覧: <code>/disabled-users</code> (ダウンロード: '
                                       '<code>/api/export/users.xlsx?enabled=false</code>)</li>\n'
                                       '  <li>一括更新・全件: <code>/csv</code> (ダウンロード: '
                                       '<code>/api/export/users.xlsx?enabled=all</code>)</li>\n'
                                       '</ul>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                       '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                       '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                       'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                       'class="mermaid text-sm">sequenceDiagram\n'
                                       '    autonumber\n'
                                       '    actor Admin as 管理者\n'
                                       '    participant Console as OmusuBI Console (2 Pods)\n'
                                       '    participant KC as Keycloak REST API\n'
                                       '\n'
                                       '    Admin->>Console: /users 画面を開く\n'
                                       '    Console->>KC: GET /admin/realms/master/users (enabled=true)\n'
                                       '    KC-->>Console: ユーザーリスト返却\n'
                                       '    Console-->>Admin: 一覧描画 (有効9名)\n'
                                       '    Admin->>Console: 「Excelエクスポート」クリック\n'
                                       '    Console->>Console: 不要ロール/グループ除外 & EnableAt/DisableAt 整形\n'
                                       '    Console-->>Admin: keycloak-users-active.xlsx ダウンロード</pre></div>\n'
                                       '\n'
                                       '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 '
                                       '(Runbook)</h2>\n'
                                       '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash"># 1. Console Pod 状態確認\n'
                                       'kubectl get pods -n omusubi -l app.kubernetes.io/name=omusubi-console -o wide\n'
                                       '\n'
                                       '# 2. ログ確認\n'
                                       'kubectl logs -n omusubi -l app.kubernetes.io/name=omusubi-console -f '
                                       '--tail=50\n'
                                       '\n'
                                       '# 3. Pod 再起動\n'
                                       'kubectl -n omusubi rollout restart deployment omusubi-console</code></pre>\n'
                                       '</div>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                       '<div class="space-y-4 mb-6">\n'
                                       '  <div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash"># イメージ更新 &amp; 反映\n'
                                       'kubectl set image deployment/omusubi-console '
                                       'omusubi-console=localhost/omusubi-console:20260910-v2 -n omusubi\n'
                                       'kubectl rollout status deployment/omusubi-console -n omusubi</code></pre>\n'
                                       '</div>\n'
                                       '</div>\n',
                       'description': '統合アカウント管理、ユーザー一覧/無効ユーザー分離エクスポート、Excel一括属性更新、アカウント有効化/無効化予約を制御するWebコンソール。',
                       'icon': 'users',
                       'id': 'omusubi-console',
                       'last_updated': '2026-09-12',
                       'service_id': 'omusubi_console',
                       'title': 'OmusuBI Console 運用保守マニュアル',
                       'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                                {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                                {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                                {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                                {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                                {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                                {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'overview': { 'badges': ['システム全体', 'Verified: 2026-09-12', 'Production'],
                'category_id': 'guidelines',
                'category_name': '設計標準 & 運用ガイドライン',
                'content_html': '\n'
                                '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n'
                                '本ドキュメントは、<strong>nigiri-rice.com</strong> プラットフォームの全インフラストラクチャ（Xserver VPS、オンプレミス '
                                'Proxmox VE、k3s Kubernetes クラスタ、Argo CD GitOps、独立 Docker '
                                'サービス群）の全体像と詳細インベントリをまとめた公式マスタードキュメントです。\n'
                                '</p>\n'
                                '\n'
                                '<div class="gh-alert gh-alert-note">\n'
                                '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                'shrink-0"></i><span>実機ファクトチェック済み</span></div>\n'
                                '  <div class="gh-alert-body">記載されているIPアドレス、ポート番号、ノード名、ストレージパス、物理回線・ハードウェア構成はすべて '
                                '2026年9月現在の実稼働環境と完全に一致しています。</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-infra-overview" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">1. インフラストラクチャ全体図 (Pan & Zoom 対応)</h2>\n'
                                '<p class="mb-4">\n'
                                '外部からの全アクセスは Cloudflare エッジで WAF・DDoS 防護および DNS 解決され、VPS ホスト（<code>nigiri-vps</code>）の '
                                'Caddy リバースプロキシを経由して k3s クラスタ内部または独立コンテナへルーティングされます。<br>\n'
                                'また、オンプレミス宅内環境（<strong>ドコモ光 10ギガ / GMOとくとくBB / TP-Link 10G ルーター / Proxmox VE '
                                '8.x</strong>）とは <strong>Tailscale Mesh VPN</strong> により安全に暗号化メッシュ接続されています。\n'
                                '</p>\n'
                                '\n'
                                '<div class="mermaid-wrapper my-6">\n'
                                '  <pre class="mermaid text-sm">graph TB\n'
                                '    subgraph Clients [&quot;クライアント &amp; 外部アクセス&quot;]\n'
                                '        User[&quot;一般ユーザー / 業務端末&quot;]\n'
                                '        Dev[&quot;開発者 / システム管理者&quot;]\n'
                                '    end\n'
                                '\n'
                                '    subgraph Cloudflare [&quot;Cloudflare Edge Network&quot;]\n'
                                '        CF_DNS[&quot;Cloudflare DNS&lt;br/&gt;(Proxy: Proxied)&quot;]\n'
                                '        CF_WAF[&quot;Cloudflare WAF / DDoS 防護&lt;br/&gt;(SSL/TLS Strict 暗号化)&quot;]\n'
                                '        CF_Tunnel[&quot;Cloudflare Tunnel&lt;br/&gt;(argocd.nigiri-rice.com)&quot;]\n'
                                '        CF_DNS --&gt; CF_WAF\n'
                                '    end\n'
                                '\n'
                                '    subgraph VPS [&quot;Xserver VPS (210.131.211.17) - Ubuntu 24.04.4 LTS&quot;]\n'
                                '        Caddy[&quot;Caddy v2&lt;br/&gt;Edge Reverse Proxy (Port 80, 443)&quot;]\n'
                                '        \n'
                                '        subgraph K3s_Cluster [&quot;k3s Kubernetes クラスタ (v1.36.4+k3s1)&quot;]\n'
                                '            Node_Master[&quot;Control Plane: nigiri-vps (Host)&quot;]\n'
                                '            Node_W1[&quot;Worker 01&lt;br/&gt;vps-worker-01 (172.30.0.2)&quot;]\n'
                                '            Node_W2[&quot;Worker 02&lt;br/&gt;vps-worker-02 (172.30.0.3)&quot;]\n'
                                '            Node_W3[&quot;Worker 03&lt;br/&gt;vps-worker-03 (172.30.0.4)&quot;]\n'
                                '            Node_W4[&quot;Worker 04&lt;br/&gt;vps-worker-04 (172.30.0.5)&quot;]\n'
                                '            Ingress_Nginx[&quot;Ingress-NGINX (NodePort 30180)&quot;]\n'
                                '            \n'
                                '            subgraph K8s_Workloads [&quot;主要 K8s ワークロード (12 アプリケーション)&quot;]\n'
                                '                SSO[&quot;Keycloak SSO&lt;br/&gt;(sso.nigiri-rice.com)&quot;]\n'
                                '                Vault[&quot;HashiCorp Vault&lt;br/&gt;(vault.nigiri-rice.com)&quot;]\n'
                                '                Console[&quot;OmusuBI '
                                'Console&lt;br/&gt;(console.nigiri-rice.com)&quot;]\n'
                                '                Harbor[&quot;Harbor '
                                'Registry&lt;br/&gt;(registry.nigiri-rice.com)&quot;]\n'
                                '                CNT_Prod[&quot;CNT Connect '
                                'Prod&lt;br/&gt;(cnt-connect.nigiri-rice.com)&quot;]\n'
                                '                CNT_Dev[&quot;CNT Connect '
                                'Dev&lt;br/&gt;(dev.cnt-connect.nigiri-rice.com)&quot;]\n'
                                '                WP[&quot;WordPress&lt;br/&gt;(www.nigiri-rice.com)&quot;]\n'
                                '                Portal[&quot;Developer '
                                'Portal&lt;br/&gt;(www.nigiri-rice.com/portal/)&quot;]\n'
                                '            end\n'
                                '        end\n'
                                '\n'
                                '        subgraph Docker_Standalone [&quot;VPS 独立 Docker サービス&quot;]\n'
                                '            '
                                'Mailcow[&quot;Mailcow-dockerized&lt;br/&gt;mail.nigiri-rice.com&lt;br/&gt;(SMTP:25,587, '
                                'IMAP:993, Web:8448)&quot;]\n'
                                '            AFFiNE[&quot;AFFiNE Knowledge Base&lt;br/&gt;affine.nigiri-rice.com (Port '
                                '8083)&quot;]\n'
                                '            Portainer_Host[&quot;Portainer '
                                'Server&lt;br/&gt;manage.nigiri-rice.com:8082&quot;]\n'
                                '            Monitoring[&quot;Prometheus / cAdvisor&lt;br/&gt;Node Exporter&quot;]\n'
                                '            Shumoku[&quot;Shumoku Discord Bot&lt;br/&gt;(Node.js)&quot;]\n'
                                '        end\n'
                                '    end\n'
                                '\n'
                                '    subgraph Home_Environment [&quot;オンプレミス 宅内インフラ基盤 (ドコモ光 10ギガ / GMOとくとくBB)&quot;]\n'
                                '        subgraph Home_Network_10G [&quot;物理光回線 &amp; 宅内ネットワーク (10Gbps WAN / 10G '
                                'LAN)&quot;]\n'
                                '            Docomo10G[&quot;ドコモ光 10ギガ&lt;br/&gt;GMOとくとくBB v6プラス&lt;br/&gt;(IPoE / '
                                'IPv4 over IPv6)&quot;]\n'
                                '            ONU_10G[&quot;NTT 10G 光回線終端装置&lt;br/&gt;(10G-EPON ONU)&quot;]\n'
                                '            Router_TP[&quot;TP-Link 10G ルーター&lt;br/&gt;(10.155.0.1 / WAN 10G SFP+, '
                                'LAN 10G/2.5G)&quot;]\n'
                                '            Switch_LAN[&quot;宅内 スイッチングハブ&lt;br/&gt;(10.155.0.0/16)&quot;]\n'
                                '\n'
                                '            Docomo10G --&gt;|10Gbps 光ファイバー| ONU_10G\n'
                                '            ONU_10G --&gt;|10GBASE-T WAN| Router_TP\n'
                                '            Router_TP --&gt;|10G/2.5G LAN| Switch_LAN\n'
                                '        end\n'
                                '\n'
                                '        subgraph PVE_Cluster [&quot;Proxmox VE 8.x 物理ホスト (10.155.0.10 - Ryzen 8C/16T, '
                                '32GB RAM, ZFS)&quot;]\n'
                                '            GPU_Hardware[&quot;NVIDIA GeForce RTX 2060 Mobile&lt;br/&gt;(TU106M / 6GB '
                                'VRAM, IOMMU Group 8)&quot;]\n'
                                '\n'
                                '            subgraph PVE_Infra_Guests [&quot;基幹 VM / 管理 LXC コンテナ群 '
                                '(10.155.0.0/16)&quot;]\n'
                                '                CT_Proxy[&quot;CT 121: reverse-proxy (Caddy '
                                'v2)&lt;br/&gt;(*.home.nigiri-rice.com / SSL自動証明書)&quot;]\n'
                                '                CT_Portal131[&quot;CT 131: aaa-portal (React '
                                'Dashboard)&lt;br/&gt;(portal.home.nigiri-rice.com)&quot;]\n'
                                '                CT_HomePortal[&quot;CT 132: home-portal (Django '
                                '機器/発電監視)&lt;br/&gt;(homeportal.home.nigiri-rice.com)&quot;]\n'
                                '                CT_VPN[&quot;CT 150: tailscale-vpn (Subnet '
                                'Router)&lt;br/&gt;(宅内メッシュ直結 10.155.0.0/16)&quot;]\n'
                                '                VM_AD[&quot;CT 144: fs-ad-server&lt;br/&gt;(Windows Server AD DS / '
                                'DNS)&quot;]\n'
                                '                VM_WAC[&quot;&lt;br/&gt;(Windows Admin '
                                'Center)&quot;]\n'
                                '            end\n'
                                '\n'
                                '            subgraph PVE_K8s_Cluster [&quot;PVE 宅内 Kubernetes クラスタ (k3s v1.36.4 - '
                                '8ノード構成)&quot;]\n'
                                '                subgraph K8s_CP_Group [&quot;Control Plane (3ノード etcd HA '
                                'クラスタ)&quot;]\n'
                                '                    CP01[&quot;CT 200: k8s-cp-01&lt;br/&gt;(10.155.200.201 / '
                                'Leader)&quot;]\n'
                                '                    CP02[&quot;CT 211: k8s-cp-02&lt;br/&gt;(10.155.200.202 / '
                                'etcd)&quot;]\n'
                                '                    CP03[&quot;CT 212: k8s-cp-03&lt;br/&gt;(10.155.200.203 / '
                                'etcd)&quot;]\n'
                                '                end\n'
                                '\n'
                                '                subgraph K8s_Worker_Group [&quot;Worker ノード (5ノード)&quot;]\n'
                                '                    W_GPU[&quot;VM 201: k8s-worker-gpu-01&lt;br/&gt;(10.155.200.204 / '
                                'GPU Worker)&quot;]\n'
                                '                    W02[&quot;CT 202: k8s-worker-02 (10.155.200.205)&quot;]\n'
                                '                    W03[&quot;CT 203: k8s-worker-03 (10.155.200.206)&quot;]\n'
                                '                    W04[&quot;CT 204: k8s-worker-04 (10.155.200.207)&quot;]\n'
                                '                    W05[&quot;CT 205: k8s-worker-05 (10.155.200.208)&quot;]\n'
                                '                end\n'
                                '\n'
                                '                subgraph K8s_Home_Workloads [&quot;主要 K8s アプリケーション &amp; '
                                'ストレージ&quot;]\n'
                                '                    PVE_Ingress[&quot;Ingress-NGINX&lt;br/&gt;(NodePort 30180 / '
                                '30444)&quot;]\n'
                                '                    PVE_ArgoCD[&quot;Argo CD (GitOps '
                                '運用自動化)&lt;br/&gt;(argocd.home.nigiri-rice.com)&quot;]\n'
                                '                    PVE_Jupyter[&quot;JupyterHub (GPU '
                                'AI開発環境)&lt;br/&gt;(jupyterhub.home.nigiri-rice.com)&quot;]\n'
                                '                    PVE_Harbor[&quot;Harbor '
                                '(コンテナレジストリ)&lt;br/&gt;(registry.home.nigiri-rice.com)&quot;]\n'
                                '                    PVE_SMB[&quot;SMB CSI Storage&lt;br/&gt;(TrueNAS / SMB '
                                '永続PVマウント)&quot;]\n'
                                '                end\n'
                                '            end\n'
                                '\n'
                                '            GPU_Hardware -.-&gt;|PCI Passthrough| W_GPU\n'
                                '            CT_Proxy --&gt;|NodePort 30180| PVE_Ingress\n'
                                '            PVE_Ingress --&gt; PVE_ArgoCD &amp; PVE_Jupyter &amp; PVE_Harbor\n'
                                '        end\n'
                                '\n'
                                '        Switch_LAN --&gt;|10G/2.5G 物理リンク| PVE_Cluster\n'
                                '    end\n'
                                '\n'
                                '    User --&gt; CF_DNS\n'
                                '    CF_WAF --&gt; Caddy\n'
                                '    Dev --&gt; CF_Tunnel --&gt; Node_Master\n'
                                '    Caddy --&gt; Ingress_Nginx\n'
                                '    Caddy --&gt; Mailcow\n'
                                '    Caddy --&gt; AFFiNE\n'
                                '    Caddy --&gt; Portainer_Host\n'
                                '    Ingress_Nginx --&gt; Node_W1 &amp; Node_W2 &amp; Node_W3 &amp; Node_W4\n'
                                '    \n'
                                '    CT_VPN &lt;--&gt;|&quot;Tailscale Mesh VPN 暗号化トンネル (宅内ポート開放不要・メッシュ直結)&quot;| '
                                'Caddy\n'
                                '    Dev -.-&gt;|&quot;Tailscale VPN 経由 / RDP・SSH&quot;| Router_TP</pre>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-inventory" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">2. ホスト & ノードインベントリ</h2>\n'
                                '<p class="mb-4">本システムはパブリック VPS（Xserver VPS）とオンプレミス仮想化基盤（Proxmox VE '
                                '8.x）が連携して稼働しています。</p>\n'
                                '\n'
                                '<div class="table-responsive">\n'
                                '  <table class="gh-table">\n'
                                '    <thead>\n'
                                '      <tr>\n'
                                '        <th>ホスト / 識別名</th>\n'
                                '        <th>種別 / 役割</th>\n'
                                '        <th>IP / ネットワーク</th>\n'
                                '        <th>OS / ハードウェア仕様</th>\n'
                                '        <th>主要サービス & 備考</th>\n'
                                '      </tr>\n'
                                '    </thead>\n'
                                '    <tbody>\n'
                                '      <tr class="bg-emerald-500/5">\n'
                                '        <td colspan="5" class="font-bold text-emerald-600 dark:text-emerald-400 '
                                'py-2">▼ Xserver VPS クラウド基盤 (210.131.211.17)</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>nigiri-vps</strong></td>\n'
                                '        <td>外部エッジ VPS / k3s Control Plane</td>\n'
                                '        <td>210.131.211.17</td>\n'
                                '        <td>Ubuntu 24.04.4 LTS (6.8.0-139)</td>\n'
                                '        <td>Caddy v2, k3s CP, Mailcow, AFFiNE, Portainer, SMB CSI Node</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>vps-worker-01</strong></td>\n'
                                '        <td>k3s Worker 01 (Docker DinD)</td>\n'
                                '        <td>172.30.0.2</td>\n'
                                '        <td>k3s v1.36.4+k3s1</td>\n'
                                '        <td>Keycloak SSO, Ingress-NGINX, Developer Portal, Vault Injector</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>vps-worker-02</strong></td>\n'
                                '        <td>k3s Worker 02 (Docker DinD)</td>\n'
                                '        <td>172.30.0.3</td>\n'
                                '        <td>k3s v1.36.4+k3s1</td>\n'
                                '        <td>OmusuBI Console, Harbor Registry, CNT Connect dev</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>vps-worker-03</strong></td>\n'
                                '        <td>k3s Worker 03 (Docker DinD)</td>\n'
                                '        <td>172.30.0.4</td>\n'
                                '        <td>k3s v1.36.4+k3s1</td>\n'
                                '        <td>CNT Connect prod, Harbor Database, Vault Injector</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>vps-worker-04</strong></td>\n'
                                '        <td>k3s Worker 04 (Docker DinD)</td>\n'
                                '        <td>172.30.0.5</td>\n'
                                '        <td>k3s v1.36.4+k3s1</td>\n'
                                '        <td>WordPress, MariaDB, CoreDNS</td>\n'
                                '      </tr>\n'
                                '      <tr class="bg-emerald-500/5">\n'
                                '        <td colspan="5" class="font-bold text-emerald-600 dark:text-emerald-400 '
                                'py-2">▼ オンプレミス 宅内インフラ基盤 (ドコモ光 10ギガ / GMOとくとくBB)</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>ドコモ光 10ギガ回線</strong></td>\n'
                                '        <td>10Gbps 超高速光回線</td>\n'
                                '        <td>WAN 光ファイバー</td>\n'
                                '        <td>GMOとくとくBB (v6プラス / IPoE / IPv4 over IPv6)</td>\n'
                                '        <td>大容量通信、低遅延、高スループット</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>10G-EPON ONU</strong></td>\n'
                                '        <td>光回線終端装置</td>\n'
                                '        <td>10GBASE-T WAN</td>\n'
                                '        <td>NTT / ドコモ光 10G 専用 ONU</td>\n'
                                '        <td>光信号 ↔ 10Gbps LAN 変換</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>TP-Link 10G ルーター</strong></td>\n'
                                '        <td>宅内コアゲートウェイ</td>\n'
                                '        <td>10.155.0.1</td>\n'
                                '        <td>WAN 10G, LAN 10G/2.5G ポート搭載</td>\n'
                                '        <td>宅内 DHCP, NAT, ルーティング, スイッチングハブ連携</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>PVE Host</strong></td>\n'
                                '        <td>Proxmox VE 8.x 仮想化基盤</td>\n'
                                '        <td>10.155.0.10</td>\n'
                                '        <td>pve-manager 9.2.11 / Kernel 7.0.14-15-pve<br>AMD Ryzen (8C/16T), 32GB '
                                'RAM, ZFS<br>NVIDIA GeForce RTX 2060 Mobile (6GB VRAM)</td>\n'
                                '        <td>KVM / LXC ハイパーバイザ<br>RTX 2060 Mobile GPU Passthrough (IOMMU 8)</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>VM 140</strong></td>\n'
                                '        <td>Active Directory ドメインコントローラ</td>\n'
                                '        <td>10.155.0.140</td>\n'
                                '        <td>Windows Server</td>\n'
                                '        <td>AD DS, DNS, Kerberos, LDAP, RDP 認証基盤</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>VM 141</strong></td>\n'
                                '        <td>Windows Admin Center</td>\n'
                                '        <td>10.155.0.141</td>\n'
                                '        <td>Windows 11 Pro</td>\n'
                                '        <td>Windows サーバー統合管理ゲートウェイ</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 150</strong></td>\n'
                                '        <td>Tailscale Subnet Router</td>\n'
                                '        <td>10.155.0.150</td>\n'
                                '        <td>AlmaLinux 9.4 (Tailscale 1.96.4)</td>\n'
                                '        <td>拠点間メッシュVPN・宅内サブネット広報 (10.155.0.0/24)</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 137</strong></td>\n'
                                '        <td>宅内 Wiki データベース</td>\n'
                                '        <td>10.155.0.137</td>\n'
                                '        <td>Debian / PostgreSQL 16.15</td>\n'
                                '        <td>社内 Wiki.js 専用データストア</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 121</strong></td>\n'
                                '        <td>宅内 Edge リバースプロキシ</td>\n'
                                '        <td>10.155.0.121</td>\n'
                                '        <td>Debian 12 / Caddy v2</td>\n'
                                '        <td>*.home.nigiri-rice.com SSL終端・内部ルーティング</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 131</strong></td>\n'
                                '        <td>AAA Portal (ポータルUI)</td>\n'
                                '        <td>10.155.0.131</td>\n'
                                '        <td>Debian 12 (Docker: Express + Caddy)</td>\n'
                                '        <td>portal.home.nigiri-rice.com (portal-dashboard)</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 132</strong></td>\n'
                                '        <td>Home Portal (宅内IoT基盤)</td>\n'
                                '        <td>10.155.0.132</td>\n'
                                '        <td>Debian 12 / Python Django (Port 8000)</td>\n'
                                '        <td>homeportal.home.nigiri-rice.com (IoT機器/発電/ネットワーク管理)</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 138</strong></td>\n'
                                '        <td>Home Auth Proxy</td>\n'
                                '        <td>10.155.0.138</td>\n'
                                '        <td>Debian 12</td>\n'
                                '        <td>宅内アクセス認証・リバースプロキシ連携</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 200 / 211 / 212</strong></td>\n'
                                '        <td>PVE K8s Control Plane (3ノード etcd HA)</td>\n'
                                '        <td>10.155.200.201, .202, .203</td>\n'
                                '        <td>Debian 12 / k3s v1.36.4 (etcd クラスター)</td>\n'
                                '        <td>k8s-cp-01 (Leader), k8s-cp-02, k8s-cp-03</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>VM 201</strong></td>\n'
                                '        <td>PVE K8s GPU Worker (k8s-worker-gpu-01)</td>\n'
                                '        <td>10.155.200.204</td>\n'
                                '        <td>Ubuntu 24.04.5 LTS / Kernel 6.8 (RTX 2060 Mobile)</td>\n'
                                '        <td>JupyterHub AI/機械学習推論、GPU パススルーワークロード</td>\n'
                                '      </tr>\n'
                                '      <tr>\n'
                                '        <td><strong>CT 202 〜 205</strong></td>\n'
                                '        <td>PVE K8s Worker ノード群 (4ノード)</td>\n'
                                '        <td>10.155.200.205 〜 .208</td>\n'
                                '        <td>Debian 12 / k3s Agent</td>\n'
                                '        <td>k8s-worker-02〜05 (ArgoCD, Harbor, Ingress-NGINX, SMB CSI)</td>\n'
                                '      </tr>\n'
                                '    </tbody>\n'
                                '  </table>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-routing" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">3. ネットワーク & ルーティングフロー</h2>\n'
                                '<p class="mb-4">Web トラフィックおよび拠点間通信は以下の 5 系統のルートで配送されます：</p>\n'
                                '<ul class="list-disc pl-6 space-y-2 mb-6">\n'
                                '  <li><strong>K8s Ingress 転送 (Harbor, Vault)</strong>: Caddy → '
                                '<code>127.0.0.1:30180</code> (Ingress-NGINX NodePort) → K8s ClusterIP Service</li>\n'
                                '  <li><strong>K8s ClusterIP 直結 (OmusuBI, CNT, WordPress, Portal)</strong>: Caddy → '
                                'K8s 内部 ClusterIP (<code>10.43.x.x</code>)</li>\n'
                                '  <li><strong>VPS 独立サービス (AFFiNE, Portainer, Webmail)</strong>: Caddy → ローカルホストポート '
                                '(<code>localhost:8083</code>, <code>localhost:8082</code>, '
                                '<code>127.0.0.1:8448</code>)</li>\n'
                                '  <li><strong>Argo CD 管理トラフィック</strong>: <code>argocd.nigiri-rice.com</code> → '
                                'Cloudflare Tunnel (cloudflared) → <code>argocd-server:443</code></li>\n'
                                '  <li><strong>拠点間 Tailscale Mesh VPN (VPS ↔ 宅内 PVE)</strong>:\n'
                                '    VPS (<code>210.131.211.17</code>) と宅内オンプレミス（ドコモ光10G / TP-Linkルーター配下の '
                                '<code>10.155.0.0/24</code>）は、CT 150 の Tailscale Subnet Router により '
                                '<strong>ポート開放不要・暗号化メッシュ直結</strong> で相互ルーティングされています。開発者は Tailscale 経由で VM 140 (AD)、VM '
                                '141 (WAC)、PVE ホスト (10.155.0.10) へ安全に RDP/SSH/Web 接続できます。\n'
                                '  </li>\n'
                                '</ul>\n'
                                '\n'
                                '<h2 id="sec-services-list" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">4. 全12サービス一覧</h2>\n'
                                '<p class="mb-4">Argo CD '
                                '(<code>https://github.com/nigiri-rice-com/k8s-cluster-yaml.git</code>) によって GitOps '
                                '管理されている 12 のアプリケーションです：</p>\n'
                                '\n'
                                '<div class="table-responsive">\n'
                                '  <table class="gh-table">\n'
                                '    <thead>\n'
                                '      <tr>\n'
                                '        <th>#</th>\n'
                                '        <th>アプリケーション名</th>\n'
                                '        <th>Namespace</th>\n'
                                '        <th>公開 URL</th>\n'
                                '        <th>ステータス</th>\n'
                                '      </tr>\n'
                                '    </thead>\n'
                                '    <tbody>\n'
                                '      '
                                '<tr><td>1</td><td><strong>nigiri-vps-root</strong></td><td>argocd</td><td>-</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>2</td><td><strong>cloudflare-argocd-tunnel</strong></td><td>cloudflare</td><td>https://argocd.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>3</td><td><strong>ingress-nginx</strong></td><td>nginx-ingress</td><td>NodePort '
                                "30180</td><td><span class='gh-badge gh-badge-green'>Synced / "
                                'Healthy</span></td></tr>\n'
                                '      '
                                '<tr><td>4</td><td><strong>smb-csi-driver</strong></td><td>smb-storage</td><td>-</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>5</td><td><strong>vault-vps</strong></td><td>vault</td><td>https://vault.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>6</td><td><strong>harbor-vps</strong></td><td>harbor</td><td>https://registry.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>7</td><td><strong>omusubi-keycloak</strong></td><td>omusubi</td><td>https://sso.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>8</td><td><strong>omusubi-console</strong></td><td>omusubi</td><td>https://console.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>9</td><td><strong>nigiri-homepage</strong></td><td>nigiri-homepage</td><td>https://www.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>10</td><td><strong>nigiri-portal</strong></td><td>nigiri-homepage</td><td>https://www.nigiri-rice.com/portal/</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>11</td><td><strong>cnt-connect-dev</strong></td><td>cnt-connect-dev</td><td>https://dev.cnt-connect.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '      '
                                '<tr><td>12</td><td><strong>cnt-connect-prod</strong></td><td>cnt-connect-prod</td><td>https://cnt-connect.nigiri-rice.com</td><td><span '
                                "class='gh-badge gh-badge-green'>Synced / Healthy</span></td></tr>\n"
                                '    </tbody>\n'
                                '  </table>\n'
                                '</div>\n',
                'description': 'nigiri-rice.com における VPS / PVE / k3s / Argo CD / 12サービス全体の構成一覧とルーティング設計です。',
                'icon': 'server',
                'id': 'overview',
                'last_updated': '2026-09-12',
                'service_id': None,
                'title': 'システム全体アーキテクチャ & インベントリ',
                'toc': [ {'id': 'sec-infra-overview', 'level': 2, 'title': '1. インフラストラクチャ全体図'},
                         {'id': 'sec-inventory', 'level': 2, 'title': '2. ホスト & ノードインベントリ'},
                         {'id': 'sec-routing', 'level': 2, 'title': '3. ネットワーク & ルーティングフロー'},
                         {'id': 'sec-services-list', 'level': 2, 'title': '4. 全12サービス一覧'}]},
  'periodic-maintenance': { 'badges': ['定期保守', 'Verified: 2026-09-12', 'Runbook'],
                            'category_id': 'guidelines',
                            'category_name': '設計標準 & 運用ガイドライン',
                            'content_html': '\n'
                                            '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n'
                                            '毎月またはセキュリティパッチ公開時に実施する、ホスト OS '
                                            'およびミドルウェアの定期メンテナンス手順です。必ず深夜帯などの低トラフィック時に事前バックアップを取得の上で実施します。\n'
                                            '</p>\n'
                                            '\n'
                                            '<h2 id="sec-vps-apt" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                            'border-slate-200 dark:border-emerald-950/70">1. VPS ホスト OS 更新手順</h2>\n'
                                            '<div class="code-block-wrapper">\n'
                                            '  <div class="code-header">\n'
                                            '    <span class="code-lang">bash</span>\n'
                                            '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                            '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                            '      <span>コピー</span>\n'
                                            '    </button>\n'
                                            '  </div>\n'
                                            '  <pre><code class="language-bash"># パッケージ更新 &amp; アップグレード\n'
                                            'apt-get update\n'
                                            'DEBIAN_FRONTEND=noninteractive apt-get upgrade -y\n'
                                            'apt-get autoremove -y &amp;&amp; apt-get clean\n'
                                            '\n'
                                            '# 再起動要否の確認\n'
                                            'if [ -f /var/run/reboot-required ]; then\n'
                                            '    echo "OS 再起動が必要です:"\n'
                                            '    cat /var/run/reboot-required.pkgs\n'
                                            'fi</code></pre>\n'
                                            '</div>\n'
                                            '\n'
                                            '<h2 id="sec-pve-update" class="text-2xl font-bold mt-10 mb-4 pb-2 '
                                            'border-b border-slate-200 dark:border-emerald-950/70">2. Proxmox VE (PVE) '
                                            '更新手順</h2>\n'
                                            '<div class="gh-alert gh-alert-caution">\n'
                                            '  <div class="gh-alert-title"><i data-lucide="shield-alert" class="w-4 '
                                            'h-4 shrink-0"></i><span>PVE 更新前の注意</span></div>\n'
                                            '  <div class="gh-alert-body">PVE ホストを更新・再起動する前に、必ず CT 144 (Active '
                                            'Directory) および重要コンテナのバックアップが存在することを確認してください。</div>\n'
                                            '</div>\n'
                                            '<div class="code-block-wrapper">\n'
                                            '  <div class="code-header">\n'
                                            '    <span class="code-lang">bash</span>\n'
                                            '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                            '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                            '      <span>コピー</span>\n'
                                            '    </button>\n'
                                            '  </div>\n'
                                            '  <pre><code class="language-bash">apt-get update\n'
                                            'apt-get dist-upgrade -y\n'
                                            'systemctl status pveproxy pvedaemon pvestatd</code></pre>\n'
                                            '</div>\n'
                                            '\n'
                                            '<h2 id="sec-k3s-update" class="text-2xl font-bold mt-10 mb-4 pb-2 '
                                            'border-b border-slate-200 dark:border-emerald-950/70">3. k3s Kubernetes '
                                            'クラスタ更新手順</h2>\n'
                                            '<p class="mb-4">Control Plane (<code>nigiri-vps</code>) '
                                            'から順次ローリングアップデートを行います：</p>\n'
                                            '<div class="code-block-wrapper">\n'
                                            '  <div class="code-header">\n'
                                            '    <span class="code-lang">bash</span>\n'
                                            '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                            '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                            '      <span>コピー</span>\n'
                                            '    </button>\n'
                                            '  </div>\n'
                                            '  <pre><code class="language-bash"># 安定版チャンネルで Control Plane を更新\n'
                                            'curl -sfL https://get.k3s.io | INSTALL_K3S_CHANNEL=stable sh -\n'
                                            'systemctl restart k3s\n'
                                            'kubectl get nodes -o wide</code></pre>\n'
                                            '</div>\n',
                            'description': 'VPS OS パッケージ、Proxmox VE、k3s クラスタ、Docker コンテナの定期アップデート手順です。',
                            'icon': 'refresh-cw',
                            'id': 'periodic-maintenance',
                            'last_updated': '2026-09-12',
                            'service_id': None,
                            'title': '定期メンテナンス & アップデート手順',
                            'toc': [ {'id': 'sec-vps-apt', 'level': 2, 'title': '1. VPS ホスト OS 更新手順'},
                                     {'id': 'sec-pve-update', 'level': 2, 'title': '2. Proxmox VE (PVE) 更新手順'},
                                     {'id': 'sec-k3s-update', 'level': 2, 'title': '3. k3s Kubernetes クラスタ更新手順'},
                                     {'id': 'sec-docker-update', 'level': 2, 'title': '4. 独立 Docker コンテナ更新手順'}]},
  'portainer': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                 'category_id': 'standalone',
                 'category_name': 'メール & 独立サービス',
                 'content_html': '\n'
                                 '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">Kubernetes '
                                 'クラスタおよびホスト Docker コンテナを可視化・管理する GUI コンソール。</p>\n'
                                 '\n'
                                 '<div class="gh-alert gh-alert-note">\n'
                                 '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                 'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                 '  <div class="gh-alert-body">本ページは Qiita '
                                 '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 '
                                 '& 背景</h3>\n'
                                 '  <p>Kubernetes クラスタ内のリソースおよび VPS ホスト上の Docker コンテナの稼働状態を直感的に監視・管理すること。</p>\n'
                                 '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 '
                                 '(KPI / 動作基準)</h3>\n'
                                 '  <ul class="list-disc pl-6 space-y-1">\n'
                                 '    <li>K8s API との安全な RBAC 連携</li><li>Portainer セルフアップデート (v2.45.0) 完了済み</li>\n'
                                 '  </ul>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                 '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                 '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                 'レイヤー</th><th>採用技術 / '
                                 'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>管理サーバー</td><td>Portainer '
                                 'Server 2.45.0 (Deployment portainer)</td><td>K8s および Docker の統合管理 UI (Port '
                                 '8082)</td></tr><tr><td>認証</td><td>Portainer Internal / Keycloak OAuth '
                                 '連携可能</td><td>管理用アカウント</td></tr></tbody></table></div>\n'
                                 '\n'
                                 '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <p>PVC <code>portainer-data</code> (namespace: <code>portainer</code>) '
                                 'に設定を永続化。</p>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <p>アクセス URL: <code>https://manage.nigiri-rice.com/</code> (Caddy -> '
                                 'localhost:8082)</p>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                 '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                 '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                 'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                 'class="mermaid text-sm">graph LR\n'
                                 '    Admin["Administrator"] -->|HTTPS:443| Caddy["Caddy (VPS)"]\n'
                                 '    Caddy -->|Proxy:8082| Portainer["Portainer (Deployment)"]\n'
                                 '    Portainer -->|ServiceAccount| K8sAPI["Kubernetes API (:6443)"]</pre></div>\n'
                                 '\n'
                                 '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                 '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <div class="code-block-wrapper">\n'
                                 '  <div class="code-header">\n'
                                 '    <span class="code-lang">bash</span>\n'
                                 '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                 '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                 '      <span>コピー</span>\n'
                                 '    </button>\n'
                                 '  </div>\n'
                                 '  <pre><code class="language-bash">kubectl get pods -n portainer -o wide\n'
                                 'kubectl logs -n portainer -l app.kubernetes.io/name=portainer '
                                 '--tail=50</code></pre>\n'
                                 '</div>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <div class="code-block-wrapper">\n'
                                 '  <div class="code-header">\n'
                                 '    <span class="code-lang">bash</span>\n'
                                 '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                 '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                 '      <span>コピー</span>\n'
                                 '    </button>\n'
                                 '  </div>\n'
                                 '  <pre><code class="language-bash">kubectl rollout restart deployment portainer -n '
                                 'portainer</code></pre>\n'
                                 '</div>\n'
                                 '</div>\n',
                 'description': 'Kubernetes クラスタおよびホスト Docker コンテナを可視化・管理する GUI コンソール。',
                 'icon': 'trello',
                 'id': 'portainer',
                 'last_updated': '2026-09-12',
                 'service_id': 'portainer',
                 'title': 'Portainer 管理基盤 運用マニュアル',
                 'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                          {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                          {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                          {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                          {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                          {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                          {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'pve-host': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                'category_id': 'infrastructure',
                'category_name': 'インフラホスト基盤',
                'content_html': '\n'
                                '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">オンプレミスに設置された Proxmox '
                                'VE ハイパーバイザ。Active Directory (CT 144) および VPN (CT150) 等を収容。</p>\n'
                                '\n'
                                '<div class="gh-alert gh-alert-note">\n'
                                '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                '  <div class="gh-alert-body">本ページは Qiita '
                                '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                                '背景</h3>\n'
                                '  <p>オンプレミス環境における Active Directory ドメインコントローラ、セキュア VPN 接続、および内部 Wiki '
                                'を安全に仮想化運用すること。</p>\n'
                                '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI '
                                '/ 動作基準)</h3>\n'
                                '  <ul class="list-disc pl-6 space-y-1">\n'
                                '    <li>PVE ホスト (pve-manager 9.2.11 / Kernel 7.0.14-15) の安定稼働</li><li>CT 144 (AD '
                                'Windows Server) の認証ポート (TCP 53, 88, 389, 636) 稼働維持</li><li>CT150 (Tailscale VPN) '
                                'による拠点間相互通信の常時疎通</li>\n'
                                '  </ul>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                'レイヤー</th><th>採用技術 / '
                                'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>ハイパーバイザ</td><td>Proxmox VE '
                                '9.2.11 (Debian 12 base)</td><td>KVM 仮想マシンおよび LXC '
                                'コンテナの統合仮想化</td></tr><tr><td>ドメイン基盤</td><td>VM 140: Windows Server Active '
                                'Directory</td><td>認証、DNS、LDAP サービス</td></tr><tr><td>VPN ゲートウェイ</td><td>CT 150: '
                                'AlmaLinux 9.4 + Tailscale</td><td>拠点間セキュアメッシュトンネル</td></tr></tbody></table></div>\n'
                                '\n'
                                '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">ストレージ構成</h4>\n'
                                '<p>ローカル ZFS / LVM-Thin プール上に仮想ディスクを格納。定期バックアップは Proxmox vzdump により取得。</p>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <p>PVE Web コンソール: <code>https://pve-host-local:8006/</code></p>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                                'text-sm">graph TD\n'
                                '    PVE["PVE Host (9.2.11)"] --> CT 144["VM 140 (Windows AD)"]\n'
                                '    PVE --> CT150["CT 150 (Tailscale VPN)"]\n'
                                '    PVE --> CT137["CT 137 (Wiki PostgreSQL)"]\n'
                                '    CT150 <-->|Tailscale Mesh| VPS["Xserver VPS (nigiri-vps)"]</pre></div>\n'
                                '\n'
                                '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <div class="code-block-wrapper">\n'
                                '  <div class="code-header">\n'
                                '    <span class="code-lang">bash</span>\n'
                                '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                '      <span>コピー</span>\n'
                                '    </button>\n'
                                '  </div>\n'
                                '  <pre><code class="language-bash">qm list\n'
                                'pct list\n'
                                'systemctl status pveproxy pvedaemon pvestatd</code></pre>\n'
                                '</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <div class="code-block-wrapper">\n'
                                '  <div class="code-header">\n'
                                '    <span class="code-lang">bash</span>\n'
                                '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                '      <span>コピー</span>\n'
                                '    </button>\n'
                                '  </div>\n'
                                '  <pre><code class="language-bash"># VM 再起動\n'
                                'qm restart 140</code></pre>\n'
                                '</div>\n'
                                '</div>\n',
                'description': 'オンプレミスに設置された Proxmox VE ハイパーバイザ。Active Directory (CT 144) および VPN (CT150) 等を収容。',
                'icon': 'cpu',
                'id': 'pve-host',
                'last_updated': '2026-09-12',
                'service_id': 'infra_pve',
                'title': 'Proxmox VE (PVE) 仮想化基盤マニュアル',
                'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                         {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                         {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                         {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                         {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                         {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                         {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'shumoku': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
               'category_id': 'standalone',
               'category_name': 'メール & 独立サービス',
               'content_html': '\n'
                               '<p class="lead text-lg text-slate-600 dark:text-slate-300 '
                               'mb-6">コミュニティ・運用通知・アカウント連携を自動化する Discord Bot サービス。</p>\n'
                               '\n'
                               '<div class="gh-alert gh-alert-note">\n'
                               '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                               'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                               '  <div class="gh-alert-body">本ページは Qiita '
                               '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                               '</div>\n'
                               '\n'
                               '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                               '<div class="space-y-4 mb-6">\n'
                               '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                               '背景</h3>\n'
                               '  <p>nigiri-rice.com Discord コミュニティにおけるロール自動付与、アラート通知、および OmusuBI 連携を行うこと。</p>\n'
                               '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI '
                               '/ 動作基準)</h3>\n'
                               '  <ul class="list-disc pl-6 space-y-1">\n'
                               '    <li>Discord Gateway 接続常時維持 (Up, healthy)</li><li>アカウント連携コマンドの 2 秒以内応答</li>\n'
                               '  </ul>\n'
                               '</div>\n'
                               '\n'
                               '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                               '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                               '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                               'レイヤー</th><th>採用技術 / '
                               'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>ランタイム</td><td>Python 3.11 / '
                               'discord.py</td><td>非同期イベント駆動型 Bot</td></tr><tr><td>デプロイ形態</td><td>Docker コンテナ '
                               '(shumoku)</td><td>ホスト上で常駐稼働</td></tr></tbody></table></div>\n'
                               '\n'
                               '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                               '<div class="space-y-4 mb-6">\n'
                               '  <p>ホストディレクトリ <code>/opt/shumoku/data</code> に設定・キャッシュを永続化。</p>\n'
                               '</div>\n'
                               '\n'
                               '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                               '<div class="space-y-4 mb-6">\n'
                               '  <p>Discord スラッシュコマンド: <code>/sync</code>, <code>/status</code>, '
                               '<code>/link</code></p>\n'
                               '</div>\n'
                               '\n'
                               '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                               '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                               '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                               'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                               'text-sm">graph LR\n'
                               '    Discord["Discord Gateway"] <-->|Websocket / WSS| Shumoku["Shumoku Bot (Docker)"]\n'
                               '    Shumoku -->|REST API| KC["Keycloak (sso.nigiri-rice.com)"]</pre></div>\n'
                               '\n'
                               '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                               '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                               '<div class="space-y-4 mb-6">\n'
                               '  <div class="code-block-wrapper">\n'
                               '  <div class="code-header">\n'
                               '    <span class="code-lang">bash</span>\n'
                               '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                               '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                               '      <span>コピー</span>\n'
                               '    </button>\n'
                               '  </div>\n'
                               '  <pre><code class="language-bash">docker ps | grep shumoku\n'
                               'docker logs shumoku -f --tail=50</code></pre>\n'
                               '</div>\n'
                               '</div>\n'
                               '\n'
                               '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                               'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                               '<div class="space-y-4 mb-6">\n'
                               '  <div class="code-block-wrapper">\n'
                               '  <div class="code-header">\n'
                               '    <span class="code-lang">bash</span>\n'
                               '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                               '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                               '      <span>コピー</span>\n'
                               '    </button>\n'
                               '  </div>\n'
                               '  <pre><code class="language-bash">docker restart shumoku</code></pre>\n'
                               '</div>\n'
                               '</div>\n',
               'description': 'コミュニティ・運用通知・アカウント連携を自動化する Discord Bot サービス。',
               'icon': 'message-square',
               'id': 'shumoku',
               'last_updated': '2026-09-12',
               'service_id': None,
               'title': 'Discord Bot (Shumoku) 運用マニュアル',
               'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                        {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                        {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                        {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                        {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                        {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                        {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'smb-storage': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                   'category_id': 'storage',
                   'category_name': 'ストレージ & レジストリ',
                   'content_html': '\n'
                                   '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">Windows ファイルサーバー '
                                   '(SMB/CIFS) の共有ディレクトリを K8s Pod に動的・静的マウントするストレージドライバ。</p>\n'
                                   '\n'
                                   '<div class="gh-alert gh-alert-note">\n'
                                   '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                   'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                   '  <div class="gh-alert-body">本ページは Qiita '
                                   '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                   '</div>\n'
                                   '\n'
                                   '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                   '<div class="space-y-4 mb-6">\n'
                                   '  <h3 class="text-lg font-semibold text-emerald-600 '
                                   'dark:text-emerald-400">プロジェクト目的 & 背景</h3>\n'
                                   '  <p>PVE 上の Windows Server (CT 144) や NAS の共有フォルダを Kubernetes Pods '
                                   'から透過的にアクセス可能にすること。</p>\n'
                                   '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 '
                                   '(KPI / 動作基準)</h3>\n'
                                   '  <ul class="list-disc pl-6 space-y-1">\n'
                                   '    <li>ホストノード（nigiri-vps）での安定稼働（desired=1/ready=1）</li><li>CIFS '
                                   'プロトコルによる大容量添付ファイル・バックアップ領域の安全な共有</li>\n'
                                   '  </ul>\n'
                                   '</div>\n'
                                   '\n'
                                   '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                   '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                   '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                   'レイヤー</th><th>採用技術 / '
                                   'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>ストレージドライバ</td><td>smb.csi.k8s.io '
                                   '(v1.15.0)</td><td>Kubernetes CSI 仕様準拠の CIFS/SMB '
                                   'ボリュームプラグイン</td></tr><tr><td>ノード制約</td><td>nodeSelector: kubernetes.io/hostname: '
                                   'nigiri-vps</td><td>Linux '
                                   'カーネルのマウント伝播仕様（rshared）に対応するためホスト限定稼働</td></tr></tbody></table></div>\n'
                                   '\n'
                                   '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                   '<div class="space-y-4 mb-6">\n'
                                   '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">技術的制約のファクト</h4>\n'
                                   '<p>worker 01〜04 は Docker コンテナ内の k3s-agent であり、overlay2 上の '
                                   '<code>/var/lib/kubelet</code> は Linux カーネル仕様上 <code>Bidirectional</code> (rshared) '
                                   'マウント伝播をサポートできません。そのため、SMB CSI Node はホスト <code>nigiri-vps</code> に固定運用されます。</p>\n'
                                   '</div>\n'
                                   '\n'
                                   '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                   '<div class="space-y-4 mb-6">\n'
                                   '  <p>StorageClass: <code>smb</code> (provisioner: '
                                   '<code>smb.csi.k8s.io</code>)</p>\n'
                                   '</div>\n'
                                   '\n'
                                   '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                   '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                   '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                   'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                   'class="mermaid text-sm">graph TD\n'
                                   '    Pod["K8s App Pod (pinned to nigiri-vps)"] -->|VolumeMount| '
                                   'Mount["/var/lib/kubelet/pods/..."]\n'
                                   '    Mount --> CSINode["csi-smb-node (nigiri-vps)"]\n'
                                   '    CSINode -->|SMB/CIFS TCP 445| AD["VM 140 / Windows SMB Share"]</pre></div>\n'
                                   '\n'
                                   '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                   '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                   '<div class="space-y-4 mb-6">\n'
                                   '  <div class="code-block-wrapper">\n'
                                   '  <div class="code-header">\n'
                                   '    <span class="code-lang">bash</span>\n'
                                   '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                   '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                   '      <span>コピー</span>\n'
                                   '    </button>\n'
                                   '  </div>\n'
                                   '  <pre><code class="language-bash">kubectl get pods -n smb-storage -o wide\n'
                                   'kubectl -n smb-storage patch daemonset csi-smb-node -p '
                                   '\'{"spec":{"template":{"spec":{"nodeSelector":{"kubernetes.io/hostname":"nigiri-vps"}}}}}\'</code></pre>\n'
                                   '</div>\n'
                                   '</div>\n'
                                   '\n'
                                   '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                   'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                   '<div class="space-y-4 mb-6">\n'
                                   '  <div class="code-block-wrapper">\n'
                                   '  <div class="code-header">\n'
                                   '    <span class="code-lang">bash</span>\n'
                                   '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                   '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                   '      <span>コピー</span>\n'
                                   '    </button>\n'
                                   '  </div>\n'
                                   '  <pre><code class="language-bash">kubectl rollout restart daemonset csi-smb-node '
                                   '-n smb-storage</code></pre>\n'
                                   '</div>\n'
                                   '</div>\n',
                   'description': 'Windows ファイルサーバー (SMB/CIFS) の共有ディレクトリを K8s Pod に動的・静的マウントするストレージドライバ。',
                   'icon': 'hard-drive',
                   'id': 'smb-storage',
                   'last_updated': '2026-09-12',
                   'service_id': 'smb_storage',
                   'title': 'SMB CSI Driver 運用マニュアル',
                   'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                            {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                            {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                            {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                            {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                            {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                            {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'standards-7docs': { 'badges': ['公式標準', 'Qiita準拠', 'Best Practice'],
                       'category_id': 'guidelines',
                       'category_name': '設計標準 & 運用ガイドライン',
                       'content_html': '\n'
                                       '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n'
                                       'Qiita のベストプラクティス記事 <em>「成果物は、7つの必須ドキュメント作成から始めよう！（付録：開発規模別の必要ドキュメント一覧）」</em> '
                                       '(komeri 著) に基づき、<strong>nigiri-rice.com</strong> '
                                       'における全サービスの開発・設計・運用で必須とする「7つの標準ドキュメント」の作成基準を規定します。\n'
                                       '</p>\n'
                                       '\n'
                                       '<div class="gh-alert gh-alert-important">\n'
                                       '  <div class="gh-alert-title"><i data-lucide="alert-circle" class="w-4 h-4 '
                                       'shrink-0"></i><span>全システムへの適用義務</span></div>\n'
                                       '  <div class="gh-alert-body">nigiri-rice.com で開発・運用されるすべてのサービス（Keycloak, '
                                       'Vault, CNT Connect, WordPress, Console等）は、本基準に沿って各個別ドキュメントが整備されています。</div>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-why-docs" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">1. なぜドキュメントが最重要なのか</h2>\n'
                                       '<p '
                                       'class="mb-4">多くの開発者は「とりあえず動くコードを書こう」としがちですが、設計・ドキュメントを先行作成することで以下の劇的なメリットが生まれます：</p>\n'
                                       '<ul class="list-disc pl-6 space-y-2 mb-6">\n'
                                       '  <li><strong>開発・運用の迷いがゼロになる</strong>: '
                                       '何を作るべきか、制約は何か、データ構造が事前に確定しているため、実装中の手戻りが発生しません。</li>\n'
                                       '  <li><strong>実務レベルの思考プロセスの可視化</strong>: '
                                       '「なぜその技術を選定したのか」「どのようなセキュリティ対策を施したのか」が客観的に証明されます。</li>\n'
                                       '  <li><strong>障害復旧 (DR) の迅速化</strong>: '
                                       'データベース構造や起動手順、環境変数が明文化されているため、障害発生時に即座に対応可能です。</li>\n'
                                       '</ul>\n'
                                       '\n'
                                       '<h2 id="sec-7docs-list" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">2. 7つの必須ドキュメント一覧</h2>\n'
                                       '<div class="table-responsive"><table '
                                       'class="gh-table"><thead><tr><th>ドキュメント名</th><th>作成フェーズ</th><th>目的</th><th>重要度</th><th>本ポータルでの掲載場所</th></tr></thead><tbody><tr><td><strong>1. '
                                       '要件定義書</strong></td><td>企画・プロジェクト開始時</td><td>何を作るか、なぜ作るか、成功基準と制約を明確化</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第1章</td></tr><tr><td><strong>2. '
                                       '技術スタック</strong></td><td>基本設計時</td><td>言語・FW・DB・基盤の選定理由とバージョン明記</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第2章</td></tr><tr><td><strong>3. '
                                       'データベース設計書</strong></td><td>詳細設計時</td><td>ER図、テーブル定義、カラム制約、初期データ</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第3章</td></tr><tr><td><strong>4. '
                                       '画面・API設計書</strong></td><td>詳細設計時</td><td>UI/UXレイアウト、エンドポイント、認証要件</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第4章</td></tr><tr><td><strong>5. '
                                       '画面遷移・フロー図</strong></td><td>詳細設計時</td><td>ユーザー導線、Ajax遷移、状態遷移、シーケンス図</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第5章</td></tr><tr><td><strong>6. README & '
                                       '運用手順書</strong></td><td>開発・デプロイ時</td><td>起動コマンド、ログ監視、再起動、日常保守Runbook</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第6章</td></tr><tr><td><strong>7. '
                                       '環境構築・復旧手順書</strong></td><td>開発・デプロイ時</td><td>依存関係、Secret設定、コンテナビルド、障害復旧手順</td><td>★★★★★</td><td>各サービスドキュメント '
                                       '第7章</td></tr></tbody></table></div>\n'
                                       '\n'
                                       '<h2 id="sec-doc-definitions" class="text-2xl font-bold mt-10 mb-4 pb-2 '
                                       'border-b border-slate-200 dark:border-emerald-950/70">3. 各ドキュメントの定義・構成基準</h2>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">① 要件定義書 (Requirements)</h3>\n'
                                       '<p '
                                       'class="mb-3">プロジェクトの目的、解決する課題、対象ユーザー、成功基準（KPI/動作要件）、および制約条件（インフラ制約、納期、人員）を明確にします。</p>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">② 技術スタック (Technology Stack)</h3>\n'
                                       '<p '
                                       'class="mb-3">単なるツール名だけでなく、「なぜその技術を採用したのか（選定理由）」を記載します。バージョン互換性やセキュリティ対策（PDO、JWT等）も明記します。</p>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">③ データベース・ストレージ設計書 (Database '
                                       'Design)</h3>\n'
                                       '<p class="mb-3">Mermaid 形式の ER 図、全テーブルのカラム型・PK/FK制約・デフォルト値、および '
                                       'PersistentVolume (PVC) やキャッシュ (Redis) のマウント設計を記載します。</p>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">④ 画面・API設計書 (UI & API Specs)</h3>\n'
                                       '<p class="mb-3">画面一覧表（画面ID, 名称, URL, 権限）、ワイヤーフレーム構成、および REST API '
                                       'のパス・メソッド・リクエスト/レスポンス形式を定義します。</p>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">⑤ 画面遷移・処理フロー図 (Screen & Sequence '
                                       'Flow)</h3>\n'
                                       '<p class="mb-3">Mermaid '
                                       'シーケンス図および状態遷移図を用いて、ユーザーの操作動線、非同期処理、認証コールバック、エラー時のフォールバック処理を可視化します。</p>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">⑥ README.md & 運用手順書 '
                                       '(Runbook)</h3>\n'
                                       '<p class="mb-3">日々の運用で即時利用可能なコマンドライン集です。Pod '
                                       '再起動、ログ追跡、ヘルスチェック、ステータス確認コマンドを収録します。</p>\n'
                                       '\n'
                                       '<h3 class="text-xl font-semibold mt-6 mb-3">⑦ 環境構築・復旧手順書 (Setup & '
                                       'Recovery)</h3>\n'
                                       '<p '
                                       'class="mb-3">初期クラスタ構築、Secret（認証トークン）の投入、データベースリストア、およびコンテナイメージの更新手順をステップバイステップで記述します。</p>\n'
                                       '\n'
                                       '<h2 id="sec-timing" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">4. 作成タイミングとフェーズ管理</h2>\n'
                                       '<div class="table-responsive"><table '
                                       'class="gh-table"><thead><tr><th>フェーズ</th><th>作成対象ドキュメント</th><th>達成基準</th></tr></thead><tbody><tr><td><strong>Phase '
                                       '1: 設計フェーズ</strong> (コーディング前)</td><td>1. 要件定義書<br>2. 技術スタック<br>3. '
                                       'データベース設計書<br>4. 画面設計書<br>5. 画面遷移図</td><td>実装に着手する前に 1〜5 '
                                       'が完成・レビュー承認されていること。</td></tr><tr><td><strong>Phase 2: 実装・公開フェーズ</strong> '
                                       '(デプロイ時)</td><td>6. README & 運用手順書<br>7. '
                                       '環境構築・復旧手順書</td><td>リポジトリへの初回コミットおよび本番配備と同時に完成していること。</td></tr></tbody></table></div>\n',
                       'description': 'Qiitaで高く評価された「7つの必須ドキュメント作成基準」を nigiri-rice.com の全サービス開発・運用の公式標準として定義します。',
                       'icon': 'file-check',
                       'id': 'standards-7docs',
                       'last_updated': '2026-09-12',
                       'service_id': None,
                       'title': '開発標準: 7つの必須ドキュメント策定基準',
                       'toc': [ {'id': 'sec-why-docs', 'level': 2, 'title': '1. なぜドキュメントが最重要なのか'},
                                {'id': 'sec-7docs-list', 'level': 2, 'title': '2. 7つの必須ドキュメント一覧'},
                                {'id': 'sec-doc-definitions', 'level': 2, 'title': '3. 各ドキュメントの定義・構成基準'},
                                {'id': 'sec-timing', 'level': 2, 'title': '4. 作成タイミングとフェーズ管理'},
                                {'id': 'sec-scale-matrix', 'level': 2, 'title': '5. 開発規模別のドキュメント要件表'}]},
  'troubleshooting': { 'badges': ['障害復旧', '緊急対応', 'Runbook'],
                       'category_id': 'guidelines',
                       'category_name': '設計標準 & 運用ガイドライン',
                       'content_html': '\n'
                                       '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">\n'
                                       'サービス停止や異常検知時に運用者が即座に実施するエマージェンシー対応手順書です。\n'
                                       '</p>\n'
                                       '\n'
                                       '<h2 id="sec-flowchart" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">1. 障害切り分けフローチャート</h2>\n'
                                       '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                       'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                       'class="mermaid text-sm">graph TD\n'
                                       '    A["アラート検知 / 異常報告"] --> B["kubectl describe pod -n <ns> <pod>"]\n'
                                       '    B --> C{"Events エラー内容"}\n'
                                       '    C -->|OOMKilled| D["limits.memory 引き上げ"]\n'
                                       '    C -->|CrashLoopBackOff| E["kubectl logs -n <ns> <pod> --previous"]\n'
                                       '    C -->|ImagePullBackOff| F["GHCR / レジストリ PAT 再発行"]\n'
                                       '    C -->|FailedScheduling| G["ノードリソース / nodeSelector 確認"]\n'
                                       '    C -->|Sealed| H["Vault Unseal 解除実行"]</pre></div>\n'
                                       '\n'
                                       '<h2 id="sec-vault-unseal" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">2. Vault Sealed (封印) 解除手順</h2>\n'
                                       '<div class="gh-alert gh-alert-important">\n'
                                       '  <div class="gh-alert-title"><i data-lucide="alert-circle" class="w-4 h-4 '
                                       'shrink-0"></i><span>再起動時の仕様</span></div>\n'
                                       '  <div class="gh-alert-body">Vault はサーバー再起動時、暗号化キー保護のため自動的に封印 (Sealed) '
                                       'されます。以下の手順で即時復帰させてください。</div>\n'
                                       '</div>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash"># 1. 状態確認 (Sealed: true の場合は解除必要)\n'
                                       'kubectl -n vault exec vault-0 -- vault status\n'
                                       '\n'
                                       '# 2. unseal-key 取得 &amp; 解除実行\n'
                                       'UNSEAL_KEY=$(kubectl -n vault get secret vault-init-keys -o '
                                       "jsonpath='{.data.unseal-key}' | base64 -d)\n"
                                       'kubectl -n vault exec vault-0 -- vault operator unseal $UNSEAL_KEY\n'
                                       '\n'
                                       '# 3. 正常確認 (Sealed: false)\n'
                                       'kubectl -n vault exec vault-0 -- vault status</code></pre>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-image-pull" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">3. ImagePullBackOff / 403 '
                                       '解消手順</h2>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash"># 有効な GitHub PAT で secret を再作成\n'
                                       'kubectl -n cnt-connect-prod create secret docker-registry ghcr-secret \\\n'
                                       '  --docker-server=ghcr.io \\\n'
                                       '  --docker-username=YOUR_GITHUB_USER \\\n'
                                       '  --docker-password=YOUR_NEW_PAT \\\n'
                                       '  --dry-run=client -o yaml | kubectl apply -f -\n'
                                       '\n'
                                       '# Pod をローリング再起動\n'
                                       'kubectl -n cnt-connect-prod rollout restart deployment api admin-web '
                                       'student-web</code></pre>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-smb-constraint" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">4. SMB CSI ドライバ制約対応</h2>\n'
                                       '<p class="mb-4">SMB CSI ドライバはホストマウント伝播（rshared）の制約上、<strong>nigiri-vps (Host) '
                                       'でのみ稼働可能</strong>です。worker 01〜04 で起動失敗した場合はノードセレクタを再適用します：</p>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash">kubectl -n smb-storage patch daemonset '
                                       'csi-smb-node -p '
                                       '\'{"spec":{"template":{"spec":{"nodeSelector":{"kubernetes.io/hostname":"nigiri-vps"}}}}}\'</code></pre>\n'
                                       '</div>\n'
                                       '\n'
                                       '<h2 id="sec-caddy-rollback" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                       'border-slate-200 dark:border-emerald-950/70">5. Caddy 設定ロールバック</h2>\n'
                                       '<div class="code-block-wrapper">\n'
                                       '  <div class="code-header">\n'
                                       '    <span class="code-lang">bash</span>\n'
                                       '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                       '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                       '      <span>コピー</span>\n'
                                       '    </button>\n'
                                       '  </div>\n'
                                       '  <pre><code class="language-bash">cp /etc/caddy/Caddyfile.bak '
                                       '/etc/caddy/Caddyfile\n'
                                       'caddy validate --config /etc/caddy/Caddyfile\n'
                                       'systemctl reload caddy</code></pre>\n'
                                       '</div>\n',
                       'description': 'Pod 異常、ImagePullBackOff、SMB 制約、Vault Sealed 状態の解除、Caddy 復旧手順です。',
                       'icon': 'alert-triangle',
                       'id': 'troubleshooting',
                       'last_updated': '2026-09-12',
                       'service_id': None,
                       'title': '障害対応・緊急トラブルシューティング Runbook',
                       'toc': [ {'id': 'sec-flowchart', 'level': 2, 'title': '1. 障害切り分けフローチャート'},
                                {'id': 'sec-vault-unseal', 'level': 2, 'title': '2. Vault Sealed (封印) 解除手順'},
                                {'id': 'sec-image-pull', 'level': 2, 'title': '3. ImagePullBackOff / 403 解消手順'},
                                {'id': 'sec-smb-constraint', 'level': 2, 'title': '4. SMB CSI ドライバ制約対応'},
                                {'id': 'sec-caddy-rollback', 'level': 2, 'title': '5. Caddy 設定ロールバック'}]},
  'vault': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
             'category_id': 'identity',
             'category_name': '認証 & ID 基盤',
             'content_html': '\n'
                             '<p class="lead text-lg text-slate-600 dark:text-slate-300 '
                             'mb-6">APIキー、暗号化キー、各種トークンのセキュアストレージ & 動的シークレット管理基盤。SSOログイン標準化およびToken限定運用に対応。</p>\n'
                             '\n'
                             '<div class="gh-alert gh-alert-note">\n'
                             '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                             'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                             '  <div class="gh-alert-body">本ページは Qiita '
                             '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                             '</div>\n'
                             '\n'
                             '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                             'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                             '<div class="space-y-4 mb-6">\n'
                             '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                             '背景</h3>\n'
                             '  <p>全社・全システム（K8s Pods, 開発者, CI/CD）における機密情報（パスワード, APIキー, '
                             'DB接続文字列）の一元暗号化管理および安全な共有動線（https://vault.nigiri-rice.com/ui/vault/dashboard）を提供すること。</p>\n'
                             '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI / '
                             '動作基準)</h3>\n'
                             '  <ul class="list-disc pl-6 space-y-1">\n'
                             '    <li>暗号化キーおよび機密情報への平文アクセスを排除し、アクセスログを100%監査可能にすること</li><li>Keycloak OIDC による SSO '
                             'ログインを標準とし、未認証アクセス時はワンクリックでログイン完了すること</li><li>K8s ワークロードに対しては vault-agent-injector '
                             'による自動サイドカー注入を実現すること</li>\n'
                             '  </ul>\n'
                             '</div>\n'
                             '\n'
                             '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                             'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                             '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                             '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                             'レイヤー</th><th>採用技術 / '
                             'バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>コアエンジン</td><td>HashiCorp Vault '
                             'v1.18.1</td><td>業界標準のシークレット管理エンジン。暗号化、動的トークン、監査ログ完備</td></tr><tr><td>ストレージエンジン</td><td>Standalone '
                             'Encrypted File Storage</td><td>PVC (vault-data) '
                             'ローカルマウントによる安全な暗号化永続ストレージ</td></tr><tr><td>サイドカー注入</td><td>vault-agent-injector (2 Pods '
                             'HA)</td><td>Mutating Webhook による Pod '
                             '起動時の自動認証情報マウント</td></tr><tr><td>認証プロバイダ</td><td>Keycloak OIDC (master '
                             'realm)</td><td>開発者向け SSO。PKCE 対応 Authorization Code '
                             'Flow</td></tr><tr><td>管理者認証</td><td>Token Auth Method</td><td>Root Token または Admin '
                             'Policy 付与トークンによる緊急保守アクセス</td></tr></tbody></table></div>\n'
                             '\n'
                             '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                             'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                             '<div class="space-y-4 mb-6">\n'
                             '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">暗号化ストレージ設計</h4>\n'
                             '<p>Vault のデータは <code>/vault/data</code> にマウントされた PersistentVolumeClaim '
                             '(<code>vault-data</code>, StorageClass: <code>local-path</code>) 上に Shamir '
                             'の秘密分散アルゴリズムで暗号化されて保管されます。</p>\n'
                             '<ul class="list-disc pl-6 space-y-1">\n'
                             '  <li>KV シークレットエンジン (v2): <code>secret/</code></li>\n'
                             '  <li>社内認証情報共有パス: <code>secret/infrastructure/</code>, <code>secret/services/</code>, '
                             '<code>secret/shared/</code></li>\n'
                             '</ul>\n'
                             '</div>\n'
                             '\n'
                             '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                             'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                             '<div class="space-y-4 mb-6">\n'
                             '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">Web UI & エンドポイント仕様</h4>\n'
                             '<ul class="list-disc pl-6 space-y-1">\n'
                             '  <li>公開ダッシュボード: <code>https://vault.nigiri-rice.com/ui/vault/dashboard</code></li>\n'
                             '  <li>SSO ログイン画面: <code>https://vault.nigiri-rice.com/ui/vault/auth?with=oidc</code> '
                             '(標準リダイレクト先)</li>\n'
                             '  <li>Admin Token ログイン画面: '
                             '<code>https://vault.nigiri-rice.com/ui/vault/auth?with=token</code></li>\n'
                             '  <li>ヘルスチェック API: <code>GET https://vault.nigiri-rice.com/v1/sys/health</code> (HTTP '
                             '200)</li>\n'
                             '</ul>\n'
                             '</div>\n'
                             '\n'
                             '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 '
                             'dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                             '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                             '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                             'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                             'text-sm">sequenceDiagram\n'
                             '    autonumber\n'
                             '    actor User as 開発者 / 運用者\n'
                             '    participant Caddy as Caddy (VPS)\n'
                             '    participant VaultUI as Vault Web UI\n'
                             '    participant Keycloak as Keycloak SSO\n'
                             '\n'
                             '    User->>Caddy: https://vault.nigiri-rice.com/ アクセス\n'
                             '    Caddy-->>User: 302 Redirect (?with=oidc)\n'
                             '    User->>VaultUI: OIDCログイン画面\n'
                             '    User->>VaultUI: 「Sign in with OIDC」クリック\n'
                             '    VaultUI->>Keycloak: OIDC認可リダイレクト (PKCE)\n'
                             '    User->>Keycloak: 統合アカウント認証\n'
                             '    Keycloak-->>VaultUI: コールバック & JWTトークン\n'
                             '    VaultUI-->>User: ログイン完了 -> Dashboard 表示</pre></div>\n'
                             '\n'
                             '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                             'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                             '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                             '<div class="space-y-4 mb-6">\n'
                             '  <div class="code-block-wrapper">\n'
                             '  <div class="code-header">\n'
                             '    <span class="code-lang">bash</span>\n'
                             '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                             '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                             '      <span>コピー</span>\n'
                             '    </button>\n'
                             '  </div>\n'
                             '  <pre><code class="language-bash"># 1. サーバー稼働状態の確認\n'
                             'kubectl exec -n vault vault-0 -- vault status\n'
                             '\n'
                             '# 2. 有効な認証方式一覧の確認 (OIDC, Token, Kubernetes)\n'
                             'kubectl exec -n vault vault-0 -- env VAULT_TOKEN=$(kubectl -n vault get secret '
                             "vault-init-keys -o jsonpath='{.data.root-token}' | base64 -d) vault auth list\n"
                             '\n'
                             '# 3. 未認証 OIDC 表示チューニング\n'
                             'kubectl exec -n vault vault-0 -- env VAULT_TOKEN=$(kubectl -n vault get secret '
                             "vault-init-keys -o jsonpath='{.data.root-token}' | base64 -d) vault auth tune "
                             '-listing-visibility=unauth oidc</code></pre>\n'
                             '</div><p class="mt-2">※ サーバー再起動時は自動封印されるため、下記の手順7を参照して Unseal を実行してください。</p>\n'
                             '</div>\n'
                             '\n'
                             '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b border-slate-200 '
                             'dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                             '<div class="space-y-4 mb-6">\n'
                             '  <div class="gh-alert gh-alert-important">\n'
                             '  <div class="gh-alert-title"><i data-lucide="alert-circle" class="w-4 h-4 '
                             'shrink-0"></i><span>封印解除 (Unseal) 手順</span></div>\n'
                             '  <div class="gh-alert-body">サーバー再起動などで Sealed 状態になった場合の解除コマンドです：</div>\n'
                             '</div>\n'
                             '<div class="code-block-wrapper">\n'
                             '  <div class="code-header">\n'
                             '    <span class="code-lang">bash</span>\n'
                             '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                             '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                             '      <span>コピー</span>\n'
                             '    </button>\n'
                             '  </div>\n'
                             '  <pre><code class="language-bash"># unseal-key の取得 &amp; 適用\n'
                             'UNSEAL_KEY=$(kubectl -n vault get secret vault-init-keys -o '
                             "jsonpath='{.data.unseal-key}' | base64 -d)\n"
                             'kubectl -n vault exec vault-0 -- vault operator unseal $UNSEAL_KEY\n'
                             'kubectl -n vault exec vault-0 -- vault status</code></pre>\n'
                             '</div>\n'
                             '</div>\n',
             'description': 'APIキー、暗号化キー、各種トークンのセキュアストレージ & 動的シークレット管理基盤。SSOログイン標準化およびToken限定運用に対応。',
             'icon': 'shield-check',
             'id': 'vault',
             'last_updated': '2026-09-12',
             'service_id': 'vault',
             'title': 'HashiCorp Vault 運用保守マニュアル',
             'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                      {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                      {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                      {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                      {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                      {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                      {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'vps-host': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                'category_id': 'infrastructure',
                'category_name': 'インフラホスト基盤',
                'content_html': '\n'
                                '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">Ubuntu 24.04 LTS '
                                'ホスト、k3s Control Plane、および 4 台の Docker Worker コンテナから成る中核インフラ基盤。</p>\n'
                                '\n'
                                '<div class="gh-alert gh-alert-note">\n'
                                '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                '  <div class="gh-alert-body">本ページは Qiita '
                                '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 & '
                                '背景</h3>\n'
                                '  <p>nigiri-rice.com の全パブリック向けサービスをホストし、高可用性と柔軟なリソース配分を実現すること。</p>\n'
                                '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 (KPI '
                                '/ 動作基準)</h3>\n'
                                '  <ul class="list-disc pl-6 space-y-1">\n'
                                '    <li>5 ノード（Control Plane 1 + Worker 4）すべての Ready 状態維持</li><li>ホストストレージ (/dev/vda1 '
                                '387GB) 空き容量 50% 以上の確保</li><li>NICT 日本標準時 (JST) との時刻同期完全性</li>\n'
                                '  </ul>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                'レイヤー</th><th>採用技術 / バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>ホスト '
                                'OS</td><td>Ubuntu 24.04.4 LTS (Kernel '
                                '6.8.0-139)</td><td>安定した長期サポートディストリビューション</td></tr><tr><td>Kubernetes</td><td>k3s '
                                'v1.36.4+k3s1 (containerd 2.3.4)</td><td>軽量・高機能なエッジ K8s '
                                'ディストリビューション</td></tr><tr><td>ワーカーノード</td><td>Docker DinD '
                                '(vps-worker-01〜04)</td><td>Docker コンテナとして稼働する 4 台の '
                                'k3s-agent</td></tr></tbody></table></div>\n'
                                '\n'
                                '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">ディスク & パーティション</h4>\n'
                                '<p>メインディスク: <code>/dev/vda1</code> 387GB。マウントポイント: <code>/</code>, '
                                '<code>/var/lib/rancher</code> (k3s データ)。</p>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <ul class="list-disc pl-6 space-y-1">\n'
                                '  <li>SSH 接続: <code>ssh root@210.131.211.17</code> (公開鍵認証)</li>\n'
                                '  <li>K8s API: <code>https://127.0.0.1:6443</code></li>\n'
                                '</ul>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre class="mermaid '
                                'text-sm">graph TD\n'
                                '    Host["nigiri-vps (Host CP)"] -->| flannel overlay | W1["vps-worker-01 '
                                '(172.30.0.2)"]\n'
                                '    Host -->| flannel overlay | W2["vps-worker-02 (172.30.0.3)"]\n'
                                '    Host -->| flannel overlay | W3["vps-worker-03 (172.30.0.4)"]\n'
                                '    Host -->| flannel overlay | W4["vps-worker-04 (172.30.0.5)"]</pre></div>\n'
                                '\n'
                                '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <div class="code-block-wrapper">\n'
                                '  <div class="code-header">\n'
                                '    <span class="code-lang">bash</span>\n'
                                '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                '      <span>コピー</span>\n'
                                '    </button>\n'
                                '  </div>\n'
                                '  <pre><code class="language-bash">kubectl get nodes -o wide\n'
                                'df -h /\n'
                                'free -m\n'
                                'uptime\n'
                                'timedatectl</code></pre>\n'
                                '</div>\n'
                                '</div>\n'
                                '\n'
                                '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                '<div class="space-y-4 mb-6">\n'
                                '  <div class="code-block-wrapper">\n'
                                '  <div class="code-header">\n'
                                '    <span class="code-lang">bash</span>\n'
                                '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                '      <span>コピー</span>\n'
                                '    </button>\n'
                                '  </div>\n'
                                '  <pre><code class="language-bash">systemctl restart k3s\n'
                                'systemctl restart docker</code></pre>\n'
                                '</div>\n'
                                '</div>\n',
                'description': 'Ubuntu 24.04 LTS ホスト、k3s Control Plane、および 4 台の Docker Worker コンテナから成る中核インフラ基盤。',
                'icon': 'server',
                'id': 'vps-host',
                'last_updated': '2026-09-12',
                'service_id': 'infra_vps',
                'title': 'Xserver VPS (nigiri-vps & k3s Workers) 基盤マニュアル',
                'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                         {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                         {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                         {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                         {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                         {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                         {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]},
  'wordpress': { 'badges': ['7つの必須ドキュメント準拠', 'Verified: 2026-09-12', 'Production'],
                 'category_id': 'apps',
                 'category_name': '業務アプリケーション',
                 'content_html': '\n'
                                 '<p class="lead text-lg text-slate-600 dark:text-slate-300 mb-6">nigiri-rice.com '
                                 '公式コーポレートサイトおよびブログ・お知らせ配信を行う CMS 基盤。</p>\n'
                                 '\n'
                                 '<div class="gh-alert gh-alert-note">\n'
                                 '  <div class="gh-alert-title"><i data-lucide="info" class="w-4 h-4 '
                                 'shrink-0"></i><span>7つの必須ドキュメント準拠</span></div>\n'
                                 '  <div class="gh-alert-body">本ページは Qiita '
                                 '策定基準に基づき、要件定義・技術選定・DB設計・画面/API・遷移フロー・運用Runbook・復旧手順の7要素を完全網羅しています。</div>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-1-requirements" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">1. 要件定義書 (Requirements)</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">プロジェクト目的 '
                                 '& 背景</h3>\n'
                                 '  <p>企業公式情報、ニュースリリース、開発者向け告知を外部へ安定して発信すること。</p>\n'
                                 '  <h3 class="text-lg font-semibold text-emerald-600 dark:text-emerald-400">成功の基準 '
                                 '(KPI / 動作基準)</h3>\n'
                                 '  <ul class="list-disc pl-6 space-y-1">\n'
                                 '    <li>表示速度（Lighthouse Performance 90+）および CDN キャッシュ活用</li><li>MariaDB '
                                 '日次自動ダンプによる記事コンテンツの完全保護</li>\n'
                                 '  </ul>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-2-techstack" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">2. 技術スタック & 選定理由</h2>\n'
                                 '<p class="mb-4">本システムで採用されている技術コンポーネントとその選定理由です：</p>\n'
                                 '<div class="table-responsive"><table class="gh-table"><thead><tr><th>カテゴリ / '
                                 'レイヤー</th><th>採用技術 / バージョン</th><th>選定理由・メリット</th></tr></thead><tbody><tr><td>CMS '
                                 'コア</td><td>WordPress 6.x (PHP 8.2)</td><td>公式 WordPress '
                                 'コンテナイメージ</td></tr><tr><td>データベース</td><td>MariaDB 10.11 (Deployment '
                                 'mariadb)</td><td>高速・安定なリレーショナルデータストア</td></tr><tr><td>Web サーバー</td><td>Nginx + '
                                 'Caddy</td><td>静的ファイルキャッシュ & HTTPS 終端</td></tr></tbody></table></div>\n'
                                 '\n'
                                 '<h2 id="sec-3-database" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">3. データベース & ストレージ設計</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <h4 class="font-semibold text-slate-800 dark:text-slate-200">ストレージ構成</h4>\n'
                                 '<ul class="list-disc pl-6 space-y-1">\n'
                                 '  <li>WordPress アップロードファイル: PVC <code>wp-content</code></li>\n'
                                 '  <li>MariaDB データ: PVC <code>mariadb-data</code></li>\n'
                                 '</ul>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-4-screen-api" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">4. 画面 & API 仕様設計書</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <ul class="list-disc pl-6 space-y-1">\n'
                                 '  <li>公式トップページ: <code>https://www.nigiri-rice.com/</code></li>\n'
                                 '  <li>管理画面: <code>https://www.nigiri-rice.com/wp-admin/</code></li>\n'
                                 '</ul>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-5-flow" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">5. 処理フロー & シーケンス図</h2>\n'
                                 '<p class="mb-4">本システムの標準的な処理シーケンスおよびデータ連携フローです：</p>\n'
                                 '<div class="mermaid-wrapper my-6 p-4 rounded-xl border border-slate-200 '
                                 'dark:border-emerald-950/60 bg-slate-50/50 dark:bg-emerald-950/10"><pre '
                                 'class="mermaid text-sm">graph LR\n'
                                 '    User["Visitor"] -->|HTTPS:443| Caddy["Caddy (VPS)"]\n'
                                 '    Caddy -->|ClusterIP:80| WP["WordPress Pod"]\n'
                                 '    WP -->|TCP:3306| DB["MariaDB Pod"]\n'
                                 '    WP -->|NFS / PVC| Media["wp-content (Uploads)"]</pre></div>\n'
                                 '\n'
                                 '<h2 id="sec-6-runbook" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">6. README & 運用保守手順書 (Runbook)</h2>\n'
                                 '<p class="mb-4">日常保守およびトラブルシューティング時に即座に実行可能なコマンドライン一覧です：</p>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <div class="code-block-wrapper">\n'
                                 '  <div class="code-header">\n'
                                 '    <span class="code-lang">bash</span>\n'
                                 '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                 '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                 '      <span>コピー</span>\n'
                                 '    </button>\n'
                                 '  </div>\n'
                                 '  <pre><code class="language-bash"># 稼働確認\n'
                                 'kubectl get pods -n nigiri-homepage -o wide\n'
                                 '\n'
                                 '# DB バックアップ\n'
                                 'WP_POD=$(kubectl -n nigiri-homepage get pods -l app=mariadb -o '
                                 "jsonpath='{.items[0].metadata.name}')\n"
                                 'kubectl -n nigiri-homepage exec $WP_POD -- mariadb-dump -u root -p$(kubectl -n '
                                 "nigiri-homepage get secret mariadb -o jsonpath='{.data.mariadb-root-password}' | "
                                 'base64 -d) wordpress &gt; /opt/backups/db-$(date '
                                 '+%Y%m%d)/wordpress.sql</code></pre>\n'
                                 '</div>\n'
                                 '</div>\n'
                                 '\n'
                                 '<h2 id="sec-7-setup" class="text-2xl font-bold mt-10 mb-4 pb-2 border-b '
                                 'border-slate-200 dark:border-emerald-950/70">7. 環境構築 & 障害復旧手順</h2>\n'
                                 '<div class="space-y-4 mb-6">\n'
                                 '  <div class="code-block-wrapper">\n'
                                 '  <div class="code-header">\n'
                                 '    <span class="code-lang">bash</span>\n'
                                 '    <button class="copy-btn" onclick="copyCodeBlock(this)">\n'
                                 '      <i data-lucide="copy" class="w-3.5 h-3.5"></i>\n'
                                 '      <span>コピー</span>\n'
                                 '    </button>\n'
                                 '  </div>\n'
                                 '  <pre><code class="language-bash"># DB 復元\n'
                                 'cat /opt/backups/db-YYYYMMDD/wordpress.sql | kubectl -n nigiri-homepage exec -i '
                                 '$WP_POD -- mariadb -u root -p$(kubectl -n nigiri-homepage get secret mariadb -o '
                                 "jsonpath='{.data.mariadb-root-password}' | base64 -d) wordpress</code></pre>\n"
                                 '</div>\n'
                                 '</div>\n',
                 'description': 'nigiri-rice.com 公式コーポレートサイトおよびブログ・お知らせ配信を行う CMS 基盤。',
                 'icon': 'layout',
                 'id': 'wordpress',
                 'last_updated': '2026-09-12',
                 'service_id': 'wordpress',
                 'title': 'WordPress (nigiri-rice.com) 運用保守マニュアル',
                 'toc': [ {'id': 'sec-1-requirements', 'level': 2, 'title': '1. 要件定義書 (Requirements)'},
                          {'id': 'sec-2-techstack', 'level': 2, 'title': '2. 技術スタック & 選定理由'},
                          {'id': 'sec-3-database', 'level': 2, 'title': '3. データベース & ストレージ設計'},
                          {'id': 'sec-4-screen-api', 'level': 2, 'title': '4. 画面 & API 仕様設計書'},
                          {'id': 'sec-5-flow', 'level': 2, 'title': '5. 処理フロー & シーケンス図'},
                          {'id': 'sec-6-runbook', 'level': 2, 'title': '6. README & 運用保守手順書'},
                          {'id': 'sec-7-setup', 'level': 2, 'title': '7. 環境構築 & 障害復旧手順'}]}}

def get_category_docs(category_id: str) -> List[Dict[str, Any]]:
    return [d for d in DOCS.values() if d.get("category_id") == category_id]

def get_all_categories() -> List[Dict[str, Any]]:
    return CATEGORIES

def get_doc(doc_id: str) -> Optional[Dict[str, Any]]:
    return DOCS.get(doc_id)

def get_docs_tree() -> List[Dict[str, Any]]:
    tree = []
    for cat in CATEGORIES:
        docs = [d for d in DOCS.values() if d.get("category_id") == cat["id"]]
        tree.append({
            "id": cat["id"],
            "title": cat["title"],
            "icon": cat["icon"],
            "description": cat["description"],
            "docs": docs
        })
    return tree

get_categories_tree = get_docs_tree
