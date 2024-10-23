import numpy as np
import math

from benchmarks import Sphere, Rastrigin, RozenBlock

#集団内の個体に評価値を与える．
def evaluate(func, poplation):
    pop_size = len(poplation)
    for i in range(pop_size):
        eval = func(poplation[i].get_x())
        poplation[i].set_eval(eval)
        

class solution:
    def __init__(self, dim):
        self.x = np.zeros(dim)
        self.y = np.zeros(dim)
        self.z = np.zeros(dim)
        self.dim = dim
        self.eval = 0.0
            
    def __str__(self):
        sol = "個体：["
        for i in range(self.dim):
            if not i == self.dim - 1:
                sol += str (self.x[i]) + ", "
            else:
                sol += str (self.x[i]) + " ]\n"
                
        sol += f"評価値：{self.eval}"
        return sol
    
    def __lt__(self, other):
        return self.eval < other.eval

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x
        
    def get_y(self):
        return self.y
    
    def set_y(self, y):
        self.y = y
    
    def get_z(self):
        return self.z
    
    def set_z(self, z):
        self.z = z

    def get_eval(self):
        return self.eval
        
    def set_eval(self, eval):
        self.eval = eval
        
    
class cmaes:
    def __init__(self, dim, pop_size, m, sigma, seed):
        np.random.seed(seed)
        #集団の保持
        self.population = []
        for _ in range(pop_size):
            sol = solution(dim)
            self.population.append(sol)
                    
        #次元数
        self.dim = dim
        
        #平均ベクトル，ステップサイズ，コレスキー分解行列B, 共分散行列C=BB^T
        self.m = np.ones(dim) * m
        self.sigma = sigma
        self.C = np.eye(dim)
        self.B = np.linalg.cholesky(self.C)

        
        #dy, dz
        self.dy = np.zeros(dim)
        self.dz = np.zeros(dim)
        
        #進化パスの初期化
        self.p_sigma = np.zeros(dim)
        self.p_c = np.zeros(dim)
        self.h_sigma = 0.0
        
#----------------------------------------------------ハイパーパラメータ-------------------------------------------        
        #集団サイズ
        self.pop_size = pop_size
        
        #パラメータの更新に使用する数\muの初期化
        self.mu = math.ceil(pop_size / 2)
        
        #重みの初期化
        self.w = np.zeros(self.pop_size)
        
        #重みの初期化
        self.w_tmp = np.zeros(pop_size)
        for i in range(pop_size):
            tmp_value = np.log(((float(pop_size) + 1.0) / 2.0) ) - np.log(i + 1)
            if 0.0 < tmp_value and i < self.mu:
                self.w_tmp[i] = tmp_value
                
        sum =  np.sum(self.w_tmp)        
        for i in range(pop_size):
            self.w[i] = (self.w_tmp[i] / sum)
        
        mu_eff = 0.0
        for i in range(pop_size):
            mu_eff += (float(self.w[i]) * float(self.w[i]))
        
        self.mu_eff = 1.0 / mu_eff
        
        #X_d E||N(0, I)||の近似値
        self.X_d = np.sqrt(dim) * (1.0 - (1.0 / (4.0 * float(dim))) + (1.0 / (21.0 * float (dim) * float (dim))))
        
        self.c_sigma = (self.mu_eff + 2.0) / (float(dim) + self.mu_eff + 5.0)   
        self.c_c = (4.0 + (self.mu_eff / float(dim))) / (4.0 + float(self.dim) + (2.0 * self.mu_eff / float(dim)))
        
        self.d_sigma = 1.0  +  self.c_sigma
        tmp = np.sqrt((self.mu_eff - 1.0) / (float (self.dim) + 1.0)) - 1.0

        if 0.0 < tmp:
            self.d_sigma += 2.0 * tmp
            
        #平均ベクトルの学習率
        self.Eta_m = 1.0
        self.Eta_c1 = 2.0 / (((float(self.dim) + 1.3) * (float(self.dim) + 1.3)) + self.mu_eff)
        self.Eta_cmu = 1.0 - self.Eta_c1
        tmp = (2.0 * (self.mu_eff - 2.0 + (1.0 / self.mu_eff))) / ((self.dim + 2) * (self.dim + 2) + self.mu_eff)
        if tmp < self.Eta_cmu:
            self.Eta_cmu = tmp
#--------------------------------------------------------------------------------------------------------------
        
    #個体のサンプリングを行う．     
    def sampling(self):
        for i in range(self.pop_size):
            z = np.random.normal(0.0, 1.0, self.dim)
            self.population[i].set_z(z)
            self.population[i].set_y(np.dot(self.B, z))
            self.population[i].set_x(self.sigma *  np.dot(self.B, z) + self.m)
                        
    #集団内の個体をソートする
    def sort(self): 
        self.population.sort()
        
    def calc_dy_dz(self):
        self.dy = np.zeros(self.dim)
        self.dz = np.zeros(self.dim)
        for i in range(self.pop_size):
            self.dy += self.w[i] * self.population[i].get_y()
            self.dz += self.w[i] * self.population[i].get_z()
            
    #進化パスの計算を行う．
    def calc_evolution_path(self): 
        #p_sigmaの計算
        self.p_sigma = (1.0 - self.c_sigma) * self.p_sigma + np.sqrt(self.c_sigma * (2.0 - self.c_sigma) * self.mu_eff) * self.dz
        
        #h_sigmaの決定
        tmp = (1.4 + (2.0 / float (self.dim + 1.0))) * self.X_d
        p_sigma_norm = np.linalg.norm(self.p_sigma)
        if p_sigma_norm < tmp:
            self.h_sigma = 1.0
        else:
            self.h_sigma = 0.0
            
        #p_cの計算
        self.p_c = (1.0 - self.c_c) * self.p_c + self.h_sigma * np.sqrt(self.c_sigma * (2.0 - self.c_sigma) * self.mu_eff) * self.dy
                    
    def update_parameters(self):
        #平均ベクトルmの更新
        self.m = self.m + self.Eta_m * self.sigma * self.dy

        # 共分散行列Cの更新
        matrix = np.zeros((self.dim, self.dim))
        for i in range(self.mu):
            tmp = self.population[i].get_y()
            tmp = tmp.reshape(self.dim, 1)
            matrix += self.w[i] * (np.dot(tmp, tmp.T))
                
        tmp = self.p_c.reshape(self.dim, 1)
        self.C = (1.0 - self.Eta_c1 - self.Eta_cmu) * self.C + self.Eta_c1 * np.dot(tmp, tmp.T) + self.Eta_cmu * matrix        
        
        #共分散行列Cに対してコレスキー分解を行い行列Bを保存する.(C = BB^T)
        self.B = np.linalg.cholesky(self.C)
                
        #ステップサイズσの更新
        self.sigma = self.sigma * np.exp((self.c_sigma / self.d_sigma) * ((np.linalg.norm(self.p_sigma) / self.X_d) - 1.0))
        
    #探索を1世代進める．
    def do_one_generation(self):
        self.sort()
        self.calc_dy_dz()
        self.calc_evolution_path()
        self.update_parameters()
        
    def get_population(self):
        return self.population
    
    def get_best_solution(self):
        self.population.sort()
        return self.population[0]
    
    def get_worst_solution(self):
        self.population.sort()
        return self.population[self.pop_size - 1]
    
    def get_m(self):
        return self.m
    

#---------------------------------パラメータ----------------------------------------------
dim = 30 #次元数(決定変数の数)
pop_size = 4  + int(math.ceil(3 * np.log(dim))) #集団サイズ：推奨値は4 + int(math.ceil(3 * np.log(dim)))
m = 3.0 #探索開始時の平均ベクトル 例：m = 3.0のとき，m = [3.0, 3.0, ...,3.0]^{dim}から探索を開始
sigma = 5.0 #探索開始時の標準偏差
seed = 1 #乱数シード(結果の再現性のため)

func = RozenBlock #解きたいタスク

iteration = 10000 #探索を行う世代数
#------------------------------------------------------------------------------------------

#インスタンスの初期化
es = cmaes(dim = dim, pop_size = pop_size, m = m, sigma = sigma, seed = seed)

#以下のループ内で探索を行う．
for itr in range(iteration):
    es.sampling() #解のサンプリング
    evaluate(func = func, poplation = es.get_population()) #各解の評価値の計算
    es.do_one_generation() #探索を1世代進める
    print(es.get_best_solution()) #現世代における最良解の出力