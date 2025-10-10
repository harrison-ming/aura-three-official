#!/usr/bin/env python3
import os
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

class AssetParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.assets = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # 图片
        if tag == 'img' and 'src' in attrs_dict:
            self.assets.append(('images', attrs_dict['src']))
        
        # CSS
        elif tag == 'link' and attrs_dict.get('rel') == 'stylesheet' and 'href' in attrs_dict:
            self.assets.append(('css', attrs_dict['href']))
        
        # JavaScript
        elif tag == 'script' and 'src' in attrs_dict:
            self.assets.append(('js', attrs_dict['src']))
        
        # 背景图片等
        if 'style' in attrs_dict:
            style = attrs_dict['style']
            urls = re.findall(r'url\([\'"]?([^\'"()]+)[\'"]?\)', style)
            for url in urls:
                self.assets.append(('images', url))

def download_file(url, filepath):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)
            print(f"✓ Downloaded: {url}")
            return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def main():
    base_dir = Path('/Users/ming/Documents/HUGO/aura-three-official/reference-pages')
    html_file = base_dir / 'index.html'
    base_url = 'https://offer.fengshuibracelets.co'
    
    # 读取 HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析资源
    parser = AssetParser(base_url)
    parser.feed(html_content)
    
    print(f"Found {len(parser.assets)} assets to download\n")
    
    # 下载资源
    downloaded = 0
    for asset_type, url in parser.assets:
        # 转换相对 URL 为绝对 URL
        if url.startswith('//'):
            full_url = 'https:' + url
        elif url.startswith('/'):
            full_url = base_url + url
        elif url.startswith('http'):
            full_url = url
        else:
            full_url = urllib.parse.urljoin(base_url + '/fengshui/news', url)
        
        # 生成本地文件路径
        parsed = urllib.parse.urlparse(full_url)
        local_path = base_dir / asset_type / parsed.path.lstrip('/')
        
        # 下载
        if download_file(full_url, str(local_path)):
            downloaded += 1
    
    print(f"\n✓ Download complete! {downloaded}/{len(parser.assets)} files downloaded")
    print(f"Files saved to: {base_dir}")

if __name__ == '__main__':
    main()
