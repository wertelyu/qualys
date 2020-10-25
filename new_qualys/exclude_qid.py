def exclude(list_dict):
    excluded_qid = ['450038', '150009', '150010', '150021', '150024',
                    '150026', '150028', '150099', '150101', '150148',
                    '150152', '150172', '150194', '150277']
    new_list_dict = []
    for dict_vuln in copy_list_dict:
        if not dict_vuln.get('QID') in exclude_qid:
            new_list_dict.append(dict_vuln)
    return new_list_dict
