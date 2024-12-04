#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 20-Nov-2024                     ####
#### Modified On 30-Nov-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsStabilityAIAPI class to initiate the     ####
#### Stability AI API, which will convert        ####
#### the promopt to Video.                       ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf
import clsStabilityAIAPI as csaa

import time
import datetime

######################################
### Get your global values        ####
######################################

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

STABLE_DIFF_API_KEY = cf.conf['STABLE_DIFFUSION_AI_KEY']
OUT_DIR_PATH = cf.conf['OUTPUT_PATH']
FILE_NM = cf.conf['FILE_NAME']
VID_FILE_NM = cf.conf['VIDEO_FILE_NAME']

maxRetryNo = cf.conf['MAX_RETRY']

# Instantiate the class
r1 = csaa.clsStabilityAIAPI(STABLE_DIFF_API_KEY, OUT_DIR_PATH, FILE_NM, VID_FILE_NM)

######################################
####         Global Flag      ########
######################################

#############################################
#########         Main Section    ###########
#############################################
def main():
    try:
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*' * 120)
        print('Start Time: ' + str(var))
        print('*' * 120)

        inputDesc = str(input('Please provide the description of a scene: '))
        x = r1.generateText2Image(inputDesc)

        if x == 'N/A':
            print('Failed to generate the image!')
        else:
            print('Successfully image generated!')

            gID = r1.image2VideoPassOne(x)

            if gID == 'N/A':
                print('Failed to generate id!')
            else:
                print('Job submitted successfully!')

                print('*' * 120)
                print("Generation ID:", gID)
                print('Fetching result will take some time!')
                print('*' * 120)

                waitTime = 10
                time.sleep(waitTime)

                # Failed case retry
                retries = 1
                success = False

                try:
                    while not success:
                        try:
                            z = r1.image2VideoPassTwo(gID)
                        except Exception as e:
                            success = False

                        if z == 0:
                            success = True
                        else:
                            wait = retries * 2 * 15
                            str_R1 = "retries Fail! Waiting " + str(wait) + " seconds and retrying!"

                            print(str_R1)

                            time.sleep(wait)
                            retries += 1

                        # Checking maximum retries
                        if retries >= maxRetryNo:
                            success = True
                            raise  Exception
                except:
                    print()

        # Clean Up process
        v = r1.delFile(x)

        if v == 0:
            print('Successfully cleaned up temp file!')
        else:
            print('Some issue cleaning temp files!')

        var_1 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*' * 120)
        print('End Time: ' + str(var_1))
        print('*' * 120)

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()