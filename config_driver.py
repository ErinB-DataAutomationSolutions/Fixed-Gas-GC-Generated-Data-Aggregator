########################################################################################################################
#
#   PROGRAM:            Rob's Data Grabber
#   FILE:               main.pu
#   FILE PURPOSE:       Run main script of program
#   Author:             Erin Bryson
#   DATE LAST MODIFIED: 12/04/2020
#
#   DESCRIPTION:
#       This file is used to test the Config class
#
########################################################################################################################

from support.datasheet import Config

filename = "support\\config.json"

config = Config(filename)

print(config)
