import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def set_conda_env():
    conda_prefix = os.environ.get('CONDA_PREFIX', 'C:\\Users\\stephan\\anaconda3')
    os.environ['PATH'] = f"{conda_prefix}\\envs\\rvm_env\\Library\\bin;{conda_prefix}\\envs\\rvm_env\\Scripts;{conda_prefix}\\envs\\rvm_env;{os.environ['PATH']}"
    os.environ['CONDA_DEFAULT_ENV'] = 'rvm_env'
    os.environ['CONDA_PREFIX'] = f"{conda_prefix}\\envs\\rvm_env"

def run_inference():
    set_conda_env()
    input_source = input_source_var.get()
    output_folder = output_folder_var.get()
    seq_chunk = seq_chunk_var.get()
    downsample_ratio = downsample_ratio_var.get()
    video_mbps = video_mbps_var.get()

    # Extract the base name of the input file
    input_base_name = os.path.basename(input_source)
    input_name, input_ext = os.path.splitext(input_base_name)

    # Construct the output file paths
    output_composition = os.path.join(output_folder, f"output-composition-{input_name}{input_ext}")
    output_alpha = os.path.join(output_folder, f"output-alpha-{input_name}{input_ext}")

    # Build the command
    command = (
        f"python inference.py --variant mobilenetv3 "
        f"--checkpoint checkpoint/rvm_mobilenetv3.pth --device cuda "
        f"--input-source \"{input_source}\" "
        f"--output-type video "
        f"--output-composition \"{output_composition}\" "
        f"--output-alpha \"{output_alpha}\" "
        f"--output-video-mbps {video_mbps} "
        f"--seq-chunk {seq_chunk} "
        f"--downsample-ratio {downsample_ratio}"
    )

    # Debugging: Print the command to verify it
    print("Running command:", command)

    # Run the processing command
    try:
        result = subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", "Processing completed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Processing failed: {e}")

def browse_file(var):
    file_path = filedialog.askopenfilename()
    var.set(file_path)

def browse_folder(var):
    folder_path = filedialog.askdirectory()
    var.set(folder_path)

# Create the main window
root = tk.Tk()
root.title("Inference GUI")

# Define Tkinter variables
input_source_var = tk.StringVar(value="input/compressed - input.mp4")
output_folder_var = tk.StringVar(value="output")
seq_chunk_var = tk.StringVar(value="12")
downsample_ratio_var = tk.StringVar(value="0.2")
video_mbps_var = tk.StringVar(value="5")

# Create and place widgets
tk.Label(root, text="Input Source").grid(row=0, column=0, sticky=tk.W)
tk.Entry(root, textvariable=input_source_var).grid(row=0, column=1, sticky=tk.EW)
tk.Button(root, text="Browse", command=lambda: browse_file(input_source_var)).grid(row=0, column=2)

tk.Label(root, text="Output Folder").grid(row=1, column=0, sticky=tk.W)
tk.Entry(root, textvariable=output_folder_var).grid(row=1, column=1, sticky=tk.EW)
tk.Button(root, text="Browse", command=lambda: browse_folder(output_folder_var)).grid(row=1, column=2)

tk.Label(root, text="Seq Chunk").grid(row=2, column=0, sticky=tk.W)
tk.Entry(root, textvariable=seq_chunk_var).grid(row=2, column=1, sticky=tk.EW)

tk.Label(root, text="Downsample Ratio").grid(row=3, column=0, sticky=tk.W)
tk.Entry(root, textvariable=downsample_ratio_var).grid(row=3, column=1, sticky=tk.EW)

tk.Label(root, text="Video Mbps").grid(row=4, column=0, sticky=tk.W)
tk.Entry(root, textvariable=video_mbps_var).grid(row=4, column=1, sticky=tk.EW)

tk.Button(root, text="Run", command=run_inference).grid(row=5, column=0, columnspan=3, pady=10)

# Make the GUI responsive
for i in range(2):
    root.grid_columnconfigure(i, weight=1)

# Start the GUI event loop
root.mainloop()