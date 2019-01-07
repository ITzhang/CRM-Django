from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random


def get_valid_img():
    # 随机颜色
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 创建画布
    img = Image.new("RGB", (130, 38), (255, 255, 255))
    # 创建画笔
    draw = ImageDraw.Draw(img)
    # 设置所使用的字体
    font = ImageFont.truetype("static/fonts/kumo.ttf", 36)

    # 保存验证码对应的字符
    code_str = ""

    # 开始绘画
    for i in range(4):
        # 随机数字
        random_num = str(random.randint(0, 9))
        # 随机小写字母
        random_lowalf = chr(random.randint(97, 122))
        # 随机大写字母
        random_upperalf = chr(random.randint(65, 90))
        # 4个随你字符中选取一个
        random_char = random.choice([random_num, random_lowalf, random_upperalf])
        # 参数说明： 1.字符位于画布中的坐标，画布左上角为0,0   2.字符   3.设置画布背景颜色   4.字符所使用字体
        draw.text((i * 30 + 5, 0), random_char, get_random_color(), font=font)
        code_str += random_char

    # 随机线条
    width = 130
    height = 38
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # 随机噪点
    for i in range(50):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 创建内存对象
    f = BytesIO()
    # 将生成的验证码图片保存到内存对象中
    img.save(f, "png")

    # 获取到这个内存对象
    data = f.getvalue()

    # 返回内存对象，和验证码对应的字符串
    return data, code_str
