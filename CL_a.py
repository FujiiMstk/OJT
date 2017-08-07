from __future__ import print_function
import sys
import os
import datetime

#import socket
from contextlib import closing

"""     socket通信※使用しない
class SVconnect:
    def SVsend(self):
        host = '127.0.0.1'
        port = 4000
        bufsize = 4096

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect((host, port))
            while True:
                line = USERinput()
                if len(line) == 0:
                    break
                for sline in line:
                    sock.send(sline.encode('utf-8'))
                    print("SV respons: %s " % sock.recv(bufsize).decode('utf-8'))
        return
"""
class Checker:
    def EIforderCheck():
        if os.path.exists("../Fpool") == False:
            os.mkdir("../Fpool")

    def InputRule(Fnum, ChVal):
        if Fnum == 0:
            Vlen = len(ChVal)
            if Vlen != 4:
                if Vlen > 4:
                    print("""入力文字数が４桁より多いです。会員IDは４桁です。
                    先ほどの入力文字数：%s文字""" % Vlen)

                elif Vlen < 4:
                    print("""入力文字数が４桁より少ないです。会員IDは４桁です。
                    先ほどの入力文字数：%s文字""" % Vlen)

                for char in ChVal:
                    if char != [0-9]:
                        
                return False

            else:
                return True

        if Fnum == 1:
            Vlen = len(ChVal)
            if Vlen != 30:
                if Vlen > 30:
                    print("""入力文字数が４桁より多いです。会員IDは４桁です。
                    先ほどの入力文字数：%s文字""" % Vlen)

            for char in
                return False

            else:
                return True




class IOcontrol:    #ファイル入出力

    Fname = ""

    def DExpt(func, writeV):    #ファイル出力
        Checker.EIforderCheck()

        Gdate = datetime.now()  #今の日時
        Pdate = Gdate.strftime('%Y%m%d_%H%M%S') #日時のSTR化

        Fname = 'Expt_' + Pdate     #出力ファイル名「Expt_YYYYmmdd_HHMMSS」

        #出力ファイル生成
        f = open('../Fpool/%s'% Fname, 'w')
        f.write("%s %s" % func , writeV)
        f.close()

        return Pdate

    def DInpt():     #ファイル読込み
        Checker.EIforderCheck()

        #SV生成ファイルの読み込み
        f = open('../Fpool/%s'% Fname, 'r')
        Gret = f.strip()    #SVからの返事を格納
        f.close()

        #使用済みファイルのリネーム
        rFname = 'cmp-' + Fname
        os.rename('../Fpool/%s'% Fname , '../Fpool/%s'% rFname)

        return Gret



class CLfunction:
    def NewCreate():
        while True:

            UserID = USERinput.inputID(1)
            UserData = USERinput.createUSER()


            IOcontrol.DExpt(2, )
            result = IOcontrol.DInpt()










#ユーザ入力
class USERinput:
    def inputID(func):
        while True:
            userID = input("IDを入力してください>>")
            Chres = Checker.InputRule(0, userID)
                if Chres == False:
                    continue


            ##SVconnect#引数で照会/削除指定の関数作成
            IOcontrol.DExpt(userID)
            reqResult = IOcontrol.DInpt()
            if len(reqResult) == 0:
                if func == 1:
                    print('')
                    return userID
                elif func == 2:
                    print('')
                elif func == 3:
                    print('')

            else:
                if func == 1:
                    print('')
                    continue
                elif func == 2:
                    print('')
                elif func == 3:
                    print('')

    def createUSER():
        userNAME = input("名前を入力してください>>")
        userPLACE = input("住所を入力してください>>")
        userTEL = input("連絡先(電話番号)を入力してください>>")
        userMAIL = input("連絡先(メールアドレス)を入力してください>>")

        return  (userNAME, userPLACE, userTEL, userMAIL)



#メイン表示
class mainTop:
    def printTop():
        print("""
            
            ##############################
            # メニューを選択してください #
            #                            #
            # 1:新規登録                 #
            # 2:会員紹介                 #
            # 3:会員情報削除             #
            #                            #
            # 0:終了                     #
            ##############################
            
            
            """)
        sl_Menu = input('>> ')

        return sl_Menu

    def printFin():
        os.system('clear')

        print("""
            
            アプリを終了します。
            エンターキーを押してください。
            
            """)

        end_Cnt = input('')

        if len(end_Cnt) >= 0:
            sys.exit()


if __name__ == '__main__':

    os.system('clear')

    while True:

        M_val = mainTop.printTop()

        print(M_val)

        #新規登録
        if M_val == '1':
            try:
                os.system('clear')
                CLfunction.NewCreate():
            except:
                os.system('clear')
                print("1 の入力を受け付けました")
        #参照
        elif M_val == '2':
            try:
                os.system('clear')
                USERinput.inputID()
            except:
                os.system('clear')
                print("2 の入力を受け付けました")
        #削除
        elif M_val == '3':
            try:
                os.system('clear')
                USERinput.inputID()
            except:
                os.system('clear')
                print("3 の入力を受け付けました")
        #終了
        elif M_val == '0':
            os.system('clear')
            mainTop.printFin()
        #入力エラー
        else:
            os.system('clear')
            print("指定と異なる値です。もう一度入れなおしてください。")
            continue

