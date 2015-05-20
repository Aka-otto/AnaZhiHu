### AnaZhiHu V1.0
+ AppName: AnaZhiHu(Analyse ZhiHu)
+ Create: 2015-05-20
+ Author: Dave, Y4ng

用户可以通过输入uid使用AnaZhiHu来获取一个人赞同过的回答(会有少数遗漏):

    ➜  AnaZhiHu git:(master) python AnaZhiHu.py dave-9
    [*] AnaZhiHu is hot.
    [+] /question/666666/answer/666666
    [+] /question/666666/answer/666666
    [+] /question/666666/answer/666666
    [+] /question/666666/answer/666666
    [+] /question/666666/answer/666666
    [+] /question/666666/answer/666666
    [+] /question/666666/answer/666666
    ...
    [+] Results the save path: ./reports/ana_example.html
    [*] Total Time Consumption: 10s

分析完成后，将输出一个精美的report界面，可在里面查看。

P.S uid是指个人主页链接中http://www.zhihu.com/people/{uid}标识的部位

### Function
+ 获取用户点赞过的回答