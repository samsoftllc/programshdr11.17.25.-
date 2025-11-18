import tkinter as tk
from tkinter import messagebox, font
import time
import random
import threading

class NesOS:
    def __init__(self, root):
        self.root = root
        self.root.title("NES OS v1.0 - Famicom Disk System Edition")
        self.root.geometry("600x400")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        self.language = "EN"
        self.hardware_connected = False
        self.emulation_active = False
        self.konami_progress = []

        self.colors = {
            "bg": "#202020", "term": "#000000", "text": "#33FF00",
            "accent": "#FF0000", "ui_bg": "#000088", "white": "#FFFFFF"
        }

        self.loc = {
            "EN": {
                "boot": "CHECKING VRAM...",
                "conn_fail": "NO HARDWARE DETECTED. SWITCHING TO SIMULATION.",
                "conn_ok": "HARDWARE LINK ESTABLISHED (6502 CPU).",
                "title": "NES OPERATING SYSTEM",
                "opt_boot": "1. BOOT CARTRIDGE",
                "opt_debug": "2. MEMORY DUMP ($0000-$07FF)",
                "opt_lang": "3. LANGUAGE / 言語",
                "opt_exit": "4. POWER OFF",
                "exec": "EXECUTING...",
                "stop": "HALTED.",
                "disk_swap": "DISK SWAP DETECTED - LOADING SIDE B..."
            },
            "JP": {
                "boot": "VRAMヲ チェック シテイマス...",
                "conn_fail": "ハードウェア ガ ミツカリマセン。シミュレーション モード。",
                "conn_ok": "ハードウェア セツゾク カンリョウ (6502 CPU)。",
                "title": "ファミコン オペレーティング システム",
                "opt_boot": "1. カートリッジ キドウ",
                "opt_debug": "2. メモリ ダンプ ($0000-$07FF)",
                "opt_lang": "3. LANGUAGE / 言語",
                "opt_exit": "4. デンゲン オフ",
                "exec": "ジッコウチュウ...",
                "stop": "テイシ。",
                "disk_swap": "ディスク チェンジ カクニン - SIDE B ローディング..."
            }
        }

        self.setup_fonts()
        self.create_boot_sequence()
        self.root.bind("<Key>", self.konami_listener)

    def setup_fonts(self):
        self.sys_font = font.Font(family="Courier New", size=12, weight="bold")
        self.header_font = font.Font(family="Courier New", size=18, weight="bold")

    def create_boot_sequence(self):
        self.boot_frame = tk.Frame(self.root, bg=self.colors["term"])
        self.boot_frame.pack(fill="both", expand=True)

        self.console_log = tk.Text(self.boot_frame, bg=self.colors["term"], fg=self.colors["text"],
                                   font=self.sys_font, bd=0, state="disabled", insertbackground=self.colors["text"])
        self.console_log.pack(fill="both", expand=True, padx=20, pady=20)

        threading.Thread(target=self.boot_logic, daemon=True).start()

    def log(self, message, color=None):
        self.console_log.config(state="normal")
        tag = f"c{random.randint(0,10000)}"
        if color:
            self.console_log.tag_config(tag, foreground=color)
        self.console_log.insert(tk.END, message + "\n", tag)
        self.console_log.see(tk.END)
        self.console_log.config(state="disabled")

    def boot_logic(self):
        time.sleep(0.8)
        self.log("> POWER ON SEQUENCE")
        time.sleep(0.6)
        self.log("> RP2C02 PPU... OK")
        self.log("> 2A03 APU... OK")
        self.log("> 2KB WRAM... OK")
        time.sleep(0.4)
        self.log(self.loc[self.language]["boot"])

        self.log("> SERIAL HANDSHAKE (9600 8N1)...")
        time.sleep(1.2)

        # 80% chance of "real hardware" because we're elite
        if random.random() < 0.8:
            self.log(self.loc[self.language]["conn_ok"], self.colors["white"])
            self.hardware_connected = True
        else:
            self.log(self.loc[self.language]["conn_fail"], self.colors["accent"])
            self.hardware_connected = False

        time.sleep(1.0)
        self.root.after(0, self.load_main_menu)

    def load_main_menu(self):
        if hasattr(self, 'boot_frame'):
            self.boot_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg=self.colors["ui_bg"])
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text=self.loc[self.language]["title"],
                 bg=self.colors["ui_bg"], fg=self.colors["white"], font=self.header_font).pack(pady=30)

        status = "HW: CONNECTED" if self.hardware_connected else "HW: SIMULATION"
        col = "#00FF00" if self.hardware_connected else "#FFFF00"
        tk.Label(self.main_frame, text=status, bg="black", fg=col, font=("Courier New", 10, "bold")).place(x=450, y=15)

        menu = tk.Frame(self.main_frame, bg=self.colors["ui_bg"])
        menu.pack(pady=20)

        self.create_button(menu, self.loc[self.language]["opt_boot"], self.run_cartridge).pack(pady=8)
        self.create_button(menu, self.loc[self.language]["opt_debug"], self.memory_dump).pack(pady=8)
        self.create_button(menu, self.loc[self.language]["opt_lang"], self.toggle_language).pack(pady=8)
        self.create_button(menu, self.loc[self.language]["opt_exit"], self.root.quit, fg="#FF0000").pack(pady=8)

        # CRT TV Screen
        self.tv_screen = tk.Canvas(self.main_frame, bg="black", width=520, height=160, highlightthickness=4, highlightbackground="#333333")
        self.tv_screen.pack(pady=20)
        self.draw_crt_overlay()
        self.draw_static()

    def create_button(self, parent, text, cmd, fg="black"):
        return tk.Button(parent, text=text, command=cmd, bg="white", fg=fg, font=("Courier New", 11, "bold"),
                         width=44, height=2, bd=4, relief="raised", activebackground="#FF0000", activeforeground="white")

    def draw_crt_overlay(self):
        # Scanlines + slight curve
        for y in range(0, 160, 4):
            self.tv_screen.create_line(0, y, 520, y, fill="#000000", stipple="gray50")
        self.tv_screen.create_oval(10, 10, 510, 150, outline="#112211", width=8)

    def draw_static(self):
        self.tv_screen.delete("static")
        for _ in range(120):
            x = random.randint(0, 520)
            y = random.randint(0, 160)
            self.tv_screen.create_rectangle(x, y, x+3, y+3, fill="#222222", outline="", tags="static")
        self.tv_screen.create_text(260, 80, text="INSERT CARTRIDGE", fill="#00FF33", font=("Courier New", 16, "bold"), tags="static")

    def run_cartridge(self):
        if self.emulation_active:
            # Disk swap easter egg
            self.tv_screen.delete("all")
            self.draw_crt_overlay()
            self.tv_screen.create_text(260, 80, text=self.loc[self.language]["disk_swap"], fill="#FFFF00", font=("Courier New", 14, "bold"))
            self.root.after(2000, self.run_cartridge)
            return

        self.emulation_active = True
        self.tv_screen.delete("all")
        self.draw_crt_overlay()
        self.tv_screen.create_text(260, 80, text=self.loc[self.language]["exec"], fill="#00FF00", font=("Courier New", 18, "bold"))

        threading.Thread(target=self.hardware_loop, daemon=True).start()

    def hardware_loop(self):
        opcodes = ["LDA", "STA", "ADC", "JSR", "RTS", "INX", "BRK", "NOP", "TAX", "BMI"]
        count = 0
        while self.emulation_active and count < 80:
            op = random.choice(opcodes)
            val = f"${random.randint(0,255):02X}"
            addr = f"${random.randint(0,65535):04X}"
            msg = f"6502 > {op} {val}  [{addr}]"

            self.root.after(0, self.update_tv, msg)
            time.sleep(0.08 + random.random()*0.05)
            count += 1

        if self.emulation_active:
            self.root.after(0, lambda: self.update_tv(self.loc[self.language]["stop"], color="#FF0000"))
            self.emulation_active = False
            self.root.after(1500, lambda: (self.tv_screen.delete("all"), self.draw_crt_overlay(), self.draw_static()))

    def update_tv(self, msg, color="#00FF00"):
        self.tv_screen.create_text(10, 155, text=msg, fill=color, anchor="w", font=("Courier New", 10, "bold"), tags="log")
        self.tv_screen.tag_raise("log")

    def memory_dump(self):
        win = tk.Toplevel(self.root)
        win.title("ZERO PAGE DUMP")
        win.geometry("560x400")
        win.configure(bg="black")

        txt = tk.Text(win, bg="black", fg="#00FF00", font=("Courier New", 10), insertbackground="#00FF00")
        txt.pack(fill="both", expand=True, padx=10, pady=10)

        for addr in range(0, 0x800, 16):
            line = f"${addr:04X}: "
            line += " ".join(f"{random.randint(0,255):02X}" for _ in range(16))
            txt.insert(tk.END, line + "\n")

    def toggle_language(self):
        self.language = "JP" if self.language == "EN" else "EN"
        self.load_main_menu()

    def konami_listener(self, event):
        code = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right", "b", "a"]
        self.konami_progress.append(event.keysym)
        if len(self.konami_progress) > 10:
            self.konami_progress = self.konami_progress[-10:]
        if self.konami_progress[-10:] == code:
            self.konami_code_triggered()

    def konami_code_triggered(self):
        self.tv_screen.delete("all")
        self.tv_screen.create_rectangle(0, 0, 520, 160, fill="#FFD700")
        self.tv_screen.create_text(260, 80, text="THE LEGEND OF ZELDA", fill="red", font=("Courier New", 20, "bold"))
        self.tv_screen.create_text(260, 110, text="DISK SYSTEM - YELLOW MODE", fill="black", font=("Courier New", 12))
        self.root.after(4000, lambda: (self.tv_screen.delete("all"), self.draw_crt_overlay(), self.draw_static()))

if __name__ == "__main__":
    root = tk.Tk()
    app = NesOS(root)
    root.mainloop()
