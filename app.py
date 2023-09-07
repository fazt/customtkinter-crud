import customtkinter
from tkcalendar import Calendar
from tkinter import ttk
from tkinter import messagebox

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.title("Tasks App")
app.geometry("650x700")

input_pady = 2
global title_entry, desc_text, date_calendar, tasks_table
editing = False

def add_task():
    title = title_entry.get()
    description = desc_text.get("1.0", "end-1c")
    date = date_calendar.get_date()
    global editing

    if title == "":
        messagebox.showerror("Error", "Title cannot be empty")
        return
    elif description == "":
        messagebox.showerror("Error", "Description cannot be empty")
        return
    elif date == "":
        messagebox.showerror("Error", "Date cannot be empty")
        return

    print(title, description, date)

    if not editing:
        tasks_table.insert("", "end", values=(title, description, date, "✎", "🗑"))
    else:
        item = tasks_table.selection()[0]
        tasks_table.item(item, values=(title, description, date, "✎", "🗑"))
        editing = False


    # clear inputs
    title_entry.delete(0, "end")
    desc_text.delete("1.0", "end")

def on_item_double_click(event):
    global editing
    if not tasks_table.selection():
        return

    # Obtener el item seleccionado
    item = tasks_table.selection()[0]
    
    # Determinar la columna donde se hizo doble clic
    col = tasks_table.identify_column(event.x)
    
    if col == "#4":
        # Código para editar
        print(f"Editing item: {item}")
        values = tasks_table.item(item, "values")

        title_entry.delete(0, "end")
        title_entry.insert(0, values[0])

        desc_text.delete("1.0", "end")
        desc_text.insert("1.0", values[1])

        date_calendar.selection_set(values[2])
        editing = True

    elif col == "#5":
        # confirm dialog
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            tasks_table.delete(item)
        # Código para eliminar
        # tasks_table.delete(item)
        print(f"deleting item {item}")


# title
title_label = customtkinter.CTkLabel(master=app, text="Write a Title", anchor="w")
title_label.pack(fill=customtkinter.X, padx=10, pady=input_pady)

title_entry = customtkinter.CTkEntry(master=app)
title_entry.pack(pady=input_pady, padx=20, fill=customtkinter.X)

# description
description_label = customtkinter.CTkLabel(master=app, text="Write a Description", anchor="w")
description_label.pack(fill=customtkinter.X, padx=10, pady=input_pady)
desc_text = customtkinter.CTkTextbox(master=app, height=100)
desc_text.pack(pady=input_pady, padx=20, fill="x")

# date
date_label = customtkinter.CTkLabel(master=app, text="Date to Accomplish", anchor="w")

# full horizontal fill
date_label.pack(fill=customtkinter.X, padx=10, pady=input_pady)
date_calendar = Calendar(master=app)
date_calendar.pack(pady=input_pady, padx=20, fill="x")


saveButton = customtkinter.CTkButton(master=app, text="Add Task", command=add_task)
saveButton.pack()


# table of tasks
tasks_table = ttk.Treeview(master=app, show="headings")

tasks_table["columns"] = ("title", "description", "date", "Edit", "Delete")
tasks_table.column("#0", width=0, stretch="no")
tasks_table.column("title", anchor="w", width=100)
tasks_table.column("description", anchor="w", width=100)
tasks_table.column("date", anchor="w", width=100)
tasks_table.column("Edit", anchor="w", width=50)
tasks_table.column("Delete", anchor="w", width=50)

tasks_table.heading("title", text="Title")
tasks_table.heading("description", text="Description")
tasks_table.heading("date", text="Date")
tasks_table.heading("Edit", text="Edit")
tasks_table.heading("Delete", text="Delete")

tasks_table.bind("<Double-1>", on_item_double_click)

tasks_table.pack(fill="x", padx=10, pady=10)

# title entry focus
app.after(500, lambda: title_entry.focus_set())

app.mainloop()