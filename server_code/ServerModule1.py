import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime
    
@anvil.server.callable
def check_admin():
    if anvil.users.get_user():
        return True

@anvil.server.callable
@anvil.tables.in_transaction
def add_msr_check(qa_name, shift, product_size, length, board_data, comments):
    # First, add board details to the `boards` table
    board_entries = []
    for board in board_data:
        # Assuming `board` is a dictionary with keys: 'moisture', 'moe', 'fractured', 'fb_value'
        fractured = (board['fractured'] == "Yes")
        board_entry = app_tables.boards.add_row(
            moisture=board['moisture'],
            moe=board['moe'],
            fractured=fractured,
            fb_value=board['fb_value'] if fractured else None
        )
        board_entries.append(board_entry)
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    
    shift_row = app_tables.shift.get(option=shift)  # Assuming 'shifts' is the table name and 'option' is the column name
    if shift_row:
        shift_row['num_checks'] = (shift_row['num_checks'] or 0) + 1

    product_size_row = app_tables.product_size.get(option=product_size)
    if product_size_row:
        product_size_row['num_checks'] = (product_size_row['num_checks'] or 0) + 1

    length_row = app_tables.length.get(option=length)
    if length_row:
        length_row['num_checks'] = (length_row['num_checks'] or 0) + 1

    # Next, add the check to the `checks` table with references to the board entries
    check_entry = app_tables.msr_checks.add_row(
        check_completed_datetime=timestamp,
        qa_name=qa_name,
        shift=shift_row,
        product_size=product_size_row,
        length=length_row,
        board_1=board_entries[0],
        board_2=board_entries[1],
        board_3=board_entries[2],
        board_4=board_entries[3],
        board_5=board_entries[4],
        comments=comments
    )
    return check_entry

@anvil.server.callable
def add_piece_to_history(
    period_start,
    period_end,
    product_size,
    piece_count
):
    product_size_row = app_tables.product_size.get(option=product_size)
    app_tables.msr_lumber_production_history.add_row(period_start=period_start, period_end=period_end, product_size=product_size_row, piece_count=piece_count)

@anvil.server.callable
def get_total_responses():
    return len(app_tables.msr_checks.search())

@anvil.server.callable
def get_tables():
    shift = app_tables.shift.search()
    product_size = app_tables.product_size.search()
    length = app_tables.length.search()
    return [shift, product_size, length]

@anvil.server.background_task
def hello_world():
    print('hello world')
    return True



