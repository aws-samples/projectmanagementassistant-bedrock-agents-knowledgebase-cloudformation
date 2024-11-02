import boto3
import random


AGENT_ALIAS_ID = "To be replaced with agent alias ID from CF stack output"
AGENT_ID = "To be replaced with alias ID from CF stack output"
REGION = "To be replaced with region from CF stack output"


# Setup bedrock
bedrock_agent_runtime = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name=REGION,
)


def generate_random_15digit():
    number = ""

    for _ in range(15):
        number += str(secrets.randbelow(9))

    return number

def process_stream(stream):
    try:
        print("Processing stream...")
        tr = stream.get("trace", {}).get("trace", {}).get("preProcessingTrace", {})
        trace = stream.get("trace", {}).get("trace", {}).get("orchestrationTrace", {})

        if trace:
            print("This is a trace")
            modelInvocationInput = trace.get("invocationInput", {}).get(
                "actionGroupInvocationInput", {}
            )
            print("actionGroupInvocationInput")
            print(modelInvocationInput)
            if modelInvocationInput:
                print(
                    f'Looking up in knowledgebase: {modelInvocationInput.get("text", "")}'
                )
            ActionGroupOutput = trace.get("observation", {}).get(
                "actionGroupInvocation", {}
            )
            if ActionGroupOutput:
                retrieved_references = ActionGroupOutput.get(
                    "text", {}
                )
                print("ActionGroupOutput"+retrieved_references)
                
        # Handle 'chunk' data
        if "chunk" in stream:
            print("This is the final answer:")
            text = stream["chunk"]["bytes"].decode("utf-8")
            print(text)
            return text

    except Exception as e:
        print(f"Error processing stream: {e}")
        print(stream)


def get_bedrock_agent_response(query):
    try:
        response = bedrock_agent_runtime.invoke_agent(
            sessionState={
                "sessionAttributes": {},
                "promptSessionAttributes": {},
            },
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=str(generate_random_15digit()),
            endSession=False,
            enableTrace=True,
            inputText=query,
        )

        results = response.get("completion")

        for stream in results:
            final_results = process_stream(stream)

     
        return (final_results)
    except Exception as e:
        print(f"Error processing stream: {e}")
        return(e)


