# coding=utf-8


class Category:
    categories = [
        [1, "VR", "vr"],
        [2, "人工智能", "ai"],
        [3, "智能硬件", "hardware"],
        [4, "游戏&直播", "game"],
        [5, "物联网", "iot"],
        [6, "医疗健康", "medical"],
        [7, "教育", "education"],
        [8, "互联网金融", "finance"],
        [9, "手机", "mobile"],
        [10, "企业服务", "enterprise"],
        [11, "汽车", "car"],
        [12, "电商", "ecommerce"],
        [13, "O2O", "o2o"],
        [14, "资本", "capital"],
        [15, "旅游", "travel"],
        [16, "评测", "evaluation"],
        [17, "物流", "logistics"],
        [18, "体育", "sport"],
        [19, "农业", "agriculture"],
        [20, "社交", "sns"],
        [21, "工具", "tool"],
        [22, "娱乐", "entertainment"],
        [23, "家居", "furniture"],
        [24, "文创", "culture"],
        [25, "房产", "property"],
        [26, "其他", "others"]]

    def __init__(self):
        self.n2c = dict([(row[0], row[1]) for row in self.categories])
        self.n2e = dict([(row[0], row[2]) for row in self.categories])
        self.c2n = dict([(row[1], row[0]) for row in self.categories])
        self.c2e = dict([(row[1], row[2]) for row in self.categories])
        self.e2n = dict([(row[2], row[0]) for row in self.categories])
        self.e2c = dict([(row[2], row[1]) for row in self.categories])

