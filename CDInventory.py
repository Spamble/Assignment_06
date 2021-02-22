#------------------------------------------#
# Title: CDInventory.py
# Desc: Program loads CD Inventory from file and allows user to add, delete,
# display or save data to file in 2d table (list of dictionaries).
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# BEagle-Jack, 2021-Feb-17, Added function for writing to file
# BEagle-Jack, 2021-Feb-18, Added function for input new inventory 
# BEagle-Jack, 2021-Feb-18, Added function to add new inventory to table
# BEagle-Jack, 2021-Feb-19, Added function for deleting line
# BEagle-Jack, 2021-Feb-21, changed title and description
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to and from temporary memory"""
    
    @staticmethod
    def add_inventory(cd_id, cd_title, cd_artist, table):
        """Function to add CD inventory to 2D table
        
        Converts cd_id to integer from string input. Creates a dictionary by assigning 
        arguments to values in key-value pairs and appends dictionary to the list 
        of dictionaries that is available to user during runtime. Displays 2D table.
        
        Args: 
            cd_id (string): value for key ID to be put in dictionary
            cd_title (string): value for key Title to be put in dictionary
            cd_artist (string): value for key Artist to be put in dictionary
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns: 
            None.       
        """
        try: 
            intID = int(cd_id)
            dicRow = {'ID': intID, 'Title': cd_title, 'Artist': cd_artist}
            table.append(dicRow)
        except: 
            print('ID must be an integer.')
        IO.show_inventory(table)
    
    @staticmethod    
    def del_id(id_num, table):
        """Function to delete a line of CD inventory from 2D table 
        
        Iterates through list of dictionaries and iterates through dictionary values
        with 'ID' key to check for input by user. If line_num matches value of 'ID'
        key then entire dictionary is removed from list and displays confirmed deletion. 
        Otherwise prints that inventory dictionary was not removed.
        
        Args:
            line_num (int): 
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == id_num:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Function that writes list of dictionaries to file
        
        Args:
            file_name (string): name of file used to write data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_inventory():
        """Function to gather inputs from user for CD inventory creation
        
        Args:
            None.
            
        Returns:
            strID (string): string stripped of new line for user input of CD ID
            strTitle (string): string stripped of new line for user input of CD Ttile
            strArtist (string): string stripped of new line for user input of CD Artist
        
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist
    
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        cdValues = IO.input_inventory()
        # 3.3.2 Add item to the table
        DataProcessor.add_inventory(cdValues[0], cdValues[1], cdValues[2], lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_id(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




