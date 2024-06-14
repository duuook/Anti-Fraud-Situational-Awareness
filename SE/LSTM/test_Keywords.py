from utilspro import Keywords

size, ans = Keywords.Get_keywords("!!!!!!")

if size == 0:
    print(ans)

test_str = "今天的午饭好好吃！我喜欢吃午饭"
size, ans = Keywords.Get_keywords(test_str)

if size > 0:
    print(size)
    print(type(ans))
    for index, key in enumerate(ans):
        fre = len(key[0]) / len(test_str)
        print('{:.0%}'.format(fre))
        print('词数：', key[1])
