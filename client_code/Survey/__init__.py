from ._anvil_designer import SurveyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import document

class Survey(SurveyTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
    def submit_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Collect metadata
        qa_name = self.text_box_qa_name.text
        shift = self.radio_button_shift_first.get_group_value()
        product_size = self.radio_button_2x4_product_size.get_group_value()
        length = self.radio_button_16ft_length.get_group_value()
    
        # Collect board data
        board_data = []
        for i in range(1, 6):  # Assuming you have 5 boards
            moisture = getattr(self, f'text_box_board_{i}_moisture').text
            moe = getattr(self, f'text_box_board_{i}_avg_moe').text
            fractured = getattr(self, f'radio_button_board_{i}_fractured_yes').get_group_value()
            fb_value = getattr(self, f'text_box_board_{i}_fb_value').text if fractured == "Yes" else "N/A"
    
            board_data.append({
                'moisture': moisture,
                'moe': moe,
                'fractured': fractured,
                'fb_value': fb_value
            })
    
        # Collect comments
        comments = self.comment_area.text
    
        # Check if all data is okay to send
        check_meta_data_ok = all([qa_name, shift, product_size, length])
        check_board_data_ok = all([all(board.values()) for board in board_data])
        
pass        if check_meta_data_ok and check_board_data_ok:
            # Call the server function
            anvil.server.call('add_msr_check', qa_name, shift, product_size, length, board_data, comments)
            open_form('FormSubmitted')
            #get_open_form().content_panel.clear()
            #get_open_form().content_panel.add_component(Survey(), full_width_row=True)
            #document.body.scrollTop = 0  # For Safari
            #document.documentElement.scrollTop = 0  # For Chrome, Firefox, IE and Opera
        else: alert("Please fill out required fields")


    def radio_button_board_1_fractured_no_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_1_fb_value.visible = False
        pass

    def radio_button_board_1_fractured_yes_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_1_fb_value.visible = True
        pass

    def radio_button_board_2_fractured_no_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_2_fb_value.visible = False
        pass

    def radio_button_board_2_fractured_yes_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_2_fb_value.visible = True
        pass

    def radio_button_board_3_fractured_no_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_3_fb_value.visible = False
        pass

    def radio_button_board_3_fractured_yes_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_3_fb_value.visible = True
        pass

    def radio_button_board_4_fractured_no_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_4_fb_value.visible = False
        pass

    def radio_button_board_4_fractured_yes_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_4_fb_value.visible = True
        pass

    def radio_button_board_5_fractured_no_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_5_fb_value.visible = False
        pass

    def radio_button_board_5_fractured_yes_clicked(self, **event_args):
        """This method is called when this radio button is selected"""
        self.column_panel_board_5_fb_value.visible = True
        pass
