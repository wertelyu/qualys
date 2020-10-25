import csv
import xml.etree.ElementTree as ET


excluded = ['FIRST_TIME_DETECTED', 'LAST_TIME_DETECTED',
            'LAST_TIME_TESTED', 'TIMES_DETECTED', 'UNIQUE_ID',
            'QID', 'ID', 'AJAX', 'PARAM', 'IGNORED', 'STATUS', 'PAYLOADS', 'ACCESS_PATH']
excluded_1 = ['WASC', 'CVSS_TEMPORAL', 'AJAX',
              'PARAM', 'IGNORED', 'STATUS', 'ACCESS_PATH']


def parse_glossary(filename):
    """
    The function parses xml file and returns list of dictionaries
    """
    tree = ET.parse(filename)
    root = tree.getroot()

    owasp = {}
    for code in root[5][2]:
        owasp_dict = {line.tag: line.text for line in code}
        owasp[owasp_dict['CODE']] = owasp_dict['NAME']

    group = {}
    for code in root[5][1]:
        group_dict = {line.tag: line.text for line in code}
        group[group_dict['CODE']] = group_dict['NAME']

    result = []
    for tag in root[5][0]:
        a = {line.tag: line.text for line in tag if line.tag not in excluded_1}
        for key in a.keys():
            if key == 'OWASP':
                a[key] = owasp[a[key]]
            if key == 'GROUP':
                a[key] = group.get(a[key], a[key])
        result.append(a)

    for tag in root[4][0][2]:
        dict_vuln = {
            line.tag: line.text for line in tag if line.tag not in excluded}
        for line in tag:
            if line.tag == "QID":
                for vuln in result:
                    if vuln.get('QID') == line.text:
                        vuln.update(dict_vuln)

    return result


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
    return dict_list


def csv_writer(file_name):
    """
    The functions creates the csv file and writes date from the list of dictionaries
    """
    with open('csv_write_dict_16.csv', 'w') as f:
        data = new_dict(parse_glossary(file_name))
        title = ['CATEGORY', 'SEVERITY', 'CVSS_BASE', 'OWASP', 'CWE', 'TITLE', 'GROUP',
                 'AUTHENTICATION', 'URL', 'DESCRIPTION', 'IMPACT', 'SOLUTION', 'QID']
        writer = csv.DictWriter(f, fieldnames=title,
                                quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    csv_writer('Web_App.xml')
