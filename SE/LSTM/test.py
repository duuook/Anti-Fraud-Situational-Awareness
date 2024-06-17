from utilspro import LSTM_predict_Email
from utilspro import LSTM_predict_PhoneNumber

a, b, c = LSTM_predict_Email.Email_predict("")

if not a:
    print(b)

a, b, c = LSTM_predict_Email.Email_predict("scut@scut.edu.com.cn")

if a:
    print(f'预测标签：{b}')
    print(f'预测概率：\n0：{c[0]:.3f} 1：{c[1]:.3f}')


a, b, c = LSTM_predict_PhoneNumber.PhoneNumber_predict("")

if not a:
    print(b)

a, b, c = LSTM_predict_PhoneNumber.PhoneNumber_predict("07537886204")

if a:
    print(f'预测标签：{b}')
    print(f'预测概率：\n0：{c[0]:.3f} 1：{c[1]:.3f}')
