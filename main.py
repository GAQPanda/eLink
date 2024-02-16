# 导入必要模块
import serial
import os
import time
import win32ui
import dde

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

# 主菜单
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
        while True:  # 卫星模式子菜单
            os.system('cls')
            print("卫星模式子菜单：")
            print("[1] 开启Sat Mode")
            print("[2] 关闭Sat Mode")
            print("[3] 修改RX频率")
            print("[4] 修改TX频率")
            print("[5] 自动多普勒校正")
            print("[6] 退出")
            choice = str(input("请选择："))
            if choice == "6":
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
            elif choice == "5":

                # 创建一个DDE客户端
                dde_client = dde.CreateServer()

                # 开始DDE会话
                dde_client.Create("MyDDEClient")

                # 连接到DDE服务
                conversation = dde.CreateConversation(dde_client)

                # 连接到特定的服务和主题
                while True:
                    try:
                        conversation.ConnectTo("Orbitron", "Tracking")
                        break
                    except dde.error as e:
                        os.system('cls')
                        print("未检测到Orbitron进程，请确保Orbitron已经启动并打开DDE服务")
                        input("请确保Orbitron已经启动并打开DDE服务，短按Enter键进行重新连接")

                while True:
                    # 请求数据
                    data = conversation.Request("TrackingData")
                    data = data.strip() if data else data
                    if data == "" or data is None:
                        os.system('cls')
                        print("没有收到DDE数据，请确保Orbitron已经启动并打开DDE服务")
                        input("请确保Orbitron已经启动并打开DDE服务，短按Enter键进行重新连接")
                    else:
                        ser.write(bytes.fromhex("000000004E"))
                        os.system('cls')
                        lst = data.split()
                        # 打印接收到的数据
                        try:
                            print("卫星名称：", lst[0].lstrip("SN"))
                        except IndexError:
                            print("卫星名称：", "未知")
                        try:
                            print("卫星方位角：", lst[1].lstrip("AZ"))
                        except IndexError:
                            print("卫星方位角：", "未知")
                        try:
                            print("卫星仰角：", lst[2].lstrip("EL"))
                        except IndexError:
                            print("卫星仰角：", "未知")
                        try:
                            print("下行多普勒频率：", lst[3].lstrip("DN"))
                        except IndexError:
                            print("下行多普勒频率：", "未知")
                        try:
                            print("上行多普勒频率：", lst[4].lstrip("UP"))
                        except IndexError:
                            print("上行多普勒频率：", "未知")
                        try:
                            print("下行解调模式：", lst[5].lstrip("MDN"))
                        except IndexError:
                            print("下行解调模式：", "未知")
                        try:
                            print("上行调制模式：", lst[6].lstrip("MUP"))
                        except IndexError:
                            print("上行调制模式：", "未知")
                        DN = str(lst[3].lstrip("DN"))
                        UP = str(lst[4].lstrip("UP"))
                        DNC = str(DN[:-1]+"11")
                        UPC = str(UP[:-1]+"21")
                        if len(DNC) != 10 or len(UPC) != 10:
                            print("多普勒频率错误")
                            input("请确保Orbitron中频率设置正确，短按Enter键进行重新控制")
                            continue
                        else:
                            ser.write(bytes.fromhex(DNC))
                            ser.write(bytes.fromhex(UPC))
                            print("正在进行多普勒校正")
                        # 等待1秒
                        time.sleep(1)

    elif choice == "3":
        # 发射控制子菜单
        Tx = 0
        os.system('cls')
        print("发射控制子菜单：")
        print("短按Enter开始TX，再按一次结束TX")
        print("输入Q退出")
        while True:
            key = input()
            if key == "":
                if Tx == 0:  # 定义变量TX，用于判断当前状态。0为RX，1为TX
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
            elif key == "Q" or "q":  # 退出发射控制子菜单
                break
