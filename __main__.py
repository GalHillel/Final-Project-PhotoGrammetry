import cv2
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar, Label

# Define the stages of Meshroom processing
STAGES = [
    "CameraInit",
    "FeatureExtraction",
    "ImageMatching",
    "FeatureMatching",
    "StructureFromMotion",
    "PrepareDenseScene",
    "DepthMap",
    "DepthMapFilter",
    "Meshing",
    "MeshFiltering",
    "Texturing",
    "Publish"
]

def capture_frames(video_path, output_folder, interval, progress_var, stage_label):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Loop through the frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Save frames at specified intervals
        if frame_count % interval == 0:
            output_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(output_path, frame)
            # Update progress and stage label
            progress_var.set(int((frame_count / total_frames) * 100))
            stage_label.config(text=f"Capturing Frames ({frame_count}/{total_frames})")
        frame_count += 1
    cap.release()

def run_meshroom(input_folder, output_folder, progress_var, stage_label):
    meshroom_batch_executable = "/home/gal/Documents/Final Project/Meshroom/meshroom_batch"
    
    # Start Meshroom processing as a subprocess
    process = subprocess.Popen([meshroom_batch_executable, "--input", input_folder, "--output", output_folder])
    
    # Poll the status of Meshroom processing
    while True:
        # Check for the existence of files that indicate processing stages
        for stage_index, stage_name in enumerate(STAGES, start=1):
            stage_file = os.path.join(output_folder, f"{stage_name}.done")
            if os.path.exists(stage_file):
                stage_label.config(text=f"[{stage_index}/{len(STAGES)}] {stage_name}")
                progress_var.set((stage_index / len(STAGES)) * 100)
                break
        
        # Check if Meshroom processing is completed
        if process.poll() is not None:
            progress_var.set(100)
            stage_label.config(text="Processing Completed")
            break

def browse_video():
    # Open file dialog to select video file
    video_path = filedialog.askopenfilename()
    video_entry.delete(0, tk.END)
    video_entry.insert(0, video_path)

def browse_output_photos_folder():
    # Open folder dialog to select output folder for photos
    output_folder = filedialog.askdirectory()
    output_photos_entry.delete(0, tk.END)
    output_photos_entry.insert(0, output_folder)

def browse_output_meshroom_folder():
    # Open folder dialog to select output folder for Meshroom processing
    output_folder = filedialog.askdirectory()
    output_meshroom_entry.delete(0, tk.END)
    output_meshroom_entry.insert(0, output_folder)

def process_video():  # Define the process_video function here
    video_path = video_entry.get()
    output_folder_photos = output_photos_entry.get()
    interval = int(interval_entry.get())
    num_photos = int(num_photos_entry.get())

    if not os.path.exists(output_folder_photos):
        os.makedirs(output_folder_photos)

    capture_frames(video_path, output_folder_photos, interval, progress_var, capture_label)
    print(f"{num_photos} photos captured from the video.")

    output_folder_meshroom = output_meshroom_entry.get()
    if not os.path.exists(output_folder_meshroom):
        os.makedirs(output_folder_meshroom)

    run_meshroom(output_folder_photos, output_folder_meshroom, progress_var, meshroom_label)

if __name__ == "__main__":
    # Create the main GUI window
    root = tk.Tk()
    root.title("Photogrammetry Project")

    # Create and place GUI elements for video selection
    video_label = tk.Label(root, text="Video:")
    video_label.grid(row=0, column=0, padx=5, pady=5)
    video_entry = tk.Entry(root, width=50)
    video_entry.grid(row=0, column=1, padx=5, pady=5)
    video_button = tk.Button(root, text="Browse", command=browse_video)
    video_button.grid(row=0, column=2, padx=5, pady=5)

    # Create and place GUI elements for selecting output folder for photos
    output_photos_label = tk.Label(root, text="Output Folder for Photos:")
    output_photos_label.grid(row=1, column=0, padx=5, pady=5)
    output_photos_entry = tk.Entry(root, width=50)
    output_photos_entry.grid(row=1, column=1, padx=5, pady=5)
    output_photos_button = tk.Button(root, text="Browse", command=browse_output_photos_folder)
    output_photos_button.grid(row=1, column=2, padx=5, pady=5)

    # Create and place GUI elements for selecting output folder for Meshroom processing
    output_meshroom_label = tk.Label(root, text="Output Folder for Meshroom:")
    output_meshroom_label.grid(row=2, column=0, padx=5, pady=5)
    output_meshroom_entry = tk.Entry(root, width=50)
    output_meshroom_entry.grid(row=2, column=1, padx=5, pady=5)
    output_meshroom_button = tk.Button(root, text="Browse", command=browse_output_meshroom_folder)
    output_meshroom_button.grid(row=2, column=2, padx=5, pady=5)

    # Create and place GUI elements for interval and number of photos to capture
    interval_label = tk.Label(root, text="Capture Interval (in frames):")
    interval_label.grid(row=3, column=0, padx=5, pady=5)
    interval_entry = tk.Entry(root)
    interval_entry.grid(row=3, column=1, padx=5, pady=5)

    num_photos_label = tk.Label(root, text="Number of Photos to Capture:")
    num_photos_label.grid(row=4, column=0, padx=5, pady=5)
    num_photos_entry = tk.Entry(root)
    num_photos_entry.grid(row=4, column=1, padx=5, pady=5)

    # Create and place GUI elements for progress indication
    capture_label = Label(root, text="Capturing Frames: 0%")
    capture_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    meshroom_label = Label(root, text="Meshroom Processing: 0%")
    meshroom_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    progress_label = Label(root, text="Progress:")
    progress_label.grid(row=7, column=0, padx=5, pady=5)
    progress_var = tk.IntVar()
    progress_bar = Progressbar(root, length=200, mode='determinate', variable=progress_var)
    progress_bar.grid(row=7, column=1, padx=5, pady=5)

    # Create the button to trigger video processing
    process_button = tk.Button(root, text="Process Video", command=process_video)
    process_button.grid(row=8, column=1, padx=5, pady=5)

    # Start the main GUI event loop
    root.mainloop()
