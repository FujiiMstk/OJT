from __future__ import print_function
import os
import time
import redis

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
                f = open('../Fpool/RSL-%s' % picFName, 'w')
                f.write("%s" % writeV)
                f.close()
            elif picFName[0] == '-':
                os.remove('../Fpool/%s' % picFName)



    def DInpt(FName):  # ファイル読込み

        Checker.EIforderCheck()

        Gret = None

        # SV生成ファイルの読み込み
        if FName[0] == 'E':
            f = open('../Fpool/%s' % FName, 'r')
            for Inpt in f:
                Gret = Inpt  # f#.strip()    #SVからの返事を格納

            f.close()

            os.rename('../Fpool/%s' % FName, '../Fpool/-%s' % FName)

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

                result = r.set(CLreq[1], CLreq[2])

                IOcontrol.DExpt(FName, result)

                continue



            elif CLreq[0] == '2':

                result = r.exists(CLreq[1])
                print(result)

                IOcontrol.DExpt(FName, result)
                continue



            elif CLreq[0] == '3':

                result = r.delete(CLreq[1])
                print(result)

                IOcontrol.DExpt(FName, result)
                continue


            elif CLreq[0] == '4':

                result = r.get(CLreq[1])
                print(result)

                IOcontrol.DExpt(FName, result.decode('utf-8'))
                continue



if __name__ == '__main__':

    main()
