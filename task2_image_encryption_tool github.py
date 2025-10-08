import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os

class ImageEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool")
        self.root.geometry("800x600")
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.image_array = None
        self.encryption_key = tk.StringVar(value="12345")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Encryption Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Operations", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="Select Image", 
                  command=self.select_image).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(file_frame, text="Save Result", 
                  command=self.save_image).grid(row=0, column=1, padx=(0, 10))
        
        # Encryption settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Encryption Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(settings_frame, text="Encryption Key:").grid(row=0, column=0, padx=(0, 10))
        ttk.Entry(settings_frame, textvariable=self.encryption_key, 
                 width=20).grid(row=0, column=1, padx=(0, 20))
        
        # Operation buttons frame
        operations_frame = ttk.LabelFrame(main_frame, text="Operations", padding="10")
        operations_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(operations_frame, text="XOR Encrypt", 
                  command=self.xor_encrypt).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(operations_frame, text="XOR Decrypt", 
                  command=self.xor_decrypt).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(operations_frame, text="Pixel Swap Encrypt", 
                  command=self.pixel_swap_encrypt).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(operations_frame, text="Pixel Swap Decrypt", 
                  command=self.pixel_swap_decrypt).grid(row=0, column=3, padx=(0, 10))
        ttk.Button(operations_frame, text="Reset", 
                  command=self.reset_image).grid(row=0, column=4, padx=(0, 10))
        
        # Image display frame
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Original image
        self.original_label = ttk.Label(image_frame, text="Original Image")
        self.original_label.grid(row=0, column=0, padx=(0, 20))
        
        self.original_canvas = tk.Canvas(image_frame, width=300, height=300, bg="white", relief="sunken", bd=2)
        self.original_canvas.grid(row=1, column=0, padx=(0, 20))
        
        # Processed image
        self.processed_label = ttk.Label(image_frame, text="Processed Image")
        self.processed_label.grid(row=0, column=1)
        
        self.processed_canvas = tk.Canvas(image_frame, width=300, height=300, bg="white", relief="sunken", bd=2)
        self.processed_canvas.grid(row=1, column=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def select_image(self):
        """Select and load an image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.image_array = np.array(self.original_image)
                self.processed_image = self.original_image.copy()
                
                self.display_image(self.original_image, self.original_canvas)
                self.display_image(self.processed_image, self.processed_canvas)
                
                self.status_var.set(f"Loaded: {os.path.basename(file_path)} - Size: {self.original_image.size}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, canvas):
        """Display image on canvas with proper scaling"""
        if image is None:
            return
        
        canvas_width = canvas.winfo_width() or 300
        canvas_height = canvas.winfo_height() or 300
        
        img_copy = image.copy()
        img_copy.thumbnail((canvas_width-4, canvas_height-4), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img_copy)
        
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, image=photo, anchor="center")
        canvas.image = photo   # prevent garbage collection
    
    def get_int_key(self):
        """Convert string key into an integer (0–255)"""
        key_str = self.encryption_key.get()
        if not key_str:
            key_str = "12345"
        return sum(ord(c) for c in key_str) % 256
    
    def xor_encrypt(self):
        """Encrypt image using XOR operation"""
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        try:
            key = self.get_int_key()
            encrypted_array = np.bitwise_xor(self.image_array, key)
            self.processed_image = Image.fromarray(encrypted_array.astype(np.uint8))
            self.display_image(self.processed_image, self.processed_canvas)
            self.status_var.set("XOR encryption applied")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def xor_decrypt(self):
        """Decrypt image using XOR (same as encryption)"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image found!")
            return
        try:
            key = self.get_int_key()
            current_array = np.array(self.processed_image)
            decrypted_array = np.bitwise_xor(current_array, key)
            self.processed_image = Image.fromarray(decrypted_array.astype(np.uint8))
            self.display_image(self.processed_image, self.processed_canvas)
            self.status_var.set("XOR decryption applied")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def pixel_swap_encrypt(self):
        """Encrypt image by swapping pixels"""
        if self.image_array is None:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        try:
            encrypted_array = self.image_array.copy()
            height, width = encrypted_array.shape[:2]
            np.random.seed(self.get_int_key())
            num_swaps = min(1000, height * width // 4)
            for _ in range(num_swaps):
                y1, x1 = np.random.randint(0, height), np.random.randint(0, width)
                y2, x2 = np.random.randint(0, height), np.random.randint(0, width)
                encrypted_array[y1, x1], encrypted_array[y2, x2] = \
                    encrypted_array[y2, x2].copy(), encrypted_array[y1, x1].copy()
            self.processed_image = Image.fromarray(encrypted_array.astype(np.uint8))
            self.display_image(self.processed_image, self.processed_canvas)
            self.status_var.set("Pixel swap encryption applied")
        except Exception as e:
            messagebox.showerror("Error", f"Pixel swap encryption failed: {str(e)}")
    
    def pixel_swap_decrypt(self):
        """Decrypt image by reversing pixel swaps"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image found!")
            return
        try:
            current_array = np.array(self.processed_image)
            decrypted_array = current_array.copy()
            height, width = decrypted_array.shape[:2]
            np.random.seed(self.get_int_key())
            swap_positions = []
            num_swaps = min(1000, height * width // 4)
            for _ in range(num_swaps):
                y1, x1 = np.random.randint(0, height), np.random.randint(0, width)
                y2, x2 = np.random.randint(0, height), np.random.randint(0, width)
                swap_positions.append(((y1, x1), (y2, x2)))
            for (y1, x1), (y2, x2) in reversed(swap_positions):
                decrypted_array[y1, x1], decrypted_array[y2, x2] = \
                    decrypted_array[y2, x2].copy(), decrypted_array[y1, x1].copy()
            self.processed_image = Image.fromarray(decrypted_array.astype(np.uint8))
            self.display_image(self.processed_image, self.processed_canvas)
            self.status_var.set("Pixel swap decryption applied")
        except Exception as e:
            messagebox.showerror("Error", f"Pixel swap decryption failed: {str(e)}")
    
    def reset_image(self):
        """Reset processed image to original"""
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_image(self.processed_image, self.processed_canvas)
            self.status_var.set("Image reset to original")
        else:
            messagebox.showwarning("Warning", "No original image to reset to!")
    
    def save_image(self):
        """Save the processed image"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save!")
            return
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionTool(root)
    root.mainloop()