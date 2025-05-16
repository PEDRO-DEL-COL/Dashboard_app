import tkinter as tk
from tkinter import messagebox

class DeleteCompanyPopup(tk.Frame):
    def __init__(self, parent, companies, on_delete_callback):
        super().__init__(parent)
        self.parent = parent
        self.companies = companies
        self.on_delete_callback = on_delete_callback

        tk.Label(self, text="Select a Company to Delete").pack(pady=10)

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack(pady=10)

        for company in self.companies:
            self.listbox.insert(tk.END, f"{company.name} ({company.companyId})")

        delete_button = tk.Button(self, text="Delete", command=self.delete_selected)
        delete_button.pack(pady=10)

    def delete_selected(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a company to delete.")
            return

        company_to_delete = self.companies[selected_index[0]]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{company_to_delete.name}'?")
        if confirm:
            del self.companies[selected_index[0]]
            self.on_delete_callback()
            self.parent.destroy()
