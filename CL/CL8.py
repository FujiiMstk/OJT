from __future__ import print_function
import timeout_decorator
import time
import sys
import os
import datetime
import re
import logging

MAIN_PROCESS_TIMEOUT = 15

class log:
    if os.path.exists("./Log/") == False:
        os.mkdir("./Log/")
    t = datetime.datetime.today()
    logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='./Log/%s_CL.log'%t.strftime("%Y%m%d"), format=logF, level=logging.DEBUG)

    def info(INFO):
        logging.info(INFO)

    def errer(INFO):
        logging.error(INFO)

    def warning(INFO):
        logging.warning(INFO)

    def critical(INFO):
        logging.critical(INFO)

    def debag(INFO):
        logging.debug(INFO)


class Checker:
    def EIforderCheck():

        if os.path.exists("../Fpool") == False:
            log.info("mkdir:Fpool")
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
        log.info("MakeExptFile")

        Checker.EIforderCheck()

        Gdate = datetime.datetime.now()  # 今の日時
        Pdate = Gdate.strftime('%Y%m%d_%H%M%S')  # 日時のSTR化

        Fname = 'Expt_' + Pdate  # 出力ファイル名「Expt_YYYYmmdd_HHMMSS」

        # 出力ファイル生成
        f = open('../Fpool/%s.prf' % Fname, 'w')
        f.write("%s %s" % (func, writeV))
        f.close()

        log.info("MadeExptFile")

        return Pdate

    def DInpt():  # ファイル読込み
        log.info("InptFile")

        Checker.EIforderCheck()
        Gret = 'brank'

        while True:
            time.sleep(2)
            FName = IOcontrol.DSearch()
            if FName == False:
                continue

            # SV生成ファイルの読み込み
            for gFName in FName:
                log.debag("gFName:%s"%gFName)

                if gFName[0] == 'R':
                    f = open('../Fpool/%s' % gFName, 'r')
                    Gret = f.read()  # SVからの返事を格納
                    f.close()
                    # 使用済みファイルのリネーム
                    rFName = 'cmp-' + gFName
                    log.debag(os.rename('../Fpool/%s' % gFName, '../Fpool/%s' % rFName))
                    log.info("renamed")

                else:
                    continue

                log.info("fin_InptFile")

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
        log.info("NewCreate")

        while True:

            mainTop.CreateTop()

            UserID = USERinput.inputID(1)
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
                log.info("Create_OK")

            else:
                print('\n登録に失敗しました\n')
                log.info("Create_BAD")

            FanCnt = USERinput.FunctionContinue()

            os.system('clear')

            if FanCnt == True:
                log.info("Create_continue")
                continue

            elif FanCnt == False:
                log.info("fin_NewCreate")
                break

    def SearchUser():
        log.info("Search")

        while True:

            mainTop.SearchTop()

            UserID = USERinput.inputID(2)

            if UserID[0] == '*':
                IOcontrol.DExpt('5', UserID[0])
                result = IOcontrol.DInpt()
            else:
                IOcontrol.DExpt('2', UserID)
                result = IOcontrol.DInpt()

            if UserID[0] == '*':
                if result != '':
                    print("『現在格納されているUserID』")
                    for ID in result:
                        print(ID)
                else:
                    print("現在格納されている情報はありません。")

            else:
                if result == 'True':
                    print('\n指定されたユーザ(UserID:%s)は存在します。\n' % UserID)
                    CLfunction.ShowUser(UserID)

                else:
                    print('\n指定されたユーザ(UserID:%s)は存在しません。\n' % UserID)

            FanCnt = USERinput.FunctionContinue()

            os.system('clear')

            if FanCnt == True:
                log.info("Search_continue")
                continue

            elif FanCnt == False:
                log.info("fin_Search")
                break

    def DeleteUser():
        log.info("Delete")

        while True:

            mainTop.DeleteTop()

            UserID = USERinput.inputID(3)

            if UserID == 'False':
                print("\n指定されたIDは存在しませんでした。\n入力しなおしてください。")
                continue
            else:
                print('\n\nID:%s を本当に削除しますか？' % UserID)

            while True:

                answer = input(' Y / N >>')

                if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
                    IOcontrol.DExpt('3', UserID)
                    result = IOcontrol.DInpt()
                    # result = 1

                    if result == '1':
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
                log.info("Delete_continue")
                continue

            elif FanCnt == False:
                log.info("fin_Delete")
                break

    def ShowUser(UserID):
        print('\n\n登録内容を確認しますか？')
        while True:
            answer = input(' Y / N >>')

            if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
                IOcontrol.DExpt('4', UserID)
                result = IOcontrol.DInpt()

                CLreq = result.split('/')

                print("\n\n\nユーザID：%s" % UserID)

                print("\n氏名：%s" % CLreq[0])
                print("\n住所：%s" % CLreq[1])
                print("\n連絡先(TEL)：%s" % CLreq[2])
                print("\n連絡先(MAIL)：%s" % CLreq[3])

                print('\n\n＜終了する場合は Enter を入力してください＞')
                while True:
                    ans = input('')
                    if ans == '':
                        return 0
                    else:
                        continue

            elif answer == 'N' or answer == 'n' or answer == 'no' or answer == 'NO':
                print("\n\nユーザの登録情報の表示をスキップします")
                break

            else:
                print("\n'Y'または'N'を入力してください\n")
                continue

# ユーザ入力

class USERinput:
    def inputID(func):
        EvCount = 0

        while True:
            EvCount+=1
            userID = input("ユーザIDを入力してください>>")

            # Chres = Checker.InputRule(0, userID)
            # if Chres == False:
            #    continue

            ##SVconnect#引数で照会/削除指定の関数作成
            if userID == "*":
                IOcontrol.DExpt(5, userID)
            elif userID == "exit":
                print("\n\n機能を終了します\n\n")
                sys.exit()
            else:
                IOcontrol.DExpt(2, userID)

            reqResult = IOcontrol.DInpt()

            if reqResult == "True":
                EvCount = 0

            if len(reqResult) == 0 or reqResult == 'False':
                if EvCount >=5:
                    sys.exit()

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
                if EvCount >=5:
                    sys.exit()

                if func == 1:
                    print('\n\n新規：ユーザデータが存在します。\n他のIDを指定してください')
                    continue

                elif func == 2:
                    print('')

                elif func == 3:
                    print('')

            print('\n')

            if userID == '*':
                return userID, reqResult

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

    def FunctionExit():

        while True:
            answer = input("\n\nこのアプリケーションを終了しますか(Y/N)>>")

            if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
                IOcontrol.DExpt('0', '0')
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
            サーバの終了をまっています。
            しばらくお待ちください。
            """)

        time.sleep(5)

        try:
            if mainTop.SVclose() == "shutdown":
                print('')
        except TimeoutError:
            print("\n\n\n\nサーバの終了を確認できませんでした。\nプロセスを確認し、手動で終了させてください。")

        os.system('clear')

        print("""
            アプリを終了します。
            エンターキーを押してください。
            """)

        end_Cnt = input('')

        if len(end_Cnt) >= 0:
            os.system('clear')
            return 0


    @timeout_decorator.timeout(MAIN_PROCESS_TIMEOUT)
    def SVclose():
        return  IOcontrol.DInpt()

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
            #                                                              #
            #　　　　※終了する場合は exit を入力してください              #
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
            #                                                              #
            #　　　　※終了する場合は exit を入力してください              #
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
            #                                                              #
            #　　　　※終了する場合は exit を入力してください              #
            ################################################################
            """)

    def BreakEvent():
        print("""


        IDが正しく入力されなかったため操作を取りやめます.
        確認の上、もう一度はじめから操作をしてください。


        """)


def mail():

    while True:
        M_val = mainTop.printTop()
        log.debag('main(Mval:%s)'%M_val)

        # 新規登録
        if M_val == '1':
            log.info("Swlwct_New")
            try:
                os.system('clear')
                CLfunction.NewCreate()
                continue

            except:
                log.errer("Geterrer:L(New)")
                os.system('clear')
                #mainTop.BreakEvent()

        # 参照
        elif M_val == '2':
            log.info("Select_Get")
            try:
                os.system('clear')
                CLfunction.SearchUser()
                continue

            except:
                log.errer("Geterrer:L530(Get)")
                os.system('clear')
                #mainTop.BreakEvent()
        # 削除

        elif M_val == '3':
            log.info("Select_Del")
            try:
                os.system('clear')
                CLfunction.DeleteUser()
                continue

            except:
                log.errer("Geterrer:L543(Del)")
                os.system('clear')
                #mainTop.BreakEvent()
        # 終了
        elif M_val == '0':
            log.info("Select_EXIT")
            try:
                result = USERinput.FunctionExit()
                if result == True:
                    os.system('clear')
                    if mainTop.printFin() == 0:
                        return 0
                else:
                    print("アプリケーションに戻ります。\nしばらくお待ちください。")
                    for p in "          ":
                        print(p, end='')
                        time.sleep(0.5)
                    os.system('clear')
                    continue
            except:
                log.errer("Geterrer:L559(EXIT)")
                os.system('clear')
                print("\n\n\n\nサーバの終了を確認できませんでした。\nプロセスを確認し、手動で終了させてください。")
                print("\n\nアプリケーションを終了しました。")
                return 0

        # 入力エラー
        else:
            log.warning("InputWarning(main:%s)"%M_val)
            os.system('clear')
            print("指定と異なる値です。もう一度入れなおしてください。")
            continue

if __name__ == '__main__':
    log.info("CL_Start")
    os.system('clear')
    mail()
