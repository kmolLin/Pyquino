import vrep
import sys, math
# child threaded script: 
# 內建使用 port 19997 若要加入其他 port, 在  serve 端程式納入
#simExtRemoteApiStart(19999)
 
vrep.simxFinish(-1)
 
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
 
if clientID!= -1:
    print("Connected to remote server")
else:
    print('Connection not successful')
    sys.exit('Could not connect')
 
errorCode,Revolute_joint_handle=vrep.simxGetObjectHandle(clientID,'Revolute_joint',vrep.simx_opmode_oneshot_wait)
 
if errorCode == -1:
    print('Can not find left or right motor')
    sys.exit()
    
deg = math.pi/180

#errorCode=vrep.simxSetJointTargetVelocity(clientID,Revolute_joint_handle,2, vrep.simx_opmode_oneshot_wait)

def setJointPosition(incAngle, steps):
    for i  in range(steps):
        errorCode=vrep.simxSetJointPosition(clientID, Revolute_joint_handle, i*incAngle*deg, vrep.simx_opmode_oneshot_wait)
    
# 每步 10 度, 轉兩圈
setJointPosition(10, 72)
# 每步 1 度, 轉兩圈
#setJointPosition(1, 720)
# 每步 0.1  度, 轉720 步
#setJointPosition(0.1, 720)

'''
三軸同動時
simxPauseCommunication(clientID,1);
simxSetJointPosition(clientID,joint1Handle,joint1Value,simx_opmode_oneshot);
simxSetJointPosition(clientID,joint2Handle,joint2Value,simx_opmode_oneshot);
simxSetJointPosition(clientID,joint3Handle,joint3Value,simx_opmode_oneshot);
simxPauseCommunication(clientID,0);
'''

        




