import os

from typing import List

import pandas as pd


# column's order: rsid, chromosome, position, result

FILE_TYPES = ('txt', 'csv')


def find_dna_files(file_types) -> List:
    all_files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    dna_files = []
    for f in all_files:
        if f.lower().endswith(file_types):
            dna_files.append(f)
    return dna_files


def clean_my_heritage(d):
    data = pd.read_csv(d, dtype=str, index_col=False, comment="#")
    # counted = data['CHROMOSOME'].value_counts()
    # print(counted.sort_index())
    data.columns = ['rsid', 'chromosome', 'position', 'result']
    return data


def clean_ancestry(d):
    data = pd.read_csv(d, dtype=str, sep='\t', comment="#")
    data["result"] = data["allele1"] + data["allele2"]
    del data['allele1']
    del data['allele2']
    data.loc[data.chromosome == '23', 'chromosome'] = 'X'
    data.loc[data.chromosome == '24', 'chromosome'] = 'Y'
    data.loc[data.chromosome == '25', 'chromosome'] = 'X'
    data.loc[data.chromosome == '26', 'chromosome'] = 'mt'
    counted = data['chromosome'].value_counts()
    print(counted.sort_index())
    print(counted.sort_index().to_dict())
    return data


if __name__ == "__main__":
    dna_files = find_dna_files(FILE_TYPES)
    for d in dna_files:
        if 'MyHeritage' in d:
            print("My Heritage:")
            my_heritage = clean_my_heritage(d)
            print(my_heritage)
        if 'Ancestry' in d:
            print("Ancestry:")
            ancestry = clean_ancestry(d)
        if 'genome' in d:
            print("23 and me:")
    merged = pd.merge(left=my_heritage,right=ancestry,on=('rsid','chromosome'),how='inner')
    print(merged)
