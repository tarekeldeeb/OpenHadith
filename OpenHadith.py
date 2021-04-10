# !/usr/bin/env python

"""
    NAME    : Open Hadith Dataset
    Author  : Tarek Eldeeb
"""
import argparse
from fnmatch import filter
from os import path, walk
import pandas as pd
from MyTimer import Timer

__version__: str = '0.1'
__author__ = 'Tarek Eldeeb'

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

dict_to_long = {
    "han": "Musnad_Ahmad_Ibn-Hanbal",
    "buk": "Sahih_Al-Bukhari",
    "daw": "Sunan_Abu-Dawud",
    "nas": "Sunan_Al-Nasai",
    "maj": "Sunan_Ibn-Maja",
    "mal": "Maliks_Muwataa",
    "mus": "Sahih_Muslim",
    "dar": "Sunan_Al-Darimi",
    "tir": "Sunan_Al-Tirmidhi"}

base_columns = ["فهرس", "كتاب", "فهرس_داخلي", "سند_ومتن"]

splitters = [['قال رسول الله صلى الله عليه وسلم', 51], ['صلى الله عليه وسلم قال', 50],
             ['أن النبي صلى الله عليه وسلم', 15], ['كان رسول الله صلى الله عليه وسلم', 10],
             ['صلى الله عليه وسلم يقول', 9], ['قال النبي صلى الله عليه وسلم', 7], ['قال صلى الله عليه وسلم', 1]]


def aggregate(books, sample):
    file_patterns = {"NoTashkeel": "*ahadith.utf8.csv", "Tashkeel": "*mushakkala*.csv"}
    books_long = [dict_to_long[x] for x in books]
    for outFile in file_patterns:
        counter = 1
        aggregate_out_name = "OpenHadith-" + outFile + ".csv"
        print("\nCreating %s .." % aggregate_out_name)
        aggregate_out = open(aggregate_out_name, "w")
        aggregate_out.write('{0}\n'.format(','.join(base_columns)))
        data_folder = path.join(path.dirname(path.realpath(__file__)), "Open-Hadith-Data")
        for root, _, filenames in walk(data_folder):
            for filename in filter(filenames, file_patterns[outFile]):
                book_name: str = root.split(path.sep)[-1]
                if book_name in books_long:
                    book_lines = 1
                    with open(path.join(data_folder, path.join(book_name, filename)), encoding="utf8") as f:
                        for line in f:
                            if sample is not None and sample < book_lines:
                                continue
                            if len(line) > 2:
                                line = str(counter) + "," + dict_to_arabic[book_name] + "," + line
                                counter = counter + 1
                                book_lines = book_lines + 1
                                aggregate_out.write(line)
                    print("  " + "{:5d}".format(book_lines - 1) + " hadith from " + book_name)
        aggregate_out.close()
        aggregated_files.append(aggregate_out_name)
    return


def print_books_list():
    print("Books\tDescription.")
    for book_shortname in dict_to_long:
        print(" %s\t %s" % (book_shortname, dict_to_long[book_shortname]))


def sm_split(full_hadith, index):
    for s in ['رسول الله', 'النبي', 'نبي الله']:
        if s in full_hadith:
            before, after = full_hadith.split(s, 1)
            if 'قال' in before:
                sanad = before.rsplit('قال', 1)[0]
                matn = before.rsplit('قال', 1)[1] + " " + s + " " + after
                return (s,) + (matn, sanad)
    print("Hadith %d was not split." % (index + 1))
    return " ", " ", " "


def process(files):
    print("\nProcessing file: %s .." % files[0])
    df = pd.read_csv(files[0])
    df['متن'] = ""
    df['مرفوع'] = ""
    df['سند'] = ""
    for row in splitters:
        row[1] = 0
    for i, fullHad in enumerate(df['سند_ومتن']):
        df.loc[i, 'مرفوع'], df.loc[i, 'متن'], df.loc[i, 'سند'] = sm_split(fullHad, i)
    df.to_csv(files[0], index=False, header=True)
    print('Splitters = \n %s' % sorted(splitters, key=lambda x: x[1], reverse=True))


def print_banner():
    banner = """   ___                                    _ _ _   _
  /___\\_ __   ___ _ __     /\\  /\\__ _  __| (_) |_| |__
 //  // '_ \\ / _ \\ '_ \\   / /_/ / _` |/ _` | | __| '_ \\
/ \\_//| |_) |  __/ | | | / __  / (_| | (_| | | |_| | | |
\\___/ | .__/ \\___|_| |_| \\/ /_/ \\__,_|\\__,_|_|\\__|_| |_|
      |_|   Github.com/TarekEldeeb/OpenHadith"""
    print(banner)
    print("\t\t\tVersion: " + __version__ + "\tLicense: Waqf 2.0")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open Hadith Data Aggregator and Processor Script")
    parser.add_argument("-b", "--books", type=str,
                        help="Comma-Separated list of books to be aggregated. Default (all).")
    parser.add_argument("-l", "--list-books", action='store_true',
                        help="List available books and exit.", default=False)
    parser.add_argument("--no-processing", action='store_true',
                        help="Do not process the aggregated files", default=False)
    parser.add_argument('--sample', nargs='?', const=10, type=int,
                        help="Include a sample only from each book. Default size 10.")
    args = vars(parser.parse_args())
    if args['list_books']:
        print_books_list()
        exit(0)
    if args["books"] is not None and args["books"].lower() != "all":
        args["books"] = [s.strip() for s in args["books"].split(",")]
        for b in args["books"]:  # Check if books exist
            if b not in dict_to_long:
                print("Unknown Book: %s, please use -l to list available books." % b)
                exit(-1)
    else:
        args["books"] = list(dict_to_long.keys())
    print_banner()
    aggregated_files = []
    aggregate(args["books"], args["sample"])
    args['no_processing'] and exit(0)
    with Timer('process(aggregated_files)'):
        process(aggregated_files)
