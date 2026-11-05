from customtkinter import *
from socket import *
from threading import *

# вікно
window = CTk()
window.geometry("500x500")
window.title("LogiTalk")

set_appearance_mode("Light") 

# палітра кольорів
BG_MAIN = ("#FFF0F5", "#2D2024")         
BG_SIDEBAR = ("#FFE4E1", "#3D2B30")      
BTN_COLOR = ("#FF69B4", "#C71585")       
BTN_HOVER = ("#FF1493", "#A10E6B")       
MSG_RIGHT = ("#FFB6C1", "#DB7093")       
MSG_LEFT = ("#E6A8B8", "#B07281")        
TEXT_MAIN = ("#4A353B", "#FFF0F5")       

window.configure(fg_color=BG_MAIN)

client_socket = socket(AF_INET, SOCK_STREAM)
is_connected = False
HOST = "localhost"
PORT = 22

try:
    client_socket.connect((HOST, PORT))
    is_connected = True
    print("Вітаємо, ви тепер на сервері!")
except:
    print("Ой-ой, помилка з'єднання :<")

my_username = "Noname"
window.menu_visible = False

def showMenu():
    if window.menu_visible == True:
        sidebar_frame.pack_forget()
        window.menu_visible = False
        btn_menu.configure(text="▶")
    else:
        sidebar_frame.pack(side="left", fill="y", before=main_frame)
        window.menu_visible = True
        btn_menu.configure(text="◀")

def add_mass(massage_text, align="right"):
    msg_label = CTkLabel(
        chat,
        text=massage_text,
        corner_radius=12,  
        fg_color=MSG_RIGHT if align == "right" else MSG_LEFT,
        padx=12, pady=6,
        text_color="white",
        font=("Helvetica", 13)
    )
    anchor = "e" if align == "right" else "w"
    msg_label.pack(anchor=anchor, padx=10, pady=5)
    
    window.update_idletasks()
    chat._parent_canvas.yview_moveto(1.0)

def send_mass(event=None):
    if is_connected == False:
        return

    message = typeMas.get()
    if message.strip():
        add_mass(f"Ви: {message}", align="right")
        full_message = f"{my_username}: {message}"
        client_socket.sendall(full_message.encode("utf-8"))
        typeMas.delete(0, "end")

def CangeTheme():
    theme = get_appearance_mode()
    if theme == "Dark":
        set_appearance_mode("Light")
    else:
        set_appearance_mode("Dark")

# бічне меню
sidebar_frame = CTkFrame(window, width=160, corner_radius=0, fg_color=BG_SIDEBAR)
sidebar_frame.pack_propagate(False)

# Круглий аватар
avatar_label = CTkLabel(
    sidebar_frame, 
    text="🐱",                  
    font=("Helvetica", 40),     
    width=80, height=80,        
    corner_radius=40,           
    fg_color=BG_MAIN,           
    text_color=TEXT_MAIN
)
avatar_label.pack(pady=(20, 5))

# Функція зміни аватарки при виборі емодзі зі списку
def change_avatar_emoji(chosen_emoji):
    avatar_label.configure(text=chosen_emoji, font=("Helvetica", 40))

# Перелік милих смайликів для вибору аватарки
emoji_list = ["🐱", "🌸", "🎀", "🧸", "🐰", "🦊", "👑", "✨", "🤍", "🍓"]

emoji_menu = CTkOptionMenu(
    sidebar_frame,
    values=emoji_list,
    command=change_avatar_emoji,
    width=70,
    height=28,
    fg_color=BTN_COLOR,
    button_color=BTN_COLOR,
    button_hover_color=BTN_HOVER,
    dropdown_fg_color=BG_SIDEBAR,
    dropdown_text_color=TEXT_MAIN,
    dropdown_hover_color=BTN_COLOR,
    text_color="white",
    font=("Helvetica", 14)
)
emoji_menu.set("🐱") # Початкова аватарка - котик
emoji_menu.pack(pady=(0, 10))

name_label = CTkLabel(sidebar_frame, text="Кицю, тебе звуть?", text_color=TEXT_MAIN, font=("Helvetica", 12, "bold"))
name_label.pack(pady=(5, 2), padx=10)

name_entry = CTkEntry(
    sidebar_frame, 
    placeholder_text="Введи своє ім'я...",
    fg_color=BG_MAIN,
    text_color=TEXT_MAIN,
    border_color=BTN_COLOR
)
name_entry.pack(pady=5, padx=10, fill="x")

def save_name_action():
    global my_username
    new_name = name_entry.get().strip()
    if new_name:
        my_username = new_name
        name_label.configure(text=my_username)
        name_entry.delete(0, "end")

save_btn = CTkButton(
    sidebar_frame, text="Save name", command=save_name_action,
    fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color="white"
)
save_btn.pack(pady=(5, 20), padx=10, fill="x")

changeThemeBtn = CTkButton(
    sidebar_frame, text="Змінити тему", command=CangeTheme,
    fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color="white"
)
changeThemeBtn.pack(side="bottom", pady=20, padx=10)


# головний екран
main_frame = CTkFrame(window, fg_color="transparent")
main_frame.pack(side="left", fill="both", expand=True)

btn_menu = CTkButton(
    main_frame, width=35, text="▶", command=showMenu,
    fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color="white"
)
btn_menu.pack(anchor="nw", padx=10, pady=10)

chat = CTkScrollableFrame(main_frame, fg_color=BG_MAIN, corner_radius=15)
chat.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

bottom_frame = CTkFrame(main_frame, fg_color="transparent")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 15))

typeMas = CTkEntry(
    bottom_frame, placeholder_text="Введіть повідомлення...",
    fg_color=BG_SIDEBAR, text_color=TEXT_MAIN, border_color=BTN_COLOR,
    height=40, corner_radius=10
)
typeMas.pack(side="left", fill="x", expand=True, padx=(0, 5))
typeMas.bind("<Return>", send_mass)

sendMas = CTkButton(
    bottom_frame, width=90, height=40, text="Надіслати", command=send_mass,
    fg_color=BTN_COLOR, hover_color=BTN_HOVER, text_color="white",
    corner_radius=10
)
sendMas.pack(side="right")

def receive_MAS():
    while is_connected == True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            message = data.decode("utf-8")
            window.after(0, lambda m=message: add_mass(m, align="left"))
        except:
            print("З'єднання з сервером розірвано")
            break

if is_connected == True:
    recieve_thread = Thread(target=receive_MAS, daemon=True)
    recieve_thread.start()

window.mainloop()
