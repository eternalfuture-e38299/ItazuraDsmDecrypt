#*******************************************************************************
#* 文件名称: itazura_dsm_decrypt.py
#* 创建时间: 2025/8/7
#* 作者: EternalFuture゙
#* Github: https://github.com/eternalfuture-e38299
#* 版权声明: Copyright © 2025 EternalFuture. All rights reserved.
#* 许可证: This program is free software: you can redistribute it and/or modify
#*         it under the terms of the GNU Affero General Public License as published
#*         by the Free Software Foundation, either version 3 of the License, or
#*         (at your option) any later version.
#*
#*         This program is distributed in the hope that it will be useful,
#*         but WITHOUT ANY WARRANTY; without even the implied warranty of
#*         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#*         GNU Affero General Public License for more details.
#*
#*         You should have received a copy of the GNU Affero General Public License
#*         along with this program. If not, see <https://www.gnu.org/licenses/>.
#*
#* 注意事项: 请严格遵守GNU AGPL v3.0协议使用本代码，任何未经授权的商业用途均属侵权行为。
#*******************************************************************************/

import base64
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
from pathlib import Path

def decrypt_dsm_file(input_path: str, output_path: str, password: str = "pass") -> None:
    """
    解密 .dsm 文件并保存为明文文本

    Args:
        input_path:  输入的 .dsm 文件路径
        output_path: 输出的解密文件路径
        password:    解密密码

    Raises:
        FileNotFoundError: 输入文件不存在
        ValueError: 解密失败（密码错误或文件损坏）
    """
    if not Path(input_path).exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    try:
        # 读取文件（自动去除 BOM 头）
        with open(input_path, 'r', encoding='utf-8-sig') as f:
            encrypted_base64 = f.read().strip()

        # 确保 base64 是纯 ASCII（移除非法字符）
        encrypted_base64 = ''.join(char for char in encrypted_base64 if ord(char) < 128)

        # 生成密钥和 IV
        salt = b'salt\xe3\x81\xaf\xe5\xbf\x85\xe3\x81\x9a8\xe3\x83\x90\xe3\x82\xa4\xe3\x83\x88\xe4\xbb\xa5\xe4\xb8\x8a'
        key_iv = PBKDF2(password.encode('utf-8'), salt, dkLen=32 + 16, count=1000)
        key, iv = key_iv[:32], key_iv[32:]

        # AES-256 CBC 解密
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(base64.b64decode(encrypted_base64)), AES.block_size)

        # 保存解密后的文本
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(decrypted_data.decode('utf-8'))

        print(f"✅ 解密成功: {Path(input_path).name} -> {Path(output_path).name}")

    except Exception as e:
        raise ValueError(f"解密失败: {e}")

def main():
    print("=== DSM 文件批量解密工具 ===")
    print("说明:")
    print("- 密码固定为 'pass'")
    print("- 批量将 .dsm 文件解密为 .txt 文件")
    print("----------------------------")
    input_dir = input("请输入包含DSM文件的文件夹路径: ").strip()
    output_dir = input("请输入解密后的输出文件夹路径: ").strip()

    if not os.path.isdir(input_dir):
        print(f"错误: 输入文件夹不存在 [{input_dir}]")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    dsm_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.dsm')]

    if not dsm_files:
        print("没有找到任何.dsm文件")
        sys.exit(0)

    print(f"\n找到 {len(dsm_files)} 个DSM文件，准备解密...")
    success_count = 0

    for filename in dsm_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")

        try:
            decrypt_dsm_file(input_path, output_path)
            success_count += 1
        except Exception as e:
            print(f"❌ 解密失败 {filename}: {e}")

    print(f"\n处理完成: 成功 {success_count}/{len(dsm_files)} 个文件")

if __name__ == "__main__":
    main()
