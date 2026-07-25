import requests
import random

def get_flag_emoji(code):
    if len(code) != 2 or not code.isalpha():
        return code
    base = ord("🇦") - ord("A")
    return chr(base + ord(code[0].upper())) + chr(base + ord(code[1].upper()))

urls = [
    "https://raw.githubusercontent.com/FoolVPN-ID/Nautica/refs/heads/main/proxyList.txt",
]

all_lines = []

for url in urls:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        lines = response.text.strip().split("\n")
        all_lines.extend(lines)
    except Exception:
        pass

all_lines = list(set(all_lines))

valid_nodes = []
target_ports = {"443", "2053", "8443", "2083", "2096"}

for line in all_lines:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) >= 4:
        ip = parts[0]
        port = parts[1]
        name = parts[2]
        dc = parts[3]
        
        country_code = name[:2].upper()
        server_name = name[2:] if len(name) > 2 else name
        display_name = f"{get_flag_emoji(country_code)}{server_name}"
        
        node = f"{ip}:{port}#{display_name}_{dc}"
        valid_nodes.append((ip, port, node))

unique_nodes = {}
for ip, port, node in valid_nodes:
    if (ip, port) not in unique_nodes:
        unique_nodes[(ip, port)] = node

pool_a = []
pool_b = []

for (ip, port), node in unique_nodes.items():
    if port in target_ports:
        pool_b.append(node)
    else:
        pool_a.append(node)

random.shuffle(pool_a)
random.shuffle(pool_b)

group1 = pool_a[:20]
group2 = pool_b[:20]

remaining = pool_a[20:] + pool_b[20:]
random.shuffle(remaining)
group3 = remaining[:20]

final_nodes = group1 + group2 + group3

with open("nodes.txt", "w", encoding="utf-8") as f:
    for node in final_nodes:
        f.write(node + "\n")

with open("nodes_5000.txt", "w", encoding="utf-8") as f:
    for node in final_nodes:
        f.write(node + "\n")
