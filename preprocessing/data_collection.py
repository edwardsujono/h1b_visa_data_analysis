import pandas_datareader as web
import pandas as pd
import datetime
from matplotlib import style
import matplotlib.pyplot as plt


class DataCollector:

    def __init__(self, is_read_clean_data):
        style.use('ggplot')
        if is_read_clean_data:

            self.df_clean = pd.read_csv(
                "/Users/edwardsujono/Python_Project/h1b_visa_analytic/data/clean_data.csv"
            )

        else:

            self.df = pd.read_csv(
                "/Users/edwardsujono/Python_Project/h1b_visa_analytic/data/h1b_kaggle.csv"
            )
            self.df_soc = pd.read_csv(
                "/Users/edwardsujono/Python_Project/h1b_visa_analytic/data/soc_code.csv"
            )

        return

    # this is for h1b case
    # need to remove the row with unecessary data
    def clean_data_from_h1b_csv(self):

        self.df.drop(self.df[self.df.CASE_STATUS == "WITHDRAWN"].index, inplace=True)
        self.df.drop("lon", 1, inplace=True)
        self.df.drop("lat", 1, inplace=True)

        # drop all the empty data
        self.df.drop(self.df[self.df.CASE_STATUS == ""].index, inplace=True)
        self.df.drop(self.df[self.df.EMPLOYER_NAME == ""].index, inplace=True)
        self.df.drop(self.df[self.df.SOC_NAME == ""].index, inplace=True)
        self.df.drop(self.df[self.df.JOB_TITLE == ""].index, inplace=True)
        self.df.drop(self.df[self.df.FULL_TIME_POSITION == ""].index, inplace=True)
        self.df.drop(self.df[self.df.PREVAILING_WAGE < 0].index, inplace=True)
        self.df.drop(self.df[self.df.WORKSITE == ""].index, inplace=True)

        # merge with the soc code
        result = pd.merge(self.df,  self.df_soc[["Code", "Title"]], left_on="SOC_NAME", right_on="Title", how="inner")

        result.to_csv("/Users/edwardsujono/Python_Project/h1b_visa_analytic/data/clean_data.csv")

    def start_plot_each_year_data(self):

        years = self.df_clean.groupby(["YEAR"]).mean().index.values
        datas = []
        statuses = ["CERTIFIED-WITHDRAWN", "CERTIFIED"]

        for year in years:
            datas.append([])

        for i in xrange(len(years)):
            for status in statuses:

                year_data = self.df_clean.YEAR == years[i]
                status_data = self.df_clean.CASE_STATUS == status

                combine_data = self.df_clean[year_data & status_data]
                datas[i].append(len(combine_data.index.values))

        plotting = pd.DataFrame(datas, index=years, columns=statuses)
        print datas
        plt.figure()
        plotting.plot()
