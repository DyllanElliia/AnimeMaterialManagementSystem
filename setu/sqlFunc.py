def sqlRun(sqlProgram):
    import psycopg2
    import sys

    con = None
    data = ""
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        data = cur.fetchall()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return data


def sqlRunCommit(sqlProgram):
    import psycopg2
    import sys

    con = None
    data = ""
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        data = cur.fetchall()
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return data


def sqlRunUpdate(sqlProgram):
    import psycopg2
    import sys

    con = None
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()


def getFileData(filePath):
    f = open(filePath, "r", encoding="utf-8")
    sqlProgram = f.read()
    f.close()
    return sqlProgram


def getPictureName(address):
    sqlProgram = getFileData("./sql_file/Get_Picture_name.sql")
    sqlProgram = sqlProgram.replace("@@linkAddress@@", address)
    data = sqlRun(sqlProgram)
    print(data)
    return data[0][0]


def getAllAddress(userName, folderName):
    sqlProgram = getFileData("./sql_file/get_link_address_all.sql")
    sqlProgram = sqlProgram.replace("@@userName", userName)
    sqlProgram = sqlProgram.replace("@@folderName", folderName)
    data = sqlRun(sqlProgram)
    # print(data)
    # addressNumber = len(data)
    addressList = [address[0] for address in data]
    return addressList


def getUserTimes(userName):
    sqlProgram = getFileData("./sql_file/get_times.sql")
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    data = sqlRun(sqlProgram)
    return data[0][0]


def updateUserTimes(userName):
    times = getUserTimes(userName)
    sqlProgram = getFileData("./sql_file/update_times.sql")
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    sqlProgram = sqlProgram.replace("@@times@@", str(times + 1))
    data = sqlRunUpdate(sqlProgram)


def getMaxIndex(user_name, keyword):

    f = open("./sql_file/Count_Folder_LinkNum.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@userName@@", user_name)
    sqlProgram = sqlProgram.replace("@@keyword@@", keyword)
    f.close()

    import psycopg2
    import sys

    con = None
    index = ""
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        index_ = cur.fetchall()
        print(len(index_))
        if len(index_) == 0:
            index = "0"
        else:
            index = index_[0][0]
            print(index)
            if index == None:
                print("1")
                return 0
            link_index = user_name + "/" + keyword + "/"
            index = index[index.find(link_index) + len(link_index) : index.find(".jpg")]
            print("f: " + index)
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return int(index) + 1


def saveLink(linkAddress, user_name, keyword):
    link_ = user_name + "/" + keyword + "/"
    link_name = linkAddress[
        linkAddress.find(link_) + len(link_) : linkAddress.find(".jpg")
    ]

    f = open("./sql_file/Save_Link.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@userName@@", user_name)
    sqlProgram = sqlProgram.replace("@@keyword@@", keyword)
    sqlProgram = sqlProgram.replace("@@linkAddress@@", linkAddress)
    sqlProgram = sqlProgram.replace("@@linkName@@", link_name)
    f.close()
    print("here: " + sqlProgram)
    import psycopg2
    import sys

    con = None
    index = ""
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        index = cur.fetchall()
        cur.connection.commit()
        if int(index[0][0]) == 2:
            print("Add folder ./" + user_name + "/" + keyword + " false!")
            return False
        if int(index[0][0]) == 2:
            print("We have link: " + linkAddress)
            return False
        return True
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()


def changeLinkName(userName, folderName, linkName_old, linkName_new):
    f = open("./sql_file/change_link_name.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    sqlProgram = sqlProgram.replace("@@keyword@@", folderName)
    sqlProgram = sqlProgram.replace("@@linkName_old@@", linkName_old)
    sqlProgram = sqlProgram.replace("@@linkName_new@@", linkName_new)
    f.close()
    print(sqlProgram)
    import psycopg2
    import sys

    con = None
    result = False
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        result = cur.fetchall()
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return result


def getAddressANDId(userName, folderName, linkName):
    f = open("./sql_file/get_link_address.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    sqlProgram = sqlProgram.replace("@@folderName@@", folderName)
    sqlProgram = sqlProgram.replace("@@linkName@@", linkName)
    f.close()
    # print(sqlProgram)
    import psycopg2
    import sys

    con = None
    linkId = -1
    address = ""
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        data = cur.fetchall()
        # print(data)
        linkId = data[0][0]
        address = data[0][1]
        # print(linkId)
        # print(address)
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return address, linkId


def getAddress(userName, folderName, linkName):
    address, linkId = getAddressANDId(userName, folderName, linkName)
    return address


# changeFolderName('321','110','7','110_')
def changeFolderName(userName, folderName_old, linkName, folderName_new):
    changeLinkName(userName, folderName_old, linkName, linkName + "_" + folderName_old)
    linkName = linkName + "_" + folderName_old
    print(linkName)
    address = getAddress(userName, folderName_old, linkName)
    if address == "":
        print("wrong address")
        return False
    index = address.find(folderName_old)
    address_new = (
        address[0:index]
        + folderName_new
        + "/"
        + str(getMaxIndex(userName, folderName_new))
        + ".jpg"
    )
    f = open("./sql_file/change_folder_name.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@address@@", address)
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    sqlProgram = sqlProgram.replace("@@addressNew@@", address_new)
    sqlProgram = sqlProgram.replace("@@folderNameNew@@", folderName_new)
    f.close()
    print(sqlProgram)
    import psycopg2
    import sys

    con = None
    result = False
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        data = cur.fetchall()
        result = data[0][0]
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    if result == True:
        address = "." + address
        dirs = (
            "." + address_new[: address_new.find(folderName_new) + len(folderName_new)]
        )
        address_new = "." + address_new
        import os

        if not os.path.exists(dirs):
            os.makedirs(dirs)
        os.rename(address, address_new)
    return result


def deleteLink(userName, folderName, linkName):
    address, linkId = getAddressANDId(userName, folderName, linkName)
    f = open("./sql_file/delete_link.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@linkId@@", str(linkId))
    f.close()
    import psycopg2
    import sys

    con = None
    result = True
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        # result = cur.fetchall()
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    if result == True:
        address = "." + address
        import os

        os.remove(address)
    return result


def deleteFolder(userName, folderName):
    # address, linkId = getAddressANDId(userName, folderName, linkId)
    f = open("./sql_file/delete_folder.sql", "r", encoding="utf-8")
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    sqlProgram = sqlProgram.replace("@@folderName@@", folderName)
    f.close()
    import psycopg2
    import sys

    con = None
    result = False
    try:
        con = psycopg2.connect(database="setu", user="postgres", password="123456")
        cur = con.cursor()
        cur.execute(sqlProgram)
        result = cur.fetchall()
        cur.connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        if con:
            con.close()
    if result == True:
        # address = './static/'+userName+'/'+folderName
        # Python简单删除目录下文件以及文件夹
        import os
        import shutil

        filelist = []
        rootdir = "./static/" + userName + "/" + folderName  # 选取删除文件夹的路径,最终结果删除img文件夹
        filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
        for f in filelist:
            filepath = os.path.join(rootdir, f)  # 将文件名映射成绝对路劲
            if os.path.isfile(filepath):  # 判断该文件是否为文件或者文件夹
                os.remove(filepath)  # 若为文件，则直接删除
                print(str(filepath) + " removed!")
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
                print("dir " + str(filepath) + " removed!")
        shutil.rmtree(rootdir, True)  # 最后删除img总文件夹
        print("删除" + rootdir + "成功")
    return result


def getRandomFolder(userName):
    sqlProgram = getFileData("./sql_file/get_newest_folder.sql")
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    data = sqlRun(sqlProgram)
    return data[0][0]


def getAllFolderName(userName):
    sqlProgram = getFileData("./sql_file/get_all_folderName.sql")
    sqlProgram = sqlProgram.replace("@@userName@@", userName)
    data = sqlRun(sqlProgram)
    FolderList = [Folder[0] for Folder in data]
    return FolderList

