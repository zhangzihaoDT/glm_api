# 一个使用智谱的练习项目

## basic_chat

- 使用智谱的chat模型，实现一个简单的对话功能

- 调用项目中的Prompt 形成 langchain 的 Prompttemplate 使用

## agent_tool

- 模型配置 : 使用智谱AI的 glm-4-flash 模型，从 .env 文件加载API密钥
- Web搜索工具 :
----
- 使用智谱AI的Web搜索功能
- 通过 @tool 装饰器定义为LangChain工具
- 支持自然语言查询并返回搜索结果
- 数据库查询工具 :
----
- 连接到指定的DuckDB数据库
- 执行SQL查询并格式化返回结果
- 限制显示结果行数以避免输出过长
- LangGraph Agent :
----
- 使用 create_react_agent 创建ReAct模式的Agent
- 能够根据用户问题自主选择使用哪个工具
- 支持交互式对话
