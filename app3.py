import tkinter as tk
import pandas as pd

from tkinter.filedialog import askopenfile
from tkinter import messagebox
from tkinter import ttk

# DataFrame transformation and Mergeing two Column

amazon = pd.read_csv('amz_com-ecommerce_sample.csv', encoding='unicode_escape')
flipkart = pd.read_csv('flipkart_com-ecommerce_sample.csv', encoding='unicode_escape')

df1 = amazon[['product_name','pid','retail_price','discounted_price']]
df2 = flipkart[['product_name','pid','retail_price','discounted_price']]

df1 = df1.rename(columns={'product_name':'Product name in Amazon','pid':'amazon_pid','retail_price':'Retail Price in Amazon','discounted_price':'Discounted Price in Amazom'})
df2 = df2.rename(columns={'product_name':'Product name in Flipkart','pid':'flipkart_pid','retail_price':'Retail Price in Flipkart','discounted_price':'Discounted Price in Flipkart'})

df2.dropna(inplace= True)
joint_data=df2.merge(df1,left_on="flipkart_pid",right_on='amazon_pid',how='inner')
joint_data.drop(['flipkart_pid','amazon_pid'], axis=1, inplace = True)

# FOR GUI

root = tk.Tk()
root.geometry("700x500")
root.pack_propagate(False)
root.resizable(0,0)

# Frame for output

frame1 = tk.LabelFrame(root, text='Result :', font='Raleway')
frame1.place(height=250, width=700)

# file frame 

file_frame = tk.LabelFrame(root, text="Enter a Product name to search", font='Raleway')
file_frame.place(height=100, width=700, rely = 0.65, relx=0)

# input
e1=tk.Entry(file_frame)
e1.place(width= 400, rely=0.1, relx=0.1)

# Buttons
button1 = tk.Button(file_frame, text="Search", font='Raleway', command=lambda:search())
button1.place(rely=0.45, relx=0.3)

# Tree Widget

tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1)

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")


def search():

    name = e1.get()   

    try:
        result= joint_data.loc[joint_data['Product name in Amazon'] == name]
    except:
        messagebox.showerror("Error in name")

    clear_scr()
    tv1["column"] = list(result.columns)
    tv1["show"] = "headings"

    for column in tv1["columns"]:
        tv1.heading(column, text=column )

    df_rows =result.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)

    return None



def clear_scr():
    pass


root.mainloop()