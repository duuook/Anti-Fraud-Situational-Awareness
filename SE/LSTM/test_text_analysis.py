from utilspro import LSTM_predict

a, b, c = LSTM_predict.Text_predict("    ")

if not a:
    print(b)

a, b, c = LSTM_predict.Text_predict("今天是个好日子")

if a:
    print(f'预测标签：{b}')
    print(f'预测概率：\n0：{c[0]:.3f} 1：{c[1]:.3f}')
