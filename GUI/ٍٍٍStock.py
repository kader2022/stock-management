
from datetime import datetime
from random import choices
import ttkbootstrap as ttk
from ttkbootstrap.style import Bootstyle
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from pathlib import Path


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
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        # buttonbar
        buttonbar = ttk.Frame(self, style='info.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        sty= INFO
        ## backup
        _func = lambda: Messagebox.ok(message='Backing up...')
        logOutBtn = ttk.Button(
            master=buttonbar, 
            text='Log out', 
            image='play', 
            compound=LEFT, 
            command=_func,
            style= sty
        )
        logOutBtn.pack(side=RIGHT, ipadx=5, ipady=5, padx=0, pady=1)


        ## settings
        _func = lambda: Messagebox.ok(message='Changing settings')
        settingsBtn = ttk.Button(
            master=buttonbar, 
            text='Settings', 
            image='properties-light',
            compound=LEFT, 
            command=_func,
            style= sty
        )
        settingsBtn.pack(side=RIGHT, ipadx=5, ipady=5, padx=0, pady=1)

        # left panel
        left_panel = ttk.Frame(self, style='bg.TFrame')
        left_panel.pack(side=LEFT, fill=Y)

        ## backup summary (collapsible)
        Article = CollapsingFrame(left_panel)
        Article.pack(fill=X, pady=1)

        ## container
        arti_frame = ttk.Frame(Article, padding=5)
        arti_frame.columnconfigure(1, weight=1)
        Article.add(
            child= arti_frame, 
            title='Article', 
            bootstyle=SECONDARY,

            )
        ## destination
        article_name_lb = ttk.Label( arti_frame, text='Name :')
        article_name_lb.grid(row=0, column=0, sticky=W, pady=1)
        art_name = ttk.Entry(arti_frame, width=20)
        art_name.grid(row=0, column=1, sticky=EW, padx=5, pady=1)
        
        price_lb = ttk.Label( arti_frame, text='Price :')
        price_lb.grid(row=1, column=0, sticky=W, pady=1)
        price = ttk.Entry(arti_frame, width=5)
        price.grid(row=1, column=1, sticky=EW, padx=5, pady=1)

        Quantity_lb = ttk.Label( arti_frame, text='Quantity :')
        Quantity_lb.grid(row=2, column=0, sticky=W, pady=1)
        Quantity = ttk.Entry(arti_frame, width=5)
        Quantity.grid(row=2, column=1, sticky=EW, padx=5, pady=1)

        ## section separator
        sep = ttk.Separator(arti_frame, bootstyle=SECONDARY)
        sep.grid(row=3, column=0, columnspan=2, pady=10, sticky=EW)

        ## properties button
        _func = lambda: Messagebox.ok(message='Changing properties')
        Add_articBTN = ttk.Button(
            master= arti_frame, 
            text='Add article', 
            image='properties-dark', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        Add_articBTN.grid(row=4, column=0, columnspan=2, sticky=W)

        ## add to backup button
        _func = lambda: Messagebox.ok(message='Adding to backup')
        edit_art = ttk.Button(
            master= arti_frame, 
            text='Edit Article', 
            image='add-to-backup-dark', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        edit_art.grid(row=5, column=0, columnspan=2, sticky=W)

        _func = lambda: Messagebox.ok(message='Adding to backup')
        delete_art = ttk.Button(
            master= arti_frame, 
            text='Delete Article', 
            image='stop-backup-dark', 
            compound=LEFT,
            command=_func, 
            bootstyle=LINK
        )
        delete_art.grid(row=6, column=0, columnspan=2, sticky=W)

        # backup status (collapsible)
        Employee = CollapsingFrame(left_panel)
        Employee.pack(fill=BOTH, pady=1)

        ## container
        Emp_frame = ttk.Frame(Employee, padding=10)
        Emp_frame.columnconfigure(1, weight=1)
        Employee.add(
            child=Emp_frame, 
            title='Employee', 
            bootstyle=SECONDARY
        )
        ## progress message

        Emp_name_lb = ttk.Label( Emp_frame, text='Name :')
        Emp_name_lb.grid(row=0, column=0, sticky=W, pady=2)
        emp_name = ttk.Entry(Emp_frame, width=20)
        emp_name.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        
        emp_phone_lb = ttk.Label( Emp_frame, text='phone :')
        emp_phone_lb.grid(row=1, column=0, sticky=W, pady=2)
        emp_phone = ttk.Entry(Emp_frame, width=5)
        emp_phone.grid(row=1, column=1, sticky=EW, padx=5, pady=2)

        salary_lb = ttk.Label( Emp_frame, text='salary :')
        salary_lb.grid(row=2, column=0, sticky=W, pady=2)
        salary = ttk.Entry(Emp_frame, width=5)
        salary.grid(row=2, column=1, sticky=EW, padx=5, pady=2)

        ## section separator
        sep = ttk.Separator( Emp_frame, bootstyle=SECONDARY)
        sep.grid(row=3, column=0, columnspan=2, pady=10, sticky=EW)
        

        ## stop button
        _func = lambda: Messagebox.ok(message='Stopping backup')
        Add_emp = ttk.Button(
            master=Emp_frame, 
            text='Add employee', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        Add_emp.grid(row=4, column=0, columnspan=2, sticky=W)

        _func = lambda: Messagebox.ok(message='Stopping backup')
        edit_emp = ttk.Button(
            master=Emp_frame, 
            text='Edit Employee', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        edit_emp.grid(row=5, column=0, columnspan=2, sticky=W)

        _func = lambda: Messagebox.ok(message='Stopping backup')
        delete_emp= ttk.Button(
            master=Emp_frame, 
            text='delete Employee', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        delete_emp.grid(row=6, column=0, columnspan=2, sticky=W)
        # section separator
        

        Coustmer= CollapsingFrame(left_panel)
        Coustmer.pack(fill='both',pady=1)

        coust_frame = ttk.Frame(Coustmer, padding=10)
        coust_frame.columnconfigure(1, weight=1)
        Coustmer.add(
            child=coust_frame, 
            title='Coustmer', 
            bootstyle=SECONDARY
        )

        #########################
        coust_name_lb = ttk.Label( coust_frame, text='Name :')
        coust_name_lb.grid(row=0, column=0, sticky=W, pady=2)
        coust_name = ttk.Entry(coust_frame, width=20)
        coust_name.grid(row=0, column=1, sticky=EW, padx=5, pady=2)
        
        coust_phone_lb = ttk.Label( coust_frame, text='phone :')
        coust_phone_lb.grid(row=1, column=0, sticky=W, pady=2)
        coust_phone = ttk.Entry(coust_frame, width=5)
        coust_phone.grid(row=1, column=1, sticky=EW, padx=5, pady=2)

        ## section separator
        sep = ttk.Separator( coust_frame, bootstyle=SECONDARY)
        sep.grid(row=2, column=0, columnspan=2, pady=10, sticky=EW)
        

        ## stop button
        _func = lambda: Messagebox.ok(message='Stopping backup')
        Add_Coustmer = ttk.Button(
            master=coust_frame, 
            text='Add Coustmer', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        Add_Coustmer.grid(row=3, column=0, columnspan=2, sticky=W)

        _func = lambda: Messagebox.ok(message='Stopping backup')
        edit_Coustmer = ttk.Button(
            master=coust_frame, 
            text='Edit Coustmer', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        edit_Coustmer.grid(row=4, column=0, columnspan=2, sticky=W)

        _func = lambda: Messagebox.ok(message='Stopping backup')
        delete_Coustmer= ttk.Button(
            master=coust_frame, 
            text='delete Coustmer', 
            image='stop-backup-dark', 
            compound=LEFT, 
            command=_func, 
            bootstyle=LINK
        )
        delete_Coustmer.grid(row=5, column=0, columnspan=2, sticky=W)
        #########################

       

        # right panel
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
        tv = ttk.Treeview(right_panel, show='headings', height=5)
        tv.configure(columns=(
            'Article ID', 'Article Name', 'Price', 
             'Quantity In Stock'
        ))
        
        for col in tv['columns']:
            tv.heading(col, text=col.title(), anchor=W)
        
        tv.pack(fill=X, pady=1)
        
        #########

        empTable = CollapsingFrame(right_panel)
        empTable.pack(fill='both', expand=NO, pady=10)
        
        empFrame = ttk.Frame(empTable, padding=1)
        empTable.add(child=empFrame, 
                     title='Employee Table',
                     bootstyle=SECONDARY)

        TE = ttk.Treeview(empFrame, show='headings', height=5)
        TE.configure(columns=(
            'Employee ID', 'Name', 'Phone', 
            'Salary'
        ))
        
        for col in TE['columns']:
            TE.heading(col, text=col.title(), anchor=W)
        
        TE.pack(fill=X, pady=5)
        


        # coustomer = CollapsingFrame(right_panel)
        # coustomer.pack(fill=BOTH, expand=YES)
        
        # coustFrame = ttk.Frame(empTable, padding=1)
        # coustomer.add(coustFrame, title='Employee Table')

        coustTable = CollapsingFrame(right_panel)
        coustTable.pack(fill=BOTH, expand=NO, pady=10)
        
        coustframe = ttk.Frame(coustTable, padding=1)
        coustTable.add(child=coustframe, 
                     title='Coustomer Table',
                     bootstyle=SECONDARY)

        TC = ttk.Treeview(coustframe, show='headings', height=5)
        TC.configure(columns=(
            'Customer ID', 'name', 'Phone'
        ))
        
        for col in TC['columns']:
            TC.heading(col, text=col.title(), anchor=W)
        
        TC.pack(fill=X, pady=1)
        TC.insert('',END,values=("1","2","3"))

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
        self.cumulative_rows = 0

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
