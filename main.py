import os
import shutil
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox


def fetch_saves():
    saves_list.delete(0, tk.END)
    for save_folder in os.listdir(save_path):
        saves_list.insert(tk.END, save_folder)


def import_saves():
    print("Import function invoked")

    folder_selected = filedialog.askdirectory(title="Select the save folder to import")
    if not folder_selected:
        print("No folder selected for import. Exiting function.")
        return

    save_folder_name = os.path.basename(folder_selected)
    dest_folder_path = os.path.join(save_path, save_folder_name)

    print(f"Source for import: {folder_selected}")
    print(f"Destination for import: {dest_folder_path}")

    try:
        if os.path.isdir(folder_selected):
            shutil.copytree(folder_selected, dest_folder_path)
        else:
            print(f"'{folder_selected}' is not a directory.")
    except Exception as e:
        print(f"Error during import: {e}")
    else:
        messagebox.showinfo("Success", "Save imported successfully!")
        fetch_saves()


def export_saves():
    folder_selected = filedialog.askdirectory(
        title="Select destination for ZIP archive"
    )
    if not folder_selected:
        print("No destination selected for export. Exiting function.")
        return

    selected_saves = saves_list.curselection()
    for save_index in selected_saves:
        save_folder = saves_list.get(save_index)
        src_folder_path = os.path.join(save_path, save_folder)

        # The destination path for the ZIP will be in the selected folder
        # and the ZIP will be named after the save folder
        zip_dest_path = os.path.join(folder_selected, save_folder)

        print(f"Source: {src_folder_path}")
        print(f"Destination ZIP: {zip_dest_path}.zip")

        try:
            shutil.make_archive(zip_dest_path, "zip", src_folder_path)
        except Exception as e:
            print(f"Error during zipping: {e}")

    messagebox.showinfo("Success", "Selected saves exported successfully as ZIP!")


# Paths
username = os.getlogin()
save_path = f"C:\\Users\\{username}\\AppData\\Local\\Larian Studios\\Baldur's Gate 3\\PlayerProfiles\\Public\\Savegames\\Story"
dest_path = os.path.join(os.getcwd(), "BaldurGate3Saves")
if not os.path.exists(dest_path):
    os.mkdir(dest_path)

# GUI setup
root = tk.Tk()
root.title("Baldur's Gate 3 Save Manager")

# Add a listbox to display save names
saves_list = Listbox(root, selectmode=tk.MULTIPLE, width=60, height=20)
saves_list.pack(pady=20)

fetch_saves()

# Add Import and Export buttons
import_btn = tk.Button(root, text="Import Selected Saves", command=import_saves)
import_btn.pack(pady=10)

export_btn = tk.Button(root, text="Export Selected Saves", command=export_saves)
export_btn.pack(pady=10)

root.mainloop()
