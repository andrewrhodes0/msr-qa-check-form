import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def check_admin():
    if anvil.users.get_user():
        return True

@anvil.server.callable
@anvil.tables.in_transaction
def add_msr_check(
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
    comments,
):
    shift_row = app_tables.shifts.get(option=shift)  # Assuming 'shifts' is the table name and 'option' is the column name
    if shift_row:
        shift_row['num_checks'] = (shift_row['num_checks'] or 0) + 1

    product_size_row = app_tables.product_sizes.get(option=product_size)  # Adjust the table and column name accordingly
    if product_size_row:
        product_size_row['num_checks'] = (product_size_row['num_checks'] or 0) + 1

    length_row = app_tables.lengths.get(option=length)  # Adjust the table and column name accordingly
    if length_row:
        length_row['num_checks'] = (length_row['num_checks'] or 0) + 1
        
    app_tables.msr_checks.add_row(
        qa_name=qa_name,
        shift=shift_row,
        product_size=product_size_row,
        length=length_row,
        board_1_moisture=board_1_moisture,
        board_1_moe=board_1_moe,
        board_1_fractured=board_1_fractured,
        board_1_fb_value=board_1_fb_value,
        board_2_moisture=board_2_moisture,
        board_2_moe=board_2_moe,
        board_2_fractured=board_2_fractured,
        board_2_fb_value=board_2_fb_value,
        board_3_moisture=board_3_moisture,
        board_3_moe=board_3_moe,
        board_3_fractured=board_3_fractured,
        board_3_fb_value=board_3_fb_value,
        board_4_moisture=board_4_moisture,
        board_4_moe=board_4_moe,
        board_4_fractured=board_4_fractured,
        board_4_fb_value=board_4_fb_value,
        board_5_moisture=board_5_moisture,
        board_5_moe=board_5_moe,
        board_5_fractured=board_5_fractured,
        board_5_fb_value=board_5_fb_value,
        comments=comments


@anvil.server.callable
def get_total_responses():
    return len(app_tables.responses.search())

@anvil.server.callable
def get_tables():
    ages = app_tables.age.search()
    frequency = app_tables.frequency.search()
    methods = app_tables.method.search()
    ratings = app_tables.ratings.search()
    return [ages, frequency, methods, ratings]

@anvil.server.background_task
def hello_world():
    print('hello world')
    return True



