#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import  AES
from Crypto import Random
from Crypto.Hash import SHA256


def encryptsymmetrickey(password,pubkey):
    encryptor = PKCS1_v1_5.new(pubkey)
    encryptedSymmetricKey = encryptor.encrypt(password)
    return encryptedSymmetricKey


def decryptsymmetrickey(encryptedSymmetricKey,privkey):
    decryptor = PKCS1_v1_5.new(privkey)
    decryptedSymmetricKey = decryptor.decrypt(encryptedSymmetricKey, 'sentinel')
    return decryptedSymmetricKey


def ana_menu():

    if (os.path.exists('pssw.txt') == False):
        f = open('pssw.txt', 'w')
        f1=open('pubkey.txt','w')
        f2=open('privkey.txt','w')
        f3=open('encryptedkey.txt','w')
        f4=open('decryptedkey.txt','w')
        password = raw_input("Lütfen şifrenizi belrleyiniz:")
        f.write(password)
        asykey = RSA.generate(2048)
        privkey = RSA.importKey(asykey.exportKey('DER'))
        pubkey = RSA.importKey(asykey.publickey().exportKey('DER'))

        f1.write(str(pubkey))
        f2.write(str(privkey))
        f3.write(encryptsymmetrickey(password,pubkey))
        f4.write(decryptsymmetrickey(encryptsymmetrickey(password,pubkey),privkey))
        f.close()
        f1.close()
        f2.close()
        f3.close()
        f4.close()
    else:
        password = raw_input("Şifrenizi Girin :")
        f = open("pssw.txt", "r")
        ch_psw = f.read()
        f.close()

        if (password == ch_psw):
            print("şifre doğru :)")



    def encrypt(key, filename):


        buffersize = 64 * 1024
        outputFile = "(encrypted)" + filename
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(16)

        encryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)

                while True:
                    chunk = infile.read(buffersize)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                    outfile.write(encryptor.encrypt(chunk))


    def decrypt(key, filename):


        buffersize = 64 * 1024
        outputFile = filename[11:]

        with open(filename, 'rb') as infile:
            filesize = int(infile.read(16))
            IV = infile.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

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
            f=open('pssw.txt','r')
            password=f.read()
            encrypt(getKey(password), filename)
            f.close()
            print("İşlem Başarılı.")
        elif (choice == 'D'):
            filename = raw_input("Çözümlenecek Dosya Adı: ")
            f=open('decryptedkey.txt','r')
            password=f.read()
            decrypt(getKey(password), filename)
            f.close()
            print("İşlem Başarılı.")
        else:
            print("Yanlış girdi yapıldı program sonlandırılıyor...")


    if __name__ == '__main__':
        Main()

ana_menu()