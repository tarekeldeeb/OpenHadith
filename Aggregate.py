# !/usr/bin/env python

'''
    NAME    : Hadith Dataset
    Author  : Tarek Eldeeb
'''

import argparse
import fnmatch
import os
from os import path


def aggregate():
    dict_to_arabic = {
        "Musnad_Ahmad_Ibn-Hanbal": "مسند_أحمد",
        "Sahih_Al-Bukhari": "صحيح_البخاري",
        "Sunan_Abu-Dawud": "سنن_أبو_داود",
        "Sunan_Al-Nasai": "سنن_النسائي",
        "Sunan_Ibn-Maja": "سنن_ابن_ماجة",
        "Maliks_Muwataa": "موطأ_مالك",
        "Sahih_Muslim": "صحيح_مسلم",
        "Sunan_Al-Darimi": "سنن_الدارمي",
        "Sunan_Al-Tirmidhi": "سنن_الترمذي"}
    file_patterns = {"NoTashkeel": "*ahadith.utf8.csv", "Tashkeel": "*mushakkala*.csv"}
    for outFile in file_patterns:
        counter = 1
        aggregate_out_name = "All-" + outFile + ".csv"
        print("Generating %s .." % aggregate_out_name)
        aggregate_out = open(aggregate_out_name, "w")
        data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Open-Hadith-Data")
        for root, _, filenames in os.walk(data_folder):
            for filename in fnmatch.filter(filenames, file_patterns[outFile]):
                book_name = root.split(os.path.sep)[-1]
                with open(path.join(data_folder, path.join(book_name, filename)), encoding="utf8") as f:
                    for line in f:
                        if len(line) > 1:
                            line = str(counter) + "," + dict_to_arabic[book_name] + "," + line
                            counter = counter + 1
                            aggregate_out.write(line)
        aggregate_out.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    aggregate()
    print("Completed")
