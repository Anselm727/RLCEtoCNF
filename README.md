# RLCE到CNF转换工具

一个将Reed-Solomon Like Code Encryption (RLCE)方案转换为CNF（Conjunctive Normal Form）格式的工具包。

## 项目概述

本项目实现了RLCE密码方案到CNF格式的转换，主要用于密码分析和SAT求解器研究。该工具可以：

1. 生成RLCE密码方案的公钥矩阵
2. 创建随机错误向量
3. 将线性方程系统转换为CNF格式
4. 输出标准的DIMACS CNF文件

## 项目结构

```
RLCEtoCNF/
├── src/                    # 源代码目录
│   ├── core/              # 核心模块
│   │   ├── field_math.py  # 有限域数学运算
│   │   ├── rlce.py        # RLCE方案实现
│   │   └── cnf_converter.py # CNF转换器
│   ├── utils/             # 工具模块
│   │   ├── config.py      # 配置管理
│   │   └── error_generator.py # 错误向量生成
│   └── main.py            # 主程序入口
├── tests/                 # 测试文件
├── examples/              # 使用示例
├── run.py                 # 快速运行脚本
├── run.bat                # Windows批处理脚本
├── requirements.txt       # 依赖包
└── README.md             # 项目说明
```

## 安装和环境配置

### 环境要求

- Python 3.7+
- NumPy >= 1.21.0
- SciPy >= 1.7.0
- reedsolo >= 1.5.4

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 快速运行（推荐）

#### Linux/macOS:
```bash
python run.py
```

#### Windows:
```bash
run.bat
# 或者
python run.py
```

### 命令行使用

```bash
# 使用默认参数
python run.py

# 自定义参数
python run.py --n 15 --k 7 --t 2 --m 4 --w 4 --seed 42

# 使用配置文件
python run.py --config config.json

# 指定输出目录
python run.py --output-dir my_output --cnf-file my_output.cnf

# 直接调用主程序
python src/main.py --help
```

### 参数说明

- `n`: 消息+ECC的总长度（默认：15）
- `k`: 消息长度（默认：7）
- `t`: 错误纠正能力（默认：2）
- `m`: 有限域的指数（默认：4）
- `w`: 插入的列数（默认：4）
- `seed`: 随机数种子（可选）
- `output-dir`: 输出目录（默认：output）
- `cnf-file`: CNF文件名（默认：output.cnf）

### 编程接口使用

```python
from src.main import RLCEToCNF
from src.utils.config import RLCEConfig

# 创建配置
config = RLCEConfig(n=15, k=7, t=2, m=4, w=4, seed=42)

# 创建转换器并运行
converter = RLCEToCNF(config)
cnf_file = converter.run()

print(f"CNF文件已生成: {cnf_file}")
```

## 输出文件

运行后会在输出目录中生成以下文件：

- `output.cnf`: 标准DIMACS格式的CNF文件
- `public_key.npy`: RLCE公钥矩阵（NumPy格式）
- `error_vector.npy`: 错误向量（NumPy格式）
- `config.json`: 使用的配置参数
- `rlce_to_cnf.log`: 运行日志

## 配置管理

### 保存配置

```python
from src.utils.config import RLCEConfig

config = RLCEConfig(n=31, k=15, t=4, m=5, w=6)
config.save_to_file("my_config.json")
```

### 加载配置

```python
config = RLCEConfig.load_from_file("my_config.json")
```

## 运行示例

查看 `examples/` 目录中的示例文件：

```bash
# 运行基本示例
python examples/basic_example.py
```

## 运行测试

```bash
# 运行所有测试
python -m unittest discover tests/

# 运行特定测试
python tests/test_rlce.py
```

## 算法原理

### RLCE方案

1. **Reed-Solomon码生成**: 基于Reed-Solomon码构造广义生成矩阵
2. **矩阵变换**: 通过稀疏矩阵、置换矩阵等变换隐藏码结构
3. **公钥生成**: 生成最终的公钥矩阵

### CNF转换

1. **二进制表示**: 将有限域元素转换为二进制表示
2. **XOR约束**: 将线性方程转换为XOR约束
3. **CNF编码**: 将XOR约束编码为CNF子句

## 技术特点

- **模块化设计**: 清晰的模块分离，易于维护和扩展
- **配置灵活**: 支持命令行参数和配置文件
- **日志记录**: 详细的运行日志和错误处理
- **测试覆盖**: 完整的单元测试
- **类型提示**: 支持Python类型提示
- **跨平台**: 支持Windows、Linux、macOS

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目基于MIT许可证开源。详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请通过GitHub Issues联系。

## 更新日志

### v1.0.0
- 初始版本发布
- 实现完整的RLCE到CNF转换功能
- 提供命令行和编程接口
- 包含完整的测试和示例
- 模块化重构，清理旧代码
- 添加快速运行脚本 