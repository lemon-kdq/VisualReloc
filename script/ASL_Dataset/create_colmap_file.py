import os
import numpy as np 
from common.read_data import read_data,list_files_in_directory
import argparse
from scipy.spatial.transform import Rotation as R
import json



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='keyframe json to colmap file.')
    parser.add_argument('-k','--keyframe_json', type=str, help='keyframe json')
    parser.add_argument('-o','--colmap_output', type=str, help='keyframe json')

    args = parser.parse_args()
    keyframes = args.keyframe_json
    output_folder = args.colmap_output
    cameras_txt = os.path.join(output_folder,"cameras.txt")
    images_txt = os.path.join(output_folder,"images.txt")
    points3D_txt = os.path.join(output_folder,"points3D.txt")   
    
    os.mkdir(output_folder)
    with open(keyframes,'r') as f:
        keyframes_data = json.load(f)
    
    c = keyframes_data["camera"]
    with open(cameras_txt,'w') as f:
        cam_info = f'1 {c["camera_model"]} {c["resolution"][0]} {c["resolution"][1]} {c["K"][0]} {c["K"][1]} {c["K"][2]} {c["K"][3]} {c["D"][0]} {c["D"][1]} {c["D"][2]} {c["D"][3]}'
        f.write(cam_info)
    with open(images_txt,'w') as f:
        for key,value in keyframes_data.items():
            if key == "camera":
                continue
            else:
                p = value["pose"]
                img_name = value["image_name"]
                image_info = f'{key} {p[7]} {p[4]} {p[5]} {p[6]} {p[1]} {p[2]} {p[3]} 1 {img_name}\n\n'
                f.write(image_info)
    with open(points3D_txt,'w') as f:
        f.write('\n')
