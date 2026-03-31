# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 14:30:48 2025

@author: ASUS
"""
a=int(input("Please enter a number: "))
b=int(input("Please enter a number: "))
if a==b:
    print("Congratulations you're number are same")
else:
    print("Unfortunately you're numbers aren't same,they're different")
    
#%%
sayi=int(input("Lutfen bir sayi giriniz: "))
liste=[]
for i in range(2,100):
    if sayi%i==0:
        liste.append(i)
print(liste)
#%%
sayi=2
liste=[]
for i in range(10):
    liste.append(sayi**i)
    
print(liste)
#%%
liste=[1,2,3,4,5,6,7,8,9]
a=int(input("Yazilmasini istemediginiz sayiyi giriniz: "))
for sayi in liste:
    if sayi==a:
        continue
    else:
        print(sayi)
#%%
liste=[1,2,3,4,5,6,7,8,9]
a=int(input("Yazilmasini istemediginiz sayiyi giriniz: "))
for sayi in liste:
    if sayi==a:
        break
    else:
        print(sayi)
#%%
sayi=int(input("Faktoriyelinin alinmasini istediginiz sayiyi giriniz: "))
sonuc=1
for i in range(1,sayi+1):
    sonuc*=i
print(f"Faktoriyelin sonucu {sonuc} degerine esittir.")
#%%
sayi=int(input("Lutfen kontrol edilmesini istediginiz sayiyi giriniz: "))
if sayi<1:
    print("Sayiniz asal degildir")
else:
    for i in range(2,sayi//2):
        if sayi%i==0:
            print("Sayiniz asal degildir.")
            break
    else:
        print("Sayiniz asaldir")
#%%
sayi=int(input("Lutfen bir sayi giriniz: "))
sayac=0
for i in range(1,sayi+1):
    if sayi%i==0:
        sayac+=1
print(f"Girdiginiz sayinin {sayac} kadar pozitif tam sayi boleni var")
#%%%
sayi=int(input("Lutfen bir sayi giriniz: "))
str_sayi=str(sayi)
toplam=0
for rakam in str_sayi:
    deger=int(rakam)
    toplam+=deger
print(f"Girilen sayinin rakamlari toplami {toplam} kadardir")
#%%
liste=[]
for sayi in range(0,5):
   sayi=int(input("Lutfen bir sayi giriniz: "))
   liste.append(sayi)
liste.sort()
print(liste)
print(max(liste))
print(min(liste))