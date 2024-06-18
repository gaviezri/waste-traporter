import tkinter as tk


class ScaleUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Waste Weighing App")
        
        # Create UI elements
        self.lbl_status = tk.Label(self.root, text="Scale off", font=("Arial", 24))
        self.lbl_status.pack(pady=50)
        
        self.btn_waste = tk.Button(self.root, text="Waste", width=10, command=lambda: self.__select_type("Waste"))
        self.btn_waste.pack(pady=10)
        
        self.btn_pmd = tk.Button(self.root, text="PMD", width=10, command=lambda: self.__select_type("PMD"))
        self.btn_pmd.pack(pady=10)
        
        self.btn_paper = tk.Button(self.root, text="Paper", width=10, command=lambda: self.__select_type("Paper"))
        self.btn_paper.pack(pady=10)
        
        # Initialize weight
        self.current_weight = 0.0
        self.last_weight = 0.0
        


    def __monitor_weight(self):
        # Simulated weight change monitoring
        while True:
            # Replace with actual weight reading mechanism
            
            new_weight = self.controller.get_current_weight()  # Assume controller method to get weight
            
            if new_weight != self.current_weight:
                self.current_weight = new_weight
                self.__display_prompt()

    def __display_prompt(self):
        # Wake up screen and display prompt
        self.root.deiconify()  # Wake up the screen
        
        # Update status label
        self.lbl_status.config(text=f"Choose waste type:")
        
        # Show buttons
        self.btn_waste.pack()
        self.btn_pmd.pack()
        self.btn_paper.pack()

        # Start a timer to go back to sleep after X seconds (e.g., 10 seconds)
        self.root.after(10000, self.__go_to_sleep)  # 10000 milliseconds = 10 seconds

    def __select_type(self, waste_type):
        # Handle waste type selection
        self.lbl_status.config(text=f"Thank you!")
        self.btn_waste.pack_forget()
        self.btn_pmd.pack_forget()
        self.btn_paper.pack_forget()
        
        # Do something with the selected waste type, e.g., inform the controller
        self.controller.process_waste_type(waste_type)

        # Go back to sleep after a brief acknowledgment
        self.root.after(5000, self.__go_to_sleep)  # 3000 milliseconds = 3 seconds

    def __go_to_sleep(self):
        # Hide UI and go to sleep mode
        self.root.withdraw()  # Hide the UI window
        self.lbl_status.config(text="Scale off")
        self.current_weight = 0.0

    def start(self):
        # Start the tkinter main loop
        Thread
        self.root.mainloop()