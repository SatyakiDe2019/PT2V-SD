################################################
####                                        ####
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 02-Dec-2024               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### personal Sarvam AI's LLM evaluation    ####
#### solution to fetch the KPIs to tune it. ####
####                                        ####
################################################

import os
import platform as pl

class clsConfigClient(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'DATA_PATH': Curr_Path + sep + 'data' + sep,
        'OUTPUT_PATH': Curr_Path + sep + 'Output' + sep,
        'TEMP_PATH': Curr_Path + sep + 'temp' + sep,
        'IMAGE_PATH': Curr_Path + sep + 'Image' + sep,
        'AUDIO_PATH': Curr_Path + sep + 'audio' + sep,
        'SESSION_PATH': Curr_Path + sep + 'my-app' + sep + 'src' + sep + 'session' + sep,
        'JSONFileNameWithPath': Curr_Path + sep + 'GUI_Config' + sep + 'CircuitConfiguration.json',
        'WORK_DIR': 'coding',
        'APP_DESC': 'Stable Defussion Demo!',
        'DEBUG_IND': 'Y',
        'INIT_PATH': Curr_Path,
        'FILE_NAME': 'lighthouse.png',
        'VIDEO_FILE_NAME': 'video.mp4',
        'FPS': 30,
        'MODEL_NAME': "gpt-3.5-turbo",
        'STABLE_MODEL_ID_1': "stabilityai/stable-diffusion-3.5-large",
        'STABLE_MODEL_ID_2': "Lykon/dreamshaper-xl-1-0",
        'API_KEY': "HHUU*4848JHZNGZtjQUxgRoDlvKi845",
        'HF_TOKENS': "hf_Hfhyyu758Kiu76FuSlzrxMUhu78",
        "FORCE_CPU": False,
        'MODEL_NAME': 'gpt-4',
        'CHANNEL_NAME': 'sd_channel',
        'STABLE_DIFFUSION_AI_KEY': "sk-Hdjideu8484hfjrfjfjZmKohpJfhuf87h",
        'ENGINE_ID': "stable-diffusion-v1-6",
        "appType":"application/json",
        "conType":"keep-alive",
        "CACHE":"no-cache",
        "MAX_RETRY": 3,
        'BASE_URL': "https://api.stability.ai",
        'TITLE': "Stable Defussion Demo!",
        'TEMP_VAL': 0.2,
        'PATH' : Curr_Path,
        'OUT_DIR': 'data',
        'OUTPUT_DIR': 'output',
        "limRec": 50,
        "DB_PATH": Curr_Path + sep + 'data' + sep
    }
