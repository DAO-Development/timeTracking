import datetime

from reportlab.lib.colors import black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# 612х792
def print_profile_form(profile):
    print(profile)
    my_canvas = canvas.Canvas("media/users/" + profile['auth_user_id']['email'] + ".pdf")
    pdfmetrics.registerFont(TTFont('Arial-Bold', './static/fonts/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial', './static/fonts/arialmt.ttf'))
    my_canvas.setLineWidth(.5)
    my_canvas.setFont('Arial-Bold', 12)
    my_canvas.drawString(285, 800, "Анкета данных")
    my_canvas.setFont('Helvetica', 9)
    my_canvas.drawString(310, 787, datetime.date.today().strftime("%d.%m.%Y"))
    my_canvas.drawImage('project-vue/src/assets/logo.png', 30, 792, width=106, height=40)
    my_canvas.drawString(30, 792, "info@asprofile.fi / +358 40 517 1212")
    my_canvas.setFont('Helvetica', 10)
    my_canvas.drawString(120, 702, "VALTTIKORTTI")
    my_canvas.drawString(400, 702, "ID")

    grid_rows = []
    titles = ['Имя и Фамилия', 'Гражданство', 'Дата рождения', 'Соц код в своей стране',
              'Финский henkilötunnus', 'Адрес в своей стране', 'Адрес в Финляндии', 'Тел. в с своей стране',
              'Тел. в Финляндии', 'Е-майл', 'Номер счета в банке', 'Veronumero (налоговый nr)', 'Свой автомобиль?',
              'Свой инструмент?', 'Английский язык', 'Эстонский язык', 'Финский язык', 'Русский язык',
              'Другой язык (какой?)', 'Основная специальность', 'Что умеете делать?']
    for i in range(1, 23):
        grid_rows.append(300 + 15 * i)
    my_canvas.grid([30, 185, 582], grid_rows)
    for i in range(len(grid_rows) - 1):
        my_canvas.setFont('Helvetica', 8)
        my_canvas.drawString(35, grid_rows[-(i + 2)] + 4, str(i + 1))
        my_canvas.setFont('Arial-Bold', 9)
        my_canvas.drawString(55, grid_rows[-(i + 2)] + 4, titles[i])

    my_canvas.setFillColor('#c0c0c0')
    my_canvas.rect(30, 300, 552, 15, stroke=0, fill=1)
    my_canvas.grid([30, 168, 306, 444, 582], [300, 315])
    my_canvas.setFillColor(black)
    grey_table = ['Ботинки', 'Куртка', 'Штаны', 'Футболка']
    for i in range(len(grey_table)):
        my_canvas.drawString(40 + 138 * i, 304, grey_table[i])

    card_grid = []
    my_canvas.setFont('Helvetica', 8)
    for i in range(6):
        card_grid.append(25 + 55 * i)
    my_canvas.grid([30, 190, 370], card_grid)
    for i in range(len(card_grid) - 1):
        my_canvas.drawString(35, card_grid[-(i + 2)] + 25, str(i + 22))
        my_canvas.drawImage('project-vue/src/assets/image' + str(i + 22) + '.PNG', 55, card_grid[-(i + 2)] + 5,
                            width=70, height=45)

    my_canvas.grid([370, 582], [25, 300])

    my_canvas.setFont('Arial', 9)
    my_canvas.drawString(200, grid_rows[-2] + 4, profile['lastname'] + ' ' + profile['name'])
    my_canvas.drawString(200, grid_rows[-3] + 4, profile['citizenship'])
    my_canvas.drawString(200, grid_rows[-4] + 4, profile['birthdate'])
    my_canvas.drawString(200, grid_rows[-5] + 4, profile['social_code_own'])
    my_canvas.drawString(200, grid_rows[-6] + 4, profile['social_code_fin'])
    my_canvas.drawString(200, grid_rows[-7] + 4,
                         profile['address_own']['country'] + '' + profile['address_own']['city'] + ' ' +
                         profile['address_own']['street'] + ' ' + profile['address_own']['house']
                         if profile['address_own'] is not None else '')
    my_canvas.drawString(200, grid_rows[-7] + 4,
                         profile['address_fin']['city'] + ' ' + profile['address_fin']['street'] + ' ' +
                         profile['address_fin']['house'] if profile['address_fin'] is not None else '')
    my_canvas.drawString(200, grid_rows[-9] + 4, profile['phone'])
    my_canvas.drawString(200, grid_rows[-10] + 4, profile['phone_fin'])
    my_canvas.drawString(200, grid_rows[-11] + 4, profile['auth_user_id']['email'])
    my_canvas.drawString(200, grid_rows[-12] + 4, profile['bank_account'])
    my_canvas.drawString(200, grid_rows[-13] + 4, profile['tax_number'])
    my_canvas.drawString(200, grid_rows[-14] + 4, 'есть' if profile['auto'] else 'нет')
    my_canvas.drawString(200, grid_rows[-15] + 4, 'есть' if profile['tool'] else 'нет')
    my_canvas.drawString(200, grid_rows[-16] + 4, 'да' if profile['english'] else 'нет')
    my_canvas.drawString(200, grid_rows[-17] + 4, 'да' if profile['estonian'] else 'нет')
    my_canvas.drawString(200, grid_rows[-18] + 4, 'да' if profile['finnish'] else 'нет')
    my_canvas.drawString(200, grid_rows[-19] + 4, 'да' if profile['russian'] else 'нет')
    my_canvas.drawString(200, grid_rows[-20] + 4, profile['other_language'])
    my_canvas.drawString(200, grid_rows[-21] + 4, profile['position']['name'])
    my_canvas.drawString(200, grid_rows[-22] + 4, profile['skills'])
    my_canvas.drawString(40 + 138 * 1, 304, profile['boots'] if profile['boots'] is not None else '')
    my_canvas.drawString(40 + 138 * 2, 304, profile['jacket'] if profile['jacket'] is not None else '')
    my_canvas.drawString(40 + 138 * 3, 304, profile['pants'] if profile['pants'] is not None else '')
    my_canvas.drawString(40 + 138 * 4, 304, profile['shirt'] if profile['shirt'] is not None else '')

    if profile['photo_path'] is not None and profile['photo_path'] != '':
        my_canvas.drawImage('media' + profile['photo_path'], 370, 25,
                            width=212, height=275)

    my_canvas.grid([370, 582], [25, 300])

    my_canvas.showPage()

    my_canvas.setLineWidth(.5)
    my_canvas.setFillColor('#c0c0c0')
    my_canvas.rect(30, 820, 552, 15, stroke=0, fill=1)
    my_canvas.rect(30, 25, 20, 15 * 54, stroke=0, fill=1)
    my_canvas.setFillColor(black)
    grid_rows = []
    for i in range(55):
        grid_rows.append(25 + 15 * i)
    my_canvas.grid([30, 50, 165, 340, 480, 582], grid_rows)

    my_canvas.setFont('Arial-Bold', 9)
    my_canvas.drawString(55, 824, "Ammatti")
    my_canvas.drawString(170, 824, "Профессия")
    my_canvas.drawString(345, 824, "Amet")
    my_canvas.drawString(520, 824, "1-10")

    my_canvas.save()
    return "media/users/" + profile['auth_user_id']['email'] + ".pdf"
