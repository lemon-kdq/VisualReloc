import os 
import numpy as np
import argparse
from common.camera import Camera
from common.read_data import read_data
from scipy.spatial.transform import Rotation as R

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load camera configuration from YAML file.')
    parser.add_argument('-f','--asl_folder', type=str, help='Path to the YAML configuration file')
    args = parser.parse_args()
    folder = args.asl_folder
    
    print(f"folder : {folder}")
    cam0_folder = os.path.join(folder,'cam0')
    cam0_yaml = os.path.join(cam0_folder,'sensor.yaml')
    cam0_param = Camera(cam0_yaml)
    cam0_param.print()
    Rbc0 = cam0_param.T_BS[:3,:3]
    tbc0 = cam0_param.T_BS[:3,3]
    
    body_pose_file = os.path.join(folder,'state_groundtruth_estimate0/data.csv')
    gt_pose = read_data(body_pose_file)
    output_file = os.path.join(cam0_folder,'cam0_gt_pose.csv')
    
    with open(output_file,'w') as file:
        for p in gt_pose:
            pose = np.array(p).astype(float)
            t,x,y,z,qw,qx,qy,qz = pose[:8]
            t = t * 1e-9
            Rwb = R.from_quat(np.array([qx,qy,qz,qw])).as_matrix()
            twb = np.array([x,y,z])
            Rwc0 = Rwb @ Rbc0
            twc0 = Rwb @ tbc0 + twb 
            qwc0 = R.from_matrix(Rwc0).as_quat()
            line = f'{t} {twc0[0]} {twc0[1]} {twc0[2]} {qwc0[0]} {qwc0[1]} {qwc0[2]} {qwc0[3]}\n'
            file.write(line)
    file.close()
            
