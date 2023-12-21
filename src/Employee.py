
import ttkbootstrap as ttk

root= ttk.Window()

empFrame = ttk.Frame(root)
empFrame.pack()



TE = ttk.Treeview(empFrame, show='headings', height=5)
TE.configure(columns=(
    'name', 'state', 'last-modified', 
    'last-run-time', 'size'
))
TE.column('name', width=240, stretch=True)

# for col in ['last-modified', 'last-run-time', 'size']:
#     TE.column(col, stretch=False)

for col in TE['columns']:
    TE.heading(col, text=col.title(), anchor='w')

TE.pack(fill='x', pady=50)


root.mainloop()