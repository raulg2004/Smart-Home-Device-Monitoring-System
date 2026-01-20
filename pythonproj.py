import asyncio
import random
import threading
import queue
import json
from abc import ABC, abstractmethod
from datetime import datetime
from functools import reduce 

#here is the oop layer, the devices
class SmartDevice(ABC):
    def __init__(self, device_id, name, location):
        self.device_id = device_id
        self.name = name
        self.location = location
        self.device_type = "GENERIC"
        self.is_connected = False
    
    async def connect(self):
        #the devices conected with delay
        print(f"{self.name} -> connecting...")
        delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(delay)
        self.is_connected = True
        print(f"{self.name} was connected successfully in {delay:.2f}s.")
    
    async def send_update(self):
        return {
            "device_id": self.device_id,
            "name": self.name,
            "location": self.location,
            "device_type": self.device_type,
            "timestamp": datetime.now().isoformat(),
            **self._get_status()
        }
    
    @abstractmethod
    def _get_status(self):
        pass
    
    @abstractmethod
    def execute_command(self, command, **kwargs):
        pass


class SmartBulb(SmartDevice):
    def __init__(self, device_id, name, location):
        super().__init__(device_id, name, location)
        self.device_type = "BULB"
        self.is_on = False
        self._brightness = 0
    
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        if value < 0:
            self._brightness = 0
        elif value > 100:
            self._brightness = 100
        else:
            self._brightness = value
    
    def _get_status(self):
        return {"is_on": self.is_on, "brightness": self.brightness}
    
    def execute_command(self, command, **kwargs):
        if command == "turn_on":
            self.is_on = True
            self.brightness = kwargs.get("brightness", 100)
            print(f"{self.device_type} command executed: Light turned on at {self.brightness}% brightness.")


class SmartThermostat(SmartDevice):
    def __init__(self, device_id, name, location):
        super().__init__(device_id, name, location)
        self.device_type = "THERMOSTAT"
        self.current_temp = random.uniform(20, 28)
        self.target_temp = 22.0
        self.humidity = 50.0
    
    def _get_status(self):
        self.current_temp += random.uniform(-1, 2)
        return {
            "current_temp": round(self.current_temp, 1),
            "target_temp": self.target_temp,
            "humidity": round(self.humidity, 1)
        }
    
    def execute_command(self, command, **kwargs):
        if command == "cool_down":
            self.current_temp = 22.0
            self.target_temp = 22.0
            print(f"{self.device_type} command executed: Temperature adjusted.")


class SmartCamera(SmartDevice):
    def __init__(self, device_id, name, location):
        super().__init__(device_id, name, location) 
        self.device_type = "CAMERA"
        self.motion_detected = False
        self._battery_level = 100
        self.last_snapshot = None
    
    @property
    def battery_level(self):
        return self._battery_level
    
    @battery_level.setter
    def battery_level(self, value):
        if value < 0:
            self._battery_level = 0
        elif value > 100:
            self._battery_level = 100
        else:
            self._battery_level = value
    
    def _get_status(self):
        self.motion_detected = random.random() < 0.15
        
        #the battery drain to see low battery alerts
        self.battery_level = self.battery_level - random.uniform(5, 12)
        
        #extra 10% drain when motion is detected
        if self.motion_detected:
            self.last_snapshot = datetime.now().isoformat()
            self.battery_level = self.battery_level - 10
        
        return {
            "motion_detected": self.motion_detected,
            "battery_level": round(self.battery_level, 1),
            "last_snapshot": self.last_snapshot
        }
    
    def execute_command(self, command, **kwargs):
        if command == "snapshot":
            self.last_snapshot = datetime.now().isoformat()
            print(f"{self.device_type} command executed: Snapshot captured.")


#network simulation
async def device_loop(device, data_queue, devices, updates_list):
    #each device sends updates asynchronously
    while True:
        await asyncio.sleep(random.uniform(2, 4))
        update = await device.send_update()
        
        #the small progress indicator
        print(".", end="", flush=True)
        
        #checking for the alerts and printing them
        if device.device_type == "THERMOSTAT" and update['current_temp'] > 30:
            print(f"\n ALERT: High Temp detected! Triggering cooling...")
            device.execute_command("cool_down")
        
        if device.device_type == "CAMERA" and update['motion_detected']:
            print(f"\n ALERT: Motion detected at {device.location}!")
        
        if device.device_type == "CAMERA" and update['battery_level'] < 10:
            print(f"\n WARNING: {device.name} battery low ({update['battery_level']}%)")
        
        data_queue.put(update)
        updates_list.append(update)  #also store for analytics


async def run_network(devices, data_queue, updates_list):
    #here we run all the devices concurrently
    tasks = [asyncio.create_task(device_loop(d, data_queue, devices, updates_list)) for d in devices]
    await asyncio.gather(*tasks)


#this is the functional layer for analytics
def process_analytics(updates):
    #so we map, filter and than reduce
    #map the extract temperatures
    temps = list(map(lambda u: u.get('current_temp', 0), 
        filter(lambda u: u['device_type'] == 'THERMOSTAT', updates)))
    
    #filter the critical events
    critical = list(filter(lambda u: 
        (u['device_type'] == 'THERMOSTAT' and u.get('current_temp', 0) > 30) or
        (u['device_type'] == 'CAMERA' and u.get('battery_level', 100) < 10),
        updates))
    
    #reduce the average temperature and total brightness
    avg_temp = reduce(lambda acc, t: acc + t, temps, 0) / len(temps) if temps else 0
    
    brightness_vals = list(map(lambda u: u.get('brightness', 0),
        filter(lambda u: u['device_type'] == 'BULB' and u.get('is_on'), updates)))
    total_brightness = reduce(lambda acc, b: acc + b, brightness_vals, 0)
    
    #calculate average battery level from cameras
    battery_vals = list(map(lambda u: u.get('battery_level', 0),
        filter(lambda u: u['device_type'] == 'CAMERA', updates)))
    avg_battery = reduce(lambda acc, b: acc + b, battery_vals, 0) / len(battery_vals) if battery_vals else 0
    
    return {
        "avg_temp": round(avg_temp, 1),
        "critical_count": len(critical),
        "total_brightness": total_brightness,
        "avg_battery": round(avg_battery, 1),
        "total_updates": len(updates)
    }


#storage layer
def storage_worker(data_queue):
    #the background thread writes to the disk
    print("Storage Thread Started...")
    with open("history.log", "a") as f:
        while True:
            try:
                update = data_queue.get(timeout=1)
                f.write(json.dumps(update) + "\n")
                f.flush()
            except queue.Empty:
                continue


#main fuction
async def main():
    #we create a queue
    data_queue = queue.Queue()
    updates = []  #updates for analytics
    
    #than starting the storage thread
    thread = threading.Thread(target=storage_worker, args=(data_queue,), daemon=True)
    thread.start()
    print("Connecting devices...")

    #create the devices 
    devices = [
        SmartBulb("b1", "Smart Bulb", "Living Room"),
        SmartThermostat("t1", "Smart Thermostat", "Main Room"),
        SmartCamera("c1", "Smart Camera", "Entrance")
    ]
    
    #conect the dev concurently
    await asyncio.gather(*[d.connect() for d in devices])
    print("All devices connected!")
    
    #initial states
    devices[0].brightness = 80
    devices[0].is_on = True
    
    #run for 30 sec
    try:
        await asyncio.wait_for(run_network(devices, data_queue, updates), timeout=30)
    except asyncio.TimeoutError:
        pass
    
    #collect any remaining updates from queue
    while not data_queue.empty():
        update = data_queue.get_nowait()
        if update not in updates:
            updates.append(update)
    
    print("\nANALYTICS SUMMARY\n")
    
    if updates:
        analytics = process_analytics(updates)
        print(f"Total Updates Processed: {analytics['total_updates']}")
        print(f"Average Temperature: {analytics['avg_temp']}°C")
        print(f"Total Brightness: {analytics['total_brightness']}%")
        print(f"Average Battery Level: {analytics['avg_battery']}%")
        print(f"Critical Events: {analytics['critical_count']}")


if __name__ == "__main__":
    asyncio.run(main())