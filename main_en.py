# Import necessary modules
import serial
import os
import time
import win32ui
import dde
import threading
import serial.tools.list_ports

# Define some initial variables
txw = "RX"
gctxw = "RX"
ser3 = "none"
version = "Releases 1.3.2"
update = "2024.05.19"

# This program complies with the Apache2.0 protocol
# Input errors in the program are re-entered using a while loop,
# resulting in bloated program results.
# I will optimize this item when I am free.
# The specific method is to use the togo library to automatically jump back when input errors are made.
# There are some repeated code segments in the program.
# It’s quite bloated and will be changed in the future.

# English version machine translated by translate.google.com


# Define a thread for receiving TX status
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

# The following threads are used for linkage control emission
# with SoundModerm software in Greencube Mode
def gcsm():
    global gctxw
    while True:
        ser.write(ser2.read())


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



# Print font samples
print("TIP DEMO")
print("\033[0;32;40m[INFO]\033[0m ")
print("\033[0;33;40m[WARN]\033[0m ")
print("\033[0;31;40m[ERRO]\033[0m ")
print("\033[0;34;40m[ERRO]\033[0m Version：", version)
os.system('cls')

#Define thread
t1 = threading.Thread(target=etx)
t2 = threading.Thread(target=gcsm)
t3 = threading.Thread(target=gcrts)
t4 = threading.Thread(target=gcdtr)
# Print the welcome interface
print("""

_____________________        ______     ______________ 
\_   _____|__    ___/       /  __  \   /  |  \______  |
 |    __)   |    |  ______  >      <  /   |  |_  /    /
 |     \    |    | /_____/ /   --   \/    ^   / /    / 
 \___  /    |____|         \______  /\____   | /____/  
     \/                           \/      |__|         

""")
print("\033[0;32;40m[INFO]\033[0m FT-847 Satellite CAT（Computer Aided Transceiver) Program")
print("\033[0;32;40m[INFO]\033[0m Made/Updated by BG5CVT", update)
print("\033[0;32;40m[INFO]\033[0m Version :", version)
print("\033[0;33;40m[WARN]\033[0m Only for Windows OS")
print("\033[0;33;40m[WARN]\033[0m Only can control 144Mhz/430Mhz band")
print("\033[0;33;40m[WARN]\033[0m Only for FT-847,DO NOT use for other radios!")
print(
    "\033[0;33;40m[WARN]\033[0m This program is only for personal use, and the author is not responsible for any consequences caused by "
    "the use of this program.")





# Ask the user to enter serial port information

PORT = str(input("\033[0;32;40m[INFO]\033[0m CAT Port:"))
RATE = int(input("\033[0;32;40m[INFO]\033[0m CAT Baud rate:"))

# Open serial port
ser = serial.Serial(PORT, RATE, timeout=0.5)
ser.setRTS(False)
ser.setDTR(False)
ser.write(bytes.fromhex(str("0000000000")))
print("\033[0;32;40m[INFO]\033[0m Connection successful!")
time.sleep(1)
os.system('cls')

# main menu
while True:
    os.system('cls')
    print("\033[0;32;40m[INFO]\033[0m Main Menu：")
    print("\033[0;32;40m[INFO]\033[0m [1] Frequency control")
    print("\033[0;32;40m[INFO]\033[0m [2] Satellite Mode")
    print("\033[0;32;40m[INFO]\033[0m [3] TX control")
    print("\033[0;32;40m[INFO]\033[0m [4] Exit")
    choice = str(input("\033[0;32;40m[INFO]\033[0m Please Choose:"))
    if choice == "4":
        ser.write(bytes.fromhex(str("0000000080")))
        break
    elif choice == "1":
        data = int(input("\033[0;32;40m[INFO]\033[0m New Frequency(KHz):"))
        freq = str(data * 10000 + 1)
        hex_freq = bytes.fromhex(freq)
        ser.write(hex_freq)
        print("\033[0;32;40m[INFO]\033[0m Successful!Frequency：" + str(data) + "KHz")
        time.sleep(1)
    elif choice == "2":
        while True:  # Satellite mode submenu
            os.system('cls')
            print("\033[0;32;40m[INFO]\033[0m Satellite Mode Submenu：")
            print("\033[0;32;40m[INFO]\033[0m [1] Turn on Sat Mode")
            print("\033[0;32;40m[INFO]\033[0m [2] Turn off Sat Mode")
            print("\033[0;32;40m[INFO]\033[0m [3] Modify RX frequency")
            print("\033[0;32;40m[INFO]\033[0m [4] Modify TX frequency")
            print("\033[0;32;40m[INFO]\033[0m [5] Automatic Doppler control")
            print("\033[0;32;40m[INFO]\033[0m [6] Greencube Mode")
            print("\033[0;32;40m[INFO]\033[0m [7] Exit")
            choice = str(input("\033[0;32;40m[INFO]\033[0m Please Choose:"))
            if choice == "7":
                break
            elif choice == "1":
                ser.write(bytes.fromhex("000000004E"))
                print("\033[0;32;40m[INFO]\033[0m Sat Mode is on")
                time.sleep(1)
            elif choice == "2":
                ser.write(bytes.fromhex("000000008E"))
                print("\033[0;32;40m[INFO]\033[0m Sat Mode is off")
                time.sleep(1)
            elif choice == "3":
                data = int(input("\033[0;32;40m[INFO]\033[0m Please enter RX frequency (KHz):"))
                freq = str(data * 10000 + 11)
                hex_freq = bytes.fromhex(freq)
                ser.write(hex_freq)
                print("\033[0;32;40m[INFO]\033[0m Modification successful! RX frequency is:" + str(data) + "KHz")
                time.sleep(1)
            elif choice == "4":
                data = int(input("\033[0;32;40m[INFO]\033[0m Please enter TX frequency (KHz):"))
                freq = str(data * 10000 + 21)
                hex_freq = bytes.fromhex(freq)
                ser.write(hex_freq)
                print("\033[0;32;40m[INFO]\033[0m Modification successful! TX frequency is:" + str(data) + "KHz")
                time.sleep(1)
            elif choice == "5":
                # Create a DDE client
                dde_client = dde.CreateServer()

                # Start DDE session
                dde_client.Create("MyDDEClient")

                # Connect to DDE service
                conversation = dde.CreateConversation(dde_client)

                # Connect to specific services and topics
                while True:
                    try:
                        conversation.ConnectTo("Orbitron", "Tracking")
                        break
                    except dde.error as e:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m Orbitron process not detected")
                        input("""\033[0;31;40m[ERRO]\033[0m Please make sure Orbitron is started and the DDE service is turned on.
                              Short press the Enter key to reconnect""")

                while True:
                    # Request data
                    data = conversation.Request("TrackingData")
                    data = data.strip() if data else data
                    if data == "" or data is None:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m No DDE data received")
                        input("""\033[0;31;40m[ERRO]\033[0m Please make sure Orbitron is started and the DDE service is turned on
                              Short press the Enter key to reconnect""")
                    else:
                        ser.write(bytes.fromhex("000000004E"))
                        os.system('cls')
                        lst = data.split()
                        tstart = False
                        if tstart is False:
                            try:
                                t1.start()
                                tstart = True
                            except RuntimeError:
                                pass
                        #Print the received data
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Satellite：", lst[0].lstrip("SN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Satellite：", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Satellite azimuth：", lst[1].lstrip("AZ"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Satellite azimuth：", "Unkonwn")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Satellite elevation angle：", lst[2].lstrip("EL"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Satellite elevation angle：", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Downlink Doppler frequency:", lst[3].lstrip("DN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Downlink Doppler frequency:", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Uplink Doppler frequency:", lst[4].lstrip("UP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Uplink Doppler frequency:", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Downlink demodulation mode:", lst[5].lstrip("MDN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Downlink demodulation mode:", "Unkonwn")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Uplink modulation mode:", lst[6].lstrip("MUP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Uplink modulation mode:", "Unknown")
                        DN = str(lst[3].lstrip("DN"))
                        UP = str(lst[4].lstrip("UP"))
                        DNC = str(DN[:-1] + "11")
                        UPC = str(UP[:-1] + "21")
                        if len(DNC) != 10 or len(UPC) != 10:
                            print("\033[0;31;40m[ERRO]\033[0m Doppler frequency error")
                            input("""\033[0;31;40m[ERRO]\033[0m Please make sure the frequency setting in Orbitron is correct
                                  Short press the Enter key to regain control""")
                            continue
                        else:
                            ser.write(bytes.fromhex(DNC))
                            ser.write(bytes.fromhex(UPC))
                            print("\033[0;32;40m[INFO]\033[0m Doppler correction in progress")
                            print("\033[0;32;40m[INFO]\033[0m Short press Enter to start TX, press again to end TX")
                            print('\033[0;32;40m[INFO]\033[0m Status:', txw)
                        # Wait 1 second
                        time.sleep(1)
            elif choice == "6":
                tstart = False
                input("""\033[0;33;40m[WARN]\033[0m Please make sure the FT-847 has exited satellite mode"
                      and turned on Split Mode RX-TX
                      Due to radio station restrictions, the secondary frequency needs to be adjusted manually.
                      Short press Enter key to continue""")
                os.system('cls')
                print("\033[0;33;40m[WARN]\033[0m Please set up the dual pass port pair in Com0Com")
                gcrate = 57600
                gccom = input("""\033[0;33;40m[WARN]\033[0m Please enter one of the serial ports 
                                and set another serial port in the CAT settings of SoundModern:""")
                while True:
                    try:
                        # Try to open gccom
                        ser2 = serial.Serial(gccom, gcrate, timeout=0.5)
                        print("\033[0;32;40m[INFO]\033[0m Serial port opened successfully")
                        time.sleep(1)
                        break
                    except:
                        print("\033[0;31;40m[ERRO]\033[0m Serial port opening failed")
                        input("\033[0;31;40m[ERRO]\033[0m Please make sure the serial port settings are correct"
                              "Short press Enter key to reset")
                        continue
                print("\033[0;32;40m[INFO]\033[0m PTT activation method:")
                print("\033[0;32;40m[INFO]\033[0m [1] CAT")
                print("\033[0;32;40m[INFO]\033[0m [2] RTS")
                print("\033[0;32;40m[INFO]\033[0m [3] DTR")
                GCTXW = input("\033[0;32;40m[INFO]\033[0m Please Choose：")
                os.system("cls")
                if GCTXW == "2":
                    while True:
                        RTSser = input("\033[0;32;40m[INFO]\033[0m RTS port:")
                        RTSrate = int(input("\033[0;32;40m[INFO]\033[0m RTS rate："))
                        try:
                            ser3 = serial.Serial(RTSser, RTSrate, timeout=0.1)
                            ser3.setRTS(False)
                            ser3.setDTR(False)
                            break
                        except:
                            print("\033[0;31;40m[ERRO]\033[0m Serial port opening failed")
                            input("\033[0;31;40m[ERRO]\033[0m Please make sure the RTS serial port settings are correct"
                                  "Short press Enter key to reset")
                            continue
                elif GCTXW == "3":
                    while True:
                        DTRser = input("\033[0;32;40m[INFO]\033[0m DTR Port：")
                        DTRrate = int(input("\033[0;32;40m[INFO]\033[0m DTR Rate："))
                        try:
                            ser3 = serial.Serial(DTRser, DTRrate, timeout=0.1)
                            ser3.setRTS(False)
                            ser3.setDTR(False)
                            break
                        except:
                            print("\033[0;31;40m[ERRO]\033[0m Serial port opening failed")
                            input("\033[0;31;40m[ERRO]\033[0m Please make sure the DTR serial port settings are correct"
                                  "Short press Enter key to reset")


                # Create a DDE client gc mode
                dde_client = dde.CreateServer()

                # Start a DDE session gc mode
                dde_client.Create("MyDDEClient")

                # Connect to DDE service gc mode
                conversation = dde.CreateConversation(dde_client)

                # Connect to specific services and topics gc mode
                while True:
                    try:
                        conversation.ConnectTo("Orbitron", "Tracking")
                        break
                    except dde.error as e:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m Orbitron process not detected")
                        input("""\033[0;31;40m[ERRO]\033[0m Please make sure Orbitron is started and the DDE service is turned on.
                              Short press the Enter key to reconnect""")

                while True:
                    # Request data
                    data = conversation.Request("TrackingData")
                    data = data.strip() if data else data
                    if data == "" or data is None:
                        os.system('cls')
                        print("\033[0;31;40m[ERRO]\033[0m No DDE data received")
                        input("""\033[0;31;40m[ERRO]\033[0m Please make sure Orbitron is started and the DDE service is turned on
                              Short press the Enter key to reconnect""")
                    else:
                        ser.write(bytes.fromhex("000000008E"))
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
                        #Print the received data
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Satellite：", lst[0].lstrip("SN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Satellite：", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Satellite azimuth：", lst[1].lstrip("AZ"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Satellite azimuth：", "Unkonwn")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Satellite elevation angle：", lst[2].lstrip("EL"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Satellite elevation angle：", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Downlink Doppler frequency:", lst[3].lstrip("DN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Downlink Doppler frequency:", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Uplink Doppler frequency:", lst[4].lstrip("UP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Uplink Doppler frequency:", "Unknown")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Downlink demodulation mode:", lst[5].lstrip("MDN"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Downlink demodulation mode:", "Unkonwn")
                        try:
                            print("\033[0;32;40m[INFO]\033[0m Uplink modulation mode:", lst[6].lstrip("MUP"))
                        except IndexError:
                            print("\033[0;32;40m[INFO]\033[0m Uplink modulation mode:", "Unknown")
                        DNGC = str(lst[3].lstrip("DN"))
                        UPGC = str(lst[4].lstrip("UP"))
                        DNCGC = str(DNGC[:-1] + "01")
                        if len(DNCGC) != 10:
                            print("\033[0;31;40m[ERRO]\033[0m Doppler frequency error")
                            input("""\033[0;31;40m[ERRO]\033[0m Please make sure the frequency setting in Orbitron is correct 
                            and press the Enter key to regain control.""")
                            continue
                        else:
                            ser.write(bytes.fromhex(DNCGC))
                            # Change Main Mode to USB
                            ser.write(bytes.fromhex("0100000007"))
                            print("\033[0;32;40m[INFO]\033[0m Doppler correction in progress")
                            print("\033[0;32;40m[INFO]\033[0m Status：", gctxw)
                        # Wait 0.5 seconds
                        time.sleep(0.3)
    elif choice == "3":
        print("\033[0;32;40m[INFO]\033[0m PTT activation method")
        print("\033[0;32;40m[INFO]\033[0m [1] CAT")
        print("\033[0;32;40m[INFO]\033[0m [2] RTS")
        print("\033[0;32;40m[INFO]\033[0m [3] DTR")
        CTTXW = input("\033[0;32;40m[INFO]\033[0m Please choose:")
        # 发射控制子菜单
        Tx = 0
        os.system('cls')
        if CTTXW == "2":
            while True:
                RTSser = input("\033[0;32;40m[INFO]\033[0m RTS port:")
                RTSrate = int(input("\033[0;32;40m[INFO]\033[0m RTS rate:"))
                try:
                    ser3 = serial.Serial(RTSser, RTSrate, timeout=0.5)
                    ser3.setRTS(False)
                    ser3.setDTR(False)
                    break
                except:
                    print("\033[0;31;40m[ERRO]\033[0m Serial port opening failed")
                    input("\033[0;31;40m[ERRO]\033[0m Please make sure the RTS serial port settings are correct"
                          "Short press Enter key to reset")
                    continue
        elif CTTXW == "3":
            while True:
                DTRser = input("\033[0;32;40m[INFO]\033[0m DTR port:")
                DTRrate = int(input("\033[0;32;40m[INFO]\033[0m DTR rate:："))
                try:
                    ser3 = serial.Serial(DTRser, DTRrate, timeout=0.5)
                    ser3.setRTS(False)
                    ser3.setDTR(False)
                    break
                except:
                    print("\033[0;31;40m[ERRO]\033[0m Serial port opening failed")
                    input("\033[0;31;40m[ERRO]\033[0m Please make sure the DTR serial port settings are correct"
                          "Short press Enter key to reset")
        else:
            input('\033[0;31;40m[ERRO]\033[0m ')
            break
        print("\033[0;32;40m[INFO]\033[0m TX Control submenu:")
        print("\033[0;32;40m[INFO]\033[0m Short press Enter to start TX, press again to end TX")
        print("\033[0;32;40m[INFO]\033[0m Enter Q to exit")
        while True:
            key = input()
            if key == "":
                if Tx == 0:  # Define variable TX, used to determine the current status. 0 is RX, 1 is TX
                    os.system('cls')
                    print("\033[0;32;40m[INFO]\033[0m TX Control submenu:")
                    print("\033[0;32;40m[INFO]\033[0m Short press Enter to start TX, press again to end TX")
                    print("\033[0;32;40m[INFO]\033[0m Enter Q to exit")
                    if CTTXW == "1":
                        ser.write(bytes.fromhex("0000000008"))
                    elif CTTXW == "2":
                        ser3.setRTS(True)
                    else:
                        ser3.setDTR(True)


                    print("\033[0;32;40m[INFO]\033[0m Status：TX")
                    Tx = 1
                else:
                    os.system('cls')
                    print("\033[0;32;40m[INFO]\033[0m TX Control submenu:")
                    print("\033[0;32;40m[INFO]\033[0m Short press Enter to start TX, press again to end TX")
                    print("\033[0;32;40m[INFO]\033[0m Enter Q to exit")
                    if CTTXW == "1":
                        ser.write(bytes.fromhex("0000000088"))
                    elif CTTXW == "2":
                        ser3.setRTS(False)
                    else:
                        ser3.setDTR(True)
                    print("\033[0;32;40m[INFO]\033[0m Status：RX")
                    Tx = 0
            elif key == "Q" or "q":  ##Exit the TX control submenu
                break
