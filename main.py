import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
import os

class MetadataRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metadata Remover")
        self.root.geometry("500x300")
        self.root.configure(bg='#2e3b4e')

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TFrame', background='#2e3b4e')
        style.configure('TLabel', background='#2e3b4e', foreground='white', font=('Helvetica', 12))
        style.configure('TButton', background='#4a90e2', foreground='white', font=('Helvetica', 12, 'bold'))
        style.configure('TProgressbar', troughcolor='#2e3b4e', background='#4a90e2')

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.label = ttk.Label(frame, text="Select an image file to remove all metadata")
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.select_button = ttk.Button(frame, text="Select Image", command=self.select_image)
        self.select_button.grid(row=1, column=0, pady=10, padx=5, sticky=(tk.W, tk.E))

        self.save_button = ttk.Button(frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.grid(row=1, column=1, pady=10, padx=5, sticky=(tk.W, tk.E))

        self.progress = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))

    def select_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.heic;*.webp")]
        )
        if self.file_path:
            self.save_button.state(['!disabled'])
            self.label.config(text=os.path.basename(self.file_path))

    def save_image(self):
        file_extension = os.path.splitext(self.file_path)[1].lower()
        output_path = filedialog.asksaveasfilename(
            defaultextension=file_extension,
            filetypes=[("Image files", f"*{file_extension}")]
        )
        if output_path:
            self.remove_all_metadata(self.file_path, output_path)
            messagebox.showinfo("Success", "All metadata removed and image saved successfully.")
            self.label.config(text="Select an image file to remove all metadata")
            self.save_button.state(['disabled'])
            self.progress['value'] = 0

    def remove_all_metadata(self, image_path, output_path):
        image = Image.open(image_path)
        data = list(image.getdata())
        mode = image.mode
        size = image.size

        clean_image = Image.new(mode, size)
        clean_image.putdata(data)

        # Save without any metadata
        if image.format == 'JPEG':
            clean_image.save(output_path, 'JPEG', quality=95)
        elif image.format == 'PNG':
            clean_image.save(output_path, 'PNG')
        elif image.format == 'HEIC':
            clean_image.save(output_path, 'HEIC')
        elif image.format == 'WEBP':
            clean_image.save(output_path, 'WEBP', quality=95)
        else:
            clean_image.save(output_path)

        self.progress['value'] = 100

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataRemoverApp(root)
    root.mainloop()
