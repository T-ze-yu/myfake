## 生成一系列伪造数据
目前支持以下类别：

    cols = ['日期','时间','年份','月份','国家','省份','城市','地点','姓名', '性别', '身份证号','出生日期', '手机号', '座机号/传真','政治面貌','民族', '学历', '专业', 
            '公司','公司性质', '职位', 'uuid/硬件标识', '邮箱','哈希值', '域名','ipv4地址','ipv6地址', 'mac地址', 'url', '用户代理(user_agent)','车牌号','信用卡号',
            '银行名称','组织机构代码','统一社会信用代码']
执行fake_tylx.py就可以生成一个表格包含以上类别。
![在这里插入图片描述](https://img-blog.csdnimg.cn/1e116cd28741457bb8bc810c73eb5107.png)

当然也可以实例化myfake类去调用相关函数去伪造自己想要的数据。

