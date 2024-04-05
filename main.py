# 导入必要模块
import serial
import os
import time
import win32ui
import dde
import threading
import serial.tools.list_ports

txw = "RX"
gctxw = "RX"


# 定义一个线程，用于接收TX状态
def etx():
    global txw
    stx = 0
    while True:
        key1 = input()
        if key1 == "":
            if stx == 0:  # 定义变量TX，用于判断当前状态。0为RX，1为TX
                ser.write(bytes.fromhex("0000000008"))
                stx = 1
                txw = "TX"
            else:
                ser.write(bytes.fromhex("0000000088"))
                stx = 0
                txw = "RX"


def gcsm():
    global gctxw
    while True:
        ser.write(ser2.read())

# 打印字体样例
print("TIP DEMO")
print("\033[0;32;40m[INFO]\033[0m ")
print("\033[0;33;40m[WARN]\033[0m ")
print("\033[0;31;40m[ERRO]\033[0m ")
os.system('cls')

t1 = threading.Thread(target=etx)
t2 = threading.Thread(target=gcsm)
# 打印欢迎界面
print("\033[0;32;40m[INFO]\033[0m FT-847 Satellite CAT（Computer Aided Transceiver) Program")
print("\033[0;32;40m[INFO]\033[0m Made/Updated by BG5CVT 2024-04-05")
print("\033[0;32;40m[INFO]\033[0m Version : Releases V1.1")
print("\033[0;33;40m[WARN]\033[0m Only for Windows OS")
print("\033[0;33;40m[WARN]\033[0m Only can control 144Mhz/430Mhz band")
print("\033[0;33;40m[WARN]\033[0m Only for FT-847,DO NOT use for other radios!")
print("\033[0;33;40m[WARN]\033[0m This program is only for personal use, and the author is not responsible for any consequences caused by "
      "the use of this program.")
time.sleep(5)

# 创建虚拟串口


# 询问用户输入串口信息
os.system('cls')
PORT = str(input("\033[0;32;40m[INFO]\033[0m 请输入端口号："))
RATE = int(input("\033[0;32;40m[INFO]\033[0m 请输入波特率："))

# 打开串口
ser = serial.Serial(PORT, RATE, timeout=0.5)
ser.write(bytes.fromhex(str("0000000000")))
print("\033[0;32;40m[INFO]\033[0m 电台连接成功！")
time.sleep(1)
os.system('cls')

# 主菜单
while True:
    os.system('cls')
    print("\033[0;32;40m[INFO]\033[0m 主菜单：")
    print("\033[0;32;40m[INFO]\033[0m [1] 修改频率")
    print("\033[0;32;40m[INFO]\033[0m [2] 卫星模式")
    print("\033[0;32;40m[INFO]\033[0m [3] 发射控制")
    print("\033[0;32;40m[INFO]\033[0m [4] 退出")
    choice = str(input("\033[0;32;40m[INFO]\033[0m 请选择："))
    if choice == "4":
        ser.write(bytes.fromhex(str("0000000080")))
        break
    elif choice == "1":
        data = int(input("\033[0;32;40m[INFO]\033[0m 请输入频率(KHz):"))
        freq = str(data * 10000 + 1)
        hex_freq = bytes.fromhex(freq)
        ser.write(hex_freq)
        print("\033[0;32;40m[INFO]\033[0m 修改成功!频率为：" + str(data) + "KHz")
        time.sleep(1)
    elif choice == "2":
        while True:  # 卫星模式子菜单
            os.system('cls')
            print("\033[0;32;40m[INFO]\033[0m 卫星模式子菜单：")
            print("\033[0;32;40m[INFO]\033[0m [1] 开启Sat Mode")
            print("\033[0;32;40m[INFO]\033[0m [2] 关闭Sat Mode")
            print("\033[0;32;40m[INFO]\033[0m [3] 修改RX频率")
            print("\033[0;32;40m[INFO]\033[0m [4] 修改TX频率")
            print("\033[0;32;40m[INFO]\033[0m [5] 自动多普勒校正")
            print("\033[0;32;40m[INFO]\033[0m [6] Greencube模式")
            print("\033[0;32;40m[INFO]\033[0m [7] 退出")
            choice = str(input("请选择："))
            if choice == "7":
                break
            elif choice == "1":
                ser.write(bytes.fromhex("000000004E"))
                print("\033[0;32;40m[INFO]\033[0m Sat Mode已开启")
                time.sleep(1)
            elif choice == "2":
                ser.write(bytes.fromhex("000000008E"))
                print("\033[0;32;40m[INFO]\033[0m Sat Mode已关闭")
                time.sleep(1)
            elif choice == "3":
                data = int(input("\033[0;32;40m[INFO]\033[0m 请输入RX频率(KHz):"))
                freq = str(data * 10000 + 11)
                hex_freq = bytes.fromhex(freq)
                ser.write(hex_freq)
                print("\033[0;32;40m[INFO]\033[0m 修改成功!RX频率为：" + str(data) + "KHz")
                time.sleep(1)
            elif choice == "4":
                data = int(input("\033[0;32;40m[INFO]\033[0m 请输入TX频率(KHz):"))
                freq = str(data * 10000 + 21)
                hex_freq = bytes.fromhex(freq)
                ser.write(hex_freq)
                print("\033[0;32;40m[INFO]\033[0m 修改成功!TX频率为：" + str(data) + "KHz")
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
                        print("\033[0;31;40m[ERRO]\033[0m 未检测到Orbitron进程")
                        input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron已经启动并打开DDE服务"
                              "短按Enter键进行重新连接")

                while True:
                    # 请求数据
                    data = conversation.Request("TrackingData")
                    data = data.strip() if data else data
                    if data == "" or data is None:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m 没有收到DDE数据")
                        input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron已经启动并打开DDE服务"
                              "短按Enter键进行重新连接")
                    else:
                        ser.write(bytes.fromhex("000000004E"))
                        os.system('cls')
                        lst = data.split()
                        try:
                            t1.start()
                        except IndexError:
                            pass
                        # 打印接收到的数据
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 卫星名称：", lst[0].lstrip("SN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 卫星名称：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 卫星方位角：", lst[1].lstrip("AZ"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 卫星方位角：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 卫星仰角：", lst[2].lstrip("EL"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 卫星仰角：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 下行多普勒频率：", lst[3].lstrip("DN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 下行多普勒频率：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 上行多普勒频率：", lst[4].lstrip("UP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 上行多普勒频率：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 下行解调模式：", lst[5].lstrip("MDN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 下行解调模式：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 上行调制模式：", lst[6].lstrip("MUP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 上行调制模式：", "未知")
                        DN = str(lst[3].lstrip("DN"))
                        UP = str(lst[4].lstrip("UP"))
                        DNC = str(DN[:-1] + "11")
                        UPC = str(UP[:-1] + "21")
                        if len(DNC) != 10 or len(UPC) != 10:
                            print("\033[0;31;40m[ERRO]\033[0m 多普勒频率错误")
                            input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron中频率设置正确"
                                  "短按Enter键进行重新控制")
                            continue
                        else:
                            ser.write(bytes.fromhex(DNC))
                            ser.write(bytes.fromhex(UPC))
                            print("\033[0;32;40m[INFO]\033[0m 正在进行多普勒校正")
                            print("\033[0;32;40m[INFO]\033[0m 短按Enter开始TX，再按一次结束TX")
                            print('\033[0;32;40m[INFO]\033[0m 当前状态：', txw)
                        # 等待1秒
                        time.sleep(1)
            elif choice == "6":
                input("\033[0;33;40m[WARN]\033[0m 请确保FT-847已经退出打开Split Mode RX-TX"
                      "由于电台限制，副频率需手动调整"
                      "短按Enter键以继续")
                os.system('cls')
                print("\033[0;33;40m[WARN]\033[0m 请在Com0Com中设置双通端口对")
                gcrate = 57600
                gccom = input("\033[0;33;40m[WARN]\033[0m 请输入其中一个串口，并在SoundModern的CAT设置里"
                              "设置另一个串口:")
                while True:
                    try:
                        # 尝试打开 gccom
                        ser2 = serial.Serial(gccom, gcrate, timeout=0.5)
                        print("\033[0;32;40m[INFO]\033[0m 串口打开成功")
                        time.sleep(1)
                        break
                    except:
                        print("\033[0;31;40m[ERRO]\033[0m 串口打开失败")
                        input("\033[0;31;40m[ERRO]\033[0m 请确保FT-847侧串口设置正确"
                              "短按Enter键进行重新设置")
                        continue
                # 创建一个DDE客户端 gc
                dde_client = dde.CreateServer()

                # 开始DDE会话 gc
                dde_client.Create("MyDDEClient")

                # 连接到DDE服务 gc
                conversation = dde.CreateConversation(dde_client)

                # 连接到特定的服务和主题 gc
                while True:
                    try:
                        conversation.ConnectTo("Orbitron", "Tracking")
                        break
                    except dde.error as e:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m 未检测到Orbitron进程")
                        input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron已经启动并打开DDE服务"
                              "短按Enter键进行重新连接")

                while True:
                    # 请求数据 gc
                    data = conversation.Request("TrackingData")
                    data = data.strip() if data else data
                    if data == "" or data is None:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m 没有收到DDE数据")
                        input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron已经启动并打开DDE服务"
                              "短按Enter键进行重新连接")
                    else:
                        ser.write(bytes.fromhex("000000008E"))
                        os.system('cls')
                        lst = data.split()
                        try:
                            t2.start()
                        except:
                            pass
                        # 打印接收到的数据 gc
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 卫星名称：", lst[0].lstrip("SN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 卫星名称：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 卫星方位角：", lst[1].lstrip("AZ"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 卫星方位角：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 卫星仰角：", lst[2].lstrip("EL"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 卫星仰角：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 下行多普勒频率：", lst[3].lstrip("DN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 下行多普勒频率：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 上行多普勒频率：", lst[4].lstrip("UP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 上行多普勒频率：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 下行解调模式：", lst[5].lstrip("MDN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 下行解调模式：", "未知")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m 上行调制模式：", lst[6].lstrip("MUP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m 上行调制模式：", "未知")
                        DNGC = str(lst[3].lstrip("DN"))
                        UPGC = str(lst[4].lstrip("UP"))
                        DNCGC = str(DNGC[:-1] + "01")
                        if len(DNCGC) != 10:
                            print("\033[0;31;40m[ERRO]\033[0m 多普勒频率错误")
                            input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron中频率设置正确，短按Enter键进行重新控制")
                            continue
                        else:
                            ser.write(bytes.fromhex(DNCGC))
                            # 将Main Mode改为USB
                            ser.write(bytes.fromhex("0100000007"))
                            print("\033[0;32;40m[INFO]\033[0m 正在进行多普勒校正")
                            print("\033[0;32;40m[INFO]\033[0m 目前状态：", gctxw)
                        # 等待1秒 gc
                        time.sleep(1)
    elif choice == "3":
        # 发射控制子菜单
        Tx = 0
        os.system('cls')
        print("\033[0;32;40m[INFO]\033[0m 发射控制子菜单：")
        print("\033[0;32;40m[INFO]\033[0m 短按Enter开始TX，再按一次结束TX")
        print("\033[0;32;40m[INFO]\033[0m 输入Q退出")
        while True:
            key = input()
            if key == "":
                if Tx == 0:  # 定义变量TX，用于判断当前状态。0为RX，1为TX
                    os.system('cls')
                    print("\033[0;32;40m[INFO]\033[0m 发射控制子菜单：")
                    print("\033[0;32;40m[INFO]\033[0m 短按Enter开始TX，再按一次结束TX")
                    print("\033[0;32;40m[INFO]\033[0m 输入Q退出")
                    ser.write(bytes.fromhex("0000000008"))
                    print("\033[0;32;40m[INFO]\033[0m 当前状态：TX")
                    Tx = 1
                else:
                    os.system('cls')
                    print("\033[0;32;40m[INFO]\033[0m 发射控制子菜单：")
                    print("\033[0;32;40m[INFO]\033[0m 短按Enter开始TX，再按一次结束TX")
                    print("\033[0;32;40m[INFO]\033[0m 输入Q退出")
                    ser.write(bytes.fromhex("0000000088"))
                    print("\033[0;32;40m[INFO]\033[0m 当前状态：RX")
                    Tx = 0
            elif key == "Q" or "q":  # 退出发射控制子菜单
                break
