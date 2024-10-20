import numpy as np
import copy
from benchmarks import Sphere, Rastrigin, RozenBlock
    
class solution:
    def __init__(self, dim):
        self.vector = np.zeros(dim)
        self.aim = np.zeros(dim)
        self.eval = 0.0
        self.eval_aim = 0.0
        self.dim = dim
            
    def __str__(self):
        sol = "個体：["
        for i in range(self.dim):
            if not i == self.dim - 1:
                sol += str (self.vector[i]) + ", "
            else:
                sol += str (self.vector[i]) + " ]\n"
                
        sol += f"評価値：{self.eval}"
        return sol
    
    def __lt__(self, other):
        return self.eval < other.eval
    
    def get_vector(self):
        return self.vector
    
    def set_vector(self, x):
        self.vector = x
        
    def get_aim(self):
        return self.aim
        
    def set_aim(self, x):
        self.aim = x
        
    def get_eval(self):
        return self.eval
    
    def set_eval(self, eval):
        self.eval = eval
    
    def get_eval_aim(self):
        return self.eval_aim

    def set_eval_aim(self, eval):
        self.eval_aim = eval
    
class DE:
    #スケール因子[0, 2]
    F = 0.5
    #交叉率[0,1]
    CR = 0.75
    
    def __init__(self, pop_size, dim, seed, max, min):
        #シード値の設定
        np.random.seed(seed)
        
        #集団サイズ
        self.pop_size = pop_size
        
        #最大値と最小値
        self.max = max
        self.min = min
        
        #交叉に用いるインデックスを求めるのに使うリスト
        self.all_list = []
        
        #集団を保持するリスト
        self.population = []
        
        #交叉に用いるインデックスのリストと集団の初期化
        for i in range(self.pop_size):
            self.all_list.append(i)
            sol = solution(dim)
            self.population.append(sol)
                
        #次元数
        self.dim = dim
        
    def initialize_population(self, function):
        for i in range(self.pop_size):
            #ベクトルの生成と評価値の計算
            vec = np.random.rand(self.dim) * (self.max - self.min) + self.min
            eval = function(vec)
            
            #ベクトルと評価値をそれぞれ個体にセットする．
            self.population[i].set_vector(vec)
            self.population[i].set_eval(eval)
            
    def generate_aim_vector(self, function):
        
        for i in range(self.pop_size):
            cross_index = np.random.randint(0, self.dim)
            
            select_list = copy.deepcopy(self.all_list)
            select_list.pop(i)
            
            #交叉に用いる親子体の選択
            index_list = np.random.choice(select_list, 3, replace = False)
            parent_0 = self.population[index_list[0]].get_vector()
            parent_1 = self.population[index_list[1]].get_vector()
            parent_2 = self.population[index_list[2]].get_vector()
            
            #突然変異ベクトルの作成
            mutation_vector = parent_0 + DE.F * (parent_1 - parent_2)
            
            #比較対象のベクトルを作成する．
            aim_vec = np.zeros(self.dim)
            for j in range(self.dim):
                if np.random.rand() < DE.CR or j == cross_index:
                    aim_vec[j] = mutation_vector[j]
                else:
                    aim_vec[j] = self.population[i].get_vector()[j]
            
            evel_aim = function(aim_vec)
        
            #aim_vectorとaim_evalをセットする．
            self.population[i].set_aim(aim_vec)
            self.population[i].set_eval_aim(evel_aim)
    
    def update_population(self):
        #aimと解の比較を行い，集団を更新する．
        for i in range(self.pop_size):
            #xとaimの評価値同士を比較し，aimの方が良ければpopulationの個体として更新．
            if self.population[i].get_eval_aim() < self.population[i].get_eval():
                self.population[i].set_vector(self.population[i].get_aim())
                self.population[i].set_eval(self.population[i].get_eval_aim())
                
    def do_one_generation(self, function):
            self.generate_aim_vector(function)
            self.update_population()
                
    def get_best_solution(self):
        return sorted(self.population)[0]
    
    def get_sorted_solutions(self):
        return sorted(self.population)

#---------------------------------パラメータ----------------------------------------------
pop_size = 100 #集団サイズ（ここは随時調整）
dim = 50 #次元数(決定変数の数)
max = 5.0 #集団を初期化する範囲の最大値
min = -5.0 #集団を初期化する範囲の最小値
seed = 0 #乱数シード(結果の再現性のため)

function = Sphere #解きたいタスク

iteration = 1000 #探索を行う世代数
#------------------------------------------------------------------------------------------

#インスタンスの初期化 
de = DE(pop_size = pop_size, dim = dim, max = max, min = min, seed = seed)

de.initialize_population(function = function) #集団を初期化し，各解の評価値の計算を行う．

#以下のループ内で探索を行う．
for i in range(iteration):
    de.do_one_generation(function = function) #探索を1世代進める
    print(de.get_best_solution()) #現世代における最良解の出力