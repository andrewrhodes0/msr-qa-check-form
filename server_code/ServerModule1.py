import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

import business_logic as bl


@anvil.server.callable
@anvil.tables.in_transaction
def compute_latest_msr_stats():
    product_sizes = app_tables.product_size.search()
    for product_size in product_sizes:
        ### Skip 'None, No CUSUM' and None product sizes
        product_size_string = product_size['option']
        if product_size_string == None or product_size_string == 'None, No CUSUM':
            continue
        ### Find the latest row in msr_process_status_snapshots according to last_updated that has the same product_size
        latest_snapshot = app_tables.msr_process_control_status_snapshots.search(
            tables.order_by("last_updated", ascending=False),
            product_size=product_size
        )
        ### Create a snapshot row if needed
        if latest_snapshot and len(latest_snapshot) > 0:
            latest_snapshot_row = latest_snapshot[0]
        else:
            latest_snapshot_row = app_tables.msr_process_control_status_snapshots.add_row(
                product_size=product_size
            )
        if not latest_snapshot_row['last_updated'] or not latest_snapshot_row['latest_msr_check_considered']:
            ### New product_size, find the first msr check to start computations
            given_product_msr_checks_ealiest_to_latest = app_tables.msr_checks.search(
                tables.order_by("check_completed_datetime", ascending=True),
                product_size=product_size
            )
            if not given_product_msr_checks_ealiest_to_latest or len(given_product_msr_checks_ealiest_to_latest) < 1:
                ### No checks found, skip this product
                continue
            ### Didn't `continue` means we found a check to start with:
            msr_check_to_consider = given_product_msr_checks_ealiest_to_latest[0]
            latest_snapshot_row['cusum'] = 0
            latest_snapshot_row['fractured_streak'] = 0
        else:
            ### Situation normal, find the next MSR check after the latest_msr_check_considered datetime for the current product
            last_update = latest_snapshot_row['latest_msr_check_considered']['check_completed_datetime']
            msr_checks_after_last_update = app_tables.msr_checks.search(
                tables.order_by("check_completed_datetime", ascending=True),
                check_completed_datetime=q.greater_than(last_update),
                product_size=product_size,
            )
            if not msr_checks_after_last_update or len(msr_checks_after_last_update) < 1:
                ### No new checks found
                continue
            ### Didn't `continue` means we have a new check to work with for this product
            msr_check_to_consider = msr_checks_after_last_update[0]
            
        ### Didn't `continue` so we have an msr check to consider
        snapshot_row_original_vals = dict(latest_snapshot_row)
        
        latest_snapshot_row['latest_msr_check_considered'] = msr_check_to_consider
        latest_snapshot_row['last_updated'] = msr_check_to_consider['check_completed_datetime']

        ### Create a list of boards to work with
        columns = [f'board_{i}' for i in range(1, 6)]
        boards = [msr_check_to_consider[column] for column in columns]
        
        ### Calculate non-sequential stats
        non_seq_stats = bl.calculate_non_sequential_stats(boards)
        for key, value in non_seq_stats.items():
            latest_snapshot_row[key] = value
    
        ### Calculate sequential stats
        seq_stats = bl.calculate_sequential_stats(
            boards,
            snapshot_row_original_vals['fractured_streak'],
            snapshot_row_original_vals['cusum'])
        for key, value in seq_stats.items():
            latest_snapshot_row[key] = value

        ### Use these stats to decide if we are "In Control"
        bl.decide_current_control_level(latest_snapshot_row)

        
    
@anvil.server.callable
def check_admin():
    if anvil.users.get_user():
        return True

@anvil.server.callable
@anvil.tables.in_transaction
def add_msr_calibration_entry(completion_time, calibration_type, moe, outcome, shift, name):
    # Add a new calibration entry to the `msr_calibrations` table
    
    calibration_type_row = app_tables.calibration_type.get(option=calibration_type)
    shift_row = app_tables.shift.get(option=shift)

    # Add the calibration entry with a reference to the calibration_type_row
    calibration_entry = app_tables.msr_calibrations.add_row(
        completion_time=completion_time,
        shift=shift_row,
        calibration_type=calibration_type_row,
        moe=moe,
        outcome_pass=(outcome=='Pass'),
        name=name
    )
    return calibration_entry


@anvil.server.callable
@anvil.tables.in_transaction
def add_msr_check(qa_name, shift, product_size, length, board_data, comments, timestamp=None):
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
    if timestamp is None:
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
def combine_rows_if_needed(row_period_start):
    # Convert row_period_start to a datetime object if it's not already one
    if not isinstance(row_period_start, datetime.datetime):
        row_period_start = anvil.server.parse_date(row_period_start)

    # Retrieve the specified row
    specified_row = app_tables.msr_lumber_production_history.get(period_start=row_period_start)
    if not specified_row:
        return "Specified row not found"

    # Fetch rows older than the specified row
    older_rows = app_tables.msr_lumber_production_history.search(
        tables.order_by("period_start", ascending=False),
        period_start=q.less_than(row_period_start)
    )

    # Find the previous row
    previous_row = None
    for row in older_rows:
        if row['period_start'] < row_period_start:
            previous_row = row
            break

    if not previous_row:
        return None

    # Check for same product_size and time criteria
    if specified_row['product_size'] == previous_row['product_size']:
        if specified_row['period_start'] <= previous_row['period_end'] or \
           (specified_row['period_start'] - previous_row['period_end']).total_seconds() <= 60:

            # Combine rows
            combined_piece_count = previous_row['piece_count'] + specified_row['piece_count']
            combined_period_end = max(previous_row['period_end'], specified_row['period_end'])

            # Update the previous row
            previous_row['piece_count'] = combined_piece_count
            previous_row['period_end'] = combined_period_end

            # Delete the specified row
            specified_row.delete()

    return previous_row['period_start']


@anvil.server.callable
def add_piece_to_history(
    period_start,
    period_end,
    product_size,
    piece_count
):
    product_size_row = app_tables.product_size.get(option=product_size)
    app_tables.msr_lumber_production_history.add_row(period_start=period_start, period_end=period_end, product_size=product_size_row, piece_count=piece_count)
    # Now call the combine function with the period_start of the new row
    combine_message = combine_rows_if_needed(period_start)

    return combine_message

@anvil.server.callable
def get_newest_row():
    # Fetch the newest row based on the period_start
    newest_row = app_tables.msr_lumber_production_history.search(
        tables.order_by("period_start", ascending=False))[:1]
    return next(newest_row, None)

@anvil.server.callable
def get_next_oldest_row(current_period_end):
    # Convert current_period_end to a datetime object if it's not already one
    if not isinstance(current_period_end, datetime.datetime):
        current_period_end = anvil.server.parse_date(current_period_end)

    # Search for the next oldest row
    next_rows = app_tables.msr_lumber_production_history.search(
        tables.order_by("period_start", ascending=True),
        period_start=q.greater_than(current_period_end)
    )
    
    # Find the next row
    next_row = None
    for row in next_rows:
        if row['period_start'] > current_period_end:
            next_row = row
            break
    return next_row

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



