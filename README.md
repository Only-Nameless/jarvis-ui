# JARVIS Advanced UI

A futuristic AI Assistant interface inspired by Iron Man's JARVIS with advanced HUD panels, real-time system monitoring, and animated elements.

## Features

✨ **Futuristic HUD Design** - Multi-panel interface with scanning animations  
📊 **Real-time System Monitoring** - CPU, Memory, Storage, and Network status  
🎯 **Command Interface** - Input and feedback display  
⚡ **Animated Elements** - Rotating scanner, pulsing indicators, scan lines  
💻 **Diagnostics Panel** - System info, temperature, and activity log  
🎨 **Color-coded Status** - Different colors for different system states  

## Installation

### Prerequisites
- Python 3.7+
- tkinter (usually comes with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Only-Nameless/jarvis-ui.git
cd jarvis-ui
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the UI
```bash
python ui.py
```

The JARVIS interface will launch with:
- **Left Panel**: System Status (CPU, Memory, Network, Command History)
- **Center Panel**: Main Interface with circular scanner and command input
- **Right Panel**: Diagnostics (System Info, Temperature, Storage, Activity Log)
- **Top Bar**: JARVIS title, status indicator, and current time

## Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│ ⬢ JARVIS                                              ONLINE │
├──────────────┬───────────────────────────┬──────────────────┤
│ SYSTEM       │                           │ DIAGNOSTICS      │
│ STATUS       │   MAIN INTERFACE          │                  │
│              │                           │                  │
│ CPU: [====]  │   ╭─────────────╮         │ CPU Temp: [===]  │
│ MEM: [====]  │   │      ◯      │         │ Storage: [====]  │
│ NET: ●       │   │   ╱   ╲    │         │                  │
│              │   │  │     │   │         │ Activity Log:    │
│              │   │   ╲   ╱    │         │ ◆ System init   │
│              │   │      ◉      │         │ ◆ Ready        │
│ Recent:      │   │             │         │                  │
│ • command1   │   ╰─────────────╯         │                  │
│ • command2   │                           │                  │
└──────────────┴───────────────────────────┴──────────────────┘
```

## Customization

### Colors
Edit the color scheme at the top of `ui.py`:
```python
PRIMARY_COLOR = "#00D9FF"      # Cyan
SECONDARY_COLOR = "#39FF14"    # Green
ACCENT_COLOR = "#FF006E"       # Pink/Red
```

### Window Size
Change the dimensions:
```python
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
```

### Animation Speed
Modify animation intervals in `_animate()` and `_update_stats()`

## System Requirements

- Works on Windows, macOS, and Linux
- Requires `psutil` for system monitoring
- tkinter must be installed (usually included with Python)

## Troubleshooting

### tkinter not found
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (with Homebrew)
brew install python-tk

# Windows - reinstall Python with tkinter checked
```

### psutil permission denied
On some systems, you may need elevated permissions:
```bash
sudo pip install psutil
```

## Future Enhancements

- Voice command integration
- More interactive panels
- Advanced data visualization
- Theme customization
- System alerts and notifications
- Command history search

## License

MIT License - Feel free to use and modify

---

**Made with ❤️ by Only-Nameless**
