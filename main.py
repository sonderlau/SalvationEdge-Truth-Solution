from scene import Scene
from enums import SHAPES, LOCATION
from itertools import permutations
from solution import solve
from validation import validate

COMBINATION_SHAPES = [SHAPES.SQUARE, SHAPES.SQUARE,
                      SHAPES.CIRCLE, SHAPES.CIRCLE,
                      SHAPES.TRIANGLE, SHAPES.TRIANGLE]

HAND_SHAPES = [SHAPES.SQUARE, SHAPES.CIRCLE, SHAPES.TRIANGLE]

if "__main__" == __name__:
    cnt = 0
    validated = 0
    achievements = 0
    # 随机生成图案

    # 雕像手中图案
    for shapes in permutations(HAND_SHAPES):
        # 内场图案
        for inside_shapes in permutations(HAND_SHAPES):
            # 外场图案(此处为简便，考虑了每个立体图中2个平面图案的顺序)
            # 实际中，该2个平面图形的顺序不应考虑
            for outside_shapes in permutations(COMBINATION_SHAPES):
                # 组合内场图案
                inside = list(inside_shapes).copy()
                # 从右到左，插入雕像手中的图案
                # PS: 内场每个人阴影图案至少有一个和自己的雕像图案一致
                for i in range(2, -1, -1):
                    inside.insert(i, shapes[i])

                # 生成此刻的场景
                scene = Scene(sculpture_hand=list(shapes), inside_shadow=list(inside), outside_3d=list(outside_shapes))
                cnt += 1
                # 求解
                solve(scene)

                # 验证
                flag_inside, flag_outside, flag_duplication = validate(scene)

                if not flag_inside and not flag_outside:
                    validated += 1

                if not flag_inside and not flag_outside and not flag_duplication:
                    achievements += 1

    print(f"组合种类：{cnt}")
    print(f"内外场正确率: {validated / cnt * 100: .2f} %")
    print(f"满足成就率: {achievements / cnt * 100: .2f} %")
