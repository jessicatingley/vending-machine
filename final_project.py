import csv
import os.path
import pandas as pd
import customtkinter
import serial
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_default_color_theme("green")
ser = serial.Serial('/dev/cu.usbmodem111401', 38400, timeout=.1)  # Adjust com port as necessary


class App(customtkinter.CTk):
    PRODUCT_TRACKING_PATH = "./product.csv"

    def __init__(self):
        super().__init__()

        self.title("Final Project")
        self.geometry("800x1600")
        self.grid_columnconfigure((0, 3), weight=1)

        # Initialize all buttons and labels
        self.label = customtkinter.CTkLabel(self, text="How many products would you like?")
        self.label.grid(row=0, column=0, padx=20, pady=20, columnspan=5)
        self.button1 = customtkinter.CTkButton(self, text="1", command=self.button1_callback)
        self.button1.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=1)
        self.button2 = customtkinter.CTkButton(self, text="2", command=self.button2_callback)
        self.button2.grid(row=1, column=1, padx=20, pady=20, sticky="ew", columnspan=1)
        self.button3 = customtkinter.CTkButton(self, text="3", command=self.button3_callback)
        self.button3.grid(row=1, column=2, padx=20, pady=20, sticky="ew", columnspan=1)
        self.button4 = customtkinter.CTkButton(self, text="4", command=self.button4_callback)
        self.button4.grid(row=1, column=3, padx=20, pady=20, sticky="ew", columnspan=1)
        self.button5 = customtkinter.CTkButton(self, text="5", command=self.button5_callback)
        self.button5.grid(row=1, column=4, padx=20, pady=20, sticky="ew", columnspan=1)
        self.button6 = customtkinter.CTkButton(self, text="Reload", command=self.rev_callback)
        self.button6.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=5)
        self.running_label = customtkinter.CTkLabel(self, text="Welcome!")
        self.running_label.grid(row=5, column=0, padx=20, pady=20, columnspan=5)

        # Initialize to existing number of product or default to full
        if os.path.exists(self.PRODUCT_TRACKING_PATH):
            self.num_products = pd.read_csv(self.PRODUCT_TRACKING_PATH).iloc[-1, 0]
        else:
            self.num_products = 5
            pd.DataFrame(columns=["NumProduct", "NumDispense", "Time"]).to_csv(self.PRODUCT_TRACKING_PATH, index=False)

        # Initialize product counting label
        self.product_label = customtkinter.CTkLabel(self,
                                                    text="There are " + str(self.num_products) + " products left.")
        self.product_label.grid(row=6, column=0, padx=20, pady=20, columnspan=5)

        # Initialize bar chart frame
        self.chart_frame = customtkinter.CTkFrame(self)
        self.chart_frame.grid(row=7, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")

        self.create_chart()

    def create_chart(self):
        # Read dispensed data if it exists
        if os.path.exists(self.PRODUCT_TRACKING_PATH):
            data = pd.read_csv(self.PRODUCT_TRACKING_PATH)
        else:
            data = pd.DataFrame(columns=["NumProduct", "NumDispense", "Time"])

        # Ensure the Time column is in datetime format
        if "Time" in data.columns:
            data["Time"] = pd.to_datetime(data["Time"], errors='coerce')
        else:
            data["Time"] = pd.NaT  # Mark as not a time (NaT) if format incorrect

        # Create figure for matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        fig.patch.set_facecolor("#242424")  # Figure background color
        ax.set_facecolor("#242424")

        # Plot
        ax.plot(data["Time"], data["NumDispense"], marker='o', linestyle='-', color='#55a276')

        ax.set_title("Number of Items Dispensed vs Time", color="#fcfcfc")
        ax.set_xlabel("Time", color="#ffffff")
        ax.set_ylabel("Num Items Dispensed", color="#ffffff")
        ax.tick_params(colors="#ffffff")
        plt.xticks(color="#ffffff")
        plt.yticks(color="#ffffff")
        plt.tight_layout()

        # Embed the figure in Tkinter
        for widget in self.chart_frame.winfo_children():  # winfo_children gets every child widget of window
            widget.destroy()  # Clear previous charts

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_product_label(self):
        self.product_label = customtkinter.CTkLabel(self, text="There are " + str(self.num_products) + " products left.")
        self.product_label.grid(row=6, column=0, padx=20, pady=20, columnspan=5)

    def update_running_label(self, indicator: str):
        """Updates the label indicating the state of the system by matching given indicator with desired expression."""
        match indicator:
            case "none":
                self.running_label = customtkinter.CTkLabel(self, text="        Not enough product left!        ")
            case "reverse":
                self.running_label = customtkinter.CTkLabel(self, text="              Reversing...              ")
            case "reset":
                self.running_label = customtkinter.CTkLabel(self, text="           Must reset system!            ")
            case "full":
                self.running_label = customtkinter.CTkLabel(self, text="            Dispenser full!             ")
            case _:
                self.running_label = customtkinter.CTkLabel(self, text="        Dispensing " + indicator + "...        ")
        # Display
        self.running_label.grid(row=5, column=0, padx=20, pady=20, columnspan=5)

    def button_commands(self, num_dispense: int):
        """Called by all dispensing buttons."""

        # Read reset data from serial
        data = ser.readline().strip().decode()
        print(data)

        # if system hasn't been reset, 1 is written to serial by arduino
        if "1" in data:
            self.update_running_label("reset")  # Update the label with the correct error mssg
        elif self.num_products < num_dispense:  # Num products trying to be dispensed > num products left
            self.update_running_label("none")  # Update the label with the correct error mssg
        else:
            # Otherwise, all clear to dispense
            ser.write(str(num_dispense).encode('utf-8'))  # Write num items to be dispensed to serial as utf-8 byte
            self.update_running_label(str(num_dispense))
            # Update appropriate items
            self.num_products -= num_dispense
            self.update_csv(num_dispense)
        self.update_product_label()
        time.sleep(0.5*num_dispense)  # Sleep so button cannot be spammed

    def update_csv(self, num_dispense: int):
        # Open CSV
        with open(self.PRODUCT_TRACKING_PATH, mode='a', newline="") as file:
            writer = csv.writer(file)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format date and time into string
            writer.writerow([self.num_products, num_dispense, timestamp])  # Write info into CSV
        self.create_chart()  # Update chart

    def button1_callback(self):
        self.button_commands(1)

    def button2_callback(self):
        self.button_commands(2)

    def button3_callback(self):
        self.button_commands(3)

    def button4_callback(self):
        self.button_commands(4)

    def button5_callback(self):
        self.button_commands(5)

    def rev_callback(self):
        if self.num_products >= 5:  # Ensure no more than 5 items
            self.update_running_label("full")
        else:
            ser.write(b'b')  # Write b byte to serial
            # Update appropriate items
            self.update_running_label("reverse")
            self.num_products += 1
        self.update_product_label()


app = App()
app.mainloop()
