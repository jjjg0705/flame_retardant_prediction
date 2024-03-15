# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import json
import torch
import torch.nn as nn
from LoiPredict import loi_Predict#导入预测模型
from model import FCmodel

#导入flask类
app = Flask(__name__, template_folder='dist')
#创建该类的实例，第一个参数是应用模块或者包的名称
CORS(app,resources=r'/*')
#在 Flask 应用程序中启用 CORS机制，用于在浏览器中处理跨域资源请求。
#它允许一个域上的网页请求来自于另一个域的资源，这样可以解决浏览器的同源策略限制。
#app 是 Flask 应用程序的实例，resources=r'/*' 表示允许来自任何路径的跨域请求

@app.route('/')
def index():
    #return render_template('templates/index.html')
    return "hello,world"

@app.route('/predict', methods=['GET','POST'])
#使用 route() 装饰器定义一个路由，来告诉 Flask 触发函数的 URL
def model_predict():
#定义了用于处理 /predict 路由的请求的函数
    print('进入预测函数')    
    matrix = request.args.get('matrix')#获取基体总量
    antioxygen = request.args.get('antioxygen')#获取抗氧剂总量
    fillers_encoded = request.args.get('fillers')#获取填料数据列表
    fillers = json.loads(fillers_encoded)
    print("Received fillers:", fillers)
    
    #x_types = '抗氧剂,基体总量（g）,十溴二苯乙烷（DBDPE）,羟基锡酸锌（ZHS）,锡酸锌（ZS）,三氧化二锑（Sb2O3）,氢氧化镁（Mg(OH)2）,BDBNCE（溴系阻燃剂）,HBCD-SF,FR-1034,DBDPO,滑石粉,DCRP,硼酸锌,BTBPIE,BPBPE,TTBNP,含PBBA的EPDM母粒,其他添加剂,PPBBA,EPDM,EDAP,APP,APP+Spinflam MF82,APP+PETOL,APP+THEIC,Exolit IFR23P,APP+PETOL+苯甲酸酯,APP+MF82,ATH,Spin-flameMF82,Mg(OH)2(MAGNIFIN H10),Mg(OH)2(MAGNIFIN H10F),包覆红磷Amgard CPC200,SFR-100,硬脂酸镁,EG,RP,Melamine phosphate (MPP),DPER,Melamine,Melamine cyanurate,Dimelamine phosphate,Melamine borate,Novolac(Durez 22091),PPO(GE 808-100),Novolac(Durez 29295),PER,triazine-based macromolecule(TBM),charring-foaming agent (CFA),Pentaerythritol phosphate (PEPA),hosphorus-contain-ing nanosponge (P–NS,a novel polysiloxane (APID), [BMIm]3PW (PIL1),[BMIm]3PMo (PIL2),[BMIm]4SiW (PIL3),[Bmim]6CoW12O40 (CoW),[C4]PMo (PIL4),[C8]PMo(PIL8),[C12]PMo(PIL12),[C18]PMo(PIL18),SiO2,BiFeO3, LaMnO3,Ni,Ni-Al(9/1),Ni-Mg(9/1),Ni-Cu(9/1),Ni(HCOO)2.2H2O,NiCl2.6H2O,NiSO4.6H2O,NiCO3,NiO,polydimethylsiloxane (PDMS),N-alkoxy hindered amine (Flamestab NOR116) ,spirobisphosphoryldicyandiamide (SPDC),Ni2O3,MnO2,TiO2,ZnO,MnO,brominated epoxy resin (BEO),MMT,Glass bubble(GB),α-zirconium phosphate (mZrP),La2O3'.split(',')
    #x_types.append("9,10-二氢-9-氧杂-10-磷杂菲-10-氧化物DOPO）")
    #x_types.append('1-oxo-4-hydroxy-methyl-2,6,7-trioxa-1-phosphabicyclo[2.2.2]octane(PEPA')
    
    x_types = '抗氧剂;基体总量（g）;十溴二苯乙烷（DBDPE）;羟基锡酸锌（ZHS）;锡酸锌（ZS）;三氧化二锑（Sb2O3）;氢氧化镁（Mg(OH)2）;BDBNCE（溴系阻燃剂）;六溴环十二烷;四溴二苯甲基二醇;十溴二苯醚;滑石粉;得克隆;硼酸锌;双（四溴邻苯二甲酰亚胺）乙烷;双（五溴苯基）乙烷;2,2-双-（溴甲基）-3-溴-1-丙醇磷酸酯;丙烯酸五溴苄基酯（PBBA）和三元乙丙橡胶（EPDM）共聚获得的母料;其他添加剂;聚丙烯酸五溴苄基酯;三元乙丙橡胶;2-乙基己基二苯基磷酸酯;聚磷酸铵;聚磷酸铵-混合膨胀型阻燃剂;聚磷酸铵和季戊四醇混合物;聚磷酸铵和异氰脲酸酯三羟乙基酯混合物;膨胀阻燃剂;聚磷酸铵、季戊四醇和苯甲酸酯混合物;聚磷酸铵-混合膨胀型阻燃剂;氢氧化铝;混合膨胀型阻燃剂;氢氧化镁（MAGNIFIN H10）;氢氧化镁（MAGNIFIN H10F）;包覆红磷;硅阻燃剂;硬脂酸镁;膨胀石墨;磷系阻燃剂;三聚氰胺磷酸盐;双季戊四醇;三聚氰胺;三聚氰胺氰尿酸盐;磷酸二甲胺;硼酸三聚氰胺;酚醛树脂1;聚2,6-二甲基亚苯基醚;酚醛树脂2;季戊四醇;三嗪基大分子;炭化发泡剂;季戊四醇磷酸酯;含磷纳米阻燃剂;一种新型聚硅氧烷;基于多金属氧酸盐的离子液体（PIL）杂化材料[BMIm]3PW (PIL1);基于多金属氧酸盐的离子液体（PIL）杂化材料[BMIm]3PMo (PIL2);基于多金属氧酸盐的离子液体（PIL）杂化材料[BMIm]4SiW (PIL3);多金属氧酸盐基有机-无机杂化材料;聚金属氧基离子液体有机部分烷基[C4]PMo(PIL4);聚金属氧基离子液体有机部分烷基[C8]PMo(PIL8);聚金属氧基离子液体有机部分烷基[C12]PMo(PIL12);聚金属氧基离子液体有机部分烷基[C18]PMo(PIL18);二氧化硅;金属氧化物2;金属氧化物1;镍;镍-铝;镍-镁;镍-铜;醋酸镍;氯化镍;硫酸镍;碳酸镍;氧化镍;聚二甲基硅氧烷;N-烷氧基受阻胺（Flamestab NOR116）;螺双磷酰双氰胺;二氧化镍;氧化锰;氧化钛;氧化锌;氧化锰;溴化环氧树脂;蒙托土;玻璃泡;α-磷酸锆;氧化镧'.split(';')

    x_types.append("9,10-二氢-9-氧杂-10-磷杂菲-10-氧化物（DOPO）")
    x_types.append('1-氧代-4-羟基-甲基-2,6,7-三氧代-1-磷杂双环[2.2.2]辛烷')
    
    #设置输入数据默认值
    X_input = np.zeros((1, 133))#0~87(88种原料),88~132(45种基体类型)
    
    #设置基体类型，目前都默认为PP0
    X_input[0][88] = 1
    
    #计算原料总质量
    weightsum = float(matrix) + float(antioxygen)#matrix和antioxygen是str类型
    for filler in fillers:
        weightsum += float(filler['weight'])
    #转化成总共1000份
    #基体份数
    X_input[0][1] = float(matrix) / weightsum * 1000
    #抗氧剂份数
    X_input[0][0] = float(antioxygen) / weightsum * 1000
    #填料份数
    for filler in fillers:
        filler_type = filler['type']
        filler_weight = filler['weight']
        # 查找 filler_type 在 x_types 中的索引位置
        if filler_type in x_types:
            index = x_types.index(filler_type)
            X_input[0][index] = float(filler_weight) / weightsum * 1000

    #调用模型执行预测
    result = loi_Predict(X_input)#返回结果是一个二维数组
    result = round(result[0][0], 1)#舍入1位
    result = str(result)#JSON序列化
    return jsonify({'result': result})
    #函数最后返回需要在用户浏览器中显示的信息
    
@app.route('/feedback', methods=['GET','POST'])
#使用 route() 装饰器定义一个路由，来告诉 Flask 触发函数的 URL
def feedback_saving():
#定义了用于处理 /predict 路由的请求的函数
    print('进入反馈函数')    
    matrix = request.args.get('matrix')#获取基体总量
    antioxygen = request.args.get('antioxygen')#获取抗氧剂总量
    fillers_encoded = request.args.get('fillers')#获取填料数据列表
    fillers = json.loads(fillers_encoded)
    predictionResult = request.args.get('predictionResult')
    real_loi = request.args.get('real_loi')
    real_env = request.args.get('real_env')

    x_types = '抗氧剂,基体总量（g）,十溴二苯乙烷（DBDPE）,羟基锡酸锌（ZHS）,锡酸锌（ZS）,三氧化二锑（Sb2O3）,氢氧化镁（Mg(OH)2）,BDBNCE（溴系阻燃剂）,HBCD-SF,FR-1034,DBDPO,滑石粉,DCRP,硼酸锌,BTBPIE,BPBPE,TTBNP,含PBBA的EPDM母粒,其他添加剂,PPBBA,EPDM,EDAP,APP,APP+Spinflam MF82,APP+PETOL,APP+THEIC,Exolit IFR23P,APP+PETOL+苯甲酸酯,APP+MF82,ATH,Spin-flameMF82,Mg(OH)2(MAGNIFIN H10),Mg(OH)2(MAGNIFIN H10F),包覆红磷Amgard CPC200,SFR-100,硬脂酸镁,EG,RP,Melamine phosphate (MPP),DPER,Melamine,Melamine cyanurate,Dimelamine phosphate,Melamine borate,Novolac(Durez 22091),PPO(GE 808-100),Novolac(Durez 29295),PER,triazine-based macromolecule(TBM),charring-foaming agent (CFA),Pentaerythritol phosphate (PEPA),hosphorus-contain-ing nanosponge (P–NS,a novel polysiloxane (APID), [BMIm]3PW (PIL1),[BMIm]3PMo (PIL2),[BMIm]4SiW (PIL3),[Bmim]6CoW12O40 (CoW),[C4]PMo (PIL4),[C8]PMo(PIL8),[C12]PMo(PIL12),[C18]PMo(PIL18),SiO2,BiFeO3, LaMnO3,Ni,Ni-Al(9/1),Ni-Mg(9/1),Ni-Cu(9/1),Ni(HCOO)2.2H2O,NiCl2.6H2O,NiSO4.6H2O,NiCO3,NiO,polydimethylsiloxane (PDMS),N-alkoxy hindered amine (Flamestab NOR116) ,spirobisphosphoryldicyandiamide (SPDC),Ni2O3,MnO2,TiO2,ZnO,MnO,brominated epoxy resin (BEO),MMT,Glass bubble(GB),α-zirconium phosphate (mZrP),La2O3'.split(',')
    x_types.append("9,10-二氢-9-氧杂-10-磷杂菲-10-氧化物DOPO）")
    x_types.append('1-oxo-4-hydroxy-methyl-2,6,7-trioxa-1-phosphabicyclo[2.2.2]octane(PEPA')
    
    #设置输入数据默认值
    X_input = np.zeros((1, 135))#0~87(88种原料),88~132(45种基体类型),133-134(预测值，实际值)
    #设置预测结果
    X_input[0][133] = predictionResult
    #设置实际测量值
    X_input[0][134] = real_loi

    
    #设置基体类型，目前都默认为PP0
    X_input[0][88] = 1
    
    #计算原料总质量
    weightsum = float(matrix) + float(antioxygen)#matrix和antioxygen是str类型
    for filler in fillers:
        weightsum += float(filler['weight'])
    #转化成总共1000份
    #基体份数
    X_input[0][1] = float(matrix) / weightsum * 1000
    #抗氧剂份数
    X_input[0][0] = float(antioxygen) / weightsum * 1000
    #填料份数
    for filler in fillers:
        filler_type = filler['type']
        filler_weight = filler['weight']
        # 查找 filler_type 在 x_new 中的索引位置
        if filler_type in x_types:
            index = x_types.index(filler_type)
            X_input[0][index] = float(filler_weight) / weightsum * 1000
    
    # 将 X_input 转换为字符串形式，以便写入文件
    X_input_str = ",".join(map(str, X_input[0]))
    
    file_name = "feedback.txt"
    with open(file_name, 'a', encoding="utf-8") as file:
        file.write('\n' + X_input_str + ',' + real_env + '\n')
    
    completed_message = "数据已成功存储！"
    print(completed_message)
    return completed_message

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
    print("Good bye!")

