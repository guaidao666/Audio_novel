"""
readme:
    1. 只能下载《逃婚奇侠传》
    2. 运行后输入章节数
    3. 小说文件会保存在同目录下的 逃婚奇侠传.txt 文件中
    4. 每次运行会覆盖之前的内容，如果需要附加内容（不覆盖），请将第102行中open函数中 w 改为 a



"""
"""
readme:
    0. 每次运行会覆盖之前的文件，如有需要，请先保存之前的文件
    1. 将要转换的文字或文件(.txt)传给content
    2. 转换的语音会保存在同目录下的 audio1/audio73 文件夹中，注：如果没有请先新建文件夹,若要存储到别的文件夹，请修改参数
    3. result可调节语音合成参数
    4. 合成后可使用 格式工厂 软件将多个音频合并成一个音频
    
    
"""


from aip import AipSpeech
# 调用本地文件会报错，无须理会
import account
import requests

import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}


# 定义函数————获取详情页链接
def get_details_link():
    # 获取数据

    url = 'http://www.maxreader.net/read/TaoHunQiXiaChuan/'
    response = requests.get(url=url, headers=HEADERS)
    response.encoding = 'utf-8'
    # print(response.text)
    # 解析数据
    # 提取数据
    # 小说部分链接http://www.maxreader.net/novel/TaoHunQiXiaChuan/read_1.html
    href = re.findall(r'<li>.*?<a\shref="(.*?)".*?</a>', response.text, re.S)[26:]
    # print(href)
    # 所有详情链接列表
    detail_links = []
    for x in href:
        detail_link1 = 'http://www.maxreader.net' + x
        detail_links.append(detail_link1)
    # 用户输入下载的章节号
    character = int(input('请输入想下载的章节编号'))
    # 详情页链接
    detail_link = 'http://www.maxreader.net' + href[character]

    # print(detail_link)
    # print(detail_links)

    # detail_links为所有详情页链接，detail_link为用户所输入的章节详情页链接

    return detail_links, detail_link

# 定义函数————获取小说内容
def get_novel(detail_links, detail_link):
    # 存放标题和内容的字典

    response = requests.get(url=detail_link, headers=HEADERS)
    response.encoding = 'utf-8'
    # print(response.text)
    # 标题
    title = re.findall(r'<h1\sclass="lh100 size26 mb20">.*?<a.*?>(.*?)</a>', response.text, re.S)[0]

    # 第一页内容
    content = re.findall(r'<div\sclass="size16 color5 pt-read-text".*?>.*?(<p>.*</p>).*?</div>', response.text, re.S)[0]
    content = re.sub('<p>', '    ', content)
    content = re.sub('</p>', '\n', content)
    print(title)
    print(content)

    # 第二页内容链接
    content2_link0 = re.findall(r'<a\sclass="pt-nextchapter"\shref="(.*?)"', response.text, re.S)[0]
    # print(content2_link0)
    content2_link = 'http://www.maxreader.net' + content2_link0

    response2 = requests.get(url=content2_link, headers=HEADERS)
    response2.encoding = 'utf-8'
    # print(response.text)
    # 标题
    title2 = re.findall(r'<h1\sclass="lh100 size26 mb20">.*?<a.*?>(.*?)</a>', response2.text, re.S)[0]
    # print(title)
    # 第二页内容
    content2 = re.findall(r'<div\sclass="size16 color5 pt-read-text".*?>.*?(<p>.*</p>).*?</div>', response2.text, re.S)[
        0]
    content2 = re.sub('<p>', '    ', content2)
    content2 = re.sub('</p>', '\n', content2)
    print(title2)
    print(content2)

    novel = {
        'title': title + '  第1页/共2页',
        'content': content,
        'title2': title2 + '  第2页/共2页',
        'content2': content2
    }
    # print(novel)
    # print(novel)
    return novel

# 定义函数————保存小说
def save_novel(novel):
    # 文件名称
    name = novel['title'].split(' ')[0]
    # print(name)
    with open('%s.txt' % name, 'w', encoding='utf-8') as file:
        file.write(novel['title'])
        file.write('\n\n\n\n')
        file.write(novel['content'])
        file.write('\n\n\n\n')
        file.write(novel['title2'])
        file.write('\n\n\n\n')
        file.write(novel['content2'])
        file.write('\n\n\n\n')
        print('保存成功')
        print('=' * 100)


# 定义函数————语音合成
def audio():
    content = '逃婚奇侠传.txt'

    """ 你的 APPID AK SK """
    APP_ID = account.APP_ID
    API_KEY = account.API_KEY
    SECRET_KEY = account.SECRET_KEY

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 将要转换的文字或文件传给content

    with open('%s' % content, 'r', encoding='utf-8') as file:
        num = 0
        while True:
            num += 1
            text = file.read(1023)
            if not text:
                break
            # print(text)
            # print('=' * 50)

            result = client.synthesis(text, 'zh', 1, {
                'vol': 10,  # 音量，取值0-15，默认为5中音量
                'spd': 4,  # 语速，取值0-9，默认为5中语速
                'pit': 5,  # 音调，取值0-9，默认为5中语调
                'per': 4  # 发音人选择：0为女声，1为男声，3为情感合成-度逍遥，
                #           4为情感合成-度丫丫，默认为普通女
                # 短时间只能合成5次
            })

            # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
            if not isinstance(result, dict):
                with open('audio1/audio73/auido{}.mp3'.format(num), 'wb') as f:
                    f.write(result)
                    print('正在生成第{}段语音......'.format(num))

# 主函数
def main():
    detail_links, detail_link = get_details_link()
    novel = get_novel(detail_links, detail_link)
    save_novel(novel)
    audio()


if __name__ == '__main__':
    main()
