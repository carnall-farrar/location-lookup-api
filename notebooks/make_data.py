import pandas as pd

# Load data
def load_data():
    ccg19 = pd.read_csv('notebooks/data/ccg_2019.csv')
    ccg19 = ccg19[['CCG19CDH', 'CCG19NM', 'STP19CD', 'STP19NM']] \
            .rename(columns = {'CCG19CDH': 'ccg_code', 'CCG19NM': 'ccg_name', 'STP19CD': 'stp_code', 'STP19NM':'stp_name'})
    ccg19['file'] = '2019 CCGs'

    ccg20 = pd.read_csv('notebooks/data/ccg_2020.csv')
    ccg20 = ccg20[['CCG20CDH', 'CCG20NM', 'STP20CD', 'STP20NM']] \
            .rename(columns = {'CCG20CDH': 'ccg_code', 'CCG20NM': 'ccg_name', 'STP20CD': 'stp_code', 'STP20NM':'stp_name'})
    ccg20['file'] = '2020 CCGs'

    ccg21 = pd.read_csv('notebooks/data/ccg_2021.csv')
    ccg21 = ccg21[['CCG21CDH', 'CCG21NM', 'STP21CD', 'STP21NM']] \
            .rename(columns = {'CCG21CDH': 'ccg_code', 'CCG21NM': 'ccg_name', 'STP21CD': 'stp_code', 'STP21NM':'stp_name'})
    ccg21['file'] = '2021 CCGs'

    stp = pd.read_csv('notebooks/data/stp_region_2020.csv')

    return ccg19, ccg20, ccg21, stp

# Concat ccg data
def concat_ccgs(ccg19, ccg20, ccg21):
    ccg_concat = pd.concat([ccg19, ccg20, ccg21])
    return ccg_concat

# Clean CCG data
def clean_ccg_data(ccg_concat):
    ccg_concat.stp_code = ccg_concat.stp_code.replace('E54000005', 'E54000054')
    ccg_concat.stp_code = ccg_concat.stp_code.replace('E54000006', 'E54000051')
    ccg_concat.stp_code = ccg_concat.stp_code.replace('E54000033', 'E54000053')
    ccg_concat.stp_code = ccg_concat.stp_code.replace('E54000035', 'E54000052')
    ccg_concat.stp_code = ccg_concat.stp_code.replace('E54000049', 'E54000050')

    ccg_concat = ccg_concat.drop_duplicates(subset=['ccg_code', 'ccg_name', 'stp_code', 'stp_name'])
    return ccg_concat

# Merge and clean 
def merge_stp_data(stp, ccg_concat):
    end_lookup = ccg_concat.merge(stp, left_on='stp_code', right_on='STP20CD', how='left')

    end_lookup.stp_name = end_lookup.stp_name.replace('Cornwall and the Isles of Scilly Health and Social Care Partnership', 'Cornwall and the Isles of Scilly')
    end_lookup.stp_name = end_lookup.stp_name.replace('Frimley Health and Care ICS', 'Frimley Health')
    end_lookup.stp_name = end_lookup.stp_name.replace('Surrey Heartlands Health and Care Partnership', 'Surrey Heartlands')
    end_lookup.stp_name = end_lookup.stp_name.replace('Sussex and East Surrey Health and Care Partnership', 'Sussex Health and Care Partnership')
    end_lookup.stp_name = end_lookup.stp_name.replace('Sussex and East Surrey', 'Sussex Health and Care Partnership')

    return end_lookup

# Export
def export_result_data(end_lookup):
    end_lookup.to_csv('server/data/combined_lookup.csv', sep="|")


if __name__ == '__main__':
    ccg_19, ccg_20, ccg_21, stp = load_data()
    ccgs = concat_ccgs(ccg19=ccg_19, ccg20=ccg_20, ccg21=ccg_21)
    clean_ccgs = clean_ccg_data(ccgs)
    result = merge_stp_data(stp, clean_ccgs)
    export_result_data(result)
