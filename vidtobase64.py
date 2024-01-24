import base64
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

def video_to_base64():
    try:
        # Dosya seçme penceresi
        file_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4')])
        
        if not file_path:
            result_label.config(text="Video seçilmedi.")
            return

        # Videoyu oku
        with open(file_path, 'rb') as video_file:
            # Video dosyasını base64 formatına dönüştür
            video_base64 = base64.b64encode(video_file.read())

            # Base64 verisini bir dosyaya yaz
            with open('base64.txt', 'wb') as output:
                output.write(video_base64)

            result_label.config(text="Video başarıyla base64 formatına dönüştürüldü ve base64.txt olarak kaydedildi.")
    except Exception as e:
        result_label.config(text=f"Hata: {str(e)}")

def play_base64_video():
    # Base64 kodunu oku
    with open('base64.txt', 'r') as file:
        base64_str = file.read()

    # Base64 kodunu videoya çevir
    video_data = base64.b64decode(base64_str)
    
    # Videoyu geçici bir dosyaya yaz
    with open('played_video.mp4', 'wb') as temp_video:
        temp_video.write(video_data)

    # Videoyu aç
    cap = cv2.VideoCapture('played_video.mp4', cv2.CAP_FFMPEG)
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
app.title("Video to Base64 and Play")

# ThemedStyle ile modern temayı uygula
style = ThemedStyle(app)
style.set_theme("radiance")

# Dosya seçme butonu
select_file_button = ttk.Button(app, text="Video Seç", command=video_to_base64)
select_file_button.pack(pady=20)

# Base64 kodunu oynatma butonu
play_button = ttk.Button(app, text="Base64 Kodunu Oynat", command=play_base64_video)
play_button.pack(pady=20)

# Sonuç etiketi
result_label = ttk.Label(app, text="")
result_label.pack(pady=20)

# Uygulamayı başlat
app.mainloop()
