from __future__ import print_function
import time
import sys
import os
import datetime
import re



class Checker:

    def EIforderCheck():

        if os.path.exists("../Fpool") == False:
            os.mkdir("../Fpool")



    def InputRule(Fnum, ChVal):
        index = 0
        if Fnum == 0:
            searchFormat = re.compile(r'[0-9]')
            Vlen = len(ChVal)
            if Vlen > 4:
                print("""入力文字数が４桁より多いです。会員IDは４桁です。\n先ほどの入力文字数：%s文字""" % Vlen)
            elif Vlen < 4:
                print("""入力文字数が４桁より少ないです。会員IDは４桁です。\n先ほどの入力文字数：%s文字""" % Vlen)
            for IDchar in ChVal:
                index += 1
                SResult = searchFormat.search(IDchar)
                if SResult == None:
                    print('%d文字目に使用不可文字「%s」が入力されています。' % (index, IDchar))
            return False
        elif Fnum == 1:
            searchFormatHK = re.compile(r'[\u3040-\u30FF]')  # ひらがな＆カタカナ
            searchFormatKN = re.compile(r'[\u4E00-\u9FFF]')  # 漢字
            spaceIndex = 0
            Vlen = len(ChVal)
            if Vlen != 30:
                if Vlen > 30:
                    print("入力文字数が多すぎます。お名前が入りきらない場合は管理者へ問い合わせてください。")
            for NameChar in ChVal:
                index += 1
                SResultHK = searchFormatHK.search(NameChar)
                SResultKN = searchFormatKN.search(NameChar)
                if index == 1 | index == Vlen:
                    if spaceIndex > 0:
                        print('%dつ目のスペースが入力されています。')
                        spaceIndex += 1
                        continue
                    elif NameChar == '　':
                        spaceIndex += 1
                        continue
                    elif NameChar == ' ':
                        spaceIndex += 1
                        continue
                elif SResultHK == None:
                    print('%d文字目に使用不可文字「%s」が入力されています。' % (index, NameChar))
                    continue
                elif SResultKN == None:
                    print('%d文字目に使用不可文字「%s」が入力されています。' % (index, NameChar))
            return False
        else:
            return True



class IOcontrol:  # ファイル入出力

    # Fname = ""

    def DExpt(func, writeV):  # ファイル出力

        Checker.EIforderCheck()

        Gdate = datetime.datetime.now()  # 今の日時
        Pdate = Gdate.strftime('%Y%m%d_%H%M%S')  # 日時のSTR化

        Fname = 'Expt_' + Pdate  # 出力ファイル名「Expt_YYYYmmdd_HHMMSS」

        # 出力ファイル生成
        f = open('../Fpool/%s.prf' % Fname, 'w')
        f.write("%s %s" % (func, writeV))
        f.close()

        return Pdate


    def DInpt():  # ファイル読込み
        Checker.EIforderCheck()
        Gret = 'brank'

        while True:
            time.sleep(2)
            FName = IOcontrol.DSearch()
            if FName == False:
                continue

            # SV生成ファイルの読み込み
            for gFName in FName:

                if gFName[0] == 'R':
                    f = open('../Fpool/%s' % gFName, 'r')
                    Gret = f.read()  # SVからの返事を格納
                    f.close()
                    # 使用済みファイルのリネーム
                    rFName = 'cmp-' + gFName
                    os.rename('../Fpool/%s' % gFName, '../Fpool/%s' % rFName)

                else:
                    continue

                return Gret



    def DSearch():

        Checker.EIforderCheck()

        SearchFile = os.listdir('../Fpool/')

        rslLen = len(SearchFile)

        if rslLen == 0:
            return False

        else:
            return SearchFile



class CLfunction:

    def NewCreate():

        while True:

            mainTop.CreateTop()

            UserID = USERinput.inputID(2)
            UserData = USERinput.createUSER()

            UpData = UserID + ' '

            for instr in UserData:
                UpData = UpData + instr
                UpData = UpData + '/'

            IOcontrol.DExpt('1', UpData)
            result = IOcontrol.DInpt()
            # result = 'OK'

            if result == 'True':
                print('\n登録が完了しました\n')

            else:
                print('\n登録に失敗しました\n')

            FanCnt = USERinput.FunctionContinue()

            os.system('clear')

            if FanCnt == True:
                continue

            elif FanCnt == False:
                break



    def SearchUser():

        while True:

            mainTop.SearchTop()

            UserID = USERinput.inputID(2)

            IOcontrol.DExpt('2', UserID)
            result = IOcontrol.DInpt()

            if result == 'True':
                print('\n指定されたユーザ(UserID:%s)は存在します。\n' % UserID)

            else:
                print('\n指定されたユーザ(UserID:%s)は存在しません。\n' % UserID)


            FanCnt = USERinput.FunctionContinue()

            os.system('clear')

            if FanCnt == True:
                continue

            elif FanCnt == False:
                break



    def DeleteUser():

        while True:

            mainTop.DeleteTop()

            UserID = USERinput.inputID(3)

            print('\n\n？？？を本当に削除しますか？')

            while True:

                answer = input(' Y / N >>')

                if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
                    IOcontrol.DExpt('3', UserID)
                    result = IOcontrol.DInpt()
                    # result = 1

                    if result == 1:
                        print("\n削除が完了しました。\n")

                    else:
                        print("\n削除が実行できませんでした。\n")

                    break

                elif answer == 'N' or answer == 'n' or answer == 'no' or answer == 'NO':
                    print("\n\nユーザの削除を中止します")
                    break

                else:
                    print("\n'Y'または'N'を入力してください\n")
                    continue



            FanCnt = USERinput.FunctionContinue()

            os.system('clear')

            if FanCnt == True:
                continue

            elif FanCnt == False:
                break





# ユーザ入力

class USERinput:

    def inputID(func):

        while True:
            userID = input("ユーザIDを入力してください>>")

            # Chres = Checker.InputRule(0, userID)
            # if Chres == False:
            #    continue

            ##SVconnect#引数で照会/削除指定の関数作成
            IOcontrol.DExpt(2, userID)

            reqResult = IOcontrol.DInpt()

            if len(reqResult) == 0:
                if func == 1:
                    print('')
                    # return userID

                elif func == 2:
                    print('\n\n指定されたユーザは存在しません。\n他のIDを指定してください')
                    continue

                elif func == 3:
                    print('\n\n指定されたユーザは存在しません。\n他のIDを指定してください')
                    continue



            else:
                if func == 1:
                    print('\n\n新規：ユーザデータが存在します。\n他のIDを指定してください')
                    continue

                elif func == 2:
                    print('')

                elif func == 3:
                    print('')

            print('\n')

            return userID



    def createUSER():

        userNAME = input("\nユーザ氏名を入力してください>>")
        userPLACE = input("\n住所を入力してください>>")
        userTEL = input("\nユーザ連絡先[TEL]を入力してください>>")
        userMAIL = input("\nユーザ連絡先[MAIL]を入力してください>>")

        return (userNAME, userPLACE, userTEL, userMAIL)



    def FunctionContinue():

        while True:
            answer = input("\n\nこの機能を続けますか(Y/N)>>")

            if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
                return True

            elif answer == 'N' or answer == 'n' or answer == 'no' or answer == 'NO':
                return False

            else:
                print('\n入力できるのは Y または N のみです。')
                continue



# 画面表示

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
            os.system('clear')
            sys.exit()



    def CreateTop():

        print("""
            ユーザの新規登録を行います。
            以下の入力要領に従って入力してください。

            ################################################################
            # 入力内容                                                     #
            #                                                              #
            # 1:ユーザＩＤ（半角数字４桁）                                 #
            # 2:ユーザ氏名                                                 #
            # 　　　　（漢字表記、姓名の間はスペースを入力）               #
            # 3:住所　（郵便番号、住所　※建物名、部屋番号等を含む）       #
            # 4:ユーザ連絡先[TEL]                                          #
            # 　　　　（ハイフンあり、市外局番含む）                       #
            # 5:ユーザ連絡先[MAIL]                                         #
            # 　　　　                                                     #
            ################################################################
            """)



    def SearchTop():

        print("""
            ユーザの検索を行います。
            以下の入力要領に従って入力してください。

            ################################################################
            # 入力内容                                                     #
            #                                                              #
            # 1:ユーザＩＤ（半角数字４桁）                                 #
            # 　　　　                                                     #
            ################################################################
            """)



    def DeleteTop():

        print("""
            ユーザの削除を行います。
            以下の入力要領に従って入力してください。

            ################################################################
            # 入力内容                                                     #
            #                                                              #
            # 1:ユーザＩＤ（半角数字４桁）                                 #
            # 　　　　                                                     #
            ################################################################
            """)





if __name__ == '__main__':

    os.system('clear')

    while True:
        M_val = mainTop.printTop()

        print(M_val)

        # 新規登録
        if M_val == '1':
            try:
                os.system('clear')
                CLfunction.NewCreate()
                continue

            except:
                os.system('clear')
                print("1 の入力を受け付けました")

        # 参照
        elif M_val == '2':
            try:
                os.system('clear')
                CLfunction.SearchUser()
                continue

            except:
                os.system('clear')
                print("2 の入力を受け付けました")

        # 削除

        elif M_val == '3':
            try:
                os.system('clear')
                CLfunction.DeleteUser()
                continue

            except:
                os.system('clear')
                print("3 の入力を受け付けました")

        # 終了
        elif M_val == '0':
            os.system('clear')
            mainTop.printFin()

        # 入力エラー
        else:
            os.system('clear')
            print("指定と異なる値です。もう一度入れなおしてください。")
            continue
