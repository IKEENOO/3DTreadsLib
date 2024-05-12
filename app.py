from tkinter import *
from tkinter import ttk


if __name__ == '__main__':
  root = Tk()
  root.title('Библиотека 3D резьб')
  root.iconbitmap(default="favicon.ico")
  end_conditions = ["Задать длину", "На всю длину"]
  combobox = ttk.Combobox(values=end_conditions)
  combobox.current(0)
  combobox.pack(anchor=NW, padx=6, pady=6)
  entry = ttk.Entry(root, width=23)
  entry.pack(anchor=NW, padx=6, pady=6)
  entry.insert(0, "10.0 мм")
  
  clicks = 0
  
  def click_button():
    label["text"] = entry.get()   

  
  btn = ttk.Button(text="Click Me", command=click_button)
  btn.pack(anchor=NW, padx=6, pady=6)
  label = ttk.Label()
  label.pack(anchor=NW, padx=6, pady=6)
  root.mainloop()