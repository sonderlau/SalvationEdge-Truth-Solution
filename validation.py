from enums import INTERACTION_TYPE, SHAPES

HAND_SHAPES = [SHAPES.SQUARE, SHAPES.CIRCLE, SHAPES.TRIANGLE]
COMBINATION_SHAPES = [SHAPES.SQUARE, SHAPES.SQUARE,
                      SHAPES.CIRCLE, SHAPES.CIRCLE,
                      SHAPES.TRIANGLE, SHAPES.TRIANGLE]


def validate(scene) -> tuple[bool, bool, bool]:
    """
    验证内外场最终状态是否满足要求
    """

    sculpture_hand = scene.get_sculpture_hand_shapes()
    inside_shadow, outside_3d = scene.get_shapes()

    # 内场消除阴影
    shadow_elimination = [set(), set(), set()]

    # Flags
    flag_inside = False
    flag_outside = False
    flag_duplication = False

    for i in range(len(sculpture_hand)):
        # 手中图案 + 内场图案
        target_inside_shapes = [sculpture_hand[i]] + inside_shadow[i]
        # 手中图案 + 外场图案
        target_outside_shapes = [sculpture_hand[i]] + outside_3d[i]

        shadow_elimination[i].add(sculpture_hand[i])

        # 检查内场
        if len(set(target_inside_shapes)) != 3:
            flag_inside = True

        # 检查外场
        if len(set(target_outside_shapes)) != 3:
            flag_outside = True

    # 检查成就
    target_interactions, _ = scene.get_logs()

    # 检查是否有重复的交互
    check_duplication = []
    # TODO: 记录有重复交互的步骤

    last_location = target_interactions[0][3]
    first_check = True

    for interaction in target_interactions:
        # 内/外场 起始位置 起始形状 目标位置 目标形状
        interaction_type, location_first, shape_first, location_second, shape_second = interaction

        # 检查内场是否是否满足消除了两个图案
        if interaction_type == INTERACTION_TYPE.REGISTER:
            shadow_elimination[location_second.value].add(shape_first)

        if first_check:
            # 第一个交互，不检测
            first_check = False
            continue

        if interaction_type == INTERACTION_TYPE.REGISTER:
            # 内场
            if location_second == last_location:
                check_duplication.append(interaction)
                flag_duplication = True

        else:
            # 外场
            if location_first == last_location:
                check_duplication.append(interaction)
                flag_duplication = True

        last_location = location_second

    return flag_inside, flag_outside, flag_duplication


def validate_states(sculpture_hand: list[SHAPES], inside_shadow: list[SHAPES], outside_3d: list[SHAPES]):
    """

    检查状态是否合法
    """

    # 检查数量
    assert len(sculpture_hand) == 3
    assert len(inside_shadow) == 6
    assert len(outside_3d) == 6

    # 检查内场雕像手中图案是否为每种形状各一个

    assert sorted(sculpture_hand, key=lambda x: x.value) == HAND_SHAPES

    # 检查内场阴影图案是否为每种形状各两个
    assert sorted(inside_shadow, key=lambda x: x.value) == COMBINATION_SHAPES

    # 检查外场3D图案是否为每种形状各两个
    assert sorted(outside_3d, key=lambda x: x.value) == COMBINATION_SHAPES

    return
