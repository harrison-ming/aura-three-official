#!/usr/bin/env python3
"""
从原始网页中提取文本结构和图片位置
为生成新版本提供参考模板
"""

import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json

# 原网页路径
ORIGINAL_HTML = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages/fengshui-bracelet-case/product-specific/content/index.html')
OUTPUT_DIR = Path(__file__).parent.parent / 'analysis'
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_text_structure(html_file):
    """提取HTML的文本结构和图片位置"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    structure = {
        'title': '',
        'sections': [],
        'images': [],
        'cta_buttons': []
    }
    
    # 提取标题
    title_tag = soup.find('title')
    if title_tag:
        structure['title'] = title_tag.get_text(strip=True)
    
    # 提取所有图片
    images = soup.find_all('img')
    for idx, img in enumerate(images, 1):
        img_info = {
            'index': idx,
            'src': img.get('src', '')[:100],  # 截短路径
            'alt': img.get('alt', ''),
            'context': ''
        }
        
        # 获取图片周围的文本作为上下文
        parent = img.find_parent(['div', 'section', 'article', 'figure'])
        if parent:
            text_content = parent.get_text(strip=True)[:200]
            img_info['context'] = text_content
        
        structure['images'].append(img_info)
    
    # 提取主要文本段落
    # 查找包含主要内容的元素
    main_content = soup.find('body')
    if main_content:
        # 提取所有h1-h6标题
        headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            heading_text = heading.get_text(strip=True)
            if heading_text and len(heading_text) > 3:
                structure['sections'].append({
                    'type': 'heading',
                    'level': heading.name,
                    'text': heading_text
                })
        
        # 提取段落
        paragraphs = main_content.find_all('p')
        for p in paragraphs:
            p_text = p.get_text(strip=True)
            if p_text and len(p_text) > 20:  # 过滤掉太短的段落
                structure['sections'].append({
                    'type': 'paragraph',
                    'text': p_text[:500]  # 最多500字符
                })
    
    # 提取CTA按钮
    buttons = soup.find_all(['button', 'a'], class_=re.compile(r'button|btn|cta', re.I))
    for btn in buttons:
        btn_text = btn.get_text(strip=True)
        if btn_text and len(btn_text) < 100:
            structure['cta_buttons'].append({
                'text': btn_text,
                'href': btn.get('href', '')
            })
    
    return structure

def save_structure(structure, output_file):
    """保存提取的结构到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)
    print(f"✅ 结构已保存到: {output_file}")

def generate_markdown_summary(structure, output_file):
    """生成Markdown格式的摘要"""
    lines = []
    lines.append("# 原网页结构分析\n")
    lines.append(f"## 标题: {structure['title']}\n")
    
    lines.append(f"## 图片统计: 共{len(structure['images'])}张\n")
    for img in structure['images'][:10]:  # 只显示前10张
        lines.append(f"- 图片{img['index']}: {img['alt'] or '无alt'}")
        if img['context']:
            lines.append(f"  - 上下文: {img['context'][:100]}...")
        lines.append("")
    
    lines.append(f"\n## 内容段落: 共{len(structure['sections'])}个\n")
    for idx, section in enumerate(structure['sections'][:30], 1):  # 只显示前30个
        if section['type'] == 'heading':
            lines.append(f"### {section['text']}\n")
        else:
            lines.append(f"{idx}. {section['text'][:200]}...\n")
    
    lines.append(f"\n## CTA按钮: 共{len(structure['cta_buttons'])}个\n")
    for btn in structure['cta_buttons'][:10]:
        lines.append(f"- \"{btn['text']}\" → {btn['href']}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ Markdown摘要已保存到: {output_file}")

def main():
    print(f"🔍 分析原网页: {ORIGINAL_HTML}")
    
    if not ORIGINAL_HTML.exists():
        print(f"❌ 文件不存在: {ORIGINAL_HTML}")
        return 1
    
    # 提取结构
    structure = extract_text_structure(ORIGINAL_HTML)
    
    # 保存JSON
    json_output = OUTPUT_DIR / 'original_structure.json'
    save_structure(structure, json_output)
    
    # 保存Markdown
    md_output = OUTPUT_DIR / 'original_structure.md'
    generate_markdown_summary(structure, md_output)
    
    print(f"\n📊 统计信息:")
    print(f"  - 图片数量: {len(structure['images'])}")
    print(f"  - 内容段落: {len(structure['sections'])}")
    print(f"  - CTA按钮: {len(structure['cta_buttons'])}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
