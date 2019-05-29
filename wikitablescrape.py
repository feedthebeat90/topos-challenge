"""Create CSVs from all tables on a Wikipedia article."""

import csv
import os

from bs4 import BeautifulSoup
import requests
from pprint import pprint


def scrape(url, output_name):
    """Create CSVs from all tables in a Wikipedia article.
    ARGS:
        url (str): The full URL of the Wikipedia article to scrape tables from.
        output_name (str): The base file name (without filepath) to write to.
    """

    # Read tables from Wikipedia article into list of HTML strings
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "lxml")
    table_classes = {"class": ["sortable", "plainrowheaders"]}
    wikitables = soup.findAll("table", table_classes)

    # Create folder for output if it doesn't exist
    os.makedirs(output_name, exist_ok=True)

    for index, table in enumerate(wikitables):
        # Make a unique file name for each CSV
        if index == 0:
            filename = output_name
        else:
            filename = output_name + "_" + str(index)

        filepath = os.path.join(output_name, filename) + ".csv"

        with open(filepath, mode="w", newline="", encoding="utf-8") as output:
            csv_writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator="\n")
            write_html_table_to_csv(table, csv_writer)

def first_row_check(header):
    """This function checks whether there is a column in header row
    spanning multiple subcolumns under the same category. 
    If there is such a column this function will reapeat the header element
    for each one of the corresponding subcolumns.
    
    ARGS:
        header (bs4.Tag): The bs4 Tag object being analyzed.
        
    RETURNS:
        cells (list): List of elements from bs4.ResultSet.
    
    """
    
    cells = []
    
    for elem in header.findAll(["th", "td"]):
        if elem.has_attr("colspan"):
            
            span = int(elem["colspan"])
            counter = 0 
            
            while counter < span:
                #pprint(vars(elem))
                cells.append(elem)
                counter += 1
        else:
            cells.append(elem)
    
    return cells


def write_html_table_to_csv(table, writer):
    """Write HTML table from Wikipedia to a CSV file.
    ARGS:
        table (bs4.Tag): The bs4 Tag object being analyzed.
        writer (csv.writer): The csv Writer object creating the output.
    """

    # Hold elements that span multiple rows in a list of
    # dictionaries that track 'rows_left' and 'value'
    first_row = True
    saved_rowspans = []
    for row in table.findAll("tr"):
        if first_row:
            cells = first_row_check(row)
            first_row = False
        else:
            cells = row.findAll(["th", "td"])


        # If the first row, use it to define width of table
        if len(saved_rowspans) == 0:
            saved_rowspans = [None for _ in cells]
        
        
        # Insert values from cells that span into this row
        elif len(cells) != len(saved_rowspans):
            for index, rowspan_data in enumerate(saved_rowspans):
                if rowspan_data is not None:
                    # Insert the data from previous row; decrement rows left
                    value = rowspan_data["value"]
                    cells.insert(index, value)

                    if saved_rowspans[index]["rows_left"] == 1:
                        saved_rowspans[index] = None
                    else:
                        saved_rowspans[index]["rows_left"] -= 1

        # If an element with rowspan, save it for future cells
        for index, cell in enumerate(cells):
            if cell.has_attr("rowspan"):
                rowspan_data = {"rows_left": int(cell["rowspan"]), "value": cell}
                saved_rowspans[index] = rowspan_data

        if cells:
            # Clean the data of references and unusual whitespace
            cleaned = clean_data(cells)

            # Fill the row with empty columns if some are missing
            # (Some HTML tables leave final empty cells without a <td> tag)
            columns_missing = len(saved_rowspans) - len(cleaned)
            if columns_missing:
                cleaned += [None] * columns_missing

            writer.writerow(cleaned)


def clean_data(row):
    """Clean table row list from Wikipedia into a string for CSV.
    ARGS:
        row (bs4.ResultSet): The bs4 result set being cleaned for output.
    RETURNS:
        cleaned_cells (list[str]): List of cleaned text items in this row.
    """

    cleaned_cells = []
    
    for cell in row:
        # Strip references from the cell
        references = cell.findAll("sup", {"class": "reference"})
        if references:
            for ref in references:
                ref.extract()

        # Strip sortkeys from the cell
        sortkeys = cell.findAll("span", {"class": "sortkey"})
        if sortkeys:
            for ref in sortkeys:
                ref.extract()

        # Strip footnotes from text and join into a single string
        text_items = cell.findAll(text=True)
        no_footnotes = [text for text in text_items if text[0] != "["]


        cleaned = (
            "".join(no_footnotes)  # Combine elements into single string
            .replace("\xa0", " ")  # Replace non-breaking spaces
            .replace("\n", " ")  # Replace newlines
            .strip()
        )

        cleaned_cells += [cleaned]

    return cleaned_cells
