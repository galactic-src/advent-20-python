EX_INPUT = [0,3,6]
INPUT = [17,1,3,16,19,0]


def run(target_turn):
    turn = 1
    spoken = {}
    last_spoken = None
    for i in INPUT:
        if i in spoken:
            spoken[i].append(turn)
        else:
            spoken[i] = [turn]
        last_spoken = i
        turn += 1

    while turn <= target_turn:
        if len(spoken[last_spoken]) > 1:
            next_spoken = spoken[last_spoken][-1] - spoken[last_spoken][-2]
        else:
            next_spoken = 0

        if next_spoken in spoken:
            spoken[next_spoken].append(turn)
        else:
            spoken[next_spoken] = [turn]
        last_spoken = next_spoken
        turn += 1

    print(f"answer: {last_spoken}")


if __name__ == "__main__":
    run(2020)  # 694
    run(30000000)  # 21768614
