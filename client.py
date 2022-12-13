from tkinter import *                                  
from tkinter import ttk
import socket             

   
#สร้างหน้าต่างเกมและเชื่อมต่อSocket
def newgame(): 
    def reset():
        game_win.destroy()
        newgame()

    #ข้อมูลที่ใช้เชื่อมต่อSocket
    def check():
        user_data = user_entry.get()                 
        client.send(user_data.encode())            
        server_data = client.recv(2048).decode()     
        user_entry.delete(0,END)
        
        if "Lost" in server_data:                                                    
            canvas_game.itemconfig(server_print, text="You Lost")
            buttonSubmit.place_forget()
            # button_newgame = Button(game_win, text="N E W  G A M E", height=2, width=26, state=NORMAL, font="Forte 16", command=reset)
            # button_newgame.place(x=400, y=390, anchor="center")
            answer = server_data[0:2]
            print(f"Answer is {answer}")
            
        elif "Win" in server_data:                                                     
            canvas_game.itemconfig(server_print, text="You  Won")
            turn = server_data[-1]
            canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
            buttonSubmit.place_forget()
            button_newgame = Button(game_win, text="N E W  G A M E", height=2, width=26, state=NORMAL, font="Forte 16", command=reset)
            button_newgame.place(x=400, y=390, anchor="center")
            score = user_name+" "+turn+"\n\n"
            f = open("scoreBoard.txt", "a") # 'a' เป็นการ append ค่า การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
            f.write(score)            #สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
            f.close()
            
        elif "High" in server_data:                                                  
            canvas_game.itemconfig(server_print, text="Too High")
            turn = server_data[-1]
            canvas_game.itemconfig(attempt, text=("Attempt: "+turn))
            
        elif "Low" in server_data:                                                      
            canvas_game.itemconfig(server_print, text="Too Low")
            turn = server_data[-1]
            canvas_game.itemconfig(attempt, text=("Attempt: " + turn))
            
        else:
            canvas_game.itemconfig(server_print, text=server_data)

    button_newgame["state"] = "disable"                                              
    button_score["state"] = "disable"                                                         

    game_win = Toplevel(mainGUI)   #สร้างหน้าต่างแยกขึ้นมา
    game_win.geometry("800x538+350+200")
    game_win.resizable(0, 0)
    game_win.title("G A M E")
    canvas_game = Canvas(game_win)   #เป็นการวาดรูปสร้างออปเจ็กขึ้นมาทับที่game_win                             
    canvas_game.pack(fill="both", expand=True)                             
    canvas_game.create_image(0, 0, image=bg_game, anchor="nw")         
    canvas_game.create_oval(50, 120, 750, 450, fill="#191970", outline='#edc0fc')

    canvas_game.create_text(400, 50, text="Guess the Number", fill="#edc0fc", font="Forte 38", justify="center", anchor="n")
    attempt = canvas_game.create_text(60, 130, text="Attempt: 1", fill="#edc0fc", font="Forte 18", justify="center", anchor="nw")
    canvas_game.create_text(60, 160, text=("Player: "+user_name), fill="#edc0fc", font="Forte 18", anchor="nw")
    server_print = canvas_game.create_text(400, 180, text="Guess Number in range\n1-20", fill="white", font="Forte 34", justify="center", anchor="n") #Server output

    user_entry = Entry(game_win, width=4, font="Forte 26 bold", justify="center", bg="#df91fa") #ผู้ใช้กรอกเลขที่ผู้ใช้ต้องการค่าที่ผู้ใช้เดา
    canvas_game.create_window(400, 300,  window=user_entry)

    buttonSubmit = Button(game_win, text="G U E S S", height=2, width=26, state=NORMAL, font="Forte 16", command=check) #Submit Button
    button_exit_score = Button(game_win, text="E X I T", fg='red', height=2, width=26, command=lambda:buttonExit(game_win), state=NORMAL, font="Forte 16") #Exit Button
    
    buttonSubmit.place(x=400, y=390, anchor="center")
    button_exit_score.place(x=400, y=490, anchor="center")  

    serverip = 'localhost'
    port = 5555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
    try:
        client.connect((serverip, port))                               
        print(f"[Connected] Client connected to server at {serverip}:{port}")
    except:
        print('ERROR!')
        buttonExit(game_win)


def buttonExit(window):   
    window.destroy()                                    
    # mainGUI.deiconify()                 #เปิดmainGUIอีกครั้ง                         
    button_newgame["state"] = "normal"  
    button_score["state"] = "normal"   
    
    
def score_board():                             
    # mainGUI.iconify()                          
    f = open("scoreBoard.txt", "r")      #อ่านscore board จากไฟล์
    scoreList = f.read()
    f.close()
    
    score_window = Toplevel(mainGUI)
    score_window.title("L E A D E R   B O A R D")
    score_window.geometry("400x700+10+20")
    score_window.resizable(0, 0)
    canvas_score = Canvas(score_window)      
    # bg_score = PhotoImage(file="score board.png")    
    canvas_score.pack(fill="both", expand=True)                          
    canvas_score.create_image(0, 0, image=bg_score, anchor="nw")     

    canvas_score.create_text(200, 80, text="L E A D E R   B O A R D", fill="white", font="Forte 30 bold",justify="center")
    canvas_score.create_text(200, 120, text=scoreList,fill="white", font="Forte 18", justify="center", anchor="n")
    button_exit_score = Button(score_window, text="E X I T", fg='red', height=2, width=26,command=lambda:buttonExit(score_window), state=NORMAL, font="Forte 16")
    button_exit_score.place(x=200, y=580, anchor="center")



def login():                                  
    # mainGUI.iconify()                        
    def start_game():
        global user_name
        user_name = enter_name.get()           
        print(user_name)
        login_window.destroy()
        newgame()
    
    login_window = Toplevel(mainGUI)
    login_window.title("L O G I N")
    login_window.geometry("550x260+350+200")
    login_window.resizable(0, 0)
    canvas_login = Canvas(login_window)
    canvas_login.pack(fill="both", expand=True)
    canvas_login.create_image(0, 0, image=bg_login, anchor="nw")

    canvas_login.create_text(270, 50, text="Enter Your Name",fill="yellow", font="Forte 26 bold",justify="center")
    canvas_login.create_text(272, 50, text="Enter Your Name",fill="red", font="Forte 26 bold",justify="center")
    enter_name = Entry(canvas_login, width=16, font="Forte 26 bold", justify="center", bg="#df91fa") #ช่องที่ให้ผู้ใช้กรอกชื่อ
    canvas_login.create_window(270, 100, window=enter_name)
    
    start_button = Button(login_window, text="S T A R T", height=1, width=20, command=start_game, state=NORMAL, font="Forte 16")
    button_exit_login = Button(login_window, text="E X I T",fg = "red", height=1, width=20, command=lambda:buttonExit(login_window), state=NORMAL, font="Forte 16")
    
    start_button.place(x=270, y=160, anchor="center")
    button_exit_login.place(x=270, y=200, anchor="center")

                                                                                                                                   
mainGUI = Tk()                                                           
mainGUI.geometry("640x480+300+200")                                              
mainGUI.resizable(0, 0)                                           #ไม่่สามารถปรับหน้าจอเองได้
mainGUI.title("G U E S S     N U M B E R")                           

user_name = ""                                                    #User name
bg_main = PhotoImage(file="menu.png")                              
bg_score = PhotoImage(file="score board.png")                             
bg_login = PhotoImage(file="login.png")                           
bg_game = PhotoImage(file="game.png")                               

canvas_main = Canvas(mainGUI)                                     #เป็นการวาดรูปสร้างออปเจ็กขึ้นมาทับที่mainGUI            
canvas_main.pack(fill="both", expand=True)                                
canvas_main.create_image(0, 0, image=bg_main, anchor="nw")                

canvas_main.create_text(320, 80, text="G u e s s  t h e  N u m b e r", fill="blue", font="Forte 45 bold", justify="center", anchor="n")
canvas_main.create_text(323, 80, text="G u e s s  t h e  N u m b e r", fill="red", font="Forte 45 bold", justify="center", anchor="n")

button_newgame = Button(canvas_main, text="N E W   G A M E", height=2, width=26, command=login, state=NORMAL, font="Forte 16") #New Game Button
button_score = Button(canvas_main, text="L E A D E R   B O A R D", height=2, width=26, command=score_board, state=NORMAL, font="Forte 16")   #Score Button
button_exit = Button(canvas_main, text="E X I T", height=2, width=26, command= mainGUI.destroy, state=NORMAL, font="Forte 16",fg="red")   #Exit Button

button_newgame.place(x=320, y=210, anchor="center")      
button_score.place(x=320, y=290, anchor="center")        
button_exit.place(x=320, y=380, anchor="center")  
      
mainGUI.mainloop()       