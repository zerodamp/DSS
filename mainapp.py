import base64
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import os
import math
from ttkthemes import ThemedStyle
import subprocess

def base64_to_video(base64_str, output_path='output_video.mp4'):
    # Base64 kodunu çöz
    video_data = base64.b64decode(base64_str)

    # Çözülen veriyi bir video dosyasına yaz
    with open(output_path, 'wb') as video_file:
        video_file.write(video_data)

def read_base64_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def split_base64(base64_str, chunk_size_mb):
    # Base64 verisini parçalara böl
    chunk_size_bytes = int(chunk_size_mb * 1024 * 1024)
    total_chunks = math.ceil(len(base64_str) / chunk_size_bytes)
    
    chunks = [base64_str[i:i+chunk_size_bytes] for i in range(0, len(base64_str), chunk_size_bytes)]

    return chunks, total_chunks

def base64_to_image(base64_str, output_path='output_image.png'):
    try:
        # Base64 kodunu çöz
        image_data = base64.b64decode(base64_str)

        # Çözülen veriyi bir resim dosyasına yaz
        with open(output_path, 'wb') as image_file:
            image_file.write(image_data)

        return True
    except Exception as e:
        print(f"Hata: {e}")
        return False

def video_to_base64():
    # Dosya seçme penceresi
    file_path = filedialog.askopenfilename(filetypes=[('MP4 Files', '*.mp4')])
    
    if not file_path:
        return

    # Videoyu oku
    with open(file_path, 'rb') as video_file:
        # Video dosyasını base64 formatına dönüştür
        video_base64 = base64.b64encode(video_file.read()).decode()

        # Soru sor
        answer = messagebox.askquestion("Parçalama", "Base64 verisini parçalara bölmek ister misiniz?")

        if answer == "yes":
            # Boyut kutusu oluştur
            chunk_size_mb = simpledialog.askfloat("Boyut", "Her parça kaç MB olsun?")
            
            if not chunk_size_mb:
                return

            # Base64 verisini parçalara böl
            chunks, total_chunks = split_base64(video_base64, chunk_size_mb)

            # Parçalara ait MB değerini görüntüle ve kaydet
            for i, chunk in enumerate(chunks, start=1):
                with open(f'base64_part_{i}.txt', 'w') as output:
                    output.write(chunk)
                print(f"Parça {i} MB: {len(chunk) / 1024 / 1024:.2f} MB")

            result_label.config(text=f"{total_chunks} parçaya bölündü. Parçalar base64_part_1.txt, base64_part_2.txt, ... olarak kaydedildi.")
        else:
            # Parçalanmamış base64 verisini bir dosyaya yaz
            with open('base64.txt', 'w') as output:
                output.write(video_base64)

            result_label.config(text="Base64 verisi base64.txt olarak kaydedildi.")

def play_base64_video():
    # Dosya seçme penceresi
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    
    if not file_path:
        return

    # Base64 kodunu oku
    with open(file_path, 'r') as file:
        base64_str = file.read()

    # Base64 kodunu videoya çevir
    base64_to_video(base64_str)
    
    # Videoyu aç
    os.system('start output_video.mp4')

    result_label.config(text="Video başarıyla oynatıldı.")

def combine_base64():
    # Dosya seçme penceresi
    file_paths = filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt')])

    if not file_paths:
        result_label.config(text="Dosya seçilmedi.")
        return

    # Seçilen tüm dosyaların içeriğini birleştir
    combined_base64 = ""
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            combined_base64 += file.read()

    # Birleştirilmiş base64 verisini bir dosyaya yaz
    with open('combined_base64.txt', 'w') as output:
        output.write(combined_base64)

    result_label.config(text="Tüm base64 verileri combined_base64.txt olarak birleştirildi.")

def photo_to_base64():
    # Dosya seçme penceresi
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif')])

    if not file_path:
        return

    # Fotoğrafı oku
    with open(file_path, 'rb') as image_file:
        # Fotoğraf dosyasını base64 formatına dönüştür
        image_base64 = base64.b64encode(image_file.read()).decode()

        # Base64 verisini bir dosyaya yaz
        with open('base64_photo.txt', 'w') as output:
            output.write(image_base64)

        result_label.config(text="Fotoğraf başarıyla base64 formatına dönüştürüldü ve base64_photo.txt olarak kaydedildi.")

def base64_to_photo():
    # Dosya seçme penceresi
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    
    if not file_path:
        return

    # Base64 kodunu oku
    base64_str = read_base64_from_file(file_path)

    # Base64 kodunu fotoğrafa çevir
    success = base64_to_image(base64_str, 'output_image.png')

    if success:
        result_label.config(text="Base64 verisi başarıyla fotoğrafa çevrildi ve output_image.png olarak kaydedildi.")
        
        # Kaydedilen fotoğrafı aç
        subprocess.run(['start', 'output_image.png'], shell=True)
    else:
        result_label.config(text="Hata: Base64 verisi fotoğrafa çevrilemedi.")

# Tkinter penceresi oluştur
app = tk.Tk()
app.title("Media to Base64 and Play")

# ThemedStyle ile modern temayı uygula
style = ThemedStyle(app)
style.set_theme("radiance")

# Dosya seçme butonları
select_file_button_1 = tk.Button(app, text="Video to Base64", command=video_to_base64, bg="black", fg="white", relief="raised")
select_file_button_1.pack(pady=20)

select_file_button_2 = tk.Button(app, text="Base64 to Video", command=play_base64_video, bg="black", fg="white", relief="raised")
select_file_button_2.pack(pady=20)

select_file_button_3 = tk.Button(app, text="Combine Base64", command=combine_base64, bg="black", fg="white", relief="raised")
select_file_button_3.pack(pady=20)

select_file_button_4 = tk.Button(app, text="Photo to Base64", command=photo_to_base64, bg="black", fg="white", relief="raised")
select_file_button_4.pack(pady=20)

select_file_button_5 = tk.Button(app, text="Base64 to Photo", command=base64_to_photo, bg="black", fg="white", relief="raised")
select_file_button_5.pack(pady=20)

# GitHub sayfasını açan buton
def open_github():
    import webbrowser
    webbrowser.open("https://github.com/zerodamp/dss-v1")

github_button = tk.Button(app, text="View GitHub Page", command=open_github, bg="black", fg="white", relief="raised")
github_button.pack(pady=20)

# Sonuç etiketi
result_label = tk.Label(app, text="", font=("Helvetica", 12))
result_label.pack(pady=20)

# Uygulamayı başlat
app.mainloop()
