#!/usr/bin/env python3
"""
FengShui Bracelet AI版本生成器
基于原网页结构，生成新的内容和AI图片
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / 'prompts'
IMAGES_DIR = PROJECT_ROOT / 'images'
CONTENT_DIR = PROJECT_ROOT / 'content'

# 确保目录存在
PROMPTS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
CONTENT_DIR.mkdir(exist_ok=True)

# 新的人物名字
NEW_CHARACTERS = {
    'female_lead': 'Emma',
    'male_lead': 'James',
    'location_female': 'Seattle',
    'location_male': 'Boston'
}

# 内容模板（基于原网页结构）
CONTENT_TEMPLATE = {
    'hero_title': "How One {location} Mom Turned $1 Into $250,000 Overnight With This Forbidden Ancient Bracelet Trick",
    
    'intro_hook': """Life feels rigged sometimes.

But what if you could flip that script?

What if luck wasn't random… but something you could control?

Think about it…

How many times have you seen someone else hit the jackpot…
Win the lottery…
Land that dream job…
Marry rich or stumble into life-changing money…

…while you're stuck thinking:

"When's it going to be my turn?"

{name} from {location} knows that feeling better than anyone.""",
    
    'story_struggle': """{name} was grinding away as a customer support rep for over a decade.

Ten years of clocking in, clocking out, barely scraping by.

Drowning in debt.

Waiting for something — anything — to finally go her way.

Then… one tiny, ancient secret flipped her life upside down.

She bought a $1 ticket… then forgot about it.

Every number matched.

She had just won $250,000.""",
    
    'story_quote': """"I still can't believe it. I've been broke my entire adult life. Now I'm sitting on a quarter million dollars. It's like the universe finally decided to give me a break."

That "break" wasn't random.

It was this.""",
    
    'product_intro': """The FengShui Bracelet™

A powerful talisman based on the ancient Chinese art of feng shui.

Handcrafted from volcanic obsidian and featuring the legendary Pixiu charm, it rebalances your energy field… attracting wealth, luck, and opportunity straight to you.

Sounds wild, right?

But here's the thing…

Thousands of people — just like {name} — are now wearing it.

And their lives are changing in ways that seem almost… impossible.""",
    
    'second_story_title': """From "Unluckiest Man Alive" to Life-Changing Fortune""",
    
    'second_story_intro': """Meet {male_name}.

For years, {male_name} felt cursed.

If he ordered food, the kitchen "ran out."
If he applied for a job, someone less qualified got it.
His friends joked he had a permanent storm cloud over his head.

Then a co-worker told him about the FengShui Bracelet™.""",
    
    'second_story_skepticism': """"{male_name} was skeptical at first — who wouldn't be?

But desperate times call for desperate measures.

He got the bracelet.

And slowly, things started to shift.

First, small things.

Then… big ones.""",
    
    'second_story_results': """Within two months:

✓ His boss offered him a promotion with double his salary
✓ An estranged relative passed away and left him an unexpected inheritance
✓ He met someone who introduced him to a business opportunity that's now his main income

He didn't win the lottery — but his life completely transformed.""",
    
    'second_story_quote': """"For years I felt invisible… like the universe had it out for me. After this bracelet, it was like someone flipped a switch. Suddenly things started working out for me instead of against me."

— {male_name}, {male_location}""",
    
    'science_section_title': """Why Does This Bracelet Work?""",
    
    'science_explanation': """It's not magic.

It's energy.

Ancient Chinese philosophers discovered that everything — including humans — vibrates at a specific frequency.

When your energy is blocked or imbalanced, you attract:

• Bad luck
• Financial struggle
• Missed opportunities
• Constant setbacks

The FengShui Bracelet™ works by:

1. Clearing energy blockages that repel wealth
2. Activating the "luck frequency" using volcanic obsidian (a powerful grounding stone)
3. Channeling abundance through the Pixiu charm — a mythical creature known for attracting and protecting wealth

Think of it like this:

Your energy is like a radio signal.

When it's fuzzy or blocked, you can't tune into the "wealth station."

The bracelet clears the static… and suddenly, opportunities start flowing your way.""",
    
    'testimonials_title': """Real People. Real Results.""",
    
    'cta_urgency': """⚠️ WARNING: Stock Running Out Fast

Due to overwhelming demand and limited production (each bracelet is handcrafted), stock sells out within days of every restock.

Right now, they're offering 50% OFF for new customers — but only while supplies last.

Don't wait.

If you've been stuck in the same financial situation for years… if you feel like good things only happen to other people… this might be your turn.""",
    
    'final_cta': """👉 Check availability and claim your 50% discount before it's gone."""
}

# 图片Prompt模板
IMAGE_PROMPTS = {
    'hero_image': {
        'description': '首屏主图 - 中奖彩票特写',
        'prompt': """Photorealistic close-up of a winning lottery ticket on a wooden table, 
surrounded by golden light rays. A elegant obsidian bracelet with gold Pixiu charm 
placed next to the ticket. Warm, cinematic lighting. 
Style: High-quality product photography, professional, inspiring.""",
        'aspect_ratio': '16:9',
        'filename': 'hero-lottery-ticket.jpg'
    },
    
    'female_protagonist': {
        'description': '女主角Emma - 快乐的客服代表',
        'prompt': """Photorealistic portrait of a happy 35-year-old woman named Emma, 
professional customer service representative, sitting at home office desk, 
genuine smile, warm lighting, casual professional attire. 
Modern American home interior. Natural, authentic photo style.""",
        'aspect_ratio': '3:4',
        'filename': 'emma-portrait.jpg'
    },
    
    'female_before': {
        'description': '女主角转变前 - 疲惫工作',
        'prompt': """Cinematic photo of tired woman in her 30s at office cubicle, 
stressed expression, late evening, overhead fluorescent lighting, 
stack of paperwork, coffee cup. Muted colors, documentary style.""",
        'aspect_ratio': '16:9',
        'filename': 'emma-before-struggle.jpg'
    },
    
    'lottery_win_moment': {
        'description': '中奖时刻 - 震惊表情',
        'prompt': """Photorealistic image of woman in shock and disbelief, 
holding lottery ticket with trembling hands, tears of joy, 
emotional moment, warm indoor lighting. Cinematic, authentic emotion.""",
        'aspect_ratio': '4:3',
        'filename': 'lottery-win-moment.jpg'
    },
    
    'bracelet_product_1': {
        'description': '产品特写1 - 黑曜石手链',
        'prompt': """Ultra high quality product photography of black obsidian bracelet 
with golden Pixiu charm, placed on white marble surface, 
soft professional lighting, luxury product shot, 
intricate details visible, 8k resolution.""",
        'aspect_ratio': '1:1',
        'filename': 'bracelet-product-closeup-1.jpg'
    },
    
    'bracelet_product_2': {
        'description': '产品特写2 - 貔貅细节',
        'prompt': """Extreme close-up of golden Pixiu charm on obsidian bracelet, 
intricate Chinese mythological creature details, 
professional jewelry photography, black background, 
dramatic side lighting highlighting texture.""",
        'aspect_ratio': '1:1',
        'filename': 'bracelet-pixiu-detail.jpg'
    },
    
    'male_protagonist': {
        'description': '男主角James - 自信的商人',
        'prompt': """Professional portrait of confident 40-year-old businessman named James, 
wearing smart casual attire, genuine smile, modern office background, 
natural lighting, success and prosperity vibe. Authentic business portrait style.""",
        'aspect_ratio': '3:4',
        'filename': 'james-portrait.jpg'
    },
    
    'male_before': {
        'description': '男主角转变前 - 失意',
        'prompt': """Documentary style photo of man in his late 30s looking disappointed, 
sitting alone in dimly lit apartment, rain visible through window, 
melancholic atmosphere, realistic lighting.""",
        'aspect_ratio': '16:9',
        'filename': 'james-before-unlucky.jpg'
    },
    
    'male_transformation': {
        'description': '男主角转变后 - 签约场景',
        'prompt': """Cinematic photo of professional man shaking hands in modern office, 
signing business contract, confident posture, bright office lighting, 
success and opportunity theme.""",
        'aspect_ratio': '16:9',
        'filename': 'james-success-handshake.jpg'
    },
    
    'energy_concept': {
        'description': '能量概念图 - 光环和频率',
        'prompt': """Abstract visualization of human energy field and frequency waves, 
person silhouette surrounded by golden energy waves, 
sacred geometry patterns, cosmic background, 
mystical yet scientific aesthetic.""",
        'aspect_ratio': '16:9',
        'filename': 'energy-frequency-concept.jpg'
    },
    
    'feng_shui_ancient': {
        'description': '风水古代图 - 中国传统',
        'prompt': """Ancient Chinese feng shui diagram with mystical symbols, 
traditional ink painting style merged with gold accents, 
yin-yang elements, dragon and Pixiu illustrations, 
aged parchment texture, authentic historical feel.""",
        'aspect_ratio': '4:3',
        'filename': 'feng-shui-ancient-diagram.jpg'
    },
    
    'obsidian_stone': {
        'description': '黑曜石原石 - 自然纹理',
        'prompt': """Macro photography of raw volcanic obsidian stone, 
glossy black surface with natural patterns, 
dramatic lighting showing depth and texture, 
geology specimen photography style.""",
        'aspect_ratio': '1:1',
        'filename': 'obsidian-raw-stone.jpg'
    },
    
    'lifestyle_wearing': {
        'description': '生活场景 - 佩戴展示',
        'prompt': """Natural lifestyle photo of person's wrist wearing black obsidian bracelet, 
casual daily setting, reading book or working on laptop, 
soft natural window light, cozy and relatable atmosphere.""",
        'aspect_ratio': '4:3',
        'filename': 'lifestyle-wearing-bracelet.jpg'
    },
    
    'wealth_symbols': {
        'description': '财富象征 - 金币和宝石',
        'prompt': """Artistic composition of Chinese wealth symbols: 
gold coins, jade ornaments, Pixiu figurines, 
arranged on red silk fabric, cinematic golden lighting, 
luxury and prosperity theme.""",
        'aspect_ratio': '16:9',
        'filename': 'wealth-symbols-collection.jpg'
    },
    
    'packaging_gift': {
        'description': '包装礼盒 - 精美展示',
        'prompt': """Premium packaging photography of FengShui Bracelet in elegant gift box, 
luxury presentation with red and gold Chinese motifs, 
soft studio lighting, high-end product photography.""",
        'aspect_ratio': '1:1',
        'filename': 'packaging-gift-box.jpg'
    },
    
    'testimonial_montage': {
        'description': '用户评价蒙太奇 - 多人合影',
        'prompt': """Collage-style image of diverse happy people wearing bracelets, 
different ages and backgrounds, genuine smiles, 
various lifestyle settings, authentic customer photos aesthetic.""",
        'aspect_ratio': '16:9',
        'filename': 'testimonials-people-montage.jpg'
    },
    
    'urgency_timer': {
        'description': '紧迫感 - 限时图标',
        'prompt': """Dramatic close-up of countdown timer showing limited time, 
red and gold color scheme, sense of urgency, 
clean graphic design with Chinese cultural elements.""",
        'aspect_ratio': '4:3',
        'filename': 'urgency-limited-stock.jpg'
    },
    
    'guarantee_badge': {
        'description': '保证徽章 - 信任标识',
        'prompt': """Professional 3D render of golden guarantee badge with checkmark, 
'50% OFF' and 'Money Back Guarantee' text, 
premium metallic texture, trust and credibility design.""",
        'aspect_ratio': '1:1',
        'filename': 'guarantee-badge-50off.jpg'
    },
}

# 评论区人物头像Prompts
AVATAR_PROMPTS = [
    {
        'name': 'Patricia Green',
        'prompt': """Professional headshot of woman in her 40s, friendly smile, 
business casual attire, natural lighting, authentic social media profile photo style.""",
        'filename': 'avatar-patricia.jpg'
    },
    {
        'name': 'Rachel Turner',
        'prompt': """Casual portrait of woman in her 30s, warm expression, 
outdoor natural lighting, genuine candid photo style.""",
        'filename': 'avatar-rachel.jpg'
    },
    {
        'name': 'Gloria White',
        'prompt': """Portrait of elegant woman in her 50s, confident posture, 
professional headshot, studio lighting.""",
        'filename': 'avatar-gloria.jpg'
    },
    {
        'name': 'Tyler Brooks',
        'prompt': """Professional photo of man in his 30s, business attire, 
friendly approachable expression, corporate headshot style.""",
        'filename': 'avatar-tyler.jpg'
    },
    {
        'name': 'Nancy Fisher',
        'prompt': """Casual portrait of woman in her late 40s, reading glasses, 
warm smile, home office background.""",
        'filename': 'avatar-nancy.jpg'
    },
    {
        'name': 'Michael Tran',
        'prompt': """Professional headshot of Asian-American man in his 30s, 
confident smile, modern business setting.""",
        'filename': 'avatar-michael.jpg'
    },
    {
        'name': 'Karen Phillips',
        'prompt': """Portrait of woman in her 40s, casual professional style, 
natural daylight, authentic social media photo.""",
        'filename': 'avatar-karen.jpg'
    },
    {
        'name': 'Jessica Harper',
        'prompt': """Lifestyle photo of woman in her 30s, casual attire, 
bright natural lighting, genuine expression.""",
        'filename': 'avatar-jessica.jpg'
    },
    {
        'name': 'Evelyn Clark',
        'prompt': """Professional portrait of mature woman in her 60s, 
elegant appearance, studio photography.""",
        'filename': 'avatar-evelyn.jpg'
    },
    {
        'name': 'Matthew Parker',
        'prompt': """Headshot of man in his 40s, casual business attire, 
friendly professional appearance.""",
        'filename': 'avatar-matthew.jpg'
    },
    {
        'name': 'Helen Carter',
        'prompt': """Portrait of woman in her 50s, warm motherly expression, 
home setting, natural lighting.""",
        'filename': 'avatar-helen.jpg'
    },
    {
        'name': 'James Foster',
        'prompt': """Professional photo of man in his late 30s, smart casual style, 
confident yet approachable demeanor.""",
        'filename': 'avatar-james-foster.jpg'
    },
]

def save_all_prompts():
    """保存所有图片prompts到文件"""
    
    # 主要图片prompts
    main_prompts_file = PROMPTS_DIR / 'main-images-prompts.json'
    with open(main_prompts_file, 'w', encoding='utf-8') as f:
        json.dump(IMAGE_PROMPTS, f, ensure_ascii=False, indent=2)
    print(f"✅ 主要图片prompts已保存: {main_prompts_file}")
    
    # 头像prompts
    avatar_prompts_file = PROMPTS_DIR / 'avatar-prompts.json'
    with open(avatar_prompts_file, 'w', encoding='utf-8') as f:
        json.dump(AVATAR_PROMPTS, f, ensure_ascii=False, indent=2)
    print(f"✅ 头像prompts已保存: {avatar_prompts_file}")
    
    # 创建Markdown格式的prompts（方便阅读）
    md_lines = [" # FengShui Bracelet AI - 图片生成Prompts\n"]
    md_lines.append(f"生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_lines.append("---\n\n")
    
    md_lines.append("## 主要内容图片\n\n")
    for idx, (key, img) in enumerate(IMAGE_PROMPTS.items(), 1):
        md_lines.append(f"### {idx}. {img['description']}\n\n")
        md_lines.append(f"**文件名**: `{img['filename']}`  \n")
        md_lines.append(f"**宽高比**: {img['aspect_ratio']}  \n\n")
        md_lines.append(f"**Prompt**:\n```\n{img['prompt']}\n```\n\n")
        md_lines.append("---\n\n")
    
    md_lines.append("## 用户头像\n\n")
    for idx, avatar in enumerate(AVATAR_PROMPTS, 1):
        md_lines.append(f"### {idx}. {avatar['name']}\n\n")
        md_lines.append(f"**文件名**: `{avatar['filename']}`  \n\n")
        md_lines.append(f"**Prompt**:\n```\n{avatar['prompt']}\n```\n\n")
        md_lines.append("---\n\n")
    
    md_file = PROMPTS_DIR / 'ALL-PROMPTS.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(''.join(md_lines))
    print(f"✅ Markdown格式prompts已保存: {md_file}")

def generate_content():
    """生成网页文本内容"""
    
    content = {}
    
    # 替换人物名字
    for key, template in CONTENT_TEMPLATE.items():
        text = template.format(
            name=NEW_CHARACTERS['female_lead'],
            location=NEW_CHARACTERS['location_female'],
            male_name=NEW_CHARACTERS['male_lead'],
            male_location=NEW_CHARACTERS['location_male']
        )
        content[key] = text
    
    # 保存内容
    content_file = CONTENT_DIR / 'page-content.json'
    with open(content_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"✅ 页面内容已生成: {content_file}")
    
    # 生成Markdown预览
    md_lines = ["# FengShui Bracelet AI - 页面内容\n\n"]
    md_lines.append(f"**女主角**: {NEW_CHARACTERS['female_lead']} from {NEW_CHARACTERS['location_female']}\n")
    md_lines.append(f"**男主角**: {NEW_CHARACTERS['male_lead']} from {NEW_CHARACTERS['location_male']}\n\n")
    md_lines.append("---\n\n")
    
    for key, text in content.items():
        title = key.replace('_', ' ').title()
        md_lines.append(f"## {title}\n\n")
        md_lines.append(f"{text}\n\n")
        md_lines.append("---\n\n")
    
    md_file = CONTENT_DIR / 'page-content.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(''.join(md_lines))
    print(f"✅ 内容Markdown预览已保存: {md_file}")

def create_project_readme():
    """创建项目README"""
    
    readme_content = f"""# FengShui Bracelet AI版本 v2.0

基于原版网页，使用AI生成新版本落地页。

## 📁 项目结构

```
fengshui-bracelet-ai-v2/
├── prompts/                 # 所有AI图片生成prompts
│   ├── main-images-prompts.json
│   ├── avatar-prompts.json
│   └── ALL-PROMPTS.md      # 可读的Markdown格式
├── images/                  # 生成的图片（待生成）
├── content/                 # 页面文本内容
│   ├── page-content.json
│   └── page-content.md     # 可读预览
├── scripts/                 # 生成脚本
│   ├── 01_extract_original_structure.py
│   ├── 02_generate_content_and_prompts.py
│   └── 03_generate_images.py
├── analysis/                # 原网页分析结果
└── index.html              # 最终网页（待生成）
```

## 👥 新版人物角色

- **女主角**: {NEW_CHARACTERS['female_lead']} (原版: Lisa)
- **男主角**: {NEW_CHARACTERS['male_lead']} (原版: David)
- **地点**: {NEW_CHARACTERS['location_female']}, {NEW_CHARACTERS['location_male']}

## 📊 内容统计

- **主要图片**: {len(IMAGE_PROMPTS)} 张
- **用户头像**: {len(AVATAR_PROMPTS)} 个
- **内容模块**: {len(CONTENT_TEMPLATE)} 个

## 🚀 使用流程

### 步骤1: 生成内容和Prompts

```bash
cd scripts
python3 02_generate_content_and_prompts.py
```

### 步骤2: 生成AI图片

```bash
python3 03_generate_images.py
```

这将调用 StellarView 的图片生成服务（MiniMax），自动生成所有图片。

### 步骤3: 生成HTML网页

```bash
python3 04_generate_html.py
```

将内容和图片组合成最终的HTML文件。

## 🎨 图片生成说明

所有图片使用 **MiniMax Image Service** 生成：
- 宽高比根据位置优化（hero: 16:9, 产品: 1:1, 人物: 3:4）
- 高质量photorealistic风格
- 自动保存到 `images/` 目录

## 📝 内容特点

完全复制原网页的：
- ✅ 故事结构（两个主角的转变故事）
- ✅ 情感节奏（痛点→希望→证明→行动）
- ✅ 说服技巧（社会证明、稀缺性、权威性）
- ✅ CTA位置和文案

仅修改：
- 人物名字
- 地理位置

## 🔗 原版参考

原网页: https://offer.fengshuibracelets.co/fengshui/news

分析文档: `../fengshui-bracelet-case/analysis/marketing-analysis.md`

---

*生成日期: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    readme_file = PROJECT_ROOT / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ 项目README已创建: {readme_file}")

def main():
    print("🚀 开始生成FengShui Bracelet AI版本...\n")
    
    # 1. 保存所有prompts
    print("📝 步骤1: 生成图片Prompts...")
    save_all_prompts()
    print()
    
    # 2. 生成页面内容
    print("✍️ 步骤2: 生成页面文本内容...")
    generate_content()
    print()
    
    # 3. 创建项目README
    print("📄 步骤3: 创建项目文档...")
    create_project_readme()
    print()
    
    print("=" * 60)
    print("✅ 内容和Prompts生成完成！")
    print("=" * 60)
    print(f"\n📂 输出位置: {PROJECT_ROOT}")
    print(f"\n📋 下一步:")
    print(f"   1. 查看 {PROMPTS_DIR}/ALL-PROMPTS.md 确认所有图片prompts")
    print(f"   2. 查看 {CONTENT_DIR}/page-content.md 预览页面内容")
    print(f"   3. 运行 03_generate_images.py 开始生成AI图片")
    print()

if __name__ == '__main__':
    sys.exit(main())
