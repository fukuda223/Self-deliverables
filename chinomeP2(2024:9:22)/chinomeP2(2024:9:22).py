import tkinter as tk
from PIL import Image, ImageTk
import time
import datetime
import math

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock")
        self.SIDE = 400
        self.CENTER = self.SIDE / 2
        self.canvas = tk.Canvas(root, width=self.SIDE, height=self.SIDE)
        self.canvas.pack()
        
        self.create_clock_face()
        self.create_hands()
        
        self.mode = 'clock'
        self.timer_running = False
        self.count = 0
        self.counter = 0
        self.v = 0
        self.timer_text_id = None  #タイマー用テキストのID
        self.digital_clock_text_id = None  # デジタル時計のテキストID
        self.date_text_id = None  #  日付のテキストID
        self.show_timer = None  # タイマーを表示するかどうか
        self.show_digital_clock = None  # デジタル時計を表示するかどうか
        self.show_date = None  # 日付を表示するかどうか
        self.lv1_text_id = None
        self.lv2_text_id = None

        self.update_time()
        self.root.bind("<Key>", self.key_pressed)

    def create_clock_face(self):
        self.clock_face = self.canvas.create_oval(0, 0, self.SIDE, self.SIDE, fill="#87CEEB")
        #self.clock_face = self.canvas.create_oval(0, 0, self.SIDE, self.SIDE, fill="#FFFE3B")
        for i in range(60):
            angle = math.radians(6 * i - 90)
            distance = self.CENTER * (0.925 if i % 5 else 0.825)
            start_x = distance * math.cos(angle) + self.CENTER
            start_y = distance * math.sin(angle) + self.CENTER
            end_x = (self.CENTER * 0.975) * math.cos(angle) + self.CENTER
            end_y = (self.CENTER * 0.975) * math.sin(angle) + self.CENTER
            line_width = self.CENTER * (0.04 if i % 15 == 0 else 0.02 if i % 5 == 0 else 0.01)
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=line_width, fill="#000000")

    def create_hands(self):
        self.hour_hand = self.canvas.create_line(0, 0, 0, 0, fill="#880000", width=self.CENTER * 0.04)
        self.minute_hand = self.canvas.create_line(0, 0, 0, 0, fill="#880000", width=self.CENTER * 0.02)
        self.second_hand = self.canvas.create_line(0, 0, 0, 0, fill="red", width=self.CENTER * 0.01)

    def get_current_time(self):
        current_time = time.localtime()
        return current_time.tm_hour, current_time.tm_min, current_time.tm_sec

    def get_current_date(self):
        return datetime.date.today().strftime("%Y-%m-%d")

    def update_time(self):
        h, m, s = self.get_current_time()
        self.update_hands(h, m, s)
        self.update_digital_clock(h, m, s)
        if self.show_date:
            self.update_date()  # 日付を更新
        self.root.after(1000, self.update_time)
        
    def update_hands(self, h, m, s):
        hour_angle = math.radians((h % 12) * 30 + (m / 60) * 30 - 90)
        minute_angle = math.radians(m * 6 + (s / 60) * 6 - 90)
        second_angle = math.radians(s * 6 - 90)

        hour_length = self.CENTER * 0.6
        minute_length = self.CENTER * 0.9
        second_length = self.CENTER * 0.9

        self.canvas.coords(self.hour_hand, self.CENTER, self.CENTER, 
                           hour_length * math.cos(hour_angle) + self.CENTER, 
                           hour_length * math.sin(hour_angle) + self.CENTER)

        self.canvas.coords(self.minute_hand, self.CENTER, self.CENTER, 
                           minute_length * math.cos(minute_angle) + self.CENTER, 
                           minute_length * math.sin(minute_angle) + self.CENTER)

        self.canvas.coords(self.second_hand, self.CENTER, self.CENTER, 
                           second_length * math.cos(second_angle) + self.CENTER, 
                           second_length * math.sin(second_angle) + self.CENTER)

    def key_pressed(self, event):
        if event.char == '2':
            self.mode = 'timer'
            self.start_timer()
            self.counter += 1
            self.date2()
        elif event.char == '3':
            self.mode = 'stopwatch'
        elif event.char == '4':
            self.mode = 'date'
            self.update_date()
        elif event.char == '5':
            if event.char.lower() == '5':  
                self.show_date = not self.show_date  # 日付の表示を切り替え
                self.show_digital_clock = not self.show_digital_clock
                self.show_timer = not self.show_timer
                if self.date_text_id is not None:
                    self.canvas.delete(self.date_text_id)  # 日付を削除
                    self.date_text_id = None  # IDをリセット
                if self.show_date:
                    self.update_date()  # 日付を再表示

                #if self.digital_clock_text_id is not None:
                    #self.canvas.delete(self.digital_clock_text_id)  
                    #self.digital_clock_text_id = None  # IDをリセット
                #if self.show_digital_clock:
                    #self.update_digital_clock()  # デジタル時計を再表示

    def update_digital_clock(self, h, m, s):
        # 既存のデジタル時計を削除
        if self.digital_clock_text_id is not None:
            self.canvas.delete(self.digital_clock_text_id)
        
        # デジタル時計のテキストを描画
        self.digital_clock_text_id = self.canvas.create_text(200, 130, 
            text=f"{h:02}:{m:02}:{s:02}", font=("Arial", 30), fill="#000000")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.count = 50  # Set your desired timer duration
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            if self.timer_text_id is not None:
                self.canvas.delete(self.timer_text_id)

            if self.count > 0:
                self.timer_text_id = self.canvas.create_text(200, 250, text=f"Timer: {self.count}", font=("Arial", 30), fill="#000000")
                self.count -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.timer_text_id = None  # タイマーが終了したらIDをリセット
                #if self.count == 0:

    def update_date(self):
        date_str = self.get_current_date()
        # 既存の日付を削除
        if self.date_text_id is not None:
            self.canvas.delete(self.date_text_id)
        
        # 日付のテキストを描画
        self.date_text_id = self.canvas.create_text(200, 250, text=date_str, font=("Arial", 30), fill="#000000")

    def date2():
        self.lv1_text_id = self.canvas.create_text(200, 250, text=counter, font=("Arial", 30), fill="#000000")
        self.lv2_text_id = self.canvas.create_text(220, 250, text="Lv", font=("Arial", 30), fill="#000000")
# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()
