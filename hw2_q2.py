from collections import namedtuple
from enum import Enum
from itertools import batched

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """

    filterd_agents = filter(lambda agent: agent.category != Condition.HEALTHY and agent.category != Condition.DEAD, agent_listing)
    non_participated_agents = filter(lambda agent: agent.category == Condition.HEALTHY or agent.category == Condition.DEAD, agent_listing)
    results = []
    results += list(non_participated_agents)
    
    meetings = batched(filterd_agents, n=2)
    for agents in meetings:
        if len(agents) != 2:
            results.append(agents[0])
            break

        if should_demote(agents[0], agents[1]):
            results.append(Agent(name=agents[1].name, category=Condition(agents[1].category.value + 1)))
        elif should_promote(agents[0], agents[1]):
            results.append(Agent(name=agents[1].name, category=Condition(agents[1].category.value - 1)))
        else:
            results.append(agents[1])

        if should_demote(agents[1], agents[0]):
            results.append(Agent(name=agents[0].name, category=Condition(agents[0].category.value + 1)))
        elif should_promote(agents[1], agents[0]):
            results.append(Agent(name=agents[0].name, category=Condition(agents[0].category.value - 1)))
        else:
            results.append(agents[0])

    return results


def should_demote(agent1, agent2):
    return (agent1.category == Condition.SICK or agent1.category == Condition.DYING) and agent2.category != Condition.CURE


def should_promote(agent1, agent2):
    return agent1.category == Condition.CURE and agent2.category != Condition.CURE

if  __name__ == '__main__':
    # Question 2
    data1 = (Agent("Buddy", Condition.CURE), Agent("Holly", Condition.DEAD))
    return_value = meetup(data1)
    print(f"Question 2 solution: {return_value}")
