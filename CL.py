from __future__ import print_function
import timeout_decorator
import time
import sys
import os
import datetime
import re
import logging
import subprocess

###タイムアウト待機時間(秒)###
MAIN_PROCESS_TIMEOUT = 15

###ログ出力用関数###
class log:

    #出力先フォルダ存在確認#
    if os.path.exists("./Log/") == False:
        os.mkdir("./Log/")

    t = datetime.datetime.today()    #出力ファイル用の日付の取得#
    logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'    #ログ出力フォーマット#

    #ログ出力#
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


###フォルダチェック・入力チェック###
class Checker:
    ###データ受け渡しフォルダ確保###
    def EIforderCheck():

        if os.path.exists("../Fpool/") == False:
            log.info("mkdir:Fpool")
            log.debag(os.mkdir("../Fpool/"))

    ###入力規則###
    def InputRule(Fnum, ChVal):

        searchFormatSP = re.compile('\s\s+')

        # ID規則#
        if Fnum == 0:
            searchFormat = re.compile('\d{4}')
            Vlen = len(ChVal)
            if Vlen > 4:
                print("""入力文字数が４桁より多いです。会員IDは４桁です。\n先ほどの入力文字数：%s文字""" % Vlen)
            elif Vlen < 4:
                print("""入力文字数が４桁より少ないです。会員IDは４桁です。\n先ほどの入力文字数：%s文字""" % Vlen)

            SResult = searchFormat.match(ChVal)
            if SResult == None:
                print('指定の形式で入力されていません。')
                return False
            else:
                return True

        # 名前入力規則#
        elif Fnum == 1:
            print("C1")

            searchFormatJP = re.compile('[ぁ-んァ-ン一-龥　\u0020]+')  # 日本語
            searchFormatAZ = re.compile('[a-zA-Z　 ]+')  # 英名 or ミドルネーム
            searchFormatNMA = re.compile('[!"#$%&\'\(\)=\~\|\-\^\`\{\@\[\]\}+*;:<>?_,./！”＃＄％＆’（）＝～｜－＾￥‘｛＠「＋＊｝；：」＜＞？＿、。・\d]+')

            Vlen = len(ChVal)
            if Vlen != 30:
                if Vlen > 30:
                    print("入力文字数が多すぎます。お名前が入りきらない場合は管理者へ問い合わせてください。")

            SResultJP = searchFormatJP.match(ChVal)
            SResultAZ = searchFormatAZ.search(ChVal)
            SResultSP = searchFormatSP.findall(ChVal)
            SResultNMA = searchFormatNMA.findall(ChVal)

            if SResultJP != None and len(SResultSP) == 0 :
                return True

            elif SResultAZ != None and len(SResultSP) == 0 :
                return True

            elif len(SResultSP) >=1 or len(SResultNMA) >= 1:
                if len(SResultSP) >=1 :
                    print('\nスペース2つ以上連続して入力されている箇所があります。\n')
                elif len(SResultNMA) >= 1:
                    print("\n使用できない文字が使用されています。\n使用されている文字：%s\n" % SResultNMA)
                return False

        # 住所規則#
        elif Fnum == 2:
            print("C2")

            searchFormatPL = re.compile('[一-龥]{2,3}[都道府県][ぁ-んァ-ン一-龥　\u0020\w\-－]+')  # 日本語/英数字/スペース/ハイフン
            searchFormatPMA = re.compile('[!"#$%&\'\(\)=\~\|\^\`\{\@\[\]\}+*;:<>?_,./！”＃＄％＆’（）＝～｜＾￥‘｛＠「＋＊｝；：」＜＞？＿、。・]+')

            Vlen = len(ChVal)
            if Vlen != 50:
                if Vlen > 50:
                    print("入力文字数が多すぎます。住所が入りきらない場合は管理者へ問い合わせてください。")

            SResultPL = searchFormatPL.match(ChVal)
            SResultSP = searchFormatSP.findall(ChVal)
            SResultPMA = searchFormatPMA.findall(ChVal)


            if SResultPL != None and len(SResultSP) == 0:
                return True

            elif len(SResultSP) >= 1 or len(SResultPMA) >= 1:
                if len(SResultSP) >= 1:
                    print('\nスペース2つ以上連続して入力されている箇所があります。\n')
                elif len(SResultPMA) >= 1:
                    print("\n使用できない文字が使用されています。\n使用されている文字：%s\n" % SResultPMA)
                return False
            else :
                print("指定の入力は無効です。受け取った値[%s]"%ChVal)
                return False

        # 連絡先(TEL)入力規則#
        elif Fnum == 3:
            print("C3")

            #国内プレフィックス「0」+[市外局番+市内局番「全5桁」]+加入者番号「4桁」#
            searchFormatTL1 = re.compile('0[346]\-\d{4}\-\d{4}')  #固定電話1
            searchFormatTL2 = re.compile('0\d{2}\-\d{3}\-\d{4}')  #固定電話2
            searchFormatTL3 = re.compile('0\d{3}\-\d{2}\-\d{4}')  #固定電話3
            searchFormatTL4 = re.compile('0\d{4}\-\d{1}\-\d{4}')  #固定電話4
            searchFormatTL5 = re.compile('0[5789]0\-\d{4}\-\d{4}')  #携帯電話
            searchFormatTMA = re.compile('\D+')

            Vlen = len(ChVal)
            if Vlen != 13:
                if Vlen > 13:
                    print("入力文字数が多すぎます。もう一度やり直してください。")

            SResultTL1 = searchFormatTL1.match(ChVal)
            SResultTL2 = searchFormatTL2.match(ChVal)
            SResultTL3 = searchFormatTL3.match(ChVal)
            SResultTL4 = searchFormatTL4.match(ChVal)
            SResultTL5 = searchFormatTL5.match(ChVal)
            SResultTMA = searchFormatTMA.findall(ChVal)


            if SResultTL1 != None or SResultTL2 != None or SResultTL3 != None or SResultTL4 != None or SResultTL5 != None :
                return True

            elif len(SResultTMA) >= 1:
                if len(SResultTMA) >= 1:
                    print("\n使用できない文字が使用されています。\n使用されている文字：%s\n" % SResultMA)
                return False

            else :
                print("指定の入力は無効です。受け取った値[%s]"%ChVal)
                return False

        # 連絡先(MAIL)入力規則#
        elif Fnum == 4:
            print("C4")

            searchFormatML = re.compile('[a-z0-9._\-]{2,30}\@[a-z0-9._\-]+')  # [30]@domein
            searchFormatDD = re.compile('\.\.+')
            searchFormatMMA = re.compile('[!"#$%&\'\(\)=\~\|\^\`\{\@\[\]\}+*;:<>?,/！”＃＄％＆’（）＝～｜－＾￥‘｛＠「＋＊｝；：」＜＞？＿、。・ 　]+')

            Vlen = len(ChVal)
            if Vlen != 100:
                if Vlen > 100:
                    print("入力文字数が多すぎます。お持ちのメールアドレスが入りきらない場合は管理者へ問い合わせてください。")

            SResultML = searchFormatML.match(ChVal)
            SResultDD = searchFormatDD.findall(ChVal)
            SResultMMA = searchFormatMMA.findall(ChVal)


            if SResultML != None and len(SResultDD) == 0:
                return True

            elif len(SResultDD) >= 1 or len(SResultMMA) >= 1:
                if len(SResultDD) >= 1:
                    print('\n[.]が2つ以上連続して入力されている箇所があります。\n')
                elif len(SResultMMA) >= 1:
                    print("\n使用できない文字が使用されています。\n使用されている文字：%s\n" % SResultMMA)
                return False

            else :
                print("指定の入力は無効です。受け取った値[%s]"%ChVal)
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
                    # 使用済みファイルのリムーブ
                    log.debag(os.remove('../Fpool/%s' % gFName))
                    log.info("removed")

                else:
                    continue

                log.info("fin_InptFile")

                return Gret

    def DSearch():#データ格納先確認#

        Checker.EIforderCheck()

        SearchFile = os.listdir('../Fpool/')

        rslLen = len(SearchFile)

        if rslLen == 0:
            return False

        else:
            return SearchFile


###機能別関数###
class CLfunction:
    #新規登録#
    def NewCreate():
        log.info("NewCreate")

        while True:

            mainTop.CreateTop()

            UserID = USERinput.inputID(1)
            UserData = USERinput.createUSER()

            UpData = UserID + ' '

            for instr in UserData:
                instr = instr.replace('\u0020', '#')
                instr = instr.replace('\u3000', '＃')
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

            mainTop.UIclean()

            if FanCnt == True:
                log.info("Create_continue")
                continue

            elif FanCnt == False:
                log.info("fin_NewCreate")
                break

    #参照#
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

            mainTop.UIclean()

            if FanCnt == True:
                log.info("Search_continue")
                continue

            elif FanCnt == False:
                log.info("fin_Search")
                break

    #削除#
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

            mainTop.UIclean()

            if FanCnt == True:
                log.info("Delete_continue")
                continue

            elif FanCnt == False:
                log.info("fin_Delete")
                break

    #参照先詳細表示#
    def ShowUser(UserID):
        print('\n\n登録内容を確認しますか？')
        while True:
            answer = input(' Y / N >>')

            if answer == 'Y' or answer == 'y' or answer == 'yes' or answer == 'YES':
                IOcontrol.DExpt('4', UserID)
                result = IOcontrol.DInpt()

                result = result.replace('#', '\u0020')
                result = result.replace('＃', '\u3000')

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

# ユーザ入力#
class USERinput:
    #ID確認#
    def inputID(func):
        EvCount = 0

        while True:
            EvCount+=1
            userID = input("ユーザIDを入力してください>>")

            Chres = Checker.InputRule(0, userID)
            print(Chres)
            if Chres == False:
               continue

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

            #ID戻り値確認#
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

    #ユーザ情報の入力#
    def createUSER():

        while True:
            userNAME = input("\nユーザ氏名を入力してください>>")
            userPLACE = input("\n住所を入力してください>>")
            userTEL = input("\nユーザ連絡先[TEL]を入力してください>>")
            userMAIL = input("\nユーザ連絡先[MAIL]を入力してください>>")

            ResultCheckName = Checker.InputRule(1, userNAME)
            ResultCheckPlace = Checker.InputRule(2, userPLACE)
            ResultCheckTel = Checker.InputRule(3, userTEL)
            ResultCheckMail = Checker.InputRule(4, userMAIL)

            if ResultCheckName == False or ResultCheckPlace == False or ResultCheckTel == False or ResultCheckMail == False:
                print("\n\n必要事項をもう一度入力しなおしてください。")
                for a in range(5):
                    print('。')
                    time.sleep(1)
                mainTop.UIclean()
                mainTop.CreateTop()
                continue

            return (userNAME, userPLACE, userTEL, userMAIL)

    #機能継続確認#
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

    #アプリケーション修了確認#
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
        mainTop.UIclean()

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

        mainTop.UIclean()

        print("""
            アプリを終了します。
            エンターキーを押してください。
            """)

        end_Cnt = input('')

        if len(end_Cnt) >= 0:
            mainTop.UIclean()
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

    def UIclean():  ###見た目きれいに###
        if os.name == 'posix':  ###LINUX用###
            subprocess.call('clear', shell=True)
        elif os.name == 'nt':  ###Windows用###
            subprocess.call('cls', shell=True)
        print()


def mail():

    while True:
        M_val = mainTop.printTop()
        log.debag('main(Mval:%s)'%M_val)

        # 新規登録
        if M_val == '1':
            log.info("Swlwct_New")
            try:
                mainTop.UIclean()
                CLfunction.NewCreate()
                continue

            except:
                log.errer("Geterrer:L(New)")
                mainTop.UIclean()
                #mainTop.BreakEvent()

        # 参照
        elif M_val == '2':
            log.info("Select_Get")
            try:
                mainTop.UIclean()
                CLfunction.SearchUser()
                continue

            except:
                log.errer("Geterrer:L530(Get)")
                mainTop.UIclean()
                #mainTop.BreakEvent()
        # 削除

        elif M_val == '3':
            log.info("Select_Del")
            try:
                mainTop.UIclean()
                CLfunction.DeleteUser()
                continue

            except:
                log.errer("Geterrer:L543(Del)")
                mainTop.UIclean()
                #mainTop.BreakEvent()
        # 終了
        elif M_val == '0':
            log.info("Select_EXIT")
            try:
                result = USERinput.FunctionExit()
                if result == True:
                    mainTop.UIclean()
                    if mainTop.printFin() == 0:
                        return 0
                else:
                    print("アプリケーションに戻ります。\nしばらくお待ちください。")
                    for p in "          ":
                        print(p, end='')
                        time.sleep(0.5)
                    mainTop.UIclean()
                    continue
            except:
                log.errer("Geterrer:L559(EXIT)")
                mainTop.UIclean()
                print("\n\n\n\nサーバの終了を確認できませんでした。\nプロセスを確認し、手動で終了させてください。")
                print("\n\nアプリケーションを終了しました。")
                return 0

        # 入力エラー
        else:
            log.warning("InputWarning(main:%s)"%M_val)
            mainTop.UIclean()
            print("指定と異なる値です。もう一度入れなおしてください。")
            continue

if __name__ == '__main__':
    log.info("CL_Start")
    mainTop.UIclean()
    mail()
    log.info("CL_fin")
