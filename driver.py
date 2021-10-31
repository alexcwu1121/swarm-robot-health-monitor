"""
driver.py:  Driver for SRHMD.
TODOS:      Depends on what other things we will implement.
Description:This file will mainly be responsive for calling out GUI for now.
"""

import display
import interface as inter
import threading

def main():
    g = inter.Gui()
    
    #wait for the user to pick a file
    while(g.get_config() == ''):
        g.refresh_gui()
    
    my_rec = display.display_base(g.get_config())
    
    dis_thread = threading.Thread(target=my_rec.run_display,args=())
    
    dis_thread.start()
    
    while(True):
        g.refresh_gui()
        for bot in my_rec.get_state():
            g.update_display(bot)
        
    
    #update_display

if __name__ == "__main__":
    main()
    