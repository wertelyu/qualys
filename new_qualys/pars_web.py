import base64
import csv
import xml.etree.ElementTree as ET
import os
import glob
from xlsxwriter.workbook import Workbook


def parser(filename):
    """
    Функция парсит из xml VULNERABILITY.
    return: list of dictionaries with vulnerability
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    owasp = {}
    for code in root[5][2]:
        owasp_dict = {line.tag: line.text for line in code}
        owasp[owasp_dict['CODE']] = owasp_dict['NAME']

    wasc = {}
    for code in root[5][3]:
        wasc_dict = {line.tag: line.text for line in code}
        wasc[wasc_dict['CODE']] = owasp_dict['NAME']

    group = {}
    for code in root[5][1]:
        group_dict = {line.tag: line.text for line in code}
        group[group_dict['CODE']] = group_dict['NAME']

    result = []
    for tag in root[4][0][2]:
        result.append(main_parser(tag))
    for tag in root[4][0][6]:
        result.append(main_parser(tag))

    for tag in root[5][0]:
        a = {line.tag: line.text for line in tag}
        for key in a.keys():
            if key == 'OWASP':
                a[key] = owasp[a[key]]
            if key == 'WASC':
                if ',' in a[key]:
                    wasc_list = []
                    for row in a[key].split(','):
                        wasc_list.append(wasc[row])
                    a[key] = ' ,'.join(wasc_list)
                else:
                    a[key] = wasc[a[key]]
            if key == 'GROUP':
                a[key] = group.get(a[key], a[key])
        for line in tag:
            if line.tag == "QID":
                for vuln in result:
                    if vuln.get('QID') == line.text:
                        vuln.update(a)
    return result


def main_parser(tag):
    dict_vulns = {line.tag: line.text for line in tag}
    payload = []
    for line in tag:
        if line.tag == 'DATA':
            dict_vulns['DATA'] = decode_64(dict_vulns['DATA'])
        if line.tag == 'ACCESS_PATH':
            access_list = [row.text for row in line]
            dict_vulns['ACCESS_PATH'] = access_list
        if line.tag == 'PAYLOADS':
            for row in line:
                payload_dict = {line.tag: line.text for line in row}
                for line in row:
                    if line.tag == 'REQUEST':
                        request_dict = {row.tag: row.text for row in line}
                        for row in line:
                            headers = []
                            if row.tag == 'HEADERS':
                                for line in row:
                                    headers_list = [
                                        row.text for row in line]
                                    headers.append(headers_list)
                            request_dict['HEADERS'] = headers
                        payload_dict['REQUEST'] = request_dict
                    if line.tag == 'RESPONSE':
                        response_dict = {row.tag: row.text for row in line}
                        if response_dict.get('CONTENTS'):
                            response_dict['CONTENTS'] = decode_64(
                                response_dict['CONTENTS'])
                        if response_dict.get('EVIDENCE'):
                            response_dict['EVIDENCE'] = decode_64(
                                response_dict['EVIDENCE'])
                        payload_dict['RESPONSE'] = response_dict
                payload.append(payload_dict)
        dict_vulns['PAYLOADS'] = payload
    return dict_vulns


def decode_64(base64_message):
    """
    На входе функция получает закодированную строку.
    return: decoding string
    """
    try:
        base64_bytes = base64_message.encode('utf-8')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('utf-8')
        return message
    except:
        print('Decode error!')


def new_dict(dict_list):
    """
    The function adds missing keys with the value "none" and returns a list of dictionaries
    """
    a = []
    for row in dict_list:
        for keys in row.keys():
            a.append(keys)
    for row in dict_list:
        for line in set(a):
            if line not in row.keys():
                row[line] = 'none'

    return exclude(dict_list)


def exclude(list_dict):
    """
    Иключает информационные QID.
    return: list of dictionaries
    """
    excluded_qid = ['450038', '150009', '150010', '150021', '150024',
                    '150026', '150028', '150099', '150101', '150148',
                    '150152', '150172', '150194', '150277']
    new_list_dict = []
    for dict_vuln in list_dict:
        if not dict_vuln.get('QID') in excluded_qid and dict_vuln:
            new_list_dict.append(dict_vuln)

    new_list_dict.sort(key=(lambda x: x['CVSS_BASE'] if x['CVSS_BASE'] != 'none' else x['SEVERITY']), reverse=True)
    new_list_dict.sort(key=lambda x: x['SEVERITY'], reverse=True)
    new_list_dict.sort(key=lambda x: x['CATEGORY'] if x['CATEGORY'] != 'Information Gathered' else 'w')
    return new_list_dict


def conv_to_xlsx():
    """
    Функция ищет в текущей директории csv файл и конвертирует его в xlsx.
    """
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()


def main(file_name):
    """
    The functions creates the csv file and writes date from the list of dictionaries
    """
    print('START')
    with open('csv_write_dict_16.csv', 'w') as f:
        data = new_dict(parser(file_name))
        title = ['UNIQUE_ID', 'ID', 'QID', 'URL', 'AUTHENTICATION', 'AJAX', 'STATUS',
                 'FIRST_TIME_DETECTED', 'LAST_TIME_DETECTED', 'LAST_TIME_TESTED', 'TIMES_DETECTED',
                 'IGNORED', 'SEVERITY', 'CATEGORY', 'CVSS_BASE', 'CVSS_TEMPORAL', 'TITLE', 'GROUP', 'OWASP', 'WASC',
                 'CWE', 'DESCRIPTION', 'IMPACT', 'SOLUTION',
                 'FORM_ENTRY_POINT', 'PARAM', 'ACCESS_PATH', 'DATA', 'SSL_DETAILS', 'PAYLOADS']
        writer = csv.DictWriter(f, fieldnames=title,
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in data:
            writer.writerow(d)
        conv_to_xlsx()
        print('FINISHED')


if __name__ == '__main__':
    main('Web_Application.xml')
