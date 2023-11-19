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

def remove_decimal_point_for_cusum(number):
    return int(round(number, 2) * 100)

def calc_cusum(board_moe_values, last_cusum):
    total = 0
    for value in board_moe_values:
        total += remove_decimal_point_for_cusum(float(value))
    average = total * 2
    standard = last_cusum + TP_GIVEN_X_VALUE_FOR_2400_2E_MSR
    cusum = standard - average
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
def calculate_sequential_stats(boards, previous_fracture_streak, previous_cusum):
    num_fractured = [x['fractured'] for x in boards].count(True)
    fracture_streak = previous_fracture_streak + 1 if num_fractured > 0 else 0
    cusum = calc_cusum([x['moe'] for x in boards], previous_cusum)
    stats = {
        'fractured_streak': fracture_streak,
        'cusum': cusum[0],
        'extra': cusum[1]
    }
    return stats

def decide_current_control_level(process_snapshot_row):
    if process_snapshot_row['cusum'] >= CUSUM_WARNING_LEVEL:
        process_snapshot_row['']
        