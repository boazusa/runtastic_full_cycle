# Main Python script.

from Runtastic_Selenium import Selenium_Runtastic, args_parser
from runtastic_analysis import runtastic_data_filter, Runtastic_Data_To_Csv, OUTPUT_DIR_LOCATION


def main():
    args = args_parser.get_args()
    test = Selenium_Runtastic(args.email, args.password)
    file_path = test.export_and_download_activities()

    if file_path:
        analyze_data = Runtastic_Data_To_Csv(_files_path=file_path, _output_path=OUTPUT_DIR_LOCATION)
        analyze_data.execute(mode=0)
        #
        plot_data = runtastic_data_filter(_files_path=file_path, _output_path=OUTPUT_DIR_LOCATION)
        plot_data.create_main_dataframe()
        #
        print(plot_data.plot_all())
        #
        print(plot_data.plot_yearly_activity(2022))
        print(plot_data.plot_yearly_activity(2023))
        print(plot_data.plot_yearly_activity(2024))
        print(plot_data.plot_yearly_activity(2025))
        #
        print(analyze_data)
        print(plot_data.create_main_dataframe())
    else:
        # print(f"file_path: {file_path}")
        analyze_data = Runtastic_Data_To_Csv(_files_path=r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC"
                                                         r"\export-20250304-000\Sport-sessions\\",
                                             _output_path=r"analysis\\")
        analyze_data.execute(mode=0)
        test = runtastic_data_filter(r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20250304-000"
                                     r"\Sport-sessions\\", "plots")
        test.create_main_dataframe()
        print(test)
        test.plot_all()
        #
        # additional
        print(test.plot_yearly_activity(2022))
        print(test.plot_yearly_activity(2023))
        print(test.plot_yearly_activity(2024))
        print(test.plot_yearly_activity(2025))


if __name__ == '__main__':
    main()
