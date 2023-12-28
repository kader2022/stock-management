import ttkbootstrap as ttk
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from pathlib import Path
import mysql.connector

def connect():
    return mysql.connector.connect(host="localhost", user="root", password="", database="gestiondestock")

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

def insert(tree, table_name, columns,entrys, condition, width):
    values = []
    # Retrieve values from entry widgets
    values = [entry.get() for entry in entrys]

    # Format the list of columns to be included in the INSERT statement
    columns_str = ', '.join(f"`{column}`" for column in columns)
    # Format the list of values to be included in the INSERT statement
    values_str = ', '.join(f"'{value}'" for value in values)
    # Assemble the complete INSERT query
    query = f"INSERT INTO `{table_name}`({columns_str}) VALUES ({values_str})"
    # Execute the query
    db_connection = connect()
    cursor = db_connection.cursor()
    cursor.execute(query)
    db_connection.commit()
    close_connection(db_connection, cursor)

    # Update the Treeview to reflect the changes
    fetch(tree, table_name, columns, condition, width)

def fetch(tree, table_name, columns, condition, width):
    # Helper function to clear the Treeview
    def empty(tree):
        tree.delete(*tree.get_children())

    # Helper function to set up columns in the Treeview
    def setup_columns(tree, columns, width):
        tree["columns"] = columns
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=width)

    # Helper function to generate a read query
    def generate_read_query(table_name, columns, condition):
        columns_str = ', '.join(f"`{column}`" for column in columns)
        where_clause = f"WHERE {condition}"
        query = f"SELECT {columns_str} FROM `{table_name}` {where_clause}"
        return query

    # Clear existing items in the Treeview
    empty(tree)

    # Set up columns in the Treeview
    setup_columns(tree, columns, width)

    # Connect to the database and fetch data
    connection = connect()
    cursor = connection.cursor(dictionary=True)

    # Generate and execute the read query
    query = generate_read_query(table_name, columns, condition)
    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    close_connection(connection, cursor)

    # Insert data into the Treeview
    for row in data:
        tree.insert('', 'end', values=tuple(row[column] for column in columns))

def update(tree, table_name, columns, entrys, condition, width):
    # Retrieve values from entry widgets
    new_values = [entry.get() for entry in entrys]
    selected_id = new_values[0]
    # Format the list of columns and new values for the SET clause in the UPDATE query
    set_clause = ', '.join([f"`{col}` = '{new_val}'" for col, new_val in zip(columns[1:], new_values[1:])])

    # Assemble the complete UPDATE query
    query = f"UPDATE `{table_name}` SET {set_clause} WHERE `{columns[0]}` = {selected_id}"
    #Execute the query
    db_connection = connect()
    cursor = db_connection.cursor()
    cursor.execute(query)
    db_connection.commit()
    close_connection(db_connection, cursor)

    # Update the Treeview to reflect the changes
    fetch(tree, table_name, columns, condition, width)

def delete(tree, table_name, columns, condition, width):
    # Get the selected row's data from the Treeview
    selected_row_id = tree.selection()[0] if tree.selection() else None
    selected_id = tree.item(selected_row_id)['values'][0] if selected_row_id else None

    if selected_id:
        # Assemble the DELETE query
        query = f"DELETE FROM `{table_name}` WHERE `{columns[0]}` = {selected_id}"

        # Execute the query
        db_connection = connect()
        cursor = db_connection.cursor()
        cursor.execute(query)
        db_connection.commit()
        close_connection(db_connection, cursor)

        # Update the Treeview to reflect the changes
        fetch(tree, table_name, columns, condition, width)
    else:
        # If no row is selected, show an error message or take appropriate action
        print("No row selected for deletion.")

def select(Article_entrys,tree) :
    def on_tree_select(event):
        # Get the selected row's data from the Treeview
        selected_row_id = tree.selection()[0] if tree.selection() else None
        selected_row_data = tree.item(selected_row_id)['values'] if selected_row_id else []
        for entry, val in zip(Article_entrys, selected_row_data[0:]):
            entry.delete(0, ttk.END)
            entry.insert(0, val)
    tree.bind('<<TreeviewSelect>>', on_tree_select)

table_columns = {
    'customers': ['CustomerID', 'Name', 'ContactPhone'],
    'employees': ['EmployeeID', 'Name', 'ContactPhone', 'Salary', 'Permissions'],
    'articles': ['ArticleID', 'ArticleName', 'Price', 'QuantityInStock'],
    'purchaseinvoices': ['InvoiceID', 'CustomerID', 'EmployeeID', 'Date', 'DiscountPercentage', 'TotalPrice'],
    'purchaseinvoiceitems': ['InvoiceItemID', 'InvoiceID', 'ArticleID', 'Quantity', 'Price']
}

themes = [
    "darkly", "flatly", "journal",
    "litera", "lumen", "minty",
    "pulse", "sandstone", "simplex",
    "solar", "superhero", "united", "yeti"
]

PATH = Path(__file__).parent / 'assets'

class Stock_App(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        image_files = {
            'properties-dark': 'icons8_settings_24px.png',
            'properties-light': 'icons8_settings_24px_2.png',
            'add-to-backup-dark': 'icons8_add_folder_24px.png',
            'add-to-backup-light': 'icons8_add_book_24px.png',
            'stop-backup-dark': 'icons8_cancel_24px.png',
            'stop-backup-light': 'icons8_cancel_24px_1.png',
            'play': 'icons8_play_24px_1.png',
            'refresh': 'icons8_refresh_24px_1.png',
            'stop-dark': 'icons8_stop_24px.png',
            'stop-light': 'icons8_stop_24px_1.png',
            'opened-folder': 'icons8_opened_folder_24px.png',
            'logo': 'backup.png'
        }
        self.photoimages = []
        for key, val in image_files.items():
            _path = PATH / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

#---------------------frame_header --------------------------------------------------------------------------------------------
        frame_header = ttk.Frame(self, style='info.TFrame');frame_header.pack(fill=X, pady=1, side=TOP)
        # LOG OUT
        logOutBtn = ttk.Button(
            master=frame_header, 
            text='Log out', 
            image='play', 
            compound=LEFT, 
            command=lambda: Messagebox.ok(message='Backing up...'),
            style= INFO
        ).pack(side=RIGHT, ipadx=5, ipady=5, padx=0, pady=1)
        ## Settings
        settingsBtn = ttk.Button(
            master=frame_header, 
            text='Settings', 
            image='properties-light',
            compound=LEFT, 
            command=lambda: Messagebox.ok(message='Changing settings'),
            style= INFO
        ).pack(side=RIGHT, ipadx=5, ipady=5, padx=0, pady=1)
#---------------------right panel ---------------------------------------------------------------------------------------------
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        ## file input
        browse_frm = ttk.Frame(right_panel)
        browse_frm.pack(side=TOP, fill=X, padx=2, pady=1)
        
        file_entry = ttk.Entry(browse_frm, textvariable='folder-path')
        file_entry.pack(side=LEFT, fill=X, expand=YES)
        
        edit_emp = ttk.Button(
            master=browse_frm, 
            image='opened-folder', 
            bootstyle=(LINK, SECONDARY),
            command=self.get_directory
        )
        edit_emp.pack(side=RIGHT)

        ## Treeview
        Article_Table = ttk.Treeview(right_panel, show='headings', height=5)
        fetch(Article_Table, "articles", table_columns["articles"], '1', 200)
        Article_Table.pack(fill=X, pady=1)
        
        #########
        empTable = CollapsingFrame(right_panel)
        empTable.pack(fill='both', expand=NO, pady=10)
        
        empFrame = ttk.Frame(empTable, padding=1)
        empTable.add(child=empFrame, 
                     title='Employee Table',
                     bootstyle=SECONDARY)

        employee_Table = ttk.Treeview(empFrame, show='headings', height=5)
        fetch(employee_Table, "employees", table_columns["employees"], '1', 200)      
        employee_Table.pack(fill=X, pady=5)


        coustTable = CollapsingFrame(right_panel)
        coustTable.pack(fill=BOTH, expand=NO, pady=10)
        
        coustframe = ttk.Frame(coustTable, padding=1)
        coustTable.add(child=coustframe, 
                     title='Coustomer Table',
                     bootstyle=SECONDARY)

        Coustmer_Table = ttk.Treeview(coustframe, show='headings', height=5)
        fetch(Coustmer_Table, "customers", table_columns["customers"], '1', 200)
        Coustmer_Table.pack(fill=X, pady=1)

        _func = lambda: Messagebox.ok(message='Stopping backup')
        sell = ttk.Button(
            master=right_panel, 
            text='Sell a product', 
            image='stop-backup-light', 
            compound=RIGHT, 
            command=_func, 
            bootstyle="success-outline"
        ).pack(side=LEFT, padx=(230,0), pady=(0,5))

        _func = lambda: Messagebox.ok(message='Stopping backup')
        show = ttk.Button(
            master=right_panel, 
            text='View invoices', 
            image='stop-backup-light', 
            compound=LEFT, 
            command=_func, 
            bootstyle="warning-outline"
        ).pack(side=RIGHT, padx=(0,230), pady=(0,5))

#--------------------- left panel ------------------------------------------------------------------------------------------
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)

    ###### article ########################################################################################################
        Article_section = CollapsingFrame(left_panel);Article_section.pack(fill=X, pady=1)
        article_frame = ttk.Frame(Article_section, padding=5);article_frame.columnconfigure(1, weight=1)
        Article_section.add(
            child= article_frame, 
            title='Article', 
            bootstyle=SECONDARY,
            )
        
        Article_entrys = []
        for column in table_columns["articles"]:
            label = ttk.Label(article_frame, text=column + " :")
            label.grid(column=0, row=table_columns["articles"].index(column), padx=5, pady=2, sticky=W)

            entry_var = ttk.StringVar()
            entry = ttk.Entry(article_frame, textvariable=entry_var)
            entry.grid(column=1, row=table_columns["articles"].index(column), padx=5, pady=2, sticky=EW)

            Article_entrys.append(entry)
        sep = ttk.Separator(article_frame, bootstyle=SECONDARY)
        sep.grid(row=len(table_columns["articles"]), column=0, columnspan=2, pady=5, sticky=EW)

        select(Article_entrys,Article_Table)

        buttons_info = [
            ('Add article', 'properties-dark', lambda: insert(Article_Table, "articles", table_columns["articles"], Article_entrys, '1', 200)),
            ('Edit Article', 'add-to-backup-dark', lambda: update(Article_Table, "articles", table_columns["articles"], Article_entrys, '1', 200)),
            ('Delete Article', 'stop-backup-dark', lambda: delete(Article_Table, "articles", table_columns["articles"], '1', 200))
        ]
        for i, (text, image, command) in enumerate(buttons_info):
            ttk.Button(
                master=article_frame, 
                text=text, 
                image=image, 
                compound=LEFT, 
                command=command, 
                bootstyle=LINK
            ).grid(row=len(table_columns["articles"]) + 1 + i, column=0, columnspan=2, sticky=W)
    #----------------------------------------------------------------------------------------------------------------------
    ###### Employee #######################################################################################################
        Employee = CollapsingFrame(left_panel);Employee.pack(fill=BOTH, pady=1)
        employee_frame = ttk.Frame(Employee, padding=10);employee_frame.columnconfigure(1, weight=1)
        Employee.add(
            child=employee_frame, 
            title='Employee', 
            bootstyle=SECONDARY
        )

        Employee_entrys = []
        for column in table_columns["employees"]:
            label = ttk.Label(employee_frame, text=column + " :")
            label.grid(column=0, row=table_columns["employees"].index(column), padx=5, pady=2, sticky=W)

            entry_var = ttk.StringVar()
            entry = ttk.Entry(employee_frame, textvariable=entry_var)
            entry.grid(column=1, row=table_columns["employees"].index(column), padx=5, pady=2, sticky=EW)

            Employee_entrys.append(entry)
        sep = ttk.Separator(employee_frame, bootstyle=SECONDARY)
        sep.grid(row=len(table_columns["employees"]), column=0, columnspan=2, pady=5, sticky=EW)

        select(Employee_entrys,employee_Table)

        buttons_info = [
            ('Add employee', 'properties-dark', lambda: insert(employee_Table, "employees", table_columns["employees"], Employee_entrys, '1', 200)),
            ('Edit employee', 'add-to-backup-dark', lambda: update(employee_Table, "employees", table_columns["employees"], Employee_entrys, '1', 200)),
            ('Delete employee', 'stop-backup-dark', lambda: delete(employee_Table, "employees", table_columns["employees"], '1', 200))
        ]
        for i, (text, image, command) in enumerate(buttons_info):
            ttk.Button(
                master=employee_frame, 
                text=text, 
                image=image, 
                compound=LEFT, 
                command=command, 
                bootstyle=LINK
            ).grid(row=len(table_columns["employees"]) + 1 + i, column=0, columnspan=2, sticky=W)
    #----------------------------------------------------------------------------------------------------------------------
    ###### Costumer #######################################################################################################
        Coustmer= CollapsingFrame(left_panel);Coustmer.pack(fill='both',pady=1)
        customer_frame = ttk.Frame(Coustmer, padding=10);customer_frame.columnconfigure(1, weight=1)
        Coustmer.add(
            child=customer_frame, 
            title='Coustmer', 
            bootstyle=SECONDARY
        )

        Coustmer_entrys = []
        for column in table_columns["customers"]:
            label = ttk.Label(customer_frame, text=column + " :")
            label.grid(column=0, row=table_columns["customers"].index(column), padx=5, pady=2, sticky=W)

            entry_var = ttk.StringVar()
            entry = ttk.Entry(customer_frame, textvariable=entry_var)
            entry.grid(column=1, row=table_columns["customers"].index(column), padx=5, pady=2, sticky=EW)

            Coustmer_entrys.append(entry)
        sep = ttk.Separator(customer_frame, bootstyle=SECONDARY)
        sep.grid(row=len(table_columns["customers"]), column=0, columnspan=2, pady=5, sticky=EW)

        select(Coustmer_entrys,Coustmer_Table)

        buttons_info = [
            ('Add Coustmer', 'properties-dark', lambda: insert(Coustmer_Table, "customers", table_columns["customers"], Coustmer_entrys, '1', 200)),
            ('Edit Coustmer', 'add-to-backup-dark', lambda: update(Coustmer_Table, "customers", table_columns["customers"], Coustmer_entrys, '1', 200)),
            ('Delete Coustmer', 'stop-backup-dark', lambda: delete(Coustmer_Table, "customers", table_columns["customers"], '1', 200))
        ]
        for i, (text, image, command) in enumerate(buttons_info):
            ttk.Button(
                master=customer_frame, 
                text=text, 
                image=image, 
                compound=LEFT, 
                command=command, 
                bootstyle=LINK
            ).grid(row=len(table_columns["customers"]) + 1 + i, column=0, columnspan=2, sticky=W)
    #-----------------------------------------------------------------------------------------------------------------------

    def get_directory(self):
        """Open dialogue to get directory and update variable"""
        self.update_idletasks()
        d = askdirectory()
        if d:
            self.setvar('folder-path', d)

class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0 #?

        # widget images
        self.images = [
            ttk.PhotoImage(file=PATH/'icons8_double_up_24px.png'),
            ttk.PhotoImage(file=PATH/'icons8_double_right_24px.png')
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return
        
        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = ttk.Label(
            master=frm,
            text=title,
            bootstyle=(style_color, INVERSE)
        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child): return self._toggle_open_close(c)
        btn = ttk.Button(
            master=frm,
            image=self.images[0],
            bootstyle=style_color,
            command=_func
        )
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button 
        image accordingly.

        Parameters:
            
            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])

if __name__ == '__main__':
    app = ttk.Window(title="Stock",themename="darkly")
    Stock_App(app)
    app.mainloop()
