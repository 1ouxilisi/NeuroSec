import os
import zipfile
import struct

# APK文件路径
mobile_dir = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\mobile_test"
apk_files = [f for f in os.listdir(mobile_dir) if f.endswith('.apk.1')]
apk_path = os.path.join(mobile_dir, apk_files[0])

print(f"分析APK: {apk_path}")
print("=" * 50)

# 读取AndroidManifest.xml（二进制格式）
with zipfile.ZipFile(apk_path, 'r') as z:
    manifest_data = z.read('AndroidManifest.xml')

print(f"AndroidManifest.xml大小: {len(manifest_data)} 字节")

# 简单解析二进制XML，找exported=true的组件
# 这里用简单的字符串搜索
manifest_str = manifest_data.decode('utf-8', errors='ignore')

# 找activity、service、receiver、provider
components = []
for tag in ['activity', 'service', 'receiver', 'provider']:
    count = manifest_str.count(tag)
    print(f"\n{tag}: {count}个")

# 找exported=true
exported_count = manifest_str.count('exported')
print(f"\nexported属性出现次数: {exported_count}")

# 找debuggable
debuggable_count = manifest_str.count('debuggable')
print(f"debuggable属性出现次数: {debuggable_count}")

# 找权限
permissions = []
for i in range(len(manifest_str)):
    if manifest_str[i:i+5] == 'PERMI':
        # 提取后面的字符串
        pass

print("\n" + "=" * 50)
print("初步分析完成！")
