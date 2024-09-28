import rospy
import numpy as np
import rosbag
from geometry_msgs.msg import TransformStamped
import argparse
from std_msgs.msg import Header
from common.read_data import read_data
def read_and_write_rosbag(topic, camera_pose, output_bag_path):
    # 初始化 ROS 节点
    rospy.init_node('rosbag_reader_writer', anonymous=True)

    # 打开输入和输出 rosbag
    with rosbag.Bag(output_bag_path, 'a') as output_bag:
        for p in camera_pose:
            # 处理 TransformStamped 消息
            pose = np.array(p).astype(float)
            t,x,y,z,qx,qy,qz,qw = pose
            print(f't = {t}')
                # 你可以在这里对 msg 进行处理
            transform_msg = TransformStamped()
                # 假设 msg 是 TransformStamped 类型
            transform_msg.header = Header()
            transform_msg.header.stamp = rospy.Time(t)
            transform_msg.header.frame_id = "/world"
            transform_msg.child_frame_id = "/cam0"
            transform_msg.transform.rotation.w = qw
            transform_msg.transform.rotation.x = qx
            transform_msg.transform.rotation.y = qy
            transform_msg.transform.rotation.z = qz
            transform_msg.transform.translation.x = x 
            transform_msg.transform.translation.y = y 
            transform_msg.transform.translation.z = z 
            output_bag.write(topic, transform_msg, transform_msg.header.stamp)
    output_bag.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='write camera pose into rosbag')
    parser.add_argument('-t','--topic_name', type=str)
    parser.add_argument('-o','--output_rosbag', type=str)
    parser.add_argument('-c','--camera_pose', type=str)
    
    args = parser.parse_args()
    
    
    topic = args.topic_name
    output_rosbag = args.output_rosbag
    camera_pose = args.camera_pose
    
    pose_data = read_data(camera_pose,' ')
    read_and_write_rosbag(topic,pose_data,output_rosbag)