# Smart Home Device Monitoring System

A Python-based smart home monitoring system that simulates and manages multiple IoT devices concurrently using asynchronous programming, OOP principles, and functional programming paradigms.

## Features

- **Multi-Device Support**: Simulates three types of smart devices:
  - Smart Bulbs with brightness control
  - Smart Thermostats with temperature monitoring
  - Smart Cameras with motion detection and battery monitoring

- **Asynchronous Device Management**: Uses Python's `asyncio` for concurrent device operation and network simulation

- **Real-Time Monitoring**: Continuous device status updates with automatic alert detection

- **Data Persistence**: Background thread stores all device updates to a log file

- **Analytics Dashboard**: Functional programming approach for data analysis including:
  - Average temperature tracking
  - Total brightness monitoring
  - Battery level statistics
  - Critical event counting

## System Architecture

### OOP Layer (Devices)
- Abstract base class `SmartDevice` with concrete implementations
- Property decorators for validated data access
- Polymorphic command execution

### Network Layer
- Asynchronous device loops with random update intervals
- Concurrent task management using `asyncio.gather()`
- Simulated connection delays

### Functional Layer (Analytics)
- `map()` for data extraction
- `filter()` for event filtering
- `reduce()` for aggregations

### Storage Layer
- Thread-based background worker
- Queue-based data pipeline
- JSON-formatted logging to `history.log`

## Requirements

```bash
Python 3.7+
```

No external dependencies required - uses only Python standard library.

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd UVTyear3
```

2. No additional installation needed!

## Usage

Run the application:
```bash
python pythonproj.py
```

The system will:
1. Connect all devices with simulated delays
2. Run for 30 seconds, collecting device updates
3. Display real-time alerts for:
   - High temperature events (>30°C)
   - Motion detection
   - Low battery warnings (<10%)
4. Generate analytics summary at the end

## Sample Output

```
Connecting devices...
Smart Bulb -> connecting...
Smart Thermostat -> connecting...
Smart Camera -> connecting...
Smart Bulb was connected successfully in 1.23s.
Smart Thermostat was connected successfully in 1.45s.
Smart Camera was connected successfully in 0.87s.
All devices connected!
Storage Thread Started...
............
ALERT: Motion detected at Entrance!
..........
WARNING: Smart Camera battery low (8.3%)
.......

ANALYTICS SUMMARY

Total Updates Processed: 24
Average Temperature: 24.3°C
Total Brightness: 960%
Average Battery Level: 35.2%
Critical Events: 3
```

## Project Structure

```
.
├── pythonproj.py       # Main application file
├── history.log         # Auto-generated device update log
└── README.md          # This file
```

## Device Classes

### SmartBulb
- **Properties**: `is_on`, `brightness` (0-100%)
- **Commands**: `turn_on` with brightness parameter

### SmartThermostat
- **Properties**: `current_temp`, `target_temp`, `humidity`
- **Commands**: `cool_down` to adjust temperature
- **Alerts**: Triggers when temperature exceeds 30°C

### SmartCamera
- **Properties**: `motion_detected`, `battery_level`, `last_snapshot`
- **Commands**: `snapshot` to capture images
- **Alerts**: Motion detection and low battery warnings
- **Battery Drain**: Simulates 5-12% drain per update, +10% on motion

## Key Concepts Demonstrated

- **Object-Oriented Programming**: Abstract classes, inheritance, encapsulation
- **Asynchronous Programming**: `async`/`await`, concurrent task execution
- **Functional Programming**: `map()`, `filter()`, `reduce()` for data processing
- **Multi-threading**: Background storage worker
- **Design Patterns**: Template method, observer-like event handling

## Future Enhancements

- [ ] Add more device types (locks, sensors, etc.)
- [ ] Web dashboard for visualization
- [ ] Database integration
- [ ] Remote device control API
- [ ] Machine learning for predictive alerts

## License

This project is available for educational purposes.

## Author

Raul Peres
