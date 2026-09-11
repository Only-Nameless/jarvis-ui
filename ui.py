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
        
        # Create main canvas
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                           bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Draw UI elements
        self._draw_background()
        self._draw_left_panel()
        self._draw_center_panel()
        self._draw_right_panel()
        self._draw_top_bar()
        
        # Start animations
        self._animate()
        self._update_stats()
        
        print("[JARVIS UI] Advanced interface initialized")
    
    def _draw_background(self):
        """Draw animated background grid and scan lines"""
        # Vertical grid lines
        for x in range(0, WINDOW_WIDTH, 50):
            self.canvas.create_line(x, 0, x, WINDOW_HEIGHT, 
                                   fill=BORDER_COLOR, width=0.5, stipple="gray25")
        
        # Horizontal grid lines
        for y in range(0, WINDOW_HEIGHT, 50):
            self.canvas.create_line(0, y, WINDOW_WIDTH, y,
                                   fill=BORDER_COLOR, width=0.5, stipple="gray25")
        
        # Scan line effect (horizontal line that moves)
        self.scan_line = self.canvas.create_line(0, 100, WINDOW_WIDTH, 100,
                                                fill=PRIMARY_COLOR, width=2, stipple="gray50")
    
    def _draw_top_bar(self):
        """Draw top status bar"""
        # Top bar background
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, 60,
                                     fill=PANEL_COLOR, outline=PRIMARY_COLOR, width=2)
        
        # JARVIS title
        self.canvas.create_text(30, 30, text="⬢ JARVIS",
                               font=("Arial", 24, "bold"),
                               fill=SECONDARY_COLOR, anchor="w")
        
        # Status indicator
        self.status_circle = self.canvas.create_oval(1300, 20, 1330, 50,
                                                    fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=2)
        self.canvas.create_text(1345, 35, text="ONLINE",
                               font=("Arial", 10, "bold"),
                               fill=SECONDARY_COLOR, anchor="w")
        
        # Time display
        self.time_text = self.canvas.create_text(WINDOW_WIDTH - 200, 30,
                                                text="00:00:00",
                                                font=("Arial", 12, "bold"),
                                                fill=TEXT_COLOR)
    
    def _draw_left_panel(self):
        """Draw left panel with system stats"""
        left_x = 10
        top_y = 70
        panel_width = 280
        panel_height = WINDOW_HEIGHT - 80
        
        # Panel border
        self.canvas.create_rectangle(left_x, top_y, left_x + panel_width, top_y + panel_height,
                                     fill=PANEL_COLOR, outline=PRIMARY_COLOR, width=2)
        
        # Title
        self.canvas.create_text(left_x + 140, top_y + 20,
                               text="SYSTEM STATUS",
                               font=("Arial", 12, "bold"),
                               fill=PRIMARY_COLOR)
        
        # CPU status
        self.canvas.create_text(left_x + 15, top_y + 60,
                               text="CPU",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        self.cpu_bar = self.canvas.create_rectangle(left_x + 15, top_y + 80, left_x + 260, top_y + 95,
                                                   fill=BORDER_COLOR, outline=PRIMARY_COLOR, width=1)
        self.cpu_value = self.canvas.create_text(left_x + 200, top_y + 87,
                                                text="0%",
                                                font=("Arial", 9, "bold"),
                                                fill=PRIMARY_COLOR)
        
        # Memory status
        self.canvas.create_text(left_x + 15, top_y + 130,
                               text="MEMORY",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        self.mem_bar = self.canvas.create_rectangle(left_x + 15, top_y + 150, left_x + 260, top_y + 165,
                                                   fill=BORDER_COLOR, outline=PRIMARY_COLOR, width=1)
        self.mem_value = self.canvas.create_text(left_x + 200, top_y + 157,
                                                text="0%",
                                                font=("Arial", 9, "bold"),
                                                fill=PRIMARY_COLOR)
        
        # Network status
        self.canvas.create_text(left_x + 15, top_y + 200,
                               text="NETWORK",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        self.network_indicator = self.canvas.create_oval(left_x + 15, top_y + 220, left_x + 35, top_y + 240,
                                                        fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=2)
        self.canvas.create_text(left_x + 45, top_y + 230,
                               text="Connected",
                               font=("Arial", 9),
                               fill=TEXT_COLOR, anchor="w")
        
        # Command history
        self.canvas.create_text(left_x + 15, top_y + 290,
                               text="RECENT COMMANDS",
                               font=("Arial", 10, "bold"),
                               fill=PRIMARY_COLOR, anchor="w")
        
        self.history_display = self.canvas.create_text(left_x + 15, top_y + 350,
                                                       text="No commands yet",
                                                       font=("Arial", 8),
                                                       fill=TEXT_COLOR, anchor="nw", width=260)
    
    def _draw_center_panel(self):
        """Draw center panel with main JARVIS interface"""
        center_x = 310
        top_y = 70
        panel_width = 780
        panel_height = WINDOW_HEIGHT - 80
        center_panel_x = center_x + panel_width // 2
        center_panel_y = top_y + panel_height // 2
        
        # Panel border
        self.canvas.create_rectangle(center_x, top_y, center_x + panel_width, top_y + panel_height,
                                     fill=PANEL_COLOR, outline=SECONDARY_COLOR, width=2)
        
        # Title
        self.canvas.create_text(center_panel_x, top_y + 20,
                               text="MAIN INTERFACE",
                               font=("Arial", 12, "bold"),
                               fill=SECONDARY_COLOR)
        
        # Draw circular scanner
        radius = 100
        # Outer circle
        self.canvas.create_oval(center_panel_x - radius, center_panel_y - radius,
                               center_panel_x + radius, center_panel_y + radius,
                               outline=SECONDARY_COLOR, width=3)
        
        # Inner circles
        for r in [70, 50, 30]:
            self.canvas.create_oval(center_panel_x - r, center_panel_y - r,
                                    center_panel_x + r, center_panel_y + r,
                                    outline=PRIMARY_COLOR, width=1.5, stipple="gray25")
        
        # Center dot
        self.center_dot = self.canvas.create_oval(center_panel_x - 5, center_panel_y - 5,
                                                 center_panel_x + 5, center_panel_y + 5,
                                                 fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=2)
        
        # Scanning dot animation
        self.scanner_dot = self.canvas.create_oval(center_panel_x - 8, center_panel_y - 100 - 8,
                                                  center_panel_x + 8, center_panel_y - 100 + 8,
                                                  fill=PRIMARY_COLOR, outline=SECONDARY_COLOR, width=2)
        
        # Crosshair
        self.canvas.create_line(center_panel_x - 20, center_panel_y, center_panel_x - 10, center_panel_y,
                               fill=PRIMARY_COLOR, width=2)
        self.canvas.create_line(center_panel_x + 10, center_panel_y, center_panel_x + 20, center_panel_y,
                               fill=PRIMARY_COLOR, width=2)
        self.canvas.create_line(center_panel_x, center_panel_y - 20, center_panel_x, center_panel_y - 10,
                               fill=PRIMARY_COLOR, width=2)
        self.canvas.create_line(center_panel_x, center_panel_y + 10, center_panel_x, center_panel_y + 20,
                               fill=PRIMARY_COLOR, width=2)
        
        # Status text
        self.main_status = self.canvas.create_text(center_panel_x, center_panel_y + 150,
                                                   text="SYSTEM READY",
                                                   font=("Arial", 14, "bold"),
                                                   fill=SECONDARY_COLOR)
        
        # Command input area
        self.canvas.create_text(center_x + 20, top_y + 320,
                               text="INPUT COMMAND:",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.command_box = self.canvas.create_rectangle(center_x + 20, top_y + 340,
                                                       center_x + panel_width - 20, top_y + 380,
                                                       fill="#0A0E27", outline=PRIMARY_COLOR, width=2)
        
        self.command_text = self.canvas.create_text(center_x + 30, top_y + 360,
                                                    text="> Enter command here",
                                                    font=("Arial", 10),
                                                    fill=TEXT_COLOR, anchor="w")
        
        # Store center coordinates for later use
        self.center_panel_coords = (center_panel_x, center_panel_y, radius)
    
    def _draw_right_panel(self):
        """Draw right panel with system info and diagnostics"""
        right_x = WINDOW_WIDTH - 290
        top_y = 70
        panel_width = 280
        panel_height = WINDOW_HEIGHT - 80
        
        # Panel border
        self.canvas.create_rectangle(right_x, top_y, right_x + panel_width, top_y + panel_height,
                                     fill=PANEL_COLOR, outline=ACCENT_COLOR, width=2)
        
        # Title
        self.canvas.create_text(right_x + 140, top_y + 20,
                               text="DIAGNOSTICS",
                               font=("Arial", 12, "bold"),
                               fill=ACCENT_COLOR)
        
        # System info
        self.system_info = self.canvas.create_text(right_x + 15, top_y + 60,
                                                   text="System: Online\nVersion: 2.1.0\nUptime: 00:00:00",
                                                   font=("Arial", 9),
                                                   fill=TEXT_COLOR, anchor="nw")
        
        # Temperature
        self.canvas.create_text(right_x + 15, top_y + 150,
                               text="TEMPERATURE",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.temp_bar = self.canvas.create_rectangle(right_x + 15, top_y + 170, right_x + 260, top_y + 185,
                                                    fill=BORDER_COLOR, outline=ACCENT_COLOR, width=1)
        self.temp_value = self.canvas.create_text(right_x + 200, top_y + 177,
                                                 text="45°C",
                                                 font=("Arial", 9, "bold"),
                                                 fill=ACCENT_COLOR)
        
        # Storage
        self.canvas.create_text(right_x + 15, top_y + 220,
                               text="STORAGE",
                               font=("Arial", 10, "bold"),
                               fill=TEXT_COLOR, anchor="w")
        
        self.storage_bar = self.canvas.create_rectangle(right_x + 15, top_y + 240, right_x + 260, top_y + 255,
                                                       fill=BORDER_COLOR, outline=ACCENT_COLOR, width=1)
        self.storage_value = self.canvas.create_text(right_x + 200, top_y + 247,
                                                    text="0%",
                                                    font=("Arial", 9, "bold"),
                                                    fill=ACCENT_COLOR)
        
        # Activity log
        self.canvas.create_text(right_x + 15, top_y + 300,
                               text="ACTIVITY LOG",
                               font=("Arial", 10, "bold"),
                               fill=ACCENT_COLOR, anchor="w")
        
        self.activity_log = self.canvas.create_text(right_x + 15, top_y + 340,
                                                    text="System initialized\nListening for commands",
                                                    font=("Arial", 8),
                                                    fill=TEXT_COLOR, anchor="nw", width=260)
    
    def _animate(self):
        """Main animation loop"""
        # Update scanner dot position
        if hasattr(self, 'center_panel_coords'):
            center_x, center_y, radius = self.center_panel_coords
            rad = math.radians(self.current_angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            
            self.canvas.coords(self.scanner_dot, x - 8, y - 8, x + 8, y + 8)
            self.current_angle = (self.current_angle + 2) % 360
        
        # Update scan line position
        y_pos = (int(time.time() * 100) % WINDOW_HEIGHT)
        self.canvas.coords(self.scan_line, 0, y_pos, WINDOW_WIDTH, y_pos)
        
        # Update pulse effect on center dot
        pulse_size = 5 + 3 * math.sin(time.time() * 3)
        if hasattr(self, 'center_panel_coords'):
            center_x, center_y, _ = self.center_panel_coords
            self.canvas.coords(self.center_dot, 
                              center_x - pulse_size, center_y - pulse_size,
                              center_x + pulse_size, center_y + pulse_size)
        
        # Update time
        current_time = datetime.now().strftime("%H:%M:%S")
        self.canvas.itemconfig(self.time_text, text=current_time)
        
        # Continue animation
        self.root.after(50, self._animate)
    
    def _update_stats(self):
        """Update system statistics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_width = int((cpu_percent / 100) * 245)
            self.canvas.itemconfig(self.cpu_value, text=f"{cpu_percent:.0f}%")
            
            # Memory usage
            memory = psutil.virtual_memory()
            mem_width = int((memory.percent / 100) * 245)
            self.canvas.itemconfig(self.mem_value, text=f"{memory.percent:.0f}%")
            
            # Storage usage
            disk = psutil.disk_usage('/')
            disk_width = int((disk.percent / 100) * 245)
            self.canvas.itemconfig(self.storage_value, text=f"{disk.percent:.0f}%")
        
        except Exception as e:
            print(f"[Stats] Error updating stats: {e}")
        
        # Update stats every 2 seconds
        self.root.after(2000, self._update_stats)
    
    def update_command(self, command_text):
        """Update command display"""
        self.canvas.itemconfig(self.command_text, text=f"> {command_text}")
        self.command_history.append(command_text)
        
        # Update history display
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
