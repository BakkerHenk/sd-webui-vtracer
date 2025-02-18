# vTracerIntegration for Stable Diffusion WebUI

This is a Gradio extension for integrating **vTracer** with Stable Diffusion to convert generated images to vectorized SVGs using various customizable options. This extension offers flexibility to control the vectorization process with different settings to fine-tune the conversion output.

## Features

- Convert generated images to SVG using vTracer.
- **Color Mode**: Choose between color or binary vectorization.
- **Hierarchical Mode**: Select stacked or cutout vectorization.
- **Mode**: Pick between spline, polygon, or none for the vectorization type.
- **Advanced Controls**: Adjust filters, precision, and thresholds using sliders.

## Installation

To use this extension, you need to have **vTracer** installed and configured. If it is not already available, it will be installed automatically.

### Requirements

- Python 3.7+
- **Stable Diffusion** installed with Gradio and necessary dependencies.
- **vTracer** Python package (automatically installed if not available).

### Steps to Install

1. Clone the repository or download the `script.py` file.
2. Make sure you have Stable Diffusion running and working.
3. Install the necessary dependencies if not already installed:

   ```bash
   pip install gradio vtracer
