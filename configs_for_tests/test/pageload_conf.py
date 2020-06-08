# -*- coding: utf-8 -*-
""" Конфигурационный файл"""
# from page_object.base_test import get_current_time, get_today_date, get_yesterday_date, \
#     get_actual_interval, get_month_year

COMPANY_NAME = 'Рудник Комсомольский'
pit_name = "Восток"

# Путь к группе СБУ
sbu_group = "Рудник Комсомольский;СБУ"

# Выбор языка 'ru', 'en', 'fr'
# Для выбора нужно добавить параметр lang в open_page в хелпер
# По умолчанию везде выбран русский
language = 'ru'

# Cмены на выбор
shift_number = "09-21"  # Нестрогое соответствие

# Потом можно будет вводить не рандомную дату, а, например, дату вчерашней завершенной смены
# shift_date = get_yesterday_date()
shift_date = '03.04.2020'
oreflow_date = '03.04.2020'

# Даты для периода смен (например, СДО за период)
# start_date = get_yesterday_date()
# end_date = get_today_date()
start_date = '02.04.2020'
end_date = '03.04.2020'

# Диапазон времени можно задавать с часами и минутами
# start_datetime = get_actual_interval()[0]
# end_datetime = get_actual_interval()[1]
start_datetime = '02.04.2020 01:47'
end_datetime = '03.04.2020 11:58'

# Название СДО для выбора, через ; (для детального)
sdo_name = "Рудник Комсомольский;ПДМ;ПДМ;33 Cat R1700g"

# Выбор оператора по имени (для профиля)
operator_name = "Ахмедов А. Г."
# ПЛюм еще несколько для отчета
op3 = "Темиров З. А."

# Год-месяц для Профиля оператора
# year_month = get_month_year()
month_year = "03.2020"

# выбор диагностического параметра
diagparam = "Объем загрузки по давлению"
diagparam_datetime_end = "03.04.2020 21:58"

# Наименование Погрузочной единицы. Например. для паспорта характеристики выработок
shovel_name = 'KАМ-11-41-2'

SEARCH_WORDS = False
WORDLIST = []
