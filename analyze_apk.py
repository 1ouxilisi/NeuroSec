import os
import zipfile
import xml.etree.ElementTree as ET

# APK文件路径
apk_path = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\mobile_test\106_1a3a2919...e.apk.1"

# 先找到真实的文件名
mobile_dir = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\mobile_test"
apk_files = [f for f in os.listdir(mobile_dir) if f.endswith('.apk') or f.endswith('.apk.1')]
print("找到的APK文件：")
for f in apk_files:
    size = os.path.getsize(os.path.join(mobile_dir, f))
    print(f"  {f} - {size/1024/1024:.1f}MB")

# 选择不是抖音的那个APK
target_apk = None
for f in apk_files:
    if '抖音' not in f and 'douyin' not in f.lower():
        target_apk = os.path.join(mobile_dir, f)
        break

if target_apk:
    print(f"\n目标APK: {target_apk}")
    
    # 打开APK看看里面有什么
    with zipfile.ZipFile(target_apk, 'r') as z:
        print("\nAPK内容（前20个文件）：")
        for i, name in enumerate(z.namelist()[:20]):
            print(f"  {i+1}. {name}")
        
        # 看看有没有AndroidManifest.xml
        if 'AndroidManifest.xml' in z.namelist():
            print("\n✅ 找到AndroidManifest.xml")
        
        # 看看有没有classes.dex
        dex_files = [f for f in z.namelist() if f.endswith('.dex')]
        print(f"\n✅ 找到 {len(dex_files)} 个dex文件")
else:
    print("\n❌ 没找到OPPO商城APK")
