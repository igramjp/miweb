import argparse
import re
import sys
from html import unescape
from urllib.request import urlopen

parser = argparse.ArgumentParser(
        prog = 'miweb',
        usage = 'python miweb.pyc [OPTION]',
        description = 'get current promotions at media integration, and output csv.',
        epilog = '',
        add_help = True)
 
# 引数の追加
parser.add_argument('-v', '--version', help='show this version information and exit', action='store_const', const=True, default=False)
parser.add_argument('-t', '--template', help='convert template html tags for online store', action='store_const', const=True, default=False)
 
# 引数を解析する
args = parser.parse_args()
 
if args.version:
    print('miweb.pyc 0.1.0 (2019-05-20)')
else:
    f = urlopen('https://www.minet.jp/?s-type=promotion&s=&costom-search=on')
    encoding = f.info().get_content_charset(failobj="utf-8")
    html = f.read().decode(encoding)

    ret = ''
    for idx, partial_html in enumerate(re.findall(r'<section>.*?<div class="searchPage__posts-item">.*?</div>.*?</section>', html, re.DOTALL)):
        url = re.search(r'<h3 class="searchPage__posts-item-data-title"><a href="(.*?)"', partial_html).group(1)
        img = re.search(r'<img src="(.*?)"', partial_html).group(1)
        cat = re.search(r'<span class="item-data-category-promotion">(.*?)</span>', partial_html).group(1)
        ttl = re.search(r'<h3 class="searchPage__posts-item-data-title"><a href="'+url+'">(.*?)</a></h3>', partial_html).group(1).strip()
        dsc = re.search(r'<div class="searchPage__posts-item-data-excerpt"><a href="'+url+'">(.*?)</a></div>', partial_html).group(1).strip()

        if args.template:
            ret += '<div class="feature-list">\n'
            ret += '  <div class="feature-image" style="background-image: url('+img+');"></div>\n'
            ret += '  <div class="feature-info">\n'
            ret += '    <div class="feature-title">\n'
            ret += '      <h1>'+ttl+'</h1>\n'
            ret += '    </div>\n'
            ret += '    <a href="/category/[PLEASE INSERT CATEGORY CODE]/">\n'
            ret += '      <button class="feature-button">詳しく見る</button>\n'
            ret += '    </a>\n'
            ret += '    <div class="feature-date">\n'
            ret += '      <img class="icon_date" src="images/icon_date.svg">\n'
            ret += '      <p>〜yyyy年mm月dd日（曜日）まで</p>\n'
            ret += '    </div>\n'
            ret += '    <div class="feature-category-list">\n'
            ret += '      <div class="feature-category bg-purple">'+cat+'</div>\n'
            ret += '    </div>\n'
            ret += '  </div>\n'
            ret += '</div>\n'
            ret += '\n'
        else:
            if idx == 0:
                ret += 'Category,Title,Description,Contents URL,Image URL\n'
                
            ret += ('"'+cat+'","'+ttl+'","'+dsc+'","'+url+'","'+img+'"\n')

    print(ret)

