"""修复端口扫描器：增加常见Web开发端口"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\modules\recon\port_scanner.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

old = '''COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS", 587: "SMTP",
    993: "IMAPS", 995: "POP3S", 1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle",
    2049: "NFS", 2375: "Docker", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt",
    8888: "HTTP-Alt", 9000: "PHP-FPM", 9200: "Elasticsearch", 11211: "Memcached",
    27017: "MongoDB", 50070: "Hadoop",
}'''

new = '''COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS", 587: "SMTP",
    993: "IMAPS", 995: "POP3S", 1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle",
    2049: "NFS", 2375: "Docker", 3000: "Node.js", 3001: "Node.js-Alt",
    3306: "MySQL", 3389: "RDP", 5000: "Flask/Python", 5432: "PostgreSQL",
    5601: "Kibana", 5900: "VNC", 6379: "Redis", 8000: "HTTP-Alt",
    8001: "HTTP-Alt2", 8080: "HTTP-Proxy", 8081: "HTTP-Alt3",
    8443: "HTTPS-Alt", 8888: "HTTP-Alt", 9000: "PHP-FPM", 9090: "Prometheus",
    9200: "Elasticsearch", 11211: "Memcached", 27017: "MongoDB", 50070: "Hadoop",
}'''

if old in c:
    c = c.replace(old, new)
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(c)
    print("✅ 端口扫描器修复完成")
    print("  新增端口: 3000(Node.js), 3001, 5000(Flask), 5601(Kibana), 8000, 8001, 8081, 9090(Prometheus)")
else:
    print("❌ 未找到目标代码段")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")

# 验证3000端口在列表中
from pentestai.modules.recon.port_scanner import COMMON_PORTS, DEPTH_PORTS
print(f"\n✅ COMMON_PORTS总数: {len(COMMON_PORTS)}")
print(f"✅ 3000端口: {COMMON_PORTS.get(3000, '不存在')}")
print(f"✅ 5000端口: {COMMON_PORTS.get(5000, '不存在')}")
print(f"✅ standard深度端口数: {len(DEPTH_PORTS['standard'])}")
assert 3000 in DEPTH_PORTS['standard'], "3000应在standard端口列表中"
print("\n✅ 端口扫描器修复验证通过！")
