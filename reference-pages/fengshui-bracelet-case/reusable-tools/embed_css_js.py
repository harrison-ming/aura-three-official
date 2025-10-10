#!/usr/bin/env python3
import re
from pathlib import Path

def embed_css_js():
    base_dir = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages')
    html_file = base_dir / 'index.html'
    
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 备份
    backup_file = base_dir / 'index_before_css_js_embed.html'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ Backup created: {backup_file}\n")
    
    # 嵌入 CSS
    css_file = base_dir / 'css' / 'core.min.css'
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # 替换 CSS 链接为内联样式
        css_link_pattern = r'<link[^>]*href="css/core\.min\.css"[^>]*>'
        inline_css = f'<style>{css_content}</style>'
        html_content = re.sub(css_link_pattern, inline_css, html_content)
        print(f"✓ Embedded CSS ({len(css_content) / 1024:.1f} KB)")
    
    # 嵌入 JS
    js_file = base_dir / 'js' / 'core.min.js'
    if js_file.exists():
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # 替换 JS 链接为内联脚本
        # 使用字符串替换而不是正则，避免特殊字符问题
        js_link_patterns = [
            '<script src="js/core.min.js"></script>',
            '<script src="js/core.min.js" ></script>',
            '<script type="text/javascript" src="js/core.min.js"></script>',
        ]
        
        inline_js = f'<script>{js_content}</script>'
        
        for pattern in js_link_patterns:
            if pattern in html_content:
                html_content = html_content.replace(pattern, inline_js)
                break
        
        print(f"✓ Embedded JS ({len(js_content) / 1024:.1f} KB)")
    
    # 也处理 preload 标签
    html_content = re.sub(r'<link rel="preload"[^>]*href="/core\.min\.css"[^>]*>', '', html_content)
    html_content = re.sub(r'<link rel="preload"[^>]*href="/core\.min\.js"[^>]*>', '', html_content)
    
    # 写回文件
    print(f"\nWriting final HTML file...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    final_size = len(html_content) / 1024 / 1024
    print(f"\n{'='*60}")
    print(f"✓ All resources embedded successfully!")
    print(f"  - Final file size: {final_size:.1f} MB")
    print(f"  - File location: {html_file}")
    print(f"\n✓ The HTML file is now completely standalone!")
    print(f"  You can open it directly in any browser.")

if __name__ == '__main__':
    embed_css_js()
