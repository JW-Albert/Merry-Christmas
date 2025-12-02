import os
import time
import random
import re
import shutil
from typing import List, Tuple
from datetime import datetime, timedelta

# --- Configuration Constants ---

# 巨型樹的尺寸調整 (再次加大)
HEIGHT = 60
WIDTH = 120

# The total number of lines the tree structure occupies (Star + Branches + Trunk)
TOTAL_TREE_BODY_LINES = 1 + (HEIGHT // 2) + 5

# 動畫更新率（FPS）
ANIMATION_FPS = 30  # 30 FPS 提供流暢的動畫效果
FRAME_TIME = 1.0 / ANIMATION_FPS  # 每幀時間（約 0.033 秒）

# Colors (ANSI escape codes)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[34m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"
ORANGE = "\033[38;5;208m"
GOLD = "\033[38;5;220m"
PINK = "\033[38;5;200m"
BROWN = "\033[38;5;94m"  # ANSI 256 color code for Brown

# 所有會閃爍的燈泡顏色
ALL_COLORS = [RED, YELLOW, BLUE, CYAN, MAGENTA, ORANGE, GOLD, PINK]

# ANSI 清屏序列（避免使用系統命令造成的閃爍）
CLEAR_SCREEN = "\033[2J"  # 清除整個畫面
CURSOR_HOME = "\033[H"  # 將游標移到左上角


# --- Utility Functions ---


def strip_ansi(s: str) -> str:
    """Removes ANSI escape codes from a string (for accurate width calculation)."""
    return re.sub(r"\033\[.*?m", "", s)


def get_terminal_size() -> Tuple[int, int]:
    """獲取終端機的寬度和高度。"""
    try:
        size = shutil.get_terminal_size()
        return (size.columns, size.lines)
    except:
        # 如果無法獲取，使用預設值
        return (120, 30)


def get_countdown() -> Tuple[str, timedelta]:
    """
    Calculates the time remaining until December 25th of the current year (or next year).
    Returns a formatted string (Days:Hours:Minutes:Seconds) and the delta for time control.
    """
    now = datetime.now()
    # Target is 00:00:00 on December 25th of the current year
    target_date = datetime(now.year, 12, 25, 0, 0, 0)

    # If 12/25 has passed, target next year's 12/25
    if now > target_date:
        target_date = datetime(now.year + 1, 12, 25, 0, 0, 0)

    time_remaining = target_date - now

    if time_remaining.total_seconds() <= 0:
        # 英文提示
        return (f"{RED}MERRY CHRISTMAS!{RESET}", timedelta(seconds=1))

    # Calculate days, hours, minutes, seconds
    days = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    seconds = time_remaining.seconds % 60

    # 英文格式：Days:Hrs:Mins:Secs
    countdown_str = f"COUNTDOWN to Dec 25th, {target_date.year}: {days:02} Days {hours:02} Hrs {minutes:02} Mins {seconds:02} Secs"

    return (countdown_str, time_remaining)


def _get_tree_line_content(line_idx: int, terminal_width: int) -> str:
    """
    Generates the tree content (Star, Branch, or Trunk) for a given line index.
    使用終端機寬度來置中內容。
    """

    # 0: Star
    if line_idx == 0:
        content = YELLOW + "★" + RESET
        content_width = len(strip_ansi(content))
        padding_left = (terminal_width - content_width) // 2
        return " " * padding_left + content

    # 1 to TOTAL_TREE_BODY_LINES - 6: Branches
    elif line_idx >= 1 and line_idx <= TOTAL_TREE_BODY_LINES - 6:
        i = (line_idx - 1) * 2 + 1
        branch_width = min(i * 2 + 1, terminal_width)

        branch = ""
        for _ in range(branch_width):
            if random.random() < 0.1:  # Light flicker (0.1 density)
                branch += random.choice(ALL_COLORS) + "●" + GREEN
            else:
                branch += "▲"

        content_width = branch_width
        padding_left = (terminal_width - content_width) // 2
        return " " * padding_left + GREEN + branch + RESET

    # TOTAL_TREE_BODY_LINES - 5 to TOTAL_TREE_BODY_LINES - 1: Trunk
    elif line_idx >= TOTAL_TREE_BODY_LINES - 5 and line_idx < TOTAL_TREE_BODY_LINES:
        trunk_width = HEIGHT // 8

        # 樹幹顏色為木頭色 (BROWN)
        content = BROWN + "█" * trunk_width + RESET

        content_width = trunk_width
        padding_left = (terminal_width - content_width) // 2
        return " " * padding_left + content

    return ""  # Fallback to empty line


def draw_tree(countdown_str: str):
    """Draws the large shining Christmas tree and the countdown timer."""

    # 獲取終端機尺寸
    terminal_width, terminal_height = get_terminal_size()

    # 使用 ANSI 序列清屏（避免閃爍）
    print(CLEAR_SCREEN + CURSOR_HOME, end="")

    # 計算總內容高度（樹 + 訊息 + 倒數計時器 + 空白行）
    total_content_lines = TOTAL_TREE_BODY_LINES + 4  # 樹 + 訊息行 + 倒數行 + 額外空白

    # 計算垂直置中的空白行數
    vertical_padding = max(0, (terminal_height - total_content_lines) // 2)

    # 使用雙緩衝：先構建所有內容，然後一次性輸出
    output_lines = []

    # 頂部空白行（垂直置中）
    for _ in range(vertical_padding):
        output_lines.append("")

    # 繪製樹的每一行
    for line_idx in range(TOTAL_TREE_BODY_LINES):
        tree_line = _get_tree_line_content(line_idx, terminal_width)
        output_lines.append(tree_line)

    # 繪製底部訊息 (英文)
    message_content = "MERRY CHRISTMAS!"
    message_padding = " " * ((terminal_width - len(message_content)) // 2)
    output_lines.append("")
    output_lines.append(f"{message_padding}{RED}{message_content}{RESET}")

    # 繪製倒數計時器
    countdown_width = len(strip_ansi(countdown_str))
    countdown_padding = " " * ((terminal_width - countdown_width) // 2)
    output_lines.append("")
    output_lines.append(f"{countdown_padding}{YELLOW}{countdown_str}{RESET}")

    # 底部空白行（垂直置中）
    for _ in range(vertical_padding):
        output_lines.append("")

    # 一次性輸出所有內容（避免閃爍）
    print("\n".join(output_lines), end="", flush=True)


# --- Main Animation Loop ---


def animate():
    """Animates the shining tree and updates the countdown continuously."""

    # 程式啟動提示 (英文)
    print("Drawing Giant Christmas Tree with Countdown. Press Ctrl+C to stop...")

    try:
        while True:
            # 1. 計算倒數時間
            countdown_str, time_remaining = get_countdown()

            # 2. 繪製（每次循環都繪製，讓燈泡閃爍更流暢）
            draw_tree(countdown_str)

            # 3. 使用固定高更新率（30 FPS）來減少閃爍
            time.sleep(FRAME_TIME)

    except KeyboardInterrupt:
        # 程式停止提示 (英文)
        print("\nAnimation stopped. Merry Christmas!")


if __name__ == "__main__":
    animate()
