"""
配置管理模块
管理RLCE方案的参数配置
"""

from dataclasses import dataclass
from typing import Optional
import json
import os


@dataclass
class RLCEConfig:
    """RLCE方案配置类"""
    n: int = 15          # 消息+ECC的总长度
    k: int = 7           # 消息长度
    t: int = 2           # 错误纠正能力
    m: int = 4           # 有限域的指数
    w: int = 4           # 插入的列数
    seed: Optional[int] = None  # 随机数种子
    output_dir: str = "output"   # 输出目录
    cnf_file: str = "output.cnf" # CNF输出文件名
    
    @property
    def nsym(self) -> int:
        """ECC长度"""
        return self.n - self.k
    
    def validate(self) -> bool:
        """验证配置参数的有效性"""
        if self.n <= self.k:
            raise ValueError("n必须大于k")
        if self.t <= 0:
            raise ValueError("t必须为正数")
        if self.m <= 0:
            raise ValueError("m必须为正数")
        if self.w <= 0:
            raise ValueError("w必须为正数")
        if self.k <= 0:
            raise ValueError("k必须为正数")
        return True
    
    def save_to_file(self, filepath: str):
        """保存配置到文件"""
        config_dict = {
            'n': self.n,
            'k': self.k,
            't': self.t,
            'm': self.m,
            'w': self.w,
            'seed': self.seed,
            'output_dir': self.output_dir,
            'cnf_file': self.cnf_file
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'RLCEConfig':
        """从文件加载配置"""
        with open(filepath, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return cls(**config_dict)
    
    @classmethod
    def get_default_config(cls) -> 'RLCEConfig':
        """获取默认配置"""
        return cls()
    
    def __str__(self) -> str:
        return f"RLCE配置: n={self.n}, k={self.k}, t={self.t}, m={self.m}, w={self.w}" 