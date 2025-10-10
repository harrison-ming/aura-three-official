#!/usr/bin/env python3
import os
import re
import base64
from pathlib import Path

def get_image_base64(image_path):
    """将图片转换为 base64 编码"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            
            # 根据扩展名判断 MIME 类型
            ext = os.path.splitext(image_path)[1].lower()
            mime_map = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_map.get(ext, 'image/jpeg')
            
            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"✗ Error reading {image_path}: {e}")
        return None

def embed_comment_avatars():
    base_dir = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages')
    html_file = base_dir / 'index.html'
    
    # 读取 HTML
    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"Original file size: {len(html_content) / 1024 / 1024:.1f} MB\n")
    
    # 查找所有评论区的图片
    pattern = r'src=images/api/portraits/(men|women)/(\d+)\.jpg'
    matches = list(re.finditer(pattern, html_content))
    
    print(f"Found {len(matches)} avatar images\n")
    
    replaced_count = 0
    
    # 从后往前替换
    for match in reversed(matches):
        gender = match.group(1)
        number = match.group(2)
        img_url = f"images/api/portraits/{gender}/{number}.jpg"
        local_path = base_dir / img_url
        
        if local_path.exists():
            base64_data = get_image_base64(local_path)
            
            if base64_data:
                # 替换
                start, end = match.span()
                html_content = html_content[:start] + f'src={base64_data}' + html_content[end:]
                
                print(f"✓ Embedded: {gender}/{number}.jpg ({local_path.stat().st_size / 1024:.1f} KB)")
                replaced_count += 1
        else:
            print(f"✗ Not found: {img_url}")
    
    # 写回文件
    print(f"\nWriting updated HTML file...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n{'='*60}")
    print(f"✓ Avatar embedding complete!")
    print(f"  - Successfully embedded: {replaced_count} avatars")
    print(f"  - New file size: {len(html_content) / 1024 / 1024:.1f} MB")

if __name__ == '__main__':
    embed_comment_avatars()
