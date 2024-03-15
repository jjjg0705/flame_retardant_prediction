import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

def loi_Predict(X_input):
    #print("预测中，请稍后……")
    data = pd.read_csv('第二轮loi.csv')
    x_new = '抗氧剂,基体总量（g）,十溴二苯乙烷（DBDPE）3份,羟基锡酸锌（ZHS）,锡酸锌（ZS）,三氧化二锑（Sb2O3）1份,氢氧化镁（Mg(OH)2）(g),BDBNCE（溴系阻燃剂）,HBCD-SF,FR-1034,DBDPO,滑石粉,DCRP,硼酸锌,BTBPIE,BPBPE,TTBNP,含PBBA的EPDM母粒,其他添加剂,PPBBA,EPDM,EDAP,APP,APP+Spinflam MF82,APP+PETOL,APP+THEIC,Exolit IFR23P,APP+PETOL+苯甲酸酯,APP+MF82,ATH,Spin-flameMF82,Mg(OH)2(MAGNIFIN H10),Mg(OH)2(MAGNIFIN H10F),包覆红磷Amgard CPC200,SFR-100,硬脂酸镁,EG,RP,Melamine phosphate (MPP),DPER,Melamine,Melamine cyanurate,Dimelamine phosphate,Melamine borate,Novolac(Durez 22091),PPO(GE 808-100),Novolac(Durez 29295),PER,triazine-based macromolecule(TBM),charring-foaming agent (CFA),Pentaerythritol phosphate (PEPA),hosphorus-contain-ing nanosponge (P–NS,a novel polysiloxane (APID), [BMIm]3PW (PIL1),[BMIm]3PMo (PIL2),[BMIm]4SiW (PIL3),[Bmim]6CoW12O40 (CoW),[C4]PMo (PIL4),[C8]PMo(PIL8),[C12]PMo(PIL12),[C18]PMo(PIL18),SiO2,BiFeO3, LaMnO3,Ni,Ni-Al(9/1),Ni-Mg(9/1),Ni-Cu(9/1),Ni(HCOO)2.2H2O,NiCl2.6H2O,NiSO4.6H2O,NiCO3,NiO,polydimethylsiloxane (PDMS),N-alkoxy hindered amine (Flamestab NOR116) ,spirobisphosphoryldicyandiamide (SPDC),Ni2O3,MnO2,TiO2,ZnO,MnO,brominated epoxy resin (BEO),MMT,Glass bubble(GB),α-zirconium phosphate (mZrP),La2O3'.split(
        ',')
    x_new.append("9,10-二氢-9-氧杂-10-磷杂菲-10-氧化物DOPO）")
    x_new.append('1-oxo-4-hydroxy-methyl-2,6,7-trioxa-1-phosphabicyclo[2.2.2]octane(PEPA')

    X_raw = data[x_new].values  # X_raw是567行88列的数据
    y_raw = data['氧指数%'].values

    for i in range(45):
        p = []
        for pp in data['基体名称'].values:
            p.append(pp == i)
        X_raw = np.concatenate((X_raw, np.array(p).reshape(-1, 1)), axis=1)


    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    stdx = StandardScaler()
    stdy_ = StandardScaler()
    stdy = MinMaxScaler()
    stdx = stdx.fit(X_raw)
    stdy_ = stdy_.fit(y_raw.reshape(-1, 1))
    x_std = stdx.transform(X_raw)
    y_std_ = stdy_.transform(y_raw.reshape(-1, 1))
    stdy = stdy.fit(y_std_)
    y_std = stdy.transform(y_std_)

    stdX_input=stdx.transform(X_input)

    from sklearn.linear_model import LassoCV, RidgeCV
    lmodel = LassoCV(cv=5, max_iter=20000)
    rmodel = RidgeCV(cv=5)
    lmodel.fit(x_std, y_std.ravel())
    rmodel.fit(x_std, y_std.ravel())
    cl = lmodel.predict(stdX_input)
    cr = rmodel.predict(stdX_input)
    TestX_nn = np.concatenate((stdX_input, cl.reshape(-1, 1), cr.reshape(-1, 1)), axis=1)
    
    #model = torch.load('lann_fold_14.pth'.format(0))
    model = torch.load('lann_fold_14.pth', map_location=torch.device('cpu'))
    #pred = model(torch.from_numpy(TestX_nn.astype(np.float32)).cuda())
    TestX_nn = torch.from_numpy(TestX_nn.astype(np.float32))
    TestX_nn = TestX_nn.to(torch.device('cpu'))
    pred = model(TestX_nn)
    #pr = stdy_.inverse_transform(stdy.inverse_transform(pred.cpu().detach().numpy()))
    pr = stdy_.inverse_transform(stdy.inverse_transform(pred.detach().numpy()))
    #print("预计此配方合成材料的氧指数(%)为",pr)
    
    return pr


