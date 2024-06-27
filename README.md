# 《命运2》救赎的边缘突袭第四关：真理 - 机制与解的分析实验代码

> 本仓库使用了 `lfs` 来保存 pdf 文件

> 本仓库的代码在 `python == 3.10, rich ==13.7.1` 上测试通过 



## 项目结构

```
    .
    ├── README.md					# 本文档
    ├── doc.pdf						# 本文的 PDF 版本
    ├── enums.py					# 常量
    ├── main.py						# 随机生成，并测试
    ├── solution.py				    # 本文的求解方法
    ├── test.py						# 某一个情况的求解，并输出求解过程
    ├── scene.py					# 某个情况下的包装类
    └── validation.py			    # 校验函数

```





## 结果复现

文章的实验结果浮现，请直接运行 `main.py`，即可看到输出结果：

```
组合种类：25920
内外场正确率:  100.00 %
满足成就率:  100.00 %
```



## 输出结果

需要安装第三方库用于输出表格格式：

```bash
pip install rich
```



之后运行 `test.py` 即可看到对应情况下的求解结果。



`print_table()` 函数中有两个可选参数：

- `print_validation_result` 是否输出验证的结果
- `print_intermediate_result` 是否在每步后输出内外场结果。





```
                  交互顺序表                  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃        -        ┃ 左雕像 ┃ 中雕像 ┃ 右雕像 ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│    雕像手中     │   🔺   │   🟢   │   🟨   │
├─────────────────┼────────┼────────┼────────┤
│    内场图形     │ 🔺  🔺 │ 🟢  🟢 │ 🟨  🟨 │
├─────────────────┼────────┼────────┼────────┤
│ 内场_左雕像交出 │   ➖   │   🔺   │   ➖   │
│ 内场_左雕像交出 │   ➖   │   ➖   │   🔺   │
│ 内场_中雕像交出 │   🟢   │   ➖   │   ➖   │
│ 内场_中雕像交出 │   ➖   │   ➖   │   🟢   │
│ 内场_右雕像交出 │   🟨   │   ➖   │   ➖   │
│ 内场_右雕像交出 │   ➖   │   🟨   │   ➖   │
├─────────────────┼────────┼────────┼────────┤
│  内场阴影结果   │ 🟢  🟨 │ 🔺  🟨 │ 🔺  🟢 │
├─────────────────┼────────┼────────┼────────┤
│    外场图形     │ 🟢  🟨 │ 🔺  🔺 │ 🟢  🟨 │
├─────────────────┼────────┼────────┼────────┤
│   第 1 轮选中   │   ➖   │ 2 / 🔺 │ 1 / 🟨 │
├─────────────────┼────────┼────────┼────────┤
│ 外场立体图结果  │ 🟢  🟨 │ 🟨  🔺 │ 🟢  🔺 │
└─────────────────┴────────┴────────┴────────┘
             校验结果             
┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ 内场阴影 ┃ 外场组合 ┃ 满足成就 ┃
┡━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ ✅       │ ✅       │ ✅       │
└──────────┴──────────┴──────────┘
```



## 求解函数

参考 `solution.py` 文件。求解的顺序和文章所提一致，满足优先级(左到右)和成就约束。

也可以参考本文所写的方法，实现你自己的求解函数，并使用本文提供的测试方法进行测试，得到最终结果。
