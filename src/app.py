import os
import time
import random
import re
from typing import List, Tuple
from datetime import datetime, timedelta

# --- Configuration Constants ---

# 巨型樹的尺寸調整
HEIGHT = 50
WIDTH = 100

# The total number of lines the tree structure occupies (Star + Branches + Trunk)
TOTAL_TREE_BODY_LINES = 1 + (HEIGHT // 2) + 5 

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

# 新增木頭色 (棕色)
BROWN = "\033[38;5;94m" # ANSI 256 color code for Brown

# 所有會閃爍的燈泡顏色
ALL_COLORS = [RED, YELLOW, BLUE, CYAN, MAGENTA, ORANGE, GOLD, PINK]


# --- Utility Functions ---

def strip_ansi(s: str) -> str:
    """Removes ANSI escape codes from a string (for accurate width calculation)."""
    return re.sub(r"\033\[.*?m", "", s)

def get_countdown():
    """
    Calculates the time remaining until December 25th of the current year (or next year).
    Returns a formatted string (天:時:分:秒) and the delta for time control.
    """
    now = datetime.now()
    # 目標設定為當前年份的 12 月 25 日 00:00:00
    target_date = datetime(now.year, 12, 25, 0, 0, 0)
    
    # 如果 12/25 已經過了，則設為下一年的 12/25
    if now > target_date:
        target_date = datetime(now.year + 1, 12, 25, 0, 0, 0)

    time_remaining = target_date - now
    
    if time_remaining.total_seconds() <= 0:
        return (f"{RED}聖誕節到了！{RESET}", timedelta(seconds=1))

    # 計算天、時、分、秒
    days = time_remaining.days
    hours = time_remaining.seconds // 3600
    minutes = (time_remaining.seconds % 3600) // 60
    seconds = time_remaining.seconds % 60
    
    # 倒數計時器的格式：天:時:分:秒
    countdown_str = f"倒數至 {target_date.year} 聖誕節: {days:02}天 {hours:02}時 {minutes:02}分 {seconds:02}秒"
    
    # 返回格式化字串和剩餘的秒數（用於計算下一次更新的時間間隔）
    return (countdown_str, time_remaining)


def _get_tree_line_content(line_idx: int) -> str:
    """
    Generates the tree content (Star, Branch, or Trunk) for a given line index.
    Ensures the *visible* output width is always exactly WIDTH for stable centering.
    """

    # 0: Star
    if line_idx == 0:
        content = YELLOW + "★" + RESET
        content_width = len(strip_ansi(content))
        padding_left = (WIDTH - content_width) // 2
        padding_right = WIDTH - content_width - padding_left
        return " " * padding_left + content + " " * padding_right

    # 1 to TOTAL_TREE_BODY_LINES - 6: Branches
    elif line_idx >= 1 and line_idx <= TOTAL_TREE_BODY_LINES - 6:
        i = (line_idx - 1) * 2 + 1
        branch_width = min(i * 2 + 1, WIDTH)

        branch = ""
        for _ in range(branch_width):
            if random.random() < 0.1:  # 燈泡閃爍
                branch += random.choice(ALL_COLORS) + "●" + GREEN
            else:
                branch += "▲"
        
        content_width = branch_width
        padding_left = (WIDTH - content_width) // 2
        padding_right = WIDTH - content_width - padding_left
        return " " * padding_left + GREEN + branch + RESET + " " * padding_right

    # TOTAL_TREE_BODY_LINES - 5 to TOTAL_TREE_BODY_LINES - 1: Trunk
    elif line_idx >= TOTAL_TREE_BODY_LINES - 5 and line_idx < TOTAL_TREE_BODY_LINES:
        trunk_width = HEIGHT // 8
        
        # ***修正：樹幹顏色改為木頭色 (BROWN)***
        content = BROWN + "█" * trunk_width + RESET
        
        content_width = trunk_width
        padding_left = (WIDTH - content_width) // 2
        padding_right = WIDTH - content_width - padding_left
        return " " * padding_left + content + " " * padding_right

    return " " * WIDTH # Fallback to full width space


def draw_tree(countdown_str: str):
    """Draws the large shining Christmas tree and the countdown timer."""

    # 清空畫面
    os.system("cls" if os.name == "nt" else "clear")
    print()

    # 繪製樹的每一行
    for line_idx in range(TOTAL_TREE_BODY_LINES):
        tree_line = _get_tree_line_content(line_idx)
        print(tree_line)

    # 繪製底部訊息
    message_line_content = (
        "\n" + " " * ((WIDTH - 15) // 2) + RED + "Merry Christmas!" + RESET
    )
    print(message_line_content)
    
    # ***新增：繪製倒數計時器***
    countdown_width = len(strip_ansi(countdown_str))
    countdown_padding = " " * ((WIDTH - countdown_width) // 5 * 2)
    print(f"\n{YELLOW}{countdown_padding}{countdown_str}{RESET}")
    print()


# --- Main Animation Loop ---


def animate():
    """Animates the shining tree and updates the countdown continuously."""
    
    print("正在繪製巨型聖誕樹並啟動倒數計時器，按 Ctrl+C 停止...")

    try:
        while True:
            # 1. 計算倒數時間
            countdown_str, time_remaining = get_countdown()
            
            # 2. 繪製
            draw_tree(countdown_str)

            # 3. 閃爍與計時控制
            
            # 計算到下一秒需要等待多久
            sleep_duration = time_remaining.total_seconds() % 1.0 
            
            # 確保閃爍速度不會太慢 (至少 0.15 秒)
            # 如果剩餘時間很長，則使用 0.15 秒作為閃爍間隔
            sleep_time = min(0.15, max(0.01, sleep_duration))

            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n動畫停止。聖誕快樂！")


if __name__ == "__main__":
    animate()