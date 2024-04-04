import customtkinter as ctk
from coreai import Footwork
from PIL import ImageTk, Image
import threading

# Thiết lập giao diện
ctk.set_appearance_mode("dark")  # Chế độ: system (mặc định), light, dark
ctk.set_default_color_theme("dark-blue")  # Chủ đề: blue (mặc định), dark-blue, green

app = ctk.CTk()
app.geometry("1080x680")
app.resizable(False, False)
app.iconbitmap(r"imgs\icon.ico")
app.title('Chouwzi BAF')

# Lớp Setting quản lý các thiết lập
class Setting():
    def __init__(self, mode, data, interval, voice, repeat):
        self.modes = ['random', 'data']
        self.mode = mode
        self.data = data
        self.interval = interval
        self.voice = voice
        self.repeat = repeat
    # Cập nhật chế độ
    def up_mode(self, value):
        self.mode = value
        if value == 'data':
            repeat_label.configure(text_color='#50F7A3')
            repeat_check.place(x=125, y=170)
            data_label.configure(text_color='#50F7A3')
            data_entry.place(x=125, y=130)
        else:
            repeat_check.place(x=9999, y =9999)
            data_entry.place(x=9999, y =9999)
            data_label.configure(text_color='#212121')
            repeat_label.configure(text_color='#212121')
            
    # Cập nhật dữ liệu
    def up_data(self):
        if self.mode == "data":
            
            data_split = data_entry.get().split(',')
            self.data = [int(x) for x in data_split]
            
            
    # Cập nhật khoảng dừng
    def up_interval(self):
        self.interval = int(interval_entry.get())
    
    # Cập nhật giọng nói
    def up_voice(self):
        self.voice = voice_var.get()
    
    # Cập nhật lặp lại
    def up_repeat(self):
        self.repeat = repeat_var.get()
    
# Khởi tạo đối tượng Setting với các thiết lập mặc định
setting = Setting('random', '', 3, True, False)
side_panel_width = 250

# Lớp Start quản lý việc bắt đầu và dừng chương trình
class Start(Setting):
    def __init__(self):
        self.start = False
        self.button = None
        self.fw = Footwork(app, setting.mode, setting.interval, setting.voice, setting.data, setting.repeat)
        self.create()
        
    # Tạo nút bắt đầu
    def create(self):
        self.button = ctk.CTkButton(master=app, 
                        text="Bắt đầu",
                        font=("Helvetica", 22, 'bold'),
                        width=side_panel_width,
                        height=65,
                        fg_color="#50F7A3",
                        hover_color="#72FFB8",
                        text_color="black",
                        command=self.start_func
                        )
        self.button.place(relx=0.99, rely=0.99, anchor=ctk.E, y=-320)
        
    # Hành động khi bấm nút bắt đầu
    def start_func(self):
        setting.up_data()
        setting.up_interval()
        self.fw.mode = setting.mode
        self.fw.interval = setting.interval
        self.fw.data = setting.data
        self.fw.voice = setting.voice
        self.fw.repeat = setting.repeat
        print(f'--Settings--\nMode: {setting.mode}\nData: {setting.data}\nInterval: {setting.interval}\nVoice: {setting.voice}\nStart: {self.start}')
        if setting.mode == 'random':
            if not self.start:
                self.button.configure(text="Dừng lại")
                self.fw.practice(points, self)
            else:
                self.button.configure(text="Bắt đầu") 
                threading.Thread(target=self.fw.stop_random_mode, args=()).start()
        elif setting.mode == 'data':
            if not self.start:
                self.button.configure(text="Dừng lại")
                self.fw.practice(points, self)
                
        self.start = not self.start

# Lớp Point đại diện cho các điểm
class Point():
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self.text = text
        self.point = None
        self.disabled = False
        self.create()
        
    # Tạo điểm
    def create(self):
        self.point = ctk.CTkButton(master=app, 
                        text= self.text,
                        font=("Helvetica", 22, 'bold'),
                        width=50,
                        height=50,
                        fg_color="white",
                        bg_color="#107b43",
                        hover_color="#DCDCDC",
                        text_color="black",
                        command=self.onclick
                        )
        self.point.place(x=self.x, y = self.y)
    
    # Đánh dấu điểm
    def highlight(self, boolean):
        if boolean:
            self.point.configure(fg_color='#00E3FF')
        elif self.disabled:
            self.point.configure(fg_color="#FF2B00", hover_color="#FF6242", text='X')
        else:
            self.point.configure(fg_color="white", hover_color="#DCDCDC", text=self.text)
            
    # Xử lý sự kiện khi bấm vào điểm
    def onclick(self):
        if setting.mode == 'random':
            if not self.disabled:
                self.point.configure(fg_color="#FF2B00", hover_color="#FF6242", text='X')
            else:
                self.point.configure(fg_color="white", hover_color="#DCDCDC", text=self.text)
            self.disabled = not self.disabled

# Load ảnh từ file
image = Image.open(r"Software Projects\Making\badminton_advanced_footwork\imgs\badminton-court.jpg")

# Resize ảnh
resized_image = image.resize((1000, 850), Image.ANTIALIAS)

# Chuyển đổi ảnh thành đối tượng ImageTk
image = ImageTk.PhotoImage(resized_image)

# Tạo một label để hiển thị ảnh
image_label = ctk.CTkLabel(app, text="", image=image)
image_label.pack(side=ctk.TOP, anchor=ctk.W, padx=10, pady=10)

# Khởi tạo các điểm
points = [
    Point("1", 140, 70), 
    Point("2", 385, 70), 
    Point("3", 630, 70), 
    Point("4", 140, 310), 
    Point("5", 630, 310), 
    Point("6", 140, 575), 
    Point("7", 385, 575),
    Point("8", 630, 575)
]

# Tạo giao diện chọn thiết lập
custom_frame = ctk.CTkFrame(app, 
                            width=side_panel_width, 
                            height=300,
                            corner_radius=10
                            )
custom_frame.place(relx=1, rely=0, anchor=ctk.NE, x=-10, y=10) 

mode_label = ctk.CTkLabel(custom_frame, text='Chế độ', text_color='#50F7A3', font=("Helvetica", 15, 'bold'))
mode_label.place(x=10, y=10)
mode_combobox = ctk.CTkComboBox(custom_frame, values=setting.modes, width=116, command=setting.up_mode)
mode_combobox.place(x=125, y=10)

interval_label = ctk.CTkLabel(custom_frame, text='Khoảng dừng', text_color='#50F7A3', font=("Helvetica", 15, 'bold'))
interval_label.place(x=10, y=50)
interval_entry = ctk.CTkEntry(custom_frame, placeholder_text='3', width=116)
interval_entry.place(x=125, y=50)
interval_entry.insert(0, str(setting.interval))

voice_label = ctk.CTkLabel(custom_frame, text='Giọng nói', text_color='#50F7A3', font=("Helvetica", 15, 'bold'))
voice_label.place(x=10, y=90)
voice_var = ctk.BooleanVar(custom_frame, True)
voice_check = ctk.CTkCheckBox(custom_frame, variable=voice_var, onvalue=True, text='', checkmark_color='black', fg_color='#50F7A3', command=setting.up_voice)
voice_check.place(x=125, y=90)

data_label = ctk.CTkLabel(custom_frame, text='Bước', text_color='#212121', font=("Helvetica", 15, 'bold'))
data_label.place(x=10, y=130)
data_entry = ctk.CTkEntry(custom_frame, placeholder_text='VD: 1,3,5,2,4,8', width=116)
data_entry.place(x=9999, y=9999)

repeat_label = ctk.CTkLabel(custom_frame, text='Lặp lại', text_color='#212121', font=("Helvetica", 15, 'bold'))
repeat_label.place(x=10, y=170)
repeat_var = ctk.BooleanVar(custom_frame, False)
repeat_check = ctk.CTkCheckBox(custom_frame, variable=repeat_var, onvalue=True, text='', checkmark_color='black', fg_color='#50F7A3', command=setting.up_repeat)
repeat_check.place(x=9999, y=9999)

copyright_label = ctk.CTkLabel(app, text="© 2024 BAF. All rights reserved.", text_color='white', font=("Helvetica", 13))
copyright_label.place(relx=0.99, rely=0.99, anchor=ctk.E, y=-10)
# Khởi tạo và hiển thị nút bắt đầu
start_btn = Start()

app.mainloop()