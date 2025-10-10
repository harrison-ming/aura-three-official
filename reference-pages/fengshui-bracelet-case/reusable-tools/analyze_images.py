#!/usr/bin/env python3
"""
分析 FengShui Bracelet 营销页面
- 文案结构
- 情感调动
- 转化策略
- 视觉设计
"""

import os
from pathlib import Path

# 设置路径
base_dir = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages')
images_dir = base_dir / 'images'

# 统计图片
image_files = []
for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            rel_path = Path(root).relative_to(images_dir)
            image_files.append({
                'name': file,
                'path': str(rel_path / file),
                'size': (Path(root) / file).stat().st_size,
                'type': 'gif' if file.endswith('.gif') else 'static'
            })

# 分类图片
product_images = [img for img in image_files if 'FENGSHUI' in img['name'].upper() or 'bracelet' in img['name'].lower()]
lifestyle_images = [img for img in image_files if 'Gemini' in img['name'] or 'ChatGPT' in img['name']]
avatar_images = [img for img in image_files if 'portraits' in img['path']]
icon_images = [img for img in image_files if 'check' in img['name'].lower()]
animated_images = [img for img in image_files if img['type'] == 'gif']

print("=" * 80)
print("图片资源统计")
print("=" * 80)
print(f"\n总图片数: {len(image_files)}")
print(f"- 产品展示图: {len(product_images)}")
print(f"- 生活场景图: {len(lifestyle_images)}")
print(f"- 用户头像: {len(avatar_images)}")
print(f"- 图标: {len(icon_images)}")
print(f"- 动画GIF: {len(animated_images)}")

print("\n\n" + "=" * 80)
print("动画图片详情 (关键视觉元素)")
print("=" * 80)
for img in animated_images:
    print(f"\n文件名: {img['name']}")
    print(f"大小: {img['size'] / 1024 / 1024:.2f} MB")
    print(f"位置: {img['path']}")

print("\n\n" + "=" * 80)
print("产品图片详情")
print("=" * 80)
for img in product_images:
    print(f"\n文件名: {img['name']}")
    print(f"大小: {img['size'] / 1024:.1f} KB")

print("\n\n" + "=" * 80)
print("分析完成")
print("=" * 80)
