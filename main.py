########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/04/2020
#
#   PROGRAM STEPS
#   ) Set Current path
#   ) Import the following from config_default.json:
#       - data_dir:     Directory housing generated child-directories
#       - report_name:  File name of generated report
#       - report_ext:   File extension of generated report
#       - data_sheets:  Dictionary of sheets to use, each containing a list of required info
#       - data_columns: List of required columns in extracted data
#   ) Construct dir paths
#   ) Get list of all generated child directories
#   ) Create empty master DataFrame
#   ) For each report in directory
#   )   Create pandas ExcelFile object
#   )   For each required sheet
#   )       Create temp_data_df DataFrame from sheet
#   )       Extract specific data slice from DataFrame
#   )       Append data to master table
#
########################################################################################################################


class DataExport:

    def __init__(self, export_dir: str, export_file_nm: str, export_file_ext: str, export_data):
        self.export_dir = export_dir
        self.export_file_nm = export_file_nm
        self.export_data = export_data
        self.export_file_ext = export_file_ext

    def export(self):
        self.export_data.to_excel(f"{self.export_file_nm}.{self.export_file_ext}")


if __name__ == "__main__":
    pass
