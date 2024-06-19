from time import sleep
import PySimpleGUI as sg
from constants import CANCEL, WEIGHT, WHITE, GREEN
from modules.types import TrashType

sg.theme_background_color(WHITE)
sg.theme_text_color(GREEN)

def VPush():
    return sg.VPush(background_color=WHITE)

def Push():
    return sg.Push(background_color=WHITE)


class UIDriver:
    def __init__(self, controller):
        # Define layouts
        def screen1_layout():
            return [
                [VPush()],
                [Push(), sg.Text('Ready', size=(15, 1), justification='center', font=('Helvetica', 25), background_color=WHITE), Push()],
                [VPush()]
            ]   

        def screen2_layout():
            return [
                [VPush()],
                [Push(),
                    sg.Text('', size=(15, 1), justification='center', font=('Helvetica', 24), key=WEIGHT, background_color=WHITE),
                    Push()],
                [VPush()],
                [Push(), 
                    sg.Text('Which one is it?', size=(15, 1), justification='center', font=('Helvetica', 16), background_color=WHITE),
                    Push()],
                [VPush()],
                [Push(),
                    sg.Button('PMD', size=(10, 2), button_color=GREEN, enable_events=True, key=TrashType.PMD),
                    sg.Button('Paper', size=(10, 2), button_color=GREEN, enable_events=True, key=TrashType.PAPER),
                    sg.Button('Waste', size=(10, 2), button_color=GREEN, enable_events=True, key=TrashType.WASTE), 
                    Push()],
                [VPush()],
                [Push(), sg.Button('Cancel', button_color="#e23a08", enable_events=True, key=CANCEL), Push()],
                [VPush()],
            ]

        def screen3_layout():
            return [
                [VPush()],
                [Push(), sg.Text('Saved.', size=(15, 1), justification='center', font=('Helvetica', 20), background_color=WHITE), Push()],
                [Push(), sg.Text('Thank You', size=(15, 1), justification='center', font=('Helvetica', 14), background_color=WHITE), Push()],
                [VPush()],
            ]   

        self.layouts = {
            1: screen1_layout,
            2: screen2_layout,
            3: screen3_layout
        }
        
        self.__controller = controller 
        self.__stage = 1
        self.__recorded_weight = None
        self.window = sg.Window('Scale UI', self.layouts[self.__stage](), size=(800,480), no_titlebar=True, grab_anywhere=True, element_justification='c', finalize=True)

    def __update_weight_label(self, new_weight):
        self.window[WEIGHT].update(f'Weight: {new_weight:.3f} kg')

    def __load_layout(self, action = None):
        new_window = sg.Window('Scale UI', self.layouts[self.__stage](), size=(800,480), no_titlebar=True, grab_anywhere=True, element_justification='c', finalize=True)
        new_window.Shown = True
        self.window.close()
        self.window = new_window
        if action is not None:
            action()

    def __handle_stage_one(self):
        self.__recorded_weight = None
        weight = self.__controller.get_weight()  # Replace with actual weight retrieval logic
        if weight > 0.005:
            # Once weight condition is met, switch to layout 2
            self.__recorded_weight = weight
            self.__stage = 2
            self.__load_layout()
            self.__update_weight_label(weight)
    
    def __handle_stage_two(self, event):
        if isinstance(event, TrashType):
            self.__controller.record_weighing((event, self.__recorded_weight))
            self.__stage = 3
            self.__load_layout()
        
        elif event == CANCEL:
            self.__stage = 1
            self.__load_layout()
            
            

    def __handle_stage_three(self):
        sleep(2)
        self.__stage = 1
        self.__load_layout()

        


    def start(self):
        # Main event loop
        while True:
            event, _ = self.window.read(timeout=50)  # 100 ms timeout for polling
            if event == sg.WIN_CLOSED:
                break

            if self.__stage == 1:
                self.__handle_stage_one()
            elif self.__stage == 2:
                self.__handle_stage_two(event)
            elif self.__stage == 3:
               self.__handle_stage_three()


