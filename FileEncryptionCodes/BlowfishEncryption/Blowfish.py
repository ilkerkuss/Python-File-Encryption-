#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
from Crypto import Random


def encrypt(key, filename):
    buffersize = 64 * 1024
    outputFile = "(encrypted)" + filename
    filesize = str(os.path.getsize(filename)).zfill(8)
    IV = Random.new().read(8)

    encryptor = Blowfish.new(key, Blowfish.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(buffersize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 8 != 0:
                    chunk += b' ' * (8 - (len(chunk) % 8))

                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    buffersize = 64 * 1024
    outputFile = filename[11:]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(8))
        IV = infile.read(8)

        decryptor = Blowfish.new(key, Blowfish.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(buffersize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


def Main():
    choice = raw_input("Yapılacak İşlemi giriniz ((E)ncrypt veya (D)ecrypt) : ")

    if (choice == 'E'):
        filename = raw_input("Şifrelenecek Dosya Adı: ")
        password = raw_input("Parola: ")
        encrypt(getKey(password), filename)
        print("İşlem Başarılı.")
    elif (choice == 'D'):
        filename = raw_input("Çözümlenecek Dosya Adı: ")
        password = raw_input("Parola: ")
        decrypt(getKey(password), filename)
        print("İşlem Başarılı.")
    else:
        print("Yanlış girdi yapıldı program sonlandırılıyor...")


if __name__ == '__main__':
    Main()


