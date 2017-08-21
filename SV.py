from __future__ import print_function
from datetime import datetime
import os
import time
import redis

import logging


class log:
    if os.path.exists("./Log/") == False:
        os.mkdir("./Log/")
    t = datetime.today()
    logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='./Log/%s_SV.log'%t.strftime("%Y%m%d"), format=logF, level=logging.DEBUG)

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
            os.mkdir("../Fpool")



class IOcontrol:  # ファイル入出力

    def DExpt(FName, writeV):  # ファイル出力

        Checker.EIforderCheck()

        # 出力ファイル生成
        for picFName in FName:

            if picFName[0] == 'E':
                f = open('../Fpool/RSL_%s' % picFName, 'w')
                log.info("Create:RSL_%s" % picFName)
                f.write("%s" % writeV)
                f.close()
            elif picFName[0] == '_':
                log.info(os.remove('../Fpool/%s' % picFName))



    def DInpt(FName):  # ファイル読込み

        Checker.EIforderCheck()

        Gret = None

        # SV生成ファイルの読み込み
        if FName[0] == 'E':
            f = open('../Fpool/%s' % FName, 'r')
            for Inpt in f:
                Gret = Inpt  # f#.strip()    #SVからの返事を格納

            f.close()

            log.info(os.rename('../Fpool/%s' % FName, '../Fpool/_%s' % FName))

        return Gret



    def DSearch():
        Checker.EIforderCheck()

        SearchFile = os.listdir('../Fpool/')
        rslLen = len(SearchFile)

        if rslLen == 0:
            return False

        else:
            return SearchFile  # [0]


def main():
    log.info("SV_wake")
    r = redis.Redis(host='localhost', port=6379, db=15)

    TgFName = 'brank'
    GetCLreq = 'brank'

    while True:
        time.sleep(1)
        FName = IOcontrol.DSearch()

        if FName == False:
            continue

        else:
            for gFName in FName:
                GetCLreq = IOcontrol.DInpt(gFName)

                if GetCLreq != None:
                    TgFName = gFName
                    break

        if GetCLreq != None:

            CLreq = GetCLreq.split()
            if CLreq[0] == '1':
                log.info("Select1")

                result = r.set(CLreq[1], CLreq[2])

                log.debag(IOcontrol.DExpt(FName, result))

                continue



            elif CLreq[0] == '2':
                log.info("Select2")

                result = r.exists(CLreq[1])
                #print(result)

                log.debag(IOcontrol.DExpt(FName, result))
                continue



            elif CLreq[0] == '3':
                log.info("Select3")

                result = r.delete(CLreq[1])
                #print(result)

                log.debag(IOcontrol.DExpt(FName, result))
                continue


            elif CLreq[0] == '4':
                log.info("Select4")

                result = r.get(CLreq[1])
                #print(result)

                log.debag(IOcontrol.DExpt(FName, result.decode('utf-8')))
                continue

            elif CLreq[0] == '5':
                log.info("Select5")

                result = r.keys(CLreq[1])
                #print(result)

                log.debag(IOcontrol.DExpt(FName, result.decode('utf-8')))
                continue

            elif CLreq[0] == '0':
                log.info("Select0")

                result = "shutdown"
                #print(result)

                log.debag(IOcontrol.DExpt(FName, result))
                print("Server Shutdown")
                return 0



if __name__ == '__main__':

    main()
