"""Graphical user interface for Py2APK"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from threading import Thread
from ..builder import APKBuilder
from ..config import find_android_sdk

class MainWindow(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.title("Py2APK Converter")
        self.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6)
        self.style.configure("TLabel", padding=6)
        
        # Create widgets
        self._create_widgets()
        
    def _create_widgets(self):
        """Initialize UI components"""
        # Project selection
        self.project_path = tk.StringVar()
        ttk.Label(self, text="Python Project:").pack(pady=5)
        ttk.Entry(self, textvariable=self.project_path, width=50).pack(pady=5)
        ttk.Button(self, text="Browse", command=self._browse_project).pack(pady=5)
        
        # Log display
        self.log_text = tk.Text(self, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Build APK", command=self._start_build).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
    def _browse_project(self):
        """Handle directory selection"""
        path = filedialog.askdirectory(title="Select Python Project")
        if path:
            self.project_path.set(path)
            
    def _log_message(self, message: str):
        """Append message to log display"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.update_idletasks()
            
    def _start_build(self):
        """Start APK build process in background thread"""
        def build_thread():
            try:
                project_path = Path(self.project_path.get())
                output_dir = Path.cwd() / "dist"
                
                builder = APKBuilder(project_path, output_dir)
                if builder.create_android_project():
                    self._log_message("Building APK...")
                    success = builder.build_apk(callback=self._log_message)
                    
                    if success:
                        messagebox.showinfo("Success", "APK built successfully!")
                    else:
                        messagebox.showerror("Error", "Build failed - check logs")
                        
            except Exception as e:
                self._log_message(f"Error: {str(e)}")
                
        Thread(target=build_thread, daemon=True).start()

def launch_gui():
    """Start the graphical interface"""
    window = MainWindow()
    window.mainloop()
