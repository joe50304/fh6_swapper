"""
Forza Horizon 6 語音語言資料夾交換器
=====================================
使用說明：
1. 遊戲內先選好你想要的「語音語言」（例如：日語），然後關閉遊戲
2. 開啟此工具，路徑會自動偵測 Forza Horizon 6 的 StringTables 資料夾
3. 選擇你要的「文字語言」資料夾（例如 CHT）與「語音語言」資料夾（例如 JP）
4. 點「交換資料夾」完成 → 遊戲即變成中文介面 + 日文語音
5. 遊戲更新後點「還原」即可換回原始設定
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, json, shutil, datetime, sys, pathlib

APP_TITLE  = "FH6 語音語言交換器"
APP_VER    = "v1.0"
STATE_FILE = pathlib.Path(os.environ.get("APPDATA", os.path.expanduser("~"))) / "FH6Swapper" / "state.json"

# ─── 常見語言代碼對照 ─────────────────────────────────────
LANG_MAP = {
    "CHT": "繁體中文",
    "CHS": "簡體中文",
    "JP":  "日文",
    "EN":  "英文",
    "KR":  "韓文",
    "FR":  "法文",
    "DE":  "德文",
    "ES":  "西班牙文",
    "IT":  "義大利文",
    "PT":  "葡萄牙文",
    "RU":  "俄文",
    "PL":  "波蘭文",
    "AR":  "阿拉伯文",
}

# ─── 自動搜尋 StringTables 路徑 ───────────────────────────
def find_default_path():
    candidates = []
    for drive in "CDEFG":
        for program_dir in ["Program Files", "Program Files (x86)", "Games", "XboxGames"]:
            p = pathlib.Path(f"{drive}:\\{program_dir}\\Forza Horizon 6\\media\\Stripped\\StringTables")
            candidates.append(p)
    # Steam / MS Store paths
    localappdata = os.environ.get("LOCALAPPDATA", "")
    if localappdata:
        candidates.append(pathlib.Path(localappdata) / "Packages" / "Microsoft.SunriseBaseGame_8wekyb3d8bbwe" / "LocalCache" / "Local" / "media" / "Stripped" / "StringTables")
    for p in candidates:
        if p.exists():
            return str(p)
    return ""


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE} {APP_VER}")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
        self._center()
        self._build_ui()
        self._load_state()
        self._detect_folders()

    def _center(self):
        self.update_idletasks()
        w, h = 620, 580
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ─── UI ───────────────────────────────────────────────
    def _build_ui(self):
        BG   = "#0f172a"
        CARD = "#1e293b"
        ACC  = "#38bdf8"
        FG   = "#e2e8f0"
        MUT  = "#64748b"
        FONT      = ("Microsoft JhengHei UI", 10)
        FONT_BOLD = ("Microsoft JhengHei UI", 10, "bold")
        FONT_MONO = ("Consolas", 9)
        FONT_H    = ("Microsoft JhengHei UI", 13, "bold")

        def card(parent, **kw):
            f = tk.Frame(parent, bg=CARD, relief="flat", **kw)
            return f

        def label(parent, text, font=FONT, fg=FG, **kw):
            # 如果使用者沒指定 bg，才自動代入 parent 的 bg 顏色，避免衝突
            if "bg" not in kw:
                kw["bg"] = parent["bg"]
            return tk.Label(parent, text=text, font=font, fg=fg, **kw)

        def sep(parent):
            return tk.Frame(parent, bg="#334155", height=1)

        pad = dict(padx=16, pady=8)

        # ── 頂部標題 ────────────────────────────────────
        hdr = tk.Frame(self, bg="#0c1a2e")
        hdr.pack(fill="x")
        label(hdr, f"  🎮  {APP_TITLE}", font=FONT_H, fg=ACC, bg="#0c1a2e").pack(side="left", pady=12, padx=8)
        label(hdr, APP_VER, font=FONT_MONO, fg=MUT, bg="#0c1a2e").pack(side="right", padx=16)

        # ── 使用說明 ────────────────────────────────────
        instr = card(self)
        instr.pack(fill="x", padx=14, pady=(12,4))
        guide = (
            "📋 使用步驟：\n"
            "① 遊戲內「選項 → 語言」選好你要的語音語言（例：日語），然後關閉遊戲\n"
            "② 確認下方路徑指向 Forza Horizon 6\\media\\Stripped\\StringTables\n"
            "③ 選擇「介面文字語言」（你想看的字幕語言，例：CHT 繁體中文）\n"
            "④ 選擇「語音語言」（遊戲內剛選的那個，例：JP 日文）\n"
            "⑤ 點「交換資料夾」→ 重啟遊戲即生效（中文介面 + 日文語音）\n"
            "⑥ 遊戲更新後點「還原」即可換回，更新完再重新交換"
        )
        label(instr, guide, font=("Microsoft JhengHei UI", 9), fg="#94a3b8",
              justify="left", wraplength=580).pack(padx=12, pady=10, anchor="w")

        # ── StringTables 路徑 ───────────────────────────
        path_card = card(self)
        path_card.pack(fill="x", padx=14, pady=4)
        label(path_card, "StringTables 路徑", font=FONT_BOLD, fg=ACC).pack(anchor="w", padx=12, pady=(8,2))

        prow = tk.Frame(path_card, bg=CARD)
        prow.pack(fill="x", padx=12, pady=(0,10))
        self.var_path = tk.StringVar()
        self.entry_path = tk.Entry(prow, textvariable=self.var_path, font=FONT_MONO,
                                   bg="#0f172a", fg=FG, insertbackground=ACC,
                                   relief="flat", bd=0, highlightthickness=1,
                                   highlightbackground="#334155", highlightcolor=ACC)
        self.entry_path.pack(side="left", fill="x", expand=True, ipady=5, padx=(0,6))
        tk.Button(prow, text="瀏覽…", font=FONT, bg="#1d4ed8", fg=FG,
                  activebackground="#2563eb", activeforeground=FG,
                  relief="flat", cursor="hand2", bd=0,
                  command=self._browse_path, padx=10).pack(side="left")

        self.lbl_path_status = label(path_card, "", font=("Microsoft JhengHei UI", 9), fg=MUT)
        self.lbl_path_status.pack(anchor="w", padx=12, pady=(0,6))

        # ── 語言選擇 ────────────────────────────────────
        lang_card = card(self)
        lang_card.pack(fill="x", padx=14, pady=4)
        label(lang_card, "語言資料夾選擇", font=FONT_BOLD, fg=ACC).pack(anchor="w", padx=12, pady=(8,4))

        grid = tk.Frame(lang_card, bg=CARD)
        grid.pack(fill="x", padx=12, pady=(0,10))

        label(grid, "🖥  介面文字語言（CHT = 繁體中文）", fg=FG).grid(row=0, column=0, sticky="w", pady=2)
        self.var_a = tk.StringVar()
        self.combo_a = ttk.Combobox(grid, textvariable=self.var_a, width=28, font=FONT_MONO, state="readonly")
        self.combo_a.grid(row=0, column=1, padx=(10,0), pady=2, sticky="w")
        self.lbl_a_desc = label(grid, "", fg="#22d3ee", font=("Microsoft JhengHei UI", 9))
        self.lbl_a_desc.grid(row=0, column=2, padx=8, sticky="w")

        label(grid, "🎵  語音語言（JP = 日文）", fg=FG).grid(row=1, column=0, sticky="w", pady=2)
        self.var_b = tk.StringVar()
        self.combo_b = ttk.Combobox(grid, textvariable=self.var_b, width=28, font=FONT_MONO, state="readonly")
        self.combo_b.grid(row=1, column=1, padx=(10,0), pady=2, sticky="w")
        self.lbl_b_desc = label(grid, "", fg="#22d3ee", font=("Microsoft JhengHei UI", 9))
        self.lbl_b_desc.grid(row=1, column=2, padx=8, sticky="w")

        self.var_a.trace_add("write", lambda *_: self._update_desc())
        self.var_b.trace_add("write", lambda *_: self._update_desc())
        self.var_path.trace_add("write", lambda *_: self._detect_folders())

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#0f172a", background="#0f172a",
                        foreground=FG, selectbackground="#1d4ed8", selectforeground=FG)

        # ── 狀態 ────────────────────────────────────────
        st_card = card(self)
        st_card.pack(fill="x", padx=14, pady=4)
        label(st_card, "目前狀態", font=FONT_BOLD, fg=ACC).pack(anchor="w", padx=12, pady=(8,2))
        self.lbl_status = label(st_card, "尚未操作", fg=MUT, font=FONT)
        self.lbl_status.pack(anchor="w", padx=12, pady=(0,6))
        self.lbl_backup = label(st_card, "", fg=MUT, font=("Microsoft JhengHei UI", 9))
        self.lbl_backup.pack(anchor="w", padx=12, pady=(0,8))

        # ── 按鈕 ────────────────────────────────────────
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=10)

        def btn(text, cmd, bg, width=14):
            return tk.Button(btn_row, text=text, command=cmd,
                             font=FONT_BOLD, bg=bg, fg=FG,
                             activebackground=bg, activeforeground=FG,
                             relief="flat", cursor="hand2", bd=0,
                             width=width, pady=8)

        self.btn_swap    = btn("🔄  交換資料夾", self._do_swap,    "#0ea5e9")
        self.btn_restore = btn("↩  還原",        self._do_restore, "#7c3aed")
        self.btn_open    = btn("📂  開啟目錄",    self._open_dir,   "#0f766e", width=12)

        self.btn_swap.pack(side="left", padx=6)
        self.btn_restore.pack(side="left", padx=6)
        self.btn_open.pack(side="left", padx=6)

        # ── 日誌 ────────────────────────────────────────
        log_card = card(self)
        log_card.pack(fill="both", expand=True, padx=14, pady=(4,14))
        label(log_card, "操作日誌", font=FONT_BOLD, fg=ACC).pack(anchor="w", padx=12, pady=(8,2))

        log_frame = tk.Frame(log_card, bg="#0a0f1e")
        log_frame.pack(fill="both", expand=True, padx=12, pady=(0,10))

        self.log_box = tk.Text(log_frame, font=FONT_MONO, bg="#0a0f1e", fg=FG,
                               relief="flat", bd=0, state="disabled",
                               height=7, wrap="word",
                               insertbackground=ACC)
        sb = tk.Scrollbar(log_frame, command=self.log_box.yview, bg=CARD)
        self.log_box.configure(yscrollcommand=sb.set)
        self.log_box.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        sb.pack(side="right", fill="y")

        self.log_box.tag_config("ok",   foreground="#4ade80")
        self.log_box.tag_config("err",  foreground="#f87171")
        self.log_box.tag_config("warn", foreground="#fbbf24")
        self.log_box.tag_config("info", foreground="#38bdf8")
        self.log_box.tag_config("ts",   foreground="#475569")

    # ─── 路徑瀏覽 ─────────────────────────────────────────
    def _browse_path(self):
        d = filedialog.askdirectory(title="選擇 StringTables 資料夾",
                                    initialdir=self.var_path.get() or "C:\\")
        if d:
            self.var_path.set(d.replace("/", "\\"))

    # ─── 偵測子資料夾 ────────────────────────────────────
    def _detect_folders(self):
        p = self.var_path.get().strip()
        if not p or not os.path.isdir(p):
            self.lbl_path_status.config(text="⚠ 路徑不存在，請手動選擇", fg="#fbbf24")
            self.combo_a["values"] = []
            self.combo_b["values"] = []
            return

        folders = sorted([f for f in os.listdir(p) if os.path.isdir(os.path.join(p, f))])
        if not folders:
            self.lbl_path_status.config(text="⚠ 找不到語言子資料夾", fg="#fbbf24")
            return

        self.lbl_path_status.config(text=f"✔ 找到 {len(folders)} 個語言資料夾：{', '.join(folders)}", fg="#4ade80")
        self.combo_a["values"] = folders
        self.combo_b["values"] = folders

        # 自動預設 CHT / JP
        if "CHT" in folders and not self.var_a.get():
            self.var_a.set("CHT")
        elif folders and not self.var_a.get():
            self.var_a.set(folders[0])

        if "JP" in folders and not self.var_b.get():
            self.var_b.set("JP")
        elif len(folders) > 1 and not self.var_b.get():
            self.var_b.set(folders[1])

    def _update_desc(self):
        a = self.var_a.get()
        b = self.var_b.get()
        self.lbl_a_desc.config(text=LANG_MAP.get(a, ""))
        self.lbl_b_desc.config(text=LANG_MAP.get(b, ""))

    # ─── 交換 ────────────────────────────────────────────
    def _do_swap(self):
        base = self.var_path.get().strip()
        a    = self.var_a.get().strip()
        b    = self.var_b.get().strip()

        if not base or not os.path.isdir(base):
            messagebox.showerror("錯誤", "StringTables 路徑無效，請重新選擇。")
            return
        if not a or not b:
            messagebox.showwarning("提示", "請選擇兩個語言資料夾。")
            return
        if a == b:
            messagebox.showwarning("提示", "兩個資料夾不能相同。")
            return

        path_a = os.path.join(base, a)
        path_b = os.path.join(base, b)

        if not os.path.isdir(path_a):
            messagebox.showerror("錯誤", f"找不到資料夾：{path_a}")
            return
        if not os.path.isdir(path_b):
            messagebox.showerror("錯誤", f"找不到資料夾：{path_b}")
            return

        tmp = os.path.join(base, f"__tmp_fh6swap_{int(datetime.datetime.now().timestamp())}__")
        try:
            os.rename(path_a, tmp)
            os.rename(path_b, path_a)
            os.rename(tmp, path_b)
        except Exception as e:
            messagebox.showerror("錯誤", f"交換失敗：{e}\n請確認遊戲已完全關閉，且以系統管理員執行此程式。")
            return

        record = {
            "time": datetime.datetime.now().isoformat(),
            "base": base,
            "a": a,
            "b": b,
        }
        state = self._load_raw_state()
        state.setdefault("history", []).append(record)
        self._save_raw_state(state)

        msg = f"✔ 交換完成：「{a}」↔「{b}」"
        self._log(msg, "ok")
        self._log(f"  效果：{LANG_MAP.get(a,'?')} 介面 + {LANG_MAP.get(b,'?')} 語音", "info")
        self.lbl_status.config(text=f"已交換 {a} ↔ {b}（{LANG_MAP.get(a,'')} 介面 + {LANG_MAP.get(b,'')} 語音）", fg="#4ade80")
        self._refresh_backup_label()

    # ─── 還原 ────────────────────────────────────────────
    def _do_restore(self):
        state = self._load_raw_state()
        history = state.get("history", [])
        if not history:
            messagebox.showinfo("提示", "沒有可還原的備份記錄。")
            return

        last = history[-1]
        base = last["base"]
        a    = last["a"]
        b    = last["b"]

        path_a = os.path.join(base, a)
        path_b = os.path.join(base, b)

        if not os.path.isdir(path_a) or not os.path.isdir(path_b):
            messagebox.showerror("錯誤", f"資料夾不存在，可能路徑已變更。\n{path_a}\n{path_b}")
            return

        tmp = os.path.join(base, f"__tmp_fh6swap_{int(datetime.datetime.now().timestamp())}__")
        try:
            os.rename(path_a, tmp)
            os.rename(path_b, path_a)
            os.rename(tmp, path_b)
        except Exception as e:
            messagebox.showerror("錯誤", f"還原失敗：{e}\n請確認遊戲已完全關閉。")
            return

        history.pop()
        self._save_raw_state(state)

        self._log(f"↩ 已還原：「{a}」↔「{b}」（回到原始配置）", "warn")
        self.lbl_status.config(text="已還原至原始配置", fg="#fbbf24")
        self._refresh_backup_label()

    # ─── 開啟目錄 ─────────────────────────────────────────
    def _open_dir(self):
        p = self.var_path.get().strip()
        if p and os.path.isdir(p):
            os.startfile(p)
        else:
            messagebox.showwarning("提示", "路徑無效。")

    # ─── 日誌 ────────────────────────────────────────────
    def _log(self, text, tag=""):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[{ts}] ", "ts")
        self.log_box.insert("end", text + "\n", tag)
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    # ─── 狀態持久化 ───────────────────────────────────────
    def _load_raw_state(self):
        try:
            if STATE_FILE.exists():
                return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {}

    def _save_raw_state(self, state):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_state(self):
        state = self._load_raw_state()
        path  = state.get("last_path", find_default_path())
        self.var_path.set(path)
        self._refresh_backup_label()
        self._log("程式啟動", "info")
        if path and os.path.isdir(path):
            self._log(f"偵測到路徑：{path}", "ok")
        else:
            self._log("⚠ 未偵測到 FH6 路徑，請手動選擇 StringTables 資料夾", "warn")

    def _refresh_backup_label(self):
        h = self._load_raw_state().get("history", [])
        if h:
            t = datetime.datetime.fromisoformat(h[-1]["time"]).strftime("%m/%d %H:%M")
            self.lbl_backup.config(text=f"備份 {len(h)} 筆，最後操作：{t}", fg="#4ade80")
        else:
            self.lbl_backup.config(text="無備份記錄", fg="#64748b")

    def destroy(self):
        # Save last path on exit
        state = self._load_raw_state()
        state["last_path"] = self.var_path.get()
        self._save_raw_state(state)
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()