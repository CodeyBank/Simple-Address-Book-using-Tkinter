from tkinter import *
from PIL import ImageTk, Image
import sqlite3

# noinspection PyUnresolvedReferences
# from addressbook_backend import db

root = Tk()
root.title("Databases")
root.iconbitmap('icon.ico')
root.geometry('1100x600')
root.configure(bg="white")


# **************************************Screen Definitions********************************************************
def screen1():
    global frame_entry2, f_name, l_name, city, addr, state, zipcode, del_box
    frame_entry2 = LabelFrame(frame_parent, bg="white", padx=20, pady=20, bd=0)  # padding inside the frame
    frame_entry2.grid(row=1, column=1, padx=2, pady=2)  # outside the frame padding
    # Form entries
    fname_lbl = Label(frame_entry2, text="First Name", font="gothic 14 bold", bg="white", fg="#6272a4")
    fname_lbl.grid(row=0, column=1, padx=5, pady=5, sticky=N)
    f_name = Entry(frame_entry2, width=40, font="gothic 14 bold")
    f_name.grid(row=0, column=2, padx=5, pady=5, sticky=N)

    lname_lbl = Label(frame_entry2, text="Last Name", font="gothic 14 bold", bg="white", fg="#6272a4")
    lname_lbl.grid(row=1, column=1, padx=5, pady=5, sticky=N)
    l_name = Entry(frame_entry2, width=40, relief=SUNKEN, font="gothic 14 bold")
    l_name.grid(row=1, column=2, padx=5, pady=5, sticky=N)

    address_lbl = Label(frame_entry2, text="Address", font="gothic 14 bold", bg="white", fg="#6272a4")
    address_lbl.grid(row=2, column=1, padx=5, pady=5)
    addr = Entry(frame_entry2, width=40, font="gothic 14 bold")
    addr.grid(row=2, column=2, padx=5, pady=5)

    city_lbl = Label(frame_entry2, text="City", font="gothic 14 bold", bg="white", fg="#6272a4")
    city_lbl.grid(row=3, column=1, padx=5, pady=5)
    city = Entry(frame_entry2, width=40, font="gothic 14 bold")
    city.grid(row=3, column=2, padx=5, pady=5)

    state_lbl = Label(frame_entry2, text="State", font="gothic 14 bold", bg="white", fg="#6272a4")
    state_lbl.grid(row=4, column=1, padx=5, pady=5)
    state = Entry(frame_entry2, width=40, font="gothic 14 bold")
    state.grid(row=4, column=2, padx=5, pady=5)

    zipcode_lbl = Label(frame_entry2, text="Zipcode", font="gothic 14 bold", bg="white", fg="#6272a4")
    zipcode_lbl.grid(row=5, column=1, padx=5, pady=5)
    zipcode = Entry(frame_entry2, width=40, font="gothic 14 bold")
    zipcode.grid(row=5, column=2, padx=5, pady=5)

    del_box_lbl = Label(frame_entry2, text="ID Number", font="gothic 14 bold", bg="white", fg="#6272a4")
    del_box_lbl.grid(row=6, column=1, padx=5, pady=5)
    del_box = Entry(frame_entry2, width=10, font="gothic 14 bold")
    del_box.grid(row=6, column=2, padx=5, pady=5)
    # del_box_value = del_box.get()


def screen2():
    global frame_entry_new, query_list
    # Recreate the frame again since it will be used again
    frame_entry_new = LabelFrame(frame_parent, bg="white", padx=20, pady=20, bd=0)  # padding inside the frame
    frame_entry_new.grid(row=1, column=1, padx=2, pady=2)  # outside the frame padding

    query_list = Listbox(frame_entry_new, width=80, height=20)
    query_list.grid(row=0, column=1, rowspan=6, columnspan=3)

    # retrieve the index of the selected listbox item
    query_list.bind('<<ListboxSelect>>', get_selected_row)

    # Scroll bar
    sb1 = Scrollbar(frame_entry_new)
    sb1.grid(row=0, column=4, rowspan=6)
    # Configure querylist to work with scroll bar
    query_list.configure(yscrollcommand=sb1.set)
    sb1.configure(command=query_list.yview)

    for record in records:
        # insert item into list box
        query_list.insert(END, record)


# *********************************end of screen definitions **********************************************************


# *****************************************Function definitions*****************************************************

def query():
    global records
    conn = sqlite3.connect("address_book1.db")
    # self.tablename = tablename
    c = conn.cursor()
    c.execute("SELECT *,oid FROM contacts")
    # print_records = ''
    records = c.fetchall()
    conn.commit()
    conn.close()
    # Clear the frame_entry2 to insert the list box
    frame_entry2.grid_forget()
    screen2()


def previous():
    frame_entry_new.grid_forget()
    screen1()


def get_selected_row(event):
    global selected_tuple
    global index
    try:
        global index
        index = query_list.curselection()[0]  # curselection returns the list of tuples(each entry of the list box)
        selected_tuple = query_list.get(index)
        # print(selected_tuple)
    except IndexError:
        pass


def delete():
    conn = sqlite3.connect("address_book1.db")
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (selected_tuple[0],))
    conn.commit()
    conn.close()
    print("Deleted")


def create():
    conn = sqlite3.connect("address_book1.db")
    # self.tablename = tablename
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS contacts (
    id integer primary key,
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode int)
    """)
    conn.commit()


create()


def clear():
    f_name.delete(0, END)
    l_name.delete(0, END)
    addr.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


def submit(fname, lname, addr, cty, st, zpcd):
    conn = sqlite3.connect("address_book1.db")
    # self.tablename = tablename
    c = conn.cursor()
    """
        c.execute("INSERT INTO contacts VALUES (:id, :f_name, :l_name, :address, :city, :state, :zipcode)",
              {
                  'id': "NULL",
                  'first_name': f_name.get(),
                  'last_name': l_name.get(),
                  'address': addr.get(),
                  'city': city.get(),
                  'state': state.get(),
                  'zipcode': zipcode.get()
              }
              )
    """
    c.execute("INSERT INTO contacts VALUES(NULL,?,?,?,?,?,?)", (
        fname, lname, addr, cty, st,
        zpcd))  # NULL is used for the primary key because the DB automatically increments this
    conn.commit()
    conn.close()
    clear()


def update():
    conn = sqlite3.connect("address_book1.db")
    c = conn.cursor()

    record_id = del_box.get()
    c.execute("""UPDATE contacts SET 
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode
        
        WHERE oid = :oid""",
              {'first': f_name_editor.get(),
               'last': l_name_editor.get(),
               'address': addr_editor.get(),
               'city': city_editor.get(),
               'state': state_editor.get(),
               'zipcode': zipcode_editor.get(),
               'oid': record_id
               }
              )

    conn.commit()
    conn.close()

    editor.destroy()
    # Close all fields


def edit():
    global editor
    editor = Tk()
    editor.title("Update")
    editor.iconbitmap('icon.ico')
    editor.geometry('600x600')
    editor.configure(bg="white")

    # create a connection to the database
    conn = sqlite3.connect("address_book1.db")
    c = conn.cursor()

    record_id = del_box.get()
    c.execute('SELECT * FROM contacts WHERE oid=' + record_id)
    recorder = c.fetchall()

    # create global variables so that it can be called from update function
    global f_name_editor, l_name_editor, city_editor, state_editor, addr_editor, zipcode_editor

    fname_lbl = Label(editor, text="First Name", font="gothic 14 bold", bg="white", fg="#6272a4")
    fname_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=N)
    f_name_editor = Entry(editor, width=40, font="gothic 14 bold")
    f_name_editor.grid(row=0, column=1, padx=5, pady=5, sticky=N)

    lname_lbl = Label(editor, text="Last Name", font="gothic 14 bold", bg="white", fg="#6272a4")
    lname_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=N)
    l_name_editor = Entry(editor, width=40, relief=SUNKEN, font="gothic 14 bold")
    l_name_editor.grid(row=1, column=1, padx=5, pady=5, sticky=N)

    address_lbl = Label(editor, text="Address", font="gothic 14 bold", bg="white", fg="#6272a4")
    address_lbl.grid(row=2, column=0, padx=5, pady=5)
    addr_editor = Entry(editor, width=40, font="gothic 14 bold")
    addr_editor.grid(row=2, column=1, padx=5, pady=5)

    city_lbl = Label(editor, text="City", font="gothic 14 bold", bg="white", fg="#6272a4")
    city_lbl.grid(row=3, column=0, padx=5, pady=5)
    city_editor = Entry(editor, width=40, font="gothic 14 bold")
    city_editor.grid(row=3, column=1, padx=5, pady=5)

    state_lbl = Label(editor, text="State", font="gothic 14 bold", bg="white", fg="#6272a4")
    state_lbl.grid(row=4, column=0, padx=5, pady=5)
    state_editor = Entry(editor, width=40, font="gothic 14 bold")
    state_editor.grid(row=4, column=1, padx=5, pady=5)

    zipcode_lbl = Label(editor, text="Zipcode", font="gothic 14 bold", bg="white", fg="#6272a4")
    zipcode_lbl.grid(row=5, column=0, padx=5, pady=5)
    zipcode_editor = Entry(editor, width=40, font="gothic 14 bold")
    zipcode_editor.grid(row=5, column=1, padx=5, pady=5)

    # save button

    save_btn = Button(editor, text="Save", font="gothic 14 bold", bg="white", fg="#6272a4", command=update)
    save_btn.grid(row=6, column=1, ipadx=40)

    for record in recorder:
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        addr_editor.insert(0, record[4])
        state_editor.insert(0, record[5])
        zipcode_editor.insert(0, record[6])

    conn.close()


# ************************************End of Function Definitions******************************************************


# **************************************Frame Definitions**************************************************************
frame_parent = LabelFrame(root, bg="white", padx=20, pady=20, bd=0)  # padding inside the frame
frame_parent.grid(row=0, column=1, padx=2, pady=2)  # outside the frame padding

frame_img = LabelFrame(root, bg="white", bd=0)  # padding inside the frame
frame_img.grid(row=0, column=0, padx=2, pady=2)  # outside the frame padding

frame_entry1 = LabelFrame(frame_parent, bg="white", padx=20, pady=20, bd=0)  # padding inside the frame
frame_entry1.grid(row=0, column=1, padx=2, pady=2)  # outside the frame padding

frame_entry3 = LabelFrame(frame_parent, bg="white", padx=20, pady=20, bd=0)  # padding inside the frame
frame_entry3.grid(row=2, column=1, padx=2, pady=2)  # outside the frame padding
# ***************************************End of Frame Definitions******************************************************


# load the image into a label

img = ImageTk.PhotoImage(Image.open("graduate.jpg"))
img_lbl = Label(frame_img, image=img)
img_lbl.pack()

#
# ****************************************Frame1 Entries***************************************************************
Welcome = Label(frame_entry1, text="CypherPoint Learning", bg="white", font="gothic 18 bold", fg='#6272a4',
                anchor=W).grid(row=0, column=0, padx=5, pady=5)
# login = Button(frame_entry1, text="Login", font="gothic 14 bold", bg="white", fg='#6272a4').grid(row=0, column=5)

prev = Button(frame_entry1, text="Prev", font="gothic 14 bold", bg="white", fg='#6272a4', command=previous)
prev.grid(row=0, column=1, sticky=W, padx=(200, 0))
edit_entry = Button(frame_entry1, text="Edit", font="gothic 14 bold", bg="white", fg='#6272a4', command=edit)
edit_entry.grid(row=1, column=1, sticky=W, padx=(200, 0))
# ***************************************End of Frame1 Entries*********************************************************

# *************************************Frame 3 Entries*****************************************************************
submit_btn = Button(frame_entry3, text="submit", font="gothic 14 bold", bg='#6272a4', fg='white',
                    command=lambda: submit(f_name.get(), l_name.get(), addr.get(), city.get(), state.get(),
                                           zipcode.get()))
submit_btn.grid(row=0, column=0, columnspan=2, ipadx=100)
# lambda: database.insert(f_name.get(), l_name.get(), addr.get(), city.get(), state.get(),
#                                                 zipcode.get())
query_btn = Button(frame_entry3, text="Show Entry", font="gothic 14 bold", bg='#6272a4', fg='white',
                   command=query)
query_btn.grid(row=1, column=0)
delete_btn = Button(frame_entry3, text="Delete Entry", font="gothic 14 bold", bg='#6272a4', fg='white',
                    command=delete)
delete_btn.grid(row=1, column=1)
# ************************************End of Frame3 Entries************************************************************

screen1()

root.mainloop()
