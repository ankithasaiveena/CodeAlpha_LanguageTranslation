import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import threading

# ── Language data ──────────────────────────────────────────
LANGUAGES = {
    "English": "en", "Telugu": "te", "Hindi": "hi",
    "Tamil": "ta", "Kannada": "kn", "Malayalam": "ml",
    "French": "fr", "Spanish": "es", "German": "de",
    "Japanese": "ja", "Chinese": "zh-CN", "Arabic": "ar",
    "Russian": "ru", "Portuguese": "pt", "Italian": "it",
    "Korean": "ko", "Dutch": "nl", "Turkish": "tr",
    "Polish": "pl", "Swedish": "sv"
}
lang_names = list(LANGUAGES.keys())

# ── Translation logic ───────────────────────────────────────
def do_translate():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        status_var.set("⚠  Please enter some text first!")
        return
    src = LANGUAGES[source_var.get()]
    tgt = LANGUAGES[target_var.get()]
    status_var.set("⏳  Translating...")
    translate_btn.config(state="disabled")

    def run():
        try:
            result = GoogleTranslator(source=src, target=tgt).translate(text)
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, result)
            output_box.config(state="disabled")
            char_count = len(result)
            status_var.set(f"✅  Translation complete — {char_count} characters")
        except Exception as e:
            status_var.set(f"❌  Error: {str(e)}")
        finally:
            translate_btn.config(state="normal")

    threading.Thread(target=run, daemon=True).start()

def copy_text():
    t = output_box.get("1.0", tk.END).strip()
    if t:
        root.clipboard_clear()
        root.clipboard_append(t)
        status_var.set("📋  Copied to clipboard!")

def clear_all():
    input_box.delete("1.0", tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    status_var.set("🌍  Ready to translate")
    char_var.set("0 / 500")

def swap_languages():
    s = source_var.get()
    t = target_var.get()
    source_var.set(t)
    target_var.set(s)
    status_var.set("🔄  Languages swapped!")

def count_chars(event=None):
    n = len(input_box.get("1.0", tk.END).strip())
    char_var.set(f"{n} / 500")

# ── Window ──────────────────────────────────────────────────
root = tk.Tk()
root.title("LinguaSwift — Language Translator")
root.geometry("780x650")
root.resizable(False, False)
root.configure(bg="#0f0f1a")

# Set custom icon color (taskbar)
root.tk_setPalette(background="#0f0f1a")

# ── Fonts ───────────────────────────────────────────────────
FONT_TITLE  = ("Georgia", 22, "bold")
FONT_LABEL  = ("Trebuchet MS", 11)
FONT_TEXT   = ("Consolas", 12)
FONT_BTN    = ("Trebuchet MS", 11, "bold")
FONT_SMALL  = ("Trebuchet MS", 9)
FONT_STATUS = ("Trebuchet MS", 10)

# ── Colors ──────────────────────────────────────────────────
BG          = "#0f0f1a"
CARD        = "#1a1a2e"
ACCENT      = "#e94560"
ACCENT2     = "#0f3460"
TEXT        = "#eaeaea"
MUTED       = "#888899"
INPUT_BG    = "#12122a"
SUCCESS     = "#4ecca3"
BTN_COPY    = "#4ecca3"
BTN_CLEAR   = "#e94560"
BTN_SWAP    = "#f5a623"

# ── Header ──────────────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT2, height=70)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header,
         text="🌐  LinguaSwift",
         font=FONT_TITLE,
         bg=ACCENT2,
         fg=TEXT).pack(side="left", padx=25, pady=15)

tk.Label(header,
         text="Powered by Google Translate API",
         font=FONT_SMALL,
         bg=ACCENT2,
         fg=MUTED).pack(side="right", padx=25)

# ── Accent line ─────────────────────────────────────────────
tk.Frame(root, bg=ACCENT, height=3).pack(fill="x")

# ── Language selector card ───────────────────────────────────
lang_card = tk.Frame(root, bg=CARD, pady=15)
lang_card.pack(fill="x", padx=20, pady=(15, 5))

# Source
tk.Label(lang_card, text="FROM", font=FONT_SMALL,
         bg=CARD, fg=MUTED).grid(row=0, column=0, padx=(20,5), sticky="w")
source_var = tk.StringVar(value="English")
src_dd = ttk.Combobox(lang_card, textvariable=source_var,
                      values=lang_names, width=18,
                      font=FONT_LABEL, state="readonly")
src_dd.grid(row=1, column=0, padx=(20,5), pady=5)

# Swap button
swap_btn = tk.Button(lang_card, text="⇄",
                     font=("Trebuchet MS", 14, "bold"),
                     bg=BTN_SWAP, fg="#0f0f1a",
                     bd=0, padx=10, pady=4,
                     command=swap_languages,
                     cursor="hand2",
                     relief="flat")
swap_btn.grid(row=1, column=1, padx=15)

# Target
tk.Label(lang_card, text="TO", font=FONT_SMALL,
         bg=CARD, fg=MUTED).grid(row=0, column=2, padx=5, sticky="w")
target_var = tk.StringVar(value="Telugu")
tgt_dd = ttk.Combobox(lang_card, textvariable=target_var,
                      values=lang_names, width=18,
                      font=FONT_LABEL, state="readonly")
tgt_dd.grid(row=1, column=2, padx=5, pady=5)

# Style dropdowns
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox",
                fieldbackground=INPUT_BG,
                background=INPUT_BG,
                foreground=TEXT,
                selectbackground=ACCENT2,
                selectforeground=TEXT,
                bordercolor=ACCENT2)

# ── Input area ───────────────────────────────────────────────
input_frame = tk.Frame(root, bg=CARD, bd=0)
input_frame.pack(fill="x", padx=20, pady=(5,0))

tk.Label(input_frame, text="✏  Enter Text",
         font=FONT_LABEL, bg=CARD, fg=MUTED).pack(anchor="w", padx=10, pady=(10,2))

input_box = tk.Text(input_frame,
                    height=7, font=FONT_TEXT,
                    bg=INPUT_BG, fg=TEXT,
                    insertbackground=ACCENT,
                    bd=0, padx=10, pady=8,
                    relief="flat",
                    wrap="word",
                    selectbackground=ACCENT2)
input_box.pack(fill="x", padx=10, pady=(0,5))
input_box.bind("<KeyRelease>", count_chars)

# Char counter
char_var = tk.StringVar(value="0 / 500")
tk.Label(input_frame, textvariable=char_var,
         font=FONT_SMALL, bg=CARD, fg=MUTED).pack(anchor="e", padx=10)

# ── Buttons ───────────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=12)

translate_btn = tk.Button(btn_frame,
                          text="🔁  Translate",
                          font=FONT_BTN,
                          bg=ACCENT, fg=TEXT,
                          bd=0, padx=25, pady=10,
                          command=do_translate,
                          cursor="hand2",
                          relief="flat",
                          activebackground="#c73652",
                          activeforeground=TEXT)
translate_btn.grid(row=0, column=0, padx=8)

copy_btn = tk.Button(btn_frame,
                     text="📋  Copy",
                     font=FONT_BTN,
                     bg=BTN_COPY, fg="#0f0f1a",
                     bd=0, padx=25, pady=10,
                     command=copy_text,
                     cursor="hand2",
                     relief="flat")
copy_btn.grid(row=0, column=1, padx=8)

clear_btn = tk.Button(btn_frame,
                      text="🗑  Clear",
                      font=FONT_BTN,
                      bg=BTN_CLEAR, fg=TEXT,
                      bd=0, padx=25, pady=10,
                      command=clear_all,
                      cursor="hand2",
                      relief="flat")
clear_btn.grid(row=0, column=2, padx=8)

# ── Output area ───────────────────────────────────────────────
out_frame = tk.Frame(root, bg=CARD)
out_frame.pack(fill="x", padx=20, pady=(0,10))

tk.Label(out_frame, text="📄  Translated Text",
         font=FONT_LABEL, bg=CARD, fg=MUTED).pack(anchor="w", padx=10, pady=(10,2))

output_box = tk.Text(out_frame,
                     height=7, font=FONT_TEXT,
                     bg=INPUT_BG, fg=SUCCESS,
                     bd=0, padx=10, pady=8,
                     relief="flat",
                     wrap="word",
                     state="disabled",
                     selectbackground=ACCENT2)
output_box.pack(fill="x", padx=10, pady=(0,10))

# ── Status bar ────────────────────────────────────────────────
status_var = tk.StringVar(value="🌍  Ready to translate")
status_bar = tk.Label(root,
                      textvariable=status_var,
                      font=FONT_STATUS,
                      bg=ACCENT2,
                      fg=TEXT,
                      anchor="w",
                      padx=15)
status_bar.pack(fill="x", side="bottom")

root.mainloop()