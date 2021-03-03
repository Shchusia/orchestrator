"""
Example create Orchestrators
"""
import examples.blocks as blocks
import examples.flows as flows
from orchestrator import Orchestrator

# print(type(flows))
# print(str(Orchestrator.__name__))

orchestrator = Orchestrator(flows, blocks)
orchestrator = Orchestrator([flows.ExampleSecondFlow(), flows.ExampleFirstFlow, ], blocks)
