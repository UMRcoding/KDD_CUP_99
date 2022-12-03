import csv
import sys
import os
import time

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

os.environ["PATH"] += os.pathsep + 'D:/DATA/ProgramData/Graphviz/bin'

import pydotplus
from sklearn import tree
from sklearn import model_selection as cv
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class AnalyseData():
    # 加载KDD数据集
    def load_data(self, filename):
        x = []
        with open(filename) as f:
            for line in f:
                line = line.strip('\n')
                line = line.split(',')
                x.append(line)
        return x

    def get_rootkit2andNormal(self, x):
        v = []
        w = []
        y = []
        # 筛选标记为KDD99和normal且是telent的数据
        for x1 in x:
            if (x1[41] in ['rootkit.', 'normal.']) and (x1[2] == 'telnet'):
                if x1[41] == 'rootkit.':
                    y.append(1)
                else:
                    y.append(0)

                x1 = x1[9:21]
                v.append(x1)
        # 挑选与Rookit相关的特征作为样本特征
        for x1 in v:
            v1 = []
            for x2 in x1:
                v1.append(float(x2))
            w.append(v1)
        # w: 符合筛选的数据中, 第10到22列的内容, 转float精度
        # y: 符合筛选的数据中, 是rootkit记录为1, 不是则为0
        return w, y


    def get_guess_passwdandNormal(self, x):
        v = []
        w = []
        y = []
        for x1 in x:
            if (x1[41] in ['guess_passwd.', 'normal.']) and (x1[2] == 'pop_3'):
                if x1[41] == 'guess_passwd.':
                    y.append(1)
                else:
                    y.append(0)

                x1 = [x1[0]] + x1[4:8] + x1[22:30]
                v.append(x1)

        for x1 in v:
            v1 = []
            for x2 in x1:
                v1.append(float(x2))
            w.append(v1)
        return w, y

    def get_apache2andNormal(self, x):
        v = []
        w = []
        y = []
        for x1 in x:
            if (x1[41] in ['apache2.', 'normal.']) and (x1[2] == 'http'):
                if x1[41] == 'apache2.':
                    y.append(1)
                else:
                    y.append(0)

                x1 = [x1[0]] + x1[4:8] + x1[22:30] + x1[31:40]
                # x1 = x1[4:8]
                v.append(x1)

        for x1 in v:
            v1 = []
            for x2 in x1:
                v1.append(float(x2))
            w.append(v1)
        return w, y

    def DataConvy(self):
        f = open('DataConvy.csv', 'w', encoding='utf-8-sig', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(['持续时间', '协议类型', '连接状态', '发送字节数', '接收字节数', '加急包个数', '访问敏感文件和目录次数', '登录失败次数','登录成功次数'])

        v = self.load_data('../KDD_Data/003-kddcup.data_10_percent_corrected')
        for i in v:
            csv_writer.writerow([i[0],i[1],i[3],i[4],i[5],i[8],i[9],i[10],i[11]] )
        f.close()
        print('写入成功')

    def ToCSV(self):
        f = open('AllData.csv', 'w', encoding='utf-8-sig', newline='')
        csv_writer = csv.writer(f)
        v = self.load_data('../KDD_Data/003-kddcup.data_10_percent_corrected')
        for i in v:
            csv_writer.writerow([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], [8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16], i[17], i[18], i[19], i[20], i[21], i[22], i[23], i[24], i[25], i[26], i[27], i[28], i[29], i[30], i[31], i[32], i[33], i[34], i[35], i[36], i[37], i[38], i[39], i[40], i[41]])
        f.close()
        print('写入成功')


    def KNN_01(self):
        v = self.load_data('../KDD_Data/003-kddcup.data_10_percent_corrected')
        # for i in data_list:
        #     print(i[1])

        x, y = self.get_rootkit2andNormal(v)
        # K近邻算法,选取最近的点的个数3
        clf = KNeighborsClassifier(n_neighbors=3)
        print(cv.cross_val_score(clf, x, y, n_jobs=-1, cv=10))

    def decide_Tree(self):
        v = self.load_data("../KDD_Data/003-kddcup.data_10_percent_corrected")
        x, y = self.get_guess_passwdandNormal(v)
        clf = tree.DecisionTreeClassifier()
        print(cv.cross_val_score(clf, x, y, n_jobs=-1, cv=10))

        clf = clf.fit(x, y)
        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_pdf("iris-dt.pdf")


    def main03(self):
        v = self.load_data("../KDD_Data/003-kddcup.data_10_percent_corrected")
        x, y = self.get_apache2andNormal(v)
        clf = GaussianNB()
        print(cv.cross_val_score(clf, x, y, n_jobs=-1, cv=10))

    def KNN_Select(self):
        start_time = time.perf_counter()

        # 加载数据
        df = pd.read_csv('D:\KDD_CUP_99\kdd_cup\DataConvy.csv')

        # 提取样本数据
        target = df['发送字节数']

        # 有许多特征与发送字节数无关，所以需要手动抽取关联特征
        # 提取出关联特征：1. 持续时间 2. 协议类型 3. 接收字节数 4. 加急包个数
        feature = df[['持续时间', '协议类型', '接收字节数', '加急包个数']]
        # feature.shape  # (494021, 4)  494021行 4列
        # target.shape   # (494021,)

        # 数据集拆分：拆分完观察样本数据中的特征是否需要特征工程。10%比例
        x_train, x_test, y_train, y_test = train_test_split(feature, target, test_size=0.1, random_state=2020)

        # 观察特征数据是否需要特征工程。协议类型为非数值型数据，需要特征值化，转换为数值型数据
        # x_train

        # 特征值化：对训练集特征进行手动onehot编码
        occ_one_hot = pd.get_dummies(x_train['协议类型'])
        # occ_one_hot

        # 将 occ_one_hot 与 x_train 进行级联。 x_train 为 DataFrame，axis=0表示行，axis=1表示列
        # pd.concat((x_train, occ_one_hot),axis=1)
        x_train = pd.concat((x_train, occ_one_hot), axis=1).drop(labels='协议类型', axis=1)
        # x_train

        # 对测试集特征进行手动onehot编码
        occ_one_hot_test = pd.get_dummies(x_test['协议类型'])
        # occ_one_hot_test

        # 对测试集级联
        x_test = pd.concat((x_test, occ_one_hot_test), axis=1).drop(labels='协议类型', axis=1)

        scores = []
        ks = []

        # 用学习曲线，寻找最优K值
        for i in range(1, 2):
            # 实例化
            knn = KNeighborsClassifier(n_neighbors=i, n_jobs = 4)

            # 训练模型
            knn.fit(x_train, y_train)

            # 训练好模型后进行评分
            score = knn.score(x_test, y_test)

            # 拿到不同K的得分
            scores.append(score)
            ks.append(i)

        # 转换为np数组
        scores_arr = np.array(scores)
        ks_arr = np.array(ks)

        # 绘图  参数：(自变量，因变量)
        plt.plot(ks_arr, scores_arr)
        plt.xlabel('k_value')
        plt.ylabel('score')

        # 找出最大值。scores_arr.argmax() 最大值下标
        max_k = ks_arr[scores_arr.argmax()]
        print('最优的K为', max_k)

        end_time = time.perf_counter()
        print("Running time:", (end_time - start_time))  # 输出程序运行时间

class Menu():
    def __init__(self):
        self.choices = {
            "00": AnalyseData().DataConvy,
            "01": AnalyseData().KNN_01,
            "02": AnalyseData().decide_Tree,
            "03": AnalyseData().main03,
            "04": AnalyseData().KNN_Select,
            "05": AnalyseData().ToCSV,
            "99": self.quit
        }

    def display_menu(self):
        print("""
操作菜单:
00. DataConvy
01. KNN
02. decide_Tree
03. main03
04. KNN_Select
05. ToCSV
99. 退出
""")

    def run(self):
        while True:
            self.display_menu()
            try:
                choice = input("键入选项: ")
            except Exception as e:
                print("\033[1;31m输入无效\033[0m")
                continue

            choice = str(choice).strip()
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} 不是有效选择".format(choice))

    def quit(self):
        print("\n感谢使用!\n")
        sys.exit(0)

if __name__ == '__main__':
    Menu().run()


