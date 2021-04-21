# Ben Levering    Student ID: 000953458

import csv


# create hashtable class
class HashTable:

    # initialize HashTable and set all buckets to empty
    def __init__(self):
        self.size = 40
        self.table = []
        for i in range(self.size):
            self.table.append([])

    # add new item into HashTable
    def add(self, item_id, item_data):
        id_hash = item_id % self.size
        item_hash = self.table[id_hash]
        item_info = [item_id, item_data]

        # if no item exists at hash add new item, else chain new item to hash
        if not item_hash:
            self.table[id_hash] = list([item_info])
        else:
            for pkg in item_hash:
                if pkg[0] == item_id:
                    pkg[1] = item_data
            item_hash.append(item_info)

    # look up package based on package id and return info
    def lookup(self, item_id):
        id_hash = item_id % self.size
        item_hash = self.table[id_hash]

        if self.table:
            for i in item_hash:
                if i[0] == item_id:
                    return i[1]
        else:
            return None


# create min heap class
class MinHeap:

    # initialize MinHeap and set to empty
    def __init__(self):
        self.heap = ([])

    # add item to heap
    def add(self, distance, i):
        data = [distance, i]
        self.heap.append(data)
        self.percolate_up(len(self.heap) - 1)

    # if heap isn't empty, return min value
    def get_min(self):
        if len(self.heap) > 0:
            return self.heap[0]
        else:
            return None

    # if heap isn't empty, pop min value
    def remove_min(self):
        if len(self.heap) > 1:
            min_value = self.heap[0]
            self.heap[0] = self.heap.pop()
            self.percolate_down(0)
            return min_value
        elif len(self.heap) == 1:
            return self.heap.pop()
        else:
            return None

    # compare index to parent value, if parent is larger, swap index and parent
    def percolate_up(self, item_index):
        parent_index = item_index // 2

        if item_index > 0 and self.heap[item_index] < self.heap[parent_index]:
            temp = self.heap[parent_index]
            self.heap[parent_index] = self.heap[item_index]
            self.heap[item_index] = temp
            self.percolate_up(parent_index)
        else:
            return

    # compare index to both children value, if either child is smaller, swap index and child
    def percolate_down(self, item_index):
        l_index = (item_index * 2) + 1
        r_index = (item_index * 2) + 2
        min_value = item_index

        if len(self.heap) > l_index and self.heap[l_index] < self.heap[min_value]:
            min_value = l_index

        if len(self.heap) > r_index and self.heap[r_index] < self.heap[min_value]:
            min_value = r_index

        if min_value != item_index:
            temp = self.heap[item_index]
            self.heap[item_index] = self.heap[min_value]
            self.heap[min_value] = temp
            self.percolate_down(min_value)


# create class for each truck route
class TruckRoute:

    # initiate starting values
    def __init__(self):
        self.packages = []
        self.distance = []
        self.time = []
        self.start_time = 0
        self.capacity = 16
        self.mph = 18
        self.mpm = (60 / self.mph)

        for i in range(self.capacity):
            self.distance.append([])
            self.time.append('')

    # add new item to truck, sort package into correct location on the trucks route and verify it meets deadline
    def add(self, i):
        self.packages.append(i)
        greedy_sort(self)
        if not time_check(self):
            return False
        else:
            return True


# find unloaded packages that have the same address of packages already loaded on a truck and load the packages
def groupSameAddress(item_list):
    for pkg in item_list[:]:
        removed = False
        package_address = package_list.lookup(pkg)[0]

        # check list of packages passed into function for all addresses that match packages loaded on truck_route1
        # add packages to truck with matching addresses
        for i in truck_route1.packages:
            if package_address == package_list.lookup(i)[0] and len(truck_route1.packages) < truck_route1.capacity:
                truck_route1.add(pkg)
                item_list.remove(pkg)
                removed = True
                break
        # check list of packages passed into function for all addresses that match packages loaded on truck_route2
        # add packages to truck with matching addresses
        for i in truck_route2.packages:
            if not removed:
                if package_address == package_list.lookup(i)[0] and len(truck_route2.packages) < truck_route2.capacity:
                    truck_route2.add(pkg)
                    item_list.remove(pkg)
                    removed = True
                    break
        # check list of packages passed into function for all addresses that match packages loaded on truck_route3
        # add packages to truck with matching addresses
        for i in truck_route3.packages:
            if not removed:
                if package_address == package_list.lookup(i)[0] and len(truck_route3.packages) < truck_route3.capacity:
                    truck_route3.add(pkg)
                    item_list.remove(pkg)
                    break


# algorithm to sort packages on truck
# place package that is closes to the hub first, then fine next closes package to current package
def greedy_sort(route):
    first_location_index = -1
    min_dist_hub = 500

    # find closes package to hub and put it as the first package on the route
    for i in range(len(route.packages)):
        distance_hub = distanceLookup(0, int(package_list.lookup(route.packages[i])[0]))
        if distance_hub < min_dist_hub:
            first_location_index = i
            min_dist_hub = distance_hub
    temp = route.packages[0]
    route.packages[0] = route.packages[first_location_index]
    route.packages[first_location_index] = temp

    # find the next closes package to current, then put that package next in route
    # since packages at same address are 0m from each other they will be placed next to each other on the route
    for i in range(len(route.packages) - 1):
        min_distance = 500
        min_location_index = -1
        for j in range(i + 1, len(route.packages)):
            location_from = int(package_list.lookup(route.packages[i])[0])
            location_to = int(package_list.lookup(route.packages[j])[0])
            distance = distanceLookup(location_from, location_to)
            if distance < min_distance:
                min_location_index = j
                min_distance = distance
        temp = route.packages[i + 1]
        route.packages[i + 1] = route.packages[min_location_index]
        route.packages[min_location_index] = temp


# receive address id for two different locations, function returns the distance found on the address_list hash
def distanceLookup(location1, location2):
    distance = address_list.lookup(location1)[location2]
    return float(distance)


# for each package loaded on a truck, calculate the distance the package is from the previous and what time the package
# will arrive to its destination
def set_dis_time(route):
    route.distance[0] = distanceLookup(0, int(package_list.lookup(route.packages[0])[0]))
    route.time[0] = route.start_time + (route.distance[0] * route.mpm)

    for i in range(1, len(route.packages)):
        location_from = int(package_list.lookup(route.packages[i - 1])[0])
        location_to = int(package_list.lookup(route.packages[i])[0])
        route.distance[i] = distanceLookup(location_from, location_to)
        route.time[i] = route.time[i - 1] + (route.distance[i] * route.mpm)


# verify that each package will arrive by the given deadline for the package
# if a package will not arrive in time, move that package and all other packages at the same address earlier in the
# route until it will arrive before the deadline
def time_check(route):
    i = 1
    looped = 0
    set_dis_time(route)

    while i < len(route.packages):
        # prevent endless loop if not all package can make deadline that are on the truck
        if looped > 20:
            return False
        else:
            # if current package will arrive before its deadline, move to next package to check
            if float(route.time[i]) <= float(package_list.lookup(route.packages[i])[5]):
                i += 1
            # if the current package will not arrive before its deadline move the package and all other packages at the
            # same address back in the route and check again
            else:
                x = i
                # check for packages before and after current package for distance == 0
                # if the distance between the packages is 0, then the packages are at the same address and need to be
                # moved back with the package that did not meet the deadline
                while float(route.distance[x]) == 0:
                    x -= 1
                temp = route.packages[x - 1]
                route.packages[x - 1] = route.packages[i]
                route.packages[i] = temp

                y = i + 1
                while float(route.distance[y]) == 0:
                    y += 1

                temp = route.packages[y - 1]
                route.packages[y - 1] = route.packages[i]
                route.packages[i] = temp
    return True


# create address table from csv distance table file
def createAddressTable():
    # open distance csv and read in distance details
    with open('distance_table.csv', 'r') as csv_file:
        address_reader = csv.reader(csv_file, delimiter=',')
        address_reader.__next__()  # skip first row of csv file

        # read csv file line by line and add each address distance to address_list hash table
        for line in address_reader:
            address_list.add(int(line[1]), (line[2:]))


# load package csv file and load package details
def loadPackageFile():
    # open packages csv and read in package details
    with open('packages.csv', 'r') as csv_file:
        package_reader = csv.reader(csv_file)

        # read csv file line by line and add each package to package_list hash table
        # then add to unloaded package list
        for line in package_reader:
            pkg_deadline = int(line[6])
            pkg_note = line[8]

            package_list.add(int(line[0]), (line[1:]))

            # if the package is waiting for an address correction, then load on truck 3
            if pkg_note == '2':
                truck_route3.add(int(line[0]))
            # if the package has an express delivery deadline and was delayed or is required to be on truck 2, then load
            # on truck 2
            elif (pkg_note == '1') or pkg_note == '4':
                truck_route2.add(int(line[0]))
            # if the package has an express delivery and was not delayed or is required to be on the same truck as other
            # packages on truck 1, then load on truck 1
            elif pkg_deadline <= 540 or pkg_note == '3':
                truck_route1.add(int(line[0]))
            elif pkg_deadline <= 630:
                express_packages.append(int(line[0]))
            # load remaining packages to unloaded_packages list
            else:
                unloaded_packages.append(int(line[0]))


# main algorithm to call functions to load all packages
def loadTrucks():
    # call function to create address table
    createAddressTable()
    # call function to create package hash
    loadPackageFile()
    # group all packages from the same address to get all of the express packages and packages with the same addresses
    # as the express packages
    groupSameAddress(unloaded_packages)
    groupSameAddress(express_packages)
    # create a min heap for the remaining express packages with the min distance from the hub
    express_heap = MinHeap()

    for i in range(len(express_packages)):
        dis_hub = distanceLookup(0, int(package_list.lookup(express_packages[i])[0]))
        pkg_id = express_packages[i]
        express_heap.add(dis_hub, pkg_id)

    # while the express min heap is not empty load the packages onto truck 1, if the package will not meet the deadline
    # move the package onto truck 2
    while express_heap.get_min() is not None:
        min_item = express_heap.remove_min()[1]
        if truck_route1.add(min_item):
            express_packages.remove(min_item)
        else:
            truck_route2.add(min_item)
            unloaded_packages.remove(min_item)

    # group remaining unloaded packages with packages loaded on the truck routes
    groupSameAddress(unloaded_packages)

    # create a min heap for remaining packages with the min distance from the hub
    unloaded_heap = MinHeap()

    for i in range(len(unloaded_packages)):
        dis_hub = distanceLookup(0, int(package_list.lookup(unloaded_packages[i])[0]))
        pkg_id = unloaded_packages[i]
        unloaded_heap.add(dis_hub, pkg_id)

    # load remaining packages onto the truck routes as long as they have space
    while unloaded_heap.get_min() is not None:
        min_item = unloaded_heap.remove_min()[1]
        if len(truck_route1.packages) < truck_route1.capacity:
            if truck_route1.add(min_item):
                unloaded_packages.remove(min_item)
        elif len(truck_route2.packages) < truck_route2.capacity:
            if truck_route2.add(min_item):
                unloaded_packages.remove(min_item)
        else:
            truck_route3.add(min_item)
            unloaded_packages.remove(min_item)

    truck_route2_return = distanceLookup(int(package_list.lookup(truck_route2.packages[15])[0]), 0)
    truck_route3.start_time = int(truck_route2.time[15]) + (truck_route2_return * truck_route2.mpm)
    time_check(truck_route3)


# convert minutes in the day to hour:minute format and return to displaying to user
def getTime(time_min):
    hours = time_min // 60
    minutes = time_min % 60

    return '%0.2d' ':' '%0.2d' % (hours, minutes)


address_list = HashTable()
package_list = HashTable()
unloaded_packages = []  # hold package id until shipped
express_packages = []
truck_route1 = TruckRoute()
truck_route1.start_time = 480
truck_route2 = TruckRoute()
truck_route2.start_time = 545
truck_route3 = TruckRoute()
truck_route3.start_time = 900
total_distance_1 = 0
total_distance_2 = 0
total_distance_3 = 0
total_distance_all = 0
loadTrucks()

print('___________________________________________________________________________________________________')
print('Truck 1 Route 1:')
print('Depart Hub at:', getTime(truck_route1.start_time))
print('Package ID:', truck_route1.packages)
print('package distance:', truck_route1.distance)

for i in range(len(truck_route1.packages)):
    total_distance_1 += truck_route1.distance[i]

total_distance_all += total_distance_1
print('Total miles driven:', total_distance_1)

print('___________________________________________________________________________________________________')
print('Truck 2 Route 1:')
print('Depart Hub at:', getTime(truck_route2.start_time))
print('Package ID:', truck_route2.packages)
print('package distance:', truck_route2.distance)

for i in range(len(truck_route2.packages)):
    total_distance_2 += truck_route2.distance[i]

truck_route2_return = distanceLookup(int(package_list.lookup(truck_route2.packages[15])[0]), 0)
total_distance_2 += truck_route2_return
total_distance_all += total_distance_2
print('Total miles driven:', total_distance_2)

print('___________________________________________________________________________________________________')
print('Truck 2 Route 2:')
print('Depart Hub at:', getTime(truck_route3.start_time))
print('Package ID:', truck_route3.packages)
print('package distance:', truck_route3.distance)

for i in range(len(truck_route3.packages)):
    total_distance_3 += truck_route3.distance[i]

total_distance_all += total_distance_3
print('Total miles driven:', total_distance_3)

print('___________________________________________________________________________________________________')
print('Total distance driven by all trucks: %.2f miles' % total_distance_all)
choice = ''
while choice != 'Q':
    print('___________________________________________________________________________________________________')
    print('Choose an option:')
    print('A = View all packages')
    print('P = Package lookup')
    print('T = Check the status of all packages during a set time')
    print('Q = Quit')
    choice = input().upper()

    if choice == 'A':
        print('ID | Address                                 | City                |State | Zip | Deadline |Mass|')
        for item in range(package_list.size):
            k = package_list.lookup(item + 1)
            print('%-3s| %-40s| %-20s|  %-2s  |%-5s|   %-4s  |%3sk|' % ((item + 1), k[1], k[2], k[3], k[4],
                                                                        getTime(int(k[5])), k[6]))

    elif choice == 'P':
        package_id = input('Select a package ID: ')
        package_info = package_list.lookup(int(package_id))
        if package_info is not None:
            print('Package ID:', package_id)
            print('Address: ID:', package_info[0])
            print('Address: %s, %s %s, %s' % (package_info[1], package_info[2], package_info[3], package_info[4]))
            print('Mass:', package_info[6])
            print('Deadline:', getTime(int(package_info[5])))
        else:
            print('Package not found')
    elif choice == 'T':
        s_time = input('Enter start time(00:00):').split(':')
        e_time = input('Enter end time(00:00):').split(':')
        s_min = (int(s_time[0]) * 60) + int(s_time[1])
        e_min = (int(e_time[0]) * 60) + int(e_time[1])

        print('___________________________________________________________________________________________________')
        print('Truck 1, Route 1')
        for item in range(len(truck_route1.packages)):
            deadline = int(package_list.lookup(truck_route1.packages[item])[5])
            d_time = truck_route1.time[item]
            if e_min > truck_route1.start_time:
                if e_min > int(d_time):
                    print('%-2s Status: Delivered at %s' % (truck_route1.packages[item], getTime(int(d_time))))
                else:
                    print('%-2s Status: On Truck, ETA: %s' % (truck_route1.packages[item], getTime(int(d_time))))
            elif e_min < truck_route1.start_time:
                if package_list.lookup(truck_route1.packages[item])[7] == '1':
                    print('%-2s Status: Delayed On Flight, ETA: %s' % (truck_route1.packages[item], getTime(int(d_time))))
                else:
                    print('%-2s Status: At Hub, ETA: %s' % (truck_route1.packages[item], getTime(int(d_time))))

        print('___________________________________________________________________________________________________')
        print('Truck 2, Route 1')
        for item in range(len(truck_route2.packages)):
            deadline = int(package_list.lookup(truck_route2.packages[item])[5])
            d_time = truck_route2.time[item]
            if e_min > truck_route2.start_time:
                if e_min > int(d_time):
                    print('%-2s Status: Delivered at %s' % (truck_route2.packages[item], getTime(int(d_time))))
                else:
                    print('%-2s Status: On Truck, ETA: %s' % (truck_route2.packages[item], getTime(int(d_time))))
            elif e_min < truck_route2.start_time:
                if package_list.lookup(truck_route2.packages[item])[7] == '1':
                    print(
                        '%-2s Status: Delayed On Flight, ETA: %s' % (truck_route2.packages[item], getTime(int(d_time))))
                else:
                    print('%-2s Status: At Hub, ETA: %s' % (truck_route2.packages[item], getTime(int(d_time))))

        print('___________________________________________________________________________________________________')
        print('Truck 2, Route 2')
        for item in range(len(truck_route3.packages)):
            deadline = int(package_list.lookup(truck_route3.packages[item])[5])
            d_time = truck_route3.time[item]
            if e_min > truck_route3.start_time:
                if e_min > int(d_time):
                    print('%-2s Status: Delivered at %s' % (truck_route3.packages[item], getTime(int(d_time))))
                else:
                    print('%-2s Status: On Truck, ETA: %s' % (truck_route3.packages[item], getTime(int(d_time))))
            elif e_min < truck_route3.start_time:
                if package_list.lookup(truck_route3.packages[item])[7] == '1':
                    print(
                        '%-2s Status: Delayed On Flight, ETA: %s' % (truck_route3.packages[item], getTime(int(d_time))))
                else:
                    print('%-2s Status: At Hub, ETA: %s' % (truck_route3.packages[item], getTime(int(d_time))))
