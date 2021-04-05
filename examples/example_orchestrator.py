"""
Example create Orchestrators
"""
import examples.blocks as blocks
import examples.flows as flows
from service_orchestrator import Orchestrator

orchestrator_1 = Orchestrator(flows, blocks)
orchestrator_2 = Orchestrator([flows.ExampleSecondFlow(), flows.ExampleFirstFlow, ], blocks)
