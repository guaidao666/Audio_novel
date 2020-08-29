"""
update:
        0.每次运行不会覆盖之前的文件
        1.可下载多个章节、音频
        2.自动建立音频文件夹
        3.自动保存txt格式小说


readme1:
    1. 只能下载《逃婚奇侠传》
    2. 也可运行前修改 initial_character(开始章节) 和 final_character(最后章节)参数，修改章节范围
    3. 小说文件(.txt)会保存在同目录下的 character文件夹中

readme2:
    1. 转换的语音会保存在同目录下的 audio2/audio+数字 文件夹中
    2. result可调节语音合成参数
    3. 合成后可使用 格式工厂 软件将多个音频合并成一个音频
    
"""

from aip import AipSpeech
# 调用本地文件会报错，无须理会
import account
import requests
import os
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
    # 下载的章节号
    # 开始章节
    initial_character = int(input('请输入开始章节'))
    # 最后章节
    final_character = int(input('请输入最后章节'))
    # 用户下载的章节数74-77
    detail_link_list = []
    # 章节序号范围
    nums = range(initial_character, final_character + 1)
    # print(nums)
    for num in range(initial_character, final_character + 1):
        # 详情页链接
        detail_link = 'http://www.maxreader.net' + href[num]
        detail_link_list.append(detail_link)

        # print(detail_link)
        # print(detail_links)

        # detail_links为所有详情页链接，detail_link_list为用户所输入的章节详情页链接
    # print(detail_link_list)
    return detail_links, detail_link_list, nums


# 定义函数————获取小说内容
def get_novel(detail_links, detail_link_list, nums):
    # 存放多个章节内容的列表
    characters = []
    for detail_link, num in zip(detail_link_list, nums):
        # print(detail_link)
        # print(num)
        # print('=' * 100)

        response = requests.get(url=detail_link, headers=HEADERS)
        response.encoding = 'utf-8'
        # print(response.text)
        # 章节序号
        # 标题
        title = re.findall(r'<h1\sclass="lh100 size26 mb20">.*?<a.*?>(.*?)</a>', response.text, re.S)[0]

        # 第一页内容
        content = \
        re.findall(r'<div\sclass="size16 color5 pt-read-text".*?>.*?(<p>.*</p>).*?</div>', response.text, re.S)[0]
        content = re.sub('<p>', '    ', content)
        content = re.sub('</p>', '\n', content)

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
        content2 = \
        re.findall(r'<div\sclass="size16 color5 pt-read-text".*?>.*?(<p>.*</p>).*?</div>', response2.text, re.S)[
            0]
        content2 = re.sub('<p>', '    ', content2)
        content2 = re.sub('</p>', '\n', content2)

        character = {
            'num': num,
            'title': title + '  第1页/共2页',
            'content': content,
            'title2': title2 + '  第2页/共2页',
            'content2': content2

        }

        characters.append(character)

        # print(title)
        # print(content)
        # print(title2)
        # print(content2)

    # print(characters)
    return characters


# 定义函数————保存小说
def save_novel(characters):
    # 文件名称
    # 创建一个novel文件夹
    if not os.path.exists('character'):
        os.mkdir('character')
    else:
        # print('character已存在')
        pass

    # 名字列表
    names = []
    for novel in characters:
        name = novel['title'].split()[0] + ' 第%s章 ' % novel['num'] + novel['title'].split()[2]
        # print(name)
        with open('character/%s.txt' % name, 'w', encoding='utf-8') as file:
            file.write(novel['title'])
            file.write('\n\n\n\n')
            file.write(novel['content'])
            file.write('\n\n\n\n')
            file.write(novel['title2'])
            file.write('\n\n\n\n')
            file.write(novel['content2'])
            file.write('\n\n\n\n')
            print('%s保存成功' % name)
            print('=' * 100)
        names.append(name + '.txt')
    return names


# 定义函数————语音合成
def audio(names, characters):
    for content0, character in zip(names, characters):
        print(content0)
        content = 'character/' + content0
        num = character['num']
        # print(content)
        # print(num)


        # 创建一个novel文件夹
        if not os.path.exists('audio2/audio%s' % num):
            os.makedirs('audio2/audio%s' % num)
        else:
            # print('audio%s已存在' % num)
            pass


        """ 你的 APPID AK SK """
        APP_ID = account.APP_ID
        API_KEY = account.API_KEY
        SECRET_KEY = account.SECRET_KEY

        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

        # 将要转换的文字或文件传给content

        with open('%s' % content, 'r', encoding='utf-8') as file:
            number = 0
            while True:
                number += 1



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
                    with open('audio2/audio{x}/auido{y}.mp3'.format(x=num, y=number), 'wb') as f:
                        f.write(result)
                        print('正在生成第{y}段语音......'.format(y=number))
        print('=' * 100)



# 主函数
def main():
    detail_links, detail_link_list, nums = get_details_link()
    characters = get_novel(detail_links, detail_link_list, nums)
    names = save_novel(characters)
    audio(names, characters)


if __name__ == '__main__':
    main()
