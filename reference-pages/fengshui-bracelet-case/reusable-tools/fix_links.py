#!/usr/bin/env python3
import re
from pathlib import Path
import urllib.parse

def fix_html_links():
    html_file = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages/index.html')
    
    # 读取 HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 备份原文件
    backup_file = html_file.with_suffix('.html.backup')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Backup created: {backup_file}")
    
    # 替换规则
    replacements = [
        # CSS 文件
        (r'href="/core\.min\.css"', 'href="css/core.min.css"'),
        
        # JS 文件
        (r'src="/core\.min\.js"', 'src="js/core.min.js"'),
        
        # Funnelish 图片 - 协议相对 URL (//img.funnelish.com/)
        (r'//img\.funnelish\.com/', 'images/'),
        
        # Funnelish 图片 - 完整 URL
        (r'https://img\.funnelish\.com/', 'images/'),
        
        # Random user 图片
        (r'https://randomuser\.me/api/', 'images/api/'),
    ]
    
    # 应用替换
    modified_content = html_content
    for pattern, replacement in replacements:
        count = len(re.findall(pattern, modified_content))
        modified_content = re.sub(pattern, replacement, modified_content)
        print(f"✓ Replaced {count} occurrences of '{pattern}' with '{replacement}'")
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"\n✓ HTML links fixed successfully!")
    print(f"✓ Original file backed up to: {backup_file}")
    print(f"✓ Modified file: {html_file}")

if __name__ == '__main__':
    fix_html_links()
