# Badminton Advanced Footwork (BAF)
# Version 1.1

# Thư viện
import time
import random
import threading
import customtkinter as ctk
from module import speech, delete_files_in_directory

# Danh sách các góc trên sân
corners = {
    1: 'Trên trái', 2: 'Trên giữa', 3: 'Trên phải',
    4: 'Giữa trái', 5: 'Giữa phải', 6: 'Dưới trái',
    7: 'Dưới giữa', 8: 'Dưới phải'
}

# Lớp Footwork quản lý các chức năng chính của chương trình
class Footwork():
    def __init__(self, app, mode, interval, voice, data, repeat, log_enabled=True):
        self.app = app
        self.mode = mode
        self.data = data
        self.interval = interval
        self.voice = voice
        self.repeat = repeat
        self.stop_event = False
        self.log_enabled = log_enabled

    # Chế độ ngẫu nhiên
    def random_mode(self, corner_points):
        # Tạo danh sách góc có thể chọn dựa trên các góc chưa bị vô hiệu hóa
        corner_list = [corner for corner in corner_points if not corner.disabled]
        while not self.stop_event:  
            # Chọn một góc ngẫu nhiên từ danh sách và phát âm góc đó
            corner_ran = random.choice(corner_list)
            corner = corners[int(corner_ran.text)]
            corner_ran.highlight(True)  # Đánh dấu góc đã chọn
            if self.log_enabled:
                print(f"Selected corner: {corner}")  # In ra log góc đã chọn
            speech(corner, self.voice)  # Phát âm góc
            time.sleep(self.interval)   # Dừng trong một khoảng thời gian
            corner_ran.highlight(False)  # Xóa đánh dấu sau khi đã phát âm
        self.stop_event = False
        
    # Chế độ dữ liệu
    def data_mode(self, corner_points):
        # Tạo danh sách góc từ dữ liệu đã cho
        corner_list = [corner_point for corner in self.data for corner_point in corner_points if corner_point.text == str(corner)]
        if self.repeat:
            while not self.stop_event: 
                # Lặp lại việc phát âm cho mỗi góc trong danh sách
                for corner in corner_list:
                    if self.stop_event: break
                    corner.highlight(True)  # Đánh dấu góc đã chọn
                    if self.log_enabled:
                        print(f"Selected corner: {corners[int(corner.text)]}")  # In ra log góc đã chọn
                    speech(corners[int(corner.text)], self.voice)  # Phát âm góc
                    time.sleep(self.interval)  # Dừng trong một khoảng thời gian
                    corner.highlight(False)  # Xóa đánh dấu sau khi đã hết thời gian
                    if self.stop_event: break
        else:
            for corner in corner_list:
                if self.stop_event: break
                corner.highlight(True)  # Đánh dấu góc đã chọn
                if self.log_enabled:
                    print(f"Selected corner: {corners[int(corner.text)]}")  # In ra log góc đã chọn
                speech(corners[int(corner.text)], self.voice)  # Phát âm góc
                time.sleep(self.interval)  # Dừng trong một khoảng thời gian
                corner.highlight(False)  # Xóa đánh dấu sau khi đã hết thời gian
                if self.stop_event: break
        self.start_button.configure(text="Bắt đầu")
        self.stop_event = False
        
    # Bắt đầu thực hành
    def practice(self, corner_points, start):
        if self.log_enabled:
            print(f"Selected practice mode: {self.mode}")  # In ra log chế độ thực hành được chọn
        if self.mode == 'random':
            # Bắt đầu chế độ ngẫu nhiên bằng cách tạo một luồng mới
            self.ran_mode = threading.Thread(target=self.random_mode, args=(corner_points,))
            self.ran_mode.start()            
        elif self.mode == 'data':
            if self.data is not None:
                self.start_button = start.button
                # Bắt đầu chế độ dữ liệu bằng cách tạo một luồng mới
                data_mode = threading.Thread(target=self.data_mode, args=(corner_points, ))
                data_mode.start()
            else:
                print('Data not found, please import data!')
        else:
            print('Practice mode not found (random, data)')
        print('Footwork practice done.')
        delete_files_in_directory(r"temp")  # Xóa các tệp tạm sau khi thực hành
    
    # Dừng chế độ ngẫu nhiên
    def stop_random_mode(self):
        self.stop_event = True  # Đặt sự kiện để dừng luồng chế độ ngẫu nhiên
