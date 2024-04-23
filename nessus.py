import os
import yaml
import pandas as pd

input_file = input("Enter the path to the file: ")
with open(input_file, 'r') as file:
    data = yaml.safe_load(file)

names = []
risks = []
cvss3_base_scores = []
hosts = []
cves = []

for risk, vulnerabilities in data.items():
    for vulnerability_id, vulnerability_data in vulnerabilities.items():
        name = vulnerability_data.get('name', '')
        risk = vulnerability_data.get('risk', '')
        cvss3_base_score = vulnerability_data.get('cvss3_base_score', '')
        hosts_info = vulnerability_data.get('hosts', [])
        host_str = ', '.join([h[0] for h in hosts_info]) if hosts_info else ''
        cve_list = vulnerability_data.get('cves', [])
        cve_str = '\n'.join(cve_list)

        names.append(name)
        risks.append(risk)
        cvss3_base_scores.append(cvss3_base_score)
        hosts.append(host_str)
        cves.append(cve_str)

df = pd.DataFrame({
    'Name': names,
    'Risk': risks,
    'CVSS3 Base Score': cvss3_base_scores,
    'Hosts': hosts,
    'CVEs': cves
})
output_file = os.path.splitext(input_file)[0] + "." + "xlsx"
df.to_excel(output_file, index=False)
