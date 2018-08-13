# PoemMining
Chinese Classic Poem Mining Project including corpus buiding by spyder and content analysis by nlp methods, 基于爬虫与nlp的中国古代诗词文本挖掘项目

# 项目介绍
中国古代诗词文化无疑是文化瑰宝，如何运用计量语言学方法对古代诗词进行挖掘，将有重要意义，本项目将从以下几个方面进行尝试:  
１）基于诗词集合的诗人画像生成  
２）基于诗词集合的诗人地点足迹识别  
３）基于诗词集合的相似诗人聚类,  基于ATM模型，user2vec模型  
４）基于诗词集合的情绪分类，标签自动生成  
５）基于诗词集合的意象挖掘  

# 项目结构
项目主要包括两个任务:    
1) 古代诗词语料库的构建     
2) 基于古代诗词语料库的挖掘

# 脚本结构
1, poem_spider.py:主要完成古代诗词语料库的构建，选取的是古诗文网 (https://so.gushiwen.org)，结果已经保存至corpus_poem.zip文件当中  
2, poem_process.py:主要基于构建起来的古诗词语料库，进行基础的文本分析，根据网站上的用户交互信息，得到古诗词文本本身的外部信息  
3, atm_model.py:利用作者－主题模型，对古诗词进行主题分析，最终目的是实现作者主题分布与风格聚类  
4, location_mining.py:基于诗人百科生平记事的地点挖掘与可视化，最终最终实现对诗人关联地点的一键生成．  
# 阶段性成果
1, 古代诗词语料库,一共采集到92127首古代诗词
2, 古代诗词外部计量分析结果，结果保存至result文件夹
3, 诗人足迹一键生成，示例如下：
李白足迹
![image](https://github.com/liuhuanyong/PoemMining/blob/master/image/libai.png)
李清照足迹
![image](https://github.com/liuhuanyong/PoemMining/blob/master/image/libai.png)
苏轼足迹
![image](https://github.com/liuhuanyong/PoemMining/blob/master/image/sushi.png)
文天祥足迹
![image](https://github.com/liuhuanyong/PoemMining/blob/master/image/wtx.png)
