import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")

        self.image_label = tk.Label(self.root, text="No Image Loaded", bg="gray", width=40, height=10)
        self.image_label.pack(pady=10)

        self.encrypt_button = tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image, state=tk.DISABLED)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image, state=tk.DISABLED)
        self.decrypt_button.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        self.image = None
        self.original_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.display_image(self.image)
            self.encrypt_button.config(state=tk.NORMAL)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")]
        )
        if file_path and self.image:
            # Convert to RGB if saving as JPEG
            if file_path.lower().endswith((".jpg", ".jpeg")) and self.image.mode == "RGBA":
                self.image = self.image.convert("RGB")
            try:
                self.image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

    def display_image(self, image):
        img_resized = image.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img_resized)
        self.image_label.config(image=img_tk, text="")
        self.image_label.image = img_tk

    def encrypt_image(self):
        if self.image:
            np_image = np.array(self.image, dtype=np.uint8)
            np_encrypted = (np_image + 50).astype(np.uint8)  # Ensure the result is uint8
            self.image = Image.fromarray(np_encrypted)
            self.display_image(self.image)
            self.decrypt_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)

    def decrypt_image(self):
        if self.image:
            np_image = np.array(self.image, dtype=np.uint8)
            np_decrypted = (np_image - 50).astype(np.uint8)  # Ensure the result is uint8
            self.image = Image.fromarray(np_decrypted)
            self.display_image(self.image)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()