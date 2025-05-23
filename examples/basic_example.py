"""
RLCE到CNF转换基本使用示例
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import RLCEToCNF
from utils.config import RLCEConfig


def basic_example():
    """基本使用示例"""
    print("=== RLCE到CNF转换基本示例 ===")
    
    # 创建配置
    config = RLCEConfig(
        n=15,           # 总长度
        k=7,            # 消息长度
        t=2,            # 错误纠正能力
        m=4,            # 有限域指数
        w=4,            # 插入列数
        seed=42,        # 随机数种子，确保可重现
        output_dir="example_output",
        cnf_file="example.cnf"
    )
    
    print(f"使用配置: {config}")
    
    # 创建转换器并运行
    converter = RLCEToCNF(config)
    cnf_file = converter.run()
    
    print(f"转换完成！输出文件: {cnf_file}")
    
    # 显示一些统计信息
    print(f"变量数: {converter.cnf_converter.variable_count}")
    print(f"子句数: {converter.cnf_converter.clause_count}")


def custom_parameters_example():
    """自定义参数示例"""
    print("\n=== 自定义参数示例 ===")
    
    # 使用更大的参数
    config = RLCEConfig(
        n=31,           # 更大的总长度
        k=15,           # 更大的消息长度
        t=4,            # 更强的错误纠正能力
        m=5,            # 更大的有限域
        w=6,            # 更多插入列
        seed=123,
        output_dir="custom_output",
        cnf_file="custom.cnf"
    )
    
    print(f"使用自定义配置: {config}")
    
    converter = RLCEToCNF(config)
    cnf_file = converter.run()
    
    print(f"自定义参数转换完成！输出文件: {cnf_file}")


def config_file_example():
    """配置文件示例"""
    print("\n=== 配置文件使用示例 ===")
    
    # 创建并保存配置到文件
    config = RLCEConfig(
        n=23,
        k=11,
        t=3,
        m=4,
        w=5,
        seed=999,
        output_dir="config_example_output",
        cnf_file="from_config.cnf"
    )
    
    config_file = "example_config.json"
    config.save_to_file(config_file)
    print(f"配置已保存到: {config_file}")
    
    # 从文件加载配置
    loaded_config = RLCEConfig.load_from_file(config_file)
    print(f"从文件加载的配置: {loaded_config}")
    
    # 使用加载的配置运行转换
    converter = RLCEToCNF(loaded_config)
    cnf_file = converter.run()
    
    print(f"从配置文件的转换完成！输出文件: {cnf_file}")
    
    # 清理配置文件
    os.remove(config_file)
    print(f"已删除临时配置文件: {config_file}")


if __name__ == "__main__":
    # 运行各种示例
    basic_example()
    custom_parameters_example()
    config_file_example()
    
    print("\n=== 所有示例完成 ===")
    print("请查看各个输出目录中的文件："
          "\n- example_output/"
          "\n- custom_output/"
          "\n- config_example_output/") 