def solution(T):
    path = []
    for i, x in enumerate(T):
    	path += [(i%2, [i])]
    
    m = 0
    while path:
    	new_p = []
    	for p in path:
    		for i, x in enumerate(T):
    			if not (p[0] and i % 2) and x == p[1][-1] and i not in p[1]:
    				n = [p[0] or i % 2, p[1] + [i]]
    				m = max(m, len(n[1]))
    				new_p += [n]
    	path = new_p

    return m




print solution([0, 9, 0, 2, 6, 8, 0, 8, 3, 0])
