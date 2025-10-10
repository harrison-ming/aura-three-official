#!/usr/bin/env python3
"""
Celestial Decree - 图片批量生成脚本
使用 StellarView 的图片生成服务批量生成所有图片
"""

import os
import sys
import json
import django
from pathlib import Path
from datetime import datetime

# 添加 StellarView 到 Python 路径
STELLARVIEW_PATH = Path('/Users/ming/Documents/host/StellarView')
sys.path.insert(0, str(STELLARVIEW_PATH))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StellarView.settings')
django.setup()

# 现在可以导入 StellarView 的模块
from utils.services.image_generation_service import get_image_generation_service
import logging

LOG = logging.getLogger(__name__)

# 项目目录
PROJECT_ROOT = Path('/Users/ming/Documents/HUGO/aura-three-official/product')
PROMPTS_DIR = PROJECT_ROOT / 'prompts'
IMAGES_DIR = PROJECT_ROOT / 'images'

# 确保images目录存在
IMAGES_DIR.mkdir(exist_ok=True)

def generate_single_image(prompt, aspect_ratio, output_path, description):
    """
    生成单张图片

    Args:
        prompt: 图片生成提示词
        aspect_ratio: 宽高比
        output_path: 输出路径
        description: 图片描述（用于日志）

    Returns:
        bool: 是否成功
    """
    try:
        print(f"  🎨 生成: {description}")
        print(f"     提示词: {prompt[:80]}...")
        print(f"     宽高比: {aspect_ratio}")
        print(f"     输出: {output_path.name}")

        # 获取图片生成服务（使用MiniMax）
        image_service = get_image_generation_service(provider='minimax')

        # 生成图片
        result = image_service.generate_image(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            output_path=str(output_path)
        )

        if result and output_path.exists():
            file_size = output_path.stat().st_size / 1024  # KB
            print(f"  ✅ 成功! 文件大小: {file_size:.1f}KB\n")
            return True
        else:
            print(f"  ❌ 失败: 生成结果为空或文件不存在\n")
            return False

    except Exception as e:
        print(f"  ❌ 错误: {str(e)}\n")
        LOG.error(f"生成图片失败: {description}", exc_info=True)
        return False

def generate_main_images():
    """生成所有主要内容图片"""

    print("=" * 70)
    print("📸 开始生成主要内容图片...")
    print("=" * 70)
    print()

    # 读取prompts
    prompts_file = PROMPTS_DIR / 'celestial-decree-prompts.json'
    with open(prompts_file, 'r', encoding='utf-8') as f:
        prompts_data = json.load(f)

    total = len(prompts_data)
    success_count = 0
    failed = []

    for idx, (key, img_data) in enumerate(prompts_data.items(), 1):
        print(f"[{idx}/{total}] {img_data['description']}")
        print("-" * 70)

        output_path = IMAGES_DIR / img_data['filename']

        # 如果文件已存在，询问是否跳过
        if output_path.exists():
            print(f"  ⚠️  文件已存在，跳过: {img_data['filename']}\n")
            success_count += 1
            continue

        success = generate_single_image(
            prompt=img_data['prompt'],
            aspect_ratio=img_data['aspect_ratio'],
            output_path=output_path,
            description=img_data['description']
        )

        if success:
            success_count += 1
        else:
            failed.append({
                'key': key,
                'description': img_data['description'],
                'filename': img_data['filename']
            })

    print("=" * 70)
    print(f"✅ 主要图片生成完成: {success_count}/{total} 成功")
    if failed:
        print(f"❌ 失败 {len(failed)} 张:")
        for item in failed:
            print(f"   - {item['description']} ({item['filename']})")
    print("=" * 70)
    print()

    return success_count, len(failed)

def generate_avatar_images():
    """生成所有用户头像"""

    print("=" * 70)
    print("👤 开始生成用户头像...")
    print("=" * 70)
    print()

    # 读取头像prompts
    prompts_file = PROMPTS_DIR / 'avatar-prompts.json'
    with open(prompts_file, 'r', encoding='utf-8') as f:
        avatar_data = json.load(f)

    # 创建avatars子目录
    avatars_dir = IMAGES_DIR / 'avatars'
    avatars_dir.mkdir(exist_ok=True)

    total = len(avatar_data)
    success_count = 0
    failed = []

    for idx, avatar in enumerate(avatar_data, 1):
        print(f"[{idx}/{total}] {avatar['name']}")
        print("-" * 70)

        output_path = avatars_dir / avatar['filename']

        # 如果文件已存在，跳过
        if output_path.exists():
            print(f"  ⚠️  文件已存在，跳过: {avatar['filename']}\n")
            success_count += 1
            continue

        success = generate_single_image(
            prompt=avatar['prompt'],
            aspect_ratio='1:1',  # 头像使用正方形
            output_path=output_path,
            description=f"{avatar['name']} 头像"
        )

        if success:
            success_count += 1
        else:
            failed.append({
                'name': avatar['name'],
                'filename': avatar['filename']
            })

    print("=" * 70)
    print(f"✅ 头像生成完成: {success_count}/{total} 成功")
    if failed:
        print(f"❌ 失败 {len(failed)} 张:")
        for item in failed:
            print(f"   - {item['name']} ({item['filename']})")
    print("=" * 70)
    print()

    return success_count, len(failed)

def generate_summary_report(main_success, main_failed, avatar_success, avatar_failed):
    """生成总结报告"""

    report_lines = []
    report_lines.append("# Celestial Decree - 图片生成报告\n\n")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    report_lines.append("## 统计信息\n\n")
    report_lines.append(f"- **主要图片**: {main_success} 成功, {main_failed} 失败\n")
    report_lines.append(f"- **用户头像**: {avatar_success} 成功, {avatar_failed} 失败\n")
    report_lines.append(f"- **总计**: {main_success + avatar_success} 成功, {main_failed + avatar_failed} 失败\n\n")

    # 计算成功率
    total = main_success + main_failed + avatar_success + avatar_failed
    success_rate = ((main_success + avatar_success) / total * 100) if total > 0 else 0
    report_lines.append(f"**成功率**: {success_rate:.1f}%\n\n")

    report_lines.append("## 生成的文件\n\n")
    report_lines.append("### 主要图片\n\n")
    for img_file in sorted(IMAGES_DIR.glob('*.jpg')):
        size_kb = img_file.stat().st_size / 1024
        report_lines.append(f"- ✅ `{img_file.name}` ({size_kb:.1f}KB)\n")

    report_lines.append("\n### 用户头像\n\n")
    avatars_dir = IMAGES_DIR / 'avatars'
    if avatars_dir.exists():
        for img_file in sorted(avatars_dir.glob('*.jpg')):
            size_kb = img_file.stat().st_size / 1024
            report_lines.append(f"- ✅ `avatars/{img_file.name}` ({size_kb:.1f}KB)\n")

    # 保存报告
    report_file = PROJECT_ROOT / 'IMAGE_GENERATION_REPORT.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(''.join(report_lines))

    print(f"📄 生成报告已保存: {report_file}")

def main():
    print("\n")
    print("=" * 70)
    print("🚀 Celestial Decree - 图片批量生成")
    print("=" * 70)
    print(f"📂 输出目录: {IMAGES_DIR}")
    print(f"🔧 图片服务: MiniMax (via StellarView)")
    print("=" * 70)
    print("\n")

    # 生成主要图片
    main_success, main_failed = generate_main_images()

    # 生成头像
    avatar_success, avatar_failed = generate_avatar_images()

    # 生成总结报告
    generate_summary_report(main_success, main_failed, avatar_success, avatar_failed)

    # 最终总结
    total_success = main_success + avatar_success
    total_failed = main_failed + avatar_failed
    total = total_success + total_failed

    print("\n")
    print("=" * 70)
    print("🎉 批量生成完成!")
    print("=" * 70)
    print(f"✅ 成功: {total_success}/{total}")
    print(f"❌ 失败: {total_failed}/{total}")
    print(f"📁 输出目录: {IMAGES_DIR}")
    print("=" * 70)
    print("\n💡 下一步: 更新 Hugo 页面中的图片路径")
    print()

    return 0 if total_failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
