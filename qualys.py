import os
import yaml
import pandas as pd
import xml.etree.ElementTree as ET

input_file = input("Enter the path to the file: ")
with open(input_file, 'r') as file:
    data = yaml.safe_load(file)

def extract_titles(data, categories, category):
    titles_info = {}
    for cat in data['SCAN']['IP']:
        ip = cat['@value']
        if isinstance(cat, dict) and categories in cat:
            for cat_info in cat[categories]['CAT']:
                if isinstance(cat_info, dict) and category in cat_info:
                    port = cat_info.get('@port', None)
                    for item in cat_info[category]:
                        if isinstance(item, dict) and 'TITLE' in item:
                            title = item['TITLE']
                            severity = item['@severity']
                            cve_id = item.get('@cveid', None)
                            if title in titles_info:
                                if severity not in titles_info[title]['severity']:
                                    titles_info[title]['severity'].append(severity)
                                titles_info[title]['ip'].append(ip)
                                if port:
                                    titles_info[title]['port'].append(port)
                                if cve_id:
                                    titles_info[title]['cveid'].append(cve_id)
                            else:
                                titles_info[title] = {'severity': [severity], 'ip': [ip], 'port': [port] if port else [], 'cveid': [cve_id] if cve_id else []}
    return titles_info

def display_titles_info(titles_info):
    names = []
    severities = []
    ips = []
    ports = []
    cves = []

    for title, info in titles_info.items():
        names.append(title)
        severities.append(', '.join(info['severity']))
        ips.append(', '.join(info['ip']))
        ports.append(', '.join(info['port']) if 'port' in info else '')
        cves.append('\n'.join(info['cveid']) if 'cveid' in info else '')

    df = pd.DataFrame({
        'Title': names,
        'Severity': severities,
        'IP': ips,
        'Port': ports,
        'CVEs': cves
    })
    return df

titles_info = extract_titles(data, 'INFOS', 'INFO')
titles_vulns = extract_titles(data, 'VULNS', 'VULN')
titles_practices = extract_titles(data, 'PRACTICES', 'PRACTICE')

df_info = display_titles_info(titles_info)
df_vulns = display_titles_info(titles_vulns)
df_practices = display_titles_info(titles_practices)

df = pd.concat([df_info, df_vulns, df_practices], ignore_index=True)
output_file = os.path.splitext(input_file)[0] + "." + "xlsx"
df.to_excel(output_file, index=False)