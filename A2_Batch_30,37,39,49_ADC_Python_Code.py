#Names: Atharva Suryavanshi{211030}, Atharva Maslekar{211037}, Sameer Chavan{211039}, Atharva Joshi{211049}
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import sys

class ModulationSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AM and FM Modulation Simulation")
        self.master.geometry("1200x800")
        self.master.configure(bg='#f0f0f0')
        
        # Create frames
        self.control_frame = ttk.Frame(self.master, padding="10")
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.plot_frame = ttk.Frame(self.master)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Initialize zoom states for each plot
        self.zoom_states = {
            'am_time': {'xlim': (0, 5), 'ylim': (-3, 3)},
            'am_freq': {'xlim': None, 'ylim': None},
            'fm_time': {'xlim': (0, 7), 'ylim': (-1.5, 1.5)},
            'fm_freq': {'xlim': None, 'ylim': None}
        }
        
        # Set up signal parameters
        self.setup_signal_parameters()
        
        # Create the matplotlib figure
        self.create_figure()
        
        # Create controls
        self.create_controls()
        
        # Generate initial plots
        self.update_plots()
        
    def setup_signal_parameters(self):
        # AM Parameters
        self.fs1 = 200000000  # Sampling frequency for AM (200 MHz)
        self.fm1 = 500000     # Message frequency for AM (500 kHz)
        self.fc_am = 20000000  # Carrier frequency for AM (20 MHz)
        self.Am = 1.0          # Message amplitude
        self.Ac = 1.0          # Carrier amplitude
        self.t_am = np.arange(0, 0.0001, 1/self.fs1)  # AM time array
        
        # FM Parameters
        self.fs2 = 200000000  # Sampling frequency for FM (200 MHz)
        self.fm2 = 200000     # Message frequency for FM (200 kHz)
        self.fc_fm = 20000000  # Carrier frequency for FM (20 MHz)
        self.t_fm = np.arange(0, 0.0001, 1/self.fs2)  # FM time array
        
        # AM & FM Message and Carrier
        self.m_am = self.Am * np.cos(2 * np.pi * self.fm1 * self.t_am)
        self.carrier_am = self.Ac * np.cos(2 * np.pi * self.fc_am * self.t_am)
        self.m_fm = self.Am * np.cos(2 * np.pi * self.fm2 * self.t_fm)
        self.carrier_fm = self.Ac * np.cos(2 * np.pi * self.fc_fm * self.t_fm)
        
        # Initial modulation indices
        self.am_index = 0.7
        self.fm_index = 5.0
    
    def create_figure(self):
        self.fig = Figure(figsize=(12, 8), dpi=100)
        self.fig.subplots_adjust(hspace=0.4, wspace=0.3)
        
        # Create subplots
        self.ax1 = self.fig.add_subplot(221)  # AM Time domain
        self.ax2 = self.fig.add_subplot(222)  # AM Frequency domain
        self.ax3 = self.fig.add_subplot(223)  # FM Time domain
        self.ax4 = self.fig.add_subplot(224)  # FM Frequency domain
        
        # Dictionary to map axes to their identifiers
        self.axes_map = {
            self.ax1: 'am_time',
            self.ax2: 'am_freq',
            self.ax3: 'fm_time',
            self.ax4: 'fm_freq'
        }
        
        # Embed the matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Connect the zoom event handler
        self.canvas.mpl_connect('scroll_event', self.on_scroll_zoom)
    
    def create_controls(self):
        # Style for controls
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TScale', background='#f0f0f0')
        
        # AM Modulation Index slider
        am_frame = ttk.Frame(self.control_frame)
        am_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        am_label = ttk.Label(am_frame, text="AM Modulation Index (μ):")
        am_label.pack(side=tk.LEFT, padx=5)
        
        self.am_value_label = ttk.Label(am_frame, text=f"{self.am_index:.2f}")
        self.am_value_label.pack(side=tk.RIGHT, padx=5)
        
        self.am_slider = ttk.Scale(
            am_frame, from_=0.0, to=1.5, 
            orient=tk.HORIZONTAL, length=500,
            command=self.on_am_slider_change
        )
        self.am_slider.set(self.am_index)
        self.am_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # FM Modulation Index slider
        fm_frame = ttk.Frame(self.control_frame)
        fm_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        fm_label = ttk.Label(fm_frame, text="FM Modulation Index (β):")
        fm_label.pack(side=tk.LEFT, padx=5)
        
        self.fm_value_label = ttk.Label(fm_frame, text=f"{self.fm_index:.2f}")
        self.fm_value_label.pack(side=tk.RIGHT, padx=5)
        
        self.fm_slider = ttk.Scale(
            fm_frame, from_=0.0, to=15.0, 
            orient=tk.HORIZONTAL, length=500,
            command=self.on_fm_slider_change
        )
        self.fm_slider.set(self.fm_index)
        self.fm_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Additional control buttons
        button_frame = ttk.Frame(self.control_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_sliders)
        reset_button.pack(side=tk.LEFT, padx=10)
        
        save_button = ttk.Button(button_frame, text="Save Plot", command=self.save_plot)
        save_button.pack(side=tk.LEFT, padx=10)
        
        # Add frequency control section
        freq_frame = ttk.LabelFrame(self.control_frame, text="Signal Parameters", padding=10)
        freq_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        # AM Message Frequency
        am_msg_frame = ttk.Frame(freq_frame)
        am_msg_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(am_msg_frame, text="AM Message Freq (kHz):").pack(side=tk.TOP)
        self.am_freq_var = tk.StringVar(value=str(self.fm1//1000))
        am_freq_entry = ttk.Entry(am_msg_frame, textvariable=self.am_freq_var, width=8)
        am_freq_entry.pack(side=tk.TOP, pady=5)
        
        # FM Message Frequency
        fm_msg_frame = ttk.Frame(freq_frame)
        fm_msg_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(fm_msg_frame, text="FM Message Freq (kHz):").pack(side=tk.TOP)
        self.fm_freq_var = tk.StringVar(value=str(self.fm2//1000))
        fm_freq_entry = ttk.Entry(fm_msg_frame, textvariable=self.fm_freq_var, width=8)
        fm_freq_entry.pack(side=tk.TOP, pady=5)
        
        # Carrier Frequency
        carrier_frame = ttk.Frame(freq_frame)
        carrier_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(carrier_frame, text="Carrier Freq (MHz):").pack(side=tk.TOP)
        self.carrier_freq_var = tk.StringVar(value=str(self.fc_am//1000000))
        carrier_freq_entry = ttk.Entry(carrier_frame, textvariable=self.carrier_freq_var, width=8)
        carrier_freq_entry.pack(side=tk.TOP, pady=5)
        
        # Update button
        update_button = ttk.Button(freq_frame, text="Update Parameters", command=self.update_parameters)
        update_button.pack(side=tk.LEFT, padx=20)
    
    def on_am_slider_change(self, value):
        self.am_index = float(value)
        self.am_value_label.config(text=f"{self.am_index:.2f}")
        self.update_plots()
    
    def on_fm_slider_change(self, value):
        self.fm_index = float(value)
        self.fm_value_label.config(text=f"{self.fm_index:.2f}")
        self.update_plots()
    
    def reset_sliders(self):
        self.am_index = 0.7
        self.fm_index = 5.0
        self.am_slider.set(self.am_index)
        self.fm_slider.set(self.fm_index)
        self.am_value_label.config(text=f"{self.am_index:.2f}")
        self.fm_value_label.config(text=f"{self.fm_index:.2f}")
        
        # Reset zoom states
        self.zoom_states = {
            'am_time': {'xlim': None, 'ylim': None},
            'am_freq': {'xlim': None, 'ylim': None},
            'fm_time': {'xlim': None, 'ylim': None},
            'fm_freq': {'xlim': None, 'ylim': None}
        }
        
        self.update_plots()
    
    def update_parameters(self):
        try:
            # Update frequencies from entry fields
            self.fm1 = int(self.am_freq_var.get()) * 1000  # Convert kHz to Hz
            self.fm2 = int(self.fm_freq_var.get()) * 1000  # Convert kHz to Hz
            self.fc_am = int(self.carrier_freq_var.get()) * 1000000  # Convert MHz to Hz
            self.fc_fm = self.fc_am  # Use same carrier for both
            
            # Recalculate signals
            self.m_am = self.Am * np.cos(2 * np.pi * self.fm1 * self.t_am)
            self.carrier_am = self.Ac * np.cos(2 * np.pi * self.fc_am * self.t_am)
            self.m_fm = self.Am * np.cos(2 * np.pi * self.fm2 * self.t_fm)
            self.carrier_fm = self.Ac * np.cos(2 * np.pi * self.fc_fm * self.t_fm)
            
            self.update_plots()
        except ValueError:
            # Show error message if invalid input
            tk.messagebox.showerror("Invalid Input", "Please enter valid numeric values for frequencies")
    
    def plot_fft(self, signal, fs):
        N = len(signal)
        freq = np.fft.fftfreq(N, d=1/fs)[:N//2]
        magnitude = np.abs(np.fft.fft(signal))[:N//2]
        return freq, magnitude
    
    def on_scroll_zoom(self, event):
        # Only process if we're in a subplot
        if not event.inaxes:
            return
        
        # Get the plot identifier for the current axes
        plot_id = self.axes_map.get(event.inaxes)
        if not plot_id:
            return
        
        # Get current axis limits
        x_min, x_max = event.inaxes.get_xlim()
        y_min, y_max = event.inaxes.get_ylim()
        
        # Calculate zoom factor based on scroll direction
        # Use a smaller factor for smoother zooming
        base_scale = 1.1
        if event.button == 'up':
            scale_factor = 1.0 / base_scale  # Zoom in
        else:
            scale_factor = base_scale  # Zoom out
        
        # Get the mouse position in data coordinates
        x_data = event.xdata
        y_data = event.ydata
        
        # Calculate new limits centered on mouse position
        x_range = (x_max - x_min) * scale_factor
        y_range = (y_max - y_min) * scale_factor
        
        # Calculate relative position of mouse in view (0 to 1)
        x_rel = (x_data - x_min) / (x_max - x_min)
        y_rel = (y_data - y_min) / (y_max - y_min)
        
        # Set new limits maintaining mouse position
        new_xlim = (x_data - x_range * x_rel, x_data + x_range * (1 - x_rel))
        new_ylim = (y_data - y_range * y_rel, y_data + y_range * (1 - y_rel))
        
        # Update the axis limits
        event.inaxes.set_xlim(new_xlim)
        event.inaxes.set_ylim(new_ylim)
        
        # Store the new limits in zoom_states
        self.zoom_states[plot_id]['xlim'] = new_xlim
        self.zoom_states[plot_id]['ylim'] = new_ylim
        
        # Redraw the canvas
        self.canvas.draw_idle()
    
    def update_plots(self):
        # Clear all axes
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        
        # Generate signals
        am_signal = self.Ac * (1 + self.am_index * self.m_am) * self.carrier_am
        fm_signal = self.Ac * np.cos(2 * np.pi * self.fc_fm * self.t_fm + self.fm_index * np.sin(2 * np.pi * self.fm2 * self.t_fm))
        
        # Calculate FFT
        freq_am, mag_am = self.plot_fft(am_signal, self.fs1)
        freq_fm, mag_fm = self.plot_fft(fm_signal, self.fs2)
        
        # Plot AM Time Domain
        self.ax1.plot(self.t_am*1e6, self.m_am, 'r', label='AM Message', linewidth=1.5)
        self.ax1.plot(self.t_am*1e6, am_signal, 'b', alpha=0.7, label='AM Signal', linewidth=1)
        self.ax1.set_title(f"AM Modulation (μ={self.am_index:.2f})", fontweight='bold')
        self.ax1.set_xlabel("Time (μs)")
        self.ax1.set_ylabel("Amplitude")
        if self.zoom_states['am_time']['xlim']:
            self.ax1.set_xlim(self.zoom_states['am_time']['xlim'])
            self.ax1.set_ylim(self.zoom_states['am_time']['ylim'])
        else:
            self.ax1.set_xlim(0, 5)
            self.ax1.set_ylim(-3, 3)
        self.ax1.legend(loc='upper right')
        self.ax1.grid(True, alpha=0.3)
        
        # Plot AM Frequency Domain
        self.ax2.plot(freq_am/1e6, mag_am, color='royalblue', linewidth=1.5)
        self.ax2.set_title("AM Signal Spectrum", fontweight='bold')
        self.ax2.set_xlabel('Frequency (MHz)')
        self.ax2.set_ylabel('Magnitude')
        center_freq = self.fc_am / 1e6
        if self.zoom_states['am_freq']['xlim']:
            self.ax2.set_xlim(self.zoom_states['am_freq']['xlim'])
            self.ax2.set_ylim(self.zoom_states['am_freq']['ylim'])
        else:
            self.ax2.set_xlim(center_freq - 2, center_freq + 2)
        self.ax2.grid(True, alpha=0.3)
        
        # Plot FM Time Domain
        self.ax3.plot(self.t_fm*1e6, self.m_fm, 'r', label='FM Message', linewidth=1.5)
        self.ax3.plot(self.t_fm*1e6, fm_signal, 'g', alpha=0.7, label='FM Signal', linewidth=1)
        self.ax3.set_title(f"FM Modulation (β={self.fm_index:.2f})", fontweight='bold')
        self.ax3.set_xlabel("Time (μs)")
        self.ax3.set_ylabel("Amplitude")
        if self.zoom_states['fm_time']['xlim']:
            self.ax3.set_xlim(self.zoom_states['fm_time']['xlim'])
            self.ax3.set_ylim(self.zoom_states['fm_time']['ylim'])
        else:
            self.ax3.set_xlim(0, 7)
            self.ax3.set_ylim(-1.5, 1.5)
        self.ax3.legend(loc='lower right')
        self.ax3.grid(True, alpha=0.3)
        
        # Plot FM Frequency Domain
        self.ax4.plot(freq_fm/1e6, mag_fm, color='forestgreen', linewidth=1.5)
        self.ax4.set_title("FM Signal Spectrum", fontweight='bold')
        self.ax4.set_xlabel('Frequency (MHz)')
        self.ax4.set_ylabel('Magnitude')
        if self.zoom_states['fm_freq']['xlim']:
            self.ax4.set_xlim(self.zoom_states['fm_freq']['xlim'])
            self.ax4.set_ylim(self.zoom_states['fm_freq']['ylim'])
        else:
            self.ax4.set_xlim(center_freq - 5, center_freq + 5)
        self.ax4.grid(True, alpha=0.3)
        
        # Update the canvas
        self.fig.tight_layout()
        self.canvas.draw()
    
    def save_plot(self):
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", ".png"), ("All files", ".*")],
                title="Save Plot As"
            )
            if file_path:
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                tk.messagebox.showinfo("Success", f"Plot saved to {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save plot: {str(e)}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ModulationSimulationApp(root)
    root.mainloop()