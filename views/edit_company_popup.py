import tkinter as tk
from tkinter import messagebox

class EditCompanyPopup(tk.Toplevel):
    def __init__(self, master, companies, on_edit_callback):
        super().__init__(master)
        self.title("Edit Company")
        self.geometry("400x300")
        self.companies = companies
        self.on_edit_callback = on_edit_callback
        self.selected_index = None

        tk.Label(self, text="Select a company").pack(pady=5)
        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack(pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        tk.Label(self, text="New name").pack(pady=5)
        self.entry_name = tk.Entry(self, width=40)
        self.entry_name.pack(pady=5)

        tk.Button(self, text="Save Changes", command=self.edit_company).pack(pady=10)

        self.update_company_list()

    def update_company_list(self):
        self.listbox.delete(0, tk.END)
        for company in self.companies:
            self.listbox.insert(tk.END, f"{company.name} ({company.companyId})")

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            selected_company = self.companies[self.selected_index]
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, selected_company.name)

    def edit_company(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Please select a company.")
            return

        new_name = self.entry_name.get().strip()
        if not new_name:
            messagebox.showwarning("Warning", "Company name cannot be empty.")
            return

        self.companies[self.selected_index].name = new_name
        self.on_edit_callback()
        messagebox.showinfo("Success", "Company name updated.")
        self.destroy()
