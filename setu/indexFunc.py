from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect


def index(request):
    if request.GET.get("USER"):
        return render(
            request, "index.html", {"USER_NAME": str(request.GET.get("USER"))}
        )
    else:
        return HttpResponse("Wrong USER!!!")


def index_onlineMag(request):
    context = {}
    context["USER_NAME"] = "" + request.GET.get("USER")
    url = request.GET.get("PIC_SRC")
    context["PIC_SRC"] = url
    from setu.sqlFunc import getUserTimes, getPictureName

    context["RENEW"] = getUserTimes(request.GET.get("USER"))
    context["PIC_NAME"] = getPictureName(url[url.find("/static") :])
    return render(request, "index_onlineMag.html", context)


def index_search(request):
    if request.method == "POST":
        keyWord = request.POST.get("KEYWORD")
        serN = request.POST.get("SerN")
        imageNum = int(request.POST.get("NUM"))
        print(keyWord)
        print(serN)
        print(imageNum)
        userName = request.GET.get("USER")

        import reptilePY.reptilePY as rep
        from setu.sqlFunc import getMaxIndex, saveLink

        imgIndex = getMaxIndex(userName, keyWord)
        url = rep.getImg(serN, request.GET.get("USER"), keyWord, imageNum, imgIndex)
        for u in url:
            print(u)
            saveLink(u, userName, keyWord)
        # rResult = '爬取成功！已爬取了%d张图，保存在标签为%s。'%(imageNum,keyWord)
        return render(
            request,
            "index_search.html",
            {
                "USER_NAME": str(request.GET.get("USER")),
                "reptileResult": "爬取成功！已爬取了%d张图，保存在标签为%s。" % (imageNum, keyWord),
            },
        )
    # print(request)
    if request.GET.get("USER"):
        return render(
            request, "index_search.html", {"USER_NAME": str(request.GET.get("USER"))}
        )
    else:
        return HttpResponse("Wrong USER!!!")


# save_asdf = 10


def index_dowload(request):
    if request.method == "POST":
        # print('post!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # print(request.POST)
        action = request.POST.get("action")
        content = request.POST.get("content")
        print(action)
        print(content)
        # print(type(content))
        # print(str(content).split('::'))
        urls = list(filter(None, str(content).split("::")))
        headData = urls[0]
        del urls[0]
        print(action)
        print(urls)
        for data in urls:
            name = data[
                data.find("/static/images/")
                + len("/static/images/") : data.find("?temp")
            ]
            name = name[: name.find("/")]
            folderName = data[
                data.find("/static/images/" + name + "/")
                + len("/static/images/" + name + "/") : data.find("?temp")
            ]
            folderName = folderName[: folderName.find("/")]
            from setu.sqlFunc import getPictureName

            linkName = getPictureName(
                data[data.find("/static/images/") : data.find("?temp")]
            )
            print(folderName)
            print("here" + linkName)
            if action == "delete":
                from setu.sqlFunc import deleteLink, updateUserTimes

                updateUserTimes(name)
                deleteLink(name, folderName, linkName)
                continue
            if action == "changeTag":
                from setu.sqlFunc import changeFolderName, updateUserTimes

                updateUserTimes(name)
                changeFolderName(name, folderName, linkName, headData)
                continue
            if action == "changeName":
                from setu.sqlFunc import (
                    changeLinkName,
                    changeFolderName,
                    updateUserTimes,
                )

                updateUserTimes(name)
                # print("here")
                changeLinkName(name, folderName, linkName, headData)
                changeFolderName(name, folderName, headData, folderName)
                continue
            if action == "changePic":
                return

    if request.method == "GET":
        if request.GET.get("USER"):
            userName = str(request.GET.get("USER"))
            from setu.sqlFunc import getAllAddress
            from setu.sqlFunc import getAllFolderName

            # mode = "asdf"
            folderName = ""
            if request.GET.get("TAG"):
                folderName = request.GET.get("TAG")
            else:
                from setu.sqlFunc import getRandomFolder

                folderName = getRandomFolder(userName)

            # if str(request.GET.get('USER')) == "asdf":
            # if mode == "asdf":
            #     folderName = '吴亦凡'
            context = {}
            context["USER_NAME"] = userName
            context["src_list"] = getAllAddress(userName, folderName)
            context["tag_list"] = getAllFolderName(userName)
            context["NUM_TOTAL"] = len(context["src_list"])
            from setu.sqlFunc import getUserTimes

            context["RENEW"] = getUserTimes(userName)
            return render(request, "index_dowload.html", context)
        else:
            return HttpResponse("Wrong USER!!!")
