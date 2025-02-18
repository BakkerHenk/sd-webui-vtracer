import subprocess
import sys
import os

# Define a function to clone vtracer if it's not already available.
def install_vtracer():
    try:
        # Try to install vtracer using pip
        print("[vTracer] Attempting to install vtracer via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "vtracer"])
        print("[vTracer] vtracer installation successful.")
    except subprocess.CalledProcessError as e:
        print(f"[vTracer] Error installing vtracer: {e}")
        raise e

# Try importing vtracer, and if that fails, attempt to install it.
try:
    import vtracer
except ImportError:
    install_vtracer()
    try:
        import vtracer
    except ImportError as e:
        print("[vTracer] Failed to import vtracer even after cloning.")
        raise e

import gradio as gr
from PIL import Image
from modules import scripts, script_callbacks, shared
import pprint

class VTracerIntegration(scripts.Script):
    def title(self):
        return "vTracer"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, *args, **kwargs):
        # Create a collapsible panel under the "Generation" tab in txt2img.
        with gr.Accordion(open=False, label=self.title()):
            convert_checkbox = gr.Checkbox(label="Convert generated image to SVG", value=False)
            
            # Dropdown for colormode
            colormode = gr.Dropdown(
                label="Color Mode",
                choices=["color", "binary"],
                value="color"
            )

            # Dropdown for hierarchical mode
            hierarchical = gr.Dropdown(
                label="Hierarchical Mode",
                choices=["stacked", "cutout"],
                value="stacked"
            )

            # Dropdown for vectorization mode
            mode = gr.Dropdown(
                label="Mode",
                choices=["spline", "polygon", "none"],
                value="spline"
            )

            # Sliders for additional parameters
            filter_speckle = gr.Slider(minimum=0, maximum=10, step=1, label="Filter Speckle", value=4)
            color_precision = gr.Slider(minimum=1, maximum=10, step=1, label="Color Precision", value=8)
            layer_difference = gr.Slider(minimum=1, maximum=50, step=1, label="Layer Difference", value=16)
            corner_threshold = gr.Slider(minimum=1, maximum=100, step=1, label="Corner Threshold", value=60)
            length_threshold = gr.Slider(minimum=1, maximum=10, step=0.1, label="Length Threshold", value=4.0)
            max_iterations = gr.Slider(minimum=1, maximum=20, step=1, label="Max Iterations", value=10)
            splice_threshold = gr.Slider(minimum=1, maximum=100, step=1, label="Splice Threshold", value=45)
            path_precision = gr.Slider(minimum=1, maximum=10, step=1, label="Path Precision", value=8)

        # Return all components inside a list
        return [
            convert_checkbox,
            colormode,
            hierarchical,
            mode,
            filter_speckle,
            color_precision,
            layer_difference,
            corner_threshold,
            length_threshold,
            max_iterations,
            splice_threshold,
            path_precision
        ]

    def postprocess(self, p, processed, convert_checkbox, colormode, hierarchical, mode, filter_speckle, color_precision, layer_difference, corner_threshold, length_threshold, max_iterations, splice_threshold, path_precision):
        if not convert_checkbox:
            return
        
        try:
            
            # Get the first image from the processed images list
            image = processed.images[0]

            # Get the saved image path directly from the 'already_saved_as' attribute
            saved_image_path = image.already_saved_as
            print(f"[vTracer] Using saved image path: {saved_image_path}")

            # Convert the image to SVG using vtracer
            svg_path = os.path.splitext(saved_image_path)[0] + ".svg"
            print(f"[vTracer] Saving SVG to: {svg_path}")
            
            # Convert the image to SVG using vtracer
            vtracer.convert_image_to_svg_py(
                saved_image_path,
                svg_path,
                colormode=colormode,
                hierarchical=hierarchical,
                mode=mode,
                filter_speckle=filter_speckle,
                color_precision=color_precision,
                layer_difference=layer_difference,
                corner_threshold=corner_threshold,
                length_threshold=length_threshold,
                max_iterations=max_iterations,
                splice_threshold=splice_threshold,
                path_precision=path_precision
            )
            
            print(f"[vTracer] SVG file saved at: {svg_path}")
            
        except Exception as e:
            print(f"[vTracer] Error during vectorization: {e}")
