#!/bin/bash

# サイドバー追加用のスクリプト

# 追加するCSS（.container の定義の後に追加）
SIDEBAR_CSS='
  /* 2カラムレイアウト */
  .content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    gap: 32px;
    align-items: flex-start;
  }
  .main-content {
    flex: 1;
    max-width: 780px;
  }
  .sidebar {
    width: 280px;
    flex-shrink: 0;
    position: sticky;
    top: 80px;
  }
  .sidebar-section {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .sidebar-section h3 {
    font-size: 14px;
    font-weight: 900;
    color: var(--color-text);
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--color-accent);
  }
  .sidebar-section h3::after {
    display: none;
  }
  .sidebar-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .sidebar-list li {
    padding: 0;
    margin-bottom: 12px;
  }
  .sidebar-list li::before {
    display: none;
  }
  .sidebar-list a {
    color: var(--color-text);
    text-decoration: none;
    font-size: 13px;
    line-height: 1.6;
    display: block;
    transition: color 0.2s;
  }
  .sidebar-list a:hover {
    color: var(--color-accent);
  }
  .sidebar-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .sidebar-tags li {
    margin: 0;
    padding: 0;
  }
  .sidebar-tags li::before {
    display: none;
  }
  .sidebar-tag {
    display: inline-block;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    color: var(--color-accent);
    background: #fff;
    border: 1px solid var(--color-accent);
    border-radius: 12px;
    text-decoration: none;
    transition: all 0.2s;
  }
  .sidebar-tag:hover {
    background: var(--color-accent);
    color: #fff;
  }

  @media (max-width: 1024px) {
    .content-wrapper {
      flex-direction: column;
    }
    .sidebar {
      width: 100%;
      position: static;
      max-width: 780px;
      margin: 0 auto;
    }
  }

  @media (max-width: 768px) {
    .content-wrapper {
      padding: 0 16px;
    }
    .sidebar-section {
      padding: 16px;
    }
  }
'

# 追加するHTML（サイドバー部分）
SIDEBAR_HTML='
      <aside class="sidebar">
        <div class="sidebar-section">
          <h3>最新記事</h3>
          <ul class="sidebar-list">
            <li><a href="../backtest-overview/">トレードシステム概要編</a></li>
            <li><a href="../backtest-failures/">トレードシステム失敗編</a></li>
            <li><a href="../backtest-method/">トレードシステム仕組み編</a></li>
            <li><a href="../multi-agent-flow/">マルチエージェント連携</a></li>
            <li><a href="../cron-heartbeat/">cron + heartbeat</a></li>
          </ul>
        </div>
        
        <div class="sidebar-section">
          <h3>人気記事</h3>
          <ul class="sidebar-list">
            <li><a href="../soul-md-merged/">SOUL.mdの書き方</a></li>
            <li><a href="../token-efficiency/">AGENTS.mdを83%削減した話</a></li>
            <li><a href="../backtest-overview/">非エンジニアがAIに28,000行のトレードシステムを作らせた話</a></li>
          </ul>
        </div>
        
        <div class="sidebar-section">
          <h3>タグ</h3>
          <ul class="sidebar-tags">
            <li><span class="sidebar-tag">OpenClaw</span></li>
            <li><span class="sidebar-tag">Claude Code</span></li>
            <li><span class="sidebar-tag">トレードシステム</span></li>
            <li><span class="sidebar-tag">ComfyUI</span></li>
            <li><span class="sidebar-tag">自動化</span></li>
            <li><span class="sidebar-tag">コスト削減</span></li>
          </ul>
        </div>
      </aside>
'

echo "サイドバー追加スクリプトを実行します..."

# 対象ファイル
files=(
  "day1/index.html"
  "soul-md-merged/index.html"
  "comfyui/index.html"
  "morning-briefing/index.html"
  "token-efficiency/index.html"
  "cron-heartbeat/index.html"
  "multi-agent-flow/index.html"
  "backtest-overview/index.html"
  "backtest-failures/index.html"
  "backtest-method/index.html"
)

# aboutがあれば追加
if [ -f "about/index.html" ]; then
  files+=("about/index.html")
fi

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "処理中: $file"
    
    # バックアップ
    cp "$file" "$file.bak"
    
    # 処理は後続でPythonスクリプトに任せる
  else
    echo "スキップ（ファイルなし）: $file"
  fi
done

echo "完了"
