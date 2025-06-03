import os
import requests
import duckdb
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# 加载环境变量
load_dotenv('/Users/zihao_/Documents/github/GLM/.env')

# 定义模型
model = ChatOpenAI(
    model='glm-4-flash',
    api_key=os.getenv('glm4_AI_KEY'),
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
)

# 搜索工具 - 基于智谱AI的Web搜索API
@tool
def web_search(query: str) -> str:
    """
    使用智谱AI的Web搜索功能搜索互联网信息
    
    Args:
        query: 搜索查询字符串
    
    Returns:
        搜索结果的文本内容
    """
    try:
        # 使用智谱AI的Web搜索API
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.getenv('glm4_AI_KEY'),
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        
        # 使用带有web_search工具的模型
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role": "user",
                    "content": f"请搜索并总结关于'{query}'的最新信息"
                }
            ],
            tools=[
                {
                    "type": "web_search",
                    "web_search": {
                        "enable": True
                    }
                }
            ],
            tool_choice="auto"
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"搜索失败: {str(e)}"

# 数据库查询工具
@tool
def query_database(sql_query: str) -> str:
    """
    查询DuckDB数据库
    
    Args:
        sql_query: SQL查询语句
    
    Returns:
        查询结果的字符串表示
    """
    try:
        # 连接到DuckDB数据库
        conn = duckdb.connect('/Users/zihao_/Documents/github/GLM/data/central_analytics.duckdb')
        
        # 执行查询
        result = conn.execute(sql_query).fetchall()
        
        # 获取列名
        columns = [desc[0] for desc in conn.description]
        
        # 格式化结果
        if not result:
            return "查询结果为空"
        
        # 构建结果字符串
        result_str = "查询结果:\n"
        result_str += " | ".join(columns) + "\n"
        result_str += "-" * (len(" | ".join(columns))) + "\n"
        
        for row in result[:10]:  # 限制显示前10行
            result_str += " | ".join(str(cell) for cell in row) + "\n"
        
        if len(result) > 10:
            result_str += f"... (共{len(result)}行，仅显示前10行)\n"
        
        conn.close()
        return result_str
    
    except Exception as e:
        return f"数据库查询失败: {str(e)}"

# 创建工具列表
tools = [web_search, query_database]

# 创建Agent
agent = create_react_agent(model, tools)

def main():
    print("Agent已启动！你可以问我任何问题，我会根据需要使用搜索或数据库查询工具。")
    print("输入 'quit' 退出程序\n")
    
    while True:
        user_input = input("请输入你的问题: ")
        
        if user_input.lower() == 'quit':
            print("再见！")
            break
        
        try:
            # 使用Agent处理用户输入
            response = agent.invoke({
                'messages': [HumanMessage(content=user_input)]
            })
            
            # 获取最后一条消息（Agent的回复）
            last_message = response['messages'][-1]
            print(f"\nAgent回复: {last_message.content}\n")
            
        except Exception as e:
            print(f"处理请求时出错: {str(e)}\n")

if __name__ == "__main__":
    main()
