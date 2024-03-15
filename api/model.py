import torch
import torch.nn as nn

class DropoutFC(nn.Module):
    def __init__(self, input_size=8, output_size=800, dropout_rate=0, is_bn=1, act='elu'):
        super(DropoutFC, self).__init__()
        layers = []
        if is_bn:
            layers += [nn.BatchNorm1d(input_size)]
        if dropout_rate > 0:
            layers += [nn.Dropout(dropout_rate)]
        layers += [nn.Linear(input_size, output_size)]
        if act == 'elu':
            layers += [nn.ELU()]
        else:
            layers += [nn.Tanh()]
        self.fc = nn.Sequential(*layers)

    def forward(self, x):
        out = self.fc(x)
        return out


class FCmodel(nn.Module):
    def __init__(self, input_size=7, hid=512, dropout_rate=0, is_bn=1):
        super(FCmodel, self).__init__()
        layers = []
        layers += [DropoutFC(input_size, (input_size + hid) // 2, dropout_rate, is_bn)]
        layers += [DropoutFC((input_size + hid) // 2, hid, dropout_rate, is_bn)]
        self.up = nn.Sequential(*layers)

        layers = []
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        self.fc1 = nn.Sequential(*layers)

        layers = []
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        self.fc2 = nn.Sequential(*layers)

        layers = []
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        self.fc3 = nn.Sequential(*layers)

        layers = []
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        layers += [DropoutFC(hid, hid, dropout_rate, is_bn)]
        self.fc4 = nn.Sequential(*layers)

        layers = []
        layers += [DropoutFC(hid, hid // 4, dropout_rate, is_bn)]
        layers += [DropoutFC(hid // 4, hid // 16, dropout_rate, is_bn)]
        layers += [DropoutFC(hid // 16, 4, dropout_rate, is_bn)]
        layers += [DropoutFC(4, 1, dropout_rate, 0)]
        self.down = nn.Sequential(*layers)

    def forward(self, input):
        x = input
        x = self.up(x)
        x = x + self.fc1(x)
        x = x + self.fc2(x)
        x = x + self.fc3(x)
        x = x + self.fc4(x)
        x = self.down(x)
        # print(t)
        return x