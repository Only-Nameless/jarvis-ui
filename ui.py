"""
Advanced JARVIS UI
Futuristic AI Assistant Interface with HUD panels and system stats
"""

import tkinter as tk
from tkinter import Canvas
import math
import time
import threading
import psutil
from datetime import datetime

# ==================== COLOR SCHEME ====================
BG_COLOR = "#0A0E27"          # Deep blue background
PRIMARY_COLOR = "#00D9FF"     # Cyan
SECONDARY_COLOR = "#39FF14"   # Green
ACCENT_COLOR = "#FF006E"      # Pink/Red accent
TEXT_COLOR = "#E0E6FF"        # Light text
PANEL_COLOR = "#0F1535"       # Panel background
BORDER_COLOR = "#1A2A4F"      # Border color
GLOW_COLOR = "#00A8CC"        # Glow effect

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

class AdvancedJarvisUI:
    """Advanced JARVIS UI with HUD panels and animations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS - Advanced AI System")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        # Animation variables
        self.current_angle = 0
        self.pulse_value = 0
        self.command_history = []
        self.system_stats = {}
        self.glitch_offset = 0
        
        # Create main canvas
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                           bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Draw UI elements
        self._draw_background()
        self._draw_top_bar()
        self._draw_left_panel()
        self._draw_center_panel()
        self._draw_right_panel()
        self._draw_decorative_elements()
        
        # Start animations
        self._animate()
        self._update_stats()
        
        print("[JARVIS UI] Advanced interface initialized")
    
    def _draw_background(self):
        """Draw enhanced background with grid and ambient effects"""
        # Subtle grid background
        for x in range(0, WINDOW_WIDTH, 40):
            self.canvas.create_line(x, 0, x, WINDOW_HEIGHT, 
                                   fill=BORDER_COLOR, width=0.5, stipple="gray50")
        
        for y in range(0, WINDOW_HEIGHT, 40):
            self.canvas.create_line(0, y, WINDOW_WIDTH, y,
                                   fill=BORDER_COLOR, width=0.5, stipple="gray50")
        
        # Decorative corner elements
        corner_size = 20
        self.canvas.create_line(0, corner_size, 0, 0, corner_size, 0, 
                               fill=PRIMARY_COLOR, width=1.5)
        self.canvas.create_line(WINDOW_WIDTH - corner_size, 0, WINDOW_WIDTH, 0, 
                               WINDOW_WIDTH, corner_size, fill=PRIMARY_COLOR, width=1.5)
        self.canvas.create_line(0, WINDOW_HEIGHT - corner_size, 0, WINDOW_HEIGHT, 
                               corner_size, WINDOW_HEIGHT, fill=PRIMARY_COLOR, width=1.5)
        self.canvas.create_line(WINDOW_WIDTH - corner_size, WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, 
                               WINDOW_WIDTH, WINDOW_HEIGHT - corner_size, fill=PRIMARY_COLOR, width=1.5)
        
        # Scan line effect
        self.scan_line = self.canvas.create_line(0, 100, WINDOW_WIDTH, 100,
                                                fill=PRIMARY_COLOR, width=1.5, stipple="gray75")
    
    def _draw_top_bar(self):
        """Draw top status bar with enhanced styling"""
        # Top bar background
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, 70,
                                     fill=PANEL_COLOR, outline=PRIMARY_COLOR, width=2)
        
        # Accent line under top bar
        self.canvas.create_line(0, 70, WINDOW_WIDTH, 70,
                               fill=SECONDARY_COLOR, width=2)
        
        # JARVIS title with glow effect
        self.canvas.create_text(30, 35, text="◈ JARVIS",
                               font=("Arial", 26, "bold"),
                               fill=SECONDARY_COLOR, anchor="w")
        
        # Subtitle
        self.canvas.create_text(30, 55, text="Advanced AI System v2.1.0",
                               font=("Arial", 9),
                               fill=TEXT_COLOR, anchor="w")
        
        # Status indicator with pulsing effect
        self.status_circle = self.canvas.create_oval(1310, 22, 1340, 52,
                                                    fill=SECONDARY_COLOR, 
                                                    outline=PRIMARY_COLOR, width=2)
        self.canvas.create_text(1355, 37, text="ONLINE",
                               font=("Arial", 11, "bold"),
                               fill=SECONDARY_COLOR, anchor="w")
        
        # Time display with better styling
        self.time_text = self.canvas.create_text(WINDOW_WIDTH - 150, 35,
                                                text="00:00:00",
                                                font=("Courier", 14, "bold"),
                                                fill=PRIMARY_COLOR)
        
        # Date display
        self.date_text = self.canvas.create_text(WINDOW_WIDTH - 150, 55,
                                                text="00/00/00",
                                                font=("Arial", 9),
                                                fill=TEXT_COLOR)
    
    def _draw_left_panel(self):
        """Draw left panel with system stats and better styling"""
        left_x = 10
        top_y = 80
        panel_width = 290
        panel_height = WINDOW_HEIGHT - 90
        
        # Panel background
        self.canvas.create_rectangle(left_x, top_y, left_x + panel_width, top_y + panel_height,
                                     fill=PANEL_COLOR, outline=PRIMARY_COLOR, width=2.5)
        
        # Panel header bar
        self.canvas.create_rectangle(left_x, top_y, left_x + panel_width, top_y + 40,
                                     fill=BORDER_COLOR, outline=PRIMARY_COLOR, width=1)
        
        # Title
        self.canvas.create_text(left_x + 145, top_y + 20,
                               text="SYSTEM STATUS",
                               font=("Arial", 12, "bold"),
                               fill=PRIMARY_COLOR)
        
        # CPU status section
        self.canvas.create_text(left_x + 20, top_y + 70,
                               text="CPU LOAD",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.canvas.create_rectangle(left_x + 20, top_y + 90, left_x + 270, top_y + 105,
                                    fill=BORDER_COLOR, outline=PRIMARY_COLOR, width=1)
        self.cpu_bar_fill = self.canvas.create_rectangle(left_x + 20, top_y + 90, left_x + 20, top_y + 105,
                                                        fill=PRIMARY_COLOR, outline="")
        self.cpu_value = self.canvas.create_text(left_x + 210, top_y + 97,
                                                text="0%",
                                                font=("Arial", 9, "bold"),
                                                fill=PRIMARY_COLOR)
        
        # Memory status
        self.canvas.create_text(left_x + 20, top_y + 140,
                               text="MEMORY",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.canvas.create_rectangle(left_x + 20, top_y + 160, left_x + 270, top_y + 175,
                                    fill=BORDER_COLOR, outline=PRIMARY_COLOR, width=1)
        self.mem_bar_fill = self.canvas.create_rectangle(left_x + 20, top_y + 160, left_x + 20, top_y + 175,
                                                        fill=PRIMARY_COLOR, outline="")
        self.mem_value = self.canvas.create_text(left_x + 210, top_y + 167,
                                                text="0%",
                                                font=("Arial", 9, "bold"),
                                                fill=PRIMARY_COLOR)
        
        # Network status
        self.canvas.create_text(left_x + 20, top_y + 210,
                               text="NETWORK",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.network_indicator = self.canvas.create_oval(left_x + 20, top_y + 230, left_x + 40, top_y + 250,
                                                        fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=2)
        self.canvas.create_text(left_x + 50, top_y + 240,
                               text="Connected",
                               font=("Arial", 9),
                               fill=TEXT_COLOR, anchor="w")
        
        # Separator line
        self.canvas.create_line(left_x + 10, top_y + 290, left_x + 280, top_y + 290,
                               fill=BORDER_COLOR, width=1)
        
        # Command history
        self.canvas.create_text(left_x + 20, top_y + 310,
                               text="RECENT COMMANDS",
                               font=("Arial", 10, "bold"),
                               fill=PRIMARY_COLOR, anchor="w")
        
        self.history_display = self.canvas.create_text(left_x + 20, top_y + 350,
                                                       text="No commands yet",
                                                       font=("Arial", 8),
                                                       fill=TEXT_COLOR, anchor="nw", width=250)
    
    def _draw_center_panel(self):
        """Draw center panel with main JARVIS interface"""
        center_x = 320
        top_y = 80
        panel_width = 760
        panel_height = WINDOW_HEIGHT - 90
        center_panel_x = center_x + panel_width // 2
        center_panel_y = top_y + panel_height // 2
        
        # Panel background
        self.canvas.create_rectangle(center_x, top_y, center_x + panel_width, top_y + panel_height,
                                     fill=PANEL_COLOR, outline=SECONDARY_COLOR, width=2.5)
        
        # Panel header
        self.canvas.create_rectangle(center_x, top_y, center_x + panel_width, top_y + 40,
                                     fill=BORDER_COLOR, outline=SECONDARY_COLOR, width=1)
        
        # Title
        self.canvas.create_text(center_panel_x, top_y + 20,
                               text="MAIN INTERFACE",
                               font=("Arial", 12, "bold"),
                               fill=SECONDARY_COLOR)
        
        # Draw enhanced circular scanner
        radius = 90
        
        # Outer glowing circle
        for i in range(3, 0, -1):
            self.canvas.create_oval(
                center_panel_x - radius - i*2, center_panel_y - radius - i*2,
                center_panel_x + radius + i*2, center_panel_y + radius + i*2,
                outline=GLOW_COLOR, width=0.5, stipple="gray75"
            )
        
        # Main outer circle
        self.canvas.create_oval(center_panel_x - radius, center_panel_y - radius,
                               center_panel_x + radius, center_panel_y + radius,
                               outline=SECONDARY_COLOR, width=3)
        
        # Inner circles with varying opacity
        for r, color in [(70, PRIMARY_COLOR), (50, BORDER_COLOR), (30, PRIMARY_COLOR)]:
            self.canvas.create_oval(center_panel_x - r, center_panel_y - r,
                                    center_panel_x + r, center_panel_y + r,
                                    outline=color, width=1.5, stipple="gray50")
        
        # Crosshair with better styling
        cross_size = 25
        self.canvas.create_line(center_panel_x - cross_size, center_panel_y, 
                               center_panel_x - 10, center_panel_y,
                               fill=PRIMARY_COLOR, width=2)
        self.canvas.create_line(center_panel_x + 10, center_panel_y, 
                               center_panel_x + cross_size, center_panel_y,
                               fill=PRIMARY_COLOR, width=2)
        self.canvas.create_line(center_panel_x, center_panel_y - cross_size, 
                               center_panel_x, center_panel_y - 10,
                               fill=PRIMARY_COLOR, width=2)
        self.canvas.create_line(center_panel_x, center_panel_y + 10, 
                               center_panel_x, center_panel_y + cross_size,
                               fill=PRIMARY_COLOR, width=2)
        
        # Center dot
        self.center_dot = self.canvas.create_oval(center_panel_x - 6, center_panel_y - 6,
                                                 center_panel_x + 6, center_panel_y + 6,
                                                 fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=2)
        
        # Scanning dot animation
        self.scanner_dot = self.canvas.create_oval(center_panel_x - 8, center_panel_y - radius - 8,
                                                  center_panel_x + 8, center_panel_y - radius + 8,
                                                  fill=PRIMARY_COLOR, outline=SECONDARY_COLOR, width=2)
        
        # Status text
        self.main_status = self.canvas.create_text(center_panel_x, center_panel_y + 140,
                                                   text="SYSTEM READY",
                                                   font=("Arial", 14, "bold"),
                                                   fill=SECONDARY_COLOR)
        
        # Command input area
        self.canvas.create_text(center_x + 30, top_y + 340,
                               text="INPUT COMMAND:",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.canvas.create_rectangle(center_x + 30, top_y + 360, center_x + panel_width - 30, top_y + 400,
                                    fill="#050A1A", outline=PRIMARY_COLOR, width=2)
        
        self.command_text = self.canvas.create_text(center_x + 40, top_y + 380,
                                                    text="> Ready for input",
                                                    font=("Courier", 10),
                                                    fill=PRIMARY_COLOR, anchor="w")
        
        # Store center coordinates
        self.center_panel_coords = (center_panel_x, center_panel_y, radius)
    
    def _draw_right_panel(self):
        """Draw right panel with diagnostics"""
        right_x = WINDOW_WIDTH - 300
        top_y = 80
        panel_width = 290
        panel_height = WINDOW_HEIGHT - 90
        
        # Panel background
        self.canvas.create_rectangle(right_x, top_y, right_x + panel_width, top_y + panel_height,
                                     fill=PANEL_COLOR, outline=ACCENT_COLOR, width=2.5)
        
        # Panel header
        self.canvas.create_rectangle(right_x, top_y, right_x + panel_width, top_y + 40,
                                     fill=BORDER_COLOR, outline=ACCENT_COLOR, width=1)
        
        # Title
        self.canvas.create_text(right_x + 145, top_y + 20,
                               text="DIAGNOSTICS",
                               font=("Arial", 12, "bold"),
                               fill=ACCENT_COLOR)
        
        # System info
        self.system_info = self.canvas.create_text(right_x + 20, top_y + 70,
                                                   text="System: Online\nVersion: 2.1.0\nUptime: 00:00:00",
                                                   font=("Arial", 9),
                                                   fill=TEXT_COLOR, anchor="nw")
        
        # Temperature
        self.canvas.create_text(right_x + 20, top_y + 160,
                               text="TEMPERATURE",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.canvas.create_rectangle(right_x + 20, top_y + 180, right_x + 270, top_y + 195,
                                    fill=BORDER_COLOR, outline=ACCENT_COLOR, width=1)
        self.temp_bar_fill = self.canvas.create_rectangle(right_x + 20, top_y + 180, right_x + 20, top_y + 195,
                                                         fill=ACCENT_COLOR, outline="")
        self.temp_value = self.canvas.create_text(right_x + 210, top_y + 187,
                                                 text="0°C",
                                                 font=("Arial", 9, "bold"),
                                                 fill=ACCENT_COLOR)
        
        # Storage
        self.canvas.create_text(right_x + 20, top_y + 230,
                               text="STORAGE",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.canvas.create_rectangle(right_x + 20, top_y + 250, right_x + 270, top_y + 265,
                                    fill=BORDER_COLOR, outline=ACCENT_COLOR, width=1)
        self.storage_bar_fill = self.canvas.create_rectangle(right_x + 20, top_y + 250, right_x + 20, top_y + 265,
                                                            fill=ACCENT_COLOR, outline="")
        self.storage_value = self.canvas.create_text(right_x + 210, top_y + 257,
                                                    text="0%",
                                                    font=("Arial", 9, "bold"),
                                                    fill=ACCENT_COLOR)
        
        # Separator
        self.canvas.create_line(right_x + 10, top_y + 300, right_x + 280, top_y + 300,
                               fill=BORDER_COLOR, width=1)
        
        # Activity log
        self.canvas.create_text(right_x + 20, top_y + 320,
                               text="ACTIVITY LOG",
                               font=("Arial", 10, "bold"),
                               fill=ACCENT_COLOR, anchor="w")
        
        self.activity_log = self.canvas.create_text(right_x + 20, top_y + 360,
                                                    text="System initialized\nListening for commands",
                                                    font=("Arial", 8),
                                                    fill=TEXT_COLOR, anchor="nw", width=250)
    
    def _draw_decorative_elements(self):
        """Draw additional decorative elements"""
        # Corner brackets for center panel
        bracket_size = 15
        center_x = 320
        top_y = 80
        
        # Top-left corner
        self.canvas.create_line(center_x, top_y, center_x + bracket_size, top_y,
                               fill=PRIMARY_COLOR, width=1.5)
        self.canvas.create_line(center_x, top_y, center_x, top_y + bracket_size,
                               fill=PRIMARY_COLOR, width=1.5)
        
        # Top-right corner
        right_edge = center_x + 760
        self.canvas.create_line(right_edge - bracket_size, top_y, right_edge, top_y,
                               fill=PRIMARY_COLOR, width=1.5)
        self.canvas.create_line(right_edge, top_y, right_edge, top_y + bracket_size,
                               fill=PRIMARY_COLOR, width=1.5)
    
    def _animate(self):
        """Main animation loop with smooth effects"""
        # Update scanner dot position
        if hasattr(self, 'center_panel_coords'):
            center_x, center_y, radius = self.center_panel_coords
            rad = math.radians(self.current_angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            
            self.canvas.coords(self.scanner_dot, x - 8, y - 8, x + 8, y + 8)
            self.current_angle = (self.current_angle + 1.5) % 360
        
        # Update scan line
        y_pos = (int(time.time() * 150) % WINDOW_HEIGHT)
        self.canvas.coords(self.scan_line, 0, y_pos, WINDOW_WIDTH, y_pos)
        
        # Pulse effect on center dot
        pulse_size = 6 + 2.5 * math.sin(time.time() * 3)
        if hasattr(self, 'center_panel_coords'):
            center_x, center_y, _ = self.center_panel_coords
            self.canvas.coords(self.center_dot, 
                              center_x - pulse_size, center_y - pulse_size,
                              center_x + pulse_size, center_y + pulse_size)
        
        # Update time
        now = datetime.now()
        self.canvas.itemconfig(self.time_text, text=now.strftime("%H:%M:%S"))
        self.canvas.itemconfig(self.date_text, text=now.strftime("%m/%d/%y"))
        
        # Continue animation
        self.root.after(50, self._animate)
    
    def _update_stats(self):
        """Update system statistics with bar animations"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_width = int((cpu_percent / 100) * 250)
            self.canvas.coords(self.cpu_bar_fill, 20, 90, 20 + cpu_width, 105)
            self.canvas.itemconfig(self.cpu_value, text=f"{cpu_percent:.0f}%")
            
            # Memory usage
            memory = psutil.virtual_memory()
            mem_width = int((memory.percent / 100) * 250)
            self.canvas.coords(self.mem_bar_fill, 20, 160, 20 + mem_width, 175)
            self.canvas.itemconfig(self.mem_value, text=f"{memory.percent:.0f}%")
            
            # Storage usage
            disk = psutil.disk_usage('/')
            disk_width = int((disk.percent / 100) * 250)
            self.canvas.coords(self.storage_bar_fill, 20 + 980, 250, 20 + 980 + disk_width, 265)
            self.canvas.itemconfig(self.storage_value, text=f"{disk.percent:.0f}%")
            
            # Temperature (simulated)
            import random
            temp = 45 + random.randint(-5, 10)
            temp_width = int((temp / 100) * 250)
            self.canvas.coords(self.temp_bar_fill, 20 + 980, 180, 20 + 980 + temp_width, 195)
            self.canvas.itemconfig(self.temp_value, text=f"{temp}°C")
        
        except Exception as e:
            print(f"[Stats] Error: {e}")
        
        self.root.after(2000, self._update_stats)
    
    def update_command(self, command_text):
        """Update command display"""
        self.canvas.itemconfig(self.command_text, text=f"> {command_text}")
        self.command_history.append(command_text)
        
        history_text = "\n".join(self.command_history[-5:])
        self.canvas.itemconfig(self.history_display, text=history_text)
    
    def update_status(self, status_text, status_color=SECONDARY_COLOR):
        """Update main status display"""
        self.canvas.itemconfig(self.main_status, text=status_text, fill=status_color)
    
    def update_activity(self, activity_text):
        """Update activity log"""
        self.canvas.itemconfig(self.activity_log, text=activity_text)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = AdvancedJarvisUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
