import os
from tkinter import Tk, Label, Button, Frame, filedialog, Listbox, Scrollbar, messagebox
from PyPDF2 import PdfMerger
import datetime

# Global variable to store selected PDF files
pdf_files = []

# Function to add files via file dialog
def add_files():
    global pdf_files
    files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")],
    )
    for file in files:
        if file not in pdf_files:
            pdf_files.append(file)
            file_listbox.insert("end", os.path.basename(file))

# Function to merge selected PDFs
def merge_pdfs():
    global pdf_files
    if not pdf_files:
        messagebox.showerror("Error", "No PDF files selected!")
        return

    output_file = filedialog.asksaveasfilename(
        title="Save Merged PDF As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
    )
    if not output_file:
        return

    try:
        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(pdf)
        merger.write(output_file)
        merger.close()

        messagebox.showinfo("Success", f"Merged PDF saved as: {output_file}")
        clear_list()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to clear the file list
def clear_list():
    global pdf_files
    pdf_files = []
    file_listbox.delete(0, "end")

# Function to handle drag-and-drop events
def handle_drop(event):
    global pdf_files
    dragged_files = event.data.splitlines()
    for file in dragged_files:
        if file.endswith('.pdf') and file not in pdf_files:
            pdf_files.append(file)
            file_listbox.insert("end", os.path.basename(file))

# Move a file up in the list
def moveFileUP():
    global pdf_files
    selected_indices = file_listbox.curselection()
    if not selected_indices:
        return  # No selection

    index = selected_indices[0]
    if index > 0:  # Ensure it's not the first item
        # Swap in the list
        pdf_files[index], pdf_files[index - 1] = pdf_files[index - 1], pdf_files[index]
        
        # Update the listbox
        file_listbox.delete(index)
        file_listbox.insert(index - 1, os.path.basename(pdf_files[index - 1]))
        file_listbox.selection_set(index - 1)  # Maintain selection

# Move a file down in the list
def moveFileDown():
    global pdf_files
    selected_indices = file_listbox.curselection()
    if not selected_indices:
        return  # No selection

    index = selected_indices[0]
    if index < len(pdf_files) - 1:  # Ensure it's not the last item
        # Swap in the list
        pdf_files[index], pdf_files[index + 1] = pdf_files[index + 1], pdf_files[index]
        
        # Update the listbox
        file_listbox.delete(index)
        file_listbox.insert(index + 1, os.path.basename(pdf_files[index + 1]))
        file_listbox.selection_set(index + 1)  # Maintain selection

# Main GUI setup
root = Tk()
root.title("PDF Merger Tool by Shashwat")
root.geometry("500x500")
root.config(bg="#f4f4f4")

# Title Label
Label(
    root,
    text="PDF Merger Tool",
    font=("Arial", 20, "bold"),
    fg="#333",
    bg="#f4f4f4",
).pack(pady=10)

# Listbox for displaying selected files
file_list_frame = Frame(root, bg="#f4f4f4")
file_list_frame.pack(pady=10, padx=20)

scrollbar = Scrollbar(file_list_frame, orient="vertical")
file_listbox = Listbox(
    file_list_frame,
    width=50,
    height=8,
    yscrollcommand=scrollbar.set,
    selectmode="single",  # Changed from "multiple" to "single" for Move Up/Down
    font=("Arial", 12),
)
scrollbar.config(command=file_listbox.yview)
scrollbar.pack(side="right", fill="y")
file_listbox.pack(side="left", fill="both", expand=True)

# Buttons Section
button_frame = Frame(root, bg="#f4f4f4")
button_frame.pack(pady=15)

Button(
    button_frame,
    text="Move Up",
    command=moveFileUP,
    bg="#9ACBD0",
    fg="#ffffff",
    font=("Arial", 12, "bold"),
    width=15,
).grid(row=0, column=0, padx=10, pady=5)

Button(
    button_frame,
    text="Move Down",
    command=moveFileDown,
    bg="#9ACBD0",
    fg="#ffffff",
    font=("Arial", 12, "bold"),
    width=15,
).grid(row=0, column=1, padx=10, pady=5)

Button(
    button_frame,
    text="Add Files",
    command=add_files,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=15,
).grid(row=1, column=0, columnspan=2 ,padx=10, pady=5)

Button(
    button_frame,
    text="MERGE PDFs",  # Emphasized text
    command=merge_pdfs,
    bg="#3674B5",  # Eye-catching color
    fg="white",
    font=("Arial", 12, "bold"),  # Larger size and bold
    width=15,
    relief="raised",  # 3D effect for emphasis
    bd=4,  # Thicker border
).grid(row=2, column=0,columnspan=2, padx=10, pady=5)

Button(
    button_frame,
    text="Clear List",
    command=clear_list,
    bg="#f44336",
    fg="white",
    font=("Arial", 12, "bold"),
    width=15,
).grid(row=3, column=0, columnspan=2, pady=5)

# Footer Label
Label(
    root,
    text="© All Rights Reserved " + str(datetime.datetime.now().year) + " by Shashwat Singh",
    font=("Arial", 10, "bold"),
    fg="#555",  # Subtle gray color
    bg="#f4f4f4"
).pack(side="bottom", pady=10)

# Run the GUI
root.mainloop()
