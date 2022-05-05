import pygetwindow as gw
import pywinauto
import time

var = gw.getWindowsWithTitle('Gersang')[0] # Gersang 창 

var1 = gw.getWindowsWithTitle('Gersang')[1] # Gersang 창 

var2 = gw.getWindowsWithTitle('Gersang')[2] # Gersang 창 

var3 = gw.getWindowsWithTitle('Gersang')[3] # Gersang 창 

print(var)
print(var1)
print(var2)

if var.isActive == False:
    pywinauto.application.Application().connect(handle=var._hWnd).top_window().set_focus()

var2.activate()