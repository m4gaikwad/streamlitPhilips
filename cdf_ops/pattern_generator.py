import pandas as pd
import numpy as np
from collections import defaultdict
pd.set_option('display.max_colwidth', None)
pd.options.mode.chained_assignment = None


class PatternFinder():

    def cleaned_text(self,text):
        text = text.encode().decode("utf-8")
        text = text.lower()
        return text

    def preprocess_data(self,full_df):
        full_df.drop_duplicates()
        stand_df = full_df[['TimeStamp','TimeFraction','Unit','EventCategory','Description','FileName','Version','ProductID','SerialNumber']]
        stand_df["Cause"] = np.nan
        stand_df["Solution"] = np.nan
        stand_df['Description_clean'] = stand_df['Description'].apply(lambda x : self.cleaned_text(x))
        
        exclusion_list = ["OsaErrorCallback: Error","MergeCOM Error"]
        for term in exclusion_list:
            stand_df = stand_df[stand_df["Description_clean"].str.contains(term.lower())==False]        
        return stand_df

    def get_rows_by_error(self,df,error,n_rows=10):
        appended_data = []
        indexes = df[df['Description_clean'].str.contains(error)].index
        for idx in indexes:
            part_df = df.iloc[(max(df.index.get_loc(idx)-n_rows,0)):min(df.index.get_loc(idx)+n_rows,len(df))]
            appended_data.append(part_df)
        if appended_data:
            appended_data = pd.concat(appended_data)
            appended_data=appended_data.groupby(appended_data.index).first()
            return appended_data
        return None

    def sort_by_time(self, df):
        try:
            df['TimeStamp_full'] = df['TimeStamp'].str.cat(df['TimeFraction'], sep =":")
            df['Datetime_cleaned'] = pd.to_datetime(df['TimeStamp_full'], format="%Y-%m-%dT%H:%M:%S:%f")
            return df.sort_values(by='Datetime_cleaned')
        except:
            return None

    def filter_by_component(self, df,component="STAND"):
        try:
            return df.loc[df['Unit'] == component]
        except:
            return None

    def get_patterns(self, df):
        patterns = defaultdict(int)
        try:
            for row in df['Description']:
                if row not in patterns:
                    patterns[row] = 1
                else:
                    patterns[row] = patterns[row] + 1
            return sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        except:
            return None
    
    def find_patterns(self,df,error=None):
        stand_df = self.preprocess_data(df)
        if not error:
            error = "no x-ray after switch on"

        dose_df = self.get_rows_by_error(stand_df,error) # segment
        dose_time_df = self.sort_by_time(dose_df) # confirmation
        dose_rslt_df = self.filter_by_component(dose_time_df)
        return self.get_patterns(dose_rslt_df)
