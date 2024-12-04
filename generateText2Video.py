#####################################################
####                                             ####
#### Written By: SATYAKI DE                      ####
#### Written On: 25-Nov-2024                     ####
#### Modified On 02-Dec-2024                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsText2Video custom class to initiate the  ####
#### Stability AI python-sdk, which will convert ####
#### the promopt to Video.                       ####
####                                             ####
#####################################################

# We keep the setup code in a different class as shown below.
from clsConfigClient import clsConfigClient as cf
from datetime import datetime

import clsText2Video as ctv

######################################################
########       Initializing the Class         ########
######################################################
# Force CPU set to False
force_cpu = cf.conf['FORCE_CPU']
model_id_1 = str(cf.conf['STABLE_MODEL_ID_1'])
model_id_2 = str(cf.conf['STABLE_MODEL_ID_2'])
output_path = cf.conf['OUTPUT_PATH']
filename = cf.conf['FILE_NAME']
vidfilename = cf.conf['VIDEO_FILE_NAME']
fps = int(cf.conf['FPS'])

# Instantiate the classes
r1 = ctv.clsText2Video(model_id_1, model_id_2, output_path, filename, vidfilename, fps, force_cpu)

######################################################
########    End of   Initializing the Class   ########
######################################################

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

#############################################
#########         Main Section    ###########
#############################################

def main():
    try:
        var = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('Start Time: ' + str(var))
        print('*'*120)

        # Initialize pipeline
        prompt = input('Please provide the description of a scene: ')
        p = r1.getPrompt2Video(prompt)

        if p == 0:
            print('Congratulation! You have successfully converted Video from Text!')

        else:
            print('Oh No! Something wrong! But, Dont Worry! Check your log for more info!')

        var_1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('End Time: ' + str(var_1))
        print('*'*120)
                
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        var_1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('End Time: ' + str(var_1))
        print('*'*120)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        var_1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('End Time: ' + str(var_1))
        print('*'*120)
    finally:
        print("\nThank you for using the Image Generator!")
        var_1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('End Time: ' + str(var_1))
        print('*'*120)

if __name__ == "__main__":
    main()