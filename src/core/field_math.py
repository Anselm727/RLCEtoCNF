"""
多项式域数学计算模块
提供在多项式域中进行数学计算的方法，用于矩阵的高斯消元
"""

import numpy as np
import reedsolo as rs

class FieldMath:
    def __init__(self, m, prim=None):
        """
        初始化FieldMath类
        
        Args:
            m (int): 有限域的指数
            prim: 本原多项式，如果为None则自动生成
        """
        self.m = m
        if prim is None:
            self.prim = rs.find_prime_polys(c_exp=m, fast_primes=True, single=True)
        else:
            self.prim = prim
        rs.init_tables(prim=self.prim, generator=2, c_exp=m)
    
    def gf_mul(self, a, b):
        """多项式域乘法"""
        return rs.gf_mul(a, b)
    
    def gf_add(self, a, b):
        """多项式域加法"""
        return rs.gf_add(a, b)
    
    def gf_inverse(self, a):
        """多项式域求逆"""
        return rs.gf_inverse(a)
    
    def matrix_mul(self, A, B):
        """
        多项式域矩阵乘法
        
        Args:
            A: 第一个矩阵
            B: 第二个矩阵
            
        Returns:
            矩阵乘法结果
        """
        res = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for m in range(len(B)):
                    x = self.gf_mul(A[i][m], B[m][j])
                    res[i][j] = self.gf_add(res[i][j], x)
        return np.array(res) 