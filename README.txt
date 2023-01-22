This is an (admittedly pretty lazy) attempt to produce a program that corrects for a quirk of SpectroVis photometers used in LoggerPro: under some circumstances, the wavelengths absorbance is measured at can get changed between samples, resulting in data that is difficult to compare. Such data is shown in sampledata.csv.

This program attempts to assign a standard set of wavelengths (leftmost column of a spreadsheet) to all absorbance values (past a column with the second, non-matching wavelengths), outputting the result as a csv file (sampledata.csv).

Two changeable variables in main.py allow the number of columns considered to be changed (see comments for more details).

I've had no issues with the code, but I'm not absolutely convinced that it works properly. Also, I fully recognize that the code is highly inefficient.