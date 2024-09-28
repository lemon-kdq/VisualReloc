import yaml
import numpy as np

class Camera:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)

        self.sensor_type = data['sensor_type']
        self.comment = data['comment']
        self.T_BS = np.array(data['T_BS']['data']).reshape((4, 4))
        self.rate_hz = data['rate_hz']
        self.resolution = data['resolution']
        self.camera_model = data['camera_model']
        self.intrinsics = data['intrinsics']
        self.distortion_model = data['distortion_model']
        self.distortion_coefficients = data['distortion_coefficients']
    
    def print(self):
        print(f'sensor_type: {self.sensor_type}')
        print(f'camera_mode: {self.camera_model} \n intrinsic: {self.intrinsics} \n distortion_model: {self.distortion_model} distrotion_param: {self.distortion_coefficients} \n')
        print(f'Tbc: {self.T_BS}')
    def __repr__(self):
        return f"Camera(sensor_type={self.sensor_type}, comment={self.comment}, rate_hz={self.rate_hz})"


