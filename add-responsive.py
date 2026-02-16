#!/usr/bin/env python3

import os

# 記事ページ用の共通レスポンシブCSS
RESPONSIVE_CSS = '''
  /* スマホ対応 */
  @media (max-width: 768px) {
    .header-inner {
      padding: 0 16px;
    }
    .logo {
      font-size: 16px;
    }
    .breadcrumb {
      font-size: 11px;
    }
    .hero {
      padding: 40px 0 30px;
    }
    .hero-bg-num {
      font-size: 200px;
      top: -20px;
      left: -10px;
    }
    .hero-inner {
      padding: 0 16px;
    }
    .hero-label {
      font-size: 12px;
      margin-bottom: 12px;
    }
    .hero-title {
      gap: 8px;
    }
    .hero-num {
      font-size: 80px;
    }
    .hero-text .line1,
    .hero-text .line2 {
      font-size: 20px;
    }
    .hero-text .line3 {
      font-size: 18px;
    }
    .hero-sep {
      width: 60px;
      height: 2px;
      margin: 12px 0;
    }
    .hero-meta {
      font-size: 12px;
    }
    .article {
      padding: 40px 16px;
    }
    .article h2 {
      font-size: 22px;
      margin-top: 48px;
      margin-bottom: 20px;
      padding: 12px 16px;
    }
    .article h3 {
      font-size: 19px;
      margin-top: 40px;
      margin-bottom: 16px;
    }
    .article h4 {
      font-size: 17px;
      margin-top: 32px;
      margin-bottom: 14px;
    }
    .article p {
      font-size: 15px;
      margin-bottom: 24px;
    }
    .article ul,
    .article ol {
      font-size: 15px;
      padding-left: 24px;
    }
    .article pre {
      font-size: 13px;
      padding: 16px;
      margin: 24px 0;
      overflow-x: auto;
    }
    .article code {
      font-size: 13px;
    }
    .article blockquote {
      font-size: 15px;
      padding: 16px 16px 16px 20px;
      margin: 24px 0;
    }
    .article img {
      max-width: 100%;
      height: auto;
    }
    .info-box,
    .meta-block {
      padding: 20px 16px;
      margin: 24px 0;
      font-size: 14px;
    }
    .next-article,
    .read-next {
      padding: 24px 16px;
      margin: 40px 0 0;
    }
    .next-article h3,
    .read-next h3 {
      font-size: 18px;
      margin-bottom: 12px;
    }
    .next-article .next-title,
    .read-next .next-title {
      font-size: 18px;
      margin-bottom: 8px;
    }
    .next-article .next-desc,
    .read-next .next-desc {
      font-size: 13px;
    }
    .footer {
      padding: 32px 16px;
      font-size: 12px;
    }
  }
'''

# 対象ファイルリスト
FILES = [
    "day1/index.html",
    "soul-md-merged/index.html",
    "comfyui/index.html",
    "morning-briefing/index.html",
    "token-efficiency/index.html",
    "cron-heartbeat/index.html",
    "multi-agent-flow/index.html",
    "about/index.html"
]

for filepath in FILES:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # すでにレスポンシブCSSがあるかチェック
    if "/* スマホ対応 */" in content:
        print(f"  -> Already has responsive CSS, skipping")
        continue
    
    # </style>の直前に挿入
    content = content.replace("</style>", RESPONSIVE_CSS + "\n</style>")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  -> Added responsive CSS")

print("Done!")
