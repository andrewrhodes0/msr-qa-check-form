from ._anvil_designer import SurveyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Survey(SurveyTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def submit_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        qa_name = self.text_box_qa_name.text
        shift = self.radio_button_shift_first.get_group_value()
        product_size = self.radio_button_2x4_product_size.get_group_value()
        length = self.radio_button_16ft_length.get_group_value()
        check_meta_data_ok = qa_name and shift and product_size and length
        board_1_moisture = self.text_box_board_1_moisture.text
        board_1_moe = self.text_box_board_1_moe.text
        board_1_fractured = self.radio_button_board_1_fractured_yes.get_group_value()
        if board_1_fractured == "Yes":
            board_1_fb_value = self.text_box_board_1_fb_value.text
        else:
            board_1_fb_value = "N/A"
        board_1_data_ok = board_1_moisture and board_1_moe and board_1_fractured and board_1_fb_value
        board_2_moisture = self.text_box_board_2_moisture.text
        board_2_moe = self.text_box_board_2_moe.text
        board_2_fractured = self.radio_button_board_2_fractured_yes.get_group_value()
        if board_2_fractured == "Yes":
            board_2_fb_value = self.text_box_board_2_fb_value.text
        else:
            board_2_fb_value = "N/A"
        board_2_data_ok = board_2_moisture and board_2_moe and board_2_fractured and board_2_fb_value
        board_3_moisture = self.text_box_board_3_moisture.text
        board_3_moe = self.text_box_board_3_moe.text
        board_3_fractured = self.radio_button_board_3_fractured_yes.get_group_value()
        if board_3_fractured == "Yes":
            board_3_fb_value = self.text_box_board_3_fb_value.text
        else:
            board_3_fb_value = "N/A"
        board_3_data_ok = board_3_moisture and board_3_moe and board_3_fractured and board_3_fb_value
        board_4_moisture = self.text_box_board_4_moisture.text
        board_4_moe = self.text_box_board_4_moe.text
        board_4_fractured = self.radio_button_board_4_fractured_yes.get_group_value()
        if board_4_fractured == "Yes":
            board_4_fb_value = self.text_box_board_4_fb_value.text
        else:
            board_4_fb_value = "N/A"
        board_4_data_ok = board_4_moisture and board_4_moe and board_4_fractured and board_4_fb_value
        board_5_moisture = self.text_box_board_5_moisture.text
        board_5_moe = self.text_box_board_5_moe.text
        board_5_fractured = self.radio_button_board_5_fractured_yes.get_group_value()
        if board_5_fractured == "Yes":
            board_5_fb_value = self.text_box_board_5_fb_value.text
        else:
            board_5_fb_value = "N/A"
        board_5_data_ok = board_5_moisture and board_5_moe and board_5_fractured and board_5_fb_value
        comments = self.comment_area.text

        if check_meta_data_ok and board_1_data_ok and board_2_data_ok and board_3_data_ok and board_4_data_ok and board_5_data_ok:
            anvil.server.call(
                'add_check',
                qa_name,
                shift,
                product_size,
                length,
                board_1_moisture,
                board_1_moe,
                board_1_fractured,
                board_1_fb_value,
                board_2_moisture,
                board_2_moe,
                board_2_fractured,
                board_2_fb_value,
                board_3_moisture,
                board_3_moe,
                board_3_fractured,
                board_3_fb_value,
                board_4_moisture,
                board_4_moe,
                board_4_fractured,
                board_4_fb_value,
                board_5_moisture,
                board_5_moe,
                board_5_fractured,
                board_5_fb_value,
                comments
            )
            alert("Thank you for submitting feedback!")
            get_open_form().content_panel.clear()
            get_open_form().content_panel.add_component(Survey(), full_width_row=True)
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
