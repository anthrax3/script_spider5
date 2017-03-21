# -*- coding:utf-8 -*-
from io import BytesIO
import lxml.html
from download import download_agent as D

# 一个包含处理验证码图像的高级方法的库
# 安装方法： pip install Pillow
from PIL import Image


def get_captcha(html):
	# 建立lxml的抓取树
	tree = lxml.html.fromstring(html)

	# 抓取存储验证码图像的html部分，这里是recaptcha
	img_data = tree.cssselect('div#recaptcha img')[0].get('src')

	# 存储图像的码中前缀定义了数据类型，这里是消除前缀
	img_data = img_data.partition(',')[-1]

	# 使用Base64解码图像数据，回到最初的二进制格式
	binary_img_data = img_data.decode('base64')

	# 要想加载图像，PIL需要一个类似文件的接口，所以使用BytesIO对图像进行封装
	file_like = BytesIO(binary_img_data)

	# 得到img
	img = Image.open(file_like)
	return img

URL = 'http://example.webscraping.com/user/register'

# 光学字符识别(Optical Character Recognition)
# 用于从图像中抽取文本，这里使用的是开源的Tesseract OCR引擎
# 安装方法 pip install pytesseract
import pytesseract
def get_str(html):
	img = get_captcha(html)

	# 保存原始图像
	#img.save('captcha_original.png')

	# 验证文本一般都是黑色，背景则会更加明亮，所以我们可以通过
	# 检查像素是否为黑色将文本分离出来，该处理过程又称为阀值化

	# 改变色调，变为灰色并保存
	gray = img.convert('L')
	#gray.save('captcha_gray.png')

	# 阀值化去除背景颜色，并保存图像
	bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
	#bw.save('captcha_thresholded.png')
	strr = pytesseract.image_to_string(bw)
	return strr

if __name__ == '__main__':
	html = D(URL)
	result = get_str(html)
	print result