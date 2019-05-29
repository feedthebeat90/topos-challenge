# topos-challenge
Scraper for Wikipedia Tables

In order to complete the following challenge I based my work on the following repository by rocheio:

https://github.com/rocheio

(See LICENSE file attach for Copyright purposes)

-----------------------------------------------------------------------------------------------------------------------------------

Installation
This is a Python 3 module that depends on the Beautiful Soup and requests packages.

### Create and activate a virtualenv for Python 3
python3 -m venv venv
. venv/bin/activate

### Install requirements from pip
pip install -r requirements.txt

------------------------------------------------------------------------------------------------------------------------------------

While scraping Wikipedia tables with Python there are several challenges that need to be addressed, 
such as:

- Handling multiple tables in an article 
- Data cells that span multiple rows
- Removing footnotes from cells.

(See https://roche.io/2016/05/scrape-wikipedia-with-python)

The aforementioned challenges are taken into consideration in "wikitablescrape.py"

However, Topos Assignment involved reading a Wikipedia Table that had an additional characteristic:

- Some data Cells from the "Header Row" Span Multiple Subcolumns

To solve the additional requirement I added the following function:

def first_row_check(header):

    """
    This function checks whether there is a column in header row
    spanning multiple subcolumns under the same category. 
    If there is such a column this function will reapeat the header element
    for each one of the corresponding subcolumns.
    """

-------------------------------------------------------------------------------------------------------------------------------------

As an extension to the Challenge I looked a second table on wikipedia that included additional geographical information
(i.e. Area information splitted in land and water area by city and state).

I loaded both tables into Pandas Dataframes and performed a join between them. 
Implementation: DataMerge.ipynb
Output File: topos_table.csv






