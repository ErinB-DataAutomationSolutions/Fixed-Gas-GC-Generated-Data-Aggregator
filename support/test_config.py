########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/20/2020
#
#   DESCRIPTION:
#       This file is used to test the Config class in library file data_upload.py
#
########################################################################################################################

# IMPORTS
import unittest as ut
from support.data_upload import Config

# Set Test Variables
config_file = "config_files\\config_default.json"    # Set filename
test_data_dir = "Data_Directories"
test_report_ext = "xls"

config = Config(config_file)            # Set config object


if __name__ == '__main__':
    ut.main()
