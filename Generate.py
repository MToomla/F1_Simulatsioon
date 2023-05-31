import random

names = ['Morten', 'Madis', 'Rannar', 'Rasmus', 'Sten']  # Soitjad listis
laps = 10  # Võistluse pikkus
filename = 'Result.txt'
file_header = 'Ring;Nimi;Aeg;Sektor1;Sektor2;Sektor3;Viga\n'  # Faili esimene rida
results = []  # Tühi list ehk kogu võistluse info
minimum = 23  # Väikseim sektori aeg k.a
maximum = 26  # Suurim sektori aeg k.a
fastest_lap = ['Unknown', 999]  # Kiirema ringi sõitja ja aeg
# Kolme sektori kiirem ajad eraldi
three_sectors = [['Unknown', 999], ['Unknown', 999], ['Unknown', 999]]
sectors_data = []  # Ühe ringi kolm sektorit (GLOBAALNE MUUTUJA)


def random_sector_time(mini, maxi):
    """Juhuslik sektori aeg ette antud vahemikus k.a"""
    thousandth = random.randint(0, 999) / 1000
    return random.randint(mini, maxi) + thousandth


def one_lap_time(mini, maxi, driver_name):
    """ Ühele sõitjale ühe ringi aeg (tagastatakse) s.h. sektori ajad (global.) """
    this_total = 0  # Sektorid kokku liidetuna
    sectors_data.clear()  # Tühjenda sektori aegade massiivi. GLOBAALNE
    for z in range(3):  # kolme sektori tegemiseks
        this_sector = random_sector_time(mini, maxi)  # Ühe sektori aeg
        if this_sector < three_sectors[z][1]:  # Kas on uus kiireim sektor
            three_sectors[z][0] = driver_name  # Sektori sõitja nimi
            three_sectors[z][1] = this_sector  # Uus sektori aeg
        this_total += this_sector  # Liidame sektori aja kogu ajale
        sectors_data.append(this_sector)  # Sektori kaup listi
    return this_total  # Tagasta ringi aeg


def is_fastest_lap(driver_name, fastest_data):
    """ Kas on kiireima ringi aeg ja sõitja. Väljastuse juures vaja. """
    if driver_name == fastest_data[0]:
        return sec2time(fastest_data[1])  # Kiireim ring vormindatul kujul
    else:
        return ""  # Pole fiireima ajaga


def sec2time(sec, n_msec=3):
    """Convert seconds to 'D days, HH:MM:SS.FFF'"""
    # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
    if hasattr(sec,'__len__'):
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


if __name__ == '__main__':
    f = open(filename, 'w', encoding='utf-8')  # Ava fail üle kirjutamiseks
    f.write(file_header)  # Kirjuta faili päis
    for name in names:  # Kõokide isikutega tuleb teha allolev tegevus
        lap_times = 0  # Nullime isiku ringide arvu
        errors = []  # Siia tulevad vigased/koperdamiste ringide numbrid
        for lap in range(laps):  # Hakkame sõitjale "ringe tegema"
            error = False  # Pole vigane/koperdatud ring
            if random.randint(0, 9) == 2:  # See on koperdatud ring
                lap_times += one_lap_time(30, 90, 'Unknown')  # Ühe ringi aeg arvutatakse teisiti
                errors.append(lap+1)  # Lisa ringi number listi
                error = True  # See on koperdatud ring
            else:  # See on tavaline ring
                this_lap = one_lap_time(minimum, maximum, name)
                if this_lap < fastest_lap[1]:  # Kui ring on kiirem kui teadaolev
                    fastest_lap[0] = name  # Uue kiirema ringi sõitja nimi
                    fastest_lap[1] = this_lap  # Uue ringi uus rekord
                lap_times += this_lap  # Liidame ringi aja kogu sõidu ajale
            # See on rida mis läheb faili
            line = ';'.join([str(lap+1)] + [name] + [str(sum(sectors_data))] + [str(sectors_data[0])] + [str(sectors_data[1])] + [str(sectors_data[2])] + [str(error)])
            f.write(line + '\n')  # Kirjuta rida faili reavahetusega
        results.append([name, lap_times, errors])  # Kirjuta vajalik info listi
    f.close()  # Sulge fail et saaks hiljem uuesti avada

    results = sorted(results, key=lambda x: x[1])  # Sorteeri list aegade järgi
    # print(results)  # TEST sisu vaatamiseks

    # Näita info konsooli
    for idx, person in enumerate(results):
        if idx > 0:  # Alates teisest isikust
            difference = sec2time(person[1] - results[0][1])
            # Nimi, kogu sõiduaeg, erinevus esimesega, kopertatud ringid, kiireim ringi aeg, kui on
            print(person[0].ljust(10), sec2time(person[1], 3), difference, person[2], is_fastest_lap(person[0], fastest_lap))
        else:  # Ainult esimene isik
            # Nimi, kogu sõiduaeg, kopertatud ringid, kiireim ringi aeg, kui on
            print(person[0].ljust(10), sec2time(person[1], 3), person[2], is_fastest_lap(person[0], fastest_lap))

    print('Sektorite parimad')
    total = 0
    for idx, driver in enumerate(three_sectors):
        total += driver[1]  # Liida sektorite ajad kokku üheks ringiks
        # Näita sektorite infot
        print('Sektor', (idx+1), driver[0].ljust(10), sec2time(driver[1]))
    print('Unelmate ring', sec2time(total))  # Unelmate ring
