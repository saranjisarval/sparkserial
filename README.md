# SparkSerial Pro

A premium serial communication and hardware testing tool built with Python and PyQt6. Inspired by professional tools like Docklight, **SparkSerial** provides a modern, high-performance interface for engineers and developers.

![Icon](assets/icon.png)

## Features

- **Professional Configuration**: Comprehensive port settings (Baudrate up to 921600, Data Bits, Parity, Stop Bits, Flow Control).
- **Command Shortcuts**: Save frequently used commands (Text or Hex) for quick access and batch testing.
- **Advanced Terminal**: Real-time logging with timestamps, Hex view, and autoscroll.
- **Persistence**: Automatically saves your command library and connection preferences.
- **Modern UI**: Dark-mode aesthetic with optimized layout for hardware debugging.
- **Cross-Platform**: Designed for macOS, Windows, and Linux.

## Installation

### From PyPI (Coming Soon)
```bash
pip install sparkserial
```

### Local Development
Ensure you have [uv](https://github.com/astral-sh/uv) installed:

```bash
./setup.sh
./run.sh
```

## Usage

After installing via pip, you can launch the tool directly:
```bash
sparkserial
```

## Technologies Used

- **UI Framework**: PyQt6
- **Serial Communication**: PySerial
- **Backend Architecture**: Worker-thread pattern for non-blocking I/O.
- **Styling**: Custom CSS for premium dark-mode aesthetics.
