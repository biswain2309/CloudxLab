import os
import eml_parser
from collections import Counter
import fnmatch


def listemails(path, select, where, matches):
    item_f = []
    cntr_1 = cntr_2 = cntr_3 = cntr_4 = cntr_5 = cntr_6 = 0
    dict_slot = {}
    list_from = []
    list_to = []
    fname = []

    for item in select:
        to1 = select[0]
        from1 = select[1]
        subject1 = select[2]
    for dirpath, dirs, files in os.walk(path):
        for fa in fnmatch.filter(files, matches):
            file = str(dirpath) + str('/') + fa
            #             print('file :', file)
            with open(file, 'rb') as fhdl:
                raw_email = fhdl.read()
                parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

                parsed_eml_from = parsed_eml['header'][from1]
                parsed_eml_subject = parsed_eml['header'][subject1]
                parsed_eml_time = parsed_eml['header']['received']

                # cases for sent items:
                if parsed_eml_time == []:
                    parsed_eml_time = parsed_eml['header']['date']
                    slot1 = str(parsed_eml_time).split(' ')[1]
                    parsed_eml_to = parsed_eml['header'][to1][0]
                    parsed_eml_from = ''
                #                 print('parsed_eml_to :', parsed_eml_to)
                else:
                    # cases for inbox items:
                    src1 = str(parsed_eml_time[0])
                    value = src1.split(';')[1]
                    slot = value.split(' ')[5]
                    parsed_eml_to = ''

                item_a = (parsed_eml_to, parsed_eml_from, parsed_eml_subject)
                item_f.append(item_a)

                if ((int(slot[0:2]) >= 0 and int(slot[3:5]) >= 0) and (int(slot[0:2]) <= 5 and int(slot[3:5]) <= 59)):
                    cntr_1 = cntr_1 + 1
                elif (int(slot[0:2]) >= 6 and int(slot[3:5]) >= 0) and (int(slot[0:2]) <= 8 and int(slot[3:5]) <= 59):
                    cntr_2 = cntr_2 + 1
                elif (int(slot[0:2]) >= 9 and int(slot[3:5]) >= 0) and (int(slot[0:2]) <= 11 and int(slot[3:5]) <= 59):
                    cntr_3 = cntr_3 + 1
                elif (int(slot[0:2]) >= 12 and int(slot[3:5]) >= 0) and (int(slot[0:2]) <= 15 and int(slot[3:5]) <= 59):
                    cntr_4 = cntr_4 + 1
                elif (int(slot[0:2]) >= 16 and int(slot[3:5]) >= 0) and (int(slot[0:2]) <= 22 and int(slot[3:5]) <= 30):
                    cntr_5 = cntr_5 + 1
                elif int(slot[0:2]) <= 23 and int(slot[3:5]) <= 59:
                    cntr_6 = cntr_6 + 1
                dict_slot['12 midnight until 6am'] = cntr_1
                dict_slot['6am until 9am'] = cntr_2
                dict_slot['9 am until 12 noon'] = cntr_3
                dict_slot['12 noon until 4pm'] = cntr_4
                dict_slot['4pm until 11:30pm'] = cntr_5
                dict_slot['11:30pm until 12 midnight'] = cntr_6
                highest_slot = max(dict_slot, key=dict_slot.get)

                if parsed_eml_from != '':
                    list_from.append(parsed_eml_from)
                elif parsed_eml_to != '':
                    list_to.append(parsed_eml_to)

    counter_from = Counter(list_from)
    #     print('counter_from :', counter_from)
    counter_to = Counter(list_to)
    #     print('counter_to :', counter_to)
    max_mails_from = max(counter_from, key=counter_from.get)
    max_mails_to = max(counter_to, key=counter_to.get)
    if max_mails_from == max_mails_to:
        print('%s is my closest buddy.' % max_mails_to)
    else:
        print('%s is my closest buddy.' % max_mails_from)

    print('The highest_slot is %s.' % highest_slot)
    print('%s has sent the maximum mails.' % max_mails_from)
    print('Maximum mails are sent to %s.' % max_mails_to)
    return item_f


directory = '/home/indranibiswas233141/GYB-GMail-Backup-ibiswas.2309@gmail.com'
values = listemails(directory, ['to', 'from', 'subject'], 'subject', '*.eml')
print(values)