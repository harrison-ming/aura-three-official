#!/usr/bin/env python3
import os
import re
import base64
from pathlib import Path
import mimetypes

def get_image_base64(image_path):
    """将图片转换为 base64 编码"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            
            # 获取 MIME 类型
            mime_type = mimetypes.guess_type(image_path)[0]
            if not mime_type:
                # 根据扩展名手动判断
                ext = os.path.splitext(image_path)[1].lower()
                mime_map = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }
                mime_type = mime_map.get(ext, 'image/png')
            
            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"✗ Error reading {image_path}: {e}")
        return None

def find_local_image_path(relative_url, base_dir):
    """根据相对 URL 找到本地图片文件"""
    # 清理 URL，移除查询参数
    clean_url = relative_url.split('?')[0]
    
    # 构建可能的路径
    possible_paths = [
        base_dir / clean_url.lstrip('/'),
        base_dir / clean_url.replace('images/', ''),
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # 如果找不到，尝试在 images 目录下搜索文件名
    filename = os.path.basename(clean_url)
    for root, dirs, files in os.walk(base_dir / 'images'):
        if filename in files:
            return Path(root) / filename
    
    return None

def embed_images_in_html():
    base_dir = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages')
    html_file = base_dir / 'index.html'
    
    # 读取 HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 备份原文件
    backup_file = base_dir / 'index_before_embed.html'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Backup created: {backup_file}\n")
    
    # 查找所有图片标签
    img_pattern = r'<img[^>]*?(?:src|data-src)=["\']([^"\']+)["\'][^>]*?>'
    matches = list(re.finditer(img_pattern, html_content))
    
    print(f"Found {len(matches)} image tags\n")
    
    replaced_count = 0
    failed_count = 0
    
    # 从后往前替换，避免位置偏移
    for match in reversed(matches):
        img_tag = match.group(0)
        
        # 提取所有 src 和 data-src 属性
        src_match = re.search(r'(?:src|data-src)=["\']([^"\']+)["\']', img_tag)
        if not src_match:
            continue
        
        img_url = src_match.group(1)
        
        # 跳过已经是 data: URL 的图片
        if img_url.startswith('data:'):
            continue
        
        # 跳过外部字体等非图片资源
        if 'fonts.gstatic.com' in img_url:
            continue
        
        # 查找本地图片文件
        local_path = find_local_image_path(img_url, base_dir)
        
        if local_path and local_path.exists():
            # 转换为 base64
            base64_data = get_image_base64(local_path)
            
            if base64_data:
                # 替换所有的 src 和 data-src 为 base64
                new_img_tag = img_tag
                new_img_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{base64_data}"', new_img_tag)
                new_img_tag = re.sub(r'data-src=["\'][^"\']+["\']', f'data-src="{base64_data}"', new_img_tag)
                new_img_tag = re.sub(r'data-srcset=["\'][^"\']+["\']', '', new_img_tag)  # 移除 srcset
                
                # 替换 HTML 内容
                start, end = match.span()
                html_content = html_content[:start] + new_img_tag + html_content[end:]
                
                print(f"✓ Embedded: {os.path.basename(img_url)} ({local_path.stat().st_size / 1024:.1f} KB)")
                replaced_count += 1
            else:
                print(f"✗ Failed to encode: {img_url}")
                failed_count += 1
        else:
            print(f"✗ Not found: {img_url}")
            failed_count += 1
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n{'='*60}")
    print(f"✓ Embedding complete!")
    print(f"  - Successfully embedded: {replaced_count} images")
    print(f"  - Failed: {failed_count} images")
    print(f"  - Original file backed up to: {backup_file}")
    print(f"  - Modified file: {html_file}")
    
    # 显示文件大小
    original_size = backup_file.stat().st_size / 1024
    new_size = html_file.stat().st_size / 1024
    print(f"\nFile sizes:")
    print(f"  - Original: {original_size:.1f} KB")
    print(f"  - With embedded images: {new_size:.1f} KB")
    print(f"  - Increase: {new_size - original_size:.1f} KB")

if __name__ == '__main__':
    embed_images_in_html()
