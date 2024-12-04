#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Nov-2024                     ####
#### Modified On 30-Nov-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsImage2Video class to initiate the        ####
#### second pass that takes the intermediate -   ####
#### images to videos in real-time.              ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf

import torch
from PIL import Image
import numpy as np
import imageio
import gc

######################################
### Get your global values        ####
######################################

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

######################################
####         Global Flag      ########
######################################

class clsImage2Video:
    def __init__(self, pipeline):
        
        # Optimize model loading
        torch.mps.empty_cache()
        self.pipeline = pipeline

    def generate_frames(self, pipeline, init_image, prompt, duration_seconds=10):
        try:
            torch.mps.empty_cache()
            gc.collect()

            base_frames = []
            img = Image.open(init_image).convert("RGB").resize((1024, 1024))
            
            for _ in range(10):
                result = pipeline(
                    prompt=prompt,
                    image=img,
                    strength=0.45,
                    guidance_scale=7.5,
                    num_inference_steps=25
                ).images[0]

                base_frames.append(np.array(result))
                img = result
                torch.mps.empty_cache()

            frames = []
            for i in range(len(base_frames)-1):
                frame1, frame2 = base_frames[i], base_frames[i+1]
                for t in np.linspace(0, 1, int(duration_seconds*24/10)):
                    frame = (1-t)*frame1 + t*frame2
                    frames.append(frame.astype(np.uint8))
            
            return frames
        except Exception as e:
            frames = []
            print(f'Error: {str(e)}')

            return frames
        finally:
            torch.mps.empty_cache()
            gc.collect()

    # Main method
    def genVideo(self, prompt, inputImage, targetVideo, fps):
        try:
            print("Starting animation generation...")
            
            init_image_path = inputImage
            output_path = targetVideo
            fps = fps
            
            frames = self.generate_frames(
                pipeline=self.pipeline,
                init_image=init_image_path,
                prompt=prompt,
                duration_seconds=20
            )
            
            imageio.mimsave(output_path, frames, fps=30)

            print("Animation completed successfully!")

            return 0
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1


