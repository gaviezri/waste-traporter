import tkinter as tk

class ScaleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scale Garbage")
        
        self.label = tk.Label(root, text="Place an item on the scale")
        self.label.pack(pady=20)
        
        self.button_waste = tk.Button(root, text="Waste", command=self.record_waste)
        self.button_recycle = tk.Button(root, text="Recycle", command=self.record_recycle)
        
    def show_options(self, weight):
        self.label.config(text=f"Weight: {weight}g\nChoose payload type:")
        self.button_waste.pack(pady=10)
        self.button_recycle.pack(pady=10)
        
    def record_waste(self):
        self.record_payload("waste")
        
    def record_recycle(self):
        self.record_payload("recycle")
        
    def record_payload(self, payload):
        self.label.config(text="Thank you, payload recorded. You can now remove it")
        self.button_waste.pack_forget()
        self.button_recycle.pack_forget()
        
        print(f'{{"type": "{payload_type}", "weight_grams": {self.weight}}}')
        
        # Turn off the screen until the weight is zero
        self.root.update_idletasks()
        self.root.after(1000, self.wait_for_zero_weight)
        
    def wait_for_zero_weight(self):
        self.label.config(text="Place an item on the scale")
        # Simulate turning off the screen (you might need to adjust this for your actual hardware)
        self.root.update_idletasks()
        self.root.attributes("-fullscreen", False)
        
def main():
    root = tk.Tk()
    app = ScaleApp(root)
    root.attributes("-fullscreen", True)
    
    # Example weight, replace this with actual weight from the scale
    weight = 123.45
    app.show_options(weight)
    
    root.mainloop()

if __name__ == "__main__":
    main()
