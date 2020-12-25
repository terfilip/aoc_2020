subject_number0 = 7
door_public_key = 13768789
card_public_key = 11404017
s1_door_public_key = 17807724
s1_card_public_key = 5764801


def transform_number(subject_number, loop_size, start_pos=0, start_val=1):
    value = start_val

    for i in range(start_pos, loop_size):
        value *= subject_number
        value %= 20201227
    return value


def find_loop_size(subject_number, tgt_val):
    loop_size = 1
    start_val = 1
    start_pos = 0
    num = transform_number(subject_number, loop_size, start_pos, start_val)

    while num != tgt_val:
        loop_size += 1
        start_pos += 1
        start_val = num
        num = transform_number(subject_number, loop_size, start_pos, start_val)

    return loop_size


def get_encryption_key(door_public_key, card_public_key):
    print('Finding door loop size')
    loop_size_door = find_loop_size(subject_number0, door_public_key)
    print('Finding card loop size')
    loop_size_card = find_loop_size(subject_number0, card_public_key)
    door_encryption_key = transform_number(door_public_key, loop_size_card)
    card_encryption_key = transform_number(card_public_key, loop_size_door)
    assert door_encryption_key == card_encryption_key
    return door_encryption_key


print("Ans: ", get_encryption_key(door_public_key, card_public_key))