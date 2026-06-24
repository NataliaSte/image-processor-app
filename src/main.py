import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import cv2
import numpy as np
import os
import sys

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображений")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)

        self.image = None
        self.original_image = None
        self.image_path = None

        self.create_widgets()
        self.status_update("Ожидание загрузки изображения")

    def create_widgets(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.btn_load = tk.Button(toolbar, text="Загрузить изображение", command=self.load_image)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_camera = tk.Button(toolbar, text="Снимок с камеры", command=self.capture_from_camera)
        self.btn_camera.pack(side=tk.LEFT, padx=5)

        self.btn_red = tk.Button(toolbar, text="Красный канал", command=lambda: self.show_channel("R"))
        self.btn_red.pack(side=tk.LEFT, padx=5)

        self.btn_green = tk.Button(toolbar, text="Зелёный канал", command=lambda: self.show_channel("G"))
        self.btn_green.pack(side=tk.LEFT, padx=5)

        self.btn_blue = tk.Button(toolbar, text="Синий канал", command=lambda: self.show_channel("B"))
        self.btn_blue.pack(side=tk.LEFT, padx=5)

        self.btn_negative = tk.Button(toolbar, text="Негатив", command=self.apply_negative)
        self.btn_negative.pack(side=tk.LEFT, padx=5)

        self.btn_border = tk.Button(toolbar, text="Границы", command=self.add_border)
        self.btn_border.pack(side=tk.LEFT, padx=5)

        self.btn_line = tk.Button(toolbar, text="Нарисовать линию", command=self.draw_line)
        self.btn_line.pack(side=tk.LEFT, padx=5)

        self.btn_reset = tk.Button(toolbar, text="Сброс", command=self.reset_image)
        self.btn_reset.pack(side=tk.LEFT, padx=5)

        self.btn_save = tk.Button(toolbar, text="Сохранить", command=self.save_image)
        self.btn_save.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Готов", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.info_label = tk.Label(self.root, text="Изображение не загружено", font=("Arial", 10))
        self.info_label.pack(side=tk.BOTTOM, pady=5)

        self.camera_hint = tk.Label(
        self.root,
        text="Для снимка с камеры нажмите ПРОБЕЛ, для отмены — ESC",
        font=("Arial", 10),
        fg="gray"
        )
        self.camera_hint.pack(side=tk.BOTTOM, pady=2)

    def status_update(self, message):
        self.status_label.config(text=message)
        self.root.update()

    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path:
                return

            self.image_path = file_path
            self.original_image = Image.open(file_path).convert("RGB")
            self.image = self.original_image.copy()

            self.update_display()
            self.info_label.config(text=f"Загружено: {os.path.basename(file_path)} | Размер: {self.image.size}")
            self.status_update("Изображение загружено успешно")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")
            self.status_update("Ошибка загрузки")

    def capture_from_camera(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Ошибка", "Не удалось открыть веб-камеру")
                self.status_update("Ошибка: камера не обнаружена")
                return

            self.status_update("Нажмите Пробел для снимка или Esc для отмены")
            window_name = "Веб-камера - нажмите ПРОБЕЛ для снимка, ESC для отмены"
            cv2.namedWindow(window_name)

            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Ошибка", "Не удалось получить кадр с камеры")
                    break
                cv2.imshow(window_name, frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):
                    self.original_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    self.image = self.original_image.copy()
                    self.image_path = None
                    cap.release()
                    cv2.destroyAllWindows()
                    self.update_display()
                    self.info_label.config(text="Снимок сделан с веб-камеры")
                    self.status_update("Снимок успешно сделан")
                    return
                elif key == 27:  # Esc
                    cap.release()
                    cv2.destroyAllWindows()
                    self.status_update("Съемка отменена")
                    return

            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при работе с камерой: {str(e)}")
            self.status_update("Ошибка камеры")
            cv2.destroyAllWindows()

    def update_display(self):
        if self.image is None:
            return

        max_width = 800
        max_height = 600
        img_copy = self.image.copy()
        img_copy.thumbnail((max_width, max_height))

        photo = ImageTk.PhotoImage(img_copy)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def show_channel(self, channel):
        if self.original_image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение!")
            return

        try:
            img_array = np.array(self.original_image.copy().convert("RGB"))

            if channel == "R":
                img_array[:, :, 1] = 0
                img_array[:, :, 2] = 0
            elif channel == "G":
                img_array[:, :, 0] = 0
                img_array[:, :, 2] = 0
            elif channel == "B":
                img_array[:, :, 0] = 0
                img_array[:, :, 1] = 0

            self.image = Image.fromarray(img_array)
            self.update_display()
            self.status_update(f"Показан {channel}-канал")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось показать канал: {str(e)}")

    def apply_negative(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение!")
            return

        try:
            self.image = ImageOps.invert(self.image.convert("RGB"))
            self.update_display()
            self.status_update("Негатив применен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось применить негатив: {str(e)}")

    def add_border(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение!")
            return

        try:
            border_size_str = simpledialog.askstring(
                "Размер границы",
                "Введите толщину границы (в пикселях):",
                initialvalue="10"
            )
            if not border_size_str:
                return

            border_size = int(border_size_str)
            if border_size < 0:
                messagebox.showwarning("Внимание", "Размер должен быть положительным")
                return

            self.image = ImageOps.expand(self.image.convert("RGB"), border=border_size, fill="black")
            self.update_display()
            self.status_update(f"Добавлены границы размером {border_size} пикселей")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении границ: {str(e)}")

    def draw_line(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение!")
            return

        try:
            coords = simpledialog.askstring(
                "Координаты линии",
                "Введите координаты в формате: x1,y1,x2,y2\nНапример: 50,50,200,200"
            )
            if not coords:
                return

            parts = coords.split(',')
            if len(parts) != 4:
                messagebox.showerror("Ошибка", "Введите 4 числа через запятую")
                return

            x1, y1, x2, y2 = map(int, parts)

            thickness = simpledialog.askstring(
                "Толщина линии",
                "Введите толщину линии (в пикселях):",
                initialvalue="3"
            )
            if not thickness:
                return

            thickness_int = int(thickness)
            if thickness_int < 1:
                messagebox.showwarning("Внимание", "Толщина должна быть положительной")
                return

            draw = ImageDraw.Draw(self.image)
            draw.line((x1, y1, x2, y2), fill="green", width=thickness_int)
            self.update_display()
            self.status_update(f"Нарисована зеленая линия от ({x1},{y1}) до ({x2},{y2}) толщиной {thickness_int}")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Введите корректные числовые значения: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при рисовании линии: {str(e)}")

    def reset_image(self):
        if self.original_image is None:
            messagebox.showwarning("Внимание", "Нет изображения для сброса")
            return

        self.image = self.original_image.copy()
        self.update_display()
        self.status_update("Изображение сброшено к оригиналу")

    def save_image(self):
        if self.image is None:
            messagebox.showwarning("Внимание", "Нет изображения для сохранения")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if not file_path:
                return

            self.image.save(file_path)
            self.status_update(f"Изображение сохранено: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()