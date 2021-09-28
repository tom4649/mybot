import random
hands=['グー', 'チョキ', 'パー']

p=0
m=0
while (p-m+3)%3==0:
    print("手を入力してください") 
    print("0:グー 1:チョキ 2:パー")
    
    try:
        p=int(input("ジャンケン..."))
    except ValueError:
        print('ちゃんと入力してくれ')
    

    player=hands[p]
    print("あなたは"+player+"を出したね")

    m=random.randint(0,2)
    com=hands[m]
    print("相手は"+com+"を出した")
    if (p-m+3)%3==0:
        print("あいこです。もう一度。")
    elif (p-m)%3==2:
        print("勝ち!!")
    elif (p-m+3)%3==1:
        print("負け!!")


