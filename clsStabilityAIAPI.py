#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Nov-2024                     ####
#### Modified On 30-Nov-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsStabilityAIAPI class to initiate the     ####
#### main API-class in real-time.                ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf

import requests
import base64
import os

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

######################################
### Get your global values        ####
######################################

engine_id = cf.conf['ENGINE_ID']
api_host = cf.conf['BASE_URL']

######################################
####         Global Flag      ########
######################################

class clsStabilityAIAPI:
    def __init__(self, STABLE_DIFF_API_KEY, OUT_DIR_PATH, FILE_NM, VID_FILE_NM):
        self.STABLE_DIFF_API_KEY = STABLE_DIFF_API_KEY
        self.OUT_DIR_PATH = OUT_DIR_PATH
        self.FILE_NM = FILE_NM
        self.VID_FILE_NM = VID_FILE_NM

    def delFile(self, fileName):
        try:
            # Deleting the intermediate image
            os.remove(fileName)

            return 0 
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1

    def generateText2Image(self, inputDescription):
        try:
            STABLE_DIFF_API_KEY = self.STABLE_DIFF_API_KEY
            fullFileName = self.OUT_DIR_PATH + self.FILE_NM
            
            if STABLE_DIFF_API_KEY is None:
                raise Exception("Missing Stability API key.")
            
            response = requests.post(f"{api_host}/v1/generation/{engine_id}/text-to-image",
                                    headers={
                                        "Content-Type": "application/json",
                                        "Accept": "application/json",
                                        "Authorization": f"Bearer {STABLE_DIFF_API_KEY}"
                                        },
                                        json={
                                            "text_prompts": [{"text": inputDescription}],
                                            "cfg_scale": 7,
                                            "height": 1024,
                                            "width": 576,
                                            "samples": 1,
                                            "steps": 30,
                                            },)
            
            if response.status_code != 200:
                raise Exception("Non-200 response: " + str(response.text))
            
            data = response.json()

            for i, image in enumerate(data["artifacts"]):
                with open(fullFileName, "wb") as f:
                    f.write(base64.b64decode(image["base64"]))      
            
            return fullFileName

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 'N/A'

    def image2VideoPassOne(self, imgNameWithPath):
        try:
            STABLE_DIFF_API_KEY = self.STABLE_DIFF_API_KEY

            response = requests.post(f"https://api.stability.ai/v2beta/image-to-video",
                                    headers={"authorization": f"Bearer {STABLE_DIFF_API_KEY}"},
                                    files={"image": open(imgNameWithPath, "rb")},
                                    data={"seed": 0,"cfg_scale": 1.8,"motion_bucket_id": 127},
                                    )
            
            print('First Pass Response:')
            print(str(response.text))
            
            genID = response.json().get('id')

            return genID 
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 'N/A'

    def image2VideoPassTwo(self, genId):
        try:
            generation_id = genId
            STABLE_DIFF_API_KEY = self.STABLE_DIFF_API_KEY
            fullVideoFileName = self.OUT_DIR_PATH + self.VID_FILE_NM

            response = requests.request("GET", f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}",
                                        headers={
                                            'accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
                                            'authorization': f"Bearer {STABLE_DIFF_API_KEY}"
                                            },) 
            
            print('Retrieve Status Code: ', str(response.status_code))
            
            if response.status_code == 202:
                print("Generation in-progress, try again in 10 seconds.")

                return 5
            elif response.status_code == 200:
                print("Generation complete!")
                with open(fullVideoFileName, 'wb') as file:
                    file.write(response.content)

                print("Successfully Retrieved the video file!")

                return 0
            else:
                raise Exception(str(response.json()))
            
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
