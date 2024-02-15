# 导入必要模块
import serial
import os
import time

# 打印欢迎界面
print("FT-847 Satellite CAT（Computer Aided Transceiver) Program")
print("Made by BG5EBX 2024-02-15")
print("Version : Beta 1.0")
print("Notice:Only for Windows OS")
print("Notice:Only can control 144Mhz/430Mhz band")
print("Notice:Only for FT-847,DO NOT use for other radios!")
print("Notice:This program is only for personal use, and the author is not responsible for any consequences caused by "
      "the use of this program.")
time.sleep(5)

# 询问用户输入串口信息
os.system('cls')
PORT = str(input("请输入端口号："))
RATE = int(input("请输入波特率："))

# 打开串口
ser = serial.Serial(PORT, RATE, timeout=0.5)
ser.write(bytes.fromhex(str("0000000000")))
print("电台连接成功！")
time.sleep(1)
os.system('cls')

# 询问用户输入要发送的数据
while True:
    os.system('cls')
    print("主菜单：")
    print("[1] 修改频率")
    print("[2] 卫星模式")
    print("[3] 发射控制")
    print("[4] 退出")
    choice = str(input("请选择："))
    if choice == "4":
        print("感谢使用！")
        ser.write(bytes.fromhex(str("0000000080")))
        break
    elif choice == "1":
        data = int(input("请输入频率(KHz):"))
        freq = str(data*10000+1)
        hex_freq = bytes.fromhex(freq)
        ser.write(hex_freq)
        print("修改成功!频率为："+str(data)+"KHz")
        time.sleep(1)
    elif choice == "2":
        while True:
            os.system('cls')
            print("卫星模式子菜单：")
            print("[1] 开启Sat Mode")
            print("[2] 关闭Sat Mode")
            print("[3] 修改RX频率")
            print("[4] 修改TX频率")
            print("[5] 退出")
            choice = str(input("请选择："))
            if choice == "5":
                break
            elif choice == "1":
                ser.write(bytes.fromhex("000000004E"))
                print("Sat Mode已开启")
                time.sleep(1)
            elif choice == "2":
                ser.write(bytes.fromhex("000000008E"))
                print("Sat Mode已关闭")
                time.sleep(1)
            elif choice == "3":
                data = int(input("请输入RX频率(KHz):"))
                freq = str(data*10000+11)
                hex_freq = bytes.fromhex(freq)
                ser.write(hex_freq)
                print("修改成功!RX频率为："+str(data)+"KHz")
                time.sleep(1)
            elif choice == "4":
                data = int(input("请输入TX频率(KHz):"))
                freq = str(data*10000+21)
                hex_freq = bytes.fromhex(freq)
                ser.write(hex_freq)
                print("修改成功!TX频率为："+str(data)+"KHz")
                time.sleep(1)

    elif choice == "3":
        Tx = 0
        os.system('cls')
        print("发射控制子菜单：")
        print("短按Enter开始TX，再按一次结束TX")
        print("输入Q退出")
        while True:
            key = input()
            if key == "":
                if Tx == 0:
                    os.system('cls')
                    print("发射控制子菜单：")
                    print("短按Enter开始TX，再按一次结束TX")
                    print("输入Q退出")
                    ser.write(bytes.fromhex("0000000008"))
                    print("当前状态：TX")
                    Tx = 1
                else:
                    os.system('cls')
                    print("发射控制子菜单：")
                    print("短按Enter开始TX，再按一次结束TX")
                    print("输入Q退出")
                    ser.write(bytes.fromhex("0000000088"))
                    print("当前状态：RX")
                    Tx = 0
            elif key == "Q" or "q":
                break




