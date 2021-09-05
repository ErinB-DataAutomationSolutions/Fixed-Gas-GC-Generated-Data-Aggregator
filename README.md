# Fixed Gas GC Generated Data Aggregator
This program will be used to collect, clean, and aggregate sample data obtained through a Fixed Gas GC machine. 

Required Libraries to be PIP Installed:
- Pandas

JSON config file structure and definitions:
- <b>Report Name:</b> Data file name
- <b>Report Ext:</b> Data file extension
- <b>DataSheets:</b>:
    - <b>Headers Bool</b>: If <i>TRUE</i>, import data from specified columns. If <i>FALSE</i>, import data form all 
    columns
    - <b>Headers NM:</b> Columns to import data from, if required
    - <b>Transpose Bool:</b> If <i>TRUE</i>, transpose imported data.
    - <b>Data Map:</b> Data dictionary that maps existing data labels to desired export-table column names
