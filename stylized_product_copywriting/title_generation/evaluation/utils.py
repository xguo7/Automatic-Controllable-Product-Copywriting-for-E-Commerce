import jieba


def class_by_keyword(tokens):
    if len(set(['机身','外观','外壳']) & set(tokens))>0:
        a = 0
    elif len(set(['面容','解锁','指纹','人脸识别','面容ID']) & set(tokens))>0:
        a = 6          
    elif len(set(['屏','屏幕','英寸']) & set(tokens))>0:
        a = 1
    elif len(set(['网络','5G','双模']) & set(tokens))>0:
        a = 2
    elif len(set(['摄像头','三摄','四摄','广角','变焦','长焦','镜头','美颜','拍摄','镜头','后置','拍照','人像','单摄']) & set(tokens))>0:
        a = 3
    elif len(set(['处理器','存储','液冷','散热','内存','芯片']) & set(tokens))>0:
        a = 4
    elif len(set(['充电','续航','快充','电池']) & set(tokens))>0:
        a = 5          
    else:
        a = -1
    return a 



def stopwordslist():
    stopwords = [line.strip() for line in open('/home/xiaojie.guo/stylized_product_copywriting/topic_modeling/stop_words.txt', 'r', encoding='UTF-8').readlines()]
    stopwords.extend([])
    return stopwords

def seg_depart(sentence):
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr 

def check_multi(tokens):
    topic_words=[['拍摄', '镜头', '后置', '拍照','三摄','四摄','人像','单摄','散热', '液冷'],
    ['运行', '麒麟', '处理器', '骁龙', '高通', '大容量'],
    ['电池', '续航',  '持久', '快充', '电量', '充电','闪充'],
    ['解锁', '指纹','隐私'],
    ['屏',  '视野', '英寸', '屏幕','全面','显示屏','显示'],
    ['5G', '双模','双卡'],
    ['材料','防水','进水','外观','机身']]
    count=0
    for topic in topic_words:
        for word in tokens:
            if word in topic:
                count+=1
                break       
    return count   


class diagnose():
    def __init__(self, input_sentence, aspect, lda_model_path, lda_dct_path):
        self.txt = input_sentence
        self.aspect = aspect
        self.lda_model = lda_model_path
        self.lda_dic = lda_dct_path
        from pycorrector.macbert.macbert_corrector import MacBertCorrector

    def macbert_correct(self):
        m = MacBertCorrector()
        return m.macbert_correct(self.txt)

    def if_aspect(self):
        from eval_tool import classify, seg_depart
        tokens = [seg_depart(item).split(' ') for item in self.txt]
        lda_model = LdaModel.load(datapath(self.lda_model_name))
        lda_dct = Dictionary.load_from_text(self.lda_dct_path)
        if classify(tokens, lda_model, lda_dct) == self.aspect:
            return True
        else:
            return False

def class_by_keyword_1342(tokens):
    if len(set(['面料','布料','加绒','纯棉','亲肤','材质','手感','透气性','羊毛','毛呢','鸭绒','保暖','羽绒','鹅绒','填充',
    '涤纶']) & set(tokens))>0:
        a = 0   
    elif len(set(['身材','比例','修身','宽松','版型']) & set(tokens))>0:
        a = 1
    elif len(set(['格纹', '千鸟格','色','颜色','条纹','图案','印花','撞色','字母','竖纹','刺绣']) & set(tokens))>0:
        a = 2
    elif len(set(['口袋','插手','插袋','开袋','贴袋','插兜','物品']) & set(tokens))>0:
        a = 3
    elif len(set(['立领','圆领','衣领','领','翻领','领口','字领','颈部','高领','颈','尖领','连帽','帽']) & set(tokens))>0:
        a = 4
    elif len(set(['袖口','袖']) & set(tokens))>0:
        a = 5                          
    elif len(set(['时尚','复古','潮','个性','帅气','不羁','潮流','时髦','性感','休闲','潮酷']) & set(tokens))>0:
        a = 6     
    elif len(set(['百搭','配搭','搭','穿搭']) & set(tokens))>0:
        a = 7                               
    else:
        a = -1
    return a 


