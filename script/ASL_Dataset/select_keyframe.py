import numpy as np 
from common.read_data import read_data,list_files_in_directory
import argparse
import math
from scipy.spatial.transform import Rotation as R
import json

def get_matched_pose_with_timestamp(timestamp,pose):
    matched_pose = None
    for p in pose:
        pose = np.array(p).astype(float)
        t,x,y,z,qx,qy,qz,qw = pose
        if math.fabs(t- timestamp) < 0.001:
            matched_pose = pose
            break
    return matched_pose

def check_pose_change_beyond_threshold(p,keymap_poses,change_angle,change_position):
    
    for pp in keymap_poses:
        t1,x1,y1,z1,qx1,qy1,qz1,qw1 = pp
        t2,x2,y2,z2,qx2,qy2,qz2,qw2 = p
        delta_position = np.array([x2 - x1,y2 - y1,z2 - z1])
        if np.linalg.norm(delta_position) < change_position:
            return False
        else: 
            R1 = R.from_quat(np.array([qx1,qy1,qz1,qw1])).as_matrix()
            R2 = R.from_quat(np.array([qx2,qy2,qz2,qw2])).as_matrix()
            dR = R2.T @ R1
            rotation = R.from_matrix(dR)
            angle_diff = rotation.magnitude() * 57.3
            if angle_diff < change_angle:
                return False
    return True
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='select keyframe according to pose change')
    parser.add_argument('-p','--pose', type=str, help='pose file')
    parser.add_argument('-f','--folder_image', type=str, help='image folder path')
    parser.add_argument('-a','--angle_change', type=float,default=5.0,help='angle change for keyframe select')
    parser.add_argument('-s','--position_change', type=float,default=0.25,help='position change for keyframe select')
    parser.add_argument('-o','--output_json', type=str, help='output json')

    args = parser.parse_args()
    folder = args.folder_image
    pose_file = args.pose
    change_angle = args.angle_change
    change_position = args.position_change
    output_json = args.output_json
    
    
    
    pose = read_data(pose_file,' ')
    
    image_infos = list_files_in_directory(folder)
    img_map = {}
    keymap_poses = []
    index = 0
    ss_index = 0
    all_size = len(image_infos)
    for img in image_infos:
        ss_index = ss_index + 1
        img_name = img[0]
        img_path = img[1]
        t = float(img_name.split('.')[0]) * 1e-9
        p = get_matched_pose_with_timestamp(t,pose)
        if p is None:
            None
        else:
            if len(keymap_poses) == 0 or check_pose_change_beyond_threshold(p,keymap_poses,change_angle,change_position) == True:
                keymap_poses.append(p)
                index = index + 1
                img_map[index] = {}
                img_map[index]["timestamp"] = t
                img_map[index]["image_path"] = img_path
                img_map[index]["pose"] = np.array(p).tolist() 
                print(f"keyframe size: {index}")
        print(f"process: {ss_index}/{all_size}")
    with open(output_json,'w') as json_file:
        json.dump(img_map,json_file) 