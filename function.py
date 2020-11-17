from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect

from setu.indexFunc import *

def pathNULL(request):
    return redirect('/login')

def login(request):
    if request.method == "GET":
        # print('t: '+str(request.GET.get('result')))
        if request.GET.get('result'):
            return render(request,'New_login.html',{"state":str(request.GET.get('result'))})
        return render(request,'New_login.html')

    if request.method == "POST":
        # print('t: '+str(request.GET.get('result')))
        User = request.POST.get('USER')
        Upwd = request.POST.get('PWD')
        # print('U: '+User)
        # print('P: '+Upwd)
        f = open('./sql_file/Login_Get_Password.sql','r',encoding='utf-8')
        sqlProgram = f.read()
        sqlProgram = sqlProgram.replace('@@userName@@',User)
        f.close()

        import psycopg2
        import sys

        con = None
        try:
            con = psycopg2.connect(database='setu', user='postgres',password='123456')
            cur = con.cursor()
            cur.execute(sqlProgram)
            sqlRetPWD = cur.fetchall()
            # print(sqlRetPWD[0][0])
            if sqlRetPWD[0][0] == Upwd:
                # state_str='哥哥我进♂去了！'
                # return render(request,'New_login.html',{"state":state_str})
                newURL = '/index?USER=%s'%(User)
                return redirect(newURL)
        except psycopg2.DatabaseError as e:
            print(f'Error {e}')
            sys.exit(1)
        finally:
            if con:
                con.close()

    state_str='用户名或者密码有误(⊙︿⊙)'
    return render(request,'New_login.html',{"state":state_str})

def register(request):
    # print('t: '+str(request.GET.get('result')))
    if request.method == "GET":
        return render(request,'register.html')

    User = request.POST.get('USER')
    Upwd = request.POST.get('PWD')
    f = open('./sql_file/Create_User.sql','r',encoding='utf-8')
    sqlProgram = f.read()
    sqlProgram = sqlProgram.replace('@@user_name@@',User)
    sqlProgram = sqlProgram.replace('@@user_password@@',Upwd)
    f.close()

    import psycopg2
    import sys

    con = None
    try:
        con = psycopg2.connect(database='setu', user='postgres',password='123456')
        cur = con.cursor()
        cur.execute(sqlProgram)
        sqlRetPWD = cur.fetchall()
        cur.connection.commit()
        
        print(sqlRetPWD[0][0])
        if sqlRetPWD[0][0] == True:
            state_str = '注册成功！'
            print(state_str)
            newURL = '/login?result=%s' %(state_str)
            return redirect(newURL)
            # return render(request,'New_login.html',{"state":state_str})
    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)
    finally:
        if con:
            con.close()
    state_str = '注册失败！'
    print(state_str)
    return render(request,'register.html',{"state":state_str})

