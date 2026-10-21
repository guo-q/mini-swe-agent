"""Agent implementations for mini-SWE-agent."""

import copy
import importlib

from minisweagent import Agent, Environment, Model

_AGENT_MAPPING = {
    "default": "minisweagent.agents.default.DefaultAgent",
    "interactive": "minisweagent.agents.interactive.InteractiveAgent",
}


def get_agent_class(spec: str) -> type[Agent]:
    """
    这里的设计是既支持短短写简称 default/interactive，也支持完整的自定义Agent类路径。后面的spec是默认值，如果传入的是自定义类路径，跟定就get不到，会直接作为默认值返回。
    """
    full_path = _AGENT_MAPPING.get(spec, spec)
    try:
        module_name, class_name = full_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ValueError, ImportError, AttributeError):
        msg = f"Unknown agent type: {spec} (resolved to {full_path}, available: {_AGENT_MAPPING})"
        raise ValueError(msg)


def get_agent(model: Model, env: Environment, config: dict, *, default_type: str = "") -> Agent:
    config = copy.deepcopy(config)
    agent_class = get_agent_class(config.pop("agent_class", default_type))
    return agent_class(model, env, **config)
