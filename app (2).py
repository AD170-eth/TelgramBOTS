import asyncio, json, random
import time
import tkinter as tk
from tkinter import messagebox
from telethon import TelegramClient, types
from telethon.sync import TelegramClient
from telethon.tl.types import MessageService


class AddMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add member')

        # Phone number input
        tk.Label(self, text='Phone number:').grid(row=0, column=0)
        self.phone_number_var = tk.StringVar()
        tk.Entry(self, textvariable=self.phone_number_var).grid(row=0, column=1)

        # API hash input
        tk.Label(self, text='API hash:').grid(row=1, column=0)
        self.apihash_var = tk.StringVar()
        tk.Entry(self, textvariable=self.apihash_var).grid(row=1, column=1)

        # API ID input
        tk.Label(self, text='API ID:').grid(row=2, column=0)
        self.apiid_var = tk.StringVar()
        tk.Entry(self, textvariable=self.apiid_var).grid(row=2, column=1)

        # Add button
        tk.Button(self, text='Add', command=self.add_member).grid(row=3, column=0, columnspan=2)

    def add_member(self):
        # Get inputs
        phone_number = self.phone_number_var.get()
        apihash = self.apihash_var.get()
        apiid = self.apiid_var.get()

        with open('database.json', 'r') as f:
            # load the existing data from the file
            database = json.load(f)

        # make sure the loaded data is a list
        if not isinstance(database, list):
            database = []

        # append the new data to the list
        database.append({
            'phonenum': phone_number,
            'apihash': apihash,
            'apiid': apiid,
            'groups': []
        })

        with open('database.json', 'w') as f:
            # save the updated data to the file
            json.dump(database, f)
        print('Added new user\nPhone number: {}\nAPI hash: {}\nAPI ID: {}'.format(phone_number, apihash, apiid))
        # Close window
        self.destroy()
        messagebox.showinfo("Success", "Member added successfully.")

class RemoveMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Remove Member")
        self.geometry("300x150")
        self.resizable(False, False)
        self.parent = parent

        # Labels
        tk.Label(self, text="Enter Phone Number:").grid(row=0, column=0, padx=5, pady=5)

        # Entry
        self.phone_number_entry = tk.Entry(self, width=30)
        self.phone_number_entry.grid(row=0, column=1, padx=5, pady=5)

        # Add button
        tk.Button(self, text="Remove Member", command=self.remove_member).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def remove_member(self):
        phone_number = self.phone_number_entry.get()

        with open('database.json', 'r') as f:
            # load the existing data from the file
            database = json.load(f)
        
        # Remove member from database and if not found, show error
        for account in database:
            if account['phonenum'] == phone_number:
                database.remove(account)
                break
        else:
            self.destroy()
            messagebox.showerror("Error", "Member not found.")
            return
    
        # Save database
        with open('database.json', 'w') as f:
            # save the updated data to the file
            json.dump(database, f)
        
        # Close window
        self.destroy()
        messagebox.showinfo("Success", "Member removed successfully.")
        print('Removed user\nPhone number: {}'.format(phone_number))

class AddMemberToGroupWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("Add Member to Group")

        tk.Label(self, text="Phone Number: ").grid(row=0, sticky="W")
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=0, column=1)

        tk.Label(self, text="Group ID: ").grid(row=1, sticky="W")
        self.group_entry = tk.Entry(self)
        self.group_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self, text="Add Member", command=self.add_member)
        self.add_button.grid(row=2, column=1)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=2, column=0)

    def add_member(self):
        phone_number = self.phone_entry.get().strip()
        group_id = self.group_entry.get().strip()
        if phone_number == "" or group_id == "":
            messagebox.showerror("Error", "Please enter a phone number and group ID.")
            return
        try:
            with open('database.json', 'r') as f:
                # load the existing data from the file
                database = json.load(f)
            for account in database:
                if account['phonenum'] == phone_number:
                    account['groups'].append(group_id)
                    break
            else:
                self.destroy()
                messagebox.showerror("Error", "Member not found.")
                return
            with open('database.json', 'w') as f:
                # save the updated data to the file
                json.dump(database, f)
            self.destroy()
            messagebox.showinfo("Success", "Member added to group successfully.")
            print('Added user to group\nPhone number: {}\nGroup ID: {}'.format(phone_number, group_id))
        except Exception as e:
            self.destroy()
            messagebox.showerror("Error", "An error occurred.")
            print(e)


class ChangeMemberGroupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Change Member Group")
        self.geometry("400x200")
        self.resizable(False, False)
        self.parent = parent

        # Labels
        tk.Label(self, text="Enter Phone Number:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Enter New Group ID:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text="Enter Old Group ID:").grid(row=2, column=0, padx=5, pady=5)

        # Entry
        self.phone_number_entry = tk.Entry(self, width=30)
        self.phone_number_entry.grid(row=0, column=1, padx=5, pady=5)
        self.new_group_id_entry = tk.Entry(self, width=30)
        self.new_group_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.old_group_id_entry = tk.Entry(self, width=30)
        self.old_group_id_entry.grid(row=2, column=1, padx=5, pady=5)

        # Add button
        tk.Button(self, text="Change Group", command=self.change_group).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def change_group(self):
        phone_number = self.phone_number_entry.get()
        new_group_id = self.new_group_id_entry.get()
        old_group_id = self.old_group_id_entry.get()

        with open('database.json', 'r') as f:
            # load the existing data from the file
            database = json.load(f)

        # Change group of member and if not found, show error
        for account in database:
            if account['phonenum'] == phone_number:
                if old_group_id in account['groups']:
                    account['groups'].remove(old_group_id)
                    account['groups'].append(new_group_id)
                    break
                else:
                    # If old group id not found, show error
                    messagebox.showerror("Error", "Old group ID not found.")
                    return
        else:
            messagebox.showerror("Error", "Member not found.")
            return

        # Save database
        with open('database.json', 'w') as f:
            # save the updated data to the file
            json.dump(database, f)
        
        # Close window
        self.destroy()
        messagebox.showinfo("Success", "Member group changed successfully.")
        print("Changed group of member with phone number:", phone_number, "from group", old_group_id, "to group", new_group_id)

class RemoveMemberFromGroupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Remove Member from Group")
        self.geometry("400x200")
        self.resizable(False, False)
        self.parent = parent

        # Labels
        tk.Label(self, text="Enter Phone Number:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Enter Group ID:").grid(row=1, column=0, padx=5, pady=5)

        # Entry
        self.phone_number_entry = tk.Entry(self, width=30)
        self.phone_number_entry.grid(row=0, column=1, padx=5, pady=5)
        self.group_id_entry = tk.Entry(self, width=30)
        self.group_id_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add button
        tk.Button(self, text="Remove Member", command=self.group_remove).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    def group_remove(self):
        phone_number = self.phone_number_entry.get()
        group_id = self.group_id_entry.get()

        with open('database.json', 'r') as f:
            # load the existing data from the file
            database = json.load(f)

        # Remove member from group and if not found, show error
        for account in database:
            if account['phonenum'] == phone_number:
                if group_id in account['groups']:
                    account['groups'].remove(group_id)
                    break
                else:
                    # If group id not found, show error
                    self.destroy()
                    messagebox.showerror("Error", "Group ID not found.")
                    return
        else:
            self.destroy()
            messagebox.showerror("Error", "Member not found.")
            return

        # Save database
        with open('database.json', 'w') as f:
            # save the updated data to the file
            json.dump(database, f)
        
        # Close window
        self.destroy()
        messagebox.showinfo("Success", "Member removed from group successfully.")
        print("Removed member with phone number:", phone_number, "from group", group_id)


class ForwardMessagesWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Forward Messages")

        # Create label and entry widgets for source group id
        tk.Label(self, text="Source Group ID: ").grid(row=0, column=0, padx=5, pady=5)
        self.source_group_id_entry = tk.Entry(self)
        self.source_group_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create label and entry widgets for target group id
        tk.Label(self, text="Target Group ID: ").grid(row=1, column=0, padx=5, pady=5)
        self.target_group_id_entry = tk.Entry(self)
        self.target_group_id_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create label and entry widgets for cycle time
        tk.Label(self, text="Cycle Time (in seconds): ").grid(row=2, column=0, padx=5, pady=5)
        self.cycle_time_entry = tk.Entry(self)
        self.cycle_time_entry.grid(row=2, column=1, padx=5, pady=5)

        # Create label and entry widgets for forward count
        tk.Label(self, text="Forward Count: ").grid(row=3, column=0, padx=5, pady=5)
        self.forward_count_entry = tk.Entry(self)
        self.forward_count_entry.grid(row=3, column=1, padx=5, pady=5)

        # Create dropdown menu for account type selection
        self.account_type_var = tk.StringVar(self)
        self.account_type_var.set("Auto Account")  # default value
        self.account_type_menu = tk.OptionMenu(self, self.account_type_var, "Auto Account", "Manual Account")
        self.account_type_menu.grid(row=4, column=0, padx=5, pady=5)

        # Create label and entry widgets for manual account input
        self.manual_account_entry = tk.Entry(self, state="disabled")
        self.manual_account_entry.grid(row=4, column=1, padx=5, pady=5)

        # Bind dropdown menu selection to show/hide manual account entry
        self.account_type_var.trace("w", self.toggle_manual_account_entry)

        # Create forward button
        tk.Button(self, text="Forward", command=self.forward_messages).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def toggle_manual_account_entry(self, *args):
        """
        Toggle state of manual account entry based on account type selection
        """
        if self.account_type_var.get() == "Manual Account":
            self.manual_account_entry.config(state="normal")
        else:
            self.manual_account_entry.config(state="disabled")

    def forward_messages(self):
            # Get user input
            source_group_id = self.source_group_id_entry.get().strip()
            target_group_id = self.target_group_id_entry.get().strip()
            cycle_time = self.cycle_time_entry.get().strip()
            forward_count = self.forward_count_entry.get().strip()

            # Check if user input is valid
            if not source_group_id or not target_group_id or not cycle_time or not forward_count:
                messagebox.showerror("Error", "Please fill all fields")
                return

            try:
                cycle_time = int(cycle_time)
                forward_count = int(forward_count)
            except ValueError:
                messagebox.showerror("Error", "Cycle time and Forward count must be integers")
                return

            # Check if user wants to use auto account or manual account
            if self.account_type_var.get() == "Auto Account":
                None

            elif self.account_type_var.get() == "Manual Account":
                # Check if user provided phone number
                phone_number = self.manual_account_entry.get().strip()
                if not phone_number:
                    messagebox.showerror("Error", "Please enter phone number")
                    return
                
                # Check if phone number is registered
                with open('database.json', 'r') as f:
                    database = json.load(f)
                for account in database:
                    if account['phonenum'] == phone_number:
                        break
                else:
                    messagebox.showerror("Error", "Phone number not registered")
                    return

                 # Check if is subscribed to the source group
                if any(source_group_id == group for item in database for group in account['groups']):
                    pass
                else:
                    messagebox.showerror("Error", "Phone number not subscribed to source group")
                    return
                
                if any(target_group_id == group for item in database for group in account['groups']):
                    pass
                else:
                    messagebox.showerror("Error", "Phone number not subscribed to target group")
                    return

                # Create the client object
                # apiid and apihash get them
                for item in database:
                    if item["phonenum"] == phone_number:
                        apiid = item["apiid"]
                        apihash = item["apihash"]
                        break
                session = ("forwarder" + str(random.randint(100000, 999999)))
                client = TelegramClient(session, apiid, apihash)
                # Login
                client.start(phone_number)
                # Now, we have to do the forwarding
                # Get the entity of the source and target groups
                source_group = client.get_entity(source_group_id)
                target_group = client.get_entity(target_group_id)
                count = 0
                while True:
                    # Forward messages
                    for message in client.iter_messages(source_group):
                        if not isinstance(message, MessageService):
                            client.forward_messages(target_group, message)
                            count += 1
                    if count >= forward_count:
                        break
                    time.sleep(cycle_time)
                # Close the client
                client.disconnect()      
            else:
                raise ValueError("Invalid account type")
            


class ApplicationWindow(tk.Tk):
    def __init__(self, database_path):
        super().__init__()

        # Set window title
        self.title("Automation Bot")

        # Add member button
        add_member_button = tk.Button(self, text="Add Member", command=self.add_member_window)
        add_member_button.pack(pady=10)

        # Remove member button
        remove_member_button = tk.Button(self, text="Remove Member", command=self.remove_member_window)
        remove_member_button.pack(pady=10)

        # Add member to group button
        add_member_to_group_button = tk.Button(self, text="Add Member to Group", command=self.add_member_to_group_window)
        add_member_to_group_button.pack(pady=10)

        # Remove member from group button
        remove_member_from_group_button = tk.Button(self, text="Remove Member from Group", command=self.remove_member_from_group_window)
        remove_member_from_group_button.pack(pady=10)

        # Change groups of member button
        change_groups_button = tk.Button(self, text="Change Groups of Member", command=self.change_groups_window)
        change_groups_button.pack(pady=10)

        # Forward messages button
        forward_messages_button = tk.Button(self, text="Forward Messages", command=self.forward_messages_window)
        forward_messages_button.pack(pady=10)

    def add_member_window(self):
        add_member_window = AddMemberWindow(self)
        add_member_window.grab_set()

    def remove_member_window(self):
        remove_member_window = RemoveMemberWindow(self)
        remove_member_window.grab_set()

    def add_member_to_group_window(self):
        add_member_to_group_window = AddMemberToGroupWindow(self)
        add_member_to_group_window.grab_set()

    def remove_member_from_group_window(self):
        remove_member_from_group_window = RemoveMemberFromGroupWindow(self)
        remove_member_from_group_window.grab_set()

    def change_groups_window(self):
        change_groups_window = ChangeMemberGroupWindow(self)
        change_groups_window.grab_set()

    def forward_messages_window(self):
        forward_messages_window = ForwardMessagesWindow(self)
        forward_messages_window.grab_set()

    def run(self):
        self.mainloop()

# Run the application
if __name__ == "__main__":
    app = ApplicationWindow("database.json")
    app.run()