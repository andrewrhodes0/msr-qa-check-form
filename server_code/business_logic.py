from anvil.tables import app_tables

CUSUM_WARNING_LEVEL = 100
TP_GIVEN_X_VALUE_FOR_2400_2E_MSR = 1950
TP_GIVEN_Y_VALUE_FOR_2400_2E_MSR = 316
TP_GIVEN_Z_VALUE_FOR_2400_2E_MSR = 542
TP_GIVEN_W_MIN_MOE_FOR_2400_2E_MSR = 1.64
TP_GIVEN_MAX_BELOW_MIN_MOE_FOR_2400_2E_MSR = 1
TP_GIVEN_MAX_FRACTURES_FOR_2400_2E_MSR = 1
TP_GIVEN_NUM_CUSUMS_FOR_OUT_OF_CONTROL_TEST = 6
# How many consecutive 5 pieces CUSUM tests can we have with a fracture in each and remain "In Control"
TP_GIVEN_MAX_FRACTURE_STREAK_FOR_2400_2E_MSR = 2 # 3 in a row == "Out-Of-Control"

def get_control_level_row(status):
    row = app_tables.msr_control_level.get(status=status)
    if row is None:
        raise ValueError(f"No row found for status: {status}")
    return row
# Global variables for caching
in_control_row = get_control_level_row("In Control")
leaving_control_row = get_control_level_row("Leaving Control")
out_of_control_row = get_control_level_row("Out-Of-Control")

def remove_decimal_point_for_cusum(number):
    return int(round(number, 2) * 100)

def calc_cusum(board_moe_values, last_cusum, out_of_control):
    total = 0
    for value in board_moe_values:
        total += remove_decimal_point_for_cusum(float(value))
    average = total * 2
    standard = last_cusum + TP_GIVEN_X_VALUE_FOR_2400_2E_MSR
    cusum = standard - average
    if out_of_control:
        if cusum >= TP_GIVEN_Z_VALUE_FOR_2400_2E_MSR:
            cusum = TP_GIVEN_Z_VALUE_FOR_2400_2E_MSR
    else:
        if cusum >= TP_GIVEN_Y_VALUE_FOR_2400_2E_MSR:
            cusum = TP_GIVEN_Z_VALUE_FOR_2400_2E_MSR
    extra = cusum
    if cusum <= 0:
        cusum = 0
    return (cusum, extra)

# Function to calculate non-sequential statistics
def calculate_non_sequential_stats(boards):
    stats = {
        'num_fractured': [x['fractured'] for x in boards].count(True),
        'avg_moe': sum([x['moe'] for x in boards]) / len(boards),
        'num_too_flexible': sum([x['moe'] < TP_GIVEN_W_MIN_MOE_FOR_2400_2E_MSR for x in boards])
    }
    return stats

# Function to calculate sequential statistics
def calculate_sequential_stats(boards, previous_fracture_streak, previous_cusum, out_of_control):
    num_fractured = [x['fractured'] for x in boards].count(True)
    fracture_streak = previous_fracture_streak + 1 if num_fractured > 0 else 0
    cusum = calc_cusum([x['moe'] for x in boards], previous_cusum, out_of_control)
    stats = {
        'fractured_streak': fracture_streak,
        'cusum': cusum[0],
        'extra': cusum[1]
    }
    return stats

def is_control_regained(msr_checks):
    assert len(msr_checks) % TP_GIVEN_NUM_CUSUMS_FOR_OUT_OF_CONTROL_TEST == 0
    considered_checks = cusum_stats[-TP_GIVEN_NUM_CUSUMS_FOR_OUT_OF_CONTROL_TEST:] # grab the last bunch
    cusum_good = False
    too_flexible_count = 0
    fracture_count = 0
    for msr_check in considered_checks:
        if msr_check['cusum'] <= TP_GIVEN_OUT_OF_CONTROL_MIN_CUSUM:
            cusum_good = True
        too_flexible_count += msr_check['num_too_flexible']
        fracture_count += msr_check['num_fractured']
    
    flex_good = too_flexible_count <= TP_GIVEN_OUT_OF_CONTROL_TEST_MAX_TOO_FLEX_COUNT
    fractures_good = fracture_count <= TP_GIVEN_OUT_OF_CONTROL_TEST_MAX_FRACTURE_COUNT

    return cusum_good and flex_good and fractures_good