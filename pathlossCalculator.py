"""
Sebuah program sederhana untuk kalkuator pathloss.
"""
import math as m
import datetime as dt
import sys
import os
import socket

def walfish_Ikegami(Model, Freq, Htx, Hrx, Distance, width_road, road_rad, B):
    road_deg = m.degrees(road_rad)
    Delta_Hb = Htx - Hrx
    Delta_Hm = Hrx - Htx
    Kf = 4 + ((Freq/925) - 1)

    if Model == '1':
        Lf = 32.4 + 20*m.log10(Distance) + 20*m.log10(Freq)
    elif Model == '2':
        if road_deg >= 0 and road_deg <= 35:
            L = -10 + 0.354*road_deg
        elif road_deg > 35 and road_deg <= 55:
            L = 2.5 + 0.075*(road_deg-35)
        elif road_deg > 35 and road_deg <= 55:
            L = 4 - 0.114*(road_deg - 55)
        else:
            L = 0
        return (-16.9) + 10*m.log10(width_road) + 20*m.log10(Freq) + 20*m.log10(abs(Htx - Hrx)) + L
    elif Model == '3':
        if Htx < Hrx:
            Lbsh = -18 + m.log10(1 + Delta_Hm)
            Kd = 18 - 15(Delta_Hb/Delta_Hm)
            Ka = 54 + 0.8*Htx
        else:
            Ka = 54
            Kd = 18
            Lbsh = road_deg

        return Lbsh + Ka + Kd*m.log10(Distance) + Kf*m.log10(Freq) - 9*m.log10(B)
    else:
        return "Invalid Model Ikegami!"


def COST_231(Environment, Freq, Htx, Hrx, Distance):
    Lu=0
    C1:46.3; C2: 33.9; C3:13.82; C4: 44.9; C5=6.55; 

    aHr_kecil  = (1.1*m.log10(Freq)-0.7)*Hrx - (1.56*m.log10(Freq)-0.8)
    aHr_Besar1 = 8.29*((m.log10(1.54*Hrx))**2) - 1.1
    aHr_Besar2 = 3.2*((m.log10(11.75*Hrx))**2) - 4.97

    if Freq >= 1500 and Freq <= 2000:
        if Hrx >= 1 and aHr_kecil <= 10:
            Lu = C1 + C2*m.log10(Freq) - C3*m.log10(Htx) - aHr_kecil + (C4 - C5*m.log10(Htx))*m.log10(Distance)
            if Freq <= 300:
                Lu = C1 + C2*m.log10(Freq) - C3*m.log10(Htx) - aHr_Besar1 + (C4 - C5*m.log10(Htx))*m.log10(Distance)
            else:
                Lu = C1 + C2*m.log10(Freq) - C3*m.log10(Htx) - aHr_Besar2 + (C4 - C5*m.log10(Htx))*m.log10(Distance)
    else:
        return "Invalid Frequency"
    
    if Environment == 1:
        return Lu + 0
    elif Environment == 2:
        return Lu + 3

    else:
     return "Invalid Environment"


def Okumura_Hatta(Environment, Freq, Htx, Hrx, Distance):
    Lu = 0
    C1 = 69.55; C2=26.16; C3=13.83; C4=44.9; C5=6.55;

    aHr_kecil  = (1.1*m.log10(Freq)-0.7)*Hrx - (1.56*m.log10(Freq)-0.8)
    aHr_Besar1 = 8.29*((m.log10(1.5*Hrx))**2) - 1.1
    aHr_Besar2 = 3.2*((m.log10(11.75*Hrx))**2) - 4.97
    
    if Freq >= 150 and Freq <= 1500:
        if Hrx >= 1 and aHr_kecil <= 10:
            Lu = C1 + C2*m.log10(Freq) - C3*m.log10(Htx) - aHr_kecil + ((C4 - C5*m.log10(Htx))*m.log10(Distance))
        else:
            if Freq <= 300:
                Lu = C1 + C2*m.log10(Freq) - C3*m.log10(Htx) - aHr_Besar1 + ((C4 - C5*m.log10(Htx))*m.log10(Distance))
            elif Freq > 300:
                Lu = C1 + C2*m.log10(Freq) - C3*m.log10(Htx) - aHr_Besar2 + ((C4 - C5*m.log10(Htx))*m.log10(Distance))
    else:
        return "Invalid Frequency"
    
    if Environment == '1':
        return Lu
    elif Environment == '2':
        return Lu - 2*((m.log10(Freq/28)**2) - 5.4)

    elif Environment == '3':
       return  Lu - 4.78*(m.log10(Freq))**2 + 18.33*m.log10(Freq) - 40.94
    else:
     return "Invalid Environment"

def FSL(Distance, Freq):
    return 92.45 + 20*m.log10(Freq)+20*m.log10(Distance)

def Ray2Methd(Htx, Hrx, Distance):
    return (Distance**4)/((Htx**2)*(Hrx**2))

def day():
    Day = dt.datetime.now()
    DayConv = Day.strftime("%A")

    if DayConv == "Monday":
        return "Senin"
    elif DayConv == "Tuesday":
        return("Selasa")
    elif DayConv == "Wednesday":
        return("Rabu")
    elif DayConv == "Thursday":
        return("Kamis")
    elif DayConv == "Friday":
        return("Jumat")
    elif DayConv == "Saturday":
        return("Sabtu")
    else:
        return("Minggu")

def getHostname():
    return socket.gethostname()
    
def Lanjut():
    while True:
        print("<=======================================================>")
        y_n = input("Lanjut atau Tidak [y/n]? ")
        if y_n == 'y':
            break
        elif y_n == 'n':
            print("Terima Kasih! Selamat Hari",day())
            sys.exit()
        else:
            print("Input tidak Valid!!!")


# Menu Utama Kalkulator
while True:
    os.system("cls")
    print("<============= Hello",getHostname(),"Selamat Datang ============>")
    print("<=================KALKULATOR PATHLOSS===================>")
    print("<=======================================================>")
    print("1. Free Space Loss")
    print("2. Two Ray Model")
    print("3. Okumura-Hatta")
    print("4. COST-231")
    print("5. COST 231 Walfish Ikegami")
    print("6. Keluar")
    print("<=======================================================>")
    choice = input("Masukkan Model Pathloss [1-6]: ")
    print("<=======================================================>")

    # Aksi untuk 1-5 kondisi
    if choice == '1':
        frequency = float(input("Masukkan frekuensi (GHz): "))
        Distance = float(input("Masukkan Jarak (KM)     : "))
        print("Result : ", FSL(Distance,frequency), " dB")

    elif choice == '2':
        H1 = float(input("Masukkan Tinggi Tx (m): "))
        H2 = float(input("Masukkan Tinggi Rx (m): "))
        Distance = float(input("Masukkan Jarak (m)   : "))
        result = Ray2Methd(H1, H2, Distance)
        print("Result : ", result , " dB")

    elif choice == '3':
        frequency = float(input("Masukkan frekuensi (MHz): "))
        H1 = float(input("Masukkan Tinggi Tx (m): "))
        H2 = float(input("Masukkan Tinggi Rx (m): "))
        Distance = float(input("Masukkan Jarak (m)   : "))
        print("<=======================================================>")
        print("1. Urban")
        print("2. Suburban")
        print("3. Open Area")
        print("<=======================================================>")
        Env = int(input("Masukan Lingkungan: "))
        print("<=======================================================>")
        print("Result : ", Okumura_Hatta(Env,frequency,H1,H2,Distance), " dB")

    elif choice == '4':
        frequency = float(input("Masukkan frekuensi (MHz): "))
        H1 = float(input("Masukkan Tinggi Tx (m): "))
        H2 = float(input("Masukkan Tinggi Rx (m): "))
        Distance = float(input("Masukkan Jarak (m)   : "))
        print("<=======================================================>")
        print("1. Urban")
        print("2. Suburban")
        print("<=======================================================>")
        Env =input("Masukan Lingkungan: ")
        print("<=======================================================>")

        if choice not in('1', '2'):
            print("Input tidak Valid!!!")
            continue
        else:
            print("Result : ", COST_231(Env,frequency,H1,H2,Distance), " dB")

    elif choice == '5':
        frequency = float(input("Masukkan frekuensi (MHz): "))
        H1 = float(input("Masukkan Tinggi Tx (m): "))
        H2 = float(input("Masukkan Tinggi Rx (m): "))
        Distance = float(input("Masukkan Jarak (m)   : "))
        print("<=======================================================>")
        print("1. Free Space Loss (Lf)")
        print("2. Roof to street diffraction and scatter loss (LRTS)")
        print("3. Multiscreen loss (Lms)")
        print("<=======================================================>")
        Model = input("Masukan Model: ")
        print("<=======================================================>")
        
        if Model == '1':
            print("Result : ", walfish_Ikegami(Model,frequency,H1,H2,Distance,0,0,0), " dB")
        elif Model == '2':
            road_degrees = float(input("Masukan Sudut antara Tx dan Jalan:" ))
            road_width = float(input("Masukan Lebar Jalan                :" ))
            print("Result : ", walfish_Ikegami(Model,frequency,H1,H2,Distance,road_width,road_degrees,0), " dB")
        elif Model == '3':
            road_degrees = float(input("Masukan Sudut antara Tx dan Jalan:" ))
            road_width = float(input("Masukan Lebar Jalan                :" ))
            B = float(input("Masukan jarak Antar Gedung                 :" ))
            print("Result : ", walfish_Ikegami(Model,frequency,H1,H2,Distance,road_width,road_degrees,B), " dB")
        if choice not in ('1','2','3'):
            print("Input tidak Valid!!!")
            continue

    elif choice == 6:
        print("Terima Kasih !!! Selamat hari", day())
        sys.exit(0)

    if choice not in ('1','2','3','4','5','6'):
        print("Input tidak Valid!!!")
        continue


    Lanjut()


# while True:
#     try:

# except ValueError:
#     # Handling the exception
#     print("Error: Value didnt match")
#     print("<=======================================================>")
#     y_n = input("Lanjut atau Tidak? [y/n]")
#     try:
#         Lanjut(y_n)
#     except ValueError:
#         print("Input Salah!!!")
#         break
        
        


