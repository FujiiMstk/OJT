from __future__ import print_function
import sys
import os
import datetime
import re

import glob
import redis

#import socket
#import select
from contextlib import closing

"""
def main():
  host = '127.0.0.1'
  port = 4000
  backlog = 10
  bufsize = 4096

  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  readfds = set([server_sock])
  try:
    server_sock.bind((host, port))
    server_sock.listen(backlog)

    while True:
      rready, wready, xready = select.select(readfds, [], [])
      for sock in rready:
        if sock is server_sock:
          conn, address = server_sock.accept()
          readfds.add(conn)
        else:
          msg = sock.recv(bufsize)
          if len(msg) == 0:
            sock.close()
            readfds.remove(sock)
          else:
            print(msg.decode('utf-8'))
            sock.send(msg)
  finally:
    for sock in readfds:
      sock.close()
  return
"""

class Checker:
    def EIforderCheck():
        if os.path.exists("../Fpool") == False:
            os.mkdir("../Fpool")

class IOcontrol:    #ファイル入出力
    def DExpt(FName, writeV):    #ファイル出力
        Checker.EIforderCheck()
        print('test')
        #出力ファイル生成
        if FName[0] == '-':
            f = open('../Fpool/RSL%s'% FName, 'w')
            f.write("%s" % writeV)
            f.close()


    def DInpt(FName):     #ファイル読込み
        Checker.EIforderCheck()
        Gret = None

        #SV生成ファイルの読み込み
        if FName[0] == 'E':
            f = open('../Fpool/%s'% FName, 'r')
            for Inpt in f:
                Gret =Inpt#f#.strip()    #SVからの返事を格納
            f.close()

        #使用済みファイルのリネーム
        if FName[0] != '-':
            rFName = '-' + FName
            os.rename('../Fpool/%s'% FName , '../Fpool/%s'% rFName)
        #elif FName[0] == '-':
        #    os.remove('../Fpool/%s' % FName)

        return Gret

    def DSearch():
        Checker.EIforderCheck()

        SearchFile = os.listdir('../Fpool/')

        rslLen = len(SearchFile)
        if rslLen == 0:
            return False
        else:
            return SearchFile[0]

def main():
    r = redis.Redis(host='localhost', port=6379, db=15)

    while True:
        FName = IOcontrol.DSearch()
        if FName == False:
            continue
        else:
            GetCLreq = IOcontrol.DInpt(FName)

        if GetCLreq != None:
            CLreq = GetCLreq.split()

            if CLreq[0] == '1':
                result = '1'#r.set(CLreq[1], CLreq[2])

                IOcontrol.DExpt(FName, result)
                continue

            elif CLreq[0] == '2':
                print('test')
                result = '2'#r.exists(CLreq[1])

                IOcontrol.DExpt(FName, result)
                continue

            elif CLreq[0] == '3':
                result = '3'#r.delete(CLreq[1])

                IOcontrol.DExpt(FName, result)
                continue


if __name__ == '__main__':
    main()

