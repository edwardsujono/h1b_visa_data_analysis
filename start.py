from preprocessing.data_collection import DataCollector


if __name__ == "__main__":

    data_collector = DataCollector(is_read_clean_data=True)
    data_collector.start_plot_each_year_data()
