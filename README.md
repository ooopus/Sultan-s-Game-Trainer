# Sultan's Game 存档修改器

这是一个用于修改 Sultan's Game 游戏存档的图形界面工具。通过这个工具，你可以方便地修改游戏中角色的各项属性值。

## 功能特点

- 图形化界面，操作简单直观
- 支持通过 UID 或 ID 查找角色
- 可修改角色的核心属性（体质、魅力、智慧等）

## 安装和使用

### 环境要求

- Python 3.x

### 安装步骤

   ```bash
   git clone https://github.com/ooopus/Sultan-s-Game-Trainer
   cd Sultan-s-Game-Trainer
   python -m venv venv
   # source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install PyQt6
   python main.py
   ```

## 配置说明

在使用前，需要正确配置存档文件路径。配置步骤如下：

1. 复制 `config.py.example` 文件，重命名为 `config.py`
2. 打开 `config.py`，修改 `DEFAULT_SAVE_FILE_PATH` 为你的游戏存档路径
   - Windows 路径示例：`C:\Users\用户名\AppData\LocalLow\DoubleCross\SultansGame\SAVEDATA\一串数字\auto_save.json`
   - 注意：路径中的反斜杠需要使用双反斜杠（\\）或正斜杠（/）

### 核心属性配置

在 `config.py` 中，`CORE_ATTRIBUTES` 列表定义了需要显示的核心属性：
- physique（体质）
- charm（魅力）
- wisdom（智慧）
- social（社交）
- battle（战斗）
- conceal（隐匿）
- survival（生存）
- magic（魔法）

## 项目结构

```
├── main.py          # 程序入口
├── config.py        # 配置文件
├── data_handler.py  # 数据处理模块
└── ui/
    └── main_window.py  # 主窗口界面
```

## 使用说明

1. 启动程序后，界面会显示当前配置的存档路径
2. 点击"加载存档"按钮加载游戏存档
3. 输入角色的 UID 或 ID 进行查找
4. 在属性编辑区域修改需要调整的属性值
5. 修改会自动保存到存档文件

## 注意事项

- 修改存档前建议先备份原存档文件
- 确保游戏未运行时再修改存档
- 修改属性值时注意游戏平衡，过高的属性值可能影响游戏体验