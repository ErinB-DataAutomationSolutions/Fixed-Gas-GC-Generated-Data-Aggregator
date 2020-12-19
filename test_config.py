########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/04/2020
#
#   DESCRIPTION:
#       This file is used to test the Config class in library file datasheet.py
#
########################################################################################################################

# IMPORTS
import unittest as ut
from support.datasheet import Config

# Set Test Variables
config_file = "support\\config.json"    # Set filename
test_data_dir = "Data_Directories"
test_report_ext = "xls"

config = Config(config_file)            # Set config object


class TestConfigImports(ut.TestCase):
    def test_data_dit(self):
        self.assertTrue(config.report_ext, test_report_ext)


if __name__ == '__main__':
    ut.main()
    pass
