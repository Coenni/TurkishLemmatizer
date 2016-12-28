import sys
import traceback
from lemmatizer import Lemmatizer


'''
    Copyright 2011, 2013 Baturman SEN
    Reimplemention with Python Nijat Suleymanov Coenni

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

'''
    Testing lemmatizing
'''
def main():
    try:
        lemmatizer = Lemmatizer()

        lemmatizer.add_stem("kitap");
        lemmatizer.add_stem("kulak");
        lemmatizer.add_stem("ağaç");
        lemmatizer.add_stem("yemek");
        lemmatizer.add_stem("kalp");
        lemmatizer.add_stem("çelenk");
        lemmatizer.add_stem("metot");
        lemmatizer.add_stem("hukuk");
        lemmatizer.add_stem("genç");
        lemmatizer.add_stem("et");
        lemmatizer.add_stem("bekle");
        lemmatizer.add_stem("kal");
        lemmatizer.add_stem("özle");
        lemmatizer.add_stem("solla");
        lemmatizer.add_stem("de");
        lemmatizer.add_stem("ye");
        lemmatizer.add_stem("oğul");
        lemmatizer.add_stem("gönül");
        lemmatizer.add_stem("küçük");
        lemmatizer.add_stem("nesil");
        lemmatizer.add_stem("resim");
        lemmatizer.add_stem("resmi");
        lemmatizer.add_stem("alçak");
        lemmatizer.add_stem("yüksek");
        lemmatizer.add_stem("seyrek");
        lemmatizer.add_stem("seyir");
        lemmatizer.add_stem("af");
        lemmatizer.add_stem("zan");
        lemmatizer.add_stem("sağlam");
        lemmatizer.add_stem("kırmızı");
        lemmatizer.add_stem("yeşil");
        lemmatizer.add_stem("sarı");
        lemmatizer.add_stem("karın");
        lemmatizer.add_stem("hastane");
        lemmatizer.add_stem("baş");
        lemmatizer.add_stem("başbakan");
        lemmatizer.add_stem("elazığ");
        lemmatizer.add_stem("koğuş");
        lemmatizer.add_stem("sabır");
        lemmatizer.add_stem("kork");
        lemmatizer.add_stem("sen");
        lemmatizer.add_stem("bahçe");

        words = [
            "kitabım", "kulağım", "ağacımız", "yemeğe",
                 "kalbim"
            , "çelengi", "metodumuzu", "hukukun", "hukuğun",
                "gencecik", "ediliyor",
                "bekliyor", "kalmıyor", "özlüyorum", "solluyorum", "solladım", "diyorum", "diyerek", "deyince",
                "yiyerek", "yedirdi", "oğlum", "gönlüm",
                "küçüğüm", "neslimiz", "resminde", "resmi", "küçücük", "alçalmak", "yükselmek", "seyreldi", "seyrettim",
                "affetmek", "zannedersen", "sapasağlam",
                "kıpkırmızı", "yemyeşil"
            , "sarardım", "sapsarı", "karnından", "karındaş", "hastanelik", "başından",
                "başbakanın", "elazığlı", "koğuşunda", "sabrım",
                "sabreden", "korktu", "sana", "bahçesi"
                ]
        words_len = len(words)
        for i in range(0, words_len):
            message = words[i] + ' = '
            print('lemmatizing -> '+words[i])
            default_stem = lemmatizer.lemmatize(words[i])
            message += default_stem
            list = lemmatizer.get_all_candidates()
            if len(list) > 1:
                list_len = len(list)
                message += ' -> '
                for j in range(0, list_len):
                    message += list[j] + ' '
            message += '\n'
            message += lemmatizer.get_trace()
            print(message)
            print()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()

if __name__ == '__main__':
    main()