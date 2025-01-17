import os
from tkinter import Tk, Label, Button, Frame, filedialog, Listbox, Scrollbar, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES  # Import drag-and-drop support
from PyPDF2 import PdfMerger

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

# Main GUI setup using TkinterDnD for drag-and-drop
root = TkinterDnD.Tk()  # Use TkinterDnD.Tk() instead of Tk()
root.title("PDF Merger Tool by Shashwat")
root.geometry("500x400")
root.config(bg="#f4f4f4")

# Title Label
Label(
    root,
    text="PDF Merger Tool",
    font=("Arial", 18, "bold"),
    fg="#333",
    bg="#f4f4f4",
).pack(pady=10)

# Drag-and-drop frame
drag_drop_frame = Frame(root, bg="#e0e0e0", height=150, width=400, relief="sunken", bd=2)
drag_drop_frame.pack(pady=10)
drag_drop_frame.pack_propagate(False)

Label(
    drag_drop_frame,
    text="Drag and Drop PDF files here",
    font=("Arial", 12),
    fg="#666",
    bg="#e0e0e0",
).pack(expand=True)

# Register the drag-and-drop event
drag_drop_frame.drop_target_register(DND_FILES)
drag_drop_frame.dnd_bind('<<Drop>>', handle_drop)

# Listbox for displaying selected files
file_list_frame = Frame(root, bg="#f4f4f4")
file_list_frame.pack(pady=10)

scrollbar = Scrollbar(file_list_frame, orient="vertical")
file_listbox = Listbox(
    file_list_frame,
    width=60,
    height=8,
    yscrollcommand=scrollbar.set,
    selectmode="multiple",
)
scrollbar.config(command=file_listbox.yview)
scrollbar.pack(side="right", fill="y")
file_listbox.pack(side="left", fill="both", expand=True)

# Buttons
Button(root, text="Add Files", command=add_files, bg="#4CAF50", fg="white", width=15).pack(pady=5)
Button(root, text="Merge PDFs", command=merge_pdfs, bg="#2196F3", fg="white", width=15).pack(pady=5)
Button(root, text="Clear List", command=clear_list, bg="#f44336", fg="white", width=15).pack(pady=5)

# Run the GUI
root.mainloop()
