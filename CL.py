from __future__ import print_function
import sys
import os
import socket
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
class IOcontrol:
    def DExpt(self):
        



#ユーザ入力
class USERinput:
    def inputID(self, M_vla):
        userID = input("IDを入力してください>>")

        SVconnect#引数で照会/削除指定の関数作成

        return  userID

    def createUSER(self):
        userID = input("IDを入力してください>>")
        userNAME = input("名前を入力してください>>")
        userPLACE = input("住所を入力してください>>")
        userTEL = input("連絡先(電話番号)を入力してください>>")
        userMAIL = input("連絡先(メールアドレス)を入力してください>>")

        return  (userID, userNAME, userPLACE, userTEL, userMAIL)

#メイン表示
class mainTop:
    def printTop(self):
        os.system('cls')

        print("""
            
            ##############################
            # メニューを選択してください   #
            #                            #
            # 1:新規登録                  #
            # 2:会員紹介                  #
            # 3:会員情報削除              #
            #                            #
            # 0:終了                     #
            ##############################
            
            
            """)
        sl_Menu = input('>> ')

        return sl_Menu

    def printFin(self):
        os.system('cls')

        print("""
            
            アプリを終了します。
            エンターキーを押してください。
            
            """)

        end_Cnt = input('')

        if len(end_Cnt) >= 0:
            sys.exit()


if __name__ == '__main__':

    while True:
        M_val = mainTop.printTop()

        if M_val == 1:
            USERinput.createUSER()
        elif M_val == 2:
            USERinput.inputID(M_val)
        elif M_val == 3:
            USERinput.inputID(M_val)
        elif M_val == 0:
            mainTop.printFin()
        else:
            continue

