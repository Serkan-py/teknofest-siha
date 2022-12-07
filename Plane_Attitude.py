# Bu kod ardupilot un kendi sitl uygulamasini destekler, denemeler ardupilot sitl kullanilarak yapilmistir.
# Bu kodu calistirmak icin oncelikle bir baglanti olmasi gerekmektedir.
# Ardindan herhangi bir yeristastonu kullanilarak takeoff verilmesi gerekmektedir.
# Ucak havada iken bu kodu calistigimizda yazilmis gorevleri yaptirabilecegiz. Kolay gelsin.

import sys, time , math
from pymavlink import mavutil,mavwp
from pymavlink.quaternion import QuaternionBase
# Baglantiyi olustur
#master = mavutil.mavlink_connection("/dev/serial0", baud=57600)
#master = mavutil.mavlink_connection("/dev/ttyACM1", baud=115200)
master = mavutil.mavlink_connection('127.0.0.1:14560',wait_ready=True)
master.wait_heartbeat()
print('baglandi')


# Mod degisimi
mode = 'GUIDED'
master.set_mode('GUIDED')
print(mode)



def set_target_attitude(roll, pitch, yaw):

    #'roll', 'pitch', and 'yaw' degiskenleri derece cinsinden aci degerleri alir.

    
    # https://mavlink.io/en/messages/common.html#ATTITUDE_TARGET_TYPEMASK
    # 1<<6 = THROTTLE_IGNORE -> maskelemesi yapildi, mod geregi yukseklik kendini sabit tutacagi icin bu maskeleme yapildi.
    bitmask = 1<<6

    master.mav.set_attitude_target_send(
        int(1e3 * (time.time() - boot_time)), # boot dan itibaren gecen sure (ms)
        master.target_system, master.target_component,
        bitmask,
        QuaternionBase([math.radians(angle) for angle in (roll, pitch, yaw)]),
        0, 0, 0, 0 # roll rate, pitch rate, yaw rate, thrust
    )

boot_time = time.time()


# (her saniye 5 er derece artirarak hedef pitch olan 15 dereceyi tamamlar.)

print("basliyor")
yaw_angle = roll_angle = 0
for pitch_angle in range(0, 15, 5):
    set_target_attitude(roll_angle, pitch_angle, yaw_angle)
    print("pitch")
    time.sleep(1)


# (her saniye 20 ser derece artirarak hedef yaw olan 60 dereceyi tamamlar.)

time.sleep(3)
print("basliyor")
roll_angle = pitch_angle = 0
for yaw_angle in range(0, 60, 20):
    set_target_attitude(roll_angle, pitch_angle, yaw_angle)
    print("yaw")
    time.sleep(1)


# (her saniye 20 er derece artirarak hedef roll olan 40 dereceyi tamamlar.)

time.sleep(3)
print("basliyor")
yaw_angle = pitch_angle = 0
for roll_angle in range(0, 40, 20):
    set_target_attitude(roll_angle, pitch_angle, yaw_angle)
    print("roll")
    time.sleep(1)
