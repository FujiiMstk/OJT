from __future__ import print_function
from datetime import datetime
import os
import time
import redis
import sys
import traceback
import logging
import inspect

###ログ出力用関数###
class log:

    #出力先フォルダ存在確認#
    if os.path.exists("./Log/") == False:
        os.mkdir("./Log/")

    t = datetime.today()    #出力ファイル用の日付の取得#
    logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'    #ログ出力フォーマット#

    #ログ出力#
    logging.basicConfig(filename='./Log/%s_SV.log'%t.strftime("%Y%m%d"), format=logF, level=logging.DEBUG)


    def INFO(INFO, line):
        formatLine = None
        for spritLine in line:
            formatLine = formatLine + spritLine
        logging.info(INFO+formatLine)

    def ERROR(INFO, line):
        formatLine = None
        for spritLine in line:
            formatLine = formatLine + spritLine
        logging.error(INFO+line)

    def WARN(INFO, line):
        formatLine = None
        for spritLine in line:
            formatLine = formatLine + spritLine
        logging.warning(INFO+line)

    def CRIT(INFO, line):
        formatLine = None
        for spritLine in line:
            formatLine = formatLine + spritLine
        logging.critical(INFO+line)

    def DEBUG(INFO, line):
        formatLine = None
        for spritLine in line:
            formatLine = formatLine + spritLine
        logging.debug(INFO+line)

    def location(depth=0):
        frame = inspect.currentframe().f_back
        return os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno




###データ受け渡しフォルダ確保###
class Checker:
    def EIforderCheck():
        if os.path.exists("../Fpool") == False:
            os.mkdir("../Fpool")



###データ受け渡し###
class IOcontrol:  # ファイル入出力

    def DExpt(FName, writeV):  # ファイル出力

        Checker.EIforderCheck()

        # 出力ファイル生成
        for picFName in FName:

            if picFName[0] == 'E':
                f = open('../Fpool/RSL_%s' % picFName, 'w')
                log.INFO("Create:RSL_%s" % picFName, log.location())
                f.write("%s" % writeV)
                f.close()
            elif picFName[0] == '_':
                log.INFO(os.remove('../Fpool/%s' % picFName), log.location())



    def DInpt(FName):  # ファイル読込み

        Checker.EIforderCheck()

        Gret = None

        # SV生成ファイルの読み込み
        if FName[0] == 'E':
            f = open('../Fpool/%s' % FName, 'r')
            for Inpt in f:
                Gret = Inpt  # f#.strip()    #SVからの返事を格納

            f.close()

            log.INFO(os.remove('../Fpool/%s' % FName), log.location()) #os.rename('../Fpool/%s' % FName, '../Fpool/_%s' % FName))

        return Gret



    def DSearch():  #データ格納先確認#
        Checker.EIforderCheck()

        SearchFile = os.listdir('../Fpool/')
        rslLen = len(SearchFile)

        if rslLen == 0:
            return False

        else:
            return SearchFile  # [0]


def main():
    log.INFO("join:main()", log.location())
    r = redis.Redis(host='localhost', port=6379, db=15) #Redis接続#

    TgFName = 'brank'
    GetCLreq = 'brank'

    while True:
        time.sleep(1)
        FName = IOcontrol.DSearch()

        try:
            if len(FName) == 0: #FName == None:
                continue

            else:
                for gFName in FName:
                    GetCLreq = IOcontrol.DInpt(gFName)

                    if GetCLreq != None:
                        TgFName = gFName
                        break

            if GetCLreq != None:

                CLreq = GetCLreq.split()

                #新規登録#
                if CLreq[0] == '1':
                    log.INFO("Select1", log.location())

                    result = r.set(CLreq[1], CLreq[2])

                    log.DEBUG(IOcontrol.DExpt(FName, result), log.location())

                    continue


                #参照#
                elif CLreq[0] == '2':
                    log.INFO("Select2", log.location())

                    result = r.exists(CLreq[1])
                    #print(result)

                    log.DEBUG(IOcontrol.DExpt(FName, result), log.location())
                    continue


                #削除#
                elif CLreq[0] == '3':
                    log.INFO("Select3", log.location())

                    result = r.delete(CLreq[1])
                    #print(result)

                    log.DEBUG(IOcontrol.DExpt(FName, result), log.location())
                    continue

                #詳細情報を取得#
                elif CLreq[0] == '4':
                    log.INFO("Select4", log.location())

                    result = r.get(CLreq[1])
                    #print(result)

                    log.DEBUG(IOcontrol.DExpt(FName, result.decode('utf-8')), log.location())
                    continue


                #登録済みkey取得#
                elif CLreq[0] == '5':
                    log.INFO("Select5", log.location())

                    result = r.keys(CLreq[1])
                    #print(result)

                    log.DEBUG(IOcontrol.DExpt(FName, result.decode('utf-8')), log.location())
                    continue

                #終了#
                elif CLreq[0] == '0':
                    log.INFO("Select0", log.location())

                    result = "shutdown"
                    #print(result)

                    log.DEBUG(IOcontrol.DExpt(FName, result), log.location())
                    print("Server Shutdown")
                    log.INFO("Server Shutdown", log.location())
                    sys.exit()
            else:
                continue

        except SystemExit:
            return  0

        else:
            log.INFO("GetException", log.location())
            log.DEBUG(FName, log.location())
            log.WARN(traceback.format_exc(), log.location())
            #traceback.print_exception()
            continue


if __name__ == '__main__':
    log.INFO("Wake SV!:", log.location())
    main()
    log.INFO("See You!", log.location())