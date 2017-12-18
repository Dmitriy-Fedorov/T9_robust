from Desk import T9Desk


env = T9Desk()

'''
print(env.state())
print(type(env.state()[1]))
print(type(env.desk['p1']))
print(type(env.desk['p1'][1]))
print(env.get_action_space())
# print(env.score['p1'])
print(env.get_dest_cell(1))
print(env.get_dest_cell(2))

print(-2//9)
a = env.state()
a[7:10] += 1
print(a)
'''
print(0//9)
env.desk['p1'][0] = 18
env.render()
env.move(1)
env.render()
# env.move(3)
# env.render()
