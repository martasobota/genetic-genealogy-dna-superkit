import os

from typing import List

import pandas as pd


# column's order: rsid, chromosome, position, result

FILE_TYPES = ('txt', 'csv')

replacement_values = {
    '00': '--',
    'CA': 'AC',
    'TA': 'AT',
    'TC': 'CT',
    'ID': 'DI',
    'GA': 'AG',
    'GC': 'CG',
    'TG': 'GT',
    'A': 'AA',
    'T': 'TT',
    'D': 'DD',
    'C': 'CC',
}


def find_dna_files(file_types) -> List:
    all_files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    dna_files = []
    for f in all_files:
        if f.lower().endswith(file_types):
            dna_files.append(f)
    return dna_files


def clean_ancestry(d):
    data = pd.read_csv(d, dtype=str, sep='\t', comment="#")
    data["result"] = data["allele1"] + data["allele2"]
    del data['allele1']
    del data['allele2']
    data.loc[data.chromosome == '23', 'chromosome'] = 'X'
    data.loc[data.chromosome == '24', 'chromosome'] = 'Y'
    data.loc[data.chromosome == '25', 'chromosome'] = 'X'
    data.loc[data.chromosome == '26', 'chromosome'] = 'mt'
    data['company'] = 'ancestry'
    # counted = data['chromosome'].value_counts()
    # print(counted.sort_index().to_dict())
    return data


def clean_23_and_me(d):
    data = pd.read_csv(d, dtype=str, sep='\t', comment="#", index_col=False, engine='python')
    data.columns = ['rsid', 'chromosome', 'position', 'result']
    data['company'] = '23andme'
    # counted = data['chromosome'].value_counts()
    # print(counted.sort_index().to_dict())
    # data.to_csv('23me.txt', sep='\t', index=None)
    # 23andme files require additonal data cleaning due to wrong position for inserted rsid's
    return data


def clean_my_heritage(d):
    data = pd.read_csv(d, dtype=str, comment="#")
    data.columns = ['rsid', 'chromosome', 'position', 'result']
    data['company'] = 'MH'
    # counted = data['chromosome'].value_counts()
    # print(counted.sort_index().to_dict())
    return data


if __name__ == "__main__":
    dna_files = find_dna_files(FILE_TYPES)
    result_files = []
    for f in dna_files:
        if 'Ancestry' in f:
            print("Ancestry")
            ancestry = clean_ancestry(f)
            result_files.append(ancestry)
        # if 'genome' in f:
        #     print("23 and me:")
        #     twentythree_and_me = clean_23_and_me(f)
        #     result_files.append(twentythree_and_me)
        if 'MyHeritage' in f:
            print("My Heritage:")
            my_heritage = clean_my_heritage(f)
            result_files.append(my_heritage)
        
    # print(df_final.drop_duplicates(subset=['position', 'chromosome'], keep=False))
    # print(df_final)

    merged = pd.merge(left=my_heritage, right=ancestry,on=('chromosome', 'position'), how='outer')
    merged.replace(to_replace=replacement_values, inplace=True)
    merged.to_csv('test.csv', sep='\t', index=None)
    
    # 1 Delete duplicates that matches on position and result (genome)
    
    