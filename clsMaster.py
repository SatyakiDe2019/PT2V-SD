#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Nov-2024                     ####
#### Modified On 30-Nov-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsMaster class to initiate the             ####
#### reusable tasks in real-time.                ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf

import torch
from diffusers import StableDiffusionXLImg2ImgPipeline, StableDiffusion3Pipeline

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

######################################
### Get your global values        ####
######################################

# Set device for Apple Silicon GPU
def setup_gpu(force_cpu=False):
    if not force_cpu and torch.backends.mps.is_available() and torch.backends.mps.is_built():
        print('Running on Apple Silicon MPS GPU!')
        return torch.device("mps")
    return torch.device("cpu")

######################################
####         Global Flag      ########
######################################

class clsMaster:
    def __init__(self, force_cpu=False):
        self.device = setup_gpu(force_cpu)

    def getTorchType(self):
        try:
            # Check if MPS (Apple Silicon GPU) is available
            if not torch.backends.mps.is_available():
                torch_dtype = torch.float32
                raise RuntimeError("MPS (Metal Performance Shaders) is not available on this system.")
            else:
                torch_dtype = torch.float16
            
            return torch_dtype
        except Exception as e:
            torch_dtype = torch.float16
            print(f'Error: {str(e)}')

            return torch_dtype

    def getText2ImagePipe(self, model_id, torchType):
        try:
            device = self.device

            torch.mps.empty_cache()
            self.pipe = StableDiffusion3Pipeline.from_pretrained(model_id, torch_dtype=torchType, use_safetensors=True, variant="fp16",).to(device)

            return self.pipe
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            torch.mps.empty_cache()
            self.pipe = StableDiffusion3Pipeline.from_pretrained(model_id, torch_dtype=torchType,).to(device)

            return self.pipe
        
    def getImage2VideoPipe(self, model_id, torchType):
        try:
            device = self.device

            torch.mps.empty_cache()
            self.pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torchType, use_safetensors=True, use_fast=True).to(device)

            return self.pipeline
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            torch.mps.empty_cache()
            self.pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torchType).to(device)

            return self.pipeline


