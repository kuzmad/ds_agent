from langgraph.types import Command

def run_graph_with_hitl(graph, initial_state: dict, config: dict):
    """Запускает граф и обрабатывает все interrupt() автоматически"""
    
    result = graph.invoke(initial_state, config=config)
    
    while "__interrupt__" in result:
        interrupt_value = result["__interrupt__"][0].value
        
        print(f"\n{interrupt_value['question']}")
        for key, val in interrupt_value.items():
            if key != "question":
                print(f"{key}: {val}")
        
        user_input = input("Ваш ответ: ")
        
        result = graph.invoke(Command(resume=user_input), config=config)
    
    return result