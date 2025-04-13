import json
import os
from typing import Dict, Optional, Any, Tuple
from config import DEFAULT_SAVE_FILE_PATH


class SaveDataHandler:
    def __init__(self, save_file_path: str = DEFAULT_SAVE_FILE_PATH):
        self.save_file_path = save_file_path
        self.game_data: Optional[Dict[str, Any]] = None

    def load_save_file(self) -> Tuple[bool, str]:
        """加载存档文件
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        if not os.path.exists(self.save_file_path):
            return False, f"存档文件未找到: {self.save_file_path}"

        try:
            with open(self.save_file_path, "r", encoding="utf-8") as f:
                self.game_data = json.load(f)

            if (
                not isinstance(self.game_data, dict)
                or "cards" not in self.game_data
                or not isinstance(self.game_data["cards"], list)
            ):
                return False, "存档结构不符合预期 (缺少 'cards' 列表)"

            return True, f"存档加载成功: {self.save_file_path}"

        except json.JSONDecodeError:
            return False, "存档文件格式无效 (非 JSON)"
        except Exception as e:
            return False, f"加载存档时发生未知错误: {e}"

    def find_card(self, search_value: int) -> Tuple[int, Optional[Dict[str, Any]]]:
        """根据UID或ID查找角色卡片
        Args:
            search_value: UID或ID值
        Returns:
            Tuple[int, Optional[Dict]]: (找到的索引, 卡片数据)
        """
        if not self.game_data:
            return -1, None

        # 优先匹配UID
        for i, card in enumerate(self.game_data["cards"]):
            if isinstance(card, dict) and card.get("uid") == search_value:
                return i, card

        # 再尝试匹配ID
        for i, card in enumerate(self.game_data["cards"]):
            if isinstance(card, dict) and card.get("id") == search_value:
                return i, card

        return -1, None

    def save_changes(
        self, card_index: int, attributes: Dict[str, int]
    ) -> Tuple[bool, str]:
        """保存修改到文件
        Args:
            card_index: 要修改的卡片索引
            attributes: 属性名和值的字典
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        if (
            not self.game_data
            or card_index < 0
            or card_index >= len(self.game_data["cards"])
        ):
            return False, "无效的卡片索引"

        card_data = self.game_data["cards"][card_index]
        if "tag" not in card_data or not isinstance(card_data.get("tag"), dict):
            card_data["tag"] = {}

        # 更新属性
        card_data["tag"].update(attributes)

        try:
            # 创建备份
            backup_path = self.save_file_path + ".bak"
            if os.path.exists(self.save_file_path):
                os.replace(self.save_file_path, backup_path)

            # 写入修改后的数据
            with open(self.save_file_path, "w", encoding="utf-8") as f:
                json.dump(self.game_data, f, ensure_ascii=False, separators=(",", ":"))

            return True, "修改已成功保存"

        except Exception as e:
            # 尝试恢复备份
            if os.path.exists(backup_path):
                try:
                    os.replace(backup_path, self.save_file_path)
                    return False, f"保存失败并已恢复备份: {e}"
                except Exception as restore_e:
                    return False, f"保存失败且恢复备份也失败: {restore_e}"
            return False, f"保存失败: {e}"
