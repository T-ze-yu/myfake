from faker import Faker
import random

class fake_time_place():
    def __init__(self, seed=None) -> None:
        self.fake = Faker(['zh_CN'])
        self.seed = seed
        if self.seed:
            Faker.seed(self.seed)
            random.seed(self.seed)
        self.number_list = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        self.function = {1:self.get_time, 2:self.get_year, 3:self.get_month, 4:self.get_country, 5:self.get_province, 6:self.get_place}

    #两位数转中文
    def num_cn(self, n):  
        if n<=10:
            return self.number_list[n]
        elif n%10==0:
            return self.number_list[n//10]+'十'
        elif n<20:
            return random.choice([self.number_list[n//10]+'十'+self.number_list[n%10], '十'+self.number_list[n%10]])
        else:
            return self.number_list[n//10]+'十'+self.number_list[n%10]  

    #获取日期/时间
    def get_time(self):
        tm = self.fake.date_time()
        ra = random.random()
        year = str(tm.year)
        year_cn = ''
        for i in year:
            year_cn += self.number_list[int(i)]      #中文年
        #一位数时在两位与一位随机
        month = random.choice([str(tm.month),'0'+str(tm.month)]) if tm.month<10 else str(tm.month)
        month_cn = self.num_cn(tm.month)     #中文月
        # month_cn = self.number_list[tm.month] if tm.month<=10 else '十'+self.number_list(int(month[1]))     #中文月

        day = random.choice([str(tm.day),'0'+str(tm.day)]) if tm.day<10 else str(tm.day)
        day_cn = self.num_cn(tm.day)                                                                #中文日         

        hour = random.choice([str(tm.hour),'0'+str(tm.hour)]) if tm.hour<10 else str(tm.hour)
        hour_cn = self.num_cn(tm.hour)
        minute = random.choice([str(tm.minute),'0'+str(tm.minute)]) if tm.minute<10 else str(tm.minute)
        minute_cn = self.num_cn(tm.minute)
        second = random.choice([str(tm.second),'0'+str(tm.second)]) if tm.second<10 else str(tm.second)
        second_cn = self.num_cn(tm.second)

        ms = random.choice([' ','-','/'])
        if ra<0.35: #日期为月日
            rq = random.choices([month+ ms+ day, month+ '月'+ day+'日', month_cn+ '月'+ day_cn+'日'], weights=[6,4,3])
        elif ra<0.7: #日期为年月
            rq = random.choices([year+ ms+ month, year+ '年'+ month+'月', year_cn+ '年'+ month_cn+'月'], weights=[6,4,3])
        else:           #日期为年月日
            rq = random.choices([year+ ms+ month+ ms+ day, year+ '年'+ month+ '月'+ day+'日', year_cn+ '年'+ month_cn+ '月'+ day_cn+'日'], weights=[7,3,3])
        
        stm = str(tm)
        if ra<0.3:      #时间为年月日时分秒 0.3
            sj = random.choices([stm, stm.replace('-','/'), stm.replace('-',' '), year+ '年'+ month+ '月'+ day+'日 '+stm.split()[1],
            year+ '年'+ month+ '月'+ day+'日'+ hour+'时'+minute+'分'+second+'秒', year_cn+ '年'+ month_cn+ '月'+ day_cn+'日'+ hour_cn+'时'+minute_cn+'分'+second_cn+'秒'],
                                weights=[3,2,2,1.5,1.5,1.5])
        elif ra<0.45:   #时间为年月日时分   0.45
            stm = stm[:-3]
            sj = random.choices([stm, stm.replace('-','/'), stm.replace('-',' '), year+ '年'+ month+ '月'+ day+'日 '+stm.split()[1],
            year+ '年'+ month+ '月'+ day+'日'+ hour+'时'+minute+'分', year_cn+ '年'+ month_cn+ '月'+ day_cn+'日'+ hour_cn+'时'+minute_cn+'分'],
                                weights=[3,2,2,1.5,1.5,1.5])
        elif ra<0.6:   #时间为月日时分秒   0.6
            stm = stm[5:]
            sj = random.choices([stm, stm.replace('-','/'), stm.replace('-',' '), month+ '月'+ day+'日 '+stm.split()[1],
            month+ '月'+ day+'日'+ hour+'时'+minute+'分'+second+'秒', month_cn+ '月'+ day_cn+'日'+ hour_cn+'时'+minute_cn+'分'+second_cn+'秒'],
                                weights=[3,2,2,1.5,1.5,1.5])
        elif ra<0.7:    #时间为月日时分     0.7
            stm = stm[5:16]
            sj = random.choices([stm, stm.replace('-','/'), stm.replace('-',' '), month+ '月'+ day+'日 '+stm.split()[1],
            month+ '月'+ day+'日'+ hour+'时'+minute+'分', month_cn+ '月'+ day_cn+'日'+ hour_cn+'时'+minute_cn+'分'],
                                weights=[3,2,2,1.5,1.5,1.5])
        elif ra<0.9:    #时间为时分秒       0.9
            stm = stm.split()[1]
            sj = random.choices([stm, hour+'时'+minute+'分'+second+'秒', hour_cn+'时'+minute_cn+'分'+second_cn+'秒'],
                                weights=[4,2,2])
        else:       #时间为时分         1
            stm = stm.split()[1][:-3]
            sj = random.choices([stm, hour+'时'+minute+'分', hour_cn+'时'+minute_cn+'分'],
                                weights=[3,2,2])

        return [rq[0], sj[0]]

    #获取年份
    def get_year(self):
        year = self.fake.year()
        return [random.choice([year, year+'年'])]

    #获取月份
    def get_month(self):
        ra = random.random()
        if ra<0.4:
            month = str(int(self.fake.month()))
            return[ month+'月']
        elif ra<0.8:
            return [self.fake.month_name()]
        else:
            return [Faker('en_US').month_name()]

    #获取地点（要新增多少号，小区，楼栋，村，社区，门牌号。。。。。）
    def get_place(self):  #真实到街道最后座为虚拟
        ra = random.random()
        if ra < 0.3:    #到座
            ad = self.fake.address().split()[0]
        elif ra <0.6:   #到街道
            ad = self.fake.address().split()[0][:-2]
        else:           #到号
            hao = random.randint(1,9999)
            ad = self.fake.address().split()[0][:-2]+str(hao)+'号'
        return [ad]
    
    #获取国家
    def get_country(self):
        country =  random.choices([self.fake.country(),'中国'])
        if country == '中国' and random.random<0.3:
            country = random.choices(['China','cn','CN','Cn'])
        return country
    
    #获取省份/城市
    def get_province(self):
        ad = self.fake.address()
        if '市' in ad:
            ad = ad.split('市')[0]
            return [self.fake.province(), ad+'市']
        else:
            return self.get_province()
    
