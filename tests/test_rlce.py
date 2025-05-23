"""
RLCE模块测试
"""

import unittest
import numpy as np
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.rlce import RLCE
from core.field_math import FieldMath
from utils.config import RLCEConfig
from utils.error_generator import ErrorGenerator


class TestRLCE(unittest.TestCase):
    def setUp(self):
        """测试设置"""
        self.config = RLCEConfig(n=15, k=7, t=2, m=4, w=4)
        self.rlce = RLCE(self.config.n, self.config.k, self.config.t, 
                        self.config.m, self.config.w)
    
    def test_config_validation(self):
        """测试配置验证"""
        # 有效配置
        self.assertTrue(self.config.validate())
        
        # 无效配置
        with self.assertRaises(ValueError):
            invalid_config = RLCEConfig(n=5, k=10)  # n <= k
            invalid_config.validate()
    
    def test_field_math(self):
        """测试有限域数学运算"""
        field = FieldMath(4)
        
        # 测试基本运算
        a, b = 3, 5
        result_mul = field.gf_mul(a, b)
        result_add = field.gf_add(a, b)
        
        self.assertIsInstance(result_mul, int)
        self.assertIsInstance(result_add, int)
    
    def test_rlce_generation(self):
        """测试RLCE系统生成"""
        # 测试各个矩阵生成
        g0 = self.rlce.generate_rs_poly()
        self.assertIsNotNone(g0)
        
        grs_matrix = self.rlce.generate_grs_matrix(g0)
        self.assertEqual(grs_matrix.shape, (self.config.k, self.config.n))
        
        public_key = self.rlce.generate_public_key()
        self.assertEqual(public_key.shape[0], self.config.k)
    
    def test_error_generator(self):
        """测试错误向量生成器"""
        error_gen = ErrorGenerator(seed=42)
        
        # 测试随机错误
        error_vec = error_gen.generate_random_error(10, 3)
        self.assertEqual(len(error_vec), 10)
        self.assertLessEqual(np.count_nonzero(error_vec), 3)
        
        # 测试固定重量错误
        weight_error = error_gen.generate_weight_t_error(15, 5)
        self.assertEqual(len(weight_error), 15)
        self.assertEqual(np.count_nonzero(weight_error), 5)


class TestConfig(unittest.TestCase):
    def test_config_save_load(self):
        """测试配置保存和加载"""
        config = RLCEConfig(n=20, k=10, t=3, m=5, w=6)
        
        # 保存配置
        test_file = "test_config.json"
        config.save_to_file(test_file)
        
        # 加载配置
        loaded_config = RLCEConfig.load_from_file(test_file)
        
        # 验证
        self.assertEqual(config.n, loaded_config.n)
        self.assertEqual(config.k, loaded_config.k)
        self.assertEqual(config.t, loaded_config.t)
        self.assertEqual(config.m, loaded_config.m)
        self.assertEqual(config.w, loaded_config.w)
        
        # 清理
        os.remove(test_file)


if __name__ == '__main__':
    unittest.main() 