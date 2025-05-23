"""
CNF转换器模块
将矩阵方程转换为CNF（Conjunctive Normal Form）格式
"""

import numpy as np
import os
from typing import List, Tuple
from .field_math import FieldMath


class CNFConverter:
    def __init__(self, m: int, n: int, w: int, k: int, output_file: str = "output.cnf"):
        """
        初始化CNF转换器
        
        Args:
            m (int): 有限域指数
            n (int): 消息长度
            w (int): 插入列数
            k (int): 消息维度
            output_file (str): 输出文件名
        """
        self.m = m
        self.n = n
        self.w = w
        self.k = k
        self.output_file = output_file
        self.field_math = FieldMath(m)
        self.clause_count = 0
        self.variable_count = 0
    
    def clear_output_file(self):
        """清空输出文件"""
        if os.path.exists(self.output_file):
            open(self.output_file, 'w').close()
    
    def write_clause(self, clause: str):
        """写入一个子句到文件"""
        with open(self.output_file, 'a') as f:
            f.write(f"{clause} 0\n")
        self.clause_count += 1
    
    def number_to_binary(self, num: int, bits: int) -> np.ndarray:
        """将数字转换为指定位数的二进制表示"""
        binary = []
        for i in range(bits):
            num, remainder = divmod(num, 2)
            binary.append(remainder)
        return np.array(binary).reshape(-1, 1)
    
    def generate_xor_cnf(self, variables: List[int], result: int):
        """
        生成XOR操作的CNF表示
        
        Args:
            variables: 参与XOR的变量列表
            result: XOR结果（0或1）
        """
        l = len(variables)
        
        if l == 1:
            if result == 1:
                self.write_clause(str(variables[0]))
            else:
                self.write_clause(str(-variables[0]))
        
        elif l == 2:
            if result == 1:
                self.write_clause(f"{variables[0]} {variables[1]}")
                self.write_clause(f"{-variables[0]} {-variables[1]}")
            else:
                self.write_clause(f"{variables[0]} {-variables[1]}")
                self.write_clause(f"{-variables[0]} {variables[1]}")
        
        elif l == 3:
            if result == 1:
                clauses = [
                    f"{-variables[0]} {-variables[1]} {variables[2]}",
                    f"{-variables[0]} {variables[1]} {-variables[2]}",
                    f"{variables[0]} {-variables[1]} {-variables[2]}",
                    f"{variables[0]} {variables[1]} {variables[2]}"
                ]
            else:
                clauses = [
                    f"{variables[0]} {variables[1]} {variables[2]}",
                    f"{-variables[0]} {variables[1]} {variables[2]}",
                    f"{variables[0]} {-variables[1]} {variables[2]}",
                    f"{variables[0]} {variables[1]} {-variables[2]}"
                ]
            
            for clause in clauses:
                self.write_clause(clause)
        
        elif l == 4:
            if result == 1:
                clauses = [
                    f"{variables[0]} {variables[1]} {variables[2]} {variables[3]}",
                    f"{-variables[0]} {-variables[1]} {-variables[2]} {-variables[3]}",
                    f"{-variables[0]} {-variables[1]} {variables[2]} {variables[3]}",
                    f"{-variables[0]} {variables[1]} {-variables[2]} {variables[3]}",
                    f"{-variables[0]} {variables[1]} {variables[2]} {-variables[3]}",
                    f"{variables[0]} {-variables[1]} {-variables[2]} {variables[3]}",
                    f"{variables[0]} {-variables[1]} {variables[2]} {-variables[3]}",
                    f"{variables[0]} {variables[1]} {-variables[2]} {-variables[3]}"
                ]
            else:
                clauses = [
                    f"{-variables[0]} {-variables[1]} {-variables[2]} {variables[3]}",
                    f"{-variables[0]} {-variables[1]} {variables[2]} {-variables[3]}",
                    f"{-variables[0]} {variables[1]} {-variables[2]} {-variables[3]}",
                    f"{-variables[0]} {variables[1]} {variables[2]} {variables[3]}",
                    f"{variables[0]} {-variables[1]} {-variables[2]} {-variables[3]}",
                    f"{variables[0]} {-variables[1]} {variables[2]} {variables[3]}",
                    f"{variables[0]} {variables[1]} {-variables[2]} {variables[3]}",
                    f"{variables[0]} {variables[1]} {variables[2]} {-variables[3]}"
                ]
            
            for clause in clauses:
                self.write_clause(clause)
    
    def convert_matrix_to_cnf(self, matrix: np.ndarray, vector: np.ndarray):
        """
        将矩阵方程转换为CNF格式
        
        Args:
            matrix: 系数矩阵
            vector: 结果向量
        """
        self.clear_output_file()
        
        # 计算变量总数
        self.variable_count = self.m * (self.n + self.w)
        
        # 为每个方程生成CNF子句
        for i in range(matrix.shape[0]):
            row = matrix[i]
            result_bit = vector[i] if i < len(vector) else 0
            
            # 获取非零元素的位置
            non_zero_indices = np.nonzero(row)[0]
            
            if len(non_zero_indices) == 0:
                continue
            
            if len(non_zero_indices) <= 4:
                # 直接处理小型XOR
                variables = [int(idx + 1) for idx in non_zero_indices]
                self.generate_xor_cnf(variables, result_bit)
            else:
                # 使用辅助变量处理大型XOR
                self._handle_large_xor(non_zero_indices, result_bit)
    
    def _handle_large_xor(self, indices: np.ndarray, result: int):
        """处理大型XOR操作，使用辅助变量分解"""
        # 实现大型XOR的分解逻辑
        # 这里可以进一步优化
        pass
    
    def write_cnf_header(self):
        """写入CNF文件头"""
        header = f"p cnf {self.variable_count} {self.clause_count}\n"
        
        # 读取现有内容
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        # 写入头部和内容
        with open(self.output_file, 'w') as f:
            f.write(header + content) 