import time
from dynamixel_sdk import *


DEVICENAME = '/dev/ttyS4'
BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0
DXL_ID = 1

ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MINIMUM_POSITION_VALUE = 180
DXL_MAXIMUM_POSITION_VALUE = 2245
DXL_MOVING_STATUS_THRESHOLD = 10

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Success open port")
else:
    print("Failure open port")
    exit()

if portHandler.setBaudRate(BAUDRATE):
    print("Set baudrate")
else:
    print("Can not set baudrate")
    exit()

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Failure communication: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error of servo: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("Servo is running")

goal_positions = [DXL_MAXIMUM_POSITION_VALUE, DXL_MINIMUM_POSITION_VALUE]
index = 0

try:
    while index < 2:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_positions[index])
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Failure communication: {packetHandler.getTxRxResult(dxl_comm_result)}")
        elif dxl_error != 0:
            print(f"Error of servo: {packetHandler.getRxPacketError(dxl_error)}")

        while True:
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Failure communication: {packetHandler.getTxRxResult(dxl_comm_result)}")
            elif dxl_error != 0:
                print(f"Error of servo: {packetHandler.getRxPacketError(dxl_error)}")

            print(f"Current position: {dxl_present_position}")

            if abs(goal_positions[index] - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
                break

        index+=1
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupt")

packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

portHandler.closePort()
print("Closed")
