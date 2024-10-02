import os 
import numpy as np
import argparse
import json 
import shutil
from scipy.spatial.transform import Rotation as R

def read_3d_points(points3d_txt): 
    with open(points3d_txt, 'r') as file:
        image_data_map = {}

        # 逐两行读取
        while True:
            # 读取第一行，处理元数据
            metadata_line = file.readline().strip()
            if not metadata_line:  # 如果文件结束，退出循环
                break
            if "#" in metadata_line:
                continue
            metadata = metadata_line.split()
            POINT3D_ID = metadata[0]
            X, Y, Z, R, G, B, ERROR = map(float, metadata[1:8])
            TRACK = metadata[8:]
            IMAGE_IDS = []
            for i in range(0,len(TRACK)):
                if i % 2 == 0:
                    IMAGE_IDS.append(TRACK[i])
            # 初始化对应 IMAGE_ID 的字典结构
            image_data_map[POINT3D_ID] = {
                "points": [X, Y, Z],
                "color": [R, G, B],
                "error": ERROR,
                "images_id": IMAGE_IDS
            }
  
    return image_data_map

def read_colmap_images(images_txt,points3d,keyframe_json,output_json):

# 打开文件逐行读取
    with open(keyframe_json,'r') as f:
        keyframe = json.load(f)
        
    with open(images_txt, 'r') as file:
        image_data_map = {}

    # 逐两行读取
        while True:
            # 读取第一行，处理元数据
            metadata_line = file.readline().strip()
            if not metadata_line:  # 如果文件结束，退出循环
                break
            if "#" in metadata_line:
                continue
            metadata = metadata_line.split()
            IMAGE_ID = metadata[0]
            QW, QX, QY, QZ = map(float, metadata[1:5])
            TX, TY, TZ = map(float, metadata[5:8])
            Rcw = R.from_quat(np.array([QX,QY,QZ,QW])).as_matrix()
            tcw = np.array([TX,TY,TZ])
            Rwc = Rcw.T 
            twc = - Rwc @ tcw
            Qwc = R.from_matrix(Rwc).as_quat()
            
            CAMERA_ID = metadata[8]
            NAME = metadata[9]

            #
            if NAME != keyframe[IMAGE_ID]["image_name"]:
                print("should not be happend") 
                exit(-1)
            
            # 初始化对应 IMAGE_ID 的字典结构
            image_data_map[IMAGE_ID] = {
                "timestamp": keyframe[IMAGE_ID]["timestamp"],
                "pose": [twc[0], twc[1], twc[2], Qwc[0], Qwc[1], Qwc[2], Qwc[3]],
                "image_name": NAME,
                "image_path": keyframe[IMAGE_ID]["image_path"],
                "points": []
            }

            # 读取第二行，处理2D点数据
            points_line = file.readline().strip()
            points = points_line.split()
            point_size = 0
            for i in range(0, len(points), 3):
                X = float(points[i])
                Y = float(points[i + 1])
                POINT3D_ID = int(points[i + 2])
                if POINT3D_ID == -1:
                    None
                else:
                    POINT3D_KEY = str(POINT3D_ID) 
                    if POINT3D_KEY in points3d:
                        target_image_ids = points3d[POINT3D_KEY]["images_id"]
                        if IMAGE_ID in target_image_ids:
                            image_data_map[IMAGE_ID]["points"].append([X, Y, POINT3D_ID])
                            point_size = point_size + 1 
                        else:
                            print(f'{IMAGE_ID} not in {POINT3D_ID}')
                    else:
                        print(f'{POINT3D_ID} not in points3d')
            image_data_map[IMAGE_ID]["point_size"] = point_size 
            print(f'Insert ID: {IMAGE_ID}')
        
# 输出结果   
    with open(output_json,'w') as json_file:
        json.dump(image_data_map,json_file,indent=4,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load camera configuration from YAML file.')
    parser.add_argument('-f','--colmap_folder', type=str, help='colmap_folder')
    parser.add_argument('-k','--keyframe_json', type=str, help='cameras txt file')
    parser.add_argument('-o','--output_folder', type=str, help='output json file')

    args = parser.parse_args()
    colmap_folder = args.colmap_folder
    keyframe_json = args.keyframe_json
    
    cameras_txt = os.path.join(colmap_folder,"cameras.txt")
    images_txt = os.path.join(colmap_folder,"images.txt")
    points3d_txt = os.path.join(colmap_folder,"points3D.txt")
    

    output = args.output_folder
    if os.path.exists(output):
        shutil.rmtree(output)
    os.mkdir(output)
    output_json = os.path.join(output,"reconstruction.json")
    point3d_json = os.path.join(output,"points3dInWorld.json")
    
    points3d = read_3d_points(points3d_txt)
    with open(point3d_json,'w') as f:
        json.dump(points3d,f)
    
    
    read_colmap_images(images_txt,points3d,keyframe_json,output_json)
    
    