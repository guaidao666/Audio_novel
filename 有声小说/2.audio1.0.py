"""
readme:
    0. 每次运行会覆盖之前的文件，如有需要，请先保存之前的文件
    1. 将要转换的文字或文件(.txt)传给content，以目录下的  逃婚奇侠传.txt  为例
    2. 转换的语音会保存在同目录下的audio0文件夹中
    3. result可调节语音合成参数



"""


from aip import AipSpeech
# 调用本地文件会报错，无须理会
import account


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
                with open('audio0/auido{}.mp3'.format(num), 'wb') as f:
                    f.write(result)
                    print('正在生成第{}段语音......'.format(num))


def main():
    audio()


if __name__ == '__main__':
    main()
