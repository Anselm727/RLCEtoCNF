"""
错误向量生成器模块
用于生成随机错误向量
"""

import numpy as np
import random
from typing import List, Tuple


class ErrorGenerator:
    def __init__(self, seed: int = None):
        """
        初始化错误向量生成器
        
        Args:
            seed (int): 随机数种子，用于可重现的结果
        """
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
    
    def generate_random_error(self, length: int, max_errors: int) -> np.ndarray:
        """
        生成随机错误向量
        
        Args:
            length (int): 错误向量的长度
            max_errors (int): 最大错误数量
            
        Returns:
            np.ndarray: 错误向量
        """
        error_vector = np.zeros(length, dtype=int)
        
        # 随机选择错误位置
        num_errors = random.randint(1, min(max_errors, length))
        error_positions = random.sample(range(length), num_errors)
        
        # 在错误位置设置非零值
        for pos in error_positions:
            error_vector[pos] = random.randint(1, 255)  # GF(2^8)中的非零值
        
        return error_vector
    
    def generate_weight_t_error(self, length: int, weight: int) -> np.ndarray:
        """
        生成指定重量的错误向量
        
        Args:
            length (int): 错误向量的长度
            weight (int): 错误向量的重量（非零元素个数）
            
        Returns:
            np.ndarray: 错误向量
        """
        if weight > length:
            raise ValueError("错误重量不能超过向量长度")
        
        error_vector = np.zeros(length, dtype=int)
        error_positions = random.sample(range(length), weight)
        
        for pos in error_positions:
            error_vector[pos] = random.randint(1, 255)
        
        return error_vector
    
    def generate_burst_error(self, length: int, burst_start: int, burst_length: int) -> np.ndarray:
        """
        生成突发错误向量
        
        Args:
            length (int): 错误向量的长度
            burst_start (int): 突发错误开始位置
            burst_length (int): 突发错误长度
            
        Returns:
            np.ndarray: 错误向量
        """
        if burst_start + burst_length > length:
            raise ValueError("突发错误超出向量范围")
        
        error_vector = np.zeros(length, dtype=int)
        
        for i in range(burst_start, burst_start + burst_length):
            if random.random() < 0.7:  # 70%概率出现错误
                error_vector[i] = random.randint(1, 255)
        
        return error_vector 