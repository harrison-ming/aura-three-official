#!/usr/bin/env python3
"""
生成最终的HTML页面
将生成的内容和图片组合成完整的落地页
"""

import os
import sys
import json
import base64
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / 'content'
IMAGES_DIR = PROJECT_ROOT / 'images'
OUTPUT_FILE = PROJECT_ROOT / 'index.html'

def image_to_base64(image_path):
    """将图片转换为base64编码"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def load_content():
    """加载生成的内容"""
    content_file = CONTENT_DIR / 'page-content.json'
    with open(content_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html():
    """生成完整的HTML页面"""
    
    content = load_content()
    
    # 检查必要的图片是否存在
    required_images = [
        'hero-lottery-ticket.jpg',
        'emma-portrait.jpg',
        'emma-before-struggle.jpg',
        'lottery-win-moment.jpg',
        'bracelet-product-closeup-1.jpg',
        'bracelet-pixiu-detail.jpg',
        'james-portrait.jpg',
        'james-before-unlucky.jpg',
        'james-success-handshake.jpg',
    ]
    
    missing_images = []
    for img in required_images:
        if not (IMAGES_DIR / img).exists():
            missing_images.append(img)
    
    if missing_images:
        print(f"⚠️  警告: 以下图片未找到，将使用占位符:")
        for img in missing_images:
            print(f"   - {img}")
        print()
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FengShui Bracelet - Transform Your Luck Today</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
        }}
        
        .hero {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 40px;
        }}
        
        .hero h1 {{
            font-size: 2.5em;
            margin-bottom: 20px;
            line-height: 1.2;
        }}
        
        .hero-image {{
            width: 100%;
            max-width: 700px;
            height: auto;
            border-radius: 10px;
            margin: 30px auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .section {{
            margin: 60px 0;
            padding: 20px;
        }}
        
        .section h2 {{
            font-size: 2em;
            margin-bottom: 20px;
            color: #2c3e50;
        }}
        
        .section p {{
            font-size: 1.1em;
            margin-bottom: 15px;
            line-height: 1.8;
        }}
        
        .story {{
            background: #f8f9fa;
            padding: 30px;
            border-left: 5px solid #667eea;
            margin: 30px 0;
            border-radius: 5px;
        }}
        
        .portrait {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            margin: 20px auto;
            display: block;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .quote {{
            font-style: italic;
            font-size: 1.2em;
            color: #555;
            border-left: 4px solid #f39c12;
            padding-left: 20px;
            margin: 30px 0;
        }}
        
        .product-showcase {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}
        
        .product-image {{
            width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
            color: white;
            padding: 20px 50px;
            font-size: 1.3em;
            font-weight: bold;
            text-decoration: none;
            border-radius: 50px;
            margin: 30px 0;
            box-shadow: 0 5px 20px rgba(243, 156, 18, 0.4);
            transition: transform 0.3s;
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(243, 156, 18, 0.6);
        }}
        
        .urgency-box {{
            background: #ffe5e5;
            border: 2px solid #e74c3c;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin: 40px 0;
        }}
        
        .urgency-box h3 {{
            color: #e74c3c;
            font-size: 1.8em;
            margin-bottom: 15px;
        }}
        
        .benefits-list {{
            list-style: none;
            margin: 20px 0;
        }}
        
        .benefits-list li {{
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            font-size: 1.1em;
        }}
        
        .benefits-list li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #27ae60;
            font-weight: bold;
            font-size: 1.5em;
        }}
        
        .testimonials {{
            background: #f8f9fa;
            padding: 40px 20px;
            margin: 60px 0;
        }}
        
        .testimonial {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .testimonial-avatar {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            float: left;
            margin-right: 15px;
        }}
        
        .testimonial-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            background: #2c3e50;
            color: white;
            margin-top: 60px;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 1.8em;
            }}
            
            .product-showcase {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h1>{content['hero_title']}</h1>
        </div>
        
        {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'hero-lottery-ticket.jpg') + "' class='hero-image' alt='Winning lottery ticket'>" if (IMAGES_DIR / 'hero-lottery-ticket.jpg').exists() else "<div class='hero-image' style='background:#ddd;height:400px;'></div>"}
        
        <!-- Intro Hook -->
        <div class="section">
            {_format_text_to_html(content['intro_hook'])}
        </div>
        
        <!-- Emma's Story -->
        <div class="story">
            <h2>Emma's Story: From Struggle to $250,000</h2>
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'emma-portrait.jpg') + "' class='portrait' alt='Emma portrait'>" if (IMAGES_DIR / 'emma-portrait.jpg').exists() else ""}
            
            {_format_text_to_html(content['story_struggle'])}
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'emma-before-struggle.jpg') + "' class='product-image' alt='Emma before' style='margin: 20px 0;'>" if (IMAGES_DIR / 'emma-before-struggle.jpg').exists() else ""}
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'lottery-win-moment.jpg') + "' class='product-image' alt='Lottery win moment' style='margin: 20px 0;'>" if (IMAGES_DIR / 'lottery-win-moment.jpg').exists() else ""}
            
            <div class="quote">
                {_extract_quote(content['story_quote'])}
            </div>
        </div>
        
        <!-- Product Introduction -->
        <div class="section">
            <h2>The Secret: FengShui Bracelet™</h2>
            {_format_text_to_html(content['product_intro'])}
        </div>
        
        <!-- Product Showcase -->
        <div class="product-showcase">
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'bracelet-product-closeup-1.jpg') + "' class='product-image' alt='FengShui Bracelet'>" if (IMAGES_DIR / 'bracelet-product-closeup-1.jpg').exists() else "<div class='product-image' style='background:#ddd;height:300px;'></div>"}
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'bracelet-pixiu-detail.jpg') + "' class='product-image' alt='Pixiu charm detail'>" if (IMAGES_DIR / 'bracelet-pixiu-detail.jpg').exists() else "<div class='product-image' style='background:#ddd;height:300px;'></div>"}
        </div>
        
        <div class="section" style="text-align: center;">
            <a href="#order" class="cta-button">Check Availability ➤➤</a>
        </div>
        
        <!-- James's Story -->
        <div class="story">
            <h2>{content['second_story_title']}</h2>
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'james-portrait.jpg') + "' class='portrait' alt='James portrait'>" if (IMAGES_DIR / 'james-portrait.jpg').exists() else ""}
            
            {_format_text_to_html(content['second_story_intro'])}
            {_format_text_to_html(content['second_story_skepticism'])}
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'james-before-unlucky.jpg') + "' class='product-image' alt='James before' style='margin: 20px 0;'>" if (IMAGES_DIR / 'james-before-unlucky.jpg').exists() else ""}
            
            {_format_text_to_html(content['second_story_results'])}
            
            {"<img src='data:image/jpeg;base64," + image_to_base64(IMAGES_DIR / 'james-success-handshake.jpg') + "' class='product-image' alt='James success' style='margin: 20px 0;'>" if (IMAGES_DIR / 'james-success-handshake.jpg').exists() else ""}
            
            <div class="quote">
                {_extract_quote(content['second_story_quote'])}
            </div>
        </div>
        
        <!-- Science Section -->
        <div class="section">
            <h2>{content['science_section_title']}</h2>
            {_format_text_to_html(content['science_explanation'])}
        </div>
        
        <!-- Urgency CTA -->
        <div class="urgency-box">
            <h3>⚠️ WARNING: Stock Running Out Fast</h3>
            {_format_text_to_html(content['cta_urgency'])}
            <a href="#order" class="cta-button" style="margin-top: 20px;">CLAIM YOUR 50% DISCOUNT →</a>
        </div>
        
        <!-- Final CTA -->
        <div class="section" style="text-align: center;">
            {_format_text_to_html(content['final_cta'])}
            <br><br>
            <a href="#order" class="cta-button">Click Here To Apply 50% Discount And Check Availability ➤➤</a>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="footer">
        <p>&copy; {datetime.now().year} FengShui Bracelet™. All rights reserved.</p>
        <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
            AI-Generated Version 2.0 | Original concept based on feng shui principles
        </p>
    </div>
    
    <script>
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content

def _format_text_to_html(text):
    """将文本格式化为HTML段落"""
    paragraphs = text.strip().split('\n\n')
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # 检查是否是列表项
            if p.startswith('•') or p.startswith('✓'):
                items = [item.strip() for item in p.split('\n') if item.strip()]
                html_parts.append('<ul class="benefits-list">')
                for item in items:
                    # 移除列表符号
                    clean_item = item.lstrip('•✓ ')
                    html_parts.append(f'<li>{clean_item}</li>')
                html_parts.append('</ul>')
            else:
                html_parts.append(f'<p>{p.replace(chr(10), "<br>")}</p>')
    return '\n'.join(html_parts)

def _extract_quote(text):
    """提取引用文本"""
    lines = text.strip().split('\n')
    quote_lines = [line.strip(' "') for line in lines if line.strip()]
    return '<br>'.join(quote_lines)

# 将这些方法变成类的静态方法
class HTMLGenerator:
    @staticmethod
    def format_text_to_html(text):
        return _format_text_to_html(text)
    
    @staticmethod
    def extract_quote(text):
        return _extract_quote(text)

def main():
    print("🌐 生成HTML页面...\n")
    
    # 检查内容文件是否存在
    if not (CONTENT_DIR / 'page-content.json').exists():
        print("❌ 错误: 内容文件不存在")
        print("   请先运行: python3 02_generate_content_and_prompts.py")
        return 1
    
    # 检查images目录
    if not IMAGES_DIR.exists() or not any(IMAGES_DIR.glob('*.jpg')):
        print("⚠️  警告: 图片目录为空或不存在")
        print("   请先运行: python3 03_generate_images.py")
        print("   或者继续生成带占位符的HTML")
        response = input("\n继续生成? (y/n): ")
        if response.lower() != 'y':
            return 0
    
    try:
        # 生成HTML
        html_content = generate_html()
        
        # 保存文件
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        file_size = OUTPUT_FILE.stat().st_size / 1024 / 1024  # MB
        
        print("✅ HTML页面生成成功!")
        print(f"📄 文件: {OUTPUT_FILE}")
        print(f"📦 大小: {file_size:.2f}MB")
        print(f"\n💡 在浏览器中打开: open {OUTPUT_FILE}")
        
        return 0
        
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
