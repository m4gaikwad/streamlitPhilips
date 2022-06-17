import pandas as pd
pd.set_option('display.max_colwidth', None)

def create_structured_dataframe(log_data_dict):
    # TODO: Add Columns/Headers accordingly
    er_df = pd.DataFrame(log_data_dict)
    return er_df

def create_log_report(df,logger):
    logger.warning(f"Total Rows structured: {len(df.index)}")
    logger.warning(df.head())

def convert_df_to_csv(df,file_name):
    df.to_csv(file_name, sep='\t')

def convert_df_to_excel(df,file_name):
    df.to_excel(file_name)

def filter_df_by_unit(df,unit='STAND',category=['Warning','Error']):
    unit_df = df.loc[(df.Unit == unit) & (df.EventCategory.isin(category))]
    return unit_df 

def get_version_from_meta(data_dict):
    if all(key in ['Version','Release','Level','Build'] for key in data_dict.keys()):
        version = data_dict['Release']+'.'+data_dict['Version']+'.'+data_dict['Level']+'.'+data_dict['Build']
    else:
        version = None
    return version