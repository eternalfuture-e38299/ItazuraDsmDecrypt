# ItazuraDsmDecrypt

专为《いたずらゲームです》游戏设计的 DSM 文件批量解密工具，可将加密的 `.dsm` 文件解密为可读的 `.txt` 文本文件。

## 功能特性

- 批量解密 DSM 脚本文件
- 保留原始文件结构
- 自动处理 UTF-8 BOM 头
- 支持中文/日文路径
- 详细的错误报告

## 安装要求

- Python 3.7+
- 依赖库：`pycryptodome`

```bash
pip install pycryptodome
```

## 特别说明
* 该游戏支持直接读取txt，按理说不需要加密回去
