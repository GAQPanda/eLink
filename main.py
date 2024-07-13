# 导入必要模块
import serial
import os
import time
import win32ui
import dde
import threading
import serial.tools.list_ports

# 定义一些初始变量
txw = "RX"
gctxw = "RX"
ser3 = "none"
version = "Release 1.4.0"
update = "2024.07.13"
DNCGC = "0"

# 本程序遵守Apache2.0协议
# 程序中的输入错误重新输入均用while循环完成，导致程序结果臃肿。我会在空闲时优化这一项，具体方法是使用togo库来实现输入错误自动跳转回去
# 程序中有一些重复代码段。比较臃肿，未来会更改


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

# 以下线程用于Greencube Mode下与SoundModerm软件的联动控制发射
def gcsm():
    global gctxw
    global ser3
    global ser2
    global GCTXW
    global UPCGC
    while True:
        ser2read = ser2.read()
        if ser2read == b'\x08':
            gctxw = "TX"
            ser.write(bytes.fromhex(UPCGC))
            time.sleep(0.2)
            ser.write(bytes.fromhex("0000000008"))

        elif ser2read == b'\x88':
            gctxw = "RX"
            ser.write(bytes.fromhex("0000000088"))



def gcrts():
    global gctxw
    global ser3
    global ser2
    while True:
        ser2read = ser2.read()
        if ser2read == b'\x08':
            ser3.setRTS(True)
            gctxw = "TX"
        elif ser2read == b'\x88':
            ser3.setRTS(False)
            gctxw = "RX"


def gcdtr():
    global gctxw
    global ser3
    global ser2
    while True:
        ser2read = ser2.read()
        if ser2read == b'\x08':
            ser3.setDTR(True)
            gctxw = "TX"
        elif ser2read == b'\x88':
            ser3.setDTR(False)
            gctxw = "RX"



# 打印字体样例
print("TIP DEMO")
print("\033[0;32;40m[INFO]\033[0m ")
print("\033[0;33;40m[WARN]\033[0m ")
print("\033[0;31;40m[ERRO]\033[0m ")
print("\033[0;34;40m[ERRO]\033[0m Version：", version)
os.system('cls')

# 定义线程
t1 = threading.Thread(target=etx)
t2 = threading.Thread(target=gcsm)
t3 = threading.Thread(target=gcrts)
t4 = threading.Thread(target=gcdtr)
# 打印欢迎界面
print("""

       .____    .__        __    
  ____ |    |   |__| ____ |  | __
_/ __ \|    |   |  |/    \|  |/ /
\  ___/|    |___|  |   |  \    < 
 \___  >_______ \__|___|  /__|_ |
     \/        \/       \/     \/

""")
print("\033[0;32;40m[INFO]\033[0m eLink For FT-8*7(nd)")
print("\033[0;32;40m[INFO]\033[0m Made/Updated by BG5CVT ", update)
print("\033[0;32;40m[INFO]\033[0m Version :", version)
print("\033[0;33;40m[WARN]\033[0m Only for Windows OS")
print("\033[0;33;40m[WARN]\033[0m Only can control 144Mhz/430Mhz band")
print("\033[0;33;40m[WARN]\033[0m Only for FT-8*7(nd),DO NOT use for other radios!")
print("============================================")





# 询问用户输入串口信息

PORT = str(input("\033[0;32;40m[INFO]\033[0m 请输入端口号："))
RATE = int(input("\033[0;32;40m[INFO]\033[0m 请输入波特率："))

# 打开串口
ser = serial.Serial(PORT, RATE, timeout=0.5)
# 发送FT847专有的CAT开启命令
ser.write(bytes.fromhex("0000000000"))
ser.setRTS(False)
ser.setDTR(False)
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
            print("\033[0;32;40m[INFO]\033[0m [1] 开启Sat Mode(FT847 Only）")
            print("\033[0;32;40m[INFO]\033[0m [2] 关闭Sat Mode(FT847 Only）")
            print("\033[0;32;40m[INFO]\033[0m [3] 修改RX频率(FT847 Only）")
            print("\033[0;32;40m[INFO]\033[0m [4] 修改TX频率(FT847 Only）")
            print("\033[0;32;40m[INFO]\033[0m [5] 自动多普勒校正(FT847 Only）")
            print("\033[0;32;40m[INFO]\033[0m [6] Greencube模式")
            print("\033[0;32;40m[INFO]\033[0m [7] 退出")
            choice = str(input("\033[0;32;40m[INFO]\033[0m 请选择："))
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
                        os.system('cls')
                        lst = data.split()
                        tstart = False
                        if tstart is False:
                            try:
                                t1.start()
                                tstart = True
                            except RuntimeError:
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
                        DNC = str(DN[:-1] + "01")
                        UPC = str(UP[:-1] + "01")
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
                tstart = False
                # 关闭Split模式
                print("\033[0;33;40m[WARN]\033[0m com若为FT847用户，请手动关闭Split")
                time.sleep(1.5)
                os.system("cls")
                ser.write(bytes.fromhex("0000000082"))
                # 修改模式为USB
                ser.write(bytes.fromhex("0A00000007"))
                print("\033[0;33;40m[WARN]\033[0m 请在Com0Com中设置双通端口")
                gcrate = 57600
                gccom = input("\033[0;32;40m[INFO]\033[0m 请输入其中一个串口，并在SoundModern的设置里"
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
                        input("\033[0;31;40m[ERRO]\033[0m 请确保串口设置正确"
                              "短按Enter键进行重新设置")
                        continue
                print("\033[0;32;40m[INFO]\033[0m PTT激活方式：")
                print("\033[0;32;40m[INFO]\033[0m [1] CAT")
                print("\033[0;32;40m[INFO]\033[0m [2] RTS")
                print("\033[0;32;40m[INFO]\033[0m [3] DTR")
                GCTXW = input("\033[0;32;40m[INFO]\033[0m 请选择：")
                os.system("cls")
                if GCTXW == "2":
                    while True:
                        RTSser = input("\033[0;32;40m[INFO]\033[0m 请输入RTS端口：")
                        RTSrate = int(input("\033[0;32;40m[INFO]\033[0m 请输入RTS波特率："))
                        try:
                            ser3 = serial.Serial(RTSser, RTSrate, timeout=0.1)
                            ser3.setRTS(False)
                            ser3.setDTR(False)
                            break
                        except:
                            print("\033[0;31;40m[ERRO]\033[0m 串口打开失败")
                            input("\033[0;31;40m[ERRO]\033[0m 请确保RTS串口设置正确"
                                  "短按Enter键进行重新设置")
                            continue
                elif GCTXW == "3":
                    while True:
                        DTRser = input("\033[0;32;40m[INFO]\033[0m 请输入DTR端口：")
                        DTRrate = int(input("\033[0;32;40m[INFO]\033[0m 请输入DTR波特率："))
                        try:
                            ser3 = serial.Serial(DTRser, DTRrate, timeout=0.1)
                            ser3.setRTS(False)
                            ser3.setDTR(False)
                            break
                        except:
                            print("\033[0;31;40m[ERRO]\033[0m 串口打开失败")
                            input("\033[0;31;40m[ERRO]\033[0m 请确保DTR串口设置正确"
                                  "短按Enter键进行重新设置")


                # 创建一个DDE客户端 gc mode
                dde_client = dde.CreateServer()

                # 开始DDE会话 gc mode
                dde_client.Create("MyDDEClient")

                # 连接到DDE服务 gc mode
                conversation = dde.CreateConversation(dde_client)

                # 连接到特定的服务和主题 gc mode
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
                    # 请求数据 gc mode
                    data = conversation.Request("TrackingData")
                    data = data.strip() if data else data
                    if data == "" or data is None:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m 没有收到DDE数据")
                        input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron已经启动并打开DDE服务"
                              "短按Enter键进行重新连接")
                    else:
                        os.system('cls')
                        lst = data.split()
                        if GCTXW == "2":
                            if tstart is False:
                                t3.start()
                                tstart = True
                        elif GCTXW == "3":
                            if tstart is False:
                                t4.start()
                                tstart = True
                        else:
                            if tstart is False:
                                t2.start()
                                tstart = True
                        # 打印接收到的数据 gc mode
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
                        old_DN = DNCGC
                        DNCGC = str(DNGC[:-1] + "01")
                        UPCGC = str(UPGC[:-1] + "01")
                        if len(DNCGC) != 10:
                            print("\033[0;31;40m[ERRO]\033[0m 多普勒频率错误")
                            input("\033[0;31;40m[ERRO]\033[0m 请确保Orbitron中频率设置正确，短按Enter键进行重新控制")
                            continue
                        else:
                            if gctxw == "RX":
                                if old_DN != DNCGC:
                                    ser.write(bytes.fromhex(DNCGC))
                            print("\033[0;32;40m[INFO]\033[0m 正在进行多普勒校正")
                            print("\033[0;32;40m[INFO]\033[0m 目前状态：", gctxw)
                        # 等待0.5秒
                        time.sleep(0.3)
    elif choice == "3":
        print("\033[0;32;40m[INFO]\033[0m PTT激活方式：")
        print("\033[0;32;40m[INFO]\033[0m [1] CAT")
        print("\033[0;32;40m[INFO]\033[0m [2] RTS")
        print("\033[0;32;40m[INFO]\033[0m [3] DTR")
        CTTXW = input("\033[0;32;40m[INFO]\033[0m 请选择：")
        # 发射控制子菜单
        Tx = 0
        os.system('cls')
        if CTTXW == "2":
            while True:
                RTSser = input("\033[0;32;40m[INFO]\033[0m 请输入RTS端口：")
                RTSrate = int(input("\033[0;32;40m[INFO]\033[0m 请输入RTS波特率："))
                try:
                    ser3 = serial.Serial(RTSser, RTSrate, timeout=0.5)
                    ser3.setRTS(False)
                    ser3.setDTR(False)
                    break
                except:
                    print("\033[0;31;40m[ERRO]\033[0m 串口打开失败")
                    input("\033[0;31;40m[ERRO]\033[0m 请确保RTS串口设置正确"
                          "短按Enter键进行重新设置")
                    continue
        elif CTTXW == "3":
            while True:
                DTRser = input("\033[0;32;40m[INFO]\033[0m 请输入DTR端口：")
                DTRrate = int(input("\033[0;32;40m[INFO]\033[0m 请输入DTR波特率："))
                try:
                    ser3 = serial.Serial(DTRser, DTRrate, timeout=0.5)
                    ser3.setRTS(False)
                    ser3.setDTR(False)
                    break
                except:
                    print("\033[0;31;40m[ERRO]\033[0m 串口打开失败")
                    input("\033[0;31;40m[ERRO]\033[0m 请确保DTR串口设置正确"
                          "短按Enter键进行重新设置")
        else:
            print("")
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
                    if CTTXW == "1":
                        ser.write(bytes.fromhex("0000000008"))
                    elif CTTXW == "2":
                        ser3.setRTS(True)
                    else:
                        ser3.setDTR(True)


                    print("\033[0;32;40m[INFO]\033[0m 当前状态：TX")
                    Tx = 1
                else:
                    os.system('cls')
                    print("\033[0;32;40m[INFO]\033[0m 发射控制子菜单：")
                    print("\033[0;32;40m[INFO]\033[0m 短按Enter开始TX，再按一次结束TX")
                    print("\033[0;32;40m[INFO]\033[0m 输入Q退出")
                    if CTTXW == "1":
                        ser.write(bytes.fromhex("0000000088"))
                    elif CTTXW == "2":
                        ser3.setRTS(False)
                    else:
                        ser3.setDTR(True)
                    print("\033[0;32;40m[INFO]\033[0m 当前状态：RX")
                    Tx = 0
            elif key == "Q" or "q":  # 退出发射控制子菜单
                break
