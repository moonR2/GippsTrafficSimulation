class Platoon:
    def __init__(self):
        self.n = 0
        self.platoon = []
        self.records = {}
        self.lrecords = []
        self.ltime = []
        self.delays = []
        self.vehPass = 0

    def add_vehicle(self, car):
        self.platoon.append(car)
        self.n += 1

    def run(self, loop_num):

        # run simulation
        for i in range(loop_num):
            for idx in range(self.n):
                #print("Loop Num:", loop_num, "i: " ,i, "idx: ", idx)
                self.platoon[idx].update()

        # save all vehicle information to an object

        
        #print("idx: ", idx, self.platoon[idx].records.keys())

        lastUpdate = sorted(self.platoon[idx].records.keys())[-1] #Last simulation time 
        lastUpdate2 = sorted(self.platoon[idx].ltime)[-1]

        #print(self.platoon[idx].records.keys()) 
        #print(lastUpdate)

        for idx in range(self.n):
            #print("inside loop",self.n)
            idxLoc = self.platoon[idx].records[lastUpdate][2] #Getting the location from the dic
            indexLoc = self.platoon[idx].ltime.index(lastUpdate2)
            idxLoc2 = self.platoon[idx].lrecords[indexLoc][2]
            print("idx: ", idx, "idxLoc: ", idxLoc)
            print("idx: ", idx, "idxLoc: ", idxLoc2)
            self.records[idx] = self.platoon[idx].records
            self.lrecords.append(self.platoon[idx].lrecords) # List for test purposes 
            if  idxLoc > 0:
                # count vehicle passing
                self.vehPass += 1
        print(self.vehPass)
    
        for i in range(loop_num * 2): # *2 For Correclty simulation time 
            for idx in range(self.vehPass): # Update new vehicle information 
                self.platoon[idx].update()
                #print(self.platoon[idx].records) 
                
        for idx in range(self.vehPass):
            self.delays.append(self.platoon[idx].calc_delay())

        print(len(self.platoon[0].records))
        print(self.platoon[0].records)
        #print(loop_num)
        print("--------------------------------------------------------------------------------------------------------")
        print(self.platoon[0].lrecords[0])
        print(len(self.platoon[0].lrecords))
        print(self.platoon[0].ltime[0])
        print(len(self.platoon[0].ltime))
        print("--------------------------------------------------------------------------------------------------------")
        print(lastUpdate)
        print(lastUpdate2)
        print("--------------------------------------------------------------------------------------------------------")
        print(self.delays)
        print("--------------------------------------------------------------------------------------------------------")
        print(self.records[0])
        print("--------------------------------------------------------------------------------------------------------")
        print(self.lrecords[0])