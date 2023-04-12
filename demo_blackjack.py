# NOTE 手順
# 1. ゲームが始まることを告げる
# 手札を2枚配る
# カードを捨てるか決める
# 勝負する
import random

from time import sleep


class ActionPhase():
    def call_turn(self, turn_num, name):
        self.name = name
        # ターン宣言
        if turn_num == 1:
            print(f"{name}の最初のターンです。")
        else:
            print(f"{name}の{turn_num}ターン目です。")
        turn_num += 1
        return turn_num

    def main_action(self, hands, action_status=True, change_flg=False):
        self.hands = hands

        # CPUだった場合は自動処理をする
        if self.name == "ディーラー":
            print("ヒットしますか？スタンドしますか？\nヒット or スタンド")
            cpu_hits_or_stand = random.randint(0, 1)
            if 16 <= sum(hands) <= 18 and cpu_hits_or_stand == 1:
                print("ヒット")
                hands.append(random.randint(1, 13))
            elif 15 >= sum(hands):
                print("ヒット")
                hands.append(random.randint(1, 13))
            else:
                print("スタンド")
                action_status = False
        else:
            # プレイヤーにアクションを求める
            print("ヒットしますか？スタンドしますか？\nh or s")
            action_plan = input(">> ")
            if action_plan == "h":
                hands.append(random.randint(1, 13))
                print(f"{self.name}の手札は{hands}になりました。")
                if 11 in hands or change_flg is True:
                    hands, change_flg = choise_1_or_11(self.name, hands)
            else:
                action_status = False
        return hands, action_status, change_flg


def choise_1_or_11(name, hands):
    if 11 in hands:
        print("11を1に変更しますか？")
    else:
        print("1を11に変更しますか？")
    print("y/n")
    change_status = input(">> ")
    if change_status == "y":
        eleven_index = hands.index(11)
        hands[eleven_index] = 1
        print(f"{name}の手札は{hands}になりました。")
    change_flg = True
    return hands, change_flg


def main():
    # プレイヤーの処理継続のステータス設定
    your_action_status = True
    # CPUの処理継続のステータス設定
    cpu_action_status = True

    # コンソールからの呼び名を定義
    your_name = "あなた"
    cpu_name = "ディーラー"

    # ターン数カウンタ設定
    table_turn_nums = 1

    # バースト判定
    your_burst = False
    cpu_burst = False

    # 11を1に変更したかのフラグ
    change_flg = False
    _cpu_change_flg = False

    # 処理までのディレイ時間を定義
    delay = 1

    # ゲーム開始の宣言
    print("ブラックジャックを開始します。")
    sleep(delay)
    print("手札を配ります。")
    sleep(delay)

    # プレイヤーの手札を配る処理
    your_hands = [random.randint(1, 13) for i in range(2)]

    # プレイヤー手札の宣言
    print(f"あなたの手札は{your_hands}です。")
    sleep(delay)

    # CPUの手札処理（プレイヤーには見せない）
    cpu_hands = [random.randint(1, 13) for i in range(2)]

    # CPUの手札宣言
    print("対戦相手に手札を配っています。")
    sleep(delay)

    # ゲームのメイン処理呼び出し
    # クラスのインスタンス化
    aciton_phase = ActionPhase()

    while not (your_action_status is False and cpu_action_status is False):
        # プレイヤーの処理
        if your_action_status is True:
            # ターン数の宣言と更新の関数をコール
            aciton_phase.call_turn(table_turn_nums, your_name)
            sleep(delay)

            # ブラックジャックのメインの処理の関数をコール
            main_action_rtn = aciton_phase.main_action(your_hands, your_action_status, change_flg)
            # returnの中身をアンパッキング
            your_hands, your_action_status, change_flg = main_action_rtn
            sleep(delay)

            # 結果の判定
            if sum(your_hands) >= 22:
                your_action_status = False
                your_burst = True

        # CPUの処理
        if cpu_action_status is True and your_burst is False:
            # ターン数の宣言と更新の関数をコール
            table_turn_nums = aciton_phase.call_turn(table_turn_nums, cpu_name)
            sleep(delay)

            # ブラックジャックのメインの処理の関数をコール
            main_action_rtn = aciton_phase.main_action(cpu_hands, cpu_action_status)
            # returnの中身をアンパッキング
            cpu_hands, cpu_action_status, _cpu_change_flg = main_action_rtn
            sleep(delay)

            # 結果の判定
            if sum(cpu_hands) >= 22:
                cpu_action_status = False
                cpu_burst = True

        if your_burst is True or cpu_burst is True:
            break

    # 勝敗判定
    if your_burst is True and cpu_burst is False:
        print("あなたの負けです・・・")
        print(f"{your_name}の手札：{your_hands}")
        print(f"{cpu_name}の手札：{cpu_hands}")
        sleep(delay)

    elif your_hands < cpu_hands:
        print("あなたの負けです・・・")
        print(f"{your_name}の手札：{your_hands}")
        print(f"{cpu_name}の手札：{cpu_hands}")
        sleep(delay)

    elif your_hands > cpu_hands:
        print("あなたの勝ちです！")
        print(f"{your_name}の手札：{your_hands}")
        print(f"{cpu_name}の手札：{cpu_hands}")
        sleep(delay)

    elif your_burst is False and cpu_burst is True:
        print("あなたの勝ちです！")
        print(f"{your_name}の手札：{your_hands}")
        print(f"{cpu_name}の手札：{cpu_hands}")
        sleep(delay)

    elif your_hands == cpu_hands:
        print("引き分けです！")
        print(f"{your_name}の手札：{your_hands}")
        print(f"{cpu_name}の手札：{cpu_hands}")
        sleep(delay)

    # 再実行処理
    print("もう一度遊びますか？\ny or n")
    one_more_play_status = input(">> ")
    if one_more_play_status == "y":
        sleep(delay)
        main()


if __name__ == "__main__":
    main()
