### Pakages
```
pip install python-dotenv
pip install requests

pip install langchain
pip install langchainhub
pip install langchain_openai
```
### Langchain documentation
***https://python.langchain.com/***
### Source of events API
***https://seatgeek.com/***
##### Their documentation
*https://platform.seatgeek.com/*

### Concepts

The core idea of agents is to use a language model to choose 
a sequence of actions to take. In chains, a sequence of actions
is hardcoded (in code). In agents, a language model is used
as a reasoning engine to determine which actions to take and in
which order.

There are several key components here:

__Schema__

LangChain has several abstractions to make working with agents easy.

__Agent__

This is the chain responsible for deciding what step to take
next. This is usually powered by a language model, a prompt,
and an output parser.

Different agents have different prompting styles for reasoning,
different ways of encoding inputs, and different ways of
parsing the output. For a full list of built-in agents 
see agent types. You can also easily build custom agents,
should you need further control.

______

The core idea of agents is to use a language model to
choose a sequence of actions to take.
In chains, a sequence of actions is hardcoded (in code).
In agents, a language model is used as a reasoning engine
to determine which actions to take and in which order.

__AgentExecutor__

The agent executor is the runtime for an agent.
This is what actually calls the agent, executes the actions 
it chooses, passes the action outputs back to the agent,
and repeats. In pseudocode, this looks roughly like:
```
next_action = agent.get_action(...)
while next_action != AgentFinish:
    observation = run(next_action)
    next_action = agent.get_action(..., next_action, observation)
return next_action
```

While this may seem simple, there are several complexities
this runtime handles for you, including:

1. Handling cases where the agent selects a non-existent tool
2. Handling cases where the tool errors
3. Handling cases where the agent produces output that cannot be parsed into a tool invocation
4. Logging and observability at all levels (agent decisions, tool calls) to stdout and/or to LangSmith.

__Tools__

Tools are functions that an agent can invoke.
The Tool abstraction consists of two components:

1. The input schema for the tool. This tells the LLM what parameters are needed to call the tool. Without this, it will not know what the correct inputs are. These parameters should be sensibly named and described.
2. The function to run. This is generally just a Python function that is invoked.

________

Agents are only as good as the tools they have. 

Tools are interfaces that an agent, chain,
or LLM can use to interact with the world.
They combine a few things:

1. The name of the tool
2. A description of what the tool is
3. JSON schema of what the inputs to the tool are
4. The function to call
5. Whether the result of a tool should be returned directly to the user

It is useful to have all this information
because this information can be used to build action-taking 
systems! The name, description, and JSON schema can be used to
prompt the LLM so it knows how to specify what action to take,
and then the function to call is equivalent to taking that action.

The simpler the input to a tool is, the easier it is for an LLM
to be able to use it. Many agents will only work with tools
that have a single string input. For a list of agent types
and which ones work with more complicated inputs,
please see this documentation

Importantly, the name, description, and JSON schema (if used)
are all used in the prompt. Therefore, it is really important 
that they are clear and describe exactly how the tool should be
used. You may need to change the default name, description,
or JSON schema if the LLM is not understanding how to use 
the tool.

__Considerations__

There are two important design considerations around tools:

1. Giving the agent access to the right tools
2. Describing the tools in a way that is most helpful to the agent

Without thinking through both,
you won't be able to build a working agent.
If you don't give the agent access to a correct set of tools,
it will never be able to accomplish the objectives you give it.
If you don't describe the tools well, the agent won't know
how to use them properly.

LangChain provides a wide set of built-in tools,
but also makes it easy to define your own 
(including custom descriptions). For a full list of built-in
tools, see the tools integrations section.