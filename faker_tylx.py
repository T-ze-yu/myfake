#coding=utf-8

from fake_time import fake_time_place
from fake_CreditIdentifier import CreditIdentifier
import random
import pandas as pd

class myfake(fake_time_place):
    def __init__(self, seed = None) -> None:
        super().__init__(seed = seed)
        self.quhao = self.get_quhao()   #获取区号列表
        self.bank = self.get_banklb()   #获取银行列表
        self.mz, self.mz_rs = self.get_mzrs()   #获取民族和人数列表
        self.function.update({7:self.get_name_sex, 8:self.get_idcard_birth, 9:self.get_phone, 10:self.get_telephone, 11:self.get_zzmm, 12:self.get_mz, 
                                13:self.get_xl, 14:self.get_major, 15:self.get_company, 16:self.get_job_uid, 17:self.get_email_hs, 18:self.get_network, 
                                19:self.get_car_num, 20:self.get_credit_card, 21:self.get_bank, 22:self.get_OrgCode})

    # 获取名字和性别
    def get_name_sex(self):
        sexs = ['男', '女']
        sex = random.choice(sexs)
        if sex == '男':
            name = self.fake.last_name() + self.fake.first_name_male()
            sex = random.choice(['Male','M','m','男'])
        else:
            name = self.fake.last_name() + self.fake.first_name_female()
            sex = random.choice(['Female','F','f','女'])
        return [name, sex]

    #获取身份证号 #获取生日/时间-年月日/时间-月日
    def get_idcard_birth(self):
        id_card = self.fake.ssn()
        birth_year = str(id_card[6:10])
        birth_month = str(id_card[10:12])
        birth_day = str(id_card[12:14])
        ms = random.choice([' ','-','/'])
        if random.random()<0.6:     #0.6概率的生日为月日
            birth = random.choices([birth_month+ ms+ birth_day, birth_month+ '月'+ birth_day+'日'], weights=[7,3])
        else:           #生日为年月日
            birth = random.choices([birth_year+ ms+ birth_month+ ms+ birth_day, birth_year+ '年'+ birth_month+ '月'+ birth_day+'日'], weights=[7,3])
        if random.random()>0.8:
            id_card = id_card[:6] + id_card[8:17]
        if int(birth_year)<2020 and int(birth_year)>1900:
            return [id_card, birth[0]]
        return [self.get_idcard_birth()]

    # 获取手机号码
    def get_phone(self):
        phone = self.fake.phone_number()
        ms1 = random.choice(['86','86 ','+86','+86 ', ''])
        ms2 = random.choice([' ', '-',''])
        if ms2:
            phone = phone[:3]+ms2+phone[3:7]+ms2+phone[7:]
        phone = ms1+phone
        return [phone]

    #获取区号列表
    def get_quhao(self):
        quhao = []
        with open('quhao.txt', 'r', encoding='utf-8') as fr:
            for line in fr:
                ln = line.split()
                if len(ln)>1:
                    quhao.append(ln[1])
        return quhao

    #获取座机号码(传真)
    def get_telephone(self):
        qh = random.choice(self.quhao)   #获取区号
        #随机选取一个3位数或4位数       #随机生成一个3位数 #随机生成一个4位数
        ms0 = random.choice([str(random.randint(100,999)),str(random.randint(1000,9999))])
        ms1 = random.choice([str(random.randint(100,999)),str(random.randint(1000,9999))])
        ms2 = random.choice([' ', '-',''])
        telephone = qh+ms2+ms0+ms2+ms1
        return [telephone]
    
    #获取政治面貌
    def get_zzmm(self):
        zzmm = ['中共党员', '党员','中共预备党员','预备党员', '共青团员', '团员', '民革党员', '民盟盟员','民建会员', 
                '民进会员', '农工党党员', '致公党党员', '九三学社社员', '台盟盟员', '无党派人士', '群众', '普通居民']
        wt = [3,5,2,2,5,6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,9,3]
        return random.choices(zzmm, weights=wt, k=1)

    #获取民族和人数列表
    def get_mzrs(self):
        mz = []
        mz_rs = []
        with open('mz.txt', 'r', encoding='utf-8') as fr:
            for line in fr:
                ln = line.split()
                if ln:
                    ln = ln[0].split('：')
                    mz.append(ln[0].split('、')[1])
                    mz_rs.append(int(ln[1][:-1]))
        return mz, mz_rs

    #获取民族
    def get_mz(self):
        mz  = random.choices(self.mz, weights=self.mz_rs,k=1)
        if mz == '汉族':
            return random.choices(['汉族','汉'])
        else:
            return mz

    #获取学历
    def get_xl(self):
        ra = random.random()
        sm2 = random.choice(['全日制','非全日制',''])
        sm3 = random.choice(['普通',''])
        if ra<0.4:
            sm1 = random.choice(['小学','初级中学','初中','高级中学','高中','职业高中','职高','中等专业','中专'])
            return [sm2+sm3+sm1]
        elif 0.4<= ra < 0.8:
            sm1 = random.choice(['博士','硕士', '本科','专科','高职'])
            if sm1 in ['博士','硕士'] and random.random()<0.6:
                return [sm2+sm3+sm1+'研究生']
            else:
                return [sm2+sm3+sm1]
        else:
            return [random.choice(['函授','夜大','自考','网络教育','电大'])]

    # 获取专业
    def get_major(self):
        with open('majors.txt', 'r', encoding='utf-8') as fr:
            majors = fr.read().splitlines()
            major = random.choice(majors)
            return [major]

    #获取公司/公司性质
    def get_company(self):
        return [random.choice([self.fake.company(),self.fake.company_prefix()]), self.fake.company_suffix()]

    #获取职位/uuid(硬件标识)
    def get_job_uid(self):
        return [self.fake.job(), self.fake.uuid4()]
    
    #获取邮箱/哈希值
    def get_email_hs(self):
        return [self.fake.email(), random.choice([self.fake.md5(), self.fake.sha1(), self.fake.sha256()])]

    #获取网络信息:域名/ipv4/ipv6/mac/url/user_agent
    def get_network(self):
        return [self.fake.domain_name(), self.fake.ipv4(), self.fake.ipv6(), self.fake.mac_address(), 
        random.choice([self.fake.image_url(), self.fake.url()]), self.fake.user_agent()]

    #随机生成一个车牌号码（要新增特殊单位车辆）
    def get_car_num(self):
        char0=["京","津","沪","渝","冀","豫","云","辽","黑","湘","皖","鲁","新","苏","浙","赣","鄂","桂","甘","晋","蒙","陕","吉","闽","赣","粤","青","藏","川","宁","琼"] #省份简称
        char1='ABCDEFGHJKLMNPQRSTUVWXYZ'#车牌号中没有I和O
        char2='0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
        id_1=random.choice(char0)     #车牌号第一位     省份简称
        id_2=''.join(random.sample(char1, 1))    #车牌号第二位

        while True:
            if random.random()<0.6:    #正常
                id_3=''.join(random.sample(char2, 5))
            else:                         #新能源
                id_3=''.join(random.sample(char2, 6))
            v=id_3.isalpha() #所有字符都是字母时返回 true
            if v==True:
                continue
            else:
                sm = random.choice(['',' ','-'])
                car_id=id_1+id_2+sm+id_3
                break
        return [car_id]
    
    #获取信用卡信息
    def get_credit_card(self):
        return [self.fake.credit_card_number()]

    #获取银行列表
    def get_banklb(self):
        bank = []
        with open('bank.txt', 'r', encoding='utf-8') as fr:
            for line in fr:
                ln = line.split()
                if ln:
                    bank.append(ln[0].split('、')[1])
        return bank
    
    def get_bank(self):
        return random.choices(self.bank)

    #组织机构代码/统一社会信用代码
    def get_OrgCode(self):
        factorList = [3, 7, 9, 10, 5, 8, 4, 2]#加权因子列表
        OrgCode = []#用于存放生成的组织机构代码
        sum = 0
        for i in range(8):#随机取前8位数字
            OrgCode.append(random.randint(1, 9))#随机取1位数字
            sum = sum +OrgCode[i]*factorList[i]#用orgCode*加权因子
            # print(dd)
        for i in range(len(OrgCode)):
            OrgCode[i] = str(OrgCode[i])#将orgCode（int）变成str
        C9 = 11-sum % 11 #C9代表校验码。用已经生成的前8位加权后与11取余，然后用11减
        # print(C9)
        if C9 == 10:#当C9的值为10时，校验码应用大写的拉丁字母X表示；当C9的值为11时校验码用0表示;除此之外就是C9本身
            C9 = 'X'
        else:
            if C9 == 11:
                C9 = '0'
            else:
                C9 = str(C9)
        OrgCode.append('-' + C9)

        #随机生成社会信用代码
        ct = CreditIdentifier()
        dt = ct.gen_random_credit_code()
        return ["".join(OrgCode),dt['code']]       #拼接最终生成的组织代码


if __name__ == '__main__':
    # myfake = myfake(666)
    myfake = myfake()

    # for i in range(len(myfake.function)):
    #     for j in myfake.function[i+1]():
    #         print(j)

    #生成35类，地点、姓名、车牌号、社会信用代码、组织机构代码类别数据扩充。
    cols = ['日期','时间','年份','月份','国家','省份','城市','地点','姓名', '性别', '身份证号','出生日期', '手机号', '座机号/传真','政治面貌','民族', '学历', '专业', 
            '公司','公司性质', '职位', 'uuid/硬件标识', '邮箱','哈希值', '域名','ipv4地址','ipv6地址', 'mac地址', 'url', '用户代理(user_agent)','车牌号','信用卡号',
            '银行名称','组织机构代码','统一社会信用代码']

    datas = []
    for j in range(50):
        data = []
        for i in range(len(myfake.function)):
            for j in myfake.function[i+1]():
                data.append(j)
        datas.append(data)
    df = pd.DataFrame(columns=cols, data=datas)

    file_path = './datas/通用'  + '.csv'
    df.to_csv(file_path, index=None, encoding='utf_8_sig')
