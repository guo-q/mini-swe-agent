"""Agent implementations for mini-SWE-agent."""

import copy
import importlib

from minisweagent import Agent, Environment, Model

_AGENT_MAPPING = {
    "default": "minisweagent.agents.default.DefaultAgent",
    "interactive": "minisweagent.agents.interactive.InteractiveAgent",
}


# -> type[Agent] 返回的是类，如果是 -> Agent返回的是对象 = Agent()
def get_agent_class(spec: str) -> type[Agent]:
    """
    这里的设计是既支持短短写简称 default/interactive，也支持完整的自定义Agent类路径。后面的spec是默认值，如果传入的是自定义类路径，跟定就get不到，会直接作为默认值返回。
    """
    full_path = _AGENT_MAPPING.get(spec, spec)
    try:
        """
        这是一个常见经典写法，从右开始分割，目的是从 '模块.模块.类名'中分离出 【模块路径】和【类名】
        """
        module_name, class_name = full_path.rsplit(".", 1)
        """
        这里是动态导入一个模块，根据不同的参数，把对应的模块导入到当前代码中
        """
        module = importlib.import_module(module_name)
        """
        这个是动态获取对象中的一个参数，getattr(对象, 属性字符串)，这里是获取到这个模块中的某个类，把这个类返回，这里返回的是类(Type)，并不是实例（这个应该很好理解，这里肯定还没创建对象）
        返回的类型比如是 AgentClass，那AgentClass()就是在创建对象啦，和java里的差不多，就是不需要new这个关键字。
        """
        return getattr(module, class_name)
    except (ValueError, ImportError, AttributeError):
        msg = f"Unknown agent type: {spec} (resolved to {full_path}, available: {_AGENT_MAPPING})"
        raise ValueError(msg)


def get_agent(model: Model, env: Environment, config: dict, *, default_type: str = "") -> Agent:
    config = copy.deepcopy(config)
    """ 从 config 中提取出 agent_class 的值，并把这个 key 从 config 中删掉 """
    agent_class = get_agent_class(config.pop("agent_class", default_type))
    """ 这里是在做Agent类的实例化，就是在new一个对象。**config 是字典解包，变成多个参数传给这个类的构造函数，Python中是__init__函数。 """
    return agent_class(model, env, **config)
