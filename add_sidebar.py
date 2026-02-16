#!/usr/bin/env python3
"""
ブログ記事にサイドバーを追加するスクリプト
"""

import os
import re
from pathlib import Path

SIDEBAR_CSS = """
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
"""

SIDEBAR_HTML = """      <aside class="sidebar">
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
      </aside>"""


def process_file(filepath):
    """HTMLファイルにサイドバーを追加"""
    print(f"処理中: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 既にサイドバーがあるかチェック
    if 'class="sidebar"' in content:
        print(f"  スキップ（既にサイドバーあり）")
        return
    
    # CSSを追加（.containerの定義の後に）
    # .container { の直後の } を探して、その後に追加
    css_pattern = r'(\.container\s*{[^}]+})'
    css_match = re.search(css_pattern, content)
    
    if css_match:
        # CSSを追加
        insert_pos = css_match.end()
        content = content[:insert_pos] + '\n' + SIDEBAR_CSS + content[insert_pos:]
    else:
        print(f"  警告: .containerのCSS定義が見つかりません")
        return
    
    # HTMLを変更: <div class="container"> を見つけて、content-wrapperで囲む
    # <div class="container"> を <div class="content-wrapper"><div class="main-content"> に変更
    # </div> の最後の前にサイドバーを追加
    
    # まず <div class="container"> を探す
    container_start_pattern = r'<div class="container">'
    container_start_match = re.search(container_start_pattern, content)
    
    if not container_start_match:
        print(f"  警告: <div class=\"container\"> が見つかりません")
        return
    
    # <div class="container">を置換
    content = content.replace(
        '<div class="container">',
        '<div class="content-wrapper">\n  <div class="main-content">',
        1  # 最初の1個だけ
    )
    
    # 最後の</div>の前にサイドバーを挿入
    # </body>の前で</div>を2つ閉じる必要がある
    # 戦略: </body>の直前に来る</div>を探して、その前にサイドバーを挿入
    
    # bodyの終了タグの位置を探す
    body_end_pattern = r'</body>'
    body_end_match = re.search(body_end_pattern, content)
    
    if not body_end_match:
        print(f"  警告: </body> が見つかりません")
        return
    
    # </body>の前に戻って、最後の</div>を探す
    before_body = content[:body_end_match.start()]
    # 最後の</div>を探す
    last_div_end = before_body.rfind('</div>')
    
    if last_div_end == -1:
        print(f"  警告: 終了</div>が見つかりません")
        return
    
    # その</div>の前にサイドバーを挿入し、さらに</div>を1つ追加
    content = (
        content[:last_div_end] +
        '\n' + SIDEBAR_HTML + '\n' +
        '  </div>\n' +  # main-content の終了
        content[last_div_end:]  # 元の</div>（これがcontent-wrapperの終了になる）
    )
    
    # ファイルに書き出し
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  完了")


def main():
    """メイン処理"""
    base_dir = Path('/tmp/blog-work')
    
    articles = [
        'day1',
        'soul-md-merged',
        'comfyui',
        'morning-briefing',
        'token-efficiency',
        'cron-heartbeat',
        'multi-agent-flow',
        'backtest-overview',
        'backtest-failures',
        'backtest-method',
        'about',
    ]
    
    for article in articles:
        filepath = base_dir / article / 'index.html'
        if filepath.exists():
            try:
                process_file(filepath)
            except Exception as e:
                print(f"  エラー: {e}")
        else:
            print(f"スキップ（ファイルなし）: {filepath}")
    
    print("\n全ファイルの処理が完了しました")


if __name__ == '__main__':
    main()
