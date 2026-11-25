
# 🖥️ WSL Monitor

A lightweight desktop monitoring application for Windows Subsystem for Linux (WSL), built with Python and CustomTkinter.

## Features

- Always-on-top floating dashboard
- Windows CPU and RAM monitoring
- Windows disk space monitoring
- Ubuntu and Kali Linux monitoring
- WSL distribution status (Running / Stopped)
- Linux filesystem usage
- Running process count
- Automatic refresh every 5 seconds
- Modern dark-mode interface

## Requirements

- Windows 10 or Windows 11
- Windows Subsystem for Linux (WSL)
- Python 3.10 or newer
- CustomTkinter
- Psutil

## Installation

Clone the repository:

```bash
git clone https://github.com/13loodeyes-pixel/WSL-Monitor.git
cd WSL-Monitor
```

Install dependencies:

```bash
pip install customtkinter psutil
```

## Usage

Run the application:

```bash
python monitor.py
```

The floating dashboard will display your Windows and WSL system information.

## Technologies Used

- Python
- CustomTkinter
- Psutil
- Windows Subsystem for Linux
- Subprocess
- Multithreading

## Roadmap

- [ ] Automatic WSL distribution detection
- [ ] CPU and memory usage per distribution
- [ ] System tray integration
- [ ] Custom refresh intervals
- [ ] Windows executable (.exe)
- [ ] Automated builds using GitHub Actions
- [ ] Resource usage history

## Limitations

CPU and RAM metrics represent Windows host usage.
Linux disk metrics represent filesystem usage, not physical VHDX file size.

## Contributing

Contributions, feature requests and bug reports are welcome.

## License

This project is intended to be released under the MIT License.

## Author

[13loodeyes-pixel](https://github.com/13loodeyes-pixel)

---

⭐ If you find this project useful, consider giving it a star!
