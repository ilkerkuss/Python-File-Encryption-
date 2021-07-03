#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os



def ana_prog():
    if(os.path.exists('pubpssw.txt')==False):
        f1=open('pubpssw.txt','ab+')
        f2=open('privpssw.txt','ab+')
        key = RSA.generate(2048)
        privkey = RSA.importKey(key.exportKey("DER"))
        pubkey = RSA.importKey(key.publickey().exportKey("DER"))
        f2.write(key.export_key())
        f1.write(key.publickey().export_key())
        f1.close()
        f2.close()

        def Main():
            while True:
                choice = raw_input("Yapılacak İşlemi giriniz ((E)ncrypt veya (D)ecrypt) : ")

                if (choice == 'E'):
                    filename = raw_input("Şifrelenecek Dosya Adı: ")
                    encrypt(pubkey, filename)
                    print("İşlem Başarılı.")
                elif (choice == 'D'):
                    filename = raw_input("Çözümlenecek Dosya Adı: ")
                    decrypt(privkey, filename)
                    print("İşlem Başarılı.")
                else:
                    print("Yanlış girdi yapıldı program sonlandırılıyor...")
    else:
        f1 = open('pubpssw.txt', 'rb')
        f2 = open('privpssw.txt', 'rb')
        apub=f1.read()
        apriv=f2.read()
        f1.close()
        f2.close()

        def Main():
            while True:
                choice = raw_input("Yapılacak İşlemi giriniz ((E)ncrypt veya (D)ecrypt) : ")

                if (choice == 'E'):
                    filename = raw_input("Şifrelenecek Dosya Adı: ")
                    encrypt(RSA.import_key(apub), filename)
                    print("İşlem Başarılı.")
                elif (choice == 'D'):
                    filename = raw_input("Çözümlenecek Dosya Adı: ")
                    decrypt(RSA.import_key(apriv), filename)
                    print("İşlem Başarılı.")
                else:
                    print("Yanlış girdi yapıldı program sonlandırılıyor...")



    def encrypt(pubkey,filename):
        buffersize = 128*1024
        outputFile = "(encrypted)" + filename
        filesize = str(os.path.getsize(filename)).zfill(16)

        encryptor = PKCS1_v1_5.new(pubkey)


        with open(filename, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                while True:
                    chunk = infile.read(buffersize)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                    outfile.write(encryptor.encrypt(chunk))

    def decrypt(privkey,filename):
        buffersize = 128 * 1024
        outputFile = filename[11:]

        with open(filename, 'rb') as infile:
            filesize = int(infile.read(16))

            decryptor=PKCS1_v1_5.new(privkey)


            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(buffersize)

                    if len(chunk) == 0:
                        break

                    outfile.write(decryptor.decrypt(chunk,"sentinel"))
                outfile.truncate((filesize))



    if __name__ == '__main__':
        Main()

ana_prog()
