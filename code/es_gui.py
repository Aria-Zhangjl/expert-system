#用户页面GUI
#放入提交的代码中
import easygui as eg
import user_score_of_seq as ss
import change_regulation as cr


label_list=['a','b','c','d','e','f','g','h','i','m','n','o','p','q','r','s','u','v']
tone_list=['平','仄','通']

#设置选择对联或者是修改规则
def choose_function():
    func = eg.buttonbox(msg="请选择您的操作", title="功能选择", choices=['对联练习', '规则修改','退出登录'])
    return func

#对联练习
def train_seq():
    test=ss.random_seq1()
    msg="上联是："+test
    choose=eg.buttonbox(msg=msg,title="",choices=['换一个','确认'])
    while choose == '换一个':
        test = ss.random_seq1()
        msg = "上联是：" + test
        choose = eg.buttonbox(msg=msg, title="", choices=['换一个', '确认'])
    msg=msg+"\n请输入下联："
    user_input = eg.enterbox(msg=msg)
    #基础得分
    score1,rule1=ss.basic_score(test,user_input)
    res1="您的基础得分为："+str(score1)+"。\n"
    res1+=rule1[0]
    eg.msgbox(msg=res1,title='基础得分')
    #平仄得分
    if score1 != 0:
        score2, rule2 = ss.score_of_tone(test, user_input)
        res2 = "您的格律得分为：" + str(score2)+"。\n"
        res2+="判断依据：\n"
        for i in range(len(test)-1):
            res2+=rule2[i]+","
        res2+=rule2[len(test)-1]+";\n"
        for i in range(len(test),2*len(test)-1):
            res2+=rule2[i]+","
        res2+=rule2[2*len(test)-1]+";\n"
        for i in range(2*len(test),len(rule2)):
            res2+=rule2[i]+"；\n"
        eg.msgbox(msg=res2, title='格律得分')
        #词性结构得分
        score3,rule3=ss.score_of_structure(test, user_input)
        res3="您的词性结构得分为："+str(score3)+"。\n"
        res3+="判断依据：\n"
        for i in range(len(rule3)):
            res3+=rule3[i]+"\n"
        eg.msgbox(msg=res3,title='词性结构')
        #相似性得分
        score4,rule4=ss.score_of_similarity(test, user_input)
        res4 = "您的对联相似性得分为："+str(score4)+"。\n"
        res4+="判断依据：\n"+rule4+"\n"
        eg.msgbox(msg=res4,title='相似性得分')
        eg.msgbox(msg="您的总得分为："+str(score4+score3+score1+score2)+"\n",title='总得分')

#修改规则
def correct_knowledg():
    choose=eg.buttonbox(msg="请选择要修改的规则",title='规则修改',choices=['格律','词性'])
    if choose == '格律':
        tone_choose=eg.buttonbox(msg="请选择操作",title='规则修改',choices=['汉字韵部修改','韵部评分修改'])
        if tone_choose == '汉字韵部修改':
            tone_choose = eg.buttonbox(msg="请选择操作", title='规则修改', choices=['修改汉字韵部', '删除韵部规则', '增加韵部规则'])
            if tone_choose == '修改汉字韵部':
                # 修改平仄
                fieldNames = ['汉字', '韵部']
                fieldvalue1 = []
                title = '汉字格律修改'
                msg = "请填写下列表格："
                fieldvalue1 = eg.multenterbox(msg, title, fieldNames)
                if fieldvalue1[1] not in tone_list:
                    eg.msgbox(msg="没有该韵部出现！")
                else:
                    #print(fieldvalue1)
                    cr.change_tone_of_hanzi(fieldvalue1[0], fieldvalue1[1])
                    eg.msgbox(msg="修改成功!")
            # 删除平仄
            elif tone_choose == '删除韵部规则':
                fieldNames = ['汉字']
                fieldvalue1 = []
                title = '汉字韵部规则删除'
                msg = '请输入要删除的汉字：'
                fieldvalue1 = eg.multenterbox(msg, title, fieldNames)
                cr.delete_hanzi_tone(fieldvalue1[0])
                eg.msgbox(msg="删除成功")
            # 添加平仄
            else:
                fieldNames = ['汉字', '韵部']
                fieldvalue1 = []
                title = '汉字格律添加'
                msg = "请填写下列表格："
                fieldvalue1 = eg.multenterbox(msg, title, fieldNames)
                if fieldvalue1[1] not in tone_list:
                    eg.msgbox(msg="没有该韵部出现！")
                else:
                    #print(fieldvalue1)
                    cr.add_hanzi_tone(fieldvalue1[0], fieldvalue1[1])
                    eg.msgbox(msg="添加成功!")
        else:#修改格律评分
            fieldNames = ['上联韵部', '下联韵部','得分']
            fieldvalue1 = []
            title = '格律评分修改'
            msg = "请填写下列表格："
            fieldvalue1 = eg.multenterbox(msg, title, fieldNames)
            #判断修改是否违法
            if fieldvalue1[0] not in tone_list or fieldvalue1[1] not in tone_list:
                #print(fieldNames[0],fieldNames[1])
                eg.msgbox(msg="没有该韵部出现！")
            else:
                #print(fieldvalue1)
                cr.change_score_of_tone(int(fieldvalue1[2]), fieldvalue1[0], fieldvalue1[1])
                eg.msgbox(msg="修改成功!")
    elif choose=='词性':
        #选择操作
        word_label_choose=choose = eg.buttonbox(msg="请选择操作", title='规则修改', choices=['修改词性匹配','修改词性得分'])
        if word_label_choose=='修改词性匹配':
            fieldNames = ['词性', '类别']
            fieldvalue1 = []
            title = '修改词性匹配'
            msg = "请填写下列表格："
            fieldvalue1 = eg.multenterbox(msg, title, fieldNames)
            #print(fieldvalue1)
            #检查是否有label出现
            if fieldvalue1[1] not in label_list:
                eg.msgbox(msg="没有该项类别！")
            else:
                cr.change_label_of_word(fieldvalue1[0], fieldvalue1[1])
                eg.msgbox(msg="修改成功!")
        if word_label_choose=='修改词性得分':
            fieldNames = ['词性1', '词性2','得分']
            fieldvalue1 = []
            title = '修改词性得分'
            msg = "请填写下列表格："
            fieldvalue1 = eg.multenterbox(msg, title, fieldNames)
            if fieldvalue1[0] not in label_list or fieldvalue1[1] not in label_list:
                eg.msgbox(msg="没有该项类别！")
            else:
                #print(fieldvalue1)
                cr.chang_label_score(fieldvalue1[2], fieldvalue1[0], fieldvalue1[1])
                eg.msgbox(msg="修改成功!")







if __name__ == '__main__':
    func=choose_function()
    #print(func)
    while func!='退出登录':
        if func == '对联练习':
            train_seq()
        if func == '规则修改':
            correct_knowledg()
        func=choose_function()
        #print(func)

