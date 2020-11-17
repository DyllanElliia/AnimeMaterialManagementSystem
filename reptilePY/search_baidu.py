#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: loveNight


import itertools
import urllib
import requests
import os
import re


str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')


def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=1)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True

def mkDir(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    return dirName
#检查路径是否存在 不存在则创建路径


# index here
def getImg(dowl_url,word,image_number,index=0):

    dirpath = mkDir(dowl_url)
    dirpath = mkDir(dirpath+'/'+word)

    urls = buildUrls(word)
    # here
    image_number += index
    begin = index
    for url in urls:
        print("正在请求：", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % (index-begin))

                if index >= image_number:
                    break

        if index >= image_number:
            break

if __name__ == '__main__':
    #for example
    dowl_url=input('请输入下载路径：(请用/代替\)')
    word= input('请输入爬取关键字：')
    image_number=int(input('请输入爬取数量：'))
    getImg(dowl_url,word,image_number,10)