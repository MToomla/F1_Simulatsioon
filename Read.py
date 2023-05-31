filename = 'Result.txt'
results = []

def is_fastest_lap(driver_name, fastest_data):
    """Check if it's the fastest lap time and return in formatted form."""
    if driver_name == fastest_data[0]:
        return sec2time(fastest_data[1])  # Format the fastest lap time
    else:
        return ""  # Not the fastest lap time

def sec2time(sec, n_msec=3):
    """Convert seconds to 'D days, HH:MM:SS.FFF'"""
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec + 3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)

if __name__ == '__main__':
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()

    lap_times = {}  # Dictionary to store racer lap times
    sectors_data = [[0, float('inf')], [0, float('inf')], [0, float('inf')]]  # Global sector data [lap_count, best_time]
    best_sector_racers = ["", "", ""]  # Store the racers who achieved the best sector times
    best_lap_time = float('inf')  # Initialize with a very high value
    best_lap_racer = ""  # Store the racer who achieved the best lap time

    mistakes = {}  # Dictionary to store mistakes [racer_name: [mistake_laps]]
    for line in lines[1:]:  # Skip the header line
        data = line.strip().split(';')
        lap_number = int(data[0])
        name = data[1]
        lap_time = float(data[2])
        sector_1 = float(data[3])
        sector_2 = float(data[4])
        sector_3 = float(data[5])
        error = data[6] == 'True'

        if name not in lap_times:
            lap_times[name] = 0
        lap_times[name] += lap_time

        # Update the global sector times if a faster time is found
        if sector_1 < sectors_data[0][1]:
            sectors_data[0][0] = lap_number
            sectors_data[0][1] = sector_1
            best_sector_racers[0] = name
        if sector_2 < sectors_data[1][1]:
            sectors_data[1][0] = lap_number
            sectors_data[1][1] = sector_2
            best_sector_racers[1] = name
        if sector_3 < sectors_data[2][1]:
            sectors_data[2][0] = lap_number
            sectors_data[2][1] = sector_3
            best_sector_racers[2] = name

        if lap_time < best_lap_time:
            best_lap_time = lap_time
            best_lap_racer = name

        if error:
            if name not in mistakes:
                mistakes[name] = []
            mistakes[name].append(lap_number)

    f.close()

    # Sort racers based on total lap times
    sorted_racers = sorted(lap_times.items(), key=lambda x: x[1])

    # Calculate the lap difference between first place and the rest of the racers
    first_place_time = sorted_racers[0][1]
    for racer in sorted_racers:
        name = racer[0]
        total_time = racer[1]
        lap_difference = total_time - first_place_time
        mistake_str = f"{' '.join(str(lap) for lap in mistakes.get(name, []))}" if mistakes.get(name) else ""
        if name == sorted_racers[0][0]:
            if name == best_lap_racer:
                print(f"{name:10} {sec2time(total_time)} [{mistake_str}] {sec2time(best_lap_time)}")
            else:
                print(f"{name:10} {sec2time(total_time)} [{mistake_str}]")
        else:
            if name == best_lap_racer:
                print(f"{name:10} {sec2time(total_time)} +{sec2time(lap_difference)} [{mistake_str}] {sec2time(best_lap_time)}")
            else:
                print(f"{name:10} {sec2time(total_time)} +{sec2time(lap_difference)} [{mistake_str}]")

    print('Sektorite parimad:')
    combined_sector_time = sum(sector[1] for sector in sectors_data[:3])
    for idx, sector in enumerate(sectors_data):
        lap_number = sector[0]
        best_time = sector[1]
        racer_name = best_sector_racers[idx]
        print(f"Sektor {idx+1} {racer_name:10} {sec2time(best_time)}")

    print(f"Unelmate aeg: {sec2time(combined_sector_time)}")
