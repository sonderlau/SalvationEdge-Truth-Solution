from enums import SHAPES, LOCATION
from utils import Scene

LOCATIONS = {0, 1, 2}

def solve(scene: Scene):

    sculpture_hand, inside_shadow, outside_3d = scene.get_shapes()

    # 内场最后交互的位置
    inside_last = None

    # 判断内场持有相同形状的个数
    cnt = 0

    for i in len(inside_shadow):
        shapes_hold = inside_shadow[i]

        if shapes_hold[0] == shapes_hold[1]:
            cnt += 1

    if cnt == 0:
        # 0 个雕像图案相同
        target_index = []
        # 分别找到每个玩家的目标雕像
        for i in len(sculpture_hand):
            shapes_hold = inside_shadow[i]

            # 找到目标雕像的位置
            for j in len(sculpture_hand):
                target_hold = sculpture_hand[j]

                if target_hold != shapes_hold[0] and target_hold != shapes_hold[1]:
                    target_index.append(LOCATION[target_hold])
                    break

        inside_shadow_origin = inside_shadow.copy()

        # 分成两次交换
        for i in range(2):
            # 左边的玩家交换
            scene.register(location_from=LOCATION.LEFT, location_to=target_index[0], shape=inside_shadow_origin[0][i])
            # 中间的玩家交换
            scene.register(location_from=LOCATION.MIDDLE, location_to=target_index[1], shape=inside_shadow_origin[1][i])
            # 右边的玩家交换
            scene.register(location_from=LOCATION.RIGHT, location_to=target_index[2], shape=inside_shadow_origin[2][i])

        inside_last = target_index[2]
    else:
        # 1 / 3 个雕像图案相同

        # 左 中 右
        for i in len(sculpture_hand):
            shapes_hold = inside_shadow[i].copy()

            # 另外两个位置的雕像索引
            loc_1, loc_2 = list(LOCATIONS - {i})

            if shapes_hold[0] != sculpture_hand[loc_1] and shapes_hold[1] != sculpture_hand[loc_2]:
                # 顺序登记
                pass
            else:
                # 倒序登记
                loc_1, loc_2 = loc_2, loc_1

            if loc_1 > loc_2:
                # 按照优先级，应当先交序号小的
                # 若不满足优先级，则交换位置后再进行交付
                loc_1, loc_2 = loc_2, loc_1
                shapes_hold[0], shapes_hold[1] = shapes_hold[1], shapes_hold[0]

            scene.register(location_from=LOCATION[i], location_to=LOCATION[loc_1], shape=shapes_hold[0])
            scene.register(location_from=LOCATION[i], location_to=LOCATION[loc_2], shape=shapes_hold[1])

            inside_last = LOCATION[loc_2]

    # 外场的操作

    shape_selection = [SHAPES.CIRCLE, SHAPES.SQUARE, SHAPES.TRIANGLE]
    current_selection = []
    shape_selection_origin = shape_selection.copy()

    for _ in range(2):
        for i in len(sculpture_hand):
            shape_hold = sculpture_hand[i]

            if len(shape_selection) == 0:
                # 一轮三个图案全选过了
                # 刷新三个图案
                shape_selection = shape_selection_origin.copy()

            if shape_hold in outside_3d[i] and shape_hold in shape_selection:
                # 雕像不需要的图案
                current_selection.append((i, shape_hold))
                del shape_selection[shape_selection.index(shape_hold)]
                continue

            if outside_3d[i][0] == outside_3d[i][1] and outside_3d[i][0] in shape_selection:
                # 3D图案相同
                current_selection.append((i, outside_3d[i][0]))
                del shape_selection[shape_selection.index(outside_3d[i][0])]
                continue


