from enums import SHAPES, LOCATION, INTERACTION_TYPE
from validation import validate,validate_states
from copy import deepcopy


class Scene:
    """
    每个场景生成
    """

    def __init__(self, sculpture_hand: list[SHAPES], inside_shadow: list[SHAPES], outside_3d: list[SHAPES]):
        """
        内外场的初始形状
        """

        # 检查状态是否合法
        validate_states(sculpture_hand, inside_shadow, outside_3d)

        self.sculpture_hand = tuple(sculpture_hand)

        self.inside_shadow_origin = [inside_shadow[0:2], inside_shadow[2:4], inside_shadow[4:6]]
        self.inside_shadow = [inside_shadow[0:2], inside_shadow[2:4], inside_shadow[4:6]]

        self.outside_3d_origin = [outside_3d[0:2], outside_3d[2:4], outside_3d[4:6]]
        self.outside_3d = [outside_3d[0:2], outside_3d[2:4], outside_3d[4:6]]

        self.log_interact_target = []
        self.log_states = []

    def get_sculpture_hand_shapes(self):
        """
        获取当前场景的雕像手中的形状
        """
        return self.sculpture_hand

    def get_shapes(self):
        """
        获取当前场景的形状
        返回：内场的阴影形状，外场的3D形状
        """
        return self.inside_shadow, self.outside_3d

    def register(self, location_from: LOCATION, location_to: LOCATION, shape: SHAPES):
        """
        内场的登记
        location_from: 从哪个位置
        location_to: 到哪个位置
        shape: 形状
        """

        start_location = self.inside_shadow[location_from.value]
        target_location = self.inside_shadow[location_to.value]

        self.validate_existence(start_location, shape)

        start_index = start_location.index(shape)

        target_location.append(start_location.pop(start_index))

        self.inside_shadow[location_from.value] = start_location
        self.inside_shadow[location_to.value] = target_location

        self.log(location_first=location_from, shape_first=shape, location_second=location_to)

        return

    def exchange(self, location_first: LOCATION, location_second: LOCATION, shape_first: SHAPES, shape_second: SHAPES):
        """
        外场的交换图形操作
        location_first: 第一个位置
        location_second: 第二个位置
        shape_first: 第一个形状
        shape_second: 第二个形状
        """
        first_location = self.outside_3d[location_first.value]
        second_location = self.outside_3d[location_second.value]

        self.validate_existence(first_location, shape_first)
        self.validate_existence(second_location, shape_second)

        first_index = first_location.index(shape_first)
        second_index = second_location.index(shape_second)

        # 交换图案
        first_location[first_index], second_location[second_index] = second_location[second_index], first_location[
            first_index]

        # 更新图案
        self.outside_3d[location_first.value] = first_location
        self.outside_3d[location_second.value] = second_location

        self.log(location_first=location_first, shape_first=shape_first, location_second=location_second,
                 shape_second=shape_second)

        return

    def validate_existence(self, location: list, shape: SHAPES):
        """
        检查对应位置是否存在某个图形
        """
        flag = False

        for i in location:
            if shape.value == i.value:
                flag = True
                break

        if not flag:
            raise Exception("图案不存在")

    def log(self, location_first: LOCATION, shape_first: SHAPES,
            location_second: LOCATION,
            shape_second: SHAPES = None):
        """
        记录操作
        第二个形状是可选的，若不填则为内场登记
        location_first: 第一个位置
        shape_first: 第一个形状
        location_second: 第二个位置
        shape_second: 第二个形状
        """

        if shape_second is None:
            interaction_type = INTERACTION_TYPE.REGISTER
        else:
            interaction_type = INTERACTION_TYPE.EXCHANGE

        # 内/外场 起始位置 起始形状 目标位置 目标形状
        self.log_interact_target.append((interaction_type, location_first, shape_first, location_second, shape_second))
        # 内场 / 外场
        self.log_states.append((deepcopy(self.inside_shadow), deepcopy(self.outside_3d)))

    def get_logs(self):
        return self.log_interact_target, self.log_states

    def print_table(self, print_intermediate_result: bool = False, print_validation_result: bool = False):
        """
        使用 rich.table 输出交互结果
        """

        try:
            from rich.console import Console
            from rich.table import Table
        except ModuleNotFoundError:
            raise ModuleNotFoundError("未安装 Rich 库")

        console = Console()
        table = Table(title="交互顺序表")
        table.add_column("-", justify="center")
        table.add_column("左雕像", justify="center")
        table.add_column("中雕像", justify="center")
        table.add_column("右雕像", justify="center")

        table.add_row("雕像手中", to_symbol(self.sculpture_hand[0]), to_symbol(self.sculpture_hand[1]),
                      to_symbol(self.sculpture_hand[2]), end_section=True)

        table.add_row("内场图形", to_symbol(self.inside_shadow_origin[0]), to_symbol(self.inside_shadow_origin[1]),
                      to_symbol(self.inside_shadow_origin[2]), end_section=True)
        outside_round = -1
        for i in range(len(self.log_interact_target)):
            interaction_type, location_first, shape_first, location_second, shape_second = self.log_interact_target[i]
            current_interaction = ["➖", "➖", "➖"]
            if interaction_type == INTERACTION_TYPE.REGISTER:
                current_interaction[location_second.value] = to_symbol(shape_first)

                # 内场
                table.add_row(f"内场_{to_location(location_first)}雕像交出", to_symbol(current_interaction[0]),
                              to_symbol(current_interaction[1]),
                              to_symbol(current_interaction[2]))

                if print_intermediate_result:
                    inside_shape_result, _ = self.log_states[i]
                    table.add_row("内场结果", to_symbol(inside_shape_result[0]), to_symbol(inside_shape_result[1]),
                                  to_symbol(inside_shape_result[2]), end_section=True)

            if interaction_type == INTERACTION_TYPE.EXCHANGE:
                # 外场

                if outside_round == -1:
                    inside_shape_result, outside_shape = self.log_states[i]
                    table.add_section()
                    table.add_row("内场阴影结果", to_symbol(inside_shape_result[0]), to_symbol(inside_shape_result[1]),
                                  to_symbol(inside_shape_result[2]), end_section=True)
                    table.add_row("外场图形", to_symbol(self.outside_3d_origin[0]),
                                  to_symbol(self.outside_3d_origin[1]),
                                  to_symbol(self.outside_3d_origin[2]), end_section=True)
                    outside_round = 1

                # 标注出两次选中的先后
                current_interaction[location_first.value] = "1 / " + to_symbol(shape_first)
                current_interaction[location_second.value] = "2 / " + to_symbol(shape_second)

                table.add_row(f"第 {outside_round} 轮选中", current_interaction[0], current_interaction[1],
                              current_interaction[2])
                outside_round += 1

                if print_intermediate_result:
                    _, outside_shape = self.log_states[i]
                    table.add_row("外场结果", to_symbol(outside_shape[0]), to_symbol(outside_shape[1]),
                                  to_symbol(outside_shape[2]), end_section=True)

                if i == len(self.log_interact_target) - 1:
                    # 最后一个交互
                    # 输出外场的结果

                    _, outside_shape = self.log_states[i]
                    table.add_section()
                    table.add_row("外场立体图结果", to_symbol(outside_shape[0]), to_symbol(outside_shape[1]),
                                  to_symbol(outside_shape[2]), end_section=True)

        console.print(table)

        if print_validation_result:
            # 输出校验的结果
            table_valid = Table(title="校验结果")
            table_valid.add_column("内场阴影")
            table_valid.add_column("外场组合")
            table_valid.add_column("满足成就")

            flag_inside, flag_outside, flag_duplication = validate(self)

            table_valid.add_row("✅" if not flag_inside else "❌", "✅" if not flag_outside else "❌",
                                "✅" if not flag_duplication else "❌")
            console.print(table_valid)


def to_symbol(value):
    if type(value) is list:
        symbols = [to_symbol(i) for i in value]
        return "  ".join(symbols)
    else:
        match value:
            case SHAPES.SQUARE:
                return ":yellow_square:"
            case SHAPES.CIRCLE:
                return ":green_circle:"
            case SHAPES.TRIANGLE:
                return ":red_triangle_pointed_up:"
            case _:
                return value


def to_location(value: LOCATION):
    match value:
        case LOCATION.LEFT:
            return "左"
        case LOCATION.MIDDLE:
            return "中"
        case LOCATION.RIGHT:
            return "右"
        case _:
            return value
