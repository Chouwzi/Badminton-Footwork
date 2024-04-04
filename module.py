#ffmpeg-python
from gtts import gTTS 
import playsound
import os
from random import randint

def speech(text: str, voice: bool):
    if voice: 
        output = gTTS(text=text, lang='vi', slow=False)
        id = randint(1000000, 9999999)
        output.save(f"temp\\voice{id}.mp3")
        playsound.playsound(os.path.normpath(f"temp\\voice{id}.mp3"))
        os.remove(f"temp\\voice{id}.mp3")


def delete_files_in_directory(directory):
    # Kiểm tra xem thư mục tồn tại không
    if os.path.exists(directory):
        # Duyệt qua tất cả các tệp trong thư mục và xóa chúng
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    print(f"Đã xóa tệp: {filepath}")
                else:
                    print(f"{filepath} không phải là tệp.")
            except Exception as e:
                print(f"Lỗi: {e}")
    else:
        print(f"Thư mục '{directory}' không tồn tại.")