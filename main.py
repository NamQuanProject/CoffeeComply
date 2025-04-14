import ai_service



agent = ai_service.AIAgent(default_agent=True)




response = agent.generate_response("What is this")




print(response)


agent.close()

another_data = agent.generate_response("What is this")

print(another_data)




