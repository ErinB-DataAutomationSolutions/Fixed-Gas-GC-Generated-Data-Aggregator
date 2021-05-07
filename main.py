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

# IMPORTS
from support.data_upload import Config
from support.data_upload import DataSheet


# METHODS
def get_config_file_name() -> str:
    pass


def get_export_data_dir() -> str:
    pass


if __name__ == "__main__":
    pass
