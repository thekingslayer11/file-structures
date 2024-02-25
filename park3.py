import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import hashlib


update_ride_id = None
entry_ride_id = None
entry_search = None

records = [
    {
        "Ride ID": 1,
        "Ride Name": "Roller Coaster",
        "Ride Status": "Open",
        "Ride Capacity": 20,
        "Ride Rating": 4,
    },
    {
        "Ride ID": 2,
        "Ride Name": "Ferris Wheel",
        "Ride Status": "Closed",
        "Ride Capacity": 16,
        "Ride Rating": 5,
    },
    # Add more initial records as needed
]


def save_records():
    with open("records.txt", "w") as file:
        for record in records:
            file.write(
                f"{record['Ride ID']},{record['Ride Name']},{record['Ride Status']},{record['Ride Capacity']},{record['Ride Rating']}\n"
            )


# Function to add a new record
def add_record():
    ride_id = entry_ride_id.get()
    ride_name = entry_ride_name.get()
    ride_status = ride_status_var.get()
    ride_capacity = entry_ride_capacity.get()
    ride_rating = ride_rating_var.get()

    # Validate input fields
    if ride_id and ride_name and ride_status and ride_capacity and ride_rating:
        if is_duplicate_ride_id(ride_id):
            messagebox.showerror("Error", "Ride ID already exists.")
        else:
            print("New record added:")
            print("Ride ID:", ride_id)
            print("Ride Name:", ride_name)
            print("Ride Status:", ride_status)
            print("Ride Capacity:", ride_capacity)
            print("Ride Rating:", ride_rating)
            messagebox.showinfo("Success", "New record added successfully!")
            new_record = {
                "Ride ID": ride_id,
                "Ride Name": ride_name,
                "Ride Status": ride_status,
                "Ride Capacity": ride_capacity,
                "Ride Rating": ride_rating,
            }
            records.append(new_record)
            save_records()

            # Clear input fields
            entry_ride_id.delete(0, tk.END)
            entry_ride_name.delete(0, tk.END)
            entry_ride_capacity.delete(0, tk.END)
            ride_status_var.set(0)
            ride_rating_var.set(0)
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")


def is_duplicate_ride_id(ride_id):
    # Check in the existing records
    existing_ids = [record["Ride ID"] for record in records]
    if ride_id in existing_ids:
        return True

    # Check in the file
    with open("records.txt", "r") as file:
        for line in file:
            record_data = line.strip().split(",")
            if record_data[0] == ride_id:
                return True

    return False


# Function to handle the "Search Record" button click
def search_record():
    # Create a new window for searching a record
    search_window = tk.Toplevel(window)
    search_window.title("Search Record")

    label_ride_id = tk.Label(search_window, text="Ride ID:")
    label_ride_id.pack()
    entry_ride_id = tk.Entry(search_window)
    entry_ride_id.pack()

    button_search = tk.Button(
        search_window,
        text="Search",
        command=lambda: perform_search(entry_ride_id.get(), search_window),
    )
    button_search.pack()


def perform_search(ride_id, search_window):
    if ride_id:
        with open("records.txt", "r") as file:
            found_record = None
            for line in file:
                record_data = line.strip().split(",")
                if record_data[0] == ride_id:
                    found_record = {
                        "Ride ID": record_data[0],
                        "Ride Name": record_data[1],
                        "Ride Status": record_data[2],
                        "Ride Capacity": record_data[3],
                        "Ride Rating": record_data[4],
                    }
                    break

            if found_record:
                # Display the found record in a messagebox
                messagebox.showinfo(
                    "Record Found",
                    f"Ride ID: {found_record['Ride ID']}\n"
                    f"Ride Name: {found_record['Ride Name']}\n"
                    f"Ride Status: {found_record['Ride Status']}\n"
                    f"Ride Capacity: {found_record['Ride Capacity']}\n"
                    f"Ride Rating: {found_record['Ride Rating']}",
                )
                search_window.destroy()
            else:
                messagebox.showerror("Error", "Record not found.")
    else:
        messagebox.showerror("Error", "Please enter the Ride ID.")


def perform_search_update(ride_id):
    if ride_id:
        with open("records.txt", "r") as file:
            found_record = None
            for line in file:
                record_data = line.strip().split(",")
                if record_data[0] == ride_id:
                    found_record = {
                        "Ride ID": record_data[0],
                        "Ride Name": record_data[1],
                        "Ride Status": record_data[2],
                        "Ride Capacity": record_data[3],
                        "Ride Rating": record_data[4],
                    }
                    break

            if found_record:
                update_window = tk.Toplevel(window)
                update_window.title("Update Record")

                label_ride_id = tk.Label(update_window, text="Ride ID:")
                label_ride_id.pack()
                entry_ride_id = tk.Entry(update_window)
                entry_ride_id.insert(0, found_record["Ride ID"])
                entry_ride_id.pack()

                label_ride_name = tk.Label(update_window, text="Ride Name:")
                label_ride_name.pack()
                entry_ride_name = tk.Entry(update_window)
                entry_ride_name.insert(0, found_record["Ride Name"])
                entry_ride_name.pack()

                label_ride_status = tk.Label(update_window, text="Ride Status:")
                label_ride_status.pack()
                ride_status_var = tk.StringVar()
                ride_status_var.set(found_record["Ride Status"])
                ride_status_frame = tk.Frame(update_window)
                ride_status_frame.pack()
                ride_status_open = tk.Radiobutton(
                    ride_status_frame,
                    text="Open",
                    variable=ride_status_var,
                    value="Open",
                )
                ride_status_open.pack(side="left")
                ride_status_closed = tk.Radiobutton(
                    ride_status_frame,
                    text="Closed",
                    variable=ride_status_var,
                    value="Closed",
                )
                ride_status_closed.pack(side="left")

                label_ride_capacity = tk.Label(update_window, text="Ride Capacity:")
                label_ride_capacity.pack()
                entry_ride_capacity = tk.Entry(update_window)
                entry_ride_capacity.insert(0, found_record["Ride Capacity"])
                entry_ride_capacity.pack()

                label_ride_rating = tk.Label(update_window, text="Ride Rating:")
                label_ride_rating.pack()

                ride_rating_var = tk.IntVar()
                ride_rating_var.set(int(found_record["Ride Rating"]))

                ride_rating_frame = tk.Frame(update_window)
                ride_rating_frame.pack()

                stars = []

                def set_ride_rating(rating):
                    ride_rating_var.set(rating)
                    for i in range(rating):
                        stars[i].config(text="★")
                    for i in range(rating, 5):
                        stars[i].config(text="☆")

                for i in range(5):
                    star_label = tk.Label(
                        ride_rating_frame, text="☆", font=("Arial", 20)
                    )
                    star_label.pack(side="left")
                    star_label.bind(
                        "<Button-1>",
                        lambda event, rating=i + 1: set_ride_rating(rating),
                    )
                    stars.append(star_label)

                button_update = tk.Button(
                    update_window,
                    text="Update",
                    command=lambda: perform_update(
                        entry_ride_id.get(),
                        entry_ride_name.get(),
                        ride_status_var.get(),
                        entry_ride_capacity.get(),
                        ride_rating_var.get(),
                    ),
                )
                button_update.pack()

            else:
                messagebox.showerror("Error", "Record not found.")
    else:
        messagebox.showerror("Error", "Please enter the Ride ID.")


def perform_update(ride_id, ride_name, ride_status, ride_capacity, ride_rating):
    if ride_id:
        with open("records.txt", "r") as file:
            lines = file.readlines()

        with open("records.txt", "w") as file:
            updated = False
            for line in lines:
                record_data = line.strip().split(",")
                if record_data[0] == ride_id:
                    updated = True
                    new_line = f"{ride_id},{ride_name},{ride_status},{ride_capacity},{ride_rating}\n"
                    file.write(new_line)
                else:
                    file.write(line)

            if updated:
                messagebox.showinfo("Success", "Record updated successfully!")
            else:
                messagebox.showerror("Error", "Record not found.")
    else:
        messagebox.showerror("Error", "Please enter the Ride ID.")


def delete_record():
    # Create a new window for deleting a record
    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Record")

    label_ride_id = tk.Label(delete_window, text="Ride ID:")
    label_ride_id.pack()
    entry_ride_id = tk.Entry(delete_window)
    entry_ride_id.pack()

    # Create and pack the delete button
    button_delete = tk.Button(
        delete_window,
        text="Delete",
        command=lambda: perform_delete(entry_ride_id.get()),
    )
    button_delete.pack()


def perform_delete(ride_id):
    if ride_id:
        with open("records.txt", "r") as file:
            lines = file.readlines()

        with open("records.txt", "w") as file:
            deleted = False
            for line in lines:
                record_data = line.strip().split(",")
                if record_data[0] == ride_id:
                    deleted = True
                else:
                    file.write(line)

            if deleted:
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showerror("Error", "Record not found.")
    else:
        messagebox.showerror("Error", "Please enter the Ride ID.")


# Function to handle the "Update Record" button click
def update_record():
    # Create a new window for searching a record
    search_window = tk.Toplevel(window)
    search_window.title("Search Record")

    label_ride_id = tk.Label(search_window, text="Ride ID:")
    label_ride_id.pack()
    entry_ride_id = tk.Entry(search_window)
    entry_ride_id.pack()

    button_search = tk.Button(
        search_window,
        text="Search",
        command=lambda: perform_search_update(entry_ride_id.get()),
    )
    button_search.pack()


# Function to handle the "View Records" button click
def view_records():
    # Create a new window to display the records
    records_window = tk.Toplevel(window)
    records_window.title("Records")

    # Create the table to display records
    table = ttk.Treeview(records_window)

    # Define columns
    table["columns"] = (
        "Ride ID",
        "Ride Name",
        "Ride Status",
        "Ride Capacity",
        "Ride Rating",
    )

    # Format columns
    table.column("#0", width=0, stretch=tk.NO)  # Hide the first empty column
    table.column("Ride ID", width=70, anchor=tk.CENTER)
    table.column("Ride Name", width=120, anchor=tk.W)
    table.column("Ride Status", width=80, anchor=tk.CENTER)
    table.column("Ride Capacity", width=100, anchor=tk.CENTER)
    table.column("Ride Rating", width=100, anchor=tk.CENTER)

    # Create headings
    table.heading("#0", text="", anchor=tk.W)
    table.heading("Ride ID", text="Ride ID", anchor=tk.CENTER)
    table.heading("Ride Name", text="Ride Name", anchor=tk.W)
    table.heading("Ride Status", text="Ride Status", anchor=tk.CENTER)
    table.heading("Ride Capacity", text="Ride Capacity", anchor=tk.CENTER)
    table.heading("Ride Rating", text="Ride Rating", anchor=tk.CENTER)

    # Retrieve records from the text file
    with open("records.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        record_data = line.strip().split(",")
        table.insert("", tk.END, values=record_data)

    # Add the table to the window
    table.pack(expand=True, fill=tk.BOTH)

    # Adjust window size based on the number of records
    window_width = 600
    window_height = (
        len(lines) * 25 + 40
    )  # Adjust the height based on the number of records
    records_window.geometry(f"{window_width}x{window_height}")


# Create the main window
window = tk.Tk()
window.title("Amusement Park Admin Panel")

# window.attributes("-fullscreen", True)

background_image = Image.open("bg.jpg")
resized_image = background_image.resize((1000, 500), resample=Image.LANCZOS)
background_photo = ImageTk.PhotoImage(resized_image)
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_photo

# Create and pack the widgets
label_ride_id = tk.Label(window, text="Ride ID:")
label_ride_id.pack()
entry_ride_id = tk.Entry(window)
entry_ride_id.pack()

label_ride_name = tk.Label(window, text="Ride Name:")
label_ride_name.pack()
entry_ride_name = tk.Entry(window)
entry_ride_name.pack()

label_ride_status = tk.Label(window, text="Ride Status:")
label_ride_status.pack()
ride_status_var = tk.StringVar()
ride_status_var.set(None)
ride_status_frame = tk.Frame(window)
ride_status_frame.pack()
ride_status_open = tk.Radiobutton(
    ride_status_frame, text="Open", variable=ride_status_var, value="Open"
)
ride_status_open.pack(side="left")
ride_status_closed = tk.Radiobutton(
    ride_status_frame, text="Closed", variable=ride_status_var, value="Closed"
)
ride_status_closed.pack(side="left")

label_ride_capacity = tk.Label(window, text="Ride Capacity:")
label_ride_capacity.pack()
entry_ride_capacity = tk.Entry(window)
entry_ride_capacity.pack()


label_ride_rating = tk.Label(window, text="Ride Rating:")
label_ride_rating.pack()

ride_rating_var = tk.IntVar()

ride_rating_frame = tk.Frame(window)
ride_rating_frame.pack()

stars = []


def set_ride_rating(rating):
    ride_rating_var.set(rating)
    for i in range(rating):
        stars[i].config(text="★")
    for i in range(rating, 5):
        stars[i].config(text="☆")


for i in range(5):
    star_label = tk.Label(ride_rating_frame, text="☆", font=("Arial", 20))
    star_label.pack(side="left")
    star_label.bind("<Button-1>", lambda event, rating=i + 1: set_ride_rating(rating))
    stars.append(star_label)


button_frame = tk.Frame(window)
button_frame.pack(pady=10)

button_add = tk.Button(button_frame, text="Add Record", command=add_record)
button_add.pack(side="left", padx=10)

button_delete = tk.Button(button_frame, text="Delete Record", command=delete_record)
button_delete.pack(side="left", padx=10)

button_update = tk.Button(button_frame, text="Update Record", command=update_record)
button_update.pack(side="left", padx=10)

button_search = tk.Button(button_frame, text="Search Record", command=search_record)
button_search.pack(side="left", padx=10)

button_view = tk.Button(button_frame, text="View Records", command=view_records)
button_view.pack(side="left", padx=10)


def authenticate(username, password):
    with open("accounts.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if (
                username == stored_username
                and hash_password(password) == stored_password
            ):
                return True
    return False


def create_user(username, password):
    with open("accounts.txt", "a") as file:
        hashed_password = hash_password(password)
        file.write(f"{username}:{hashed_password}\n")


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def show_signup_window():
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")

    label_username = tk.Label(signup_window, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(signup_window)
    entry_username.pack()

    label_password = tk.Label(signup_window, text="Password:")
    label_password.pack()
    entry_password = tk.Entry(signup_window, show="*")
    entry_password.pack()

    button_signup = tk.Button(
        signup_window,
        text="Sign Up",
        command=lambda: signup(entry_username.get(), entry_password.get()),
    )
    button_signup.pack(pady=10)
    signup_window.destroy()


def signup(username, password):
    if username and password:
        create_user(username, password)
        messagebox.showinfo("Success", "New user created successfully.")
    else:
        messagebox.showerror("Error", "Username and password are required.")


def login():
    username = entry_username.get()
    password = entry_password.get()

    if authenticate(username, password):
        window.deiconify()  # Show the main window
        login_window.destroy()  # Close the login window

    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


window.withdraw()  # Hide the main window initially

login_window = tk.Toplevel(window)
login_window.title("Login")

label_username = tk.Label(login_window, text="Username:")
label_username.pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

label_password = tk.Label(login_window, text="Password:")
label_password.pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

button_login = tk.Button(login_window, text="Login", command=login)
button_login.pack(pady=10)

button_signup = tk.Button(login_window, text="Sign Up", command=show_signup_window)
button_signup.pack()

login_window.geometry("1000x500")
login_window.mainloop()

window.geometry("1000x500")
window.mainloop()
