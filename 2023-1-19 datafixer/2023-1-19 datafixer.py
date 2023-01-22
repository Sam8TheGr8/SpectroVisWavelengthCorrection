import pandas as pd

#Read a csv file as raw input data. Input has a wavelength column, several columns of absorbance data, a second wavelength that almost lines up with the first one, and several more columns of wavelength data
raw_data = pd.read_csv("2023-1-19 chemdata.csv")

"""
General flow:
    -get a datapoint from one of the columns using the second wavelength
    -determine which value from the column of first wavelengths it is closest to (will always be further down)
    -Use the data point and the point after or before it to give a weighted average and get to that point
"""

#How many columns of good data (don't include the wavelength column)
COLUMNS_TO_KEEP = 9
#How many columns of data with wrong wavelengths
COLUMNS_TO_REPLACE = 9

working_data = raw_data.iloc[:,:COLUMNS_TO_KEEP+1]

for c in range(COLUMNS_TO_REPLACE):
    working_column = raw_data.columns[c + COLUMNS_TO_KEEP + 2]
    working_data.assign(col_name = working_column)
    for row_index in range(1, len(raw_data[working_column]) - 1):
        n = row_index
        point = raw_data[working_column][row_index]
        given_wavelength = raw_data["More Wavelength"][row_index]
        while raw_data["wavelength (nm)"][n] < given_wavelength:
            alternate_wavelength_low = raw_data["wavelength (nm)"][n]
            n += 1
        alternate_wavelength_high = raw_data["wavelength (nm)"][n]
        dif_low_given = given_wavelength - alternate_wavelength_low
        dif_high_given = alternate_wavelength_high - given_wavelength
    
        if dif_low_given <= dif_high_given:
            #use low. Recall that alt high and low were grabbed using n values that we can still access
            #factor is the fraction of the way down that the alternate is
            factor = (given_wavelength - alternate_wavelength_low) / (given_wavelength - raw_data["More Wavelength"][row_index-1])
            #take average of two absorbances, weighting based on the calculated factor
            weighted_absorbance = (raw_data[working_column][row_index]*(1-factor) + raw_data[working_column][row_index-1]*(factor))
            #print(alternate_wavelength_low, end=' | ')
            used_wavelength = alternate_wavelength_low
            used_row = n - 1

        else:
            #now factor is the fraction of the way up that the alternate is
            factor = -1 * (given_wavelength - alternate_wavelength_high) / (raw_data["More Wavelength"][row_index+1] - given_wavelength)
            weighted_absorbance = (raw_data[working_column][row_index]*(1-factor) + raw_data[working_column][row_index+1]*(factor))
            #print(alternate_wavelength_high, end=' || ')
            used_wavelength = alternate_wavelength_high
            used_row = n
        
        working_data.at[used_row, working_column] = weighted_absorbance

        #print("possibilities: ", alternate_wavelength_low, " and ", alternate_wavelength_high, " | ", row_index, ': ', weighted_absorbance)
        #input()
        print(used_wavelength, " ", used_row)
working_data.to_csv("Test Output.csv")