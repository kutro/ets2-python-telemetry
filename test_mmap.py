import mmap
import struct


class TelemetryMap:
    def __init__(self):
        # --------Staring with values needed to handle the data------ #
        self.sdkActive = ("?xxx", 0, 4)                     # display if game / sdk runs
        self.paused = ("?xxx", 4, 8)                        # check if the game and the telemetry is paused
        self.time = ("q", 8, 16)                            # not the game time, only a timestamp.
        self.simulatedTime = ("q", 16, 24)                  # Used to update the values on
        self.renderTime = ("q", 24, 32)                     # the other site of the shared memory
        self.buffer = ("8c", 32, 40)                        # reserve

        # --------Contains Game independent values and plugin version------ #
        self.telemetry_plugin_revision = ("i", 40, 44)      # Telemetry Plugin Version
        self.version_major = ("i", 44, 48)                  # Game major version
        self.version_minor = ("i", 48, 52)                  # Game minor version
        self.game = ("i", 52, 56)                           # Game identifier 0 for unknown,1 for ets2 and 2 for ats
        self.telemetry_version_game_major = ("i", 56, 60)   # Game telemetry version major
        self.telemetry_version_game_minor = ("i", 60, 64)   # Game telemetry version minor

        # --------Time------ #
        self.time_abs = ("i", 64, 68)                       # In game time in minutes

        # --------Drivetrain------ #
        self.gears = ("i", 68, 72)                          # Number forward gear ratios
        self.gears_reverse = ("i", 72, 76)                  # Number of gear ratios in reverse
        self.retarderStepCount = ("i", 76, 80)              # Number of retarder steps
        self.truckWheelCount = ("i", 80, 84)                # Number of truck wheels
        self.selectorCount = ("i", 84, 88)                  # Selector count
        self.time_abs_delivery = ("i", 88, 92)              # ?
        self.maxTrailerCount = ("i", 92, 96)                # Maximum number of trailers
        self.unitCount = ("i", 96, 100)                     # ?
        self.plannedDistanceKm = ("i", 100, 104)            # ?  (planned distance km)

        # --------Trailer/truck------ #
        self.shifterSlot = ("i", 104, 108)                  # Shifter slot
        self.retarderBrake = ("i", 108, 112)                # Retarder brake
        self.lightsAuxFront = ("i", 112, 116)               # Additional headlights in front
        self.lightsAuxRoof = ("i", 116, 120)                # Additional headlights on roof
        self.truck_wheelSubstance = ("16i", 120, 184)       # ?
        self.hshifterPosition = ("32i", 184, 312)           # ?
        self.hshifterBitmask = ("32i", 312, 440)            # ?

        # --------Job------ #
        self.jobDeliveredDeliveryTime = ("i", 440, 444)     # ?
        self.jobStartingTime = ("i", 444, 448)              # ?
        self.jobFinishedTime = ("i", 448, 452)              # ?
        self.buffer_ui = ("48c", 452, 500)                  # ?


class SharedMemory(TelemetryMap):
    def __init__(self):
        super(SharedMemory, self).__init__()
        self.map_name = "Local\\SCSTelemetry"
        self.map_size = 32 * 1024
        self.mmap = None
        self.er = ''
        self.d = ''
        self.a = []

    def connect(self):
        self.mmap = mmap.mmap(0, self.map_size, self.map_name, mmap.ACCESS_READ)

    def update(self, f, start, stop):
        self.connect()

        # print(struct.unpack(f, self.mmap[start: stop]))
        self.er = (struct.unpack(f, self.mmap[start: stop]))
        # print(self.er)
        for b in self.er:
            if not isinstance(b, (float, int, str)):
                self.a = b
                print("x")
            elif isinstance(b,  (float, int, str, bytes)):
                list.append(self.a, b)
                print('z')
            else:
                self.a = "пустота"

        return self.a
        # self.er = (struct.unpack("64c", self.mmap[2492: 2556]))
        # for b in self.er:
        #     if b != b'\x00':
        #         self.a = self.a + bytes.decode(b, encoding='utf-8')
        # print(self.a)


qwe = SharedMemory()
# qwe.update(*qwe.time)
# qwe.update(*qwe.paused)
print (qwe.update(*qwe.sdkActive))
# print (qwe.update(*qwe.jobFinishedTime))
# print(int((qwe.update(*qwe.version_major)) * 100 + int(qwe.update(*qwe.version_minor))) / 100)
