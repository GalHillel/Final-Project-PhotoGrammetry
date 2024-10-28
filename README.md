
# Final Project Photogrammetry

This project aims to develop a comprehensive photogrammetry processing pipeline using Python. The pipeline automates the process from video frames to high-quality point clouds and merges multiple point clouds into a final consolidated model. This `README.md` provides an overview of the project, tools, installation steps, and usage instructions.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Tools and Workflow](#tools-and-workflow)
  - [Tool 1: video2Images.py](#tool-1-video2imagespy)
  - [Tool 2: images2PointCloud.py](#tool-2-images2pointcloudpy)
  - [Tool 3: combinePointCloud.py](#tool-3-combinepointcloudpy)

---

## Project Overview

This project was developed as Final Project at Ariel University's School of Computer Science. The goal is to process videos into point clouds, merging them to create high-resolution, cohesive 3D models. The tools use open-source libraries and photogrammetry software to maximize efficiency and automate repetitive tasks.

## Features

- **Frame Extraction**: Extracts high-quality frames from video, minimizing blur and maximizing overlap.
- **Point Cloud Generation**: Converts image frames into point clouds using Meshroom.
- **Point Cloud Merging**: Merges multiple point clouds using CloudCompare’s Iterative Closest Point (ICP) algorithm.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GalHillel/Final-Project-PhotoGrammetry.git
   cd Final-Project-PhotoGrammetry
   ```
2. Install dependencies (Python 3.x and required packages):
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure that [Meshroom](https://alicevision.org/#meshroom) and [CloudCompare](https://www.cloudcompare.org/) are installed and added to your system's PATH.

## Usage

### General Workflow

1. **Extract frames**: Run `video2Images.py` to capture the best frames from video.
2. **Generate Point Clouds**: Use `images2PointCloud.py` to process frames and generate point clouds.
3. **Merge Point Clouds**: Run `combinePointCloud.py` to consolidate multiple point clouds into a single model.

---

## Tools and Workflow

### Tool 1: `video2Images.py`

**Description**: Extracts frames from video files with an emphasis on quality and overlap.

**Core Functions**:
- `calculate_sharpness`: Calculates frame clarity.
- `estimate_motion`: Measures frame-to-frame motion.
- `capture_best_frames`: Saves selected frames to a specified directory.

**Usage**:
```bash
python video2Images.py --input <path_to_video> --output <output_folder>
```

### Tool 2: `images2PointCloud.py`

**Description**: Generates point clouds from extracted images using Meshroom.

**Key Features**:
- Batch processing of images.
- Error handling and real-time Meshroom output capture.

**Usage**:
```bash
python images2PointCloud.py --input <images_folder> --output <output_folder>
```

### Tool 3: `combinePointCloud.py`

**Description**: Merges multiple point clouds using CloudCompare's CLI and saves the final result.

**Usage**:
```bash
python combinePointCloud.py --input <path_to_point_cloud1> <path_to_point_cloud2> --output <output_folder>
```

---