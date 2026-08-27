import cv2
import tkinter as tk
from tkinter import ttk
import sys
import os
import time
from datetime import datetime
import threading
import numpy as np


class FaceBlurrerApp:
    def __init__(self):
        self.camera_index = 0
        self.is_running = True
        self.is_paused = False
        self.color_r = 0
        self.color_g = 0
        self.color_b = 0
        self.language = "ru"
        self.show_debug = True
        self.cap = None

        self.last_faces = []
        self.face_timer = 0
        self.face_timeout = 60
        self.previous_faces = []
        self.max_history = 5
        self.smooth_x = 0
        self.smooth_y = 0
        self.smooth_w = 0
        self.smooth_h = 0
        self.has_smooth = False
        self.no_face_counter = 0
        self.max_no_face = 30

        self.last_debug_time = 0
        self.frame_count = 0
        self.faces_count = 0
        self.last_color = (0, 0, 0)
        self.total_faces_detected = 0

        self.keys_pressed = set()

        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'accent': '#00d4ff',
            'button_bg': '#3c3c3c',
            'button_hover': '#4a4a4a'
        }

        cascade_file = self.find_cascade_file()

        if cascade_file is None:
            print("Error: haarcascade_frontalface_default.xml not found!")
            print("Search paths:")
            for path in self.get_cascade_paths():
                print(f"  - {path}")
            input("Press Enter to exit...")
            sys.exit(1)

        print(f"Cascade file found: {cascade_file}")
        self.face_cascade = cv2.CascadeClassifier(cascade_file)

        if self.face_cascade.empty():
            print("Error: Failed to load cascade!")
            input("Press Enter to exit...")
            sys.exit(1)

        self.create_language_window()

    def get_cascade_paths(self):

        paths = []


        if hasattr(sys, '_MEIPASS'):

            paths.append(os.path.join(sys._MEIPASS, 'haarcascade_frontalface_default.xml'))
        else:

            paths.append(os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml'))


        paths.append(os.path.join(os.getcwd(), 'haarcascade_frontalface_default.xml'))


        if hasattr(sys, 'executable'):
            paths.append(os.path.join(os.path.dirname(sys.executable), 'haarcascade_frontalface_default.xml'))


        try:
            paths.append(os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_frontalface_default.xml'))
            paths.append(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except:
            pass

        return paths

    def find_cascade_file(self):
        """Ищет файл в нескольких местах"""
        for path in self.get_cascade_paths():
            if os.path.exists(path):
                return path
        return None

    def get_text(self, ru, en):
        return ru if self.language == "ru" else en

    def create_language_window(self):
        self.lang_window = tk.Tk()
        self.lang_window.title("Select Language")
        self.lang_window.geometry("500x300")
        self.lang_window.configure(bg=self.colors['bg'])
        self.lang_window.resizable(False, False)

        self.center_window(self.lang_window, 500, 300)

        title = tk.Label(self.lang_window, text="Face Blurrer",
                         font=("Segoe UI", 24, "bold"),
                         fg=self.colors['accent'], bg=self.colors['bg'])
        title.pack(pady=20)

        subtitle = tk.Label(self.lang_window, text="Select Language",
                            font=("Segoe UI", 12),
                            fg=self.colors['fg'], bg=self.colors['bg'])
        subtitle.pack(pady=10)

        btn_frame = tk.Frame(self.lang_window, bg=self.colors['bg'])
        btn_frame.pack(pady=30)

        self.create_styled_button(btn_frame, "Russian",
                                  lambda: self.set_language("ru"), 0)
        self.create_styled_button(btn_frame, "English",
                                  lambda: self.set_language("en"), 1)

        self.lang_window.mainloop()

    def create_styled_button(self, parent, text, command, side):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Segoe UI", 12, "bold"),
                        bg=self.colors['button_bg'],
                        fg=self.colors['fg'],
                        activebackground=self.colors['button_hover'],
                        activeforeground=self.colors['fg'],
                        relief="flat", padx=30, pady=10,
                        cursor="hand2")
        btn.pack(side=tk.LEFT, padx=20)

        def on_enter(e):
            btn.config(bg=self.colors['button_hover'])

        def on_leave(e):
            btn.config(bg=self.colors['button_bg'])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def set_language(self, lang):
        self.language = lang
        self.lang_window.destroy()
        self.create_main_window()

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title("Face Blurrer")
        self.root.geometry("420x500")
        self.root.configure(bg=self.colors['bg'])
        self.root.resizable(False, False)

        self.center_window(self.root, 420, 500)

        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.root.focus_set()

        title = tk.Label(self.root, text="Face Blurrer",
                         font=("Segoe UI", 20, "bold"),
                         fg=self.colors['accent'], bg=self.colors['bg'])
        title.pack(pady=10)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=5)

        color_label = tk.Label(self.root, text=self.get_text("Цвет заливки", "Fill Color"),
                               font=("Segoe UI", 11),
                               fg=self.colors['fg'], bg=self.colors['bg'])
        color_label.pack(pady=5)

        slider_frame = tk.Frame(self.root, bg=self.colors['bg'])
        slider_frame.pack(pady=5)

        self.create_color_slider(slider_frame, "Red", "r")
        self.create_color_slider(slider_frame, "Green", "g")
        self.create_color_slider(slider_frame, "Blue", "b")

        self.color_preview = tk.Canvas(self.root, width=100, height=30,
                                       bg='#000000', highlightthickness=2,
                                       highlightbackground=self.colors['accent'])
        self.color_preview.pack(pady=5)

        controls_label = tk.Label(self.root, text=self.get_text("Управление", "Controls"),
                                  font=("Segoe UI", 11),
                                  fg=self.colors['fg'], bg=self.colors['bg'])
        controls_label.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg=self.colors['bg'])
        btn_frame.pack(pady=5)

        self.create_action_button(btn_frame, self.get_text("Пауза", "Pause"), self.toggle_pause, "#f39c12")
        self.create_action_button(btn_frame, self.get_text("Сброс", "Reset"), self.reset_tracking, "#3498db")
        self.create_action_button(btn_frame, self.get_text("Выход", "Exit"), self.exit_app, "#e74c3c")

        self.debug_btn = tk.Button(self.root, text="Debug: ON",
                                   command=self.toggle_debug,
                                   font=("Segoe UI", 10, "bold"),
                                   bg="#2ecc71", fg="white",
                                   relief="flat", padx=20, pady=5,
                                   cursor="hand2")
        self.debug_btn.pack(pady=5)

        hotkeys = tk.Label(self.root,
                           text=self.get_text("Space - пауза | ESC - выход | D/F1 - дебаг | R - сброс",
                                              "Space - pause | ESC - exit | D/F1 - debug | R - reset"),
                           font=("Segoe UI", 8), fg="#95a5a6",
                           bg=self.colors['bg'])
        hotkeys.pack(pady=5)

        self.status_label = tk.Label(self.root, text=self.get_text("Запуск камеры...", "Starting camera..."),
                                     font=("Segoe UI", 9),
                                     fg="#f39c12", bg=self.colors['bg'])
        self.status_label.pack(pady=5)

        self.root.after(100, self.start_video)
        self.root.mainloop()

    def on_key_press(self, event):
        key = event.keysym
        if key == 'space':
            self.toggle_pause()
        elif key == 'Escape':
            self.exit_app()
        elif key == 'd' or key == 'F1':
            self.toggle_debug()
        elif key == 'r' or key == 'R':
            self.reset_tracking()

    def on_key_release(self, event):
        pass

    def reset_tracking(self):
        self.last_faces = []
        self.previous_faces = []
        self.face_timer = 0
        self.has_smooth = False
        self.no_face_counter = 0
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Tracking reset")
        if self.show_debug:
            self.print_debug()

    def start_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.video_thread = threading.Thread(target=self.process_video, daemon=True)
        self.video_thread.start()

    def create_color_slider(self, parent, text, color):
        frame = tk.Frame(parent, bg=self.colors['bg'])
        frame.pack(fill='x', pady=2)

        label = tk.Label(frame, text=text, width=8, anchor='w',
                         font=("Segoe UI", 10), fg=self.colors['fg'],
                         bg=self.colors['bg'])
        label.pack(side=tk.LEFT, padx=10)

        value_label = tk.Label(frame, text="0", width=3,
                               font=("Segoe UI", 10, "bold"),
                               fg=self.colors['accent'], bg=self.colors['bg'])
        value_label.pack(side=tk.RIGHT, padx=10)

        slider = tk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL,
                          length=200, bg=self.colors['button_bg'],
                          fg=self.colors['fg'],
                          highlightbackground=self.colors['bg'],
                          troughcolor='#555555',
                          activebackground=self.colors['accent'],
                          relief="flat")
        slider.pack(side=tk.LEFT, padx=5)

        if color == 'r':
            self.r_slider = slider
            self.r_label = value_label
            slider.config(command=lambda v: self.update_color('r', v, value_label))
        elif color == 'g':
            self.g_slider = slider
            self.g_label = value_label
            slider.config(command=lambda v: self.update_color('g', v, value_label))
        elif color == 'b':
            self.b_slider = slider
            self.b_label = value_label
            slider.config(command=lambda v: self.update_color('b', v, value_label))

    def update_color(self, color, value, label):
        label.config(text=str(int(float(value))))
        self.color_r = self.r_slider.get()
        self.color_g = self.g_slider.get()
        self.color_b = self.b_slider.get()
        self.update_color_preview()

    def update_color_preview(self):
        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.color_preview.config(bg=hex_color)

        if self.show_debug and (r != self.last_color[0] or g != self.last_color[1] or b != self.last_color[2]):
            self.last_color = (r, g, b)
            self.print_debug()

    def create_action_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Segoe UI", 10, "bold"),
                        bg=color, fg="white",
                        relief="flat", padx=15, pady=8,
                        cursor="hand2")
        btn.pack(side=tk.LEFT, padx=5)

        def on_enter(e):
            btn.config(bg='#ffffff', fg=color)

        def on_leave(e):
            btn.config(bg=color, fg='white')

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        status = self.get_text("Приостановлено", "Paused") if self.is_paused else self.get_text("Возобновлено",
                                                                                                "Resumed")
        self.status_label.config(text=status,
                                 fg="#f39c12" if self.is_paused else "#2ecc71")
        if self.show_debug:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")

    def toggle_debug(self):
        self.show_debug = not self.show_debug
        if self.show_debug:
            self.debug_btn.config(text="Debug: ON", bg="#2ecc71", fg="white")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Debug mode ON")
            self.print_debug()
        else:
            self.debug_btn.config(text="Debug: OFF", bg="#7f8c8d", fg="white")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Debug mode OFF")

    def print_debug(self):
        r = self.r_slider.get()
        g = self.g_slider.get()
        b = self.b_slider.get()

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] === DEBUG INFO ===")
        print(f"  Faces detected: {self.faces_count}")
        print(f"  Total faces tracked: {self.total_faces_detected}")
        print(f"  Current color: RGB({r}, {g}, {b}) - #{r:02x}{g:02x}{b:02x}")
        print(f"  Language: {self.get_text('Русский', 'English')}")
        print(f"  Timer: {self.face_timer}/{self.face_timeout}")
        print(f"  Paused: {'Yes' if self.is_paused else 'No'}")
        print(f"  Debug mode: {'ON' if self.show_debug else 'OFF'}")
        print("-" * 40)

    def exit_app(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if hasattr(self, 'root') and self.root:
            self.root.quit()
            self.root.destroy()
        if hasattr(self, 'lang_window') and self.lang_window:
            self.lang_window.quit()
            self.lang_window.destroy()
        cv2.destroyAllWindows()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Program exited")
        sys.exit(0)

    def process_video(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Opening camera...")

        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        self.cap = None

        for backend in backends:
            try:
                cap = cv2.VideoCapture(0, backend)
                if cap.isOpened():
                    self.cap = cap
                    break
                cap.release()
            except:
                pass

        if self.cap is None or not self.cap.isOpened():
            error_msg = self.get_text("Камера не найдена!", "Camera not found!")
            print(error_msg)
            self.root.after(0, lambda: self.status_label.config(text=error_msg, fg="#e74c3c"))
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera opened!")
        self.root.after(0, lambda: self.status_label.config(
            text=self.get_text("Камера подключена", "Camera connected"),
            fg="#2ecc71"))

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        while self.is_running:
            if not self.is_paused:
                ret, frame = self.cap.read()
                if not ret:
                    continue

                self.frame_count += 1

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                self.faces_count = len(faces)

                if len(faces) > 0:
                    self.total_faces_detected += len(faces)
                    self.no_face_counter = 0

                    self.previous_faces.append(faces)
                    if len(self.previous_faces) > self.max_history:
                        self.previous_faces.pop(0)

                    largest_face = max(faces, key=lambda f: f[2] * f[3])

                    x, y, w, h = largest_face
                    if not self.has_smooth:
                        self.smooth_x, self.smooth_y, self.smooth_w, self.smooth_h = x, y, w, h
                        self.has_smooth = True
                    else:
                        self.smooth_x = int(self.smooth_x * 0.7 + x * 0.3)
                        self.smooth_y = int(self.smooth_y * 0.7 + y * 0.3)
                        self.smooth_w = int(self.smooth_w * 0.7 + w * 0.3)
                        self.smooth_h = int(self.smooth_h * 0.7 + h * 0.3)

                    self.last_faces = [(self.smooth_x, self.smooth_y, self.smooth_w, self.smooth_h)]
                    self.face_timer = 0
                else:
                    self.no_face_counter += 1
                    self.face_timer += 1

                if len(self.last_faces) > 0 and self.face_timer < self.face_timeout:
                    faces_to_draw = self.last_faces
                elif len(self.previous_faces) > 0 and self.no_face_counter < self.max_no_face:
                    faces_to_draw = self.previous_faces[-1]
                else:
                    faces_to_draw = []
                    if self.face_timer >= self.face_timeout:
                        self.last_faces = []
                        self.has_smooth = False
                        self.previous_faces = []

                color = (self.b_slider.get(), self.g_slider.get(), self.r_slider.get())
                for (x, y, w, h) in faces_to_draw:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

                if self.show_debug:
                    overlay = frame.copy()
                    cv2.rectangle(overlay, (5, 5), (250, 130), (0, 0, 0), -1)
                    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

                    y_offset = 25
                    info = [
                        f"Faces: {len(faces_to_draw)}",
                        f"Color: RGB({color[2]},{color[1]},{color[0]})",
                        f"Timer: {self.face_timer}/{self.face_timeout}",
                        f"No Face: {self.no_face_counter}/{self.max_no_face}"
                    ]

                    for i, text in enumerate(info):
                        cv2.putText(frame, text, (15, y_offset + i * 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                screen_height = self.root.winfo_screenheight()
                screen_width = self.root.winfo_screenwidth()
                max_height = screen_height - 100
                max_width = screen_width - 100

                height = min(480, max_height)
                width = min(640, max_width)

                cv2.namedWindow('Face Blurrer', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Face Blurrer', width, height)
                cv2.imshow('Face Blurrer', frame)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    self.exit_app()
                    break

                current_time = time.time()
                if self.show_debug and (current_time - self.last_debug_time >= 1.0):
                    self.last_debug_time = current_time
                    self.print_debug()

        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = FaceBlurrerApp()