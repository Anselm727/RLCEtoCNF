"""
RLCE方案核心实现模块
实现Reed-Solomon Like Code Encryption方案
"""

import numpy as np
import numpy.matlib
import scipy.linalg
import reedsolo as rs
from .field_math import FieldMath

class RLCE:
    def __init__(self, n, k, t, m, w):
        """
        初始化RLCE方案
        
        Args:
            n (int): 消息+ECC的总长度
            k (int): 消息长度
            t (int): 错误纠正能力
            m (int): 有限域的指数
            w (int): 插入的列数
        """
        self.n = n
        self.k = k
        self.t = t
        self.m = m
        self.w = w
        self.nsym = n - k  # ECC长度
        self.field_math = FieldMath(m)
        
    def generate_rs_poly(self):
        """生成Reed-Solomon码生成多项式"""
        return rs.rs_generator_poly(self.nsym)
    
    def expand_poly(self, g0):
        """扩展生成多项式"""
        g1 = np.frombuffer(g0, dtype=np.uint8)
        g2 = np.pad(g1, (0, self.n-len(g1)), 'constant')
        return np.array(g2)
    
    def generate_grs_matrix(self, g):
        """生成广义Reed-Solomon码生成矩阵"""
        g = self.expand_poly(g)
        GRS = g
        for i in range(1, self.k):
            g = np.roll(g, 1)
            GRS = np.concatenate((GRS, g))
        return np.array(GRS.reshape(self.k, self.n))
    
    def generate_v_matrix(self):
        """生成V矩阵"""
        a = np.random.randint(1, self.n-2, self.n)
        return np.diag(a)
    
    def generate_gs_matrix(self, g):
        """生成Gs矩阵"""
        A = self.generate_grs_matrix(g)
        B = self.generate_v_matrix()
        return self.field_math.matrix_mul(A, B)
    
    def generate_r_matrix(self):
        """生成R矩阵"""
        return np.random.randint(1, self.n, size=(self.k, self.w))
    
    def generate_g1_matrix(self, g):
        """生成G1矩阵"""
        m = self.generate_gs_matrix(g)
        RB = self.generate_r_matrix()
        for j in range(self.w):
            x = np.random.randint(1, self.n)
            m = np.insert(m, x, RB[:, j], axis=1)
        return m
    
    def generate_a_matrix(self):
        """生成稀疏矩阵A"""
        IA = np.matlib.eye(self.n-self.w, dtype=int)
        for i in range(self.w):
            while True:
                A = np.random.randint(0, self.n-1, (2, 2))
                if np.linalg.det(A) != 0:
                    break
            IA = scipy.linalg.block_diag(IA, A)
        return IA
    
    def generate_g2_matrix(self, g):
        """生成G2矩阵"""
        a = self.generate_g1_matrix(g)
        b = self.generate_a_matrix()
        return self.field_math.matrix_mul(a, b)
    
    def generate_permutation_matrix(self):
        """生成置换矩阵P"""
        x = np.matlib.eye(self.n+self.w, dtype=int)
        return np.random.permutation(x)
    
    def generate_g3_matrix(self, g):
        """生成G3矩阵"""
        return self.field_math.matrix_mul(
            self.generate_g2_matrix(g),
            self.generate_permutation_matrix()
        )
    
    def generate_s_matrix(self):
        """生成非奇异矩阵S"""
        while True:
            x = np.random.randint(0, self.n-1, (self.k, self.k))
            if np.linalg.det(x) != 0:
                break
        return x
    
    def generate_public_key(self):
        """生成公钥"""
        g0 = self.generate_rs_poly()
        return self.field_math.matrix_mul(
            self.generate_s_matrix(),
            self.generate_g3_matrix(g0)
        ) 