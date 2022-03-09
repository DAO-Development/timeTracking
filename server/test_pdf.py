import datetime
import math

from server.config import company
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


def print_sale(sale, items):
    count = 0  # номер страницы
    pages = len(items) // 10 + 1  # количество страниц (количество items/10)
    my_canvas = canvas.Canvas("media/accounting/" + str(sale['id']) + ".pdf")
    pdfmetrics.registerFont(TTFont('Arial-Bold', './static/fonts/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial', './static/fonts/arialmt.ttf'))
    my_canvas.setLineWidth(.5)

    my_canvas.setFont('Arial-Bold', 11)
    my_canvas.setFillColor(orangered)
    # тот, кто выставил
    my_canvas.drawString(55, 795, company['name'])
    my_canvas.setFont('Arial-Bold', 9)
    my_canvas.setFillColor(black)
    # юридический адрес?
    my_canvas.drawString(55, 780, company['address_house'] + ", " + company['address_city'])
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
    my_canvas.drawString(55, 700, sale["client"]["name"].upper())
    my_canvas.drawString(55, 685,
                         sale['client']['business_address']['street'] + ' ' + sale['client']['business_address'][
                             'house'].upper())
    my_canvas.drawString(55, 670,
                         sale['client']['business_address']['index'] + ' ' + sale['client']['business_address'][
                             'city'].upper())
    my_canvas.setFont('Arial-Bold', 9)
    my_canvas.drawString(55, 580, 'Регистрационный номер')
    my_canvas.drawString(55, 570, 'или личный код: ' + sale["client"]["ogrn"])

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
    my_canvas.drawString(455, 690, 'Напоминание')
    my_canvas.drawString(325, 660, 'Срок оплаты')
    my_canvas.drawString(455, 660, 'Дата оплаты')
    my_canvas.drawString(325, 630, 'Срок уведомления')
    my_canvas.drawString(455, 630, 'Проценты по просрочке')
    my_canvas.drawString(325, 600, 'Номер объекта заказчика')
    my_canvas.drawString(455, 600, 'Заметки')
    my_canvas.drawString(325, 570, 'Адрес объекта')

    my_canvas.setFont('Arial-Bold', 12)
    my_canvas.drawString(325, 735, datetime.datetime.strptime(sale['create_date'], '%Y-%m-%d').strftime('%d.%m.%Y'))
    my_canvas.drawString(455, 735, str(sale['id']))
    my_canvas.drawString(325, 705, "")  # ссылка
    my_canvas.drawString(325, 675, str(sale['client']['id']))
    my_canvas.drawString(455, 675, '-')
    my_canvas.drawString(325, 645, str(sale['payment_terms']['days']) + ' дн.')
    my_canvas.drawString(455, 645, (datetime.datetime.strptime(sale['create_date'], '%Y-%m-%d') + datetime.timedelta(
        days=sale['payment_terms']['days'])).strftime('%d.%m.%Y'))
    my_canvas.drawString(325, 615, '-')
    my_canvas.drawString(455, 615, '-')
    my_canvas.drawString(325, 585, sale['object_number'])
    my_canvas.drawString(455, 585, sale['description'])
    my_canvas.drawString(325, 555, sale['object']['street'] + ' ' + sale['object']['house'] + ', ' + sale['object'][
        'index'] + ' ' + sale['object']['city'])

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

    i = 0
    sum = 0
    vat = {}
    sum_no_vat = 0
    for item in range(i, len(items)):
        i += 1
        y = 510 - 13 * i
        my_canvas.setFont('Arial-Bold', 10)
        my_canvas.drawString(55, y, str(i))
        my_canvas.setFont('Arial-Bold', 9)
        name = items[item]['name']
        my_canvas.drawString(68, y, name)
        my_canvas.drawString(225, y, str(items[item]['tax']))
        if items[item]['tax'] not in vat:
            vat[items[item]['tax']] = items[item]['price'] * (float(items[item]['tax']) / 100)
        else:
            vat[items[item]['tax']] += items[item]['price'] * (float(items[item]['tax']) / 100)

        my_canvas.drawRightString(300, y, str(items[item]['quantity']))
        my_canvas.drawString(305, y, items[item]['measurement'])
        my_canvas.drawRightString(375, y, str(items[item]['price']))
        sum_no_vat += items[item]['price'] * items[item]['quantity']
        my_canvas.drawRightString(435, y, str(round(items[item]['price'] * (1 + float(items[item]['tax']) / 100), 2)))
        my_canvas.drawRightString(460, y, str(items[item]['discount']) if items[item]['discount'] > 0 else '-')
        my_canvas.drawRightString(520, y, str(
            round(items[item]['price'] * items[item]['quantity'] * (1 - float(items[item]['discount']) / 100), 2)))
        my_canvas.drawRightString(575, y, str(
            round(items[item]['price'] * items[item]['quantity'] * (1 + float(items[item]['tax']) / 100) * (
                    1 - float(items[item]['discount']) / 100), 2)))
        sum += round(items[item]['price'] * items[item]['quantity'] * (1 + float(items[item]['tax']) / 100) * (
                1 - float(items[item]['discount']) / 100), 2)

    my_canvas.setFont('Arial', 8)
    vat_str = ''
    sum_vat = 0
    for key in vat.keys():
        vat_str += ' + НДС ' + str(key) + '% ' + str(vat[key])
        sum_vat += vat[key]

    my_canvas.drawString(55, 510 - 13 * (10 + 2),
                         '(' + str(sum_no_vat) + vat_str + ' = ' + str(sum) + ')')
    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawString(440, 510 - 13 * (10 + 2), 'ВСЕГО EUR')
    my_canvas.drawRightString(565, 510 - 13 * (10 + 2), str(sum))

    my_canvas.grid([50, 145, 240, 355, 450, 580], [288, 303, 315])
    my_canvas.setFont('Arial', 8)
    my_canvas.drawString(55, 305, 'Номер ссылки')
    my_canvas.drawString(150, 305, 'Дата оплаты')
    my_canvas.drawString(245, 305, 'Цена без НДС EUR')
    my_canvas.drawString(360, 305, 'НДС EUR')
    my_canvas.drawString(455, 305, 'Общая сумма EUR')
    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawString(55, 292, sale['number_link'])
    my_canvas.drawString(150, 292, (datetime.datetime.strptime(sale['create_date'], '%Y-%m-%d') + datetime.timedelta(
        days=sale['payment_terms']['days'])).strftime('%d.%m.%Y'))
    my_canvas.drawString(245, 292, str(sum_no_vat))
    my_canvas.drawString(360, 292, str(sum_vat))
    my_canvas.drawString(455, 292, str(sum))

    my_canvas.setFont('Arial', 8)
    my_canvas.drawString(55, 278, company["name"])
    my_canvas.drawString(55, 268, company["address_house"])
    my_canvas.drawString(55, 258, company["address_city"])
    my_canvas.drawString(160, 278, 'Рег. нр: ' + company["ogrn"])
    my_canvas.drawString(245, 278, 'Тел: ' + company["phone"])
    my_canvas.drawString(245, 268, 'e-mail: ' + company["email"])
    my_canvas.drawString(245, 258, 'web: ' + company["web"])
    my_canvas.setFont('Arial', 10)
    my_canvas.drawString(405, 275, company["bank_account"].upper() + ' ' + company["bank"].upper())

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

    my_canvas.setFont('Arial-Bold', 10)
    my_canvas.drawString(125, 205, company["bank"].upper() + ' ' + company['bank_account'].upper())
    my_canvas.drawString(331, 205, company['bic'])
    my_canvas.drawString(125, 180, company['name'])
    my_canvas.drawString(125, 155, sale["client"]["name"])
    my_canvas.drawString(125, 143, sale['client']['business_address']['street'] + ' ' + sale['client']['business_address'][
                             'house'].upper())
    my_canvas.drawString(125, 131, sale['client']['business_address']['index'] + ' ' + sale['client']['business_address'][
                             'city'].upper())
    my_canvas.drawString(331, 175, sale['comment'])
    my_canvas.setFont('Arial-Bold', 12)
    my_canvas.drawString(331, 125, str(sale['id']))
    my_canvas.drawString(445, 125,
                         '000/1/' + datetime.datetime.strptime(sale['create_date'], '%Y-%m-%d').strftime('%d.%m.%Y'))
    my_canvas.drawString(370, 102, sale['number_link'])
    my_canvas.drawString(370, 70, (datetime.datetime.strptime(sale['create_date'], '%Y-%m-%d') + datetime.timedelta(
        days=sale['payment_terms']['days'])).strftime('%d.%m.%Y'))
    my_canvas.drawRightString(560, 70, str(sum))

    my_canvas.save()
    return "media/accounting/" + str(sale['id']) + ".pdf"


def print_offer(offer, items):
    # items = [
    #     {
    #         'name': 'As. B 11 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 12 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 13 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 14 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 15 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 16 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 17 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 18 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    #     {
    #         'name': 'As. B 19 / 44m2 / Suojaus, reikien kittaus, seinien ja kattojen maalaus / reikien kittaus, Kylpyhuoneesta lattiamatto pois ja epoksi pinnoitus'},
    # ]
    count_page = 0  # номер страницы
    count_items = 0
    count_str = 0
    max_str = 0
    max_page_str = 20
    for item in items:
        max_str += math.ceil(len(item['name']) / 65)
    pages = math.ceil(max_str / max_page_str)
    my_canvas = canvas.Canvas("media/accounting/" + 'tarjous1' + ".pdf")
    pdfmetrics.registerFont(TTFont('Arial-Bold', './static/fonts/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial', './static/fonts/arialmt.ttf'))
    my_canvas.setLineWidth(.5)

    my_canvas.setFont('Helvetica', 9.5)
    my_canvas.drawString(30, 520, 'Yrttipolku 4 A, B, ja C Kerava / Huoneistoremontit')
    my_canvas.drawString(30, 495, 'Materiaalit:')
    my_canvas.drawString(30, 482, 'Katton maalaus - Tikkurilan Siro 2 täyshimmeä')
    my_canvas.drawString(30, 469, 'Katton maalaus - Tikkurilan Siro 2 täyshimmeä')
    my_canvas.drawString(30, 456, 'Katton maalaus - Tikkurilan Siro 2 täyshimmeä')
    my_canvas.drawString(30, 443, 'Katton maalaus - Tikkurilan Siro 2 täyshimmeä')
    my_canvas.drawString(30, 430, 'Katton maalaus - Tikkurilan Siro 2 täyshimmeä')
    my_canvas.drawString(30, 402, 'Hinnat sisältää : materiaalit, oma roskien siivous + jätteille kustannukset.')

    while count_str < max_str:
        count_page += 1
        my_canvas.setFont('Arial-Bold', 16)
        my_canvas.drawString(330, 800, 'Tarjous')
        my_canvas.setFont('Helvetica-Bold', 9)
        my_canvas.drawString(330, 750, 'Tarjouksen numero:')
        my_canvas.drawString(330, 735, 'Tarjouksen päivä:')
        my_canvas.drawString(330, 720, 'Voimassa päivään:')
        my_canvas.drawString(330, 705, 'Asiakasnumero:')
        my_canvas.drawImage('project-vue/src/assets/logo.png', 60, 750, width=106, height=40)  # todo чей лого?
        my_canvas.drawString(60, 730, 'Timanttitimpurit Oy')
        my_canvas.drawString(60, 718, 'Sami Lahti')
        my_canvas.drawString(60, 706, 'Kaivolantie 4')
        my_canvas.drawString(60, 694, '04500 Kellokoski Kellokoski')
        my_canvas.drawString(60, 682, 'Asiakasnumero: ' + str(3))

        my_canvas.setFillColor('#c0c0c0')
        my_canvas.rect(30, 360, 545, 20, stroke=0, fill=1)
        my_canvas.setFillColor(black)
        my_canvas.setFont('Helvetica-Bold', 9)
        my_canvas.drawString(35, 367, 'Kuvaus')
        my_canvas.drawRightString(340, 367, 'Päivä')
        my_canvas.drawRightString(375, 367, 'Määrä')
        my_canvas.drawRightString(420, 367, 'Yksikkö')
        my_canvas.drawRightString(470, 367, 'À-hinta')
        my_canvas.drawRightString(520, 367, 'Alv %')
        my_canvas.drawRightString(570, 367, 'Yhteensä')
        my_canvas.setFont('Helvetica', 9)
        y = 345
        count_str_local = 0
        for item in items[count_items:]:
            if (count_str_local + math.ceil(len(item['name']) / 65)) >= max_page_str:
                break
            else:
                count_items += 1
                count_str += math.ceil(len(item['name']) / 65)
                count_str_local += math.ceil(len(item['name']) / 65)
                for i in range(math.ceil(len(item['name']) / 65)):
                    if 65 * (i + 1) < len(item['name']):
                        my_canvas.drawString(35, y - 12 * i, item['name'][65 * i:65 * (i + 1)])
                    else:
                        my_canvas.drawString(35, y - 12 * i, item['name'][65 * i:])
                y -= 12 * math.ceil(len(item['name']) / 65)
        my_canvas.line(30, 70, 575, 70)
        my_canvas.setFont('Helvetica-Bold', 9)
        my_canvas.drawString(35, 58, 'AS profile')
        my_canvas.drawString(280, 58, 'Yhteystiedot')  # контакт
        my_canvas.setFont('Helvetica', 9)
        my_canvas.drawString(35, 45, 'Everstinkuja 4c-58')
        my_canvas.drawString(35, 30, '02600 Espoo')
        my_canvas.drawString(35, 15, 'Y-tunnus: 2622146-9')
        my_canvas.drawString(280, 45, 'Andrei Silevits')
        my_canvas.drawString(280, 30, '+358405171188')
        my_canvas.drawString(280, 15, 'andrei.silevits@gmail.com')
        if count_str == max_str:
            my_canvas.line(30, y, 575, y)
            my_canvas.setFont('Helvetica-Bold', 8)
            my_canvas.drawString(420, y - 20, 'Yhteensä (alv 0%)')
            my_canvas.drawString(420, y - 30, 'Alv 24,00 %')
            my_canvas.line(415, y - 35, 575, y - 35)
            my_canvas.setFont('Helvetica-Bold', 10)
            my_canvas.drawString(420, y - 50, 'Yhteensä')
        my_canvas.setFont('Helvetica', 9)
        my_canvas.drawRightString(575, 810, str(count_page) + '/' + str(pages))
        my_canvas.showPage()

    my_canvas.save()
    return "media/accounting/" + 'tarjous1' + ".pdf"


if __name__ == '__main__':
    print_offer('offer', 'items')
