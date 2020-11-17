import reptilePY.search_baidu as search_baidu

def getImg(method, user_name, word, image_number, index=0):
    url = []
    dowl_url = 'static/images/' + user_name

    switch = {
        "百度图片": search_baidu.getImg
    }
    switch[method](dowl_url, word, image_number, index)

    image_number +=index
    while index < image_number:
        url.append('/' + dowl_url + '/' + word + '/' + str(index) + '.jpg')
        index += 1
    return url