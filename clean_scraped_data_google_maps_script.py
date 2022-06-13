import numpy as np
import pandas as pd

class clean_data:
    filter_keywords = {}
    desirable_headings = []

    def __init__(self, file_name):
        self.file_name = file_name

        file = open(file_name)
        row_delimiter = "\n"
        column_delimiter = "\t"
        rows = []

        for line in file:
            rows.append(line.strip(row_delimiter))
        for column in range(len(rows)):
            rows[column] = rows[column].split(column_delimiter)
        self.matrix = np.array(rows)

    def find_heading_index(self, heading):
        heading_tuple = np.where(self.matrix[0] == heading)
        heading_index = heading_tuple[0]

        return heading_index

    def remove_empty_headings(self, heading_row = 0):
        position_of_empty_headings = []

        for column in range(len(self.matrix[heading_row])):
            if not self.matrix[heading_row, column]: position_of_empty_headings.append(column)
        self.matrix = np.delete(self.matrix, position_of_empty_headings, axis = 1)

    def remove_undesirable_rows_by_filter(self):
        places_to_remove = []
        heading_row = 0
        title_column = self.find_heading_index("title")
        category_column = self.find_heading_index("category")

        for row in range(heading_row + 1, len(self.matrix)):

            title_words = self.matrix[row, title_column][0].lower().split()
            category_words = self.matrix[row, category_column][0].lower().split()
            identifiers = set(title_words + category_words)

            #checks to see if there is an overlap
            if self.filter_keywords.isdisjoint(identifiers): 
                places_to_remove.append(row)

        self.matrix = np.delete(self.matrix, places_to_remove, axis = 0)

    def remove_undesirable_headings(self):
        """
        this function will also place the headings in the exact order of desirable_headings
        """
        self.desirable_headings = list(map(self.find_heading_index, self.desirable_headings))
        first_column = 0
        second_column = 1
        matrix_in_new_order = self.matrix[:, self.desirable_headings[first_column]] #starts matrix off as the first column 

        for column in range(second_column, len(self.desirable_headings)):
            matrix_in_new_order = np.concatenate((matrix_in_new_order, self.matrix[:, self.desirable_headings[column]]), axis = 1)
        self.matrix = matrix_in_new_order
    
    def standardize_text_to_title_format(self, heading):
        heading_column = self.find_heading_index(heading)

        for row in range(len(self.matrix)):
            self.matrix[row, heading_column] = self.matrix[row, heading_column][0].lower().title()

    def convert_column_to_data_type(self, heading, data_type):
        rating_column = self.find_heading_index(heading)
        for row in range(len(self.matrix)):
            try:
                self.matrix[row, rating_column] = data_type(self.matrix[row, rating_column])
            except:
                continue
    
    def replace_string_with(self, column = "address", old = ", ", new = " - "):
        """
        commas in the address can cause problems with CSV files
        """
        column_index = self.find_heading_index(column)

        for row in range(len(self.matrix)):
            try:
                self.matrix[row, column_index] = self.matrix[row, column_index][0].replace(old, new)
            except:
                continue
    
    def convert_array_to_data_frame(self):
        self.data_frame = pd.DataFrame(self.matrix)
    
    def save_data_frame_as_csv(self):
        self.data_frame.to_csv(f"cleaned_{self.file_name}.csv", index=False)

data_base = clean_data("tattoo_sample.txt")
data_base.remove_empty_headings()
data_base.filter_keywords = {"tattoo" , "ink"}
data_base.remove_undesirable_rows_by_filter()
data_base.desirable_headings = ["title", "rating", "reviewCount", "website", "phoneNumber", "address", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
data_base.remove_undesirable_headings()
data_base.standardize_text_to_title_format("title")
data_base.convert_column_to_data_type("rating", float)
data_base.convert_column_to_data_type("reviewCount", int)
data_base.replace_string_with("address", ", ", " - ")
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
for day in days:
    data_base.replace_string_with(day, "â€“", " - ")
data_base.convert_array_to_data_frame()
data_base.save_data_frame_as_csv()
print(data_base.matrix)