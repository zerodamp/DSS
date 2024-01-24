import base64
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

def base64_to_video(base64_str, output_path='output_video.mp4'):
    # Base64 kodunu çöz
    video_data = base64.b64decode(base64_str)

    # Çözülen veriyi bir video dosyasına yaz
    with open(output_path, 'wb') as video_file:
        video_file.write(video_data)

def read_base64_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def play_video():
    # Dosya seçme penceresi
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])

    if not file_path:
        return

    # Base64 kodunu oku
    base64_str = read_base64_from_file(file_path)

    # Base64 kodunu videoya çevir
    base64_to_video(base64_str)

    # Videoyu aç
    cap = cv2.VideoCapture('output_video.mp4', cv2.CAP_FFMPEG)
    if not cap.isOpened():
        result_label.config(text="Video oynatma hatası!")
        return

    # Video boyutlarını al
    width = cap.get(3)
    height = cap.get(4)

    # Tkinter penceresi oluştur
    video_window = tk.Toplevel(app)
    video_window.title("Oynatılan Video")

    # ThemedStyle ile modern temayı uygula
    style = ThemedStyle(video_window)
    style.set_theme("radiance")

    # Canvas oluştur
    canvas = tk.Canvas(video_window, width=width, height=height, bg="black")
    canvas.pack()

    # "Made by zerodamp" etiketi
    label = ttk.Label(video_window, text="Made by zerodamp", foreground="white", font=("Helvetica", 10))
    label.pack(side="bottom", pady=10)

    # Videoyu oynat
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # OpenCV görüntüyü PIL formatına dönüştür
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Video boyutlarına göre boyutlandır
        image = image.resize((int(width), int(height)), Image.LANCZOS)

        # PIL formatındaki görüntüyü Tkinter Canvas'a ekle
        photo = ImageTk.PhotoImage(image=image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.update()

        # Küçük bir bekleme süresi ekleyerek videoyu daha yavaş oynat
        video_window.after(30)

    # Video oynatımını durdur
    cap.release()

# Tkinter penceresi oluştur
app = tk.Tk()
app.title("Base64 to Video Converter")

# ThemedStyle ile modern temayı uygula
style = ThemedStyle(app)
style.set_theme("radiance")

# Dosya seçme butonu
select_file_button = ttk.Button(app, text="Dosya Seç", command=play_video)
select_file_button.pack(pady=20)

# Sonuç etiketi
result_label = ttk.Label(app, text="")
result_label.pack(pady=20)

# Uygulamayı başlat
app.mainloop()
