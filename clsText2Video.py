#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 25-Nov-2024                     ####
#### Modified On 01-Dec-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsText2Video class to initiate the         ####
#### main class that invokes two individual sdk  ####
#### in real-time.                               ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf
from datetime import datetime

import clsMaster as cm
import clsText2Image as cti
import clsImage2Video as civ

import os
import torch

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

#############################################
#########         Main Section    ###########
#############################################
class clsText2Video:
    def __init__(self, model_id_1, model_id_2, output_path, filename, vidfilename, fps, force_cpu=False):
        self.model_id_1 = model_id_1
        self.model_id_2 = model_id_2
        self.output_path = output_path
        self.filename = filename
        self.vidfilename = vidfilename
        self.force_cpu = force_cpu
        self.fps = fps

        # Initialize in main process
        os.environ["TOKENIZERS_PARALLELISM"] = "true"
        self.r1 = cm.clsMaster(force_cpu)
        self.torch_type = self.r1.getTorchType()
        
        torch.mps.empty_cache()
        self.pipe = self.r1.getText2ImagePipe(self.model_id_1, self.torch_type)
        self.pipeline = self.r1.getImage2VideoPipe(self.model_id_2, self.torch_type)

        self.text2img = cti.clsText2Image(self.pipe, self.output_path, self.filename)
        self.img2vid = civ.clsImage2Video(self.pipeline)

    def getPrompt2Video(self, prompt):
        try:
            input_image = self.output_path + self.filename
            target_video = self.output_path + self.vidfilename

            if self.text2img.genImage(prompt) == 0:
                print('Pass 1: Text to intermediate images generated!')
                
                if self.img2vid.genVideo(prompt, input_image, target_video, self.fps) == 0:
                    print('Pass 2: Successfully generated!')
                    return 0
            return 1
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")
            return 1


