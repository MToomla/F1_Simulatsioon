import random

names = ['Morten', 'Madis', 'Rannar', 'Rasmus', 'Sten']
laps = 10
filename = 'Result.txt'
file_header = 'Ring;Nimi;Aeg;Sektor1;Sektor2;Sektor3;Viga\n'
results = []
minimum = 23
maximum = 26
fastest_lap = ['Unknown', 999]
three_sectors = [['Unknown', 999], ['Unknown', 999], ['Unknown', 999]]
sectors_data = []


def random_sector_time(mini, maxi):
    thousandth = random.randint(0, 999) / 1000
    return random.randint(mini, maxi) + thousandth


def one_lap_time(mini, maxi, driver_name):
    this_total = 0
    sectors_data.clear()
    for z in range(3):
        this_sector = random_sector_time(mini, maxi)
        if this_sector < three_sectors[z][1]:
            three_sectors[z][0] = driver_name
            three_sectors[z][1] = this_sector
        this_total += this_sector
        sectors_data.append(this_sector)
    return this_total


def is_fastest_lap(driver_name, fastest_data):
    if driver_name == fastest_data[0]:
        return sec2time(fastest_data[1])
    else:
        return ""


def sec2time(sec, n_msec=3):
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)


def write_results_to_file(filename, header, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(header)
        for entry in data:
            lap_num = entry[0]
            name = entry[1]
            lap_time = entry[2]
            sector1 = entry[3][0]
            sector2 = entry[3][1]
            sector3 = entry[3][2]
            error = entry[4]
            line = f"{lap_num};{name};{sec2time(lap_time)};{sec2time(sector1)};{sec2time(sector2)};{sec2time(sector3)};{error}\n"
            file.write(line)


if __name__ == '__main__':
    f = open(filename, 'w', encoding='utf-8')
    f.write(file_header)
    for name in names:
        lap_times = 0
        errors = []
        for lap in range(laps):
            error = False
            if random.randint(0, 9) == 2:
                lap_times += one_lap_time(30, 90, 'Unknown')
                errors.append(lap + 1)
                error = True
            else:
                this_lap = one_lap_time(minimum, maximum, name)
                if this_lap < fastest_lap[1]:
                    fastest_lap[0] = name
                    fastest_lap[1] = this_lap
                lap_times += this_lap
            line = f'{lap + 1};{name};{sec2time(sum(sectors_data))};{sec2time(sectors_data[0])};{sec2time(sectors_data[1])};{sec2time(sectors_data[2])};{error}\n'
            f.write(line)
        results.append([lap + 1, name, lap_times, sectors_data.copy(), errors])
    f.close()

    results = sorted(results, key=lambda x: x[2])

    for idx, person in enumerate(results):
        if idx > 0:
            difference = sec2time(person[2] - results[0][2])
            print(person[1].ljust(10), sec2time(person[2], 3), difference, person[4], is_fastest_lap(person[1], fastest_lap))
        else:
            print(person[1].ljust(10), sec2time(person[2], 3), person[4], is_fastest_lap(person[1], fastest_lap))

    print('Sektorite parimad')
    total = 0
    for idx, driver in enumerate(three_sectors):
        total += driver[1]
        print('Sektor', (idx+1), driver[0].ljust(10), sec2time(driver[1]))
    print('Unelmate ring', sec2time(total))

    write_results_to_file(filename, file_header, results)
