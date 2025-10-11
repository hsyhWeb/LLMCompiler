# tool_tracker.py

# === 全局配置 ===
ENABLE_LOGGING = False  # 总开关，控制是否记录执行信息
RESOURCE_LIMITED = False  # 是否资源受限，可根据场景设置

# === 数据存储区 ===
tool_logs = []  # 结构: [{'tool': 'llm', 'time': 3.2}, ...]
resource_levels = {
    "level_1": {"delay": 0.0, "count": 1},
    "level_2": {"delay": 1.0, "count": 1},
    "level_3": {"delay": 2.0, "count": 0},  # 没资源示例
}

def get_delay(level: str) -> float:
    """
    根据level返回对应的延迟时间，找不到则返回0
    """
    info = resource_levels.get(level)
    if info:
        return info.get("delay", 0.0)
    return 0.0
# === 功能1: 添加执行记录 ===
def log_tool_execution(tool_name: str, duration: float):
    """
    记录一次工具的执行时间。

    Args:
        tool_name (str): 工具名称
        duration (float): 执行时间（秒）
    """
    if not ENABLE_LOGGING:
        print("[Logging Disabled] 跳过记录")
        return

    tool_logs.append({'tool': tool_name, 'time': duration})
    print(f"[Log] 已记录：{tool_name} 执行了 {duration:.2f} 秒")


# === 功能2: 计算平均执行时间 ===
def average_execution_time(tool_name: str) -> float:
    """
    统计某个工具的平均执行时间。

    Args:
        tool_name (str): 工具名称

    Returns:
        float: 平均时间，若无记录则返回 0.0
    """
    records = [log['time'] for log in tool_logs if log['tool'] == tool_name]
    if not records:
        print(f"[Info] 没有找到工具 '{tool_name}' 的记录")
        return 0.0
    avg = sum(records) / len(records)
    print(f"[Stats] 工具 '{tool_name}' 的平均执行时间为：{avg:.2f} 秒")
    return avg


# === 新功能3: 描述资源等级用于 prompt ===
def describe_resources_for_prompt() -> str:
    """
    返回资源等级之间的优劣顺序描述，包含资源个数（不包含具体延迟数值）。

    Returns:
        str: 用于提示词的资源说明
    """
    lines = ["当前资源从快到慢的顺序如下："]
    # 按延迟升序排序
    sorted_levels = sorted(resource_levels.items(), key=lambda x: x[1]["delay"])
    for i, (level, info) in enumerate(sorted_levels):
        count = info.get("count", 0)
        suffix = ""
        if i == 0:
            suffix = "（最快）"
        elif i == len(sorted_levels) - 1:
            suffix = "（最慢）"
        lines.append(f"- {level}，资源数：{count} {suffix}")
    return "\n".join(lines)
def describe_average_tool_times() -> str:
    """
    输出当前所有工具的平均执行时间描述。

    Returns:
        str: 格式化的平均执行时间描述
    """
    if not tool_logs:
        return "当前暂无任何工具执行记录。"

    # 统计所有工具名称（去重）
    tool_names = set(log['tool'] for log in tool_logs)
    lines = ["已记录工具的平均执行时间如下："]
    for tool_name in sorted(tool_names):
        avg_time = average_execution_time(tool_name)
        lines.append(f"- {tool_name}：平均执行时间 {avg_time:.2f} 秒")
    return "\n".join(lines)
