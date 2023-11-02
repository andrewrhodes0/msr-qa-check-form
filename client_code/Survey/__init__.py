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
    shift = self.age_dropdown.selected_value
    frequency = self.radio_button_1.get_group_value()
    methods = [box.text for box in self.check_boxes if box.checked == True]
    comments = self.comment_area.text
    
    if age and frequency and methods:
      anvil.server.call('add_responses', age, frequency, methods, comments)
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
