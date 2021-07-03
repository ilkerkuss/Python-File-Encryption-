#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyAesCrypt
import os
import os.path
bufferSize = 64 * 1024  #64kbuffer size

def ana_menu():
    if(os.path.exists('pssw.txt')==False):
        f = open('pssw.txt', 'w')
        password = input("Lütfen şifrenizi belrleyiniz:")
        f.write(password)
        f.close()
    else:
        password=input("Şifrenizi Girin :")
        f=open("pssw.txt","r")
        ch_psw=f.read()
        f.close()

        if(password==ch_psw):
            print("şifre doğru :)")

            def menu():

                girdi = input("Yapılacak işlemi giriniz ((E)ncryption - (D)ecryption - (Ç)ıkış):")

                return girdi

            while (1):
                girdi = menu()

                if (girdi == "E" or girdi == "e"):
                    filepath = input("gir")
                    pyAesCrypt.encryptFile(filepath, filepath + ".aes", password, bufferSize)

                elif (girdi == "D" or girdi == "d"):
                    filepath = input("gir")

                    string = filepath
                    list = string.rsplit('\\', -1)
                    filename = list[-1]
                    dest = ''
                    for i in range(0, len(list) - 1):
                        dest = dest + list[i] + '\\'

                    pyAesCrypt.decryptFile(filepath + ".aes", dest + "2" + filename, password, bufferSize)

                elif(girdi=="Ç" or  girdi=="ç"):
                    exit()

                else:
                    print("Yanlış Karakter Girildi.")
                    continue
        else:
            print("!!! şifre hatalı program sonlandırılıyor !!!")



ana_menu()
