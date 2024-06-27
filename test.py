from enums import SHAPES, INTERACTION_TYPE
from scene import Scene
from solution import solve
from validation import validate

sculpture = [SHAPES.TRIANGLE, SHAPES.CIRCLE, SHAPES.SQUARE]

inside = [SHAPES.TRIANGLE, SHAPES.CIRCLE, SHAPES.SQUARE]

# 从右到左，插入雕像手中的图案
# PS: 内场每个人阴影图案至少有一个和自己的雕像图案一致
for i in range(2, -1, -1):
    inside.insert(i, sculpture[i])

# print(inside)

outside = [SHAPES.CIRCLE, SHAPES.SQUARE,
           SHAPES.TRIANGLE, SHAPES.TRIANGLE,
           SHAPES.CIRCLE, SHAPES.SQUARE]

sc = Scene(sculpture_hand=sculpture, inside_shadow=inside, outside_3d=outside)

solve(sc)


flag_inside, flag_outside, flag_duplication = validate(sc)

sc.print_table(print_validation_result=True, print_intermediate_result=False)