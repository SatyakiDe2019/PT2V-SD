#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Nov-2024                     ####
#### Modified On 30-Nov-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsText2Image class to initiate the         ####
#### the first phase that converts text to image ####
#### in real-time.                               ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf

import clsMaster as cm
import torch
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

class clsText2Image:
    def __init__(self, pipe, output_path, filename):

        self.pipe = pipe
        
        # More aggressive attention slicing
        self.pipe.enable_attention_slicing(slice_size=1)

        self.output_path = f"{output_path}{filename}"
        
        # Warm up the pipeline
        self._warmup()
    
    def _warmup(self):
        """Warm up the pipeline to optimize memory allocation"""
        with torch.no_grad():
            _ = self.pipe("warmup", num_inference_steps=1, height=512, width=512)
        torch.mps.empty_cache()
        gc.collect()
    
    def generate(self, prompt, num_inference_steps=12, guidance_scale=3.0):
        try:
            torch.mps.empty_cache()
            gc.collect()
            
            with torch.autocast(device_type="mps"):
                with torch.no_grad():
                    image = self.pipe(
                        prompt,
                        num_inference_steps=num_inference_steps,
                        guidance_scale=guidance_scale,
                        height=1024,
                        width=1024,
                    ).images[0]
            
            image.save(self.output_path)
            return 0
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
        finally:
            torch.mps.empty_cache()
            gc.collect()

    def genImage(self, prompt):
        try:

            # Initialize generator
            x = self.generate(prompt)

            if x == 0:
                print('Successfully processed first pass!')
            else:
                print('Failed complete first pass!')
                raise 

            return 0

        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")

            return 1


