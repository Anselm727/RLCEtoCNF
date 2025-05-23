"""
RLCE到CNF转换工具主程序
"""

import os
import sys
import argparse
import logging
import numpy as np
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.rlce import RLCE
from core.cnf_converter import CNFConverter
from utils.config import RLCEConfig
from utils.error_generator import ErrorGenerator


class RLCEToCNF:
    def __init__(self, config: RLCEConfig):
        """
        初始化RLCE到CNF转换器
        
        Args:
            config: RLCE配置对象
        """
        self.config = config
        self.config.validate()
        
        # 创建输出目录
        os.makedirs(config.output_dir, exist_ok=True)
        
        # 初始化各个组件
        self.rlce = RLCE(config.n, config.k, config.t, config.m, config.w)
        self.cnf_converter = CNFConverter(
            config.m, config.n, config.w, config.k,
            os.path.join(config.output_dir, config.cnf_file)
        )
        self.error_generator = ErrorGenerator(config.seed)
        
        # 设置日志
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志配置"""
        log_file = os.path.join(self.config.output_dir, "rlce_to_cnf.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_rlce_system(self):
        """生成RLCE系统"""
        self.logger.info("开始生成RLCE系统...")
        self.logger.info(f"使用配置: {self.config}")
        
        # 生成公钥
        self.logger.info("生成RLCE公钥...")
        self.public_key = self.rlce.generate_public_key()
        self.logger.info(f"公钥矩阵形状: {self.public_key.shape}")
        
        # 生成错误向量
        self.logger.info("生成错误向量...")
        self.error_vector = self.error_generator.generate_weight_t_error(
            self.config.n + self.config.w, self.config.t
        )
        self.logger.info(f"错误向量重量: {np.count_nonzero(self.error_vector)}")
        
        return self.public_key, self.error_vector
    
    def convert_to_cnf(self, matrix, vector):
        """将矩阵方程转换为CNF"""
        self.logger.info("开始转换为CNF格式...")
        
        # 执行转换
        self.cnf_converter.convert_matrix_to_cnf(matrix, vector)
        
        # 写入CNF头部
        self.cnf_converter.write_cnf_header()
        
        self.logger.info(f"CNF文件已生成: {self.cnf_converter.output_file}")
        self.logger.info(f"变量数: {self.cnf_converter.variable_count}")
        self.logger.info(f"子句数: {self.cnf_converter.clause_count}")
        
        return self.cnf_converter.output_file
    
    def run(self):
        """运行完整的转换流程"""
        try:
            # 生成RLCE系统
            public_key, error_vector = self.generate_rlce_system()
            
            # 保存矩阵信息
            self._save_matrices(public_key, error_vector)
            
            # 转换为CNF
            cnf_file = self.convert_to_cnf(public_key, error_vector)
            
            self.logger.info("转换完成!")
            self.logger.info(f"输出文件: {cnf_file}")
            
            return cnf_file
            
        except Exception as e:
            self.logger.error(f"转换过程中出现错误: {str(e)}")
            raise
    
    def _save_matrices(self, public_key, error_vector):
        """保存矩阵到文件"""
        # 保存公钥矩阵
        pk_file = os.path.join(self.config.output_dir, "public_key.npy")
        np.save(pk_file, public_key)
        self.logger.info(f"公钥矩阵已保存: {pk_file}")
        
        # 保存错误向量
        error_file = os.path.join(self.config.output_dir, "error_vector.npy")
        np.save(error_file, error_vector)
        self.logger.info(f"错误向量已保存: {error_file}")
        
        # 保存配置
        config_file = os.path.join(self.config.output_dir, "config.json")
        self.config.save_to_file(config_file)
        self.logger.info(f"配置已保存: {config_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='RLCE到CNF转换工具')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--n', type=int, default=15, help='总长度 (默认: 15)')
    parser.add_argument('--k', type=int, default=7, help='消息长度 (默认: 7)')
    parser.add_argument('--t', type=int, default=2, help='错误纠正能力 (默认: 2)')
    parser.add_argument('--m', type=int, default=4, help='有限域指数 (默认: 4)')
    parser.add_argument('--w', type=int, default=4, help='插入列数 (默认: 4)')
    parser.add_argument('--seed', type=int, help='随机数种子')
    parser.add_argument('--output-dir', type=str, default='output', help='输出目录 (默认: output)')
    parser.add_argument('--cnf-file', type=str, default='output.cnf', help='CNF文件名 (默认: output.cnf)')
    
    args = parser.parse_args()
    
    # 加载或创建配置
    if args.config and os.path.exists(args.config):
        config = RLCEConfig.load_from_file(args.config)
    else:
        config = RLCEConfig(
            n=args.n, k=args.k, t=args.t, m=args.m, w=args.w,
            seed=args.seed, output_dir=args.output_dir, cnf_file=args.cnf_file
        )
    
    # 运行转换
    converter = RLCEToCNF(config)
    converter.run()


if __name__ == "__main__":
    main() 