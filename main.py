# estimated migration time as constant
def estimate_migration_time(flag):
    if flag:
        return 1
    else:
        return 0

# estimated latency overhead due to reduced instances
def estimate_node_reduction_latency(n):
    return 1.0 / n

def opt_strategy_gp(trace):
    total_latency_gp = []
    action_gp = []
    for gp_i in trace:
        l_i, a_i = optimal_migration_trigger(gp_i)
        total_latency_gp.append(l_i)
        action_gp.append(a_i)
    total_latency = sum(total_latency_gp)
    return total_latency, action_gp



def main():
    opt_total_latency = float('inf')
    opt_action_gp = [] # len(opt_action_gp) = T, # of grace periods\

    trace = [[('a', 5), ('r', 2), ('a', 1)], [('a', 2), ('a', 3), ('r', 1), ('r', 1)]]

    opt_total_latency, opt_action_gp = opt_strategy_gp(trace)

if __name__ == '__main__':
    main()


def optimal_migration_trigger(gp_i):
    l_i = [] #list of list, latency: len(l_i) = iter i, l_i[j] = the most updated latency for events up to step j at iter j
    a_i = [] #list of list, action of i: len(l_i) = iter i, l_i[j] = the most updated optimal action seq for events up to step j at iter j
    
    for i, e in enumerate(gp_i):
        if i == 0: continue
        if e == "done":
            return l_i, a_i
        if i == 1:
            get valid action space for e
            find optimal action for e at iter i: min(loss(e))
            update l_i
            update a_i
        else:
            retrieve a_i[i-1] from a_i # each a_i is calculated based on a_i[i-1]: pai_star = J(pai_minus_1_star)
            get valid action space for e based on a_i[i-1] # could be a smaller set than original valid set
            find optimal action for e at iter i: min(loss(e))
            update l_i 
            update a_i 