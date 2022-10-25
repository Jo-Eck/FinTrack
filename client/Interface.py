import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import *
from tkinter.messagebox import showinfo
from turtle import color, tilt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from ScrollableImage import *
import requests

# root window
root = tk.Tk()
root.geometry("1280x720")
root.resizable(False, False)
root.title('Financial Tracker 3000')
root.columnconfigure([0,1,2], minsize=150)
root.rowconfigure([0,1], minsize = 150)

#store value, category and balance
value = tk.StringVar()
category = tk.StringVar()
balance = 1000.00 #tk.StringVar()

def save_transaction():
    """saves the entered value and category as a new transaction for the user
    """
    msg=f"Your new transaction: {value.get()}€ for {category.get()} will be saved"
    showinfo(
        title="Saving",
        message=msg
    )
    
#input frame
input_frame = ttk.Frame(root, borderwidth=3)
input_frame.grid(row=0, column=2, padx=150)

#output frame
output_frame = ttk.Frame(root, borderwidth=3)
output_frame.place(x=25,y=25)

#transaction table frame
table_frame = ttk.Frame(root, borderwidth=3)
table_frame.grid(row=1, column=0, pady=100)

#transaction pie frame
pie_frame = ttk.Frame(root, borderwidth=3)
pie_frame.grid(row=1, column=2)

#balance
balance_label = ttk.Label(output_frame, text="Balance", font="Calibri")
balance_label.pack()

#show balance
show_balance_label = ttk.Label(output_frame, text=balance)
show_balance_label.pack(fill='x', expand=True)

#transaction label
transaction_label = ttk.Label(input_frame, text="Transaction", font="Calibri")
transaction_label.pack(fill='x', expand=True)

#Money Value
money_label = ttk.Label(input_frame, text="Value")
money_label.pack(fill='x', expand=True, )

money_label = ttk.Entry(input_frame, textvariable=value)
money_label.pack(fill='x', expand=True)
money_label.focus()

#category label
category_label = ttk.Label(input_frame, text="Category")
category_label.pack(fill='x', expand=True)

category_label = ttk.Entry(master=input_frame, textvariable=category)
category_label.pack(fill='x', expand=True)
category_label.focus() 

#save transaction button
save_transaction_button = ttk.Button(input_frame, text="Save", command=save_transaction)
save_transaction_button.pack(fill="x", expand=True, pady=10)

#transaction table label
transaction_table_label = ttk.Label(table_frame, text="Latest Transactions")
transaction_table_label.pack()

#transaction pie label
transaction_pie_label = ttk.Label(pie_frame, text="Balance over time")
transaction_pie_label.pack()

#transaction table
table_data = [["Value", "Category", "Date"],
              [60, "Weed", "01.01.2022"],
              [37, "Groceries", "10.01.2022"],
              [4.69, "Beer", "20.01.2022"],
              [15, "Gift", "29.01.2022"],
              [45, "Weed", "02.03.2022"],
              [37, "Groceries", "10.03.2022"],
              [4.69, "Beer", "09.04.2022"],
              [15, "Gift", "11.04.2022"],
              [90, "Weed", "12.04.2022"],
              [37, "Groceries", "13.05.2022"],
              [4.69, "Beer", "14.06.2022"],
              [15, "Gift", "15.06.2022"]]
fig = ff.create_table(table_data)
fig.update_layout(width = 300)
fig.write_image("Table.png")
img = PhotoImage(file='./Table.png')

table_label = ScrollableImage(table_frame, image=img, width = 300 ,scrollbarwidth = 12)
table_label.pack(padx=20)

#transaction pie
pie = px.pie(table_data, values=0, names=1)
pie.update_layout(width = 400)
pie.write_image("pie.png")
pie_img = PhotoImage(file='./pie.png')

pie_label = ttk.Label(pie_frame, image = pie_img)#ScrollableImage(pie_frame, image=pie_img,scrollbarwidth = 6)
pie_label.pack(pady=20)


root.mainloop()
