import requests
from lxml import BeautifulSoup

# 发起HTTP请求并获取页面内容
url = "https://bgp.he.net/country/CN"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到包含ASN的表格
    asn_table = soup.find('table', {'class': 'table table-dark table-bordered'})
    
    if asn_table:
        # 打开一个文件来保存ASN列表
        with open('ASN.China.list', 'w') as file:
            # 遍历表格的每一行，提取ASN并写入文件
            for row in asn_table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    asn = cells[0].text.strip()
                    description = cells[1].text.strip()
                    file.write(f"{asn} - {description}\n")

        print("ASN列表已保存到ASN.China.list文件")
    else:
        print("未找到ASN表格")
else:
    print("无法访问网站")

# 从ASN列表文件中读取ASN数据
asn_data = []
with open('ASN.China.list', 'r') as file:
    for line in file:
        asn_data.append(line.strip())

# 假设你已经有了IP地址到ASN的映射数据，将其保存在ip_to_asn_mapping.txt文件中
# 从IP到ASN映射文件中读取映射数据
ip_to_asn_mapping = {}
with open('ip_to_asn_mapping.txt', 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            ip, asn = parts[0], parts[1]
            ip_to_asn_mapping[ip] = asn

# 将ASN数据转换为IP-ASN格式
ip_asn_data = []
for asn_entry in asn_data:
    parts = asn_entry.split(' - ')
    if len(parts) == 2:
        asn, description = parts[0], parts[1]
        ip_asn_data.append(f"{asn} - {description}")

# 匹配IP地址并添加到IP-ASN格式数据中
for ip, asn in ip_to_asn_mapping.items():
    ip_asn_data.append(f"{ip} - ASN{asn}")

# 将IP-ASN数据保存到文件
with open('IP_ASN_China.list', 'w') as file:
    for line in ip_asn_data:
        file.write(f"{line}\n")

print("IP-ASN格式数据已保存到IP_ASN_China.list文件")
