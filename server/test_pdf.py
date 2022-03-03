import datetime

from reportlab.lib.colors import black, orangered
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# 612х792
def print_profile_form(profile):
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


def print_sale(sale):
    count = 0  # номер страницы
    pages = 1  # количество страниц (количество items/10)
    my_canvas = canvas.Canvas("media/accounting/" + '1' + ".pdf")
    pdfmetrics.registerFont(TTFont('Arial-Bold', './static/fonts/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial', './static/fonts/arialmt.ttf'))
    my_canvas.setLineWidth(.5)

    my_canvas.setFont('Arial-Bold', 11)
    my_canvas.setFillColor(orangered)
    # Название клиента
    my_canvas.drawString(55, 795, "Luxor Talot OY")
    my_canvas.setFont('Arial-Bold', 9)
    my_canvas.setFillColor(black)
    # юридический адрес?
    my_canvas.drawString(55, 780, "HIRSIKUJA 6C, 01680 Vantaa")
    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawString(370, 795, "Дата")
    my_canvas.setFont('Arial', 10)
    # create_date
    my_canvas.drawString(370, 780, datetime.datetime.now().strftime('%d.%m.%Y'))
    count += 1
    my_canvas.drawString(523, 795, str(count) + ' (' + str(pages) + ')')
    my_canvas.setFont('Arial-Bold', 14)
    my_canvas.drawCentredString(280, 790, 'СЧЕТ')

    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawString(55, 700, 'SRV OY'.upper())
    my_canvas.drawString(55, 685, 'KORENNONTIE 3B'.upper())
    my_canvas.drawString(55, 670, '01490 HELSINKI'.upper())
    my_canvas.setFont('Arial-Bold', 9)
    my_canvas.drawString(55, 580, 'Регистрационный номер')
    my_canvas.drawString(55, 573, 'или личный код: 2535570-5')

    my_canvas.grid([320, 450, 580], [730, 760])
    my_canvas.grid([320, 580], [700, 730])
    grid_rows = []
    for i in range(1, 6):
        grid_rows.append(550 + 30 * i)
    my_canvas.grid([320, 450, 580], grid_rows)
    my_canvas.grid([320, 580], [550, 580])
    my_canvas.setFont('Arial', 9)
    my_canvas.drawString(325, 750, 'Дата')
    my_canvas.drawString(455, 750, 'Номер счета')
    my_canvas.drawString(325, 720, 'Ссылка')
    my_canvas.drawString(325, 690, 'Номер клиента')
    my_canvas.drawString(455, 690, 'Напоминание')  # todo спросить про напоминание (нужно ли в бд?)
    my_canvas.drawString(325, 660, 'Срок оплаты')
    my_canvas.drawString(455, 660, 'Дата оплаты')
    my_canvas.drawString(325, 630, 'Срок уведомления')
    my_canvas.drawString(455, 630, 'Проценты по просрочке')  # todo спросить нужно ли в бд
    my_canvas.drawString(325, 600, 'Номер объекта заказчика')
    my_canvas.drawString(455, 600, 'Заметки')
    my_canvas.drawString(325, 570, 'Адрес объекта')

    my_canvas.setFont('Arial', 7)
    my_canvas.drawString(68, 510, 'Наименование'.upper())
    my_canvas.drawString(225, 510, 'НДС%')
    my_canvas.drawString(275, 510, 'КОЛ-ВО')
    my_canvas.drawString(305, 510, 'Ед.'.upper())
    my_canvas.drawRightString(375, 518, 'Цена за шт'.upper())
    my_canvas.drawRightString(375, 510, 'Без НДС EUR'.upper())
    my_canvas.drawRightString(435, 518, 'Цена за шт'.upper())
    my_canvas.drawRightString(435, 510, 'С НДС EUR'.upper())
    my_canvas.drawString(445, 510, 'ALE%'.upper())
    my_canvas.drawRightString(520, 526, 'Всего без'.upper())
    my_canvas.drawRightString(520, 518, 'налога'.upper())
    my_canvas.drawRightString(520, 510, 'EUR'.upper())
    my_canvas.drawRightString(575, 526, 'Всего с'.upper())
    my_canvas.drawRightString(575, 518, 'налогом'.upper())
    my_canvas.drawRightString(575, 510, 'EUR'.upper())
    my_canvas.line(50, 508, 580, 508)

    my_canvas.setFont('Arial-Bold', 10)
    for i in range(10):
        my_canvas.drawString(55, 510 - 13 * (i + 1), str(i + 1))

    my_canvas.setFont('Arial', 8)
    my_canvas.drawString(55, 510 - 13 * (10 + 2),
                         '(' + str(23433) + ' + НДС' + str(24) + '%' + str(786) + ' = ' + str(4005) + ')')
    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawString(440, 510 - 13 * (10 + 2), 'ВСЕГО EUR')
    my_canvas.drawRightString(565, 510 - 13 * (10 + 2), str(4005))

    my_canvas.grid([50, 145, 240, 355, 450, 580], [288, 303, 315])
    my_canvas.setFont('Arial', 8)
    my_canvas.drawString(55, 305, 'Номер ссылки')
    my_canvas.drawString(150, 305, 'Дата оплаты')
    my_canvas.drawString(245, 305, 'Цена без НДС EUR')
    my_canvas.drawString(360, 305, 'НДС EUR')
    my_canvas.drawString(455, 305, 'Общая сумма EUR')

    my_canvas.drawString(55, 278, 'Luxor Talot OY')
    my_canvas.drawString(55, 268, 'Hirsikuja 6C')
    my_canvas.drawString(55, 258, '01680 Vantaa')
    my_canvas.drawString(160, 278, 'Рег. нр: 2926641-9')
    my_canvas.drawString(245, 278, 'Тел: ')
    my_canvas.drawString(245, 268, 'e-mail: ')
    my_canvas.drawString(245, 258, 'web: ')
    my_canvas.setFont('Arial', 10)
    my_canvas.drawString(405, 275, 'FI30 1544 3000 0810 47 NORDEA'.upper())

    my_canvas.setDash([1.3, 2])
    my_canvas.line(50, 245, 540, 245)

    my_canvas.setDash()
    my_canvas.line(50, 225, 580, 225)
    my_canvas.line(50, 200, 580, 200)
    my_canvas.line(50, 175, 326, 175)
    my_canvas.line(326, 145, 580, 145)
    my_canvas.line(326, 120, 580, 120)
    my_canvas.line(120, 110, 326, 110)
    my_canvas.line(50, 92, 580, 92)
    my_canvas.line(50, 62, 580, 62)

    my_canvas.line(65, 175, 65, 92)
    my_canvas.line(120, 225, 120, 175)
    my_canvas.line(120, 62, 120, 92)
    my_canvas.line(326, 225, 326, 62)
    my_canvas.line(365, 120, 365, 62)
    my_canvas.line(440, 145, 440, 120)
    my_canvas.line(465, 92, 465, 62)
    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawCentredString(326, 50, 'Спасибо за своевременно оплаченный счет!'.upper())

    my_canvas.setFont('Arial', 7.5)
    my_canvas.drawRightString(115, 213, 'Номер счета')
    my_canvas.drawRightString(115, 205, 'получателя')
    my_canvas.setFont('Helvetica', 7)
    my_canvas.drawString(125, 216, 'IBAN')
    my_canvas.drawString(331, 216, 'BIC')
    my_canvas.setFont('Arial', 7.5)
    my_canvas.drawRightString(112, 185, 'Получатель')
    my_canvas.drawString(331, 190, 'Пояснение к счету')
    y = 167
    for ch in 'Перевод'.upper():
        y -= 9
        my_canvas.drawRightString(60, y, ch)
    my_canvas.drawString(70, 167, 'Плательщик')
    my_canvas.drawString(70, 115, 'Подпись')
    my_canvas.drawString(331, 137, 'Номер счета')
    my_canvas.drawString(445, 137, 'Памятка')
    my_canvas.drawCentredString(346, 108, 'Номер')
    my_canvas.drawCentredString(346, 100, 'ссылки')
    my_canvas.drawRightString(115, 78, 'Оплата с номера')
    my_canvas.drawRightString(115, 68, 'счета')
    my_canvas.drawCentredString(346, 78, 'Дата')
    my_canvas.drawCentredString(346, 68, 'оплаты')
    my_canvas.drawString(470, 83, 'Euro')

    my_canvas.save()
    return "media/accounting/" + '1' + ".pdf"


def print_offer():
    my_canvas = canvas.Canvas("media/accounting/" + '1' + ".pdf")
    pdfmetrics.registerFont(TTFont('Arial-Bold', './static/fonts/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial', './static/fonts/arialmt.ttf'))
    my_canvas.setLineWidth(.5)
    my_canvas.setFont('Arial-Bold', 12)

    my_canvas.save()
    return "media/accounting/" + '1' + ".pdf"


if __name__ == '__main__':
    print_sale()
