import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import uuid

# Fungsi untuk memilih file gambar
def pilih_gambar():
    root = tk.Tk()
    root.withdraw()  # Sembunyikan jendela utama tkinter
    file_path = filedialog.askopenfilename(
        title="Pilih Gambar",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return file_path

# Fungsi untuk colorize gambar
def colorize_image(image_path):
    # Load model colorization
    prototxt = "model/colorization_deploy_v2.prototxt"
    model = "model/colorization_release_v2.caffemodel"
    points = "model/pts_in_hull.npy"

    # Load model
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    pts = np.load(points)

    # Add centers to the model
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    # Load gambar hitam putih
    image = cv2.imread(image_path)
    if image is None:
        print("Gagal memuat gambar. Pastikan path file benar.")
        return

    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Resize gambar
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Colorize gambar
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    # Tampilkan hasil
    cv2.imshow("Original", image)
    cv2.imshow("Colorized", colorized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Simpan hasil dengan nama acak
    if not os.path.exists("images"):
        os.makedirs("images")  # Buat folder images jika belum ada

    nama_acak = str(uuid.uuid4()) + ".jpg"  # Generate nama acak
    output_path = os.path.join("images", nama_acak)
    cv2.imwrite(output_path, colorized)
    print(f"Gambar berhasil di-colorize dan disimpan sebagai {output_path}")

# Main program
if __name__ == "__main__":
    # Pilih file gambar
    gambar_path = pilih_gambar()
    if gambar_path:
        # Colorize gambar
        colorize_image(gambar_path)
    else:
        print("Tidak ada file yang dipilih.")